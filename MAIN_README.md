# GitHub Project Runner

自动化工具集，包含项目运行器和智能项目发现 Agent。

## 📁 项目结构

```
run-github-project/
├── run_github_project.py    # 项目自动运行工具
├── README.md                 # 运行器文档
├── EXAMPLES.md               # 运行器示例
├── STRUCTURE.md              # 代码结构说明
├── example_test.sh           # 测试脚本
├── .gitignore
│
└── github_agent/             # 🆕 AI Agent (智能项目发现)
    ├── agent.py              # Agent 主程序
    ├── README.md             # Agent 文档
    ├── EXAMPLES.md           # Agent 示例
    └── requirements.txt      # Agent 依赖
```

## 🚀 两个工具

### 1️⃣ 项目运行器 (`run_github_project.py`)

**用途**: 给定 GitHub URL，自动克隆和运行项目

**特点**:
- ✅ 自动安装依赖工具（Homebrew, Git, Node.js, pnpm 等）
- ✅ 智能包管理器检测
- ✅ 支持代理和 SSH
- ✅ 网络诊断

**快速开始**:
```bash
# 基本使用
python run_github_project.py https://github.com/user/repo

# 使用代理
python run_github_project.py https://github.com/user/repo --proxy http://127.0.0.1:7890

# 使用 SSH
python run_github_project.py https://github.com/user/repo --ssh
```

📖 [完整文档](./README.md) | [使用示例](./EXAMPLES.md)

---

### 2️⃣ AI Agent (`github_agent/`)

**用途**: 用自然语言查找和运行 GitHub 项目

**特点**:
- 🧠 自然语言理解 ("找 10 个 CSS 动画库")
- 🔍 智能 GitHub 搜索
- ⭐ 按 star 数排序展示
- 🎯 交互式选择
- 🚀 自动运行选中项目

**快速开始**:
```bash
# 安装依赖
pip install -r github_agent/requirements.txt

# 交互模式
python github_agent/agent.py

# 直接查询
python github_agent/agent.py --query "找 10 个 CSS 动画库"
```

📖 [Agent 文档](./github_agent/README.md) | [Agent 示例](./github_agent/EXAMPLES.md)

---

## 🎯 使用场景对比

| 场景 | 使用工具 | 命令 |
|-----|---------|------|
| 已知项目 URL，想要运行 | 运行器 | `python run_github_project.py <url>` |
| 想找某类项目 | Agent | `python github_agent/agent.py --query "找项目"` |
| 探索新技术 | Agent | 交互模式，输入需求 |
| CI/CD 自动化 | 运行器 | 脚本中调用 |

## 🔧 系统要求

- macOS 系统
- Python 3.6+
- 互联网连接

## ⚙️ 可选配置

### 设置代理（推荐）

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

### 设置 GitHub Token（Agent 推荐）

提高 API 限制从 60/小时 到 5000/小时：

```bash
export GITHUB_TOKEN=your_token_here
```

## 📚 快速导航

### 运行器相关
- [运行器完整文档](./README.md)
- [运行器使用示例](./EXAMPLES.md)
- [代码结构说明](./STRUCTURE.md)

### Agent 相关
- [Agent 完整文档](./github_agent/README.md)
- [Agent 使用示例](./github_agent/EXAMPLES.md)

## 🎓 教程

### 新手入门

1. **运行已知项目**
   ```bash
   python run_github_project.py https://github.com/vitejs/vite
   ```

2. **发现新项目**
   ```bash
   python github_agent/agent.py
   # 输入: 找 React UI 组件库
   ```

### 进阶使用

1. **使用代理**
   ```bash
   python run_github_project.py <url> --proxy http://127.0.0.1:7890
   python github_agent/agent.py --proxy http://127.0.0.1:7890
   ```

2. **创建快捷命令**
   ```bash
   # 添加到 ~/.zshrc
   alias run-github="python /path/to/run_github_project.py"
   alias gh-agent="python /path/to/github_agent/agent.py"
   ```

## 🐛 故障排除

### 网络连接问题

最常见的问题，解决方法：
```bash
# 1. 使用代理
--proxy http://127.0.0.1:7890

# 2. 使用 SSH
--ssh

# 3. 配置 Git 代理
git config --global http.proxy http://127.0.0.1:7890
```

详细故障排除请查看各自的文档。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

Created with ❤️ for the developer community

---

**快速开始**:
- 运行项目: `python run_github_project.py <url>`
- 发现项目: `python github_agent/agent.py`

