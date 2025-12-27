#!/usr/bin/env python3
"""
辅助脚本：自动加载项目目录下的 .env 文件
"""

import os
from pathlib import Path


def load_env_file(env_path: Path = None):
    """
    加载 .env 文件到环境变量
    
    Args:
        env_path: .env 文件路径，默认为当前目录下的 .env
    """
    if env_path is None:
        # 获取脚本所在目录的 .env 文件
        script_dir = Path(__file__).parent
        env_path = script_dir / '.env'
    
    if not env_path.exists():
        print(f"⚠️  未找到配置文件: {env_path}")
        print(f"💡 提示: 复制 .env.example 为 .env 并填入你的 API keys")
        return False
    
    print(f"📝 加载配置文件: {env_path}")
    
    loaded_count = 0
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            
            # 解析 KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 只有当值不为空时才设置
                if value:
                    os.environ[key] = value
                    loaded_count += 1
                    # 隐藏敏感信息
                    display_value = value[:10] + '...' if len(value) > 10 else value
                    print(f"  ✅ {key} = {display_value}")
    
    print(f"✅ 成功加载 {loaded_count} 个配置项\n")
    return True


if __name__ == '__main__':
    # 直接运行此脚本可以测试加载
    load_env_file()
    
    # 显示已加载的配置
    print("当前环境变量:")
    for key in ['DEEPSEEK_API_KEY', 'OPENAI_API_KEY', 'GITHUB_TOKEN']:
        value = os.getenv(key)
        if value:
            print(f"  {key}: {value[:10]}...")
        else:
            print(f"  {key}: (未设置)")

