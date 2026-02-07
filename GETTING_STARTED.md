# DeepRead 使用指南

## ✅ 测试完成总结

### 已安装的功能
- ✅ streamlit (Web界面)
- ✅ requests (网络请求)
- ✅ edge-tts (语音合成)
- ✅ numpy, pandas (数据处理)

### 演示版已就绪
- ✅ app_demo.py (演示版Web应用)
- ✅ demo_data.py (预设3本书籍数据)
- ✅ start_demo.bat (Windows启动脚本)

---

## 🚀 立即体验（3种方式）

### 方式1：双击启动（推荐Windows用户）

1. 进入文件夹: `c:\Users\黎又榜\每日新闻推送系统\deepread`
2. 双击文件: `start_demo.bat`
3. 浏览器自动打开: http://localhost:8501

### 方式2：命令行启动

```bash
cd "c:\Users\黎又榜\每日新闻推送系统\deepread"
python -m streamlit run app_demo.py
```

### 方式3：测试脚本（无Web界面）

```bash
cd "c:\Users\黎又榜\每日新闻推送系统\deepread"
python test_basic.py
```

---

## 📖 演示版功能

### 可用书籍（3本）
1. **原子习惯** - 詹姆斯·克利尔
2. **思考，快与慢** - 丹尼尔·卡尼曼
3. **刻意练习** - 安德斯·艾利克森

### 功能清单

#### 📖 书籍分析
- [x] 书籍基本信息展示
- [x] 核心观点（5个洞见）
- [x] 思维导图（JSON格式）
- [x] 金句卡片（可分享）
- [x] 4周阅读计划
- [x] 难度和预计时长

#### 🎧 AI播客（开发中）
- [ ] 对话式脚本生成
- [ ] Edge TTS语音合成
- [ ] 音频文件导出

#### 🧠 知识库（开发中）
- [ ] 向量存储
- [ ] 语义搜索
- [ ] 跨书籍关联

---

## 🎯 完整版功能（需要API Key）

### 启用完整功能步骤

#### 1. 获取免费API Key

**选项A: Groq（推荐，速度快）**
```
1. 访问: https://groq.com
2. 注册账号（2分钟，免费）
3. 获取API Key
4. 设置环境变量:
   set GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

**选项B: 使用本地模型（完全免费）**
```
1. 下载Ollama: https://ollama.com/download
2. 安装后运行: ollama pull llama3:8b
3. 启动服务: ollama serve
```

#### 2. 安装剩余依赖（可选）

如果需要知识库功能：
```bash
pip install chromadb sentence-transformers
```

注意: Windows Python 3.14可能遇到兼容性问题，建议使用Python 3.10-3.11

#### 3. 运行完整版

```bash
# 设置API Key
set GROQ_API_KEY=你的key

# 启动完整版应用
python -m streamlit run app.py
```

---

## 📊 当前状态

### ✅ 已完成
- [x] 项目结构搭建
- [x] 核心代码模块（4个）
- [x] 演示数据（3本书）
- [x] 演示版Web界面
- [x] Windows启动脚本
- [x] 测试脚本

### ⚠️ 已知限制
1. **Google Books API**: 速率限制（1000次/天），目前触发限制
2. **ChromaDB**: Windows Python 3.14兼容性问题
3. **SentenceTransformers**: 首次运行需下载约400MB模型

### 💡 临时解决方案
1. 使用演示版体验UI和功能流程
2. 等待Google Books API配额重置（或使用代理）
3. 使用Python 3.10-3.11版本（如需完整功能）

---

## 🎨 界面预览

### 首页
- 功能介绍卡片
- 核心特性展示

### 书籍分析页
- 书籍选择（下拉菜单）
- 书籍信息展示
- 4个Tab页面：
  - 核心观点
  - 思维导图
  - 金句卡片
  - 阅读计划

### 播客页（开发中）
- 功能预览
- 示例脚本展示

### 知识库页（开发中）
- 功能预览
- 演示书籍列表

---

## 🔧 自定义和扩展

### 添加新的演示书籍

编辑 `demo_data.py`:

```python
DEMO_BOOKS["你的书名"] = {
    "title": "你的书名",
    "author": "作者",
    "description": "简介...",
    # ... 其他字段
}

DEMO_ANALYSES["你的书名"] = {
    "key_insights": ["观点1", "观点2"],
    # ... 其他字段
}
```

### 修改提示词

编辑 `book_analyzer.py` 中的 `_build_analysis_prompt()` 方法

### 添加新的语音

编辑 `podcast_generator.py` 中的 `VOICES` 字典

---

## 📝 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| app_demo.py | 演示版Web应用 | 立即体验UI |
| start_demo.bat | Windows启动脚本 | 双击运行 |
| demo_data.py | 演示数据 | 3本书的完整数据 |
| test_basic.py | 测试脚本 | 功能测试 |
| app.py | 完整版应用 | 需要API Key |
| book_analyzer.py | 书籍分析模块 | 核心功能 |
| podcast_generator.py | 播客生成模块 | AI播客 |
| knowledge_base.py | 知识库模块 | 向量存储 |
| local_model_analyzer.py | 本地模型 | Ollama支持 |

---

## 🎓 下一步建议

### 今天（体验演示）
1. ✅ 运行 `start_demo.bat`
2. ✅ 选择一本书查看分析
3. ✅ 浏览所有Tab页面

### 本周（启用完整功能）
1. 注册Groq获取API Key
2. 测试真实书籍搜索
3. 体验AI深度分析

### 本月（深度使用）
1. 添加更多书籍到知识库
2. 生成AI播客
3. 导出Markdown笔记

### 长期（商业化准备）
1. 收集用户反馈
2. 优化提示词
3. 开发付费墙功能

---

## 💬 常见问题

**Q: 为什么演示版只有3本书？**
A: 演示版用于展示UI和功能，完整版支持任意书籍。

**Q: 什么时候能搜索真实书籍？**
A: 设置API Key后即可，详见"启用完整功能"章节。

**Q: Google Books API限制怎么办？**
A: 等待24小时配额重置，或使用代理/VPS。

**Q: 能在手机上使用吗？**
A: 可以！在局域网内，手机访问电脑IP:8501

**Q: 数据保存在哪里？**
A: 完全本地，`knowledge_db/` 和 `podcasts/` 目录

---

## 📞 技术支持

遇到问题？
1. 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
2. 查看 [QUICKSTART.md](QUICKSTART.md)
3. 运行 `python test_basic.py` 诊断

---

**现在就启动演示版看看吧！** 🚀
