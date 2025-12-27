# ⚡ 超简单配置（3 步完成）

## 📝 第 1 步：创建配置文件

在项目根目录创建 `.env` 文件：

```bash
cd /Users/lizhi/Documents/lizhi/github/run-github-project

# 创建 .env 文件
touch .env

# 编辑文件
vim .env
# 或
code .env
# 或
nano .env
```

## 📋 第 2 步：复制以下内容到 .env 文件

```bash
# 在这里填写你的 API Key（取消注释并替换）

# DeepSeek（推荐，性价比最高）
DEEPSEEK_API_KEY=sk-your-key-here

# 或使用其他模型（选一个即可）
# OPENAI_API_KEY=sk-your-key-here
# DASHSCOPE_API_KEY=sk-your-key-here
# GLM_API_KEY=your-key-here
# ANTHROPIC_API_KEY=sk-ant-your-key-here

# GitHub Token（可选）
# GITHUB_TOKEN=ghp_your-token-here

# 代理（可选）
# HTTP_PROXY=http://127.0.0.1:7890
# HTTPS_PROXY=http://127.0.0.1:7890
```

**修改**：将 `sk-your-key-here` 替换为你的真实 API key

## 🚀 第 3 步：加载并运行

```bash
# 加载配置
source .env

# 验证（应该显示你的 key）
echo $DEEPSEEK_API_KEY

# 运行 Agent
python github_agent/agent.py --llm --query "找 10 个 CSS 动画库"
```

✅ 完成！

---

## 🎯 或者使用快捷脚本

我已经创建了 `run.sh` 脚本，自动加载配置：

```bash
# 给脚本执行权限
chmod +x run.sh

# 运行（自动加载 .env）
./run.sh "找 10 个 CSS 动画库"

# 或交互模式
./run.sh
```

---

## 📚 获取 API Key

### DeepSeek（推荐）⭐
1. 访问 https://platform.deepseek.com/
2. 注册并充值（最低 ¥1 元）
3. 创建 API key
4. 复制密钥（sk-开头）

**成本**：查询 1000 次只要 ¥0.08（8分钱）！

### 其他模型
- OpenAI: https://platform.openai.com/api-keys
- 通义千问: https://dashscope.console.aliyun.com/
- 智谱 GLM: https://open.bigmodel.cn/

---

## ❓ 常见问题

### Q: .env 文件在哪里？
A: 在项目根目录（和 README.md 同级）

### Q: 会被提交到 git 吗？
A: 不会！.env 已加入 .gitignore

### Q: 为什么要用 .env？
A: 方便管理，不会误提交 API key

### Q: 还是不会配置？
A: 查看详细指南：
- [API_KEY_SETUP.md](github_agent/API_KEY_SETUP.md)
- [QUICKSTART.md](github_agent/QUICKSTART.md)

---

## 🔐 安全提示

- ✅ .env 文件不会被 git 追踪
- ✅ 不要提交含有 API key 的文件
- ✅ 不要分享你的 API key
- ✅ 定期更换 API key

---

需要帮助？提 Issue 或查看文档！

