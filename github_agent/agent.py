#!/usr/bin/env python3
"""
GitHub AI Agent - 智能 GitHub 项目发现和运行助手
使用自然语言查询 GitHub 项目，自动分析、排序、展示并运行
"""

import sys
import os
import json
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass

# 添加父目录到 Python 路径以导入 run_github_project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run_github_project import GitHubProjectRunner

# 尝试导入 LLM 分析器
try:
    from llm_analyzer import LLMQueryAnalyzer
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


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
    
    def display(self, index: int) -> str:
        """格式化显示仓库信息"""
        topics_str = ", ".join(self.topics[:5]) if self.topics else "无标签"
        return f"""
{'='*70}
[{index}] {self.full_name}
{'='*70}
⭐ Stars: {self.stars:,} | 🍴 Forks: {self.forks:,} | 📝 语言: {self.language or 'N/A'}
🏷️  标签: {topics_str}
📖 描述: {self.description or '无描述'}
🔗 链接: {self.html_url}
"""


class GitHubSearchAgent:
    """GitHub 搜索智能代理"""
    
    def __init__(self, github_token: Optional[str] = None, use_llm: bool = False, 
                 llm_provider: str = "openai", llm_api_key: Optional[str] = None):
        """
        初始化 GitHub 搜索代理
        
        Args:
            github_token: GitHub Personal Access Token（可选，用于提高 API 限制）
            use_llm: 是否使用 LLM 分析查询（需要 API key）
            llm_provider: LLM 提供商 ("openai" 或 "anthropic")
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
            if not LLM_AVAILABLE:
                print("⚠️  LLM 分析器不可用，使用简单规则分析")
                print("   提示: pip install openai 或 pip install anthropic")
                self.use_llm = False
            else:
                try:
                    self.llm_analyzer = LLMQueryAnalyzer(
                        provider=llm_provider,
                        api_key=llm_api_key
                    )
                    print(f"🤖 使用 {llm_provider.upper()} LLM 分析查询")
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
        if analysis['language']:
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
            print(f"✅ 找到 {total_count:,} 个相关仓库\n")
            
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
            print(repo.display(i))
    
    def interactive_select(self, repos: List[GitHubRepo]) -> Optional[GitHubRepo]:
        """交互式选择仓库"""
        if not repos:
            return None
        
        print("\n" + "=" * 70)
        print("🎯 请选择要运行的项目")
        print("=" * 70)
        print("输入项目编号 (1-{}), 或输入 'q' 退出".format(len(repos)))
        
        while True:
            try:
                choice = input("\n👉 你的选择: ").strip().lower()
                
                if choice == 'q':
                    print("👋 再见！")
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(repos):
                    return repos[index]
                else:
                    print(f"❌ 请输入 1-{len(repos)} 之间的数字")
            except ValueError:
                print("❌ 输入无效，请输入数字")
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                return None


class GitHubAgent:
    """GitHub AI Agent 主类"""
    
    def __init__(self, github_token: Optional[str] = None, proxy: Optional[str] = None,
                 use_llm: bool = False, llm_provider: str = "openai", llm_api_key: Optional[str] = None):
        """
        初始化 GitHub Agent
        
        Args:
            github_token: GitHub Token
            proxy: 代理地址
            use_llm: 是否使用 LLM 分析查询
            llm_provider: LLM 提供商 ("openai" 或 "anthropic")
            llm_api_key: LLM API 密钥
        """
        self.search_agent = GitHubSearchAgent(
            github_token=github_token,
            use_llm=use_llm,
            llm_provider=llm_provider,
            llm_api_key=llm_api_key
        )
        self.proxy = proxy
    
    def run_query(self, user_query: str, auto_run: bool = False):
        """
        处理用户查询
        
        Args:
            user_query: 用户的自然语言查询
            auto_run: 是否自动运行第一个项目
        """
        print("=" * 70)
        print("🤖 GitHub AI Agent")
        print("=" * 70)
        print(f"📝 你的需求: {user_query}\n")
        
        # 1. 分析查询
        analysis = self.search_agent.analyze_query(user_query)
        
        if not self.search_agent.use_llm:
            print(f"   关键词: {', '.join(analysis['keywords'])}")
        else:
            print(f"   关键词: {', '.join(analysis['keywords'])}")
            if 'description' in analysis:
                print(f"   理解: {analysis['description']}")
        
        if analysis.get('language'):
            print(f"   语言: {analysis['language']}")
        if analysis.get('category'):
            print(f"   类型: {analysis['category']}")
        print(f"   数量: {analysis['count']}\n")
        
        # 2. 构建搜索查询
        search_query = self.search_agent.build_search_query(analysis)
        
        # 3. 搜索仓库
        repos = self.search_agent.search_repositories(
            search_query, 
            count=analysis['count']
        )
        
        if not repos:
            print("😢 没有找到合适的项目")
            return
        
        # 4. 显示结果
        self.search_agent.display_results(repos)
        
        # 5. 交互式选择
        if auto_run and repos:
            selected_repo = repos[0]
            print(f"\n🚀 自动运行第一个项目: {selected_repo.full_name}")
        else:
            selected_repo = self.search_agent.interactive_select(repos)
        
        if not selected_repo:
            return
        
        # 6. 运行选中的项目
        self.run_project(selected_repo)
    
    def run_project(self, repo: GitHubRepo):
        """运行选中的项目"""
        print("\n" + "=" * 70)
        print(f"🚀 准备运行: {repo.full_name}")
        print("=" * 70)
        
        # 询问是否使用 SSH
        print("\n选择克隆方式:")
        print("1. HTTPS (默认)")
        print("2. SSH (需要配置 SSH 密钥)")
        
        try:
            clone_choice = input("\n👉 选择 (1/2, 默认 1): ").strip() or "1"
            use_ssh = (clone_choice == "2")
        except KeyboardInterrupt:
            print("\n\n👋 已取消")
            return
        
        # 创建运行器
        runner = GitHubProjectRunner(
            github_url=repo.html_url,
            use_proxy=self.proxy,
            use_ssh=use_ssh
        )
        
        # 运行项目
        print("\n")
        runner.run()
    
    def interactive_mode(self):
        """交互式模式"""
        print("=" * 70)
        print("🤖 GitHub AI Agent - 交互模式")
        print("=" * 70)
        print("输入你的需求，我会帮你找到最合适的 GitHub 项目")
        print("例如: '找 10 个 CSS 动画库'")
        print("输入 'q' 或 Ctrl+C 退出\n")
        
        while True:
            try:
                query = input("👉 你的需求: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['q', 'quit', 'exit']:
                    print("👋 再见！")
                    break
                
                print()
                self.run_query(query)
                print("\n" + "=" * 70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='GitHub AI Agent - 智能 GitHub 项目发现和运行助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式（简单规则）
  python agent.py
  
  # 使用 AI 分析（需要 API key）
  python agent.py --llm --llm-provider openai
  export OPENAI_API_KEY=your_key
  python agent.py --llm
  
  # 直接查询
  python agent.py --query "找 10 个 CSS 动画库"
  
  # 使用代理
  python agent.py --query "找 5 个 React UI 组件库" --proxy http://127.0.0.1:7890
  
  # 使用 LLM + 代理
  python agent.py --llm --proxy http://127.0.0.1:7890 --query "找前端动画库"
        """
    )
    
    parser.add_argument('--query', '-q', help='直接指定查询内容')
    parser.add_argument('--proxy', '-p', help='代理地址，例如: http://127.0.0.1:7890')
    parser.add_argument('--token', '-t', help='GitHub Personal Access Token')
    parser.add_argument('--auto-run', '-a', action='store_true', 
                       help='自动运行第一个搜索结果')
    
    # LLM 相关参数
    parser.add_argument('--llm', action='store_true',
                       help='使用 LLM 分析查询（需要 API key）')
    parser.add_argument('--llm-provider', default='openai',
                       choices=['openai', 'anthropic'],
                       help='LLM 提供商（默认: openai）')
    parser.add_argument('--llm-key', help='LLM API 密钥（或设置环境变量）')
    
    args = parser.parse_args()
    
    # 创建 Agent
    agent = GitHubAgent(
        github_token=args.token,
        proxy=args.proxy,
        use_llm=args.llm,
        llm_provider=args.llm_provider,
        llm_api_key=args.llm_key
    )
    
    # 运行模式
    if args.query:
        # 直接查询模式
        agent.run_query(args.query, auto_run=args.auto_run)
    else:
        # 交互模式
        agent.interactive_mode()


if __name__ == "__main__":
    main()

