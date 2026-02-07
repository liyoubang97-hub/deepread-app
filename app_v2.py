"""
DeepRead 深度阅读 V2 - 思考导向版
更沉浸、更有深度的阅读体验
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
    layout="centered",  # 改为居中布局，更像阅读
    initial_sidebar_state="collapsed"  # 默认收起侧边栏，减少干扰
)

# 沉浸式思考风格CSS
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        padding: 2rem 3rem;
        max-width: 800px;  /* 限制宽度，更易阅读 */
        margin: 0 auto;
    }

    /* 去除多余装饰 */
    .stDeployButton {
        display: none;
    }

    /* 标题样式 */
    .thought-title {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }

    .thought-subtitle {
        font-size: 1rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
        font-style: italic;
    }

    /* 章节标题 */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #34495e;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid #3498db;
        padding-left: 1rem;
    }

    /* 核心思考卡片 */
    .thought-card {
        background: #fafbfc;
        padding: 2rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        border-left: 3px solid #3498db;
        line-height: 1.8;
    }

    /* 深度洞察 */
    .deep-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 8px;
        margin: 2rem 0;
        line-height: 1.8;
        font-size: 1.05rem;
    }

    /* 反思提问 */
    .reflection-question {
        background: #fff9e6;
        border-left: 4px solid #f39c12;
        padding: 1.5rem;
        margin: 2rem 0;
        border-radius: 4px;
    }

    .reflection-question .question-label {
        font-weight: 600;
        color: #e67e22;
        margin-bottom: 0.5rem;
        display: block;
    }

    /* 金句 */
    .quote-text {
        font-size: 1.1rem;
        color: #2c3e50;
        font-style: italic;
        line-height: 1.8;
        padding: 1.5rem;
        background: #f8f9fa;
        border-left: 3px solid #9b59b6;
        margin: 1.5rem 0;
    }

    /* 实践建议 */
    .practice-box {
        background: #e8f5e9;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        border-left: 3px solid #27ae60;
    }

    /* 阅读进度 */
    .reading-progress {
        background: #ecf0f1;
        padding: 1rem;
        border-radius: 8px;
        margin: 2rem 0;
    }

    /* 导航按钮 */
    .nav-button {
        text-align: center;
        margin: 2rem 0;
    }

    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 侧边栏样式 */
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* 书籍卡片 */
    .book-card {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .book-card:hover {
        background: #f8f9fa;
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
        st.session_state.current_section = "intro"


def render_library():
    """书籍库页面 - 极简设计"""
    st.markdown('<div class="thought-title">📚 你的思考图书馆</div>', unsafe_allow_html=True)
    st.markdown('<div class="thought-subtitle">选择一本书，开始深度思考之旅</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 书籍列表
    books = [
        {
            "title": "原子习惯",
            "author": "詹姆斯·克利尔",
            "theme": "微小改变如何带来巨大转变",
            "color": "#3498db"
        },
        {
            "title": "思考，快与慢",
            "author": "丹尼尔·卡尼曼",
            "theme": "理解人类思维的非理性",
            "color": "#9b59b6"
        },
        {
            "title": "刻意练习",
            "author": "安德斯·艾利克森",
            "theme": "如何通过练习达到卓越",
            "color": "#27ae60"
        }
    ]

    for book in books:
        col1, col2 = st.columns([1, 5])

        with col1:
            st.markdown(f"""
            <div style="font-size: 3rem; text-align: center; color: {book['color']};">📖</div>
            """, unsafe_allow_html=True)

        with col2:
            if st.button(f"**{book['title']}**  —  {book['author']}", key=f"book_{book['title']}", use_container_width=True):
                st.session_state.current_book = book['title']
                st.session_state.current_content = get_book_content(book['title'])
                st.session_state.current_section = "intro"
                st.rerun()

            st.caption(f"💭 {book['theme']}")


def render_book_reading():
    """书籍阅读页面 - 沉浸式体验"""
    if not st.session_state.current_book:
        render_library()
        return

    content = st.session_state.current_content
    section = st.session_state.current_section

    # 顶部导航
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.button("← 返回书库"):
            st.session_state.current_book = None
            st.session_state.current_content = None
            st.rerun()

    with col3:
        if st.button("目录"):
            st.session_state.current_section = "toc"
            st.rerun()

    # 根据section渲染不同内容
    if section == "toc":
        render_table_of_contents(content)
    elif section == "intro":
        render_introduction(content)
    elif section == "core":
        render_core_thinking(content)
    elif section == "practice":
        render_practice(content)
    elif section == "reflection":
        render_reflection(content)


def render_table_of_contents(content):
    """目录页"""
    st.markdown('<div class="thought-title">目录</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="thought-subtitle">{content["title"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    sections = [
        ("intro", "📖 引言：为什么要读这本书"),
        ("core", "💭 核心思考：深层洞见"),
        ("practice", "🎯 实践：如何应用"),
        ("reflection", "🪞 反思：向自己提问"),
    ]

    for key, label in sections:
        if st.button(label, key=f"toc_{key}", use_container_width=True):
            st.session_state.current_section = key
            st.rerun()


        st.markdown("&nbsp;")

    st.markdown("---")
    st.markdown('<div class="reading-progress">', unsafe_allow_html=True)
    st.markdown("### 阅读建议")
    st.markdown("""
    - 📖 不要急于读完，给自己思考的时间
    - 💭 每读一段，停下来思考自己的经历
    - ✏️ 准备纸笔，记录你的想法
    - 🔄 读完后，过几天再回顾
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def render_introduction(content):
    """引言页"""
    intro = content["introduction"]

    st.markdown(f'<div class="thought-title">{intro["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="thought-subtitle">{intro["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 为什么要读这本书
    st.markdown('<div class="section-title">为什么要读这本书？</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="thought-card">{intro["why_read"]}</div>', unsafe_allow_html=True)

    # 这本书会挑战你的什么
    st.markdown('<div class="section-title">这本书会挑战你的什么</div>', unsafe_allow_html=True)
    for challenge in intro["challenges"]:
        st.markdown(f'<div class="thought-card">💭 {challenge}</div>', unsafe_allow_html=True)

    # 阅读前思考
    st.markdown('<div class="section-title">阅读前，先问问自己</div>', unsafe_allow_html=True)
    for question in intro["pre_questions"]:
        st.markdown(f'''
<div class="reflection-question">
    <span class="question-label">思考</span>
    {question}
</div>
''', unsafe_allow_html=True)

    # 开始阅读按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📖 开始深入阅读", use_container_width=True, type="primary"):
            st.session_state.current_section = "core"
            st.rerun()


def render_core_thinking(content):
    """核心思考页"""
    core = content["core_thinking"]

    st.markdown(f'<div class="thought-title">{core["title"]}</div>', unsafe_allow_html=True)

    # 引言
    st.markdown(f'<div class="thought-subtitle">{core["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 每一个深度洞察
    for idx, insight in enumerate(core["insights"], 1):
        # 标题
        st.markdown(f'<div class="section-title">洞察 {idx}: {insight["title"]}</div>', unsafe_allow_html=True)

        # 核心观点
        st.markdown(f'<div class="deep-insight">{insight["core_idea"]}</div>', unsafe_allow_html=True)

        # 为什么这很重要
        st.markdown("#### 为什么这很重要？")
        st.markdown(f'<div class="thought-card">{insight["why_matters"]}</div>', unsafe_allow_html=True)

        # 现实中的例子
        if insight.get("example"):
            st.markdown("#### 现实中的样子")
            st.markdown(f'<div class="thought-card">📌 {insight["example"]}</div>', unsafe_allow_html=True)

        # 思考题
        if insight.get("question"):
            st.markdown(f'''
<div class="reflection-question">
    <span class="question-label">停下来想想</span>
    {insight["question"]}
</div>
''', unsafe_allow_html=True)

        st.markdown("---")

    # 底部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 引言", use_container_width=True):
            st.session_state.current_section = "intro"
            st.rerun()
    with col3:
        if st.button("实践 →", use_container_width=True):
            st.session_state.current_section = "practice"
            st.rerun()


def render_practice(content):
    """实践页"""
    practice = content["practice"]

    st.markdown(f'<div class="thought-title">{practice["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="thought-subtitle">{practice["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 实践原则
    for item in practice["actions"]:
        st.markdown(f'<div class="section-title">{item["title"]}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="thought-card">{item["description"]}</div>', unsafe_allow_html=True)

        # 具体步骤
        if item.get("steps"):
            st.markdown("#### 具体怎么做")
            for step in item["steps"]:
                st.markdown(f'<div class="practice-box">✓ {step}</div>', unsafe_allow_html=True)

        st.markdown("---")

    # 底部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 核心思考", use_container_width=True):
            st.session_state.current_section = "core"
            st.rerun()
    with col3:
        if st.button("反思 →", use_container_width=True):
            st.session_state.current_section = "reflection"
            st.rerun()


def render_reflection(content):
    """反思页"""
    reflection = content["reflection"]

    st.markdown(f'<div class="thought-title">{reflection["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="thought-subtitle">{reflection["subtitle"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 深度思考题
    st.markdown('<div class="section-title">向自己提问</div>', unsafe_allow_html=True)

    for idx, question in enumerate(reflection["questions"], 1):
        st.markdown(f'''
<div class="reflection-question">
    <span class="question-label">问题 {idx}</span>
    {question["text"]}

    <div style="margin-top: 1rem; color: #7f8c8d; font-size: 0.9rem;">
    💡 提示：{question["hint"]}
    </div>
</div>
''', unsafe_allow_html=True)

        # 给用户写答案的空间
        user_answer = st.text_area(
            "写下你的想法...",
            key=f"answer_{idx}",
            placeholder="这里记录你的思考...",
            height=100
        )

        if user_answer:
            st.success("✓ 很好，写下想法让思考更深刻")

        st.markdown("---")

    # 金句回顾
    st.markdown('<div class="section-title">值得记住的话</div>', unsafe_allow_html=True)

    for quote in content["quotes"]:
        st.markdown(f'<div class="quote-text">{quote}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 完成按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 实践", use_container_width=True):
            st.session_state.current_section = "practice"
            st.rerun()

    with col2:
        if st.button("📚 返回书库", use_container_width=True, type="secondary"):
            st.session_state.current_book = None
            st.session_state.current_content = None
            st.rerun()


def main():
    """主函数"""
    init_session_state()

    # 侧边栏（极简）
    with st.sidebar:
        st.markdown('<div class="sidebar-title">📚 DeepRead</div>', unsafe_allow_html=True)

        if st.session_state.current_book:
            st.info(f"正在阅读: {st.session_state.current_book}")

            sections = {
                "toc": "📑 目录",
                "intro": "📖 引言",
                "core": "💭 核心思考",
                "practice": "🎯 实践",
                "reflection": "🪞 反思"
            }

            for key, label in sections.items():
                if st.button(label, key=f"sidebar_{key}", use_container_width=True):
                    st.session_state.current_section = key
                    st.rerun()

            st.markdown("---")
            if st.button("📚 返回书库", use_container_width=True):
                st.session_state.current_book = None
                st.session_state.current_content = None
                st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.85rem; color: #7f8c8d;">
        💡 给自己的思考<br/>
        留点时间<br/>
        慢慢来
        </div>
        """, unsafe_allow_html=True)

    # 主内容区
    if not st.session_state.current_book:
        render_library()
    else:
        render_book_reading()


if __name__ == "__main__":
    main()
