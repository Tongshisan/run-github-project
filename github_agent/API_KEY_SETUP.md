# API Key 配置指南

## 🔑 支持的 API Keys

根据你选择的 LLM 提供商，需要配置对应的 API key：

| 提供商 | 环境变量名 | 获取地址 |
|--------|-----------|---------|
| **DeepSeek** ⭐ | `DEEPSEEK_API_KEY` | https://platform.deepseek.com/ |
| OpenAI | `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| 通义千问 | `DASHSCOPE_API_KEY` | https://dashscope.console.aliyun.com/ |
| 智谱 GLM | `GLM_API_KEY` | https://open.bigmodel.cn/ |
| Anthropic | `ANTHROPIC_API_KEY` | https://console.anthropic.com/ |
| GitHub | `GITHUB_TOKEN` | https://github.com/settings/tokens |

---

## 📝 配置方式

### 方式 1️⃣：环境变量（推荐）⭐

#### macOS / Linux

**临时配置（当前终端会话）**

```bash
# DeepSeek（推荐）
export DEEPSEEK_API_KEY=sk-your-key-here

# 或其他模型
export OPENAI_API_KEY=sk-your-key-here
export DASHSCOPE_API_KEY=sk-your-key-here
export GLM_API_KEY=your-key-here
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# GitHub Token（可选，提高 API 限制）
export GITHUB_TOKEN=ghp_your-token-here
```

**永久配置（推荐）**

编辑你的 shell 配置文件：

```bash
# 打开配置文件
vim ~/.zshrc      # 如果用 zsh
# 或
vim ~/.bashrc     # 如果用 bash

# 添加以下内容
export DEEPSEEK_API_KEY=sk-your-key-here
export GITHUB_TOKEN=ghp_your-token-here

# 保存后重新加载
source ~/.zshrc
# 或
source ~/.bashrc
```

**验证配置**

```bash
echo $DEEPSEEK_API_KEY
# 应该输出你的 API key
```

#### Windows

**临时配置（PowerShell）**

```powershell
$env:DEEPSEEK_API_KEY="sk-your-key-here"
$env:GITHUB_TOKEN="ghp-your-token-here"
```

**永久配置**

1. 打开"环境变量"设置：
   - 右键"此电脑" → 属性
   - 高级系统设置
   - 环境变量

2. 在"用户变量"中点击"新建"：
   - 变量名：`DEEPSEEK_API_KEY`
   - 变量值：`sk-your-key-here`

3. 重启终端

---

### 方式 2️⃣：配置文件

创建配置文件 `~/.github_agent.env`：

```bash
# ~/.github_agent.env

# LLM API Keys（选择一个）
DEEPSEEK_API_KEY=sk-your-key-here
# OPENAI_API_KEY=sk-your-key-here
# DASHSCOPE_API_KEY=sk-your-key-here
# GLM_API_KEY=your-key-here
# ANTHROPIC_API_KEY=sk-ant-your-key-here

# GitHub Token（可选）
GITHUB_TOKEN=ghp-your-token-here

# 代理设置（可选）
# HTTP_PROXY=http://127.0.0.1:7890
# HTTPS_PROXY=http://127.0.0.1:7890
```

**加载配置文件**

```bash
# 方式 1：手动加载
source ~/.github_agent.env
python agent.py

# 方式 2：使用 dotenv（需要安装 python-dotenv）
pip install python-dotenv
python agent.py  # 代码会自动加载
```

在代码中自动加载（可选）：

```python
# agent.py 顶部添加
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/.github_agent.env'))
```

---

### 方式 3️⃣：命令行参数

```bash
# 直接在命令中指定
python agent.py --llm --llm-key sk-your-key-here --query "找项目"

# GitHub token
python agent.py --token ghp-your-token-here
```

⚠️ **不推荐**：API key 会显示在命令历史中

---

### 方式 4️⃣：代码中配置

**不推荐用于生产环境**，但适合测试：

```python
from github_agent.config import LLMConfig
from github_agent.llm_analyzer_v2 import LLMQueryAnalyzer

# 直接传入 API key
config = LLMConfig(
    provider="deepseek",
    api_key="sk-your-key-here"  # ⚠️ 不要提交到 git
)

analyzer = LLMQueryAnalyzer(config)
```

---

## 🎯 快速开始

### 步骤 1：获取 API Key

#### DeepSeek（推荐）

1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 点击右上角头像 → API Keys
4. 点击"创建新密钥"
5. 复制密钥（sk-开头）

**充值**：最低 ¥1 元，性价比超高！

#### OpenAI

1. 访问 https://platform.openai.com/api-keys
2. 登录账号
3. 点击"Create new secret key"
4. 复制密钥（sk-开头）

#### GitHub Token（可选）

1. 访问 https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 勾选 `public_repo` 权限
4. 生成并复制 token（ghp_开头）

### 步骤 2：配置 API Key

**最简单的方式**：

```bash
# 1. 设置环境变量
export DEEPSEEK_API_KEY=sk-your-key-here

# 2. 验证
echo $DEEPSEEK_API_KEY

