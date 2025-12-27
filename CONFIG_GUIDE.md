# 🚀 快速配置指南

## 第 1 步：填写 API Key

打开项目根目录的 `.env` 文件，填写你的 API key：

```bash
# 编辑配置文件
vim .env
# 或
code .env
# 或
open .env
```

将：
```bash
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
```

改为：
```bash
DEEPSEEK_API_KEY=sk-你的真实密钥
```

## 第 2 步：加载配置

```bash
# 在项目根目录运行
source .env

# 验证
echo $DEEPSEEK_API_KEY
```

## 第 3 步：运行 Agent

```bash
python github_agent/agent.py --llm --query "找 10 个 CSS 动画库"
```

✅ 完成！

---

## 📁 配置文件说明

```
项目根目录/
├── .env              # 你的私密配置（已加入 .gitignore）
├── .env.example      # 配置模板
└── .gitignore        # 已配置忽略 .env 文件
```

- `.env` - 你的真实密钥，**不会被提交到 git**
- `.env.example` - 配置模板，可以提交

---

## 🔄 每次使用前记得加载

```bash
# 方式 1：手动加载
cd /path/to/run-github-project
source .env
python github_agent/agent.py --llm

# 方式 2：一键运行脚本（推荐）
./run.sh "找 CSS 动画库"
```

---

## 📝 创建快捷脚本（可选）

我帮你创建一个 `run.sh` 脚本，自动加载配置：

```bash
chmod +x run.sh
./run.sh "找 10 个 CSS 动画库"
```

---

更多配置方式请查看：
- [API_KEY_SETUP.md](github_agent/API_KEY_SETUP.md) - 详细配置指南
- [QUICKSTART.md](github_agent/QUICKSTART.md) - 快速入门

