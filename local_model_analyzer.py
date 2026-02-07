"""
DeepRead - 本地模型分析器（无需API Key）
使用Ollama本地运行，完全免费
"""

import requests
import json
from typing import Dict, List
from pathlib import Path

# 导入基础类
from book_analyzer import BookInfo, BookDeepAnalyzer


class LocalBookAnalyzer(BookDeepAnalyzer):
    """
    使用本地Ollama模型的书籍分析器
    完全免费，无需API Key
    """

    def __init__(self, model_name: str = "llama3:8b", base_url: str = "http://localhost:11434"):
        """
        初始化本地模型分析器

        Args:
            model_name: Ollama模型名称，推荐 "llama3:8b" 或 "qwen2:7b"
            base_url: Ollama服务地址

        使用前需要：
        1. 安装Ollama: https://ollama.com/download
        2. 下载模型: ollama pull llama3:8b
        3. 启动服务: ollama serve
        """
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"

        # 测试连接
        self._check_connection()

    def _check_connection(self):
        """检查Ollama服务是否运行"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]

                if self.model_name not in model_names:
                    print(f"⚠️ 模型 {self.model_name} 未安装")
                    print(f"📦 已安装的模型: {', '.join(model_names)}")
                    print(f"💡 安装命令: ollama pull {self.model_name}")
                else:
                    print(f"✅ 已连接到Ollama，使用模型: {self.model_name}")
            else:
                print("❌ 无法连接到Ollama服务")
                print("💡 请确保Ollama已安装并运行: ollama serve")
        except Exception as e:
            print(f"❌ 连接错误: {e}")
            print("💡 请先安装并启动Ollama")

    def analyze_book(self, book_info: BookInfo) -> Dict:
        """
        使用本地模型分析书籍
        注意：本地模型可能比API慢，但完全免费
        """
        prompt = self._build_analysis_prompt(book_info)

        try:
            print(f"🤖 使用本地模型 {self.model_name} 分析中...")
            print("⏳ 这可能需要1-3分钟，请稍候...")

            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 4096
                    }
                },
                timeout=300  # 5分钟超时
            )
            response.raise_for_status()

            result = response.json()
            content = result.get("response", "")

            # 尝试解析JSON（Ollama可能返回JSON前后的文字）
            # 查找JSON部分
            json_start = content.find("{")
            json_end = content.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                analysis = json.loads(json_str)
                print("✅ 分析完成！")
                return analysis
            else:
                print("⚠️ 无法解析JSON，使用降级方案")
                return self._fallback_analysis(book_info)

        except Exception as e:
            print(f"❌ 本地模型分析错误: {e}")
            return self._fallback_analysis(book_info)


# 使用示例和测试
if __name__ == "__main__":
    print("=" * 60)
    print("DeepRead - 本地模型分析器")
    print("=" * 60)

    # 检查Ollama是否安装
    print("\n📋 检查Ollama安装状态...")

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama正在运行")
            print(f"📦 已安装的模型:")
            for model in models:
                print(f"   - {model['name']} ({model.get('size', 0) / 1024**3:.1f}GB)")

            print("\n" + "=" * 60)
            print("测试本地分析器")
            print("=" * 60)

            # 使用本地模型
            from book_analyzer import BookDataFetcher

            fetcher = BookDataFetcher()
            book = fetcher.search_by_title("原子习惯")

            if book:
                print(f"\n📖 书籍: {book.title} - {book.author}")

                # 使用本地分析器
                analyzer = LocalBookAnalyzer(model_name="llama3:8b")
                analysis = analyzer.analyze_book(book)

                print("\n✨ 核心观点:")
                for i, insight in enumerate(analysis.get("key_insights", []), 1):
                    print(f"{i}. {insight}")

        else:
            print("❌ Ollama未运行")
            print("\n💡 快速开始:")
            print("   1. 下载Ollama: https://ollama.com/download")
            print("   2. 安装后运行: ollama serve")
            print("   3. 下载模型: ollama pull llama3:8b")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        print("\n💡 快速开始:")
        print("   1. 下载Ollama: https://ollama.com/download")
        print("   2. 安装后运行: ollama serve")
        print("   3. 下载模型: ollama pull llama3:8b")

    print("\n" + "=" * 60)
