# 使用示例和常见场景

## 场景 1：网络正常，直接克隆

最简单的使用方式：

```bash
python run_github_project.py https://github.com/vitejs/vite
```

## 场景 2：需要使用代理（最常见）

如果你在国内或无法直接访问 GitHub：

```bash
# 方式 1：使用命令行参数
python run_github_project.py https://github.com/user/repo --proxy http://127.0.0.1:7890

# 方式 2：先设置环境变量
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
python run_github_project.py https://github.com/user/repo

# 方式 3：配置 Git 全局代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
python run_github_project.py https://github.com/user/repo
```

### 常见代理端口

- Clash: `http://127.0.0.1:7890`
- V2Ray: `http://127.0.0.1:1080` 或 `socks5://127.0.0.1:1080`
- Shadowsocks: `socks5://127.0.0.1:1080`

## 场景 3：使用 SSH 克隆

如果你已经配置了 SSH 密钥：

```bash
python run_github_project.py https://github.com/user/repo --ssh
```

脚本会自动将 HTTPS URL 转换为 SSH URL。

## 场景 4：先检查网络再运行

```bash
python run_github_project.py https://github.com/user/repo --check-network
```

## 场景 5：组合使用

```bash
# SSH + 网络检查
python run_github_project.py https://github.com/user/repo --ssh --check-network

# 代理 + 网络检查
python run_github_project.py https://github.com/user/repo --proxy http://127.0.0.1:7890 --check-network
```

## 场景 6：测试小型项目

推荐用于测试的轻量级项目：

```bash
# Vite React 模板
python run_github_project.py https://github.com/vitejs/vite --proxy http://127.0.0.1:7890

# Next.js 示例
python run_github_project.py https://github.com/vercel/next.js/tree/canary/examples/blog-starter --proxy http://127.0.0.1:7890
```

## 查看帮助

```bash
python run_github_project.py --help
```

## 完整的工作流示例

```bash
# 1. 克隆并进入项目
cd ~/projects
python run_github_project.py https://github.com/user/awesome-app --proxy http://127.0.0.1:7890

# 脚本会自动：
# - 检查并安装 Homebrew（如果需要）
# - 检查并安装 Git（如果需要）
# - 使用代理克隆项目
# - 检测项目使用的包管理器
# - 安装 Node.js 和 pnpm/npm（如果需要）
# - 安装项目依赖
# - 运行项目（npm run dev 或 npm start）

# 2. 项目运行后，按 Ctrl+C 停止
# 3. 手动进入项目目录继续开发
cd awesome-app
code .  # 用编辑器打开
```

