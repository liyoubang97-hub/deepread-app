"""
DeepRead 基础功能测试
测试书籍搜索和分析功能（不依赖ChromaDB）
"""

import os
import sys
import requests
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from book_analyzer import BookDataFetcher, BookDeepAnalyzer


def test_book_search():
    """测试书籍搜索功能"""
    print("\n" + "="*60)
    print("测试1: 书籍搜索功能")
    print("="*60)

    fetcher = BookDataFetcher()

    # 测试中文书籍
    print("\n搜索: 原子习惯")
    book = fetcher.search_by_title("原子习惯")

    if book:
        print(f"✅ 找到书籍!")
        print(f"   书名: {book.title}")
        print(f"   作者: {book.author}")
        print(f"   分类: {book.categories}")
        return book
    else:
        print("❌ 未找到书籍")
        return None


def test_book_analysis(book):
    """测试书籍分析功能（需要API Key）"""
    print("\n" + "="*60)
    print("测试2: 书籍深度分析功能")
    print("="*60)

    api_key = os.getenv("GROQ_API_KEY", "")

    if not api_key:
        print("⚠️ 未设置GROQ_API_KEY")
        print("\n你可以:")
        print("1. 访问 https://groq.com 注册免费API Key")
        print("2. 设置环境变量: set GROQ_API_KEY=你的key")
        print("3. 或者跳过此测试")
        return False

    analyzer = BookDeepAnalyzer(api_key=api_key)

    print(f"\n正在分析《{book.title}》...")
    print("⏳ 这可能需要30-60秒...")

    try:
        analysis = analyzer.analyze_book(book)

        print("\n✅ 分析完成!")
        print("\n核心观点:")
        for i, insight in enumerate(analysis.get("key_insights", [])[:3], 1):
            print(f"\n{i}. {insight}")

        print("\n金句卡片:")
        for quote in analysis.get("quotes", [])[:3]:
            print(f"\n  \"{quote}\"")

        return True

    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        print("\n可能的原因:")
        print("1. API Key无效")
        print("2. 网络连接问题")
        print("3. API额度用完")
        return False


def test_local_mode():
    """测试本地降级模式"""
    print("\n" + "="*60)
    print("测试3: 本地降级模式")
    print("="*60)

    print("\n即使没有API Key，也能使用基础功能:")

    fetcher = BookDataFetcher()
    book = fetcher.search_by_title("思考，快与慢")

    if book:
        print(f"\n✅ 书籍信息获取成功")
        print(f"   书名: {book.title}")
        print(f"   作者: {book.author}")
        print(f"   简介: {book.description[:100] if book.description else '暂无'}...")

        # 测试降级分析
        analyzer = BookDeepAnalyzer()
        analysis = analyzer._fallback_analysis(book)

        print(f"\n✅ 降级模式生成基础分析")
        print(f"   难度: {analysis['difficulty']}")
        print(f"   预计时长: {analysis['estimated_hours']} 小时")


def main():
    print("="*60)
    print("DeepRead - 基础功能测试")
    print("="*60)
    print(f"\nPython版本: {sys.version.split()[0]}")
    print(f"操作系统: {sys.platform}")

    # 检查依赖
    print("\n检查依赖...")
    try:
        import streamlit
        print("✅ streamlit 已安装")
    except ImportError:
        print("❌ streamlit 未安装")

    try:
        import requests
        print("✅ requests 已安装")
    except ImportError:
        print("❌ requests 未安装")

    try:
        import edge_tts
        print("✅ edge-tts 已安装")
    except ImportError:
        print("⚠️ edge-tts 未安装 (播客功能需要)")

    # 运行测试
    try:
        # 测试1: 书籍搜索
        book = test_book_search()

        if book:
            # 测试2: 深度分析（需要API Key）
            test_book_analysis(book)

        # 测试3: 本地模式
        test_local_mode()

    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print("\n✅ 可用功能:")
    print("   - 书籍搜索 (Google Books API)")
    print("   - 基础信息获取")

    api_key = os.getenv("GROQ_API_KEY", "")
    if api_key:
        print("   - AI深度分析")
    else:
        print("\n💡 要启用AI分析功能:")
        print("   1. 访问 https://groq.com 注册")
        print("   2. 获取API Key")
        print("   3. 设置: set GROQ_API_KEY=你的key")

    print("\n📚 下一步:")
    print("   - 运行 Web界面: streamlit run app.py")
    print("   - 或使用代码: from book_analyzer import *")


if __name__ == "__main__":
    main()
