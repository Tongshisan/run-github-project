"""
异常定义模块
"""


class GitHubAgentError(Exception):
    """Agent 基础异常"""
    pass


class ConfigurationError(GitHubAgentError):
    """配置错误"""
    pass


class LLMError(GitHubAgentError):
    """LLM 相关错误"""
    pass


class GitHubAPIError(GitHubAgentError):
    """GitHub API 错误"""
    pass


class NetworkError(GitHubAgentError):
    """网络错误"""
    pass


class ValidationError(GitHubAgentError):
    """验证错误"""
    pass

