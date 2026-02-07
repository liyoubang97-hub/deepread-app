# DeepRead 快速上手指南

## 🚀 5分钟开始使用

### 方案A：使用免费API（推荐，速度快）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 获取免费API Key
# 访问 https://groq.com 注册（完全免费，2分钟）
# 复制API Key

# 3. 创建配置文件
cp .env.example .env

# 4. 编辑 .env 文件
# GROQ_API_KEY=gsk_xxxxxxxxxxxxx

# 5. 启动
python start.py
# 或
streamlit run app.py
```

---

### 方案B：完全免费本地运行（需要8GB+内存）

```bash
# 1. 下载Ollama
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
# Windows: https://ollama.com/download

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 下载模型（约4GB，首次需要）
ollama pull llama3:8b

# 4. 启动Ollama服务
ollama serve

# 5. 在另一个终端启动DeepRead
streamlit run app.py
```

---

## 📖 第一次使用

1. **搜索一本书**
   - 在首页输入书名，如"思考，快与慢"
   - 点击搜索

2. **深度分析**
   - 点击"开始深度分析"
   - 等待30-60秒（本地模型需要1-3分钟）
   - 查看核心观点、思维导图、金句卡片

3. **添加到知识库**
   - 点击"添加到个人知识库"
   - 所有知识点自动保存到本地

4. **生成播客**
   - 切换到"AI播客"页面
   - 点击"生成播客脚本"
   - 生成15分钟对话式解读

5. **搜索知识**
   - 切换到"知识库"页面
   - 输入任何问题，如"如何克服拖延症"
   - 自动匹配相关知识点

---

## 🎯 使用场景

### 场景1：快速了解一本书
```
输入书名 → 生成核心观点 → 5分钟掌握精华
```

### 场景2：深度阅读计划
```
选择书籍 → 查看阅读计划 → 21天读完一本书
```

### 场景3：知识管理
```
读完书 → 自动添加到知识库 → 语义搜索回顾
```

### 场景4：碎片化学习
```
生成AI播客 → 通勤路上听 → 15分钟了解一本书
```

---

## 💡 常见问题

### Q: 为什么分析很慢？
A:
- 使用Groq API：30-60秒正常
- 使用本地模型：1-3分钟正常（电脑性能影响）
- 可以在 `app.py` 中调整 `timeout` 参数

### Q: 能分析英文书吗？
A: 完全支持！模型是多语言的

### Q: 知识库数据存在哪里？
A: 本地 `knowledge_db/` 目录，完全私密

### Q: 可以导出数据吗？
A: 可以！在知识库页面点击"导出为Markdown"

### Q: 需要联网吗？
A:
- 书籍搜索：需要联网
- Groq API：需要联网
- 本地Ollama模型：分析时不需要，但搜索书籍仍需要

---

## 🛠️ 高级配置

### 更换为其他LLM

编辑 `book_analyzer.py`，修改API调用：

```python
# 使用OpenAI（需要付费）
self.api_url = "https://api.openai.com/v1/chat/completions"
headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"
body["model"] = "gpt-4"

# 使用Claude（需要付费）
self.api_url = "https://api.anthropic.com/v1/messages"
# ... 修改请求格式
```

### 使用更好的本地模型

```bash
# 下载更大的模型（更智能，但更慢）
ollama pull llama3:70b
ollama pull qwen2:72b

# 修改代码中的模型名称
analyzer = LocalBookAnalyzer(model_name="llama3:70b")
```

---

## 📊 性能对比

| 方案 | 速度 | 成本 | 需要联网 |
|------|------|------|---------|
| Groq API | ⭐⭐⭐⭐⭐ | 免费 | ✅ |
| 本地Llama3-8B | ⭐⭐⭐ | 免费 | ❌ |
| 本地Llama3-70B | ⭐⭐ | 免费 | ❌ |
| OpenAI GPT-4 | ⭐⭐⭐⭐ | 付费 | ✅ |

推荐：**先用Groq测试，满意后考虑本地部署**

---

## 🎁 额外功能

### 1. 批量导入书籍

创建 `books.txt`:
```
思考，快与慢
原子习惯
刻意练习
```

运行:
```python
from book_analyzer import BookDataFetcher, BookDeepAnalyzer

fetcher = BookDataFetcher()
analyzer = BookDeepAnalyzer()

with open("books.txt") as f:
    for line in f:
        book = fetcher.search_by_title(line.strip())
        if book:
            analysis = analyzer.analyze_book(book)
            # 保存分析结果...
```

### 2. 定时阅读提醒

```python
import schedule
import time

def daily_reading_reminder():
    print("⏰ 该读书了！今天的目标：30页")

schedule.every().day.at("20:00").do(daily_reading_reminder)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 📚 下一步

1. ✅ 完成第一次书籍分析
2. ✅ 生成第一个AI播客
3. ✅ 建立个人知识库
4. 📝 分享到小红书（使用生成的金句卡片）
5. 🔄 21天深度阅读计划

**Happy Reading! 📚**
