# GitHub AI Agent 🤖

一个智能的 GitHub 项目发现和运行助手，通过自然语言查询找到最合适的开源项目，并自动克隆、配置和运行。

## ✨ 核心功能

### 🧠 智能搜索
- 📝 **自然语言理解**: 用人话描述需求，例如"找 10 个 CSS 动画库"
- 🔍 **GitHub API 集成**: 实时搜索 GitHub 上的开源项目
- ⭐ **智能排序**: 按 star 数、fork 数、更新时间排序
- 🏷️ **标签识别**: 自动识别项目技术栈和特性

### 🚀 自动化运行
- 📦 **依赖自动安装**: Homebrew、Git、Node.js、npm/pnpm 等
- 🔧 **环境自动配置**: 智能检测项目类型并配置环境
- 🎯 **一键运行**: 克隆、安装、启动一气呵成

### 🎮 交互体验
- 💬 **交互式选择**: 美观的项目列表展示
- 🎨 **彩色终端输出**: 清晰的信息分类和状态提示
- ⚡ **快速响应**: 高效的搜索和展示

## 🎯 使用场景

```bash
# 场景 1: 找 CSS 动画库
"找 10 个 CSS 动画库"

# 场景 2: 找 React 组件
"推荐 5 个最好的 React UI 组件库"

# 场景 3: 找机器学习项目
"找 Python 机器学习项目，star 数最多的"

# 场景 4: 找特定技术栈
"找 Next.js + TypeScript 的管理后台项目"

# 场景 5: 找工具
"找 CLI 工具开发框架"
```

## 🚀 快速开始

### 安装依赖

```bash
pip install requests
```

### 基本使用

#### 方式 1: 交互模式（推荐）

```bash
python github_agent.py
```

然后输入你的需求：
```
👉 你的需求: 找 10 个 CSS 动画库
```

#### 方式 2: 命令行模式

```bash
# 直接查询
python github_agent.py --query "找 10 个 CSS 动画库"

# 使用代理
python github_agent.py --query "找 5 个 React UI 库" --proxy http://127.0.0.1:7890

# 自动运行第一个结果
python github_agent.py --query "找 Vite React 模板" --auto-run
```

### GitHub Token（可选但推荐）

设置 GitHub Token 可以提高 API 调用限制（从 60/小时 提升到 5000/小时）：

```bash
# 1. 在 GitHub 创建 Personal Access Token
# https://github.com/settings/tokens

# 2. 设置环境变量
export GITHUB_TOKEN=your_token_here

# 3. 运行 Agent
python github_agent.py
```

或者直接在命令行指定：

```bash
python github_agent.py --token your_token_here --query "找项目"
```

## 📖 完整示例

### 示例 1: 找 CSS 动画库

```bash
$ python github_agent.py --query "找 10 个 CSS 动画库"

======================================================================
🤖 GitHub AI Agent
======================================================================
📝 你的需求: 找 10 个 CSS 动画库

🧠 分析需求...
   关键词: css, 动画
   数量: 10

🔍 搜索中... (查询: css 动画 stars:>100)
✅ 找到 1,234 个相关仓库

======================================================================
📊 搜索结果 (共 10 个)
======================================================================

======================================================================
[1] animate-css/animate.css
======================================================================
⭐ Stars: 80,234 | 🍴 Forks: 16,789 | 📝 语言: CSS
🏷️  标签: css, animation, cross-browser
📖 描述: 🍿 A cross-browser library of CSS animations...
🔗 链接: https://github.com/animate-css/animate.css

[2] ...
```

### 示例 2: 找 React 组件库并运行

```bash
$ python github_agent.py

🤖 GitHub AI Agent - 交互模式
输入你的需求，我会帮你找到最合适的 GitHub 项目
例如: '找 10 个 CSS 动画库'

👉 你的需求: 找 React UI 组件库

🧠 分析需求...
🔍 搜索中...
✅ 找到 567 个相关仓库

[显示结果列表]

🎯 请选择要运行的项目
输入项目编号 (1-10), 或输入 'q' 退出

👉 你的选择: 1

🚀 准备运行: ant-design/ant-design
选择克隆方式:
1. HTTPS (默认)
2. SSH (需要配置 SSH 密钥)

👉 选择 (1/2, 默认 1): 1

[自动克隆和运行项目...]
```

