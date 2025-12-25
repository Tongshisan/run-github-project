# 项目结构

run-github-project/
├── run_github_project.py   # 主程序脚本
├── example_test.sh          # 测试脚本示例
├── README.md                # 项目文档
└── .gitignore              # Git 忽略文件

## 文件说明

### run_github_project.py
主要的 Python 脚本，包含所有核心功能：
- GitHubProjectRunner 类：管理整个项目克隆和运行流程
- 自动检测和安装依赖工具
- 智能包管理器检测
- 项目克隆和运行

### example_test.sh
一个简单的 bash 测试脚本，用于演示如何使用主程序。

### README.md
详细的使用文档和说明。

## 主要功能模块

### 1. 工具检测模块
- `check_command_exists()`: 检查命令是否存在
- `check_npm_available()`: 检查 npm 是否可用

### 2. 工具安装模块
- `install_homebrew()`: 安装 Homebrew
- `install_git()`: 安装 Git
- `install_nvm()`: 安装 NVM
- `install_node()`: 安装 Node.js
- `install_pnpm()`: 安装 pnpm

### 3. 项目管理模块
- `clone_repository()`: 克隆 GitHub 仓库
- `detect_package_manager()`: 检测项目包管理器
- `install_dependencies()`: 安装项目依赖
- `run_project()`: 运行项目

### 4. 工具函数
- `run_command()`: 执行 shell 命令
- `_extract_project_name()`: 从 URL 提取项目名
- `_source_nvm()`: 生成 NVM source 命令
- `_get_npm_command()`: 获取 npm 命令
- `_get_pnpm_command()`: 获取 pnpm 命令

