"""
工具函数模块
"""

import re
from typing import List, Dict, Optional
from .config import Constants


def extract_number(text: str) -> Optional[int]:
    """
    从文本中提取数字
    
    Args:
        text: 输入文本
    
    Returns:
        提取的数字，如果没有则返回 None
    """
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else None


def detect_language(query: str) -> Optional[str]:
    """
    检测查询中的编程语言
    
    Args:
        query: 查询文本
    
    Returns:
        检测到的语言，如果没有则返回 None
    """
    query_lower = query.lower()
    
    for lang, keywords in Constants.LANGUAGE_MAP.items():
        if any(keyword in query_lower for keyword in keywords):
            return lang
    
    return None


def clean_keywords(words: List[str]) -> List[str]:
    """
    清理关键词列表
    
    Args:
        words: 原始关键词列表
    
    Returns:
        清理后的关键词列表
    """
    cleaned = []
    for word in words:
        # 去除停用词
        if word in Constants.STOP_WORDS:
            continue
        # 去除纯数字
        if word.isdigit():
            continue
        # 去除过短的词
        if len(word) < 2:
            continue
        cleaned.append(word)
    
    return cleaned


def validate_query(query: str) -> bool:
    """
    验证查询是否有效
    
    Args:
        query: 查询文本
    
    Returns:
        是否有效
    """
    if not query or not query.strip():
        return False
    
    if len(query.strip()) < 2:
        return False
    
    return True


def format_count(count: int) -> str:
    """
    格式化数字（添加千位分隔符）
    
    Args:
        count: 数字
    
    Returns:
        格式化后的字符串
    """
    return f"{count:,}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀
    
    Returns:
        截断后的文本
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

