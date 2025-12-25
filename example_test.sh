#!/bin/bash
# 测试脚本示例
# 用于测试 run_github_project.py 的功能

echo "=========================================="
echo "GitHub 项目自动运行 Agent - 测试脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}注意：此脚本仅供演示测试流程${NC}"
echo -e "${YELLOW}实际测试时请选择一个轻量级的公开 GitHub 项目${NC}"
echo ""

# 示例项目列表
echo "推荐的测试项目（轻量级）："
echo "1. https://github.com/vitejs/vite-plugin-react-pages-demo"
echo "2. https://github.com/your-username/your-test-repo"
echo ""

# 获取用户输入
read -p "请输入要测试的 GitHub 项目 URL: " GITHUB_URL

if [ -z "$GITHUB_URL" ]; then
    echo "❌ 错误：未提供 GitHub URL"
    exit 1
fi

echo ""
echo "🚀 开始测试..."
echo "目标项目: $GITHUB_URL"
echo ""

# 运行脚本
python3 run_github_project.py "$GITHUB_URL"

# 检查退出状态
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ 测试完成${NC}"
else
    echo ""
    echo "❌ 测试过程中出现错误"
    exit 1
fi

