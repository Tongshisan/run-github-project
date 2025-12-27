# 智能过滤功能说明

## 🎯 问题背景

GitHub Search API 的局限性：
1. **只能用关键词匹配** - 不理解语义
2. **结果是纯技术性的** - 按 stars 排序，不考虑是否真正符合用户需求  
3. **没有二次筛选** - 无法判断项目是否真正符合用户意图

## ✨ 智能过滤方案

结合 **GitHub API** + **LLM 评分** 实现更精准的搜索：

```
用户查询："帮我找适合毕业设计的前端项目"
   ↓
1. LLM 分析 → 关键词: ["frontend", "starter"]
   ↓
2. GitHub Search → 获取 30 个初步结果
   ↓
3. 读取每个项目的 README（前 500 字）
   ↓
4. LLM 评分（0-100）+ 生成推荐理由
   ↓
5. 按相关性排序，返回最相关的 10 个
```

## 🚀 使用方法

### 基础用法（不启用智能过滤）

```bash
python github_agent/agent.py --llm --query "找前端项目"
```

**结果**：返回 GitHub Stars 最多的 10 个项目

### 智能过滤模式（推荐！）

```bash
python github_agent/agent.py --llm --smart-filter --query "找适合毕业设计的前端项目"
```

**结果**：
1. 搜索 30 个候选项目
2. 读取每个项目的 README
3. LLM 根据用户需求评分
4. 返回最相关的 10 个项目，并显示：
   - 🧠 AI 评分：85/100
   - 💡 推荐理由："这是一个完整的前端模板项目，适合作为毕业设计基础"

## 📊 示例对比

### 场景：找适合毕业设计的前端项目

#### 不用智能过滤
```
搜索关键词: frontend starter
结果（按 stars 排序）:
  1. create-react-app (98k stars) ❌ 太简单，只是脚手架
  2. vue-cli (30k stars) ❌ 同样只是脚手架
  3. next.js (120k stars) ❌ 是框架，不是项目模板
```

#### 使用智能过滤
```
搜索关键词: frontend starter
→ 获取 30 个初步结果
→ LLM 分析 README 内容

结果（按相关性排序）:
  1. vue-element-admin (87k stars) ✅ AI评分 95/100
     💡 完整的后台管理系统，功能丰富，适合毕业设计
     
  2. react-admin (24k stars) ✅ AI评分 92/100
     💡 包含完整的 CRUD 和权限管理，文档完善
     
  3. ant-design-pro (36k stars) ✅ AI评分 90/100
     💡 企业级中后台前端解决方案，可直接使用
```

## 🔧 技术实现

### 1. README 获取

使用 GitHub Contents API：
```python
GET /repos/{owner}/{repo}/contents/README.md
```

### 2. LLM 评分

提示词模板：
```
用户需求：找适合毕业设计的前端项目

项目信息：
- 名称：vue-element-admin
- 描述：A magical vue admin
- README：Element UI + Vue.js 搭建的后台管理系统...

请评分（0-100）并说明理由。

评分标准：
- 90-100：完美匹配，强烈推荐
- 70-89：高度相关，值得推荐
- 50-69：部分相关，可以考虑
- 0-49：相关性低
```

### 3. 排序和过滤

```python
# 按 AI 评分排序
repos.sort(key=lambda x: x['ai_score'], reverse=True)

# 过滤掉不相关的（评分 < 50）
relevant_repos = [r for r in repos if r['ai_score'] >= 50]

# 返回 Top-K
return relevant_repos[:10]
```

## ⚠️ 注意事项

### 1. API 限制
- GitHub API：未认证 60 次/小时，已认证 5000 次/小时
- 智能过滤会多次调用 API 读取 README
- 建议设置 GitHub Token：`--token YOUR_TOKEN`

### 2. LLM 成本
- 智能过滤需要多次调用 LLM（30 次评分）
- DeepSeek 成本：~0.0003 CNY/次 → 总计 ~0.01 CNY
- 建议使用 DeepSeek（性价比最高）

### 3. 时间开销
- 基础搜索：~1-2 秒
- 智能过滤：~10-30 秒（取决于项目数量和 README 大小）

## 🎯 最佳实践

### 场景 1：快速浏览
```bash
python agent.py --llm --query "React UI 库"
```
不用智能过滤，快速返回结果。

### 场景 2：精准查找
```bash
python agent.py --llm --smart-filter --query "适合学习的 Vue 项目"
```
使用智能过滤，获得最相关的结果。

### 场景 3：特定需求
```bash
python agent.py --llm --smart-filter --query "包含支付功能的电商项目"
```
复杂需求场景，智能过滤效果最好。

## 📈 未来计划

- [ ] 集成 GitHub MCP 工具（直接调用 Cursor 的 MCP）
- [ ] 缓存 README 内容（避免重复请求）
- [ ] 并行评分（提升速度）
- [ ] 自定义评分标准
- [ ] 支持更多过滤条件（如：最近更新时间、维护状态等）

## 🤝 贡献

欢迎提 Issue 或 PR 改进智能过滤功能！

