#!/usr/bin/env python3
"""
GitHub Search Agent - 基础搜索代理
负责 GitHub 仓库的搜索和展示
"""

import os
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class GitHubRepo:
    """GitHub 仓库信息"""
    name: str
    full_name: str
    html_url: str
    description: str
    stars: int
    forks: int
    language: str
    topics: List[str]
    last_updated: str
    
    def display(self, index: int, show_ai_score: bool = False) -> str:
        """格式化显示仓库信息"""
        topics_str = ", ".join(self.topics[:5]) if self.topics else "无标签"
        
        result = f"""
{'='*70}
[{index}] {self.full_name}
{'='*70}
⭐ Stars: {self.stars:,} | 🍴 Forks: {self.forks:,} | 📝 语言: {self.language or 'N/A'}
🏷️  标签: {topics_str}
📖 描述: {self.description or '无描述'}"""
        
        # 如果有 AI 评分，显示
        if show_ai_score and hasattr(self, 'ai_score'):
            result += f"\n🧠 AI评分: {self.ai_score}/100 | 💡 {self.ai_reason}"
        
        result += f"\n🔗 链接: {self.html_url}\n"
        
        return result


class GitHubSearchAgent:
    """GitHub 基础搜索代理"""
    
    def __init__(self, github_token: Optional[str] = None, use_llm: bool = False, 
                 llm_provider: str = "deepseek", llm_api_key: Optional[str] = None):
        """
        初始化 GitHub 搜索代理
        
        Args:
            github_token: GitHub Personal Access Token（可选，用于提高 API 限制）
            use_llm: 是否使用 LLM 分析查询
            llm_provider: LLM 提供商
            llm_api_key: LLM API 密钥
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
        
        # LLM 配置
        self.use_llm = use_llm
        self.llm_analyzer = None
        
        if use_llm:
            try:
                from llm_analyzer import LLMQueryAnalyzer
                self.llm_analyzer = LLMQueryAnalyzer(
                    provider=llm_provider,
                    api_key=llm_api_key
                )
                print(f"🤖 使用 {llm_provider.upper()} LLM 分析查询")
            except ImportError:
                print("⚠️  LLM 分析器不可用，使用简单规则分析")
                print("   提示: pip install openai 或 pip install anthropic")
                self.use_llm = False
            except Exception as e:
                print(f"⚠️  LLM 初始化失败: {e}")
                print("   使用简单规则分析")
                self.use_llm = False
    
    def analyze_query(self, user_query: str) -> Dict[str, any]:
        """
        分析用户查询，提取关键信息
        
        如果启用了 LLM，使用大模型分析；否则使用简单规则
        """
        # 使用 LLM 分析
        if self.use_llm and self.llm_analyzer:
            try:
                print("🧠 使用 AI 分析需求...")
                return self.llm_analyzer.analyze_query(user_query)
            except Exception as e:
                print(f"⚠️  AI 分析失败，使用简单规则: {e}")
                return self._simple_analyze(user_query)
        else:
            return self._simple_analyze(user_query)
    
    def _simple_analyze(self, user_query: str) -> Dict[str, any]:
        """
        简单规则分析（降级方案）
        """
        query_lower = user_query.lower()
        
        # 提取数量
        count = 10  # 默认
        for word in user_query.split():
            if word.isdigit():
                count = int(word)
                break
        
        # 提取关键词
        keywords = []
        exclude_words = {'找', '个', '的', '库', '项目', '仓库', '相关', '最', '好', '推荐'}
        for word in user_query.replace('，', ' ').replace(',', ' ').split():
            if word and word not in exclude_words and not word.isdigit():
                keywords.append(word)
        
        # 检测语言偏好
        language = None
        language_keywords = {
            'python': ['python', 'py'],
            'javascript': ['javascript', 'js', 'node'],
            'typescript': ['typescript', 'ts'],
            'go': ['go', 'golang'],
            'rust': ['rust'],
            'java': ['java'],
        }
        
        for lang, lang_keys in language_keywords.items():
            if any(key in query_lower for key in lang_keys):
                language = lang
                break
        
        return {
            'keywords': keywords,
            'count': min(count, 100),  # GitHub API 限制
            'language': language,
            'sort': 'stars',
            'order': 'desc',
            'description': user_query
        }
    
    def build_search_query(self, analysis: Dict[str, any]) -> str:
        """根据分析结果构建 GitHub 搜索查询"""
        query_parts = []
        
        # 添加关键词
        if analysis['keywords']:
            query_parts.append(' '.join(analysis['keywords']))
        
        # 添加语言过滤
        if analysis.get('language'):
            query_parts.append(f"language:{analysis['language']}")
        
        # 添加其他过滤条件
        query_parts.append('stars:>100')  # 至少 100 个 star
        
        return ' '.join(query_parts)
    
    def search_repositories(self, query: str, count: int = 10, sort: str = 'stars') -> List[GitHubRepo]:
        """
        搜索 GitHub 仓库
        
        Args:
            query: 搜索查询字符串
            count: 返回结果数量
            sort: 排序方式 (stars, forks, updated)
            
        Returns:
            GitHubRepo 列表
        """
        url = f"{self.base_url}/search/repositories"
        params = {
            'q': query,
            'sort': sort,
            'order': 'desc',
            'per_page': count
        }
        
        print(f"🔍 搜索中... (查询: {query})")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            total_count = data.get('total_count', 0)
            
            print(f"✅ GitHub API 响应:")
            print(f"   总数: {total_count:,} 个仓库")
            print(f"   返回: {len(data.get('items', []))} 个结果")
            
            if total_count == 0:
                print(f"\n⚠️  没有找到结果！")
                print(f"   搜索查询: {query}")
                print(f"   建议：")
                print(f"   1. 尝试更通用的关键词")
                print(f"   2. 减少过滤条件（如去掉 stars:>100）")
                print(f"   3. 检查关键词拼写")
            print()
            
            repos = []
            for item in data.get('items', [])[:count]:
                repo = GitHubRepo(
                    name=item['name'],
                    full_name=item['full_name'],
                    html_url=item['html_url'],
                    description=item.get('description', ''),
                    stars=item['stargazers_count'],
                    forks=item['forks_count'],
                    language=item.get('language'),
                    topics=item.get('topics', []),
                    last_updated=item['updated_at']
                )
                repos.append(repo)
            
            return repos
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def display_results(self, repos: List[GitHubRepo]):
        """显示搜索结果"""
        if not repos:
            print("😢 没有找到匹配的仓库")
            return
        
        print("=" * 70)
        print(f"📊 搜索结果 (共 {len(repos)} 个)")
        print("=" * 70)
        
        for i, repo in enumerate(repos, 1):
            print(repo.display(i, show_ai_score=False))
    
    def interactive_select(self, repos: List[GitHubRepo]) -> Optional[GitHubRepo]:
        """交互式选择仓库"""
        if not repos:
            return None
        
        print("\n" + "=" * 70)
        print("🎯 请选择要运行的项目")
        print("=" * 70)
        print(f"输入项目编号 (1-{len(repos)}), 或输入 'q' 退出\n")
        
        try:
            choice = input("👉 你的选择: ").strip().lower()
            
            if choice == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(repos):
                return repos[index]
            else:
                print(f"❌ 无效选择，请输入 1-{len(repos)}")
                return None
                
        except (ValueError, KeyboardInterrupt):
            return None

