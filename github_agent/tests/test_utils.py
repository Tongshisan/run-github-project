"""
测试工具函数
"""

import pytest
from github_agent.utils import (
    extract_number,
    detect_language,
    clean_keywords,
    validate_query,
    format_count,
    truncate_text
)


def test_extract_number():
    """测试数字提取"""
    assert extract_number("找 10 个项目") == 10
    assert extract_number("推荐 5 个库") == 5
    assert extract_number("没有数字") is None


def test_detect_language():
    """测试语言检测"""
    assert detect_language("Python 项目") == "python"
    assert detect_language("JavaScript 库") == "javascript"
    assert detect_language("Go 语言") == "go"
    assert detect_language("CSS 动画") is None


def test_clean_keywords():
    """测试关键词清理"""
    words = ["找", "CSS", "动画", "库", "10", "a"]
    cleaned = clean_keywords(words)
    assert "CSS" in cleaned
    assert "动画" in cleaned
    assert "找" not in cleaned
    assert "10" not in cleaned
    assert "a" not in cleaned


def test_validate_query():
    """测试查询验证"""
    assert validate_query("找 CSS 库") is True
    assert validate_query("") is False
    assert validate_query("   ") is False
    assert validate_query("a") is False


def test_format_count():
    """测试数字格式化"""
    assert format_count(1000) == "1,000"
    assert format_count(1000000) == "1,000,000"
    assert format_count(100) == "100"


def test_truncate_text():
    """测试文本截断"""
    text = "这是一段很长的文本" * 20
    truncated = truncate_text(text, max_length=50)
    assert len(truncated) <= 50
    assert truncated.endswith("...")
    
    short_text = "短文本"
    assert truncate_text(short_text, max_length=50) == short_text


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

