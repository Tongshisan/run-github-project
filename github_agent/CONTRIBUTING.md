# 开发指南

## 🛠️ 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/your-username/run-github-project.git
cd run-github-project/github_agent
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 或使用 conda
conda create -n github-agent python=3.10
conda activate github-agent
```

### 3. 安装依赖

```bash
# 开发依赖
pip install -r requirements-dev.txt

# 如果没有 requirements-dev.txt，手动安装
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

## 📝 代码规范

### Python 风格

遵循 [PEP 8](https://pep8.org/) 规范：

```python
# ✅ 好的命名
def analyze_user_query(query: str) -> Dict[str, Any]:
    pass

# ❌ 不好的命名
def func1(q):
    pass
```

### 类型提示

所有公共 API 必须有类型提示：

```python
from typing import List, Dict, Optional

def search_repos(
    query: str,
    count: int = 10,
    language: Optional[str] = None
) -> List[Dict[str, Any]]:
    """搜索仓库"""
    pass
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def analyze_query(user_query: str) -> Dict[str, Any]:
    """
    分析用户查询
    
    Args:
        user_query: 用户的自然语言查询
    
    Returns:
        分析结果字典，包含关键词、数量等信息
    
    Raises:
        ValidationError: 查询无效时抛出
        LLMError: LLM 调用失败时抛出
    
    Example:
        >>> analyzer = LLMQueryAnalyzer()
        >>> result = analyzer.analyze_query("找 10 个 CSS 库")
        >>> print(result['keywords'])
        ['CSS', 'library']
    """
    pass
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_config.py

# 显示覆盖率
pytest --cov=github_agent --cov-report=html

# 详细输出
pytest -v -s
```

### 编写测试

```python
import pytest
from github_agent.config import LLMConfig

def test_llm_config_defaults():
    """测试默认配置"""
    config = LLMConfig()
    assert config.provider == "deepseek"
    assert config.temperature == 0.3

def test_llm_config_invalid_provider():
    """测试无效的提供商"""
    with pytest.raises(ValueError):
        config = LLMConfig(provider="invalid")
```

## 🔍 代码检查

### Flake8（代码风格）

```bash
flake8 github_agent/ --max-line-length=100
```

### Black（代码格式化）

```bash
# 检查
black github_agent/ --check

# 格式化
black github_agent/
```

### Mypy（类型检查）

```bash
mypy github_agent/ --ignore-missing-imports
```

## 🏗️ 项目结构

```
github_agent/
├── __init__.py           # 包初始化
├── config.py             # 配置管理
├── logger.py             # 日志系统
├── exceptions.py         # 异常定义
├── utils.py              # 工具函数
├── llm_analyzer_v2.py    # LLM 分析器
├── github_api.py         # GitHub API 封装
├── agent.py              # 主程序
│
├── tests/                # 测试
│   ├── __init__.py
│   ├── test_*.py
│   └── fixtures/         # 测试数据
│
├── docs/                 # 文档
│   ├── README.md
│   ├── MODELS.md
│   └── API.md
│
└── scripts/              # 脚本
    ├── setup.sh
    └── test.sh
```

## 📦 发布流程

### 1. 更新版本号

```python
# __init__.py
__version__ = "1.1.0"
```

### 2. 更新 CHANGELOG

```markdown
## [1.1.0] - 2024-01-01
### Added
- 新增多模型支持
- 添加配置管理系统

### Changed
- 重构 LLM 分析器

### Fixed
- 修复网络超时问题
```

### 3. 运行测试

```bash
pytest --cov=github_agent --cov-report=term
```

### 4. 打包

```bash
python setup.py sdist bdist_wheel
```

### 5. 发布到 PyPI

```bash
twine upload dist/*
```

## 🐛 调试技巧

### 1. 使用日志

```python
from github_agent.logger import logger, setup_logger

# 设置 DEBUG 级别
setup_logger(level='DEBUG')

# 详细日志
logger.debug(f"查询参数: {params}")
logger.info("开始搜索...")
logger.error(f"失败: {e}", exc_info=True)
```

### 2. 使用 pdb

```python
import pdb; pdb.set_trace()  # 设置断点
```

### 3. 使用 IPython

```python
# 在代码中嵌入 IPython shell
from IPython import embed
embed()
```

## 🤝 贡献指南

### 提交流程

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

### Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
test: 添加测试
refactor: 重构代码
style: 代码格式调整
chore: 构建/工具链更新
```

示例：
```bash
git commit -m "feat: 添加 DeepSeek 模型支持"
git commit -m "fix: 修复网络超时问题"
git commit -m "docs: 更新 README"
```

## 📚 学习资源

- [Python 最佳实践](https://docs.python-guide.org/)
- [Real Python 教程](https://realpython.com/)
- [Effective Python](https://effectivepython.com/)
- [Python Design Patterns](https://refactoring.guru/design-patterns/python)

## 🎯 性能优化

### 1. 使用缓存

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_repo_info(url: str):
    # 缓存 API 调用结果
    pass
```

### 2. 异步请求

```python
import asyncio
import aiohttp

async def fetch_multiple_repos(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_repo(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### 3. 性能分析

```python
import cProfile
import pstats

cProfile.run('main()', 'output.prof')
p = pstats.Stats('output.prof')
p.sort_stats('cumulative').print_stats(10)
```

## 🔒 安全建议

1. **不要提交 API key** - 使用环境变量
2. **验证用户输入** - 防止注入攻击
3. **限制 API 调用频率** - 使用 rate limiting
4. **使用 HTTPS** - 所有网络请求
5. **定期更新依赖** - 修复安全漏洞

---

Happy Coding! 🚀

