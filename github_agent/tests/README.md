# GitHub Agent 测试套件

## 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_config.py

# 运行并显示覆盖率
pytest --cov=github_agent --cov-report=html

# 详细输出
pytest -v
```

## 测试结构

```
tests/
├── __init__.py
├── test_config.py      # 配置测试
├── test_utils.py       # 工具函数测试
├── test_llm.py         # LLM 分析器测试
└── test_github.py      # GitHub API 测试
```

## 测试覆盖率

目标：> 80% 代码覆盖率

## Mock 数据

测试使用 mock 数据，不会真正调用 API。

