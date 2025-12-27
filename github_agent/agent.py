#!/usr/bin/env python3
"""
GitHub AI Agent - 智能 GitHub 项目发现和运行助手
使用自然语言查询 GitHub 项目，自动分析、排序、展示并运行
"""

import sys
import os
import json
from pathlib import Path

# 添加父目录到 Python 路径以导入 run_github_project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run_github_project import GitHubProjectRunner

# 尝试加载本地 .env 文件
try:
    current_dir = Path(__file__).parent
    env_file = current_dir / '.env'
    if env_file.exists():
        from load_env import load_env_file
        load_env_file(env_file)
except Exception as e:
    pass  # 如果加载失败，使用环境变量

# 导入搜索代理
from search_agent import GitHubSearchAgent
from smart_search_agent import SmartSearchAgent


class GitHubAgent:
    """GitHub AI Agent 主类"""
    
    def __init__(self, github_token=None, proxy=None,
                 use_llm=False, llm_provider="deepseek", llm_api_key=None,
                 use_smart_filter=False):
        """
        初始化 GitHub Agent
        
        Args:
            github_token: GitHub Token
            proxy: 代理地址
            use_llm: 是否使用 LLM 分析查询
            llm_provider: LLM 提供商
            llm_api_key: LLM API 密钥
            use_smart_filter: 是否使用智能过滤（基于 README 的 LLM 评分）
        """
        # 根据是否启用智能过滤选择不同的搜索代理
        if use_smart_filter:
            print("🚀 使用智能搜索模式（LLM + README 评分）")
            self.search_agent = SmartSearchAgent(
                github_token=github_token,
                use_llm=True,  # 智能过滤必须启用 LLM
                llm_provider=llm_provider,
                llm_api_key=llm_api_key
            )
        else:
            print("🔍 使用基础搜索模式")
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
        
        # 打印完整的分析结果（调试用）
        print("\n" + "="*70)
        print("🔍 LLM 分析结果（完整）：")
        print("="*70)
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
        print("="*70 + "\n")
        
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
        
        print(f"🔎 实际 GitHub 搜索查询: {search_query}")
        print(f"📊 请求数量: {analysis['count']}\n")
        
        # 3. 搜索仓库（智能代理会自动评分和排序）
        repos = self.search_agent.search_repositories(
            query=search_query, 
            count=analysis['count'],
            user_query=user_query  # 传递原始查询用于智能过滤
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
        
        # 6. 运行项目
        self.run_project(selected_repo)
    
    def run_project(self, repo):
        """运行选中的项目"""
        print("\n" + "=" * 70)
        print(f"🚀 准备运行: {repo.full_name}")
        print("=" * 70)
        
        # 创建项目运行器
        runner = GitHubProjectRunner(
            repo_url=repo.html_url,
            proxy=self.proxy
        )
        
        # 执行运行流程
        success = runner.run()
        
        if success:
            print("\n✅ 项目运行成功！")
        else:
            print("\n❌ 项目运行失败")
    
    def interactive_mode(self):
        """交互模式：持续接受用户查询"""
        print("=" * 70)
        print("🤖 GitHub AI Agent - 交互模式")
        print("=" * 70)
        print("输入你的需求，我会帮你找到最合适的 GitHub 项目")
        print("例如: '找 10 个 CSS 动画库'")
        print("输入 'q' 或 Ctrl+C 退出\n")
        
        while True:
            try:
                user_query = input("👉 你的需求: ").strip()
                
                if user_query.lower() in ['q', 'quit', 'exit']:
                    print("\n👋 再见！")
                    break
                
                if not user_query:
                    continue
                
                print()  # 空行
                self.run_query(user_query)
                print("\n" + "=" * 70 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                continue


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='GitHub AI Agent - 智能 GitHub 项目发现和运行助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础模式（简单规则）
  python agent.py --query "找 CSS 动画库"
  
  # LLM 模式（推荐）
  export DEEPSEEK_API_KEY=sk-...
  python agent.py --llm --query "找 10 个 CSS 动画库"
  
  # 智能过滤模式（最精准，但较慢）
  python agent.py --llm --smart-filter --query "找适合毕业设计的前端项目"
  
  # 使用其他模型
  python agent.py --llm --llm-provider openai    # GPT-4
  python agent.py --llm --llm-provider qwen      # 通义千问
  python agent.py --llm --llm-provider glm       # 智谱 GLM
  python agent.py --llm --llm-provider anthropic # Claude
  
  # 交互模式
  python agent.py --llm --smart-filter
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
    parser.add_argument('--llm-provider', default='deepseek',
                       choices=['deepseek', 'openai', 'anthropic', 'qwen', 'glm'],
                       help='LLM 提供商（默认: deepseek，性价比最高）')
    parser.add_argument('--llm-key', help='LLM API 密钥（或设置环境变量）')
    parser.add_argument('--smart-filter', action='store_true',
                       help='启用智能过滤（基于 README 的 LLM 评分，需要 --llm）')
    
    args = parser.parse_args()
    
    # 创建 Agent
    agent = GitHubAgent(
        github_token=args.token,
        proxy=args.proxy,
        use_llm=args.llm,
        llm_provider=args.llm_provider,
        llm_api_key=args.llm_key,
        use_smart_filter=args.smart_filter  # 智能过滤
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
