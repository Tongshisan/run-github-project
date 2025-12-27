#!/bin/bash

# GitHub Agent 启动脚本
# 自动加载配置并运行

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 加载配置文件
if [ -f .env ]; then
    echo "📝 加载配置文件..."
    source .env
else
    echo "⚠️  未找到 .env 文件"
    echo "请先复制 .env.example 为 .env 并填写 API key"
    echo ""
    echo "  cp .env.example .env"
    echo "  vim .env"
    exit 1
fi

# 检查 API key
if [ -z "$DEEPSEEK_API_KEY" ] && [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ 错误：未配置任何 LLM API key"
    echo ""
    echo "请编辑 .env 文件并填写至少一个 API key："
    echo "  vim .env"
    echo ""
    echo "获取 API key："
    echo "  DeepSeek: https://platform.deepseek.com/"
    echo "  OpenAI: https://platform.openai.com/api-keys"
    exit 1
fi

# 显示配置状态
echo "✅ 配置已加载"
if [ ! -z "$DEEPSEEK_API_KEY" ]; then
    echo "   DeepSeek: ${DEEPSEEK_API_KEY:0:10}..."
fi
if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "   OpenAI: ${OPENAI_API_KEY:0:10}..."
fi
if [ ! -z "$GITHUB_TOKEN" ]; then
    echo "   GitHub: ${GITHUB_TOKEN:0:10}..."
fi
echo ""

# 运行 Agent
if [ $# -eq 0 ]; then
    # 无参数：交互模式
    echo "🤖 启动交互模式..."
    python github_agent/agent.py --llm
else
    # 有参数：直接查询
    echo "🤖 执行查询: $1"
    python github_agent/agent.py --llm --query "$1"
fi

