# 📚 DeepRead 深度阅读工具

> 对抗碎片化，深度阅读与思考的AI助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)

---

## ✨ 核心功能

- **📖 智能书籍解析** - 输入书名，自动获取书籍信息并生成深度分析
- **💡 核心观点提炼** - AI提炼3-5个关键洞见，不是简单摘要
- **🗺️ 思维导图生成** - 自动生成知识结构
- **💬 金句卡片** - 生成适合分享到社交媒体的金句
- **🎧 AI播客生成** - 双人对话式解读，15分钟听完一本书
- **🧠 个人知识库** - 语义搜索、跨书籍知识关联
- **📅 21天阅读计划** - 科学的阅读进度安排

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
cd deepread

# 安装依赖
pip install -r requirements.txt
```

### 2. 获取免费API Key（推荐Groq）

- 访问 [https://groq.com](https://groq.com)
- 注册账号（完全免费）
- 获取API Key
- 创建 `.env` 文件并填入：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 GROQ_API_KEY
```

### 3. 启动Web界面

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

---

## 📖 使用指南

### 基础使用流程

1. **搜索书籍**：在"书籍分析"页面输入书名
2. **深度分析**：点击"开始深度分析"，等待30-60秒
3. **查看结果**：
   - 核心观点（5个洞见）
   - 思维导图
   - 金句卡片
   - 4周阅读计划
4. **添加到知识库**：一键保存所有知识
5. **生成播客**：切换到"AI播客"页面生成对话式解读

### 知识库功能

- **语义搜索**：用自然语言搜索知识点（如"认知偏差如何影响决策"）
- **相关书籍**：自动发现知识点相关的其他书籍
- **导出Markdown**：兼容Obsidian、Logseq等笔记软件

---

## 🛠️ 技术架构

### 技术栈（全部免费）

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| 前端 | Streamlit | 快速原型，适合个人使用 |
| 后端 | FastAPI + Python | 轻量级，易扩展 |
| LLM API | Groq / GitHub Models | 免费额度大，速度快 |
| 向量数据库 | ChromaDB | 本地持久化，完全免费 |
| 文本嵌入 | SentenceTransformers | 本地模型，一次下载永久使用 |
| TTS | Edge TTS | 微软免费API，质量好 |
| 书籍数据 | Google Books API | 每天1000次免费请求 |

### 项目结构

```
deepread/
├── app.py                    # Streamlit Web界面
├── book_analyzer.py          # 书籍搜索和深度分析
├── podcast_generator.py      # AI播客生成器
├── knowledge_base.py         # 知识库系统
├── requirements.txt          # 依赖包
├── .env.example              # 配置模板
├── knowledge_db/             # 本地知识库（自动创建）
└── podcasts/                 # 生成的播客音频（自动创建）
```

---

## 💰 完全免费的方案

如果你想**完全不依赖外部API**，可以使用以下本地方案：

### 方案1：Ollama（推荐）

```bash
# 1. 安装Ollama
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
# Windows: 下载安装包 https://ollama.com/download

# 2. 下载模型
ollama pull llama3:8b

# 3. 修改代码，将API调用改为本地调用
# 只需修改 book_analyzer.py 中的 API 调用部分
```

### 方案2：使用Hugging Face免费推理

```python
# 使用 transformers 库直接调用
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
# 完全本地运行，无需API
```

---

## 📊 数据示例

### 输入
```
书名：思考，快与慢
```

### 输出

```json
{
  "key_insights": [
    "人类思维有双系统：系统1快速直觉，系统2缓慢理性",
    "我们过度依赖直觉，导致很多判断偏差",
    "了解思维偏差可以帮助我们做出更好决策",
    "损失厌恶：人们对损失的敏感度是收益的2倍",
    "锚定效应：第一印象会影响后续判断"
  ],
  "mind_map": {
    "中心主题": "思考，快与慢",
    "主要分支": [
      {
        "分支名": "双系统理论",
        "子节点": ["系统1：快思考", "系统2：慢思考"]
      },
      {
        "分支名": "认知偏差",
        "子节点": ["锚定效应", "损失厌恶", "可得性启发"]
      }
    ]
  },
  "quotes": [
    "直觉是快速的、自动的、无意识的",
    "思考是缓慢的、费力的、有意识的"
  ],
  "reading_plan": {
    "week1": "第1-5章：理解双系统理论",
    "week2": "第6-10章：探索启发式和偏差",
    "week3": "第11-20章：理解过度自信",
    "week4": "第21-30章：应用于决策和生活"
  },
  "difficulty": "高级",
  "estimated_hours": 12
}
```

---

## 🎯 未来计划（商业化方向）

当前版本是**个人使用的MVP**，如果验证有价值，可以考虑：

### Phase 2：增值功能
- [ ] 多语言书籍支持
- [ ] AI辩论模式（让不同作者的观点"对话"）
- [ ] 可视化知识图谱
- [ ] 小红书分享卡片生成器

### Phase 3：商业化
- [ ] 付费墙（单次付费 / 订阅）
- [ ] 小红书博主合作分成系统
- [ ] 企业读书会SaaS

---

## 🤝 贡献

欢迎提Issue和PR！

---

## 📄 License

MIT License

---

## 💡 FAQ

**Q: 为什么选择Groq而不是OpenAI？**
A: Groq提供免费额度且速度极快，适合个人使用和MVP测试。

**Q: 知识库数据存储在哪里？**
A: 存储在本地 `knowledge_db/` 目录，完全私密。

**Q: 可以离线使用吗？**
A: 部分功能可以。书籍搜索需要网络，但如果使用Ollama本地模型，AI分析可以离线。

**Q: 生成的播客可以商用吗？**
A: Edge TTS生成的音频可以个人使用，商用需确认微软的使用条款。

**Q: 支持中文书籍吗？**
A: 完全支持！模型是多语言的。

---

## 📧 联系方式

有问题欢迎提Issue！

**Happy Reading! 📚**
