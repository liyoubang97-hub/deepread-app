"""
DeepRead V3 - 优雅阅读版
参考 ONE CUP、Medium、Substack 的设计理念
"""

import streamlit as st
from pathlib import Path
import sys

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from demo_data_v2 import get_book_content

# 页面配置
st.set_page_config(
    page_title="DeepRead 深读",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ONE CUP 风格配色方案 - 温暖优雅
st.markdown("""
<style>
    /* 全局字体 - 优先使用优雅的衬线字体 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    /* CSS变量 - 配色方案 */
    :root {
        --primary: #2D3436;
        --secondary: #636E72;
        --accent: #E17055;
        --accent-soft: #FDF2E9;
        --bg: #FAFBFC;
        --card-bg: #FFFFFF;
        --text: #2D3436;
        --text-light: #636E72;
        --text-lighter: #B2BEC3;
        --border: #E8EEF2;
        --success: #00B894;
        --shadow: rgba(45, 52, 54, 0.08);
    }

    /* 主容器 */
    .main {
        padding: 0 !important;
        max-width: 720px !important;
        margin: 0 auto;
        background: var(--bg);
    }

    /* 隐藏默认元素 */
    #MainMenu, footer, .stDeployButton {
        visibility: hidden;
        display: none !important;
    }

    /* 大标题 - ONE CUP风格 */
    .hero-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary);
        letter-spacing: -0.02em;
        line-height: 1.3;
        margin-bottom: 0.5rem;
        padding-top: 3rem;
    }

    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 400;
        color: var(--text-light);
        margin-bottom: 3rem;
        letter-spacing: 0.01em;
    }

    /* 章节标题 */
    .section-header {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--primary);
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.01em;
    }

    /* 卡片容器 */
    .content-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px var(--shadow);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }

    .content-card:hover {
        box-shadow: 0 4px 16px var(--shadow);
        transform: translateY(-2px);
    }

    /* 洞察卡片 - 重点内容 */
    .insight-card {
        background: linear-gradient(135deg, #FFF8F3 0%, #FFFFFF 100%);
        border-left: 4px solid var(--accent);
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 12px;
        line-height: 1.8;
    }

    /* 核心观点 - 大字体展示 */
    .core-idea {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.25rem;
        font-weight: 500;
        color: var(--primary);
        line-height: 1.8;
        margin: 1.5rem 0;
        padding: 1.5rem;
        background: var(--accent-soft);
        border-radius: 12px;
    }

    /* 小标题 */
    .subsection-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary);
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }

    /* 正文 */
    .body-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        line-height: 1.8;
        color: var(--text);
        margin-bottom: 1rem;
    }

    /* 提问框 - ONE CUP风格 */
    .question-box {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFFBF0 100%);
        border-left: 4px solid #FDCB6E;
        padding: 1.5rem;
        margin: 2rem 0;
        border-radius: 12px;
    }

    .question-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #E17055;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }

    .question-text {
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        font-weight: 500;
        color: var(--primary);
        line-height: 1.6;
    }

    /* 提示文字 */
    .hint-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-light);
        margin-top: 0.75rem;
        font-style: italic;
    }

    /* 金句卡片 */
    .quote-card {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.1rem;
        font-style: italic;
        color: var(--primary);
        line-height: 1.8;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
        border-radius: 12px;
        margin: 1.5rem 0;
        position: relative;
    }

    .quote-card::before {
        content: '"';
        font-size: 4rem;
        color: var(--accent);
        opacity: 0.2;
        position: absolute;
        top: -1rem;
        left: 1rem;
        font-family: Georgia, serif;
    }

    /* 导航按钮 - 优雅风格 */
    .nav-button {
        text-align: center;
        margin: 3rem 0;
    }

    /* 书籍卡片 - 库页面 */
    .book-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .book-card:hover {
        border-color: var(--accent);
        box-shadow: 0 4px 20px var(--shadow);
        transform: translateY(-2px);
    }

    .book-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }

    .book-author {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-light);
        margin-bottom: 1rem;
    }

    .book-theme {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: var(--accent);
        font-weight: 500;
    }

    /* 标签 */
    .tag {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        background: var(--accent-soft);
        color: var(--accent);
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* 分隔线 */
    .divider {
        height: 1px;
        background: var(--border);
        margin: 3rem 0;
    }

    /* 进度指示器 */
    .progress-indicator {
        display: flex;
        gap: 0.5rem;
        margin: 2rem 0;
    }

    .progress-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--border);
        transition: all 0.3s ease;
    }

    .progress-dot.active {
        background: var(--accent);
        width: 24px;
        border-radius: 4px;
    }

    /* 侧边栏 */
    .sidebar-content {
        padding: 1.5rem;
    }

    /* 按钮 */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }

    /* 输入框 */
    .stTextArea > div > div > textarea {
        font-family: 'Noto Serif SC', serif;
        font-size: 1rem;
        line-height: 1.8;
        border-radius: 8px;
        border: 1px solid var(--border);
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
    """书籍库 - ONE CUP风格"""
    st.markdown('<div class="hero-title">📖 深度阅读</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">给思考留出时间</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 书籍列表
    books = [
        {
            "title": "原子习惯",
            "author": "詹姆斯·克利尔",
            "theme": "微小改变如何带来巨大转变",
            "emoji": "🌱",
            "read_time": "15分钟",
            "insights": "3个核心洞察"
        }
    ]

    for book in books:
        st.markdown(f"""
<div class="book-card" onclick="document.querySelector('[data-testid=\"stButton\"]').click()">
    <div style="font-size: 2.5rem; margin-bottom: 1rem;">{book['emoji']}</div>
    <div class="book-title">{book['title']}</div>
    <div class="book-author">{book['author']}</div>
    <div class="book-theme">{book['theme']}</div>
    <div style="margin-top: 1rem;">
        <span class="tag">⏱️ {book['read_time']}</span>
        <span class="tag">💡 {book['insights']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

        if st.button(f"开始阅读", key=f"read_{book['title']}", use_container_width=True):
            st.session_state.current_book = book['title']
            st.session_state.current_content = get_book_content(book['title'])
            st.session_state.current_section = "intro"
            st.rerun()


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

    st.markdown(f'<div class="section-header">{intro["title"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="body-text">{intro["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 为什么要读
    st.markdown('<div class="subsection-title">为什么要读这本书？</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><div class="body-text">{intro["why_read"]}</div></div>', unsafe_allow_html=True)

    # 阅读前提问
    st.markdown('<div class="subsection-title">阅读前，先问问自己</div>', unsafe_allow_html=True)

    for i, question in enumerate(intro["pre_questions"], 1):
        st.markdown(f"""
<div class="question-box">
    <div class="question-label">问题 {i}</div>
    <div class="question-text">{question}</div>
</div>
""", unsafe_allow_html=True)

    # 开始阅读
    st.markdown('<div class="nav-button">', unsafe_allow_html=True)
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

    st.markdown(f'<div class="section-header">{core["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="body-text" style="color: var(--text-light);">{core["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 每个洞察
    for idx, insight in enumerate(core["insights"], 1):
        st.markdown(f'<div class="section-header">洞察 {idx}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="subsection-title">{insight["title"]}</div>', unsafe_allow_html=True)

        # 核心观点
        st.markdown(f'<div class="core-idea">{insight["core_idea"]}</div>', unsafe_allow_html=True)

        # 为什么重要
        st.markdown('<div class="subsection-title">为什么这很重要？</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="content-card"><div class="body-text">{insight["why_matters"]}</div></div>', unsafe_allow_html=True)

        # 现实案例
        if insight.get("example"):
            st.markdown('<div class="subsection-title">现实中的样子</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="content-card"><div class="body-text">{insight["example"]}</div></div>', unsafe_allow_html=True)

        # 思考题
        if insight.get("question"):
            st.markdown(f"""
<div class="question-box">
    <div class="question-label">停下来想想</div>
    <div class="question-text">{insight["question"]}</div>
</div>
""", unsafe_allow_html=True)

        if idx < len(core["insights"]):
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 底部导航
    st.markdown('<div class="nav-button">', unsafe_allow_html=True)
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

    st.markdown(f'<div class="section-header">{practice["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="body-text" style="color: var(--text-light);">{practice["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 实践步骤
    for item in practice["actions"]:
        st.markdown(f'<div class="content-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="subsection-title">{item["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="body-text">{item["description"]}</div>', unsafe_allow_html=True)

        if item.get("steps"):
            st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
            for step in item["steps"]:
                st.markdown(f'<div class="body-text" style="padding-left: 1rem; border-left: 2px solid var(--accent);">✓ {step}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # 底部导航
    st.markdown('<div class="nav-button">', unsafe_allow_html=True)
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

    st.markdown(f'<div class="section-header">{reflection["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="body-text" style="color: var(--text-light);">{reflection["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 思考题
    for idx, question in enumerate(reflection["questions"], 1):
        st.markdown(f"""
<div class="question-box">
    <div class="question-label">问题 {idx}</div>
    <div class="question-text">{question["text"]}</div>
    <div class="hint-text">💡 {question["hint"]}</div>
</div>
""", unsafe_allow_html=True)

        # 输入框
        user_note = st.text_area(
            "写下你的思考...",
            key=f"note_{idx}",
            placeholder="这里记录你的想法，让思考更深刻...",
            height=100,
            label_visibility="collapsed"
        )

        if user_note:
            st.success("✓ 已记录")
            st.session_state.notes[f"q{idx}"] = user_note

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # 金句回顾
    st.markdown('<div class="subsection-title">值得记住的话</div>', unsafe_allow_html=True)

    for quote in content["quotes"]:
        st.markdown(f'<div class="quote-card">{quote}</div>', unsafe_allow_html=True)

    # 完成阅读
    st.markdown('<div class="nav-button">', unsafe_allow_html=True)
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


def main():
    """主函数"""
    init_session_state()

    # 极简侧边栏
    with st.sidebar:
        st.markdown("""
<div class="sidebar-content">
    <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">📖 DeepRead</div>
    <div style="font-size: 0.875rem; color: var(--text-light); margin-bottom: 2rem;">深度阅读 · 慢思考</div>
</div>
""", unsafe_allow_html=True)

        if st.session_state.current_book:
            st.info(f"📖 {st.session_state.current_book}")

            st.markdown("""
<div style="margin-top: 2rem;">
    <div style="font-size: 0.75rem; color: var(--text-light); margin-bottom: 0.5rem;">阅读进度</div>
    <div class="progress-indicator">
""", unsafe_allow_html=True)

            sections = ["intro", "insights", "practice", "reflection"]
            current = st.session_state.current_section
            for i, sec in enumerate(sections):
                active_class = "active" if sec == current else ""
                st.markdown(f'<div class="progress-dot {active_class}"></div>', unsafe_allow_html=True)

            st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

            section_labels = {
                "intro": "引言",
                "insights": "洞察",
                "practice": "实践",
                "reflection": "反思"
            }

            for key, label in section_labels.items():
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.session_state.current_section = key
                    st.rerun()

            st.markdown('<div style="height: 1px; background: var(--border); margin: 2rem 0;"></div>', unsafe_allow_html=True)

            if st.button("📚 返回书库", use_container_width=True):
                st.session_state.current_book = None
                st.session_state.current_content = None
                st.session_state.current_section = "library"
                st.rerun()

        st.markdown("""
<div style="margin-top: auto; padding-top: 2rem; font-size: 0.75rem; color: var(--text-light);">
    <div>给自己时间</div>
    <div>慢慢来</div>
    <div style="margin-top: 1rem;">🌱</div>
</div>
""", unsafe_allow_html=True)

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
