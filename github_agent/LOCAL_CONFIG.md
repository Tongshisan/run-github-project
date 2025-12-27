# 本地配置快速开始

## 📁 已为你创建的文件

```
github_agent/
├── .env.example      # 配置模板
├── .env              # 你的实际配置（需要填写）
└── load_env.py       # 自动加载配置
```

## 🚀 快速配置（3步）

### 第 1 步：编辑 .env 文件

```bash
cd github_agent
vim .env  # 或用其他编辑器打开
```

填入你的 API Key：

```bash
# 将这行
DEEPSEEK_API_KEY=

# 改成（填入你从 https://platform.deepseek.com/ 获取的 key）
DEEPSEEK_API_KEY=sk-你的密钥
```

### 第 2 步：验证配置

```bash
# 测试加载
python load_env.py

# 应该看到
📝 加载配置文件: /path/to/.env
  ✅ DEEPSEEK_API_KEY = sk-xxxxxx...
✅ 成功加载 1 个配置项
```

### 第 3 步：运行

```bash
# 配置会自动加载
python agent.py --llm --query "找 CSS 库"
```

✅ 完成！

---

## 📝 .env 文件示例

打开 `.env` 文件，填写：

```bash
# 必填：至少配置一个 LLM
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# 可选：GitHub Token（提高搜索限制）
GITHUB_TOKEN=ghp_your-github-token-here

# 可选：代理（如果需要）
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

---

## 🔍 配置优先级

Agent 会按以下顺序查找配置：

1. **命令行参数** - 优先级最高
   ```bash
   python agent.py --llm-key sk-xxx
   ```

2. **本地 .env 文件** - 推荐！
   ```bash
   # github_agent/.env
   DEEPSEEK_API_KEY=sk-xxx
   ```

3. **系统环境变量**
   ```bash
   export DEEPSEEK_API_KEY=sk-xxx
   ```

---

## 🛠️ 管理多个配置

### 开发环境

```bash
# .env.development
DEEPSEEK_API_KEY=sk-dev-key
GITHUB_TOKEN=ghp-dev-token
```

### 生产环境

```bash
# .env.production
DEEPSEEK_API_KEY=sk-prod-key
GITHUB_TOKEN=ghp-prod-token
```

使用：
```bash
# 开发
cp .env.development .env
python agent.py --llm

# 生产
cp .env.production .env
python agent.py --llm
```

---

## ⚠️ 安全提示

`.env` 文件已经添加到 `.gitignore`，**不会被提交到 git**。

确认：
```bash
git status
# 不应该看到 .env 文件
```

---

## 🆘 常见问题

### 问题：还是提示"未设置 API key"

**解决**：
```bash
# 1. 检查 .env 文件是否存在
ls -la .env

# 2. 检查内容
cat .env

# 3. 确保格式正确（KEY=VALUE，没有空格）
DEEPSEEK_API_KEY=sk-xxx  # ✅ 正确
DEEPSEEK_API_KEY = sk-xxx # ❌ 错误（有空格）

# 4. 测试加载
python load_env.py
```

### 问题：.env 文件在哪里？

```bash
# 在 github_agent 目录下
cd github_agent
pwd
# 应该是 /path/to/run-github-project/github_agent

ls -la .env
# 应该看到 .env 文件
```

### 问题：我不想用本地文件

```bash
# 方式 1：使用系统环境变量
export DEEPSEEK_API_KEY=sk-xxx
python agent.py --llm

# 方式 2：命令行参数
python agent.py --llm --llm-key sk-xxx
```

---

## 📚 更多配置选项

查看 `.env.example` 了解所有可配置项：

```bash
cat .env.example
```

---

需要帮助？查看 [QUICKSTART.md](./QUICKSTART.md) 或 [API_KEY_SETUP.md](./API_KEY_SETUP.md)

