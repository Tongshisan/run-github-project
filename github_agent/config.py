"""
配置管理模块
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class LLMConfig:
    """LLM 配置"""
    provider: str = "deepseek"
    api_key: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.3
    timeout: int = 30
    max_retries: int = 3
    
    @property
    def api_url(self) -> str:
        """获取 API URL"""
        urls = {
            'openai': 'https://api.openai.com/v1/chat/completions',
            'anthropic': 'https://api.anthropic.com/v1/messages',
            'deepseek': 'https://api.deepseek.com/v1/chat/completions',
            'qwen': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
            'glm': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
        }
        return urls.get(self.provider, '')
    
    @property
    def default_model(self) -> str:
        """获取默认模型"""
        models = {
            'openai': 'gpt-4o-mini',
            'anthropic': 'claude-3-5-sonnet-20241022',
            'deepseek': 'deepseek-chat',
            'qwen': 'qwen-turbo',
            'glm': 'glm-4-flash',
        }
        return self.model or models.get(self.provider, '')
    
    @property
    def api_type(self) -> str:
        """获取 API 类型"""
        return 'anthropic' if self.provider == 'anthropic' else 'openai'
    
    def get_env_var_name(self) -> str:
        """获取环境变量名"""
        env_vars = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY',
            'qwen': 'DASHSCOPE_API_KEY',
            'glm': 'GLM_API_KEY',
        }
        return env_vars.get(self.provider, f'{self.provider.upper()}_API_KEY')
    
    def load_api_key(self) -> Optional[str]:
        """从环境变量加载 API key"""
        return self.api_key or os.getenv(self.get_env_var_name())


@dataclass
class GitHubConfig:
    """GitHub 配置"""
    token: Optional[str] = None
    api_base_url: str = "https://api.github.com"
    timeout: int = 10
    min_stars: int = 100
    max_results: int = 100
    
    def load_token(self) -> Optional[str]:
        """从环境变量加载 token"""
        return self.token or os.getenv('GITHUB_TOKEN')


@dataclass
class AgentConfig:
    """Agent 配置"""
    proxy: Optional[str] = None
    use_llm: bool = False
    llm_config: LLMConfig = None
    github_config: GitHubConfig = None
    
    def __post_init__(self):
        if self.llm_config is None:
            self.llm_config = LLMConfig()
        if self.github_config is None:
            self.github_config = GitHubConfig()
    
    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """从环境变量创建配置"""
        return cls(
            proxy=os.getenv('HTTP_PROXY') or os.getenv('HTTPS_PROXY'),
            llm_config=LLMConfig(),
            github_config=GitHubConfig()
        )


# 常量定义
class Constants:
    """常量"""
    DEFAULT_COUNT = 10
    MAX_COUNT = 100
    MIN_STARS = 100
    
    # 停用词
    STOP_WORDS = {
        '找', '个', '的', '库', '项目', '仓库', 
        '相关', '最', '好', '推荐', '帮', '我'
    }
    
    # 语言映射
    LANGUAGE_MAP = {
        'python': ['python', 'py'],
        'javascript': ['javascript', 'js', 'node'],
        'typescript': ['typescript', 'ts'],
        'go': ['go', 'golang'],
        'rust': ['rust'],
        'java': ['java'],
    }
    
    # LLM System Prompt
    SYSTEM_PROMPT = """你是一个 GitHub 项目搜索助手。用户会用自然语言描述他们想找的项目，你需要分析并提取关键信息。

请以 JSON 格式返回分析结果，包含以下字段：
{
  "keywords": ["关键词1"],  // ⚠️ 最多 1-2 个英文技术关键词
  "count": 10,
  "language": "javascript",
  "category": "library",
  "description": "CSS 动画库"
}

⚠️ **关键词提取规则（非常重要！）**：
1. **最多 1-2 个关键词**，GitHub 搜索是 AND 逻辑，关键词越多越搜不到
2. **只用技术术语**，不要用描述性词汇
3. **禁止使用的词**：
   - ❌ graduation（毕业）
   - ❌ university（大学）
   - ❌ study（学习）
   - ❌ practice（练习）
   - ❌ project（项目）- 太通用
   - ❌ website, repository（废话）
   - ❌ example, sample, demo - 除非用户明确要求
   - ❌ interactive, awesome, cool（形容词）

4. **正确的做法**：
   - 用户说"毕业设计" → 忽略这个描述，只提取技术栈
   - 用户说"学习 Vue" → 只用 ["vue"]
   - 用户说"前端项目" → 只用 ["frontend"] 或 设置 language: "javascript"
   - 用户说"React 管理后台" → ["react", "admin"]（2个，已经是上限）

示例（注意关键词极少）：
- "找毕业设计的前端项目" → keywords: ["frontend"] 或 ["starter"], language: "javascript"
- "websocket 库" → keywords: ["websocket"]
- "React 管理后台" → keywords: ["react", "admin"]
- "学习 Vue 的项目" → keywords: ["vue"]
- "Python 爬虫" → keywords: ["crawler"], language: "python"
- "3D 网站" → keywords: ["webgl"] 或 ["threejs"]
- "前端动画" → keywords: ["animation"], language: "javascript"
- "适合毕业设计的 Vue 项目" → keywords: ["vue"], category: "template"

注意：
- ⚠️ **宁可只用 1 个关键词，也不要用 3 个以上**
- 如果用户只说了技术栈（如"前端"），优先用 language 过滤，keywords 可以为空
- 如果用户描述很模糊，就用最核心的技术词，忽略所有修饰"""

