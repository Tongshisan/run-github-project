# GitHub Agent 使用示例

## 🎯 场景 1: 找 CSS 动画库

### 交互模式

```bash
$ python github_agent.py

🤖 GitHub AI Agent - 交互模式
输入你的需求，我会帮你找到最合适的 GitHub 项目

👉 你的需求: 找 10 个 CSS 动画库

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
📖 描述: 🍿 A cross-browser library of CSS animations
🔗 链接: https://github.com/animate-css/animate.css

[2] elrumordelaluz/csshake
======================================================================
⭐ Stars: 5,234 | 🍴 Forks: 623 | 📝 语言: CSS
🏷️  标签: css, animation, shake
📖 描述: CSS classes to move your DOM!
🔗 链接: https://github.com/elrumordelaluz/csshake

[继续显示其他 8 个...]

🎯 请选择要运行的项目
输入项目编号 (1-10), 或输入 'q' 退出

👉 你的选择: 1

🚀 准备运行: animate-css/animate.css
选择克隆方式:
1. HTTPS (默认)
2. SSH (需要配置 SSH 密钥)

👉 选择 (1/2, 默认 1): 1

📥 正在克隆项目...
✅ 项目克隆成功
...
```

### 命令行模式

```bash
# 快速查询
python github_agent.py --query "找 10 个 CSS 动画库"

# 使用代理
python github_agent.py --query "找 CSS 动画库" --proxy http://127.0.0.1:7890

# 自动运行第一个
python github_agent.py --query "找 CSS 动画库" --auto-run
```

## 🎯 场景 2: 找 React UI 组件库

```bash
$ python github_agent.py --query "推荐 5 个最好的 React UI 组件库"

======================================================================
🤖 GitHub AI Agent
======================================================================
📝 你的需求: 推荐 5 个最好的 React UI 组件库

🧠 分析需求...
   关键词: 推荐, 最好, react, ui, 组件库
   数量: 5

🔍 搜索中...
✅ 找到 892 个相关仓库

📊 搜索结果:

[1] ant-design/ant-design          ⭐ 91,234
[2] mui/material-ui                 ⭐ 92,567
[3] chakra-ui/chakra-ui            ⭐ 37,123
[4] react-bootstrap/react-bootstrap ⭐ 22,456
[5] rsuite/rsuite                   ⭐ 8,234

👉 你的选择: 2

🚀 运行 Material-UI...
```

## 🎯 场景 3: 找 Python 机器学习项目

```bash
$ python github_agent.py

👉 你的需求: 找 Python 机器学习项目

🧠 分析需求...
   关键词: python, 机器学习, 项目
   语言: python
   数量: 10

🔍 搜索中... (查询: 机器学习 项目 language:python stars:>100)
✅ 找到 3,456 个相关仓库

📊 搜索结果:

[1] tensorflow/tensorflow         ⭐ 185,234
[2] keras-team/keras             ⭐ 61,456
[3] scikit-learn/scikit-learn    ⭐ 59,123
[4] pytorch/pytorch               ⭐ 81,234
[5] huggingface/transformers     ⭐ 132,456
...
```

## 🎯 场景 4: 找 Next.js 项目模板

```bash
$ python github_agent.py --query "找 Next.js TypeScript 管理后台模板" --proxy http://127.0.0.1:7890

======================================================================
🤖 GitHub AI Agent
======================================================================
📝 你的需求: 找 Next.js TypeScript 管理后台模板

🧠 分析需求...
   关键词: next.js, typescript, 管理后台, 模板
   语言: typescript
   数量: 10

🔍 搜索中...
✅ 找到 234 个相关仓库

📊 搜索结果:

[1] vercel/nextjs-dashboard       ⭐ 12,345
[2] creativetimofficial/nextjs-... ⭐ 8,234
[3] jpuri/react-admin-dashboard  ⭐ 6,789
...

👉 你的选择: 1

🚀 准备运行: vercel/nextjs-dashboard

[自动安装依赖并运行...]

✅ 项目已启动
🌐 访问: http://localhost:3000
```

