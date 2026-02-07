"""
DeepRead V3.5 - 修复优化版
改进：
1. 修复SVG显示（简化图形）
2. 修复图书封面（使用emoji占位符）
3. 优化点击交互
4. 改成两本书一行的布局
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from demo_data_v2 import get_book_content

st.set_page_config(
    page_title="DeepRead 深读",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 优化的样式
st.markdown("""
<style>
    /* 字体引入 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    /* 主容器 */
    .main {
        padding: 0 !important;
        max-width: 900px !important;
        margin: 0 auto;
        background: #FFFFFF;
    }

    /* 隐藏默认元素 */
    #MainMenu, footer, .stDeployButton {
        visibility: hidden;
        display: none !important;
    }

    /* ===== 页面头部 ===== */
    .page-header {
        text-align: center;
        padding: 2.5rem 0 2rem 0;
        border-bottom: 2px solid #E8EEF2;
        margin-bottom: 2rem;
    }

    .page-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #2D3436;
        letter-spacing: 0.02em;
        margin-bottom: 0.5rem;
    }

    .page-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 400;
        color: #636E72;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ===== 分区标题 ===== */
    .section-block {
        margin-bottom: 2.5rem;
    }

    .section-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2D3436;
        margin-bottom: 1.25rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #2D3436;
        display: inline-block;
    }

    .section-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
        color: #636E72;
        margin-bottom: 1.25rem;
        font-style: italic;
    }

    /* ===== 内容卡片 ===== */
    .content-block {
        background: #FAFBFC;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #E8EEF2;
    }

    .content-block.highlight {
        background: #F8F9FA;
        border-left: 3px solid #636E72;
    }

    /* ===== 核心观点 - 温暖米色背景 ===== */
    .core-idea-box {
        background: linear-gradient(135deg, #FFF8F0 0%, #FFF4E6 100%);
        color: #2D3436;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #F5E6D3;
        box-shadow: 0 2px 12px rgba(245, 230, 211, 0.15);
    }

    .core-idea-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.05rem;
        font-weight: 500;
        line-height: 1.8;
        white-space: pre-wrap;
    }

    /* ===== 小标题 ===== */
    .subsection-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #2D3436;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    /* ===== 正文 ===== */
    .body-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        line-height: 1.85;
        color: #2D3436;
        margin-bottom: 0.75rem;
    }

    /* ===== 提问框 ===== */
    .question-block {
        background: #F8F9FA;
        border-left: 3px solid #636E72;
        border-radius: 0 10px 10px 0;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .question-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #636E72;
        font-style: italic;
        letter-spacing: 0.02em;
        margin-bottom: 0.5rem;
    }

    .question-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.05rem;
        font-weight: 500;
        color: #2D3436;
        line-height: 1.7;
    }

    .hint-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: #636E72;
        margin-top: 0.75rem;
        font-style: italic;
    }

    /* ===== 金句卡片 ===== */
    .quote-block {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.05rem;
        font-style: italic;
        color: #2D3436;
        line-height: 1.75;
        padding: 1.5rem;
        background: #F8F9FA;
        border-radius: 10px;
        margin: 1.25rem 0;
        position: relative;
        border: 1px solid #E8EEF2;
    }

    .quote-block::before {
        content: '"';
        font-size: 3rem;
        color: #636E72;
        opacity: 0.15;
        position: absolute;
        top: -0.25rem;
        left: 1.25rem;
        font-family: Georgia, serif;
    }

    /* ===== 分隔线 ===== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #E8EEF2, transparent);
        margin: 2rem 0;
    }

    /* ===== 书籍卡片 - 两列布局 ===== */
    .book-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1.25rem;
        border: 2px solid #E8EEF2;
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .book-card.available {
        cursor: pointer;
    }

    .book-card.available:hover {
        border-color: #636E72;
        box-shadow: 0 4px 16px rgba(45, 52, 54, 0.10);
        transform: translateY(-2px);
    }

    .book-card.unavailable {
        opacity: 0.6;
    }

    .book-cover {
        font-size: 4rem;
        margin: 0.5rem 0;
        opacity: 0.8;
    }

    .book-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .book-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #2D3436;
        margin-bottom: 0.4rem;
    }

    .book-author {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #636E72;
        margin-bottom: 0.6rem;
    }

    .book-description {
        font-family: 'Noto Serif SC', serif;
        font-size: 0.85rem;
        color: #2D3436;
        line-height: 1.5;
        margin-bottom: 0.8rem;
        min-height: 2.5rem;
    }

    /* ===== 标签 ===== */
    .tag-container {
        display: flex;
        gap: 0.3rem;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 0.6rem;
    }

    .tag {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        background: #F0F3F5;
        color: #2D3436;
        border-radius: 12px;
        font-size: 0.65rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    .tag.highlight {
        background: #E8EEF2;
        color: #2D3436;
    }

    /* ===== 导航按钮 ===== */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        padding: 1.5rem 0;
        border-top: 1px solid #E8EEF2;
    }

    /* ===== 步骤列表 ===== */
    .step-list {
        list-style: none;
        padding: 0;
        margin: 1.25rem 0;
    }

    .step-item {
        display: flex;
        align-items: flex-start;
        padding: 0.75rem 0;
        border-bottom: 1px solid #E8EEF2;
    }

    .step-item:last-child {
        border-bottom: none;
    }

    .step-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        background: #636E72;
        color: #FFFFFF;
        border-radius: 50%;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 0.875rem;
        flex-shrink: 0;
    }

    .step-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #2D3436;
        flex: 1;
    }

    /* ===== 洞察编号 - 简约线条 ===== */
    .insight-number {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #636E72;
        opacity: 0.25;
        margin-bottom: 0.5rem;
        letter-spacing: 0.1em;
    }

    /* ===== 按钮样式 ===== */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.65rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button[kind="primary"] {
        background: #2D3436;
    }

    /* ===== 文本输入框 ===== */
    .stTextArea > div > div > textarea {
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        line-height: 1.8;
        border-radius: 8px;
        border: 1px solid #E8EEF2;
    }

    /* ===== 滚动行为 ===== */
    html {
        scroll-behavior: smooth;
    }

    body {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化session state"""
    if "current_book" not in st.session_state:
        st.session_state.current_book = None
    if "current_content" not in st.session_state:
        st.session_state.current_content = None
    if "current_section" not in st.session_state:
        st.session_state.current_section = "library"
    if "notes" not in st.session_state:
        st.session_state.notes = {}
    if "should_scroll" not in st.session_state:
        st.session_state.should_scroll = False


# 书籍数据
BOOKS_DATA = [
    {
        "title": "原子习惯",
        "author": "詹姆斯·克利尔",
        "description": "微小改变如何通过时间的复利，带来人生的巨大转变。每天进步1%，一年后你会进步37倍。",
        "tags": ["习惯养成", "自我提升"],
        "available": True,
        "emoji": "📖"
    },
    {
        "title": "思考，快与慢",
        "author": "丹尼尔·卡尼曼",
        "description": "理解人类思维的双系统，认识直觉与理性的真相",
        "tags": ["认知科学", "决策"],
        "available": False,
        "emoji": "🧠"
    },
    {
        "title": "刻意练习",
        "author": "安德斯·艾利克森",
        "description": "如何通过正确的练习方法，在任何领域达到卓越",
        "tags": ["技能提升", "练习"],
        "available": False,
        "emoji": "🎯"
    },
    {
        "title": "深度工作",
        "author": "卡尔·纽波特",
        "description": "在分心的世界中进行专注工作的能力，是日益稀缺的资产",
        "tags": ["效率", "专注"],
        "available": False,
        "emoji": "💼"
    }
]


def render_library():
    """书籍库页面 - 两列布局"""
    # 页面头部
    st.markdown("""
<div class="page-header">
    <div class="page-title">🧠 深度阅读</div>
    <div class="page-subtitle">给思考留出时间</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 两列布局
    cols = st.columns(2)

    for idx, book in enumerate(BOOKS_DATA):
        col_idx = idx % 2
        with cols[col_idx]:
            # 卡片内容
            card_class = "available" if book["available"] else "unavailable"

            st.markdown(f"""
<div class="book-card {card_class}">
    <div class="book-cover">{book['emoji']}</div>
    <div class="book-info">
        <div>
            <div class="book-title">{book['title']}</div>
            <div class="book-author">{book['author']}</div>
            <div class="book-description">{book['description']}</div>
            <div class="tag-container">
                {' '.join([f'<span class="tag {("highlight" if book["available"] else "")}">{tag}</span>' for tag in book['tags']])}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

            # 可点击的按钮
            if book["available"]:
                if st.button(f"📖 阅读", key=f"read_{book['title']}", use_container_width=True):
                    st.session_state.should_scroll = True
                    st.session_state.current_book = book['title']
                    st.session_state.current_content = get_book_content(book['title'])
                    st.session_state.current_section = "intro"
                    st.rerun()
            else:
                st.markdown(f'<div style="text-align: center; color: #636E72; font-size: 0.75rem; font-style: italic; margin-top: 0.5rem;">即将推出</div>', unsafe_allow_html=True)


def render_introduction(content):
    """引言页"""
    intro = content["introduction"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← 返回", key="intro_back_library"):
            st.session_state.should_scroll = True
            st.session_state.current_book = None
            st.session_state.current_content = None
            st.session_state.current_section = "library"
            st.rerun()

    # 页面标题
    st.markdown(f'<div class="section-title">{intro["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{intro["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 内容分区
    st.markdown('<div class="section-block">', unsafe_allow_html=True)

    st.markdown('<div class="subsection-header">为什么要读这本书</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-block"><div class="body-text">{intro["why_read"]}</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 阅读前提问
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-header">阅读前，先问问自己</div>', unsafe_allow_html=True)

    for i, question in enumerate(intro["pre_questions"], 1):
        st.markdown(f"""
<div class="question-block">
    <div class="question-label">问题 {i}</div>
    <div class="question-text">{question}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 开始阅读
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    if st.button("📖 开始深入阅读", key="intro_start", use_container_width=True, type="primary"):
        st.session_state.should_scroll = True
        st.session_state.current_section = "insights"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_insights(content):
    """核心洞察页"""
    core = content["core_thinking"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 引言", key="insights_back_intro"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "intro"
            st.rerun()

    st.markdown(f'<div class="section-title">{core["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{core["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 每个洞察
    for idx, insight in enumerate(core["insights"], 1):
        # 简约线条编号
        st.markdown(f'<div class="insight-number">— {idx:02d} —</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{insight["title"]}</div>', unsafe_allow_html=True)

        # 核心观点
        st.markdown('<div class="core-idea-box">', unsafe_allow_html=True)
        core_idea = insight["core_idea"].strip()
        core_idea = '\n\n'.join(line.strip() for line in core_idea.split('\n') if line.strip())
        st.markdown(f'<div class="core-idea-text">{core_idea}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 分区内容
        st.markdown('<div class="section-block">', unsafe_allow_html=True)

        st.markdown('<div class="subsection-header">为什么这很重要</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="content-block"><div class="body-text">{insight["why_matters"]}</div></div>', unsafe_allow_html=True)

        if insight.get("example"):
            st.markdown('<div class="subsection-header">现实中的样子</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-block highlight"><div class="body-text">{insight["example"]}</div></div>', unsafe_allow_html=True)

        if insight.get("question"):
            st.markdown(f"""
<div class="question-block">
    <div class="question-label">想一想</div>
    <div class="question-text">{insight["question"]}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if idx < len(core["insights"]):
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 底部导航
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 引言", key="insights_bottom_back"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "intro"
            st.rerun()

    with col3:
        if st.button("实践 →", key="insights_to_practice"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "practice"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_practice(content):
    """实践页"""
    practice = content["practice"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 洞察", key="practice_back_insights"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "insights"
            st.rerun()

    st.markdown(f'<div class="section-title">{practice["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{practice["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 实践步骤
    for item in practice["actions"]:
        st.markdown('<div class="section-block">', unsafe_allow_html=True)

        st.markdown(f'<div class="subsection-header">{item["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="body-text" style="margin-bottom: 1.25rem;">{item["description"]}</div>', unsafe_allow_html=True)

        if item.get("steps"):
            st.markdown('<div class="step-list">', unsafe_allow_html=True)
            for step in item["steps"]:
                st.markdown(f'<div class="step-item"><div class="step-number">✓</div><div class="step-text">{step}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # 底部导航
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 洞察", key="practice_bottom_back"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "insights"
            st.rerun()

    with col3:
        if st.button("反思 →", key="practice_to_reflection"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "reflection"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_reflection(content):
    """反思页"""
    reflection = content["reflection"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 实践", key="reflection_back_practice"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "practice"
            st.rerun()

    st.markdown(f'<div class="section-title">{reflection["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{reflection["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 思考题
    for idx, question in enumerate(reflection["questions"], 1):
        st.markdown(f'<div class="section-block">', unsafe_allow_html=True)

        st.markdown(f"""
<div class="question-block">
    <div class="question-label">问题 {idx}</div>
    <div class="question-text">{question["text"]}</div>
    <div class="hint-text">💡 {question["hint"]}</div>
</div>
""", unsafe_allow_html=True)

        user_note = st.text_area(
            "",
            key=f"note_{idx}",
            placeholder="在这里记录你的思考，让想法更深刻...",
            height=100,
            label_visibility="collapsed"
        )

        if user_note:
            st.success("✓ 已记录")
            st.session_state.notes[f"q{idx}"] = user_note

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 金句回顾
    st.markdown('<div class="subsection-header">值得记住的话</div>', unsafe_allow_html=True)

    for quote in content["quotes"]:
        st.markdown(f'<div class="quote-block">{quote}</div>', unsafe_allow_html=True)

    # 完成阅读
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 返回", key="reflection_back"):
            st.session_state.should_scroll = True
            st.session_state.current_section = "practice"
            st.rerun()

    with col2:
        if st.button("📚 返回书库", key="reflection_to_library", use_container_width=True):
            st.session_state.should_scroll = True
            st.session_state.current_book = None
            st.session_state.current_content = None
            st.session_state.current_section = "library"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar():
    """侧边栏 - 简化Logo"""
    with st.sidebar:
        # Logo区域 - 使用emoji和文字
        st.markdown("""
<div style="text-align: center; padding: 2rem 0 1.5rem 0; border-bottom: 2px solid #E8EEF2; background: linear-gradient(180deg, #FAFBFC 0%, #FFFFFF 100%);">
    <div style="font-size: 3.5rem; margin-bottom: 0.75rem;">📖</div>
    <div style="font-size: 1.5rem; font-weight: 600; color: #2D3436; margin-bottom: 0.5rem; letter-spacing: 0.05em; font-family: 'Noto Serif SC', serif;">DeepRead</div>
    <div style="font-size: 0.85rem; color: #636E72; margin-top: 0.75rem; font-style: italic; letter-spacing: 0.03em;">深度阅读 · 沉浸思考</div>
</div>
""", unsafe_allow_html=True)

        if st.session_state.current_book:
            # 当前阅读
            st.markdown(f"""
<div style="background: #F0F3F5; padding: 0.875rem; border-radius: 8px; margin: 1.25rem 0;">
    <div style="font-size: 0.7rem; color: #636E72; margin-bottom: 0.25rem;">正在阅读</div>
    <div style="font-size: 0.9rem; font-weight: 600; color: #2D3436;">{st.session_state.current_book}</div>
</div>
""", unsafe_allow_html=True)

            # 阅读进度
            st.markdown('<div style="margin: 1.5rem 0 0.75rem 0;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #636E72; margin-bottom: 0.75rem;">阅读进度</div>', unsafe_allow_html=True)

            sections = [
                ("intro", "📖 引言"),
                ("insights", "💡 洞察"),
                ("practice", "✅ 实践"),
                ("reflection", "🤔 反思")
            ]

            for key, label in sections:
                is_current = st.session_state.current_section == key
                if is_current:
                    st.markdown(f"""
<div style="background: #636E72; color: #FFFFFF; padding: 0.65rem 0.875rem; border-radius: 6px; margin-bottom: 0.5rem; font-size: 0.85rem;">
    {label}
</div>
""", unsafe_allow_html=True)
                else:
                    if st.button(label, key=f"nav_{key}"):
                        st.session_state.should_scroll = True
                        st.session_state.current_section = key
                        st.rerun()

            # 返回按钮
            st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
            if st.button("📚 返回书库", use_container_width=True):
                st.session_state.should_scroll = True
                st.session_state.current_book = None
                st.session_state.current_content = None
                st.session_state.current_section = "library"
                st.rerun()

        # 底部信息 - 放大文字
        st.markdown("""
<div style="margin-top: auto; padding-top: 2rem; text-align: center; border-top: 2px solid #E8EEF2;">
    <div style="font-size: 0.85rem; color: #636E72; line-height: 1.8; font-weight: 500;">
        给自己时间<br/>慢慢来<br/><br/>🌱
    </div>
</div>
""", unsafe_allow_html=True)


def main():
    """主函数"""
    init_session_state()

    # 滚动到顶部的JavaScript
    if st.session_state.should_scroll:
        st.markdown("""
<script>
    setTimeout(function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
</script>
""", unsafe_allow_html=True)
        st.session_state.should_scroll = False

    # 侧边栏
    render_sidebar()

    # 主内容区
    if not st.session_state.current_book:
        render_library()
    else:
        content = st.session_state.current_content
        section = st.session_state.current_section

        if section == "intro":
            render_introduction(content)
        elif section == "insights":
            render_insights(content)
        elif section == "practice":
            render_practice(content)
        elif section == "reflection":
            render_reflection(content)


if __name__ == "__main__":
    main()
