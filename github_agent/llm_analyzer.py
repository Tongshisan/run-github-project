#!/usr/bin/env python3
"""
LLM 查询分析器 - 使用大模型理解自然语言需求
支持 OpenAI 和 Anthropic Claude
"""

import os
import json
from typing import Dict, Optional
import requests


class LLMQueryAnalyzer:
    """使用 LLM 分析用户查询"""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        初始化 LLM 分析器
        
        Args:
            provider: LLM 提供商 ("openai" 或 "anthropic")
            api_key: API 密钥
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.api_url = "https://api.openai.com/v1/chat/completions"
            self.model = "gpt-4o-mini"  # 使用 mini 版本更经济
        elif self.provider == "anthropic":
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            self.api_url = "https://api.anthropic.com/v1/messages"
            self.model = "claude-3-5-sonnet-20241022"
        else:
            raise ValueError(f"不支持的提供商: {provider}")
        
        if not self.api_key:
            raise ValueError(f"请设置 {self.provider.upper()}_API_KEY 环境变量")
    
    def analyze_query(self, user_query: str) -> Dict[str, any]:
        """
        使用 LLM 分析用户查询
        
        Args:
            user_query: 用户的自然语言查询
            
        Returns:
            分析结果字典，包含关键词、数量、语言等信息
        """
        system_prompt = """你是一个 GitHub 项目搜索助手。用户会用自然语言描述他们想找的项目，你需要分析并提取关键信息。

请以 JSON 格式返回分析结果，包含以下字段：
{
  "keywords": ["关键词1", "关键词2"],  // 英文关键词，用于 GitHub 搜索
  "count": 10,  // 用户想要的结果数量，默认 10
  "language": "python",  // 编程语言（如果指定），可选值: python, javascript, typescript, go, rust, java, 等，如果没有指定则为 null
  "category": "library",  // 项目类型: library, framework, tool, template, example, 等
  "description": "CSS 动画库"  // 用一句话描述用户想要什么（中文）
}

注意：
1. keywords 必须是英文，因为 GitHub 主要是英文内容
2. 如果用户说"找 10 个"，count 就是 10
3. language 只在用户明确指定编程语言时才设置
4. 关键词要准确，能找到相关项目"""

        user_prompt = f"用户需求：{user_query}\n\n请分析这个需求并返回 JSON 格式的结果。"
        
        try:
            if self.provider == "openai":
                result = self._call_openai(system_prompt, user_prompt)
            else:
                result = self._call_anthropic(system_prompt, user_prompt)
            
            # 解析 JSON 结果
            analysis = json.loads(result)
            
            # 确保必要字段存在
            if 'keywords' not in analysis:
                analysis['keywords'] = []
            if 'count' not in analysis:
                analysis['count'] = 10
            
            # 限制数量
            analysis['count'] = min(analysis['count'], 100)
            
            # 添加排序信息
            analysis['sort'] = 'stars'
            analysis['order'] = 'desc'
            
            return analysis
            
        except Exception as e:
            print(f"⚠️  LLM 分析失败，使用简单规则分析: {e}")
            # 降级到简单规则
            return self._fallback_analyze(user_query)
    
    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """调用 OpenAI API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            'response_format': {'type': 'json_object'},
            'temperature': 0.3
        }
        
        response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        """调用 Anthropic Claude API"""
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'max_tokens': 1024,
            'system': system_prompt,
            'messages': [
                {'role': 'user', 'content': user_prompt}
            ],
            'temperature': 0.3
        }
        
        response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result['content'][0]['text']
        
        # 提取 JSON（Claude 可能会加一些说明文字）
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '{' in content:
            start = content.index('{')
            end = content.rindex('}') + 1
            content = content[start:end]
        
        return content
    
    def _fallback_analyze(self, user_query: str) -> Dict[str, any]:
        """降级到简单规则分析"""
        query_lower = user_query.lower()
        
        # 提取数量
        count = 10
        for word in user_query.split():
            if word.isdigit():
                count = int(word)
                break
        
        # 提取关键词（简单处理）
        keywords = []
        exclude_words = {'找', '个', '的', '库', '项目', '仓库', '相关', '最', '好', '推荐', '推荐'}
        for word in user_query.replace('，', ' ').replace(',', ' ').split():
            if word and word not in exclude_words and not word.isdigit():
                keywords.append(word)
        
        # 检测语言
        language = None
        language_map = {
            'python': ['python', 'py'],
            'javascript': ['javascript', 'js', 'node'],
            'typescript': ['typescript', 'ts'],
            'go': ['go', 'golang'],
            'rust': ['rust'],
            'java': ['java'],
        }
        
        for lang, lang_keys in language_map.items():
            if any(key in query_lower for key in lang_keys):
                language = lang
                break
        
        return {
            'keywords': keywords,
            'count': min(count, 100),
            'language': language,
            'sort': 'stars',
            'order': 'desc',
            'description': user_query
        }


# 使用示例
if __name__ == "__main__":
    # 测试
    try:
        # 尝试使用 OpenAI
        analyzer = LLMQueryAnalyzer(provider="openai")
        
        test_queries = [
            "找 10 个 CSS 动画库",
            "推荐 Python 机器学习框架",
            "React UI 组件库",
        ]
        
        for query in test_queries:
            print(f"\n查询: {query}")
            result = analyzer.analyze_query(query)
            print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
    except ValueError as e:
        print(f"错误: {e}")
        print("\n提示: 请设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 环境变量")

