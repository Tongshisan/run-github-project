# GitHub 项目自动运行 Agent 🤖

一个智能的命令行工具，可以自动检查和安装所需依赖，然后克隆并运行任何 GitHub 项目。

## ✨ 功能特性

- 🔍 **自动依赖检测**：智能检查系统是否安装了必要的工具
- 📦 **自动安装工具链**：按需安装缺失的工具
  - Homebrew（macOS 包管理器）
  - Git（版本控制）
  - NVM（Node 版本管理器）
  - Node.js 和 npm
  - pnpm（快速的包管理器）
- 📥 **智能克隆**：自动克隆 GitHub 仓库
- 🎯 **智能包管理器检测**：自动识别项目使用的包管理器（pnpm/yarn/npm）
- 🚀 **一键运行**：自动安装依赖并启动项目

## 📋 系统要求

- macOS 系统
- Python 3.6+
- 互联网连接

## 🚀 快速开始

### 安装

克隆此仓库：

```bash
git clone https://github.com/yourusername/run-github-project.git
cd run-github-project
```

### 使用方法

基本用法：

```bash
python run_github_project.py <github_url>
```

使用代理（解决网络问题）：

```bash
python run_github_project.py <github_url> --proxy http://127.0.0.1:7890
```

使用 SSH 方式克隆：

```bash
python run_github_project.py <github_url> --ssh
```

检查网络连接：

```bash
python run_github_project.py <github_url> --check-network
```

查看所有选项：

```bash
python run_github_project.py --help
```

### 命令行参数

- `github_url`: GitHub 仓库 URL（必需）
- `--proxy, -p`: 设置代理地址，例如 `http://127.0.0.1:7890`
- `--ssh, -s`: 使用 SSH 方式克隆（需要配置 SSH 密钥）
- `--check-network, -c`: 运行前检查网络连接

### 示例

```bash
# 基本使用
python run_github_project.py https://github.com/user/awesome-project

# 使用代理（常见于需要翻墙的情况）
python run_github_project.py https://github.com/user/awesome-project --proxy http://127.0.0.1:7890

# 使用 SSH（需要先配置 GitHub SSH 密钥）
python run_github_project.py https://github.com/user/awesome-project --ssh

# 先检查网络，再克隆
python run_github_project.py https://github.com/user/awesome-project --check-network

# 组合使用
python run_github_project.py https://github.com/user/awesome-project --ssh --check-network
```

### 创建快捷命令（可选）

为了更方便使用，你可以创建一个别名：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
alias run-github="python /path/to/run-github-project/run_github_project.py"

# 然后就可以这样使用
run-github https://github.com/user/awesome-project
```

或者创建一个全局命令：

```bash
# 给脚本添加执行权限
chmod +x run_github_project.py

# 创建符号链接到 PATH 目录
sudo ln -s /path/to/run-github-project/run_github_project.py /usr/local/bin/run-github

# 现在可以直接使用
run-github https://github.com/user/awesome-project
```

## 🔧 工作原理

该工具会按照以下顺序执行：

1. **检查 Homebrew**

   - 如果未安装，自动安装 Homebrew

2. **检查 Git**

   - 如果未安装，使用 Homebrew 安装 Git

3. **克隆项目**

   - 使用 Git 克隆指定的 GitHub 仓库
   - 如果目录已存在，询问是否重新克隆

4. **检测包管理器**

   - 检查项目中的锁文件（pnpm-lock.yaml, yarn.lock, package-lock.json）
   - 智能选择合适的包管理器

5. **检查 Node.js 环境**

   - 如果未安装 npm，检查并安装 NVM
   - 使用 NVM 安装 Node.js LTS 版本
   - 如果需要 pnpm，自动安装

6. **安装依赖**

   - 使用检测到的包管理器安装项目依赖
   - 优先使用 pnpm，其次是 npm

7. **运行项目**
   - 自动执行 `dev` 或 `start` 脚本
   - 实时显示项目输出

## 📝 依赖安装顺序

```
系统
  └─ Homebrew (如果缺失)
      └─ Git (如果缺失)
          └─ NVM (如果 npm 缺失)
              └─ Node.js (如果缺失)
                  └─ pnpm (如果需要且缺失)
```

## 🎯 使用场景

- 🧪 **快速测试开源项目**：想试试某个 GitHub 项目但不想手动配置环境
- 👨‍💻 **新机器配置**：在新的开发机器上快速搭建项目
- 📚 **学习和研究**：快速运行示例项目进行学习
- 🔄 **CI/CD 环境**：在干净的环境中自动化项目部署

## ⚠️ 注意事项

- 首次安装 Homebrew 和其他工具可能需要较长时间
- 某些工具的安装可能需要输入管理员密码
- 确保有足够的磁盘空间用于下载和安装工具
- NVM 安装后可能需要重启终端才能正常使用（脚本会自动处理）

## 🐛 故障排除

### 问题 1：网络连接超时（Failed to connect to github.com）⭐

这是**最常见**的问题，通常出现在无法直接访问 GitHub 的网络环境中。

**解决方案**：

**方法一：使用代理（推荐）**

```bash
# 使用本地代理（如 Clash、V2Ray 等）
python run_github_project.py https://github.com/user/repo --proxy http://127.0.0.1:7890

# 或设置全局代理环境变量
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
python run_github_project.py https://github.com/user/repo
```

**方法二：使用 SSH 方式**

```bash
# 需要先配置 SSH 密钥
python run_github_project.py https://github.com/user/repo --ssh
```

**方法三：配置 Git 代理**

```bash
# 为 Git 设置代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 然后正常运行脚本
python run_github_project.py https://github.com/user/repo
```

**方法四：使用国内镜像**

```bash
# 将 GitHub URL 替换为镜像地址
# 例如: github.com -> hub.fastgit.xyz
python run_github_project.py https://hub.fastgit.xyz/user/repo
```

### 问题 2：SSH Permission denied

**解决方案**：

1. 检查 SSH 密钥配置：

   ```bash
   ssh -T git@github.com
   ```

2. 如果没有 SSH 密钥，生成新的：

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   cat ~/.ssh/id_ed25519.pub  # 复制并添加到 GitHub
   ```

3. 或使用 HTTPS 方式（不加 --ssh 参数）

### 问题 3：Homebrew 安装失败

**解决方案**：

- 检查网络连接
- 使用代理或 VPN
- 手动安装 Homebrew：https://brew.sh/
- 使用国内镜像：https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/

### 问题 4：Git 克隆失败

**解决方案**：

- 检查 GitHub URL 是否正确
- 确认仓库是公开的，或者你有访问权限
- 检查 SSH 密钥配置（对于 SSH URL）：`ssh -T git@github.com`
- 使用代理或 SSH 方式

### 问题 5：项目运行失败

**解决方案**：

- 检查项目的 `package.json` 中是否定义了 `dev` 或 `start` 脚本
- 查看项目的 README 了解特殊的运行要求
- 手动进入项目目录查看错误日志
- 检查 Node.js 版本是否符合项目要求

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

Created with ❤️ for the developer community
