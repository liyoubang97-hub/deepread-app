"""
DeepRead - 深度阅读工具 Web界面
使用Streamlit快速构建，适合个人使用和MVP测试
"""

import streamlit as st
import os
from pathlib import Path
import asyncio

# 导入我们的模块
from book_analyzer import BookDataFetcher, BookDeepAnalyzer
from podcast_generator import PodcastScriptGenerator, PodcastAudioGenerator
from knowledge_base import PersonalKnowledgeBase

# 页面配置
st.set_page_config(
    page_title="DeepRead 深读",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .insight-card {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .quote-card {
        background: #fffaf0;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ed8936;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)


# 初始化session state
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = None

if "current_book" not in st.session_state:
    st.session_state.current_book = None

if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None


def init_knowledge_base():
    """初始化知识库"""
    if st.session_state.knowledge_base is None:
        with st.spinner("正在加载知识库..."):
            st.session_state.knowledge_base = PersonalKnowledgeBase()
    return st.session_state.knowledge_base


def render_home():
    """首页"""
    st.markdown('<h1 class="main-title">📚 DeepRead 深读</h1>', unsafe_allow_html=True)
    st.markdown("### 对抗碎片化，深度阅读与思考")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📖 已读书籍", "0")

    with col2:
        st.metric("💡 知识卡片", "0")

    with col3:
        st.metric("🎧 播客生成", "0")

    st.markdown("---")

    # 功能介绍
    st.markdown("## ✨ 核心功能")

    features = {
        "📖 智能书籍解析": [
            "输入书名自动获取书籍信息",
            "AI提炼核心观点和思维导图",
            "生成金句卡片，一键分享"
        ],
        "🎧 AI播客生成": [
            "双人对话式解读",
            "15分钟轻松听完一本书",
            "真人感AI语音，边听边学"
        ],
        "🧠 个人知识库": [
            "所有读书笔记自动归档",
            "语义搜索相关知识点",
            "跨书籍知识关联",
            "导出Markdown/Obsidian"
        ]
    }

    cols = st.columns(3)
    for i, (title, items) in enumerate(features.items()):
        with cols[i]:
            st.markdown(f"### {title}")
            for item in items:
                st.markdown(f"- {item}")


def render_book_analysis():
    """书籍分析页面"""
    st.markdown("## 📖 书籍深度解析")

    # 搜索书籍
    col1, col2 = st.columns([3, 1])
    with col1:
        book_title = st.text_input("输入书名", placeholder="例如：思考，快与慢")
    with col2:
        st.write("")
        st.write("")
        search_button = st.button("🔍 搜索", type="primary")

    if search_button and book_title:
        with st.spinner(f"正在搜索《{book_title}》..."):
            fetcher = BookDataFetcher()
            book = fetcher.search_by_title(book_title)

            if book:
                st.session_state.current_book = book

                # 显示书籍信息
                col1, col2 = st.columns([1, 3])

                with col1:
                    if book.cover_url:
                        st.image(book.cover_url, width=200)

                with col2:
                    st.markdown(f"### {book.title}")
                    st.markdown(f"**作者**: {book.author}")
                    if book.categories:
                        st.markdown(f"**分类**: {', '.join(book.categories)}")
                    if book.average_rating:
                        st.markdown(f"**评分**: {'⭐' * int(book.average_rating)}")
                    if book.published_date:
                        st.markdown(f"**出版时间**: {book.published_date}")
                    if book.description:
                        with st.expander("📝 简介"):
                            st.markdown(book.description)

                st.markdown("---")

                # 深度分析按钮
                if st.button("🚀 开始深度分析", type="primary"):
                    with st.spinner("AI正在深度分析中，这可能需要30-60秒..."):
                        analyzer = BookDeepAnalyzer()
                        analysis = analyzer.analyze_book(book)
                        st.session_state.current_analysis = analysis

    # 显示分析结果
    if st.session_state.current_analysis:
        analysis = st.session_state.current_analysis
        book = st.session_state.current_book

        st.success("✅ 分析完成！")

        # Tab布局
        tab1, tab2, tab3, tab4 = st.tabs(["💡 核心观点", "🗺️ 思维导图", "💬 金句卡片", "📅 阅读计划"])

        with tab1:
            st.markdown("### 核心观点")
            for i, insight in enumerate(analysis.get("key_insights", []), 1):
                st.markdown(f"""
<div class="insight-card">
<strong>观点 {i}</strong><br/>
{insight}
</div>
""", unsafe_allow_html=True)

        with tab2:
            st.markdown("### 思维导图")
            mind_map = analysis.get("mind_map", {})
            st.json(mind_map)
            st.info("💡 提示：思维导图可视化功能正在开发中")

        with tab3:
            st.markdown("### 金句卡片")
            quotes = analysis.get("quotes", [])
            for quote in quotes:
                st.markdown(f'<div class="quote-card">"{quote}"</div>', unsafe_allow_html=True)

            # 导出按钮
            if st.button("📥 导出金句卡片"):
                st.info("💡 导出功能：将生成适合分享到小红书的图片格式")

        with tab4:
            st.markdown("### 阅读计划")
            reading_plan = analysis.get("reading_plan", {})

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**难度**: {analysis.get('difficulty', '未知')}")
            with col2:
                st.markdown(f"**预计时长**: {analysis.get('estimated_hours', 0)} 小时")
            with col3:
                st.markdown(f"**目标读者**: {', '.join(analysis.get('target_readers', ['所有人']))}")

            st.markdown("#### 4周阅读计划")
            for week, plan in reading_plan.items():
                st.markdown(f"**{week}**: {plan}")

        # 添加到知识库
        st.markdown("---")
        if st.button("💾 添加到个人知识库", type="primary"):
            kb = init_knowledge_base()
            kb.add_book_knowledge(book.title, book.author, analysis)
            st.success(f"✅ 已添加到知识库！")


def render_podcast():
    """播客生成页面"""
    st.markdown("## 🎧 AI播客生成器")

    # 检查是否有当前书籍
    if not st.session_state.current_book or not st.session_state.current_analysis:
        st.warning("⚠️ 请先在「书籍分析」页面选择一本书并进行分析")
        return

    book = st.session_state.current_book
    analysis = st.session_state.current_analysis

    st.markdown(f"### 当前书籍：《{book.title}》")

    # 配置选项
    col1, col2 = st.columns(2)

    with col1:
        voice_a = st.selectbox("主持人A声音", ["A_male (男声-稳重)", "A (女声-温柔)"], index=0)

    with col2:
        voice_b = st.selectbox("主持人B声音", ["B (女声-活泼)", "B_male (男声-年轻)"], index=0)

    # 生成按钮
    if st.button("🎙️ 生成播客脚本", type="primary"):
        with st.spinner("正在生成播客脚本..."):
            script_generator = PodcastScriptGenerator()
            script = script_generator.generate_script(
                book.title,
                book.author,
                analysis.get("key_insights", [])
            )

            st.session_state.current_script = script
            st.success("✅ 脚本生成完成！")

    # 显示脚本
    if "current_script" in st.session_state:
        script = st.session_state.current_script

        st.markdown("### 📝 播客脚本")
        st.markdown(f"**预计时长**: {script.total_duration // 60}分{script.total_duration % 60}秒")

        with st.expander("查看完整脚本"):
            st.markdown(f"**开场**: {script.intro}")

            for i, segment in enumerate(script.segments):
                speaker = "主持人A" if segment["speaker"] == "A" else "主持人B"
                st.markdown(f"**{speaker}**: {segment['text']}")

            st.markdown(f"**结尾**: {script.outro}")

        # 生成音频
        st.markdown("---")
        if st.button("🎵 生成音频文件", type="primary"):
            with st.spinner("正在生成音频，这可能需要几分钟..."):
                audio_generator = PodcastAudioGenerator()

                # 由于Streamlit的限制，这里使用同步方式
                voice_a_key = voice_a.split(" ")[0]
                voice_b_key = voice_b.split(" ")[0]

                # 注意：实际部署时需要处理异步问题
                st.info("💡 音频生成功能需要异步环境，请在命令行运行 podcast_generator.py")

    st.markdown("---")
    st.info("💡 提示：首次使用需要安装 edge-tts: `pip install edge-tts`")


def render_knowledge_base():
    """知识库页面"""
    st.markdown("## 🧠 个人知识库")

    kb = init_knowledge_base()

    # 统计信息
    all_results = kb.collection.get()
    total_cards = len(all_results["ids"])

    if total_cards == 0:
        st.warning("📭 知识库还是空的，去「书籍分析」页面添加第一本书吧！")
        return

    # 搜索功能
    st.markdown("### 🔍 知识搜索")
    search_query = st.text_input("搜索知识点", placeholder="例如：认知偏差、决策、心理学...")

    if search_query:
        results = kb.search_knowledge(search_query, n_results=10)

        st.markdown(f"找到 {len(results)} 条相关知识：")

        for result in results:
            metadata = result["metadata"]
            st.markdown(f"""
<div class="insight-card">
<strong>{metadata['book_title']}</strong> - {metadata['content_type']}<br/>
{result['content']}
</div>
""", unsafe_allow_html=True)

    # 相关书籍推荐
    st.markdown("---")
    st.markdown("### 📚 书籍关联")

    if st.session_state.current_book:
        related = kb.find_related_books(st.session_state.current_book.title)

        if related:
            for book in related:
                st.markdown(f"**{book['title']}** - {book['author']} ({book['count']}个相关概念)")

    # 导出功能
    st.markdown("---")
    st.markdown("### 📥 导出知识库")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("导出为Markdown"):
            output_path = kb.export_to_markdown()
            st.success(f"✅ 已导出到: {output_path}")

    with col2:
        st.info("💡 导出的Markdown文件可以导入到Obsidian、Logseq等笔记软件")


def main():
    """主函数"""
    # 侧边栏
    with st.sidebar:
        st.markdown("# 📚 DeepRead")
        st.markdown("---")

        page = st.radio(
            "导航",
            ["🏠 首页", "📖 书籍分析", "🎧 AI播客", "🧠 知识库"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # API配置
        st.markdown("### ⚙️ 配置")
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="在 https://groq.com 获取免费API Key"
        )

        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
            st.success("✅ API Key已设置")

        st.markdown("---")
        st.markdown("""
### 📖 使用说明

1. 输入书名搜索书籍
2. AI深度分析核心观点
3. 生成AI播客轻松学习
4. 所有知识自动入库

**推荐API**:
- Groq (免费，快速)
- GitHub Models

**本地方案**:
- Ollama (完全免费)
        """)

    # 路由
    if page == "🏠 首页":
        render_home()
    elif page == "📖 书籍分析":
        render_book_analysis()
    elif page == "🎧 AI播客":
        render_podcast()
    elif page == "🧠 知识库":
        render_knowledge_base()


if __name__ == "__main__":
    main()
