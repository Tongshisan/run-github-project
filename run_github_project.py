#!/usr/bin/env python3
"""
GitHub 项目自动运行 Agent
自动检查和安装所需依赖，克隆并运行 GitHub 项目
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


class GitHubProjectRunner:
    def __init__(self, github_url: str, use_proxy: str = None, use_ssh: bool = False):
        self.github_url = github_url
        self.use_proxy = use_proxy
        self.use_ssh = use_ssh
        self.project_name = self._extract_project_name(github_url)
        self.project_path = Path.cwd() / self.project_name
        
        # 如果指定使用代理，设置环境变量
        if self.use_proxy:
            os.environ['http_proxy'] = self.use_proxy
            os.environ['https_proxy'] = self.use_proxy
            os.environ['HTTP_PROXY'] = self.use_proxy
            os.environ['HTTPS_PROXY'] = self.use_proxy
            print(f"🌐 使用代理: {self.use_proxy}")
        
    def _extract_project_name(self, url: str) -> str:
        """从 GitHub URL 提取项目名称"""
        # 处理各种 URL 格式
        # https://github.com/user/repo.git
        # https://github.com/user/repo
        # git@github.com:user/repo.git
        url = url.rstrip('/')
        if url.endswith('.git'):
            url = url[:-4]
        project_name = url.split('/')[-1]
        return project_name
    
    def _convert_to_ssh_url(self, url: str) -> str:
        """将 HTTPS URL 转换为 SSH URL"""
        # https://github.com/user/repo -> git@github.com:user/repo.git
        if url.startswith('https://github.com/'):
            path = url.replace('https://github.com/', '')
            if not path.endswith('.git'):
                path += '.git'
            return f'git@github.com:{path}'
        return url
    
    def check_network_connectivity(self) -> bool:
        """检查网络连接"""
        print("🔍 检查网络连接...")
        # 尝试 ping github.com
        returncode, stdout, stderr = self.run_command('ping -c 1 -W 2 github.com')
        if returncode == 0:
            print("✅ 网络连接正常")
            return True
        else:
            print("⚠️  无法连接到 github.com")
            return False
    
    def run_command(self, command: str, shell: bool = True, check: bool = False) -> tuple[int, str, str]:
        """执行命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                check=check
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
        except Exception as e:
            return -1, "", str(e)
    
    def check_command_exists(self, command: str) -> bool:
        """检查命令是否存在"""
        return shutil.which(command) is not None
    
    def install_homebrew(self) -> bool:
        """安装 Homebrew"""
        print("📦 检测到系统缺少 Homebrew，正在安装...")
        install_script = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        returncode, stdout, stderr = self.run_command(install_script)
        
        if returncode == 0:
            print("✅ Homebrew 安装成功")
            # 刷新环境变量
            self._refresh_brew_env()
            return True
        else:
            print(f"❌ Homebrew 安装失败: {stderr}")
            return False
    
    def _refresh_brew_env(self):
        """刷新 Homebrew 环境变量"""
        # 在 M1/M2 Mac 上，Homebrew 安装在 /opt/homebrew
        brew_paths = ['/opt/homebrew/bin', '/usr/local/bin']
        for brew_path in brew_paths:
            if os.path.exists(brew_path) and brew_path not in os.environ['PATH']:
                os.environ['PATH'] = f"{brew_path}:{os.environ['PATH']}"
    
    def install_git(self) -> bool:
        """安装 Git"""
        print("📦 检测到系统缺少 Git，正在安装...")
        
        # 确保 Homebrew 可用
        if not self.check_command_exists('brew'):
            if not self.install_homebrew():
                return False
        
        returncode, stdout, stderr = self.run_command('brew install git')
        if returncode == 0:
            print("✅ Git 安装成功")
            return True
        else:
            print(f"❌ Git 安装失败: {stderr}")
            return False
    
    def install_nvm(self) -> bool:
        """安装 NVM"""
        print("📦 检测到系统缺少 NVM，正在安装...")
        
        # 下载并安装 NVM
        install_script = 'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash'
        returncode, stdout, stderr = self.run_command(install_script)
        
        if returncode == 0:
            print("✅ NVM 安装成功")
            # 设置 NVM 环境变量
            self._setup_nvm_env()
            return True
        else:
            print(f"❌ NVM 安装失败: {stderr}")
            return False
    
    def _setup_nvm_env(self):
        """设置 NVM 环境变量"""
        nvm_dir = os.path.expanduser('~/.nvm')
        os.environ['NVM_DIR'] = nvm_dir
        
    def _source_nvm(self) -> str:
        """返回 source NVM 的命令前缀"""
        nvm_dir = os.path.expanduser('~/.nvm')
        return f'export NVM_DIR="{nvm_dir}" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '
    
    def install_node(self) -> bool:
        """使用 NVM 安装 Node.js"""
        print("📦 检测到系统缺少 Node.js，正在安装...")
        
        # 检查 NVM 是否存在
        nvm_dir = os.path.expanduser('~/.nvm')
        if not os.path.exists(nvm_dir):
            if not self.install_nvm():
                return False
        
        # 使用 NVM 安装 Node.js LTS 版本
        nvm_command = self._source_nvm() + 'nvm install --lts'
        returncode, stdout, stderr = self.run_command(nvm_command)
        
        if returncode == 0:
            print("✅ Node.js 安装成功")
            return True
        else:
            print(f"❌ Node.js 安装失败: {stderr}")
            return False
    
    def install_pnpm(self) -> bool:
        """安装 pnpm"""
        print("📦 检测到系统缺少 pnpm，正在安装...")
        
        # 确保 npm 可用
        if not self.check_npm_available():
            if not self.install_node():
                return False
        
        # 使用 npm 安装 pnpm
        npm_command = self._get_npm_command('npm install -g pnpm')
        returncode, stdout, stderr = self.run_command(npm_command)
        
        if returncode == 0:
            print("✅ pnpm 安装成功")
            return True
        else:
            print(f"❌ pnpm 安装失败: {stderr}")
            return False
    
    def check_npm_available(self) -> bool:
        """检查 npm 是否可用（包括通过 nvm 安装的）"""
        if self.check_command_exists('npm'):
            return True
        
        # 尝试通过 NVM 查找 npm
        nvm_dir = os.path.expanduser('~/.nvm')
        if os.path.exists(nvm_dir):
            nvm_command = self._source_nvm() + 'npm --version'
            returncode, stdout, stderr = self.run_command(nvm_command)
            return returncode == 0
        
        return False
    
    def _get_npm_command(self, npm_cmd: str) -> str:
        """获取 npm 命令，如果需要则加上 nvm source"""
        if self.check_command_exists('npm'):
            return npm_cmd
        else:
            return self._source_nvm() + npm_cmd
    
    def _get_pnpm_command(self, pnpm_cmd: str) -> str:
        """获取 pnpm 命令，如果需要则加上 nvm source"""
        if self.check_command_exists('pnpm'):
            return pnpm_cmd
        else:
            return self._source_nvm() + pnpm_cmd
    
    def clone_repository(self) -> bool:
        """克隆 Git 仓库"""
        print(f"📥 正在克隆项目: {self.github_url}")
        
        # 确保 Git 可用
        if not self.check_command_exists('git'):
            if not self.install_git():
                return False
        
        # 检查目录是否已存在
        if self.project_path.exists():
            print(f"⚠️  项目目录已存在: {self.project_path}")
            user_input = input("是否删除现有目录并重新克隆? (y/N): ").strip().lower()
            if user_input == 'y':
                shutil.rmtree(self.project_path)
                print("🗑️  已删除现有目录")
            else:
                print("ℹ️  使用现有项目目录")
                return True
        
        # 决定使用的 URL
        clone_url = self.github_url
        if self.use_ssh:
            clone_url = self._convert_to_ssh_url(self.github_url)
            print(f"🔑 使用 SSH 方式克隆: {clone_url}")
        
        # 克隆仓库
        returncode, stdout, stderr = self.run_command(f'git clone {clone_url}')
        
        if returncode == 0:
            print(f"✅ 项目克隆成功: {self.project_path}")
            return True
        else:
            print(f"❌ 项目克隆失败: {stderr}")
            
            # 提供故障排除建议
            if 'Failed to connect' in stderr or 'Operation timed out' in stderr:
                print("\n💡 网络连接问题，建议尝试：")
                print("   1. 使用代理: --proxy http://127.0.0.1:7890")
                print("   2. 使用 SSH: --ssh (需要配置 SSH 密钥)")
                print("   3. 检查网络连接和防火墙设置")
            elif 'Permission denied' in stderr:
                print("\n💡 权限问题，建议：")
                print("   1. 检查 SSH 密钥配置: ssh -T git@github.com")
                print("   2. 或使用 HTTPS 方式克隆")
            
            return False
    
    def detect_package_manager(self) -> str:
        """检测项目使用的包管理器"""
        if (self.project_path / 'pnpm-lock.yaml').exists():
            return 'pnpm'
        elif (self.project_path / 'yarn.lock').exists():
            return 'yarn'
        elif (self.project_path / 'package-lock.json').exists():
            return 'npm'
        elif (self.project_path / 'package.json').exists():
            return 'npm'  # 默认使用 npm
        else:
            return None
    
    def install_dependencies(self) -> bool:
        """安装项目依赖"""
        print("📦 正在安装项目依赖...")
        
        if not (self.project_path / 'package.json').exists():
            print("ℹ️  未检测到 package.json，跳过依赖安装")
            return True
        
        package_manager = self.detect_package_manager()
        print(f"🔍 检测到包管理器: {package_manager}")
        
        # 切换到项目目录
        os.chdir(self.project_path)
        
        # 优先使用 pnpm
        if package_manager == 'pnpm' or self.check_command_exists('pnpm'):
            if not self.check_command_exists('pnpm'):
                if not self.install_pnpm():
                    print("⚠️  pnpm 安装失败，尝试使用 npm")
                    package_manager = 'npm'
                else:
                    package_manager = 'pnpm'
            else:
                package_manager = 'pnpm'
        
        # 如果不是 pnpm，使用 npm
        if package_manager != 'pnpm':
            if not self.check_npm_available():
                if not self.install_node():
                    return False
            package_manager = 'npm'
        
        # 执行安装
        if package_manager == 'pnpm':
            install_cmd = self._get_pnpm_command('pnpm install')
        else:
            install_cmd = self._get_npm_command('npm install')
        
        print(f"🔧 执行: {package_manager} install")
        returncode, stdout, stderr = self.run_command(install_cmd)
        
        if returncode == 0:
            print("✅ 依赖安装成功")
            return True
        else:
            print(f"❌ 依赖安装失败: {stderr}")
            return False
    
    def run_project(self) -> bool:
        """运行项目"""
        print("🚀 正在启动项目...")
        
        if not (self.project_path / 'package.json').exists():
            print("ℹ️  未检测到 package.json，无法自动运行项目")
            print(f"✅ 项目已准备就绪: {self.project_path}")
            return True
        
        # 检测使用的包管理器
        package_manager = self.detect_package_manager()
        
        # 优先使用 pnpm
        if self.check_command_exists('pnpm') or package_manager == 'pnpm':
            run_cmd = self._get_pnpm_command('pnpm dev || pnpm start')
        else:
            run_cmd = self._get_npm_command('npm run dev || npm start')
        
        print(f"🔧 执行: {package_manager} run dev/start")
        print(f"📁 项目目录: {self.project_path}")
        print("\n" + "="*50)
        print("项目正在运行中...")
        print("按 Ctrl+C 停止")
        print("="*50 + "\n")
        
        # 在项目目录中运行
        os.chdir(self.project_path)
        
        try:
            # 直接运行，输出显示给用户
            subprocess.run(run_cmd, shell=True)
        except KeyboardInterrupt:
            print("\n\n⏹️  项目已停止")
        
        return True
    
    def run(self):
        """执行完整的流程"""
        print("=" * 60)
        print("🤖 GitHub 项目自动运行 Agent")
        print("=" * 60)
        print(f"📍 目标仓库: {self.github_url}\n")
        
        # 1. 克隆项目
        if not self.clone_repository():
            print("❌ 流程终止：克隆项目失败")
            sys.exit(1)
        
        # 2. 安装依赖
        if not self.install_dependencies():
            print("❌ 流程终止：安装依赖失败")
            sys.exit(1)
        
        # 3. 运行项目
        self.run_project()
        
        print("\n" + "=" * 60)
        print("✅ 流程完成")
        print("=" * 60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='GitHub 项目自动运行工具 - 自动安装依赖并运行任何 GitHub 项目',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_github_project.py https://github.com/user/repo
  python run_github_project.py https://github.com/user/repo --proxy http://127.0.0.1:7890
  python run_github_project.py https://github.com/user/repo --ssh
  python run_github_project.py https://github.com/user/repo --check-network
        """
    )
    
    parser.add_argument('github_url', help='GitHub 仓库 URL')
    parser.add_argument('--proxy', '-p', help='代理地址，例如: http://127.0.0.1:7890')
    parser.add_argument('--ssh', '-s', action='store_true', help='使用 SSH 方式克隆（需要配置 SSH 密钥）')
    parser.add_argument('--check-network', '-c', action='store_true', help='运行前检查网络连接')
    
    args = parser.parse_args()
    
    # 如果需要，先检查网络
    if args.check_network:
        runner_temp = GitHubProjectRunner(args.github_url)
        if not runner_temp.check_network_connectivity():
            print("\n⚠️  网络连接异常，可能需要使用代理")
            sys.exit(1)
    
    runner = GitHubProjectRunner(
        github_url=args.github_url,
        use_proxy=args.proxy,
        use_ssh=args.ssh
    )
    runner.run()


if __name__ == "__main__":
    main()

