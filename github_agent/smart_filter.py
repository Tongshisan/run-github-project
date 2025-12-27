#!/usr/bin/env python3
"""
Smart Filter - 使用 GitHub MCP + LLM 智能过滤搜索结果
"""

import json
from typing import List, Dict, Optional
from logger import get_logger

logger = get_logger(__name__)


class SmartFilter:
    """智能过滤器 - 使用 README 内容和 LLM 评分"""
    
    def __init__(self, llm_analyzer=None, mcp_client=None):
        """
        Args:
            llm_analyzer: LLM 分析器实例
            mcp_client: MCP 客户端（如果有的话）
        """
        self.llm_analyzer = llm_analyzer
        self.mcp_client = mcp_client
    
    def fetch_readme(self, owner: str, repo: str) -> Optional[str]:
        """
        获取仓库的 README 内容（使用 GitHub MCP）
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            README 内容（markdown 格式）或 None
        """
        # 尝试常见的 README 文件名
        readme_names = ['README.md', 'README.MD', 'readme.md', 'README', 'Readme.md']
        
        for readme_name in readme_names:
            try:
                logger.debug(f"尝试读取 {owner}/{repo} 的 {readme_name}")
                
                # 🆕 使用 GitHub API 直接获取文件内容
                import requests
                import base64
                
                url = f"https://api.github.com/repos/{owner}/{repo}/contents/{readme_name}"
                headers = {'Accept': 'application/vnd.github.v3+json'}
                
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    # GitHub API 返回 base64 编码的内容
                    content = base64.b64decode(data['content']).decode('utf-8')
                    logger.debug(f"✅ 成功读取 {owner}/{repo}/{readme_name} ({len(content)} 字符)")
                    return content
                else:
                    logger.debug(f"文件不存在: {readme_name} (HTTP {response.status_code})")
                    
            except Exception as e:
                logger.debug(f"读取 {readme_name} 失败: {e}")
                continue
        
        logger.warning(f"⚠️  无法读取 {owner}/{repo} 的 README")
        return None
    
    def score_repo(self, repo: Dict, user_query: str, readme_content: Optional[str]) -> Dict:
        """
        使用 LLM 对仓库进行评分
        
        Args:
            repo: 仓库信息
            user_query: 用户原始查询
            readme_content: README 内容
            
        Returns:
            包含评分和理由的字典
        """
        if not self.llm_analyzer:
            # 如果没有 LLM，只能用简单规则
            return {
                'score': 50,
                'reason': '基于 stars 数量的默认评分',
                'relevant': True
            }
        
        # 构建评分提示词
        prompt = f"""用户正在寻找：{user_query}

GitHub 仓库信息：
- 名称：{repo.get('full_name', 'N/A')}
- 描述：{repo.get('description', 'N/A')}
- Stars：{repo.get('stargazers_count', 0)}
- 语言：{repo.get('language', 'N/A')}
- 标签：{', '.join(repo.get('topics', []))}

README 摘要：
{readme_content[:500] if readme_content else '（无法获取 README）'}

请评估这个项目与用户需求的相关性，返回 JSON 格式：
{{
  "score": 85,  // 0-100 的评分，100 表示完全匹配
  "reason": "这是一个完善的 WebGL 3D 示例库，包含多个交互式案例",  // 简短说明
  "relevant": true  // 是否相关
}}

评分标准：
- 90-100：完全符合需求，是最佳选择
- 70-89：高度相关，值得推荐
- 50-69：部分相关，可以作为备选
- 30-49：相关性较低
- 0-29：基本不相关
"""
        
        try:
            # 调用 LLM 评分
            response = self.llm_analyzer.client.chat.completions.create(
                model=self.llm_analyzer.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的 GitHub 项目评估专家，擅长根据用户需求评估项目的相关性。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.debug(f"📊 {repo.get('full_name')}: 评分 {result.get('score', 0)}")
            return result
            
        except Exception as e:
            logger.error(f"❌ 评分失败: {e}")
            return {
                'score': 50,
                'reason': f'评分失败: {str(e)}',
                'relevant': True
            }
    
    def filter_and_rank(
        self, 
        repos: List[Dict], 
        user_query: str, 
        top_k: int = 10,
        fetch_readme: bool = True
    ) -> List[Dict]:
        """
        智能过滤和排序仓库列表
        
        Args:
            repos: 仓库列表
            user_query: 用户原始查询
            top_k: 返回前 K 个结果
            fetch_readme: 是否获取 README 进行深度分析
            
        Returns:
            排序后的仓库列表，每个包含 score 和 reason
        """
        logger.info(f"🧠 开始智能过滤 {len(repos)} 个仓库...")
        
        scored_repos = []
        for i, repo in enumerate(repos, 1):
            owner, repo_name = repo['full_name'].split('/')
            
            # 获取 README
            readme = None
            if fetch_readme:
                logger.info(f"  [{i}/{len(repos)}] 读取 {repo['full_name']} 的 README...")
                readme = self.fetch_readme(owner, repo_name)
            
            # LLM 评分
            score_result = self.score_repo(repo, user_query, readme)
            
            # 添加评分信息到仓库数据
            repo_with_score = {
                **repo,
                'ai_score': score_result.get('score', 0),
                'ai_reason': score_result.get('reason', ''),
                'ai_relevant': score_result.get('relevant', True)
            }
            scored_repos.append(repo_with_score)
        
        # 按 AI 评分排序
        scored_repos.sort(key=lambda x: x['ai_score'], reverse=True)
        
        # 过滤不相关的
        relevant_repos = [r for r in scored_repos if r['ai_relevant']]
        
        logger.info(f"✅ 智能过滤完成: {len(relevant_repos)}/{len(repos)} 个相关仓库")
        
        return relevant_repos[:top_k]


def integrate_mcp_tools():
    """
    集成 MCP 工具的辅助函数
    
    Returns:
        包含 MCP 工具函数的字典
    """
    return {
        'get_file_contents': get_github_file_via_mcp,
        'search_repositories': search_github_via_mcp,
    }


def get_github_file_via_mcp(owner: str, repo: str, path: str, branch: str = "main") -> Optional[str]:
    """
    通过 MCP 获取 GitHub 文件内容
    
    Args:
        owner: 仓库所有者
        repo: 仓库名称
        path: 文件路径
        branch: 分支名称
        
    Returns:
        文件内容或 None
    """
    try:
        # 这里应该调用实际的 MCP 工具
        # 由于 MCP 是通过 Cursor 提供的，我们需要在运行时调用
        logger.debug(f"📥 通过 MCP 获取: {owner}/{repo}/{path}")
        
        # TODO: 实际的 MCP 调用需要在 agent.py 中实现
        # 因为 MCP 工具只能在特定环境中调用
        
        return None
    except Exception as e:
        logger.error(f"❌ MCP 获取文件失败: {e}")
        return None


def search_github_via_mcp(query: str, page: int = 1, per_page: int = 30) -> List[Dict]:
    """
    通过 MCP 搜索 GitHub 仓库
    
    Args:
        query: 搜索查询
        page: 页码
        per_page: 每页结果数
        
    Returns:
        仓库列表
    """
    try:
        logger.debug(f"🔍 通过 MCP 搜索: {query}")
        
        # TODO: 实际的 MCP 调用
        
        return []
    except Exception as e:
        logger.error(f"❌ MCP 搜索失败: {e}")
        return []

