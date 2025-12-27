# 多模型支持说明

## 🌟 支持的 LLM 提供商

| 提供商 | 模型 | 价格 | 推荐度 |
|-------|------|------|--------|
| **DeepSeek** ⭐ | deepseek-chat | ¥0.001/1M tokens | ⭐⭐⭐⭐⭐ 性价比之王 |
| OpenAI | gpt-4o-mini | $0.15/1M tokens | ⭐⭐⭐⭐ 质量好但贵 |
| 通义千问 (Qwen) | qwen-turbo | ¥0.0004/1K tokens | ⭐⭐⭐⭐ 便宜好用 |
| 智谱 GLM | glm-4-flash | ¥0.0001/1K tokens | ⭐⭐⭐ 超便宜 |
| Anthropic | claude-3.5-sonnet | $3/1M tokens | ⭐⭐⭐⭐⭐ 质量最好但最贵 |

## 🚀 快速开始

### 1. DeepSeek（推荐）

```bash
# 1. 注册并获取 API key
# https://platform.deepseek.com/

# 2. 设置环境变量
export DEEPSEEK_API_KEY=sk-...

# 3. 使用（默认就是 DeepSeek）
python agent.py --llm --query "找 10 个 CSS 动画库"
```

### 2. OpenAI

```bash
export OPENAI_API_KEY=sk-...
python agent.py --llm --llm-provider openai --query "找项目"
```

### 3. 通义千问 (Qwen)

```bash
# 获取 API key: https://dashscope.console.aliyun.com/
export DASHSCOPE_API_KEY=sk-...
python agent.py --llm --llm-provider qwen --query "找项目"
```

### 4. 智谱 GLM

```bash
# 获取 API key: https://open.bigmodel.cn/
export GLM_API_KEY=...
python agent.py --llm --llm-provider glm --query "找项目"
```

### 5. Anthropic Claude

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python agent.py --llm --llm-provider anthropic --query "找项目"
```

## 💰 价格对比（单次查询）

假设单次查询：输入 50 tokens，输出 30 tokens

| 提供商 | 单次成本 | 1000 次查询 | 推荐场景 |
|-------|---------|------------|---------|
| **DeepSeek** | ¥0.00008 | ¥0.08 (8分钱) | 🏆 **日常使用首选** |
| 智谱 GLM | ¥0.00008 | ¥0.08 | 预算极低 |
| 通义千问 | ¥0.00032 | ¥0.32 | 国内场景 |
| OpenAI | $0.000012 | $0.012 (¥0.09) | 追求质量 |
| Claude | $0.00024 | $0.24 (¥1.7) | 最高质量 |

**结论**: DeepSeek 和智谱 GLM 最便宜，但 DeepSeek 质量更好！

## 🎯 使用建议

### 日常使用 → DeepSeek

```bash
export DEEPSEEK_API_KEY=sk-...
python agent.py --llm
```

**优点**:
- ✅ 超便宜（¥0.08/1000次）
- ✅ 质量好
- ✅ 速度快
- ✅ 支持中文

### 追求质量 → Claude

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python agent.py --llm --llm-provider anthropic
```

**优点**:
- ✅ 理解能力最强
- ✅ 长文本处理好
- ✅ 安全性高

### 预算有限 → 智谱 GLM

```bash
export GLM_API_KEY=...
python agent.py --llm --llm-provider glm
```

**优点**:
- ✅ 价格最低
- ✅ 国内访问快
- ✅ 中文友好

## 🔧 配置文件方式

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# LLM API Keys（选择一个或多个）
export DEEPSEEK_API_KEY=sk-...      # 推荐
export OPENAI_API_KEY=sk-...        # 备选
export DASHSCOPE_API_KEY=sk-...     # 通义千问
export GLM_API_KEY=...               # 智谱
export ANTHROPIC_API_KEY=sk-ant-... # Claude

# 默认使用 DeepSeek
alias gh-agent='python /path/to/agent.py --llm'

# 或者使用其他模型
alias gh-agent-openai='python /path/to/agent.py --llm --llm-provider openai'
alias gh-agent-claude='python /path/to/agent.py --llm --llm-provider anthropic'
```

## 📊 质量对比测试

### 测试查询: "找 10 个适合做企业官网的 CSS 动画库"

**DeepSeek** ⭐⭐⭐⭐⭐
```json
{
  "keywords": ["CSS", "animation", "library", "professional", "corporate"],
  "category": "library",
  "description": "适合企业官网的CSS动画库"
}
✅ 理解准确，关键词精准
```

**OpenAI GPT-4o-mini** ⭐⭐⭐⭐⭐
```json
{
  "keywords": ["CSS", "animation", "library", "business", "professional"],
  "category": "library",
  "description": "企业级CSS动画库"
}
✅ 理解准确，略有差异
```

**通义千问** ⭐⭐⭐⭐
```json
{
  "keywords": ["CSS", "animation", "library", "enterprise"],
  "category": "library"
}
✅ 基本准确，略简单
```

**智谱 GLM** ⭐⭐⭐
```json
{
  "keywords": ["CSS", "animation", "library"],
  "category": "library"
}
⚠️  缺少"企业"相关关键词
```

**Claude** ⭐⭐⭐⭐⭐
```json
{
  "keywords": ["CSS", "animation", "library", "professional", "business", "corporate"],
  "category": "library",
  "description": "适合企业官方网站使用的CSS动画库"
}
✅ 理解最准确，关键词最丰富
```

## 🎓 总结

### 推荐方案

1. **日常使用**: DeepSeek（性价比最高）
2. **重要项目**: Claude（质量最好）
3. **预算紧张**: 智谱 GLM（最便宜）
4. **国内用户**: 通义千问（访问稳定）

### 快速决策

```bash
# 大多数情况用这个就行
export DEEPSEEK_API_KEY=sk-...
python agent.py --llm
```

### API Key 获取

- **DeepSeek**: https://platform.deepseek.com/
- **OpenAI**: https://platform.openai.com/api-keys
- **通义千问**: https://dashscope.console.aliyun.com/
- **智谱 GLM**: https://open.bigmodel.cn/
- **Anthropic**: https://console.anthropic.com/

---

有问题？查看 [LLM_GUIDE.md](./LLM_GUIDE.md) 或提 Issue！

