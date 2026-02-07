"""
DeepRead - 知识库系统
使用ChromaDB实现本地向量存储和知识关联
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from datetime import datetime

# 向量数据库
import chromadb
from chromadb.config import Settings

# 文本嵌入（使用Hugging Face免费模型）
from sentence_transformers import SentenceTransformer


@dataclass
class KnowledgeCard:
    """知识卡片"""
    id: str
    book_title: str
    book_author: str
    content_type: str  # "insight", "quote", "concept", "example"
    content: str
    tags: List[str]
    created_at: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class PersonalKnowledgeBase:
    """个人知识库 - 本地向量存储"""

    def __init__(self, persist_directory: str = "./knowledge_db"):
        """
        初始化知识库
        persist_directory: 数据库存储路径
        """
        self.persist_dir = Path(persist_directory)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        # 初始化ChromaDB（持久化到本地）
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.persist_dir / "chroma")
        )

        # 创建或获取collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_cards",
            metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
        )

        # 初始化嵌入模型（第一次下载后会缓存到本地）
        print("📦 加载嵌入模型（第一次会下载，约400MB）...")
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ 模型加载完成")

    def add_book_knowledge(
        self,
        book_title: str,
        book_author: str,
        analysis: Dict
    ) -> List[str]:
        """
        将书籍分析结果添加到知识库
        返回：添加的卡片ID列表
        """
        card_ids = []
        timestamp = datetime.now().isoformat()

        # 添加核心观点
        for i, insight in enumerate(analysis.get("key_insights", [])):
            card = KnowledgeCard(
                id=f"{book_title}_insight_{i}_{timestamp}",
                book_title=book_title,
                book_author=book_author,
                content_type="insight",
                content=insight,
                tags=[book_title, "核心观点", "深度思考"],
                created_at=timestamp
            )
            self._add_card(card)
            card_ids.append(card.id)

        # 添加金句
        for i, quote in enumerate(analysis.get("quotes", [])):
            card = KnowledgeCard(
                id=f"{book_title}_quote_{i}_{timestamp}",
                book_title=book_title,
                book_author=book_author,
                content_type="quote",
                content=quote,
                tags=[book_title, "金句", "可分享"],
                created_at=timestamp
            )
            self._add_card(card)
            card_ids.append(card.id)

        # 添加概念（从思维导图提取）
        mind_map = analysis.get("mind_map", {})
        for branch in mind_map.get("主要分支", []):
            branch_name = branch.get("分支名", "")
            for concept in branch.get("子节点", []):
                card = KnowledgeCard(
                    id=f"{book_title}_concept_{branch_name}_{concept}_{timestamp}",
                    book_title=book_title,
                    book_author=book_author,
                    content_type="concept",
                    content=f"{branch_name}: {concept}",
                    tags=[book_title, "概念", branch_name],
                    created_at=timestamp
                )
                self._add_card(card)
                card_ids.append(card.id)

        print(f"✅ 已添加 {len(card_ids)} 张知识卡片到知识库")
        return card_ids

    def _add_card(self, card: KnowledgeCard):
        """添加单张卡片到向量数据库"""
        # 生成embedding
        text_to_embed = f"{card.content_type}: {card.content}"
        embedding = self.embedder.encode(text_to_embed).tolist()

        # 添加到ChromaDB
        self.collection.add(
            ids=[card.id],
            embeddings=[embedding],
            metadatas=[{
                "book_title": card.book_title,
                "book_author": card.book_author,
                "content_type": card.content_type,
                "tags": json.dumps(card.tags),
                "created_at": card.created_at
            }],
            documents=[card.content]
        )

    def search_knowledge(
        self,
        query: str,
        n_results: int = 5,
        content_type: Optional[str] = None
    ) -> List[Dict]:
        """
        语义搜索知识库
        query: 搜索查询（自然语言）
        n_results: 返回结果数量
        content_type: 过滤内容类型（可选）
        """
        # 生成查询embedding
        query_embedding = self.embedder.encode(query).tolist()

        # 构建过滤条件
        where = {"content_type": content_type} if content_type else None

        # 搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )

        # 格式化结果
        cards = []
        for i in range(len(results["ids"][0])):
            cards.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None
            })

        return cards

    def find_related_books(
        self,
        book_title: str,
        n_results: int = 3
    ) -> List[Dict]:
        """
        找到与某本书相关的其他书籍
        基于知识卡的语义相似度
        """
        # 搜索这本书的所有知识卡
        results = self.search_knowledge(
            query=f"这本书的核心观点和思想：{book_title}",
            n_results=20
        )

        # 统计其他书籍的出现频率
        book_mentions = {}
        for card in results:
            card_book_title = card["metadata"]["book_title"]
            if card_book_title != book_title:
                if card_book_title not in book_mentions:
                    book_mentions[card_book_title] = {
                        "title": card_book_title,
                        "author": card["metadata"]["book_author"],
                        "count": 0,
                        "related_concepts": []
                    }
                book_mentions[card_book_title]["count"] += 1
                book_mentions[card_book_title]["related_concepts"].append(card["content"])

        # 排序并返回Top N
        sorted_books = sorted(
            book_mentions.values(),
            key=lambda x: x["count"],
            reverse=True
        )

        return sorted_books[:n_results]

    def export_to_markdown(
        self,
        output_path: Optional[str] = None
    ) -> str:
        """
        导出知识库为Markdown格式（兼容Obsidian）
        """
        if output_path is None:
            output_path = self.persist_dir / "knowledge_base.md"

        output_path = Path(output_path)

        # 获取所有知识卡
        all_results = self.collection.get()

        # 按书籍分组
        books = {}
        for i, doc_id in enumerate(all_results["ids"]):
            metadata = all_results["metadatas"][i]
            book_title = metadata["book_title"]

            if book_title not in books:
                books[book_title] = {
                    "author": metadata["book_author"],
                    "insights": [],
                    "quotes": [],
                    "concepts": []
                }

            content_type = metadata["content_type"]
            content = all_results["documents"][i]

            if content_type == "insight":
                books[book_title]["insights"].append(content)
            elif content_type == "quote":
                books[book_title]["quotes"].append(content)
            elif content_type == "concept":
                books[book_title]["concepts"].append(content)

        # 生成Markdown
        markdown = "# 我的知识库\n\n"
        markdown += f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown += "---\n\n"

        for book_title, book_data in books.items():
            markdown += f## {book_title}\n\n
            markdown += f"**作者**: {book_data['author']}\n\n"

            if book_data["insights"]:
                markdown += "### 核心观点\n\n"
                for insight in book_data["insights"]:
                    markdown += f"- {insight}\n"
                markdown += "\n"

            if book_data["quotes"]:
                markdown += "### 金句卡片\n\n"
                for quote in book_data["quotes"]:
                    markdown += f"> {quote}\n\n"
                markdown += "\n"

            if book_data["concepts"]:
                markdown += "### 关键概念\n\n"
                for concept in book_data["concepts"]:
                    markdown += f"- {concept}\n"
                markdown += "\n"

            markdown += "---\n\n"

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"✅ 知识库已导出到: {output_path}")
        return str(output_path)

    def get_knowledge_graph_data(self) -> Dict:
        """
        获取知识图谱数据（用于可视化）
        返回可用于可视化库（如pyvis、networkx）的数据
        """
        all_results = self.collection.get()

        nodes = []
        edges = []
        books = set()

        # 构建节点
        for i, doc_id in enumerate(all_results["ids"]):
            metadata = all_results["metadatas"][i]
            content = all_results["documents"][i]

            book_title = metadata["book_title"]
            books.add(book_title)

            nodes.append({
                "id": doc_id,
                "label": content[:30] + "..." if len(content) > 30 else content,
                "type": metadata["content_type"],
                "book": book_title
            })

        # 添加书籍节点
        for book in books:
            nodes.append({
                "id": f"book_{book}",
                "label": f"📖 {book}",
                "type": "book",
                "book": book
            })

        # 构建边（知识卡 -> 书籍）
        for node in nodes:
            if node["type"] != "book":
                edges.append({
                    "from": node["id"],
                    "to": f"book_{node['book']}",
                    "label": "来自"
                })

        return {
            "nodes": nodes,
            "edges": edges
        }


# 使用示例
if __name__ == "__main__":
    # 初始化知识库
    kb = PersonalKnowledgeBase()

    # 示例：添加一本书的知识
    book_title = "思考，快与慢"
    book_author = "丹尼尔·卡尼曼"

    analysis = {
        "key_insights": [
            "人类思维有双系统：系统1快速直觉，系统2缓慢理性",
            "我们过度依赖直觉，导致很多判断偏差"
        ],
        "quotes": [
            "直觉是快速的、自动的、无意识的",
            "思考是缓慢的、费力的、有意识的"
        ],
        "mind_map": {
            "主要分支": [
                {
                    "分支名": "双系统理论",
                    "子节点": ["系统1：快思考", "系统2：慢思考"]
                },
                {
                    "分支名": "认知偏差",
                    "子节点": ["锚定效应", "损失厌恶"]
                }
            ]
        }
    }

    kb.add_book_knowledge(book_title, book_author, analysis)

    # 搜索知识
    print("\n=== 搜索：认知偏差 ===")
    results = kb.search_knowledge("认知偏差如何影响决策", n_results=3)
    for result in results:
        print(f"• {result['content']}")

    # 导出Markdown
    kb.export_to_markdown()
