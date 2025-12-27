#!/usr/bin/env python3
"""
Smart Search Agent - 智能过滤搜索代理
继承基础搜索代理，添加基于 README 的 LLM 智能评分和过滤功能
"""

from typing import List, Dict, Optional
from search_agent import GitHubSearchAgent, GitHubRepo
from smart_filter import SmartFilter


class SmartSearchAgent(GitHubSearchAgent):
    """智能搜索代理 - 带 LLM 评分的搜索"""
    
    def __init__(self, github_token: Optional[str] = None, use_llm: bool = True, 
                 llm_provider: str = "deepseek", llm_api_key: Optional[str] = None):
        """
        初始化智能搜索代理
        
        Args:
            github_token: GitHub Personal Access Token
            use_llm: 必须为 True（智能过滤需要 LLM）
            llm_provider: LLM 提供商
            llm_api_key: LLM API 密钥
        """
        # 调用父类初始化
        super().__init__(github_token, use_llm, llm_provider, llm_api_key)
        
        # 初始化智能过滤器
        self.smart_filter = None
        if self.llm_analyzer:
            try:
                self.smart_filter = SmartFilter(
                    llm_analyzer=self.llm_analyzer,
                    mcp_client=None  # 未来可以集成 MCP
                )
                print(f"🧠 启用智能过滤（基于 README + LLM 评分）")
            except Exception as e:
                print(f"⚠️  智能过滤器初始化失败: {e}")
                self.smart_filter = None
        else:
            print("⚠️  智能过滤需要 LLM，请启用 --llm")
    
    def search_repositories(self, query: str, count: int = 10, sort: str = 'stars',
                           user_query: Optional[str] = None) -> List[GitHubRepo]:
        """
        智能搜索 GitHub 仓库（带 LLM 评分）
        
        Args:
            query: 搜索查询字符串
            count: 返回结果数量
            sort: 排序方式
            user_query: 用户原始查询（用于 LLM 评分）
            
        Returns:
            GitHubRepo 列表（按 AI 相关性排序）
        """
        if not self.smart_filter:
            # 降级到基础搜索
            print("⚠️  智能过滤不可用，使用基础搜索")
            return super().search_repositories(query, count, sort)
        
        # 获取更多初步结果（3倍）用于筛选
        initial_count = count * 3
        
        print(f"🔍 第 1 步：获取 {initial_count} 个候选项目...")
        
        # 调用父类的搜索方法获取初步结果
        initial_repos = super().search_repositories(query, initial_count, sort)
        
        if not initial_repos:
            return []
        
        if not user_query:
            user_query = query
        
        print(f"\n🧠 第 2 步：智能评分和过滤...")
        print(f"   读取每个项目的 README 并用 LLM 评分...")
        
        # 将 GitHubRepo 转换为字典格式（smart_filter 需要）
        repo_dicts = []
        for repo in initial_repos:
            repo_dicts.append({
                'name': repo.name,
                'full_name': repo.full_name,
                'html_url': repo.html_url,
                'description': repo.description,
                'stargazers_count': repo.stars,
                'forks_count': repo.forks,
                'language': repo.language,
                'topics': repo.topics,
                'updated_at': repo.last_updated
            })
        
        # 使用智能过滤器评分和排序
        filtered_dicts = self.smart_filter.filter_and_rank(
            repos=repo_dicts,
            user_query=user_query,
            top_k=count,
            fetch_readme=True
        )
        
        # 转换回 GitHubRepo 对象
        filtered_repos = []
        for item in filtered_dicts:
            repo = GitHubRepo(
                name=item['name'],
                full_name=item['full_name'],
                html_url=item['html_url'],
                description=item.get('description', ''),
                stars=item.get('stargazers_count', item.get('stars', 0)),
                forks=item.get('forks_count', item.get('forks', 0)),
                language=item.get('language'),
                topics=item.get('topics', []),
                last_updated=item.get('updated_at', '')
            )
            # 添加 AI 评分信息
            if 'ai_score' in item:
                setattr(repo, 'ai_score', item['ai_score'])
                setattr(repo, 'ai_reason', item['ai_reason'])
            filtered_repos.append(repo)
        
        print(f"\n✅ 第 3 步：返回最相关的 {len(filtered_repos)} 个项目\n")
        
        return filtered_repos
    
    def display_results(self, repos: List[GitHubRepo]):
        """显示搜索结果（带 AI 评分）"""
        if not repos:
            print("😢 没有找到匹配的仓库")
            return
        
        # 检查是否有 AI 评分
        has_ai_score = any(hasattr(repo, 'ai_score') for repo in repos)
        
        print("=" * 70)
        if has_ai_score:
            print(f"📊 搜索结果 (共 {len(repos)} 个，已按 AI 相关性排序)")
        else:
            print(f"📊 搜索结果 (共 {len(repos)} 个)")
        print("=" * 70)
        
        for i, repo in enumerate(repos, 1):
            print(repo.display(i, show_ai_score=has_ai_score))