## 🎯 场景 5: 批量查询

创建查询列表 `queries.txt`:
```
找 5 个 CSS 动画库
找 3 个 React 状态管理库
找 Python 爬虫框架
```

批量执行：
```bash
#!/bin/bash
while IFS= read -r query; do
  echo "处理查询: $query"
  python github_agent.py --query "$query" > "results_$(date +%s).txt"
  echo "---"
done < queries.txt
```

## 🎯 场景 6: 高级查询技巧

### 精确查询

```bash
# 指定 star 数范围
python github_agent.py --query "React 组件库 5000-10000 stars"

# 指定语言
python github_agent.py --query "JavaScript 工具库"

# 按更新时间
python github_agent.py --query "最近更新的 Vue3 项目"
```

### 组合查询

```bash
# 多条件
python github_agent.py --query "TypeScript + React + Vite 模板项目"

# 排除某些项目
python github_agent.py --query "React UI 库 不要 Material-UI"
```

## 🎯 场景 7: 使用 GitHub Token

### 设置 Token

```bash
# 方式 1: 环境变量
export GITHUB_TOKEN=ghp_your_token_here
python github_agent.py

# 方式 2: 命令行参数
python github_agent.py --token ghp_your_token_here --query "找项目"

# 方式 3: 写入配置文件
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.zshrc
source ~/.zshrc
```

### 创建 Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限: `public_repo` (读取公开仓库)
4. 生成并复制 Token

## 🎯 场景 8: 快捷命令

在 `~/.zshrc` 添加：

```bash
# Agent 别名
alias gh-agent='python /path/to/github_agent.py'
alias gh-find='python /path/to/github_agent.py --query'
alias gh-css='python /path/to/github_agent.py --query "找 CSS"'
alias gh-react='python /path/to/github_agent.py --query "找 React"'
alias gh-vue='python /path/to/github_agent.py --query "找 Vue"'

# 带代理的版本
alias gh-agent-proxy='python /path/to/github_agent.py --proxy http://127.0.0.1:7890'
```

使用：
```bash
gh-agent                          # 交互模式
gh-find "CSS 动画库"              # 快速查询
gh-css "动画库"                   # CSS 专用
gh-react "UI 组件"                # React 专用
gh-agent-proxy                    # 使用代理
```

## 🎯 场景 9: 与其他工具集成

### 结合 fzf 模糊搜索

```bash
# 搜索并用 fzf 选择
python github_agent.py --query "找 React 项目" | grep "^\[" | fzf
```

### 结合 jq 处理 JSON

```bash
# 导出为 JSON 格式（需要修改脚本）
python github_agent.py --query "找项目" --json | jq '.repos[] | {name, stars}'
```

### 保存搜索结果

```bash
# 保存到文件
python github_agent.py --query "找 CSS 库" > css_libraries.txt

# 追加到日志
python github_agent.py --query "找项目" >> search_history.log
```

## 🎯 场景 10: 常见查询模板

```bash
# UI 框架
"找 10 个最流行的 React UI 框架"
"推荐 Vue3 组件库"
"找 CSS 框架"

# 工具库
"找 JavaScript 工具库"
"推荐 Python 爬虫框架"
"找日期处理库"

# 完整项目
"找博客系统模板"
"推荐电商项目源码"
"找管理后台模板"

# 学习资源
"找前端学习项目"
"推荐算法实现项目"
"找开源书籍"

# 特定技术
"找 WebAssembly 项目"
"推荐 GraphQL 实现"
"找微前端框架"
```

## 💡 使用技巧

1. **关键词越具体，结果越精准**
   - ❌ "找项目"
   - ✅ "找 React TypeScript 电商后台管理系统"

2. **包含数量限制**
   - ✅ "找 5 个最好的 CSS 动画库"

3. **使用技术栈关键词**
   - ✅ "找 Next.js + Tailwind + TypeScript 项目"

4. **指定项目类型**
   - ✅ "找企业级 React 项目模板"

5. **使用代理解决网络问题**
   - ✅ `--proxy http://127.0.0.1:7890`

