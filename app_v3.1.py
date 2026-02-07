"""
DeepRead V3.1 - 优化版
改进：模块分区、配色、侧边栏、多书展示
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from demo_data_v2 import get_book_content

st.set_page_config(
    page_title="DeepRead 深读",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 优化的配色方案和样式
st.markdown("""
<style>
    /* 字体引入 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    /* 主容器 */
    .main {
        padding: 0 !important;
        max-width: 760px !important;
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
        padding: 4rem 0 3rem 0;
        border-bottom: 2px solid #E8EEF2;
        margin-bottom: 3rem;
    }

    .page-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #2D3436;
        letter-spacing: 0.02em;
        margin-bottom: 0.75rem;
    }

    .page-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 400;
        color: #636E72;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ===== 分区标题 ===== */
    .section-block {
        margin-bottom: 4rem;
    }

    .section-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #2D3436;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #2D3436;
        display: inline-block;
    }

    .section-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        color: #0984E3;
        margin-bottom: 1.5rem;
    }

    /* ===== 内容卡片 ===== */
    .content-block {
        background: #FAFBFC;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid #E8EEF2;
    }

    .content-block.highlight {
        background: linear-gradient(135deg, #FFF8F3 0%, #FFFFFF 100%);
        border-left: 4px solid #E17055;
    }

    /* ===== 核心观点 ===== */
    .core-idea-box {
        background: #2D3436;
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(45, 52, 54, 0.15);
    }

    .core-idea-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.15rem;
        font-weight: 500;
        line-height: 1.9;
        white-space: pre-wrap;
    }

    /* ===== 小标题 ===== */
    .subsection-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: #2D3436;
        margin-top: 2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }

    .subsection-header::before {
        content: '';
        width: 4px;
        height: 1.2rem;
        background: #0984E3;
        margin-right: 0.75rem;
        border-radius: 2px;
    }

    /* ===== 正文 ===== */
    .body-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        line-height: 1.9;
        color: #2D3436;
        margin-bottom: 1rem;
    }

    /* ===== 提问框 ===== */
    .question-block {
        background: #FDF6E3;
        border-left: 4px solid #FDCB6E;
        border-radius: 0 12px 12px 0;
        padding: 1.75rem;
        margin: 2rem 0;
    }

    .question-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #D63031;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
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
        margin-top: 1rem;
        font-style: italic;
    }

    /* ===== 金句卡片 ===== */
    .quote-block {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        font-style: italic;
        color: #2D3436;
        line-height: 1.8;
        padding: 1.75rem 2rem;
        background: #F8F9FA;
        border-radius: 12px;
        margin: 1.5rem 0;
        position: relative;
        border: 1px solid #E8EEF2;
    }

    .quote-block::before {
        content: '"';
        font-size: 4rem;
        color: #636E72;
        opacity: 0.15;
        position: absolute;
        top: -0.5rem;
        left: 1.5rem;
        font-family: Georgia, serif;
    }

    /* ===== 分隔线 ===== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #E8EEF2, transparent);
        margin: 4rem 0;
    }

    /* ===== 书籍卡片（库页面）===== */
    .book-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    .book-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 2rem;
        border: 2px solid #E8EEF2;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }

    .book-card:hover {
        border-color: #0984E3;
        box-shadow: 0 8px 30px rgba(9, 132, 227, 0.15);
        transform: translateY(-4px);
    }

    .book-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }

    .book-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #2D3436;
        margin-bottom: 0.5rem;
    }

    .book-author {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: #636E72;
        margin-bottom: 1rem;
    }

    .book-description {
        font-family: 'Noto Serif SC', serif;
        font-size: 0.95rem;
        color: #2D3436;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* ===== 标签 ===== */
    .tag-container {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 1rem;
    }

    .tag {
        display: inline-block;
        padding: 0.4rem 0.875rem;
        background: #F0F3F5;
        color: #2D3436;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    .tag.highlight {
        background: #E3F2FD;
        color: #0984E3;
    }

    /* ===== 导航按钮 ===== */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 3rem 0;
        padding: 2rem 0;
        border-top: 1px solid #E8EEF2;
    }

    /* ===== 步骤列表 ===== */
    .step-list {
        list-style: none;
        padding: 0;
        margin: 1.5rem 0;
    }

    .step-item {
        display: flex;
        align-items: flex-start;
        padding: 1rem 0;
        border-bottom: 1px solid #E8EEF2;
    }

    .step-item:last-child {
        border-bottom: none;
    }

    .step-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: #0984E3;
        color: #FFFFFF;
        border-radius: 50%;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 1rem;
        flex-shrink: 0;
    }

    .step-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        line-height: 1.7;
        color: #2D3436;
        flex: 1;
    }

    /* ===== 洞察编号 ===== */
    .insight-number {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #0984E3;
        opacity: 0.15;
        margin-bottom: -1rem;
    }

    /* ===== 按钮样式 ===== */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.75rem 1.75rem;
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

    /* ===== 信息提示 ===== */
    .info-box {
        background: #E3F2FD;
        border-left: 4px solid #0984E3;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #2D3436;
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


def render_library():
    """书籍库页面 - 清晰的多书展示"""
    # 页面头部
    st.markdown("""
<div class="page-header">
    <div class="page-title">📖 深度阅读</div>
    <div class="page-subtitle">给思考留出时间</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 书籍列表
    books = [
        {
            "title": "原子习惯",
            "author": "詹姆斯·克利尔",
            "description": "微小改变如何通过时间的复利，带来人生的巨大转变",
            "icon": "🌱",
            "tags": ["习惯养成", "自我提升", "15分钟"],
            "available": True
        },
        {
            "title": "思考，快与慢",
            "author": "丹尼尔·卡尼曼",
            "description": "理解人类思维的双系统，认识直觉与理性的真相",
            "icon": "🧠",
            "tags": ["认知科学", "决策", "即将推出"],
            "available": False
        },
        {
            "title": "刻意练习",
            "author": "安德斯·艾利克森",
            "description": "如何通过正确的练习方法，在任何领域达到卓越",
            "icon": "🎯",
            "tags": ["技能提升", "练习方法", "即将推出"],
            "available": False
        }
    ]

    # 书籍网格
    for book in books:
        if book["available"]:
            if st.button(f"**{book['title']}**  —  {book['author']}", key=f"book_{book['title']}", use_container_width=True):
                st.session_state.current_book = book['title']
                st.session_state.current_content = get_book_content(book['title'])
                st.session_state.current_section = "intro"
                st.rerun()
        else:
            st.markdown(f"""
<div class="book-card" style="opacity: 0.6; cursor: not-allowed;">
    <div class="book-icon">{book['icon']}</div>
    <div class="book-title">{book['title']}</div>
    <div class="book-author">{book['author']}</div>
    <div class="book-description">{book['description']}</div>
    <div class="tag-container">
        {' '.join([f'<span class="tag">{tag}</span>' for tag in book['tags']])}
    </div>
    <div style="margin-top: 1rem; color: #636E72; font-size: 0.875rem;">即将推出</div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)


def render_introduction(content):
    """引言页"""
    intro = content["introduction"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← 返回"):
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
    if st.button("📖 开始深入阅读", use_container_width=True, type="primary"):
        st.session_state.current_section = "insights"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_insights(content):
    """核心洞察页"""
    core = content["core_thinking"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 引言"):
            st.session_state.current_section = "intro"
            st.rerun()

    st.markdown(f'<div class="section-title">{core["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{core["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 每个洞察
    for idx, insight in enumerate(core["insights"], 1):
        st.markdown(f'<div class="insight-number">{idx:02d}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{insight["title"]}</div>', unsafe_allow_html=True)

        # 核心观点
        st.markdown('<div class="core-idea-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="core-idea-text">{insight["core_idea"]}</div>', unsafe_allow_html=True)
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
    <div class="question-label">停下来想想</div>
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
        if st.button("← 引言"):
            st.session_state.current_section = "intro"
            st.rerun()

    with col3:
        if st.button("实践 →"):
            st.session_state.current_section = "practice"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_practice(content):
    """实践页"""
    practice = content["practice"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 洞察"):
            st.session_state.current_section = "insights"
            st.rerun()

    st.markdown(f'<div class="section-title">{practice["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{practice["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 实践步骤
    for item in practice["actions"]:
        st.markdown('<div class="section-block">', unsafe_allow_html=True)

        st.markdown(f'<div class="subsection-header">{item["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="body-text" style="margin-bottom: 1.5rem;">{item["description"]}</div>', unsafe_allow_html=True)

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
        if st.button("← 洞察"):
            st.session_state.current_section = "insights"
            st.rerun()

    with col3:
        if st.button("反思 →"):
            st.session_state.current_section = "reflection"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_reflection(content):
    """反思页"""
    reflection = content["reflection"]

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 实践"):
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
        if st.button("← 返回"):
            st.session_state.current_section = "practice"
            st.rerun()

    with col2:
        if st.button("📚 返回书库", use_container_width=True):
            st.session_state.current_book = None
            st.session_state.current_content = None
            st.session_state.current_section = "library"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar():
    """优化的侧边栏"""
    with st.sidebar:
        # Logo区域
        st.markdown("""
<div style="text-align: center; padding: 2rem 0 1.5rem 0; border-bottom: 2px solid #E8EEF2;">
    <div style="font-size: 2rem; font-weight: 700; color: #2D3436; margin-bottom: 0.5rem;">📖</div>
    <div style="font-size: 1.1rem; font-weight: 600; color: #2D3436;">DeepRead</div>
    <div style="font-size: 0.8rem; color: #636E72; margin-top: 0.5rem;">深度阅读 · 慢思考</div>
</div>
""", unsafe_allow_html=True)

        if st.session_state.current_book:
            # 当前阅读
            st.markdown(f"""
<div style="background: #F0F3F5; padding: 1rem; border-radius: 8px; margin: 1.5rem 0;">
    <div style="font-size: 0.75rem; color: #636E72; margin-bottom: 0.25rem;">正在阅读</div>
    <div style="font-size: 0.95rem; font-weight: 600; color: #2D3436;">{st.session_state.current_book}</div>
</div>
""", unsafe_allow_html=True)

            # 阅读进度
            st.markdown('<div style="margin: 2rem 0 1rem 0;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size: 0.8rem; font-weight: 600; color: #636E72; margin-bottom: 1rem;">阅读进度</div>', unsafe_allow_html=True)

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
<div style="background: #2D3436; color: #FFFFFF; padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 0.5rem; font-size: 0.9rem;">
    {label}
</div>
""", unsafe_allow_html=True)
                else:
                    if st.button(label, key=f"nav_{key}", use_container_width=True):
                        st.session_state.current_section = key
                        st.rerun()

            # 返回按钮
            st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
            if st.button("📚 返回书库", use_container_width=True):
                st.session_state.current_book = None
                st.session_state.current_content = None
                st.session_state.current_section = "library"
                st.rerun()

        # 底部信息
        st.markdown("""
<div style="margin-top: auto; padding-top: 3rem; text-align: center; border-top: 2px solid #E8EEF2;">
    <div style="font-size: 0.75rem; color: #636E72; line-height: 1.8;">
        给自己时间<br/>慢慢来<br/><br/>🌱
    </div>
</div>
""", unsafe_allow_html=True)


def main():
    """主函数"""
    init_session_state()

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
