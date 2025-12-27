"""
测试配置模块
"""

import pytest
from github_agent.config import LLMConfig, GitHubConfig, AgentConfig, Constants


def test_llm_config_defaults():
    """测试 LLM 配置默认值"""
    config = LLMConfig()
    assert config.provider == "deepseek"
    assert config.temperature == 0.3
    assert config.timeout == 30


def test_llm_config_api_url():
    """测试 API URL 获取"""
    config = LLMConfig(provider="deepseek")
    assert "deepseek.com" in config.api_url
    
    config = LLMConfig(provider="openai")
    assert "openai.com" in config.api_url


def test_llm_config_default_model():
    """测试默认模型获取"""
    config = LLMConfig(provider="deepseek")
    assert config.default_model == "deepseek-chat"
    
    config = LLMConfig(provider="openai")
    assert config.default_model == "gpt-4o-mini"


def test_llm_config_env_var_name():
    """测试环境变量名获取"""
    config = LLMConfig(provider="deepseek")
    assert config.get_env_var_name() == "DEEPSEEK_API_KEY"
    
    config = LLMConfig(provider="openai")
    assert config.get_env_var_name() == "OPENAI_API_KEY"


def test_github_config_defaults():
    """测试 GitHub 配置默认值"""
    config = GitHubConfig()
    assert config.api_base_url == "https://api.github.com"
    assert config.min_stars == 100
    assert config.max_results == 100


def test_agent_config_from_env():
    """测试从环境变量创建配置"""
    config = AgentConfig.from_env()
    assert config.llm_config is not None
    assert config.github_config is not None


def test_constants():
    """测试常量"""
    assert Constants.DEFAULT_COUNT == 10
    assert Constants.MAX_COUNT == 100
    assert Constants.MIN_STARS == 100
    assert len(Constants.STOP_WORDS) > 0
    assert len(Constants.LANGUAGE_MAP) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

