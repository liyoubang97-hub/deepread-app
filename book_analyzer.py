"""
DeepRead - 书籍深度解析模块
使用免费API实现书籍信息获取和深度分析
"""

import os
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
from datetime import datetime

# 推荐使用 Groq API (免费额度大，速度快)
# 注册地址: https://groq.com
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

@dataclass
class BookInfo:
    """书籍信息数据类"""
    title: str
    author: str
    isbn: Optional[str] = None
    published_date: Optional[str] = None
    description: Optional[str] = None
    page_count: Optional[int] = None
    categories: List[str] = None
    cover_url: Optional[str] = None
    average_rating: Optional[float] = None

    def __post_init__(self):
        if self.categories is None:
            self.categories = []


class BookDataFetcher:
    """书籍数据获取器 - 使用免费API"""

    def __init__(self):
        self.google_books_api = "https://www.googleapis.com/books/v1/volumes"
        self.open_library_api = "https://openlibrary.org"

    def search_by_title(self, title: str, lang: str = "zh") -> Optional[BookInfo]:
        """
        通过书名搜索书籍信息
        优先使用 Google Books API，降级到 Open Library
        """
        # 先尝试 Google Books
        book_info = self._fetch_from_google_books(title, lang)
        if book_info:
            return book_info

        # 降级到 Open Library
        return self._fetch_from_open_library(title)

    def _fetch_from_google_books(self, title: str, lang: str) -> Optional[BookInfo]:
        """从 Google Books API 获取书籍信息"""
        try:
            params = {
                "q": title,
                "langRestrict": lang,
                "maxResults": 1,
                "printType": "books"
            }
            response = requests.get(self.google_books_api, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("totalItems", 0) == 0:
                return None

            volume = data["items"][0]
            info = volume.get("volumeInfo", {})

            # 提取作者信息
            authors = info.get("authors", [])
            author = authors[0] if authors else "未知作者"

            # 提取ISBN
            identifiers = info.get("industryIdentifiers", [])
            isbn = next(
                (id_obj.get("identifier") for id_obj in identifiers
                 if id_obj.get("type") in ["ISBN_10", "ISBN_13"]),
                None
            )

            return BookInfo(
                title=info.get("title", title),
                author=author,
                isbn=isbn,
                published_date=info.get("publishedDate"),
                description=info.get("description"),
                page_count=info.get("pageCount"),
                categories=info.get("categories", []),
                cover_url=info.get("imageLinks", {}).get("thumbnail"),
                average_rating=info.get("averageRating")
            )
        except Exception as e:
            print(f"Google Books API 错误: {e}")
            return None

    def _fetch_from_open_library(self, title: str) -> Optional[BookInfo]:
        """从 Open Library 获取书籍信息（降级方案）"""
        try:
            # Open Library 搜索接口
            search_url = f"{self.open_library_api}/search.json"
            params = {"title": title, "limit": 1}
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("numFound", 0) == 0:
                return None

            docs = data.get("docs", [])[0]

            # 获取完整信息
            work_key = docs.get("key", "")
            if work_key:
                work_url = f"{self.open_library_api}{work_key}.json"
                work_response = requests.get(work_url, timeout=10)
                work_data = work_response.json.json()

                return BookInfo(
                    title=docs.get("title", title),
                    author=docs.get("author_name", ["未知作者"])[0],
                    isbn=docs.get("isbn", [None])[0],
                    published_date=docs.get("first_publish_year"),
                    description=work_data.get("description"),
                    page_count=docs.get("number_of_pages"),
                    categories=docs.get("subject", []),
                    cover_url=f"https://covers.openlibrary.org/b/OLID/{work_key.split('/')[-1]}-M.jpg"
                )
        except Exception as e:
            print(f"Open Library 错误: {e}")
            return None


class BookDeepAnalyzer:
    """书籍深度分析器 - 使用LLM生成深度解读"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def analyze_book(self, book_info: BookInfo) -> Dict:
        """
        对书籍进行深度分析
        返回: {
            "key_insights": List[str],  # 核心观点
            "mind_map": Dict,           # 思维导图结构
            "quotes": List[str],        # 金句卡片
            "reading_plan": Dict,       # 阅读计划
            "difficulty": str,          # 难度评级
            "estimated_hours": float    # 预计阅读时长
        }
        """
        prompt = self._build_analysis_prompt(book_info)

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",  # 或 "mixtral-8x7b-32768"
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "response_format": {"type": "json_object"}
                },
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)

        except Exception as e:
            print(f"LLM分析错误: {e}")
            return self._fallback_analysis(book_info)

    def _build_analysis_prompt(self, book_info: BookInfo) -> str:
        """构建分析提示词"""
        return f"""你是一位专业的阅读顾问和书籍分析师。请对以下书籍进行深度分析，并以JSON格式返回结果。

书籍信息：
- 书名：{book_info.title}
- 作者：{book_info.author}
- 分类：{', '.join(book_info.categories)}
- 简介：{book_info.description or '暂无简介'}

请提供以下分析（必须是JSON格式）：
{{
  "key_insights": [
    "核心观点1：具体解释...",
    "核心观点2：具体解释...",
    "核心观点3：具体解释...",
    "核心观点4：具体解释...",
    "核心观点5：具体解释..."
  ],
  "mind_map": {{
    "中心主题": "书名或核心概念",
    "主要分支": [
      {{
        "分支名": "分支1",
        "子节点": ["概念1", "概念2"]
      }},
      {{
        "分支名": "分支2",
        "子节点": ["概念1", "概念2"]
      }}
    ]
  }},
  "quotes": [
    "金句1（可以是书中原话或基于内容的总结性金句）",
    "金句2",
    "金句3",
    "金句4",
    "金句5"
  ],
  "reading_plan": {{
    "week1": "第1-2章：阅读重点说明",
    "week2": "第3-5章：阅读重点说明",
    "week3": "第6-8章：阅读重点说明",
    "week4": "第9章及总结：阅读重点说明"
  }},
  "difficulty": "初级/中级/高级",
  "estimated_hours": 8.5,
  "target_readers": ["读者类型1", "读者类型2"],
  "prerequisite_knowledge": ["需要了解的基础概念1", "概念2"]
}}

注意：
1. 核心观点要具体、有洞见，不是简单的内容摘要
2. 金句要适合分享到社交媒体
3. 阅读计划要具体到每周重点
4. 难度评级要准确
5. 预计阅读时长基于普通读者（每小时20-30页）"""

    def _fallback_analysis(self, book_info: BookInfo) -> Dict:
        """降级方案：当API失败时返回基础分析"""
        return {
            "key_insights": [
                f"《{book_info.title}》是{book_info.author}的著作",
                "本书探讨的主题具有重要价值",
                "建议深入阅读并做笔记",
                "可以结合实际案例思考",
                "值得反复品读和实践"
            ],
            "mind_map": {
                "中心主题": book_info.title,
                "主要分支": [
                    {"分支名": "核心观点", "子节点": ["观点1", "观点2"]},
                    {"分支名": "实践应用", "子节点": ["应用1", "应用2"]}
                ]
            },
            "quotes": [
                f"来自《{book_info.title}》的思考",
                "深度阅读带来深度思考",
                "知识需要实践才能转化为智慧"
            ],
            "reading_plan": {
                "week1": "阅读前半部分，理解核心概念",
                "week2": "阅读后半部分，思考应用场景",
                "week3": "重读重点章节，做笔记",
                "week4": "总结实践，写读后感"
            },
            "difficulty": "中级",
            "estimated_hours": book_info.page_count / 25 if book_info.page_count else 10,
            "target_readers": ["对该领域感兴趣的读者"],
            "prerequisite_knowledge": []
        }


# 使用示例
if __name__ == "__main__":
    # 初始化
    fetcher = BookDataFetcher()
    analyzer = BookDeepAnalyzer()

    # 搜索书籍
    book = fetcher.search_by_title("思考，快与慢")

    if book:
        print(f"找到书籍：{book.title} - {book.author}")
        print(f"分类：{book.categories}")
        print(f"简介：{book.description[:200]}...")

        # 深度分析
        analysis = analyzer.analyze_book(book)

        print("\n=== 核心观点 ===")
        for insight in analysis["key_insights"]:
            print(f"• {insight}")

        print("\n=== 金句卡片 ===")
        for quote in analysis["quotes"]:
            print(f"  {quote}")