## 🎨 命令行参数

```bash
python github_agent.py [选项]

选项:
  --query, -q TEXT      直接指定查询内容
  --proxy, -p TEXT      代理地址，例如: http://127.0.0.1:7890
  --token, -t TEXT      GitHub Personal Access Token
  --auto-run, -a        自动运行第一个搜索结果（跳过选择）
  --help                显示帮助信息
```

## 🔧 高级用法

### 1. 使用代理（解决网络问题）

```bash
# 方式 1: 命令行参数
python github_agent.py --proxy http://127.0.0.1:7890

# 方式 2: 环境变量
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
python github_agent.py
```

### 2. 创建快捷命令

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# 添加别名
alias gh-agent="python /path/to/github_agent.py"
alias gh-find="python /path/to/github_agent.py --query"

# 使用
gh-agent  # 交互模式
gh-find "找 CSS 动画库"  # 直接查询
```

### 3. 与其他工具组合

```bash
# 找到项目后保存列表
python github_agent.py --query "找 React 项目" > results.txt

# 批量处理
cat queries.txt | while read query; do
  python github_agent.py --query "$query" --auto-run
done
```

## 🧠 智能分析说明

Agent 会自动分析你的查询：

| 你的输入 | Agent 理解 | 搜索条件 |
|---------|-----------|---------|
| "找 10 个 CSS 动画库" | 关键词: CSS, 动画<br>数量: 10 | `css animation stars:>100` |
| "推荐 Python 机器学习项目" | 关键词: 机器学习<br>语言: Python | `machine learning language:python stars:>100` |
| "最好的 React UI 组件" | 关键词: React, UI, 组件<br>排序: stars | `react ui component stars:>100 sort:stars` |

## 📊 项目结构

```
run-github-project/
├── github_agent.py          # AI Agent 主程序
├── run_github_project.py    # 项目运行器
├── README.md                # 项目运行器文档
├── AGENT_README.md          # 本文档
├── EXAMPLES.md              # 使用示例
└── requirements.txt         # Python 依赖
```

## 🔄 工作流程

```
用户输入自然语言查询
        ↓
    分析查询意图
  (提取关键词、数量、语言等)
        ↓
   构建 GitHub 搜索查询
        ↓
  调用 GitHub API 搜索
        ↓
   按 star 数排序展示
        ↓
    用户选择项目
        ↓
 调用运行器克隆和运行
        ↓
    项目启动成功 🎉
```

## 🎁 特色功能

### 1. 丰富的项目信息展示

- ⭐ Star 数和 Fork 数
- 📝 编程语言
- 🏷️ 项目标签
- 📖 项目描述
- 🔗 GitHub 链接

### 2. 智能过滤

- 自动过滤 star 数低的项目（>100）
- 支持按语言过滤
- 支持按更新时间过滤

### 3. 友好的交互

- 美观的终端界面
- 清晰的状态提示
- 错误处理和重试

## ⚠️ 注意事项

### API 限制

- **无 Token**: 60 次/小时
- **有 Token**: 5000 次/小时
- 建议设置 GitHub Token

### 网络问题

如果无法访问 GitHub：
```bash
# 使用代理
python github_agent.py --proxy http://127.0.0.1:7890
```

## 🚧 未来计划

- [ ] 集成 LLM（OpenAI/Claude）做更智能的需求理解
- [ ] 支持项目对比功能
- [ ] 添加项目评分系统
- [ ] 支持保存和管理收藏的项目
- [ ] 添加项目依赖分析
- [ ] 支持批量下载和运行
- [ ] Web 界面版本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**快速开始**: `python github_agent.py`

**有问题?** 查看故障排除章节或提交 Issue

Made with ❤️ for developers who love to explore

