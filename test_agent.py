#!/usr/bin/env python3
"""
测试脚本 - 测试 GitHub Agent 的搜索功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_agent.agent import GitHubAgent

def test_search():
    """测试搜索功能"""
    print("=" * 70)
    print("🧪 测试 GitHub Agent 搜索功能")
    print("=" * 70)
    print()
    
    # 创建 Agent
    agent = GitHubAgent()
    
    # 测试查询（使用英文关键词效果更好）
    test_queries = [
        "CSS animation library",
        "React UI components",
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"测试查询: {query}")
        print(f"{'='*70}\n")
        
        # 分析查询
        analysis = agent.search_agent.analyze_query(query)
        print(f"✅ 查询分析:")
        print(f"   关键词: {', '.join(analysis['keywords'])}")
        print(f"   数量: {analysis['count']}")
        if analysis['language']:
            print(f"   语言: {analysis['language']}")
        
        # 构建搜索
        search_query = agent.search_agent.build_search_query(analysis)
        print(f"   搜索查询: {search_query}")
        print()
        
        # 执行搜索（只搜 3 个）
        repos = agent.search_agent.search_repositories(
            search_query, 
            count=3
        )
        
        if repos:
            print(f"✅ 找到 {len(repos)} 个项目:\n")
            for i, repo in enumerate(repos, 1):
                print(f"[{i}] {repo.full_name}")
                print(f"    ⭐ {repo.stars:,} stars | 🍴 {repo.forks:,} forks | 📝 {repo.language or 'N/A'}")
                if repo.topics:
                    print(f"    🏷️  {', '.join(repo.topics[:5])}")
                print(f"    📖 {repo.description[:100] if repo.description else '无描述'}...")
                print(f"    🔗 {repo.html_url}")
                print()
        else:
            print("❌ 未找到项目")
        
        print()

if __name__ == "__main__":
    try:
        test_search()
        print("=" * 70)
        print("✅ 测试完成!")
        print("=" * 70)
        print("\n💡 提示:")
        print("   - 使用英文关键词搜索效果更好")
        print("   - 可以运行: python github_agent/agent.py 进入交互模式")
        print("   - 或者: python github_agent/agent.py --query 'CSS animation'")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
