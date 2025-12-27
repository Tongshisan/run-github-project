"""
LLM 查询分析器 - 重构版
使用大模型理解自然语言需求
"""

import json
from typing import Dict, Any, Optional
import requests

from .config import LLMConfig, Constants
from .logger import logger
from .exceptions import LLMError, ConfigurationError, ValidationError
from .utils import validate_query


class LLMQueryAnalyzer:
    """使用 LLM 分析用户查询"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        初始化 LLM 分析器
        
        Args:
            config: LLM 配置对象
        
        Raises:
            ConfigurationError: 配置错误时抛出
        """
        self.config = config or LLMConfig()
        
        # 加载 API key
        self.api_key = self.config.load_api_key()
        if not self.api_key:
            env_var = self.config.get_env_var_name()
            raise ConfigurationError(
                f"未设置 API key，请设置环境变量: {env_var}"
            )
        
        logger.info(
            f"初始化 LLM 分析器: {self.config.provider} / {self.config.default_model}"
        )
    
    def analyze_query(self, user_query: str) -> Dict[str, Any]:
        """
        分析用户查询
        
        Args:
            user_query: 用户的自然语言查询
        
        Returns:
            分析结果字典
        
        Raises:
            ValidationError: 查询无效时抛出
            LLMError: LLM 调用失败时抛出
        """
        # 验证查询
        if not validate_query(user_query):
            raise ValidationError("查询不能为空")
        
        logger.debug(f"分析查询: {user_query}")
        
        try:
            # 构建 prompt
            user_prompt = f"用户需求：{user_query}\n\n请分析这个需求并返回 JSON 格式的结果。"
            
            # 调用 LLM
            if self.config.api_type == 'openai':
                result = self._call_openai_compatible(
                    Constants.SYSTEM_PROMPT, 
                    user_prompt
                )
            elif self.config.api_type == 'anthropic':
                result = self._call_anthropic(
                    Constants.SYSTEM_PROMPT, 
                    user_prompt
                )
            else:
                raise LLMError(f"不支持的 API 类型: {self.config.api_type}")
            
            # 解析 JSON
            analysis = self._parse_response(result)
            
            # 验证和规范化结果
            analysis = self._normalize_analysis(analysis)
            
            logger.info(f"分析完成: {len(analysis.get('keywords', []))} 个关键词")
            logger.debug(f"分析结果: {analysis}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            raise LLMError(f"LLM 返回的结果无法解析: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求失败: {e}")
            raise LLMError(f"LLM API 调用失败: {e}")
        except Exception as e:
            logger.error(f"LLM 分析失败: {e}")
            raise LLMError(f"LLM 分析过程出错: {e}")
    
    def _call_openai_compatible(
        self, 
        system_prompt: str, 
        user_prompt: str
    ) -> str:
        """
        调用 OpenAI 兼容的 API
        
        Args:
            system_prompt: 系统提示
            user_prompt: 用户提示
        
        Returns:
            LLM 响应内容
        
        Raises:
            requests.exceptions.RequestException: 请求失败时抛出
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.config.default_model,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            'temperature': self.config.temperature
        }
        
        # 某些模型支持 response_format
        if self.config.provider in ['openai', 'deepseek']:
            data['response_format'] = {'type': 'json_object'}
        
        logger.debug(f"调用 API: {self.config.api_url}")
        
        response = requests.post(
            self.config.api_url, 
            headers=headers, 
            json=data, 
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_anthropic(
        self, 
        system_prompt: str, 
        user_prompt: str
    ) -> str:
        """
        调用 Anthropic Claude API
        
        Args:
            system_prompt: 系统提示
            user_prompt: 用户提示
        
        Returns:
            LLM 响应内容
        
        Raises:
            requests.exceptions.RequestException: 请求失败时抛出
        """
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }
        
        data = {
            'model': self.config.default_model,
            'max_tokens': 1024,
            'system': system_prompt,
            'messages': [
                {'role': 'user', 'content': user_prompt}
            ],
            'temperature': self.config.temperature
        }
        
        logger.debug(f"调用 API: {self.config.api_url}")
        
        response = requests.post(
            self.config.api_url,
            headers=headers,
            json=data,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        result = response.json()
        content = result['content'][0]['text']
        
        # 提取 JSON
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '{' in content:
            start = content.index('{')
            end = content.rindex('}') + 1
            content = content[start:end]
        
        return content
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        解析 LLM 响应
        
        Args:
            response: LLM 响应字符串
        
        Returns:
            解析后的字典
        
        Raises:
            json.JSONDecodeError: JSON 解析失败时抛出
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试清理和重新解析
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            return json.loads(response.strip())
    
    def _normalize_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        规范化分析结果
        
        Args:
            analysis: 原始分析结果
        
        Returns:
            规范化后的结果
        """
        # 确保必要字段存在
        if 'keywords' not in analysis:
            analysis['keywords'] = []
        if 'count' not in analysis:
            analysis['count'] = Constants.DEFAULT_COUNT
        
        # 限制数量
        analysis['count'] = min(analysis['count'], Constants.MAX_COUNT)
        analysis['count'] = max(analysis['count'], 1)
        
        # 添加默认值
        analysis['sort'] = 'stars'
        analysis['order'] = 'desc'
        
        return analysis

