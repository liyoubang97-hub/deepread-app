# DeepRead 项目结构

## 📁 文件树

```
deepread/
│
├── 📄 app.py                      # Streamlit Web界面主程序
├── 📄 start.py                    # 快速启动脚本（环境检测）
│
├── 📘 核心模块/
│   ├── book_analyzer.py           # 书籍搜索 + AI深度分析
│   ├── podcast_generator.py       # AI播客脚本生成 + TTS音频
│   ├── knowledge_base.py          # 本地向量知识库
│   └── local_model_analyzer.py    # 本地Ollama模型方案
│
├── ⚙️ 配置文件/
│   ├── requirements.txt           # Python依赖包
│   ├── .env.example               # 环境变量模板
│   └── .env                       # 你的配置（不提交到Git）
│
├── 📖 文档/
│   ├── README.md                  # 项目说明
│   ├── QUICKSTART.md              # 5分钟快速上手
│   └── PROJECT_STRUCTURE.md       # 本文件
│
├── 💾 数据目录（自动创建）/
│   ├── knowledge_db/              # ChromaDB向量数据库
│   │   ├── chroma/                # 向量索引
│   │   └── knowledge_base.md      # 导出的Markdown
│   └── podcasts/                  # 生成的音频文件
│
└── 🗑️ .gitignore                  # Git忽略文件
```

---

## 🔄 数据流程

```
用户输入书名
    ↓
Google Books API / Open Library
    ↓
BookInfo (书籍元数据)
    ↓
LLM深度分析 (Groq / Ollama)
    ↓
分析结果 {
    核心观点
    思维导图
    金句卡片
    阅读计划
}
    ↓
    ├─→ 保存到ChromaDB (向量知识库)
    ├─→ 生成播客脚本
    └─→ Edge TTS生成音频
```

---

## 🧩 模块说明

### 1. book_analyzer.py

**主要类**:
- `BookDataFetcher`: 从Google Books/Open Library获取书籍信息
- `BookDeepAnalyzer`: 使用LLM生成深度分析
- `BookInfo`: 书籍信息数据类

**输入**: 书名（字符串）
**输出**:
```json
{
  "key_insights": ["观点1", "观点2", ...],
  "mind_map": { "中心主题": "...", "主要分支": [...] },
  "quotes": ["金句1", "金句2", ...],
  "reading_plan": { "week1": "...", ... },
  "difficulty": "中级",
  "estimated_hours": 10
}
```

---

### 2. podcast_generator.py

**主要类**:
- `PodcastScriptGenerator`: 生成对话式播客脚本
- `PodcastAudioGenerator`: 使用Edge TTS生成音频

**输入**: 书籍信息 + 核心观点
**输出**: MP3音频文件 + 脚本JSON

**语音配置**:
```python
VOICES = {
    "A": "zh-CN-XiaoxiaoNeural",  # 女声，温柔
    "A_male": "zh-CN-YunyangNeural",  # 男声，稳重
    "B": "zh-CN-XiaoyiNeural",  # 女声，活泼
    "B_male": "zh-CN-YunxiNeural",  # 男声，年轻
}
```

---

### 3. knowledge_base.py

**主要类**:
- `PersonalKnowledgeBase`: 本地向量知识库
- `KnowledgeCard`: 知识卡片数据类

**功能**:
- 添加书籍知识（自动向量化）
- 语义搜索（基于余弦相似度）
- 找相关书籍
- 导出Markdown/Obsidian

**存储**: ChromaDB持久化到本地 `knowledge_db/chroma/`

---

### 4. local_model_analyzer.py

**主要类**:
- `LocalBookAnalyzer`: 使用Ollama本地模型

**优势**:
- 完全免费
- 数据隐私（本地运行）
- 无需API Key

**劣势**:
- 需要大内存（8GB+）
- 速度较慢（比API慢2-3倍）

---

## 🎨 Web界面 (app.py)

**页面结构**:
1. **首页**: 功能介绍
2. **书籍分析**: 搜索、分析、查看结果
3. **AI播客**: 生成脚本和音频
4. **知识库**: 搜索、浏览、导出

**Session State管理**:
```python
st.session_state.knowledge_base  # 知识库实例
st.session_state.current_book    # 当前书籍
st.session_state.current_analysis  # 当前分析结果
st.session_state.current_script  # 当前播客脚本
```

---

## 🔑 环境变量

在 `.env` 文件中配置：

```bash
# LLM API（选择一个）
GROQ_API_KEY=gsk_xxx          # Groq（推荐，免费）
GITHUB_MODELS_API_KEY=xxx     # GitHub Models
# OPENAI_API_KEY=xxx          # OpenAI（付费）

# 本地方案
# OLLAMA_BASE_URL=http://localhost:11434

# 路径配置
KNOWLEDGE_DB_PATH=./knowledge_db
PODCAST_OUTPUT_PATH=./podcasts

# 日志
LOG_LEVEL=INFO
```

---

## 📊 依赖包说明

| 包名 | 用途 | 是否必需 |
|------|------|---------|
| streamlit | Web界面 | ✅ 必需 |
| requests | HTTP请求 | ✅ 必需 |
| chromadb | 向量数据库 | ✅ 必需 |
| sentence-transformers | 文本嵌入 | ✅ 必需 |
| edge-tts | 语音合成 | ⚠️ 播客功能 |
| pydub | 音频合并 | ⚠️ 可选 |
| groq | Groq SDK | ⚠️ 使用Groq时 |

---

## 🚀 扩展方向

### 当前版本（MVP）
- ✅ 单人使用
- ✅ 本地数据
- ✅ 免费资源

### Phase 2: 增值功能
- [ ] 用户系统（多用户）
- [ ] 云端同步
- [ ] 移动端适配
- [ ] 小红书分享卡片

### Phase 3: 商业化
- [ ] 订阅付费墙
- [ ] 博主分成系统
- [ ] 企业版SaaS

---

## 📝 开发建议

### 调试技巧

```python
# 1. 查看详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. 测试单个模块
python -m book_analyzer

# 3. 查看ChromaDB数据
import chromadb
client = chromadb.PersistentClient("./knowledge_db/chroma")
collection = client.get_collection("knowledge_cards")
print(collection.get())

# 4. 清空知识库
collection.delete(where={})  # ⚠️ 危险操作
```

### 性能优化

```python
# 1. 缓存书籍搜索结果
@st.cache_data
def search_book(title):
    return fetcher.search_by_title(title)

# 2. 异步生成播客
import asyncio
await audio_generator.generate_podcast(script, book_title)

# 3. 批量处理
for batch in chunks(books, 10):  # 每次处理10本
    process_batch(batch)
```

---

## 🧪 测试

```bash
# 测试书籍搜索
python -c "from book_analyzer import BookDataFetcher; print(BookDataFetcher().search_by_title('原子习惯'))"

# 测试本地模型
python local_model_analyzer.py

# 测试知识库
python -c "from knowledge_base import PersonalKnowledgeBase; kb = PersonalKnowledgeBase(); print(kb.collection.count())"
```

---

**需要帮助？查看:**
- [README.md](README.md) - 项目说明
- [QUICKSTART.md](QUICKSTART.md) - 快速上手
- [提Issue](https://github.com/your-repo/issues) - 问题反馈
