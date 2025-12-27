# 🔑 API Key 快速配置

## 最快 2 分钟完成配置！

### 第 1 步：获取 API Key（1分钟）

访问 **DeepSeek**（推荐，最便宜）：
👉 https://platform.deepseek.com/

1. 注册账号
2. 充值最低 ¥1 元
3. 创建 API key
4. 复制密钥（sk-开头）

### 第 2 步：配置（1分钟）

```bash
# 打开终端，输入（替换成你的 key）：
export DEEPSEEK_API_KEY=sk-你的密钥

# 验证（应该显示你的密钥）：
echo $DEEPSEEK_API_KEY
```

### 第 3 步：运行！

```bash
python github_agent/agent.py --llm --query "找 10 个 CSS 动画库"
```

✅ 完成！

---

## 永久保存配置（推荐）

```bash
# 添加到配置文件（选择一个）
echo 'export DEEPSEEK_API_KEY=sk-你的密钥' >> ~/.zshrc     # zsh 用户
echo 'export DEEPSEEK_API_KEY=sk-你的密钥' >> ~/.bashrc   # bash 用户

# 重新加载
source ~/.zshrc   # 或 source ~/.bashrc
```

以后每次打开终端都会自动加载！

---

## 详细配置指南

完整的配置说明，包括：
- ✅ 多种配置方式
- ✅ Windows 配置
- ✅ 配置文件方式
- ✅ 安全建议
- ✅ 常见问题解决

👉 查看 [API_KEY_SETUP.md](./API_KEY_SETUP.md)

---

## 其他模型

| 模型 | 配置 | 价格 |
|-----|------|------|
| DeepSeek ⭐ | `DEEPSEEK_API_KEY` | ¥0.001/1M |
| OpenAI | `OPENAI_API_KEY` | $0.15/1M |
| 通义千问 | `DASHSCOPE_API_KEY` | ¥0.0004/1K |
| 智谱 GLM | `GLM_API_KEY` | ¥0.0001/1K |

详细对比：[MODELS.md](./MODELS.md)

---

## 常见问题

### Q: 为什么需要 API Key？
A: Agent 使用 AI 大模型理解你的中文需求，需要调用 LLM API。

### Q: 要花多少钱？
A: DeepSeek 超便宜！查询 1000 次只要 ¥0.08（8分钱）

### Q: 可以免费用吗？
A: 可以不用 LLM（去掉 `--llm` 参数），但中文支持会差一些。

### Q: 我设置了但还是报错？
A: 检查：
```bash
# 1. 验证是否设置
echo $DEEPSEEK_API_KEY

# 2. 如果为空，重新设置
export DEEPSEEK_API_KEY=sk-你的密钥

# 3. 确认拼写正确
```

---

**需要帮助？** 
- 📖 详细文档: [API_KEY_SETUP.md](./API_KEY_SETUP.md)
- 🤝 提问: 创建 Issue