# 3. 运行
python github_agent/agent.py --llm --query "找 CSS 动画库"
```

### 步骤 3：永久保存（推荐）

```bash
# 添加到 shell 配置
echo 'export DEEPSEEK_API_KEY=sk-your-key-here' >> ~/.zshrc
echo 'export GITHUB_TOKEN=ghp-your-token-here' >> ~/.zshrc

# 重新加载
source ~/.zshrc

# 现在每次打开终端都会自动加载
```

---

## 🔒 安全建议

### ✅ 推荐做法

1. **使用环境变量** - 不要硬编码在代码中
2. **添加到 .gitignore** - 不要提交配置文件
3. **使用 .env 文件** - 集中管理，但不要提交
4. **定期轮换** - 定期更换 API key
5. **限制权限** - 只给必要的权限

### ❌ 不要做的事

```python
# ❌ 不要这样
api_key = "sk-1234567890abcdef"  # 硬编码

# ❌ 不要提交
git add config.py  # 包含 API key 的文件
git commit -m "add config"

# ❌ 不要分享
print(f"我的 key: {api_key}")  # 泄露
```

### 📋 .gitignore 配置

确保以下文件不被提交：

```gitignore
# API Keys 和敏感信息
.env
.env.local
*.env
config.local.py
secrets.py

# 日志文件
*.log
logs/

# 临时文件
.cache/
__pycache__/
```

---

## 🧪 测试配置

### 验证 API Key 是否有效

```bash
# 运行测试脚本
python -c "
from github_agent.config import LLMConfig
config = LLMConfig(provider='deepseek')
key = config.load_api_key()
print(f'✅ API Key 已配置: {key[:10]}...' if key else '❌ 未找到 API Key')
"
```

### 测试 LLM 调用

```bash
# 简单测试
python github_agent/agent.py --llm --query "测试" --llm-provider deepseek
```

---

## 🆘 常见问题

### 问题 1：提示 "未设置 API key"

**错误信息**：
```
ConfigurationError: 请设置 DEEPSEEK_API_KEY 环境变量
```

**解决方法**：
```bash
# 检查是否设置
echo $DEEPSEEK_API_KEY

# 如果为空，设置它
export DEEPSEEK_API_KEY=sk-your-key-here

# 重新运行
python agent.py --llm
```

### 问题 2：API Key 无效

**错误信息**：
```
LLMError: 401 Unauthorized
```

**解决方法**：
1. 检查 API key 是否正确（没有多余空格）
2. 检查是否过期
3. 检查是否有余额（DeepSeek 需要充值）
4. 重新生成 API key

### 问题 3：设置了但读取不到

**可能原因**：
- 设置在不同的 shell 中（zsh vs bash）
- 没有 source 配置文件
- 拼写错误

**解决方法**：
```bash
# 检查当前 shell
echo $SHELL

# 编辑正确的配置文件
# zsh → ~/.zshrc
# bash → ~/.bashrc

# 重新加载
source ~/.zshrc
```

### 问题 4：多个环境的配置

如果你有多个项目或环境：

```bash
# 使用项目特定的配置
cd project1
export DEEPSEEK_API_KEY=sk-project1-key
python agent.py

cd project2
export DEEPSEEK_API_KEY=sk-project2-key
python agent.py
```

或使用 [direnv](https://direnv.net/)：

```bash
# 安装 direnv
brew install direnv

# 在项目目录创建 .envrc
echo 'export DEEPSEEK_API_KEY=sk-your-key' > .envrc

# 允许加载
direnv allow

# 自动加载和卸载
```

---

## 📚 完整示例

### 场景：首次使用

```bash
# 1. 获取 DeepSeek API Key
# 访问 https://platform.deepseek.com/，注册并充值最低 1 元

# 2. 配置环境变量
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx  # 可选

# 3. 验证配置
echo $DEEPSEEK_API_KEY

# 4. 运行 Agent
cd /path/to/run-github-project
python github_agent/agent.py --llm

# 5. 输入查询
👉 你的需求: 找 10 个 CSS 动画库

# 6. 如果成功，保存配置
echo 'export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx' >> ~/.zshrc
source ~/.zshrc
```

---

## 🎓 进阶配置

### 配置多个模型

```bash
# 同时配置多个，可以切换使用
export DEEPSEEK_API_KEY=sk-xxx
export OPENAI_API_KEY=sk-xxx
export ANTHROPIC_API_KEY=sk-ant-xxx

# 使用时指定
python agent.py --llm --llm-provider deepseek
python agent.py --llm --llm-provider openai
python agent.py --llm --llm-provider anthropic
```

### 使用别名

```bash
# 添加到 ~/.zshrc
alias gh-agent='python /path/to/github_agent/agent.py --llm'
alias gh-agent-deep='python /path/to/github_agent/agent.py --llm --llm-provider deepseek'
alias gh-agent-gpt='python /path/to/github_agent/agent.py --llm --llm-provider openai'

# 使用
gh-agent --query "找项目"
gh-agent-deep --query "找项目"
gh-agent-gpt --query "找项目"
```

---

需要更多帮助？查看 [MODELS.md](./MODELS.md) 了解各模型的详细配置！

