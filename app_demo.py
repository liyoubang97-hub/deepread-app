"""
DeepRead 演示版 Web界面
可以离线运行，使用演示数据
"""

import streamlit as st
from pathlib import Path
import sys

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入模块
from demo_data import get_demo_book, get_demo_analysis, DEMO_BOOKS
from book_analyzer import BookInfo

# 页面配置
st.set_page_config(
    page_title="DeepRead 深读 - 演示版",
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


def init_session_state():
    """初始化session state"""
    if "current_book" not in st.session_state:
        st.session_state.current_book = None
    if "current_analysis" not in st.session_state:
        st.session_state.current_analysis = None
    if "demo_mode" not in st.session_state:
        st.session_state.demo_mode = True


def render_home():
    """首页"""
    st.markdown('<h1 class="main-title">📚 DeepRead 深读 (演示版)</h1>', unsafe_allow_html=True)
    st.markdown("### 对抗碎片化，深度阅读与思考")

    st.info("🎉 当前运行在演示模式，可以离线使用所有功能")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📖 演示书籍", "3本")

    with col2:
        st.metric("💡 核心观点", "15+")

    with col3:
        st.metric("🎧 AI播客", "即将推出")

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

    st.info("💡 演示模式下，请从下方选择一本预设的书籍进行体验")

    # 演示书籍选择
    demo_books = list(DEMO_BOOKS.keys())

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_book = st.selectbox("选择一本书", demo_books)

    with col2:
        st.write("")
        st.write("")
        analyze_button = st.button("🚀 开始分析", type="primary")

    if analyze_button or (st.session_state.current_book is None and selected_book):
        # 获取演示数据
        book_data = DEMO_BOOKS[selected_book]
        st.session_state.current_book = BookInfo(**book_data)

        # 获取演示分析
        st.session_state.current_analysis = get_demo_analysis(selected_book)

    # 显示书籍信息
    if st.session_state.current_book:
        book = st.session_state.current_book

        col1, col2 = st.columns([1, 3])

        with col1:
            if book.cover_url:
                st.image(book.cover_url, width=200)
            else:
                st.info("📖 暂无封面")

        with col2:
            st.markdown(f"### {book.title}")
            st.markdown(f"**作者**: {book.author}")
            if book.categories:
                st.markdown(f"**分类**: {', '.join(book.categories)}")
            if book.average_rating:
                st.markdown(f"**评分**: {'⭐' * int(book.average_rating)} ({book.average_rating}/5)")
            if book.published_date:
                st.markdown(f"**出版时间**: {book.published_date}")
            if book.description:
                with st.expander("📝 简介"):
                    st.markdown(book.description)

        st.markdown("---")

        # 显示分析结果
        if st.session_state.current_analysis:
            analysis = st.session_state.current_analysis

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

                st.markdown(f"**中心主题**: {mind_map.get('中心主题', '')}")

                for branch in mind_map.get("主要分支", []):
                    with st.expander(f"📂 {branch['分支名']}"):
                        for concept in branch.get("子节点", []):
                            st.markdown(f"  - {concept}")

                with st.expander("📋 查看JSON格式"):
                    st.json(mind_map)

            with tab3:
                st.markdown("### 金句卡片")
                quotes = analysis.get("quotes", [])
                for quote in quotes:
                    st.markdown(f'<div class="quote-card">"{quote}"</div>', unsafe_allow_html=True)

                st.info("💡 实际版本中可以导出为图片分享到社交媒体")

            with tab4:
                st.markdown("### 阅读计划")
                reading_plan = analysis.get("reading_plan", {})

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**难度**: {analysis.get('difficulty', '未知')}")
                with col2:
                    st.markdown(f"**预计时长**: {analysis.get('estimated_hours', 0)} 小时")
                with col3:
                    readers = analysis.get('target_readers', ['所有人'])
                    st.markdown(f"**目标读者**: {', '.join(readers[:2])}{'...' if len(readers) > 2 else ''}")

                st.markdown("#### 4周阅读计划")
                for week, plan in reading_plan.items():
                    st.markdown(f"**{week}**: {plan}")

            st.markdown("---")
            st.success("✅ 演示模式下无需添加到知识库，所有数据已展示完毕")


def render_podcast():
    """播客生成页面"""
    st.markdown("## 🎧 AI播客生成器")

    st.info("🎵 播客功能正在开发中，敬请期待！")

    if not st.session_state.current_book:
        st.warning("⚠️ 请先在「书籍分析」页面选择一本书")
        return

    book = st.session_state.current_book
    st.markdown(f"### 当前书籍：《{book.title}》")

    st.markdown("#### 功能预览")
    st.markdown("""
    - 🎙️ **对话式播客脚本**: AI生成双人对话解读
    - 🎵 **真人感语音**: 使用Edge TTS生成自然语音
    - ⏱️ **15分钟精华**: 快速掌握书籍核心内容
    - 📥 **音频下载**: 支持MP3格式导出
    """)

    st.markdown("----")
    st.markdown("##### 示例播客脚本片段")

    st.info("""
    **主持人A**: 今天我们来聊聊《原子习惯》这本书。

    **主持人B**: 哦，我听说过这本书！它是关于如何通过微小改变来达成大目标，对吧？

    **主持人A**: 没错！书中提到一个很有意思的观点：每天进步1%，一年后你会进步37倍。这就是习惯的复利效应。

    **主持人B**: 哇，37倍！这听起来太不可思议了。

    **主持人A**: 是的，作者詹姆斯·克利尔强调，关键不在于设定宏大目标，而在于建立正确的系统。
    """)


def render_knowledge_base():
    """知识库页面"""
    st.markdown("## 🧠 个人知识库")

    st.info("💾 知识库功能正在开发中，敬请期待！")

    st.markdown("### 功能预览")
    st.markdown("""
    - 🔍 **语义搜索**: 用自然语言查找知识点
    - 🔗 **跨书籍关联**: 自动发现相关概念
    - 📊 **知识图谱**: 可视化你的知识网络
    - 📥 **Markdown导出**: 兼容Obsidian等笔记软件
    """)

    st.markdown("---")

    # 展示演示数据
    st.markdown("### 📚 演示书籍库")

    for title, book_data in DEMO_BOOKS.items():
        with st.expander(f"📖 {title} - {book_data['author']}"):
            st.markdown(f"**分类**: {', '.join(book_data['categories'])}")
            st.markdown(f"**评分**: {'⭐' * int(book_data['average_rating'])} ({book_data['average_rating']}/5)")
            st.markdown(f"**简介**: {book_data['description'][:100]}...")


def main():
    """主函数"""
    init_session_state()

    # 侧边栏
    with st.sidebar:
        st.markdown("# 📚 DeepRead")
        st.markdown("**演示版**")
        st.markdown("---")

        page = st.radio(
            "导航",
            ["🏠 首页", "📖 书籍分析", "🎧 AI播客", "🧠 知识库"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        st.markdown("### ℹ️ 关于演示版")
        st.markdown("""
        当前版本使用预设数据，
        可以离线体验所有功能。

        **完整版将支持**:
        - 任意书籍搜索
        - 真实AI分析
        - 本地知识库
        - AI播客生成
        """)

        st.markdown("---")
        st.markdown("""
        ### 📖 可用书籍
        """)

        for title in DEMO_BOOKS.keys():
            if st.button(f"📕 {title}", key=f"nav_{title}"):
                st.session_state.current_book = None
                st.session_state.current_analysis = None
                st.rerun()

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
