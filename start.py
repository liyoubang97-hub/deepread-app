"""
DeepRead 快速启动脚本
自动检测环境并启动应用
"""

import os
import sys
import subprocess
from pathlib import Path

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 10):
        print("❌ 需要Python 3.10或更高版本")
        print(f"   当前版本: {sys.version}")
        return False
    print(f"✅ Python版本: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        "streamlit",
        "requests",
        "chromadb",
        "sentence_transformers",
        "edge_tts"
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("⚠️ 缺少以下依赖包:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n💡 安装命令: pip install -r requirements.txt")
        return False

    print("✅ 所有依赖已安装")
    return True


def check_api_key():
    """检查API配置"""
    groq_key = os.getenv("GROQ_API_KEY", "")

    if groq_key and groq_key != "your_groq_api_key_here":
        print("✅ Groq API Key已配置")
        return True

    print("⚠️ 未检测到Groq API Key")
    print("\n💡 你有两个选择:")
    print("   1. 使用免费API（推荐）:")
    print("      - 访问 https://groq.com 注册")
    print("      - 创建 .env 文件并填入 GROQ_API_KEY")
    print("\n   2. 使用本地模型（完全免费，但需要8GB+内存）:")
    print("      - 下载Ollama: https://ollama.com/download")
    print("      - 运行: ollama pull llama3:8b")
    print("      - 运行: ollama serve")

    choice = input("\n是否继续？(y/n): ").lower()
    return choice == "y"


def check_ollama():
    """检查Ollama是否运行"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ 检测到Ollama服务（本地模型可用）")
            return True
    except:
        pass
    return False


def create_env_file():
    """创建.env文件"""
    env_file = Path(".env")
    if not env_file.exists():
        example_file = Path(".env.example")

        if example_file.exists():
            import shutil
            shutil.copy(example_file, env_file)
            print("✅ 已创建 .env 配置文件")
            print("💡 请编辑 .env 文件并填入你的API Key")
        else:
            print("⚠️ 未找到 .env.example")
    else:
        print("✅ .env 文件已存在")


def create_directories():
    """创建必要的目录"""
    dirs = ["knowledge_db", "podcasts"]

    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)

    print("✅ 工作目录已准备就绪")


def main():
    print("=" * 60)
    print("📚 DeepRead 深度阅读工具 - 启动检查")
    print("=" * 60)
    print()

    # 检查Python版本
    if not check_python_version():
        sys.exit(1)

    # 检查依赖
    if not check_dependencies():
        install = input("\n是否现在安装依赖？(y/n): ").lower()
        if install == "y":
            print("\n📦 安装依赖中...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            sys.exit(1)

    # 检查Ollama
    has_ollama = check_ollama()

    # 如果没有Ollama，检查API Key
    if not has_ollama:
        if not check_api_key():
            print("\n💡 提示：你可以先使用免费功能（书籍搜索），稍后配置AI功能")
            print("   继续 y，退出 n")
            choice = input("\n是否继续启动？(y/n): ").lower()
            if choice != "y":
                sys.exit(1)

    # 创建配置文件
    create_env_file()
    create_directories()

    print("\n" + "=" * 60)
    print("🚀 启动DeepRead")
    print("=" * 60)
    print("\n浏览器将自动打开: http://localhost:8501")
    print("按 Ctrl+C 停止服务\n")

    # 启动Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 DeepRead已停止")


if __name__ == "__main__":
    main()
