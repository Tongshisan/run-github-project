# GitHub Agent - LLM 集成说明

## 🤖 使用 AI 大模型分析需求

现在 Agent 支持两种模式：

### 1️⃣ 简单规则模式（默认，无需 API）

使用基础的关键词提取，适合简单场景：

```bash
python agent.py --query "CSS animation"
```

**优点**: 免费、快速
**缺点**: 中文理解差，无法处理复杂需求

---

### 2️⃣ LLM 智能模式（推荐，需要 API）

使用大模型真正理解自然语言：

```bash
# 使用 OpenAI
export OPENAI_API_KEY=sk-...
python agent.py --llm --query "找 10 个适合新手的 CSS 动画库"

# 使用 Claude
export ANTHROPIC_API_KEY=sk-ant-...
python agent.py --llm --llm-provider anthropic --query "推荐前端动画框架"
```

**优点**: 
- ✅ 理解中文自然语言
- ✅ 提取准确的英文关键词
- ✅ 识别项目类型和需求细节
- ✅ 处理复杂查询

**缺点**: 需要 API key，有成本

---

## 📦 安装 LLM 依赖

```bash
cd github_agent

# 选择一个安装
pip install openai        # 使用 OpenAI
pip install anthropic     # 使用 Claude
```

---

## 🔑 获取 API Key

### OpenAI (推荐 gpt-4o-mini，便宜)

1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API key
3. 设置环境变量:
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

### Anthropic Claude

1. 访问 https://console.anthropic.com/
2. 创建 API key
3. 设置环境变量:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

---

## 🎯 使用示例

### 简单模式（无 AI）

```bash
# 英文关键词效果更好
python agent.py --query "CSS animation library"
python agent.py --query "React UI components"
```

### AI 模式（推荐）

```bash
# 中文也能理解
python agent.py --llm --query "找 10 个适合做企业官网的 CSS 动画库"
python agent.py --llm --query "推荐 Python 爬虫框架，要简单易用的"
python agent.py --llm --query "React 的状态管理库，比 Redux 简单的"

# 交互模式
python agent.py --llm
```

---

## 🔄 对比

| 特性 | 简单规则 | LLM 模式 |
|-----|---------|---------|
| 中文理解 | ❌ 差 | ✅ 好 |
| 英文理解 | ✅ 基础 | ✅ 优秀 |
| 复杂需求 | ❌ | ✅ |
| 成本 | 免费 | 低（~$0.001/次） |
| 速度 | 快 | 稍慢（1-2秒） |

---

## 💰 成本估算

使用 GPT-4o-mini:
- 单次查询: ~$0.001 (不到 1 分钱)
- 100 次查询: ~$0.1 (1 毛钱)

非常便宜！🎉

---

## 🛠️ 高级配置

### 永久配置

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# LLM API Keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...

# Agent 别名
alias gh-agent='python /path/to/github_agent/agent.py --llm'
alias gh-find='python /path/to/github_agent/agent.py --llm --query'
```

使用：
```bash
gh-agent  # 直接进入 AI 交互模式
gh-find "找前端动画库"  # 快速查询
```

---

## 📝 示例对比

### 查询: "找 10 个适合做企业官网的 CSS 动画库"

**简单模式**:
```
关键词: 找, 10, 个, 适合做企业官网的, CSS, 动画库
搜索: 找 10 个 适合做企业官网的 CSS 动画库 stars:>100
结果: 不准确（中文关键词在 GitHub 效果差）
```

**LLM 模式**:
```
🧠 使用 AI 分析需求...
关键词: CSS, animation, library, professional, business
理解: 适合企业官网的CSS动画库
类型: library
数量: 10
搜索: CSS animation library professional business stars:>100
结果: 准确！找到高质量的专业动画库
```

---

## 🎓 最佳实践

1. **日常使用**: 简单模式足够（用英文关键词）
2. **复杂需求**: 开启 LLM 模式
3. **探索发现**: LLM 模式体验最好
4. **成本敏感**: 简单模式免费

---

需要帮助？查看 [README.md](./README.md) 或提 Issue！

