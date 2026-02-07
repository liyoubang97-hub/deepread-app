"""
DeepRead V3.8 - 导出功能版
改进：
1. 添加Markdown导出功能
2. 支持导出个人笔记
3. 支持导出完整学习笔记
4. 可导入飞书文档
"""

import streamlit as st
from pathlib import Path
import sys
import time
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64

sys.path.insert(0, str(Path(__file__).parent))

from lazy_loader import get_book_content, get_cache_info, clear_cache
from practice_tasks_enhanced import PRACTICE_TASKS

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

    /* ===== 内容卡片 - 极简设计 ===== */
    .content-block {
        background: #FFFFFF;
        border-radius: 0;
        padding: 1.5rem 0;
        margin: 1rem 0;
        border: none;
        border-left: 3px solid #E8EEF2;
    }

    .content-block.highlight {
        border-left: 3px solid #2D3436;
    }

    /* ===== 核心观点 - 移除米色背景，改为极简线条 ===== */
    .core-idea-box {
        background: #FFFFFF;
        color: #2D3436;
        padding: 1.5rem 0;
        margin: 1.5rem 0;
        border-left: 4px solid #2D3436;
        border-radius: 0;
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

    /* ===== 提问框 - 移除背景色 ===== */
    .question-block {
        background: #FFFFFF;
        border-left: 3px solid #636E72;
        border-radius: 0;
        padding: 1.5rem 0;
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

    /* ===== 金句卡片 - 移除背景色 ===== */
    .quote-block {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.05rem;
        font-style: italic;
        color: #2D3436;
        line-height: 1.75;
        padding: 1.5rem 0;
        background: #FFFFFF;
        border-radius: 0;
        margin: 1.25rem 0;
        position: relative;
        border-left: 3px solid #636E72;
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

    /* ===== 书籍卡片 - 优化设计 ===== */
    .book-card-container {
        display: flex;
        justify-content: center;
        align-items: stretch;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .book-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        flex: 1;
        max-width: 400px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }

    .book-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .book-card.available {
        cursor: pointer;
    }

    .book-card.available:hover {
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
    }

    .book-card.available:hover::before {
        opacity: 1;
    }

    .book-card.unavailable {
        opacity: 0.5;
        filter: grayscale(0.3);
    }

    .book-cover {
        font-size: 4.5rem;
        margin: 0.5rem 0;
        opacity: 0.9;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
        transition: transform 0.3s ease;
    }

    .book-card.available:hover .book-cover {
        transform: scale(1.1);
    }

    .book-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .book-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #2D3436;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }

    .book-author {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #667eea;
        font-weight: 600;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .book-description {
        font-family: 'Noto Serif SC', serif;
        font-size: 0.85rem;
        color: #636E72;
        line-height: 1.6;
        margin-bottom: 1rem;
        min-height: 2.5rem;
    }

    /* ===== 标签 - 优化设计 ===== */
    .tag-container {
        display: flex;
        gap: 0.4rem;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 0.75rem;
    }

    .tag {
        display: inline-block;
        padding: 0.3rem 0.75rem;
        background: linear-gradient(145deg, #f0f3f5 0%, #e8eef2 100%);
        color: #2D3436;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }

    .book-card.available:hover .tag {
        background: linear-gradient(145deg, #e8eef2 0%, #dfe6ed 100%);
        border-color: rgba(102, 126, 234, 0.2);
    }

    .tag.highlight {
        background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border-color: transparent;
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

    /* 收藏按钮样式 - 更优雅的图标按钮 */
    .stButton > button[title*="收藏"],
    .stButton > button[title*="取消"] {
        background: transparent !important;
        border: 1px solid #E8EEF2 !important;
        padding: 0.5rem !important;
        font-size: 1.5rem !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[title*="收藏"]:hover,
    .stButton > button[title*="取消"]:hover {
        background: #FFF5F5 !important;
        border-color: #FF6B6B !important;
        transform: scale(1.1);
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

    /* ===== 导出成功提示 ===== */
    .export-success {
        background: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .export-info {
        background: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)


# ==================== 图片生成函数 ====================

def create_quote_card_image(title, author, quote):
    """生成金句卡片图片 - 小红书风格"""
    # 小红书头图尺寸：1080x1440 (3:4比例)
    width = 1080
    height = 1440
    padding = 80

    # 字体大小（小红书风格：大而醒目）
    font_size_title = 56
    font_size_author = 36
    font_size_quote = 52
    font_size_small = 28

    # 尝试加载中文字体
    def load_chinese_font(size, bold=False):
        """加载中文字体，按优先级尝试"""
        font_list = []
        if bold:
            font_list = [
                "NotoSansSC-Bold.otf",
                "SimHei.ttf",
                "simhei.ttf",
                "STHeiti",
                "msyhbd.ttc",
                "Arial.ttf"
            ]
        else:
            font_list = [
                "NotoSansSC-Regular.otf",
                "SimSun.ttf",
                "simsun.ttf",
                "STSong",
                "msyh.ttc",
                "Arial.ttf"
            ]

        for font_name in font_list:
            try:
                return ImageFont.truetype(font_name, size)
            except:
                continue

        # 如果都失败，返回默认字体（不支持中文）
        try:
            return ImageFont.load_default()
        except:
            return None

    font_title = load_chinese_font(font_size_title, bold=True)
    font_author = load_chinese_font(font_size_author)
    font_quote = load_chinese_font(font_size_quote, bold=True)
    font_small = load_chinese_font(font_size_small)

    # 创建图片
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # 绘制柔和的渐变背景（从上到下）
    for y in range(min(200, height)):
        alpha = max(0, min(255, 255 - int(y * 1.2)))
        color = (
            max(102, 255 - int(y * 0.8)),
            max(126, 255 - int(y * 0.8)),
            234
        )
        draw.rectangle([(0, y), (width, y+1)], fill=color)

    # 绘制标题（居中，大而醒目）
    if font_title:
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 200), title, fill='#667eea', font=font_title)

    # 绘制作者（居中）
    if font_author:
        author_bbox = draw.textbbox((0, 0), author, font=font_author)
        author_width = author_bbox[2] - author_bbox[0]
        draw.text(((width - author_width) // 2, 280), author, fill='#636E72', font=font_author)

    # 绘制金句背景（优雅的卡片）
    quote_y = 400
    quote_card_height = 800
    draw.rounded_rectangle(
        [(padding, quote_y), (width - padding, quote_y + quote_card_height)],
        radius=40,
        fill='#F8F9FA',
        outline='#667eea'
    )

    # 绘制装饰线条
    draw.line([(padding + 60, quote_y + 80), (padding + 120, quote_y + 80)], fill='#667eea', width=6)
    draw.line([(width - padding - 60, quote_y + quote_card_height - 80), (width - padding - 120, quote_y + quote_card_height - 80)], fill='#667eea', width=6)

    # 绘制金句文本（简化处理，避免乱码）
    if font_quote:
        # 分行处理（最多显示4行）
        max_chars_per_line = 18
        quote_text = quote.replace('\n', ' ')
        lines = []
        for i in range(0, len(quote_text), max_chars_per_line):
            lines.append(quote_text[i:i+max_chars_per_line])

        # 限制最多4行
        lines = lines[:4]

        # 计算垂直居中
        total_quote_height = len(lines) * (font_size_quote + 20)
        start_y = quote_y + (quote_card_height - total_quote_height) // 2 - 40

        for i, line in enumerate(lines):
            line_bbox = draw.textbbox((0, 0), line, font=font_quote)
            line_width = line_bbox[2] - line_bbox[0]
            draw.text(
                ((width - line_width) // 2, start_y + i * (font_size_quote + 20)),
                line,
                fill='#2D3436',
                font=font_quote
            )

    # 绘制底部品牌
    brand_y = 1280
    if font_author:
        # 背景圆
        draw.ellipse(
            [(width//2 - 50, brand_y), (width//2 + 50, brand_y + 100)],
            fill='rgba(102, 126, 234, 0.1)',
            outline='#667eea',
            width=3
        )

        # 品牌
        brand_text = "DeepRead 深读"
        brand_bbox = draw.textbbox((0, 0), brand_text, font=font_author)
        brand_width = brand_bbox[2] - brand_bbox[0]
        draw.text((width//2 - brand_width//2, brand_y + 20), brand_text, fill='#667eea', font=font_author)

        # 标语
        if font_small:
            tagline = "深度阅读 · 沉浸思考"
            tagline_bbox = draw.textbbox((0, 0), tagline, font=font_small)
            tagline_width = tagline_bbox[2] - tagline_bbox[0]
            draw.text((width//2 - tagline_width//2, brand_y + 80), tagline, fill='#636E72', font=font_small)

    # 转换为字节
    buf = BytesIO()
    img.save(buf, format='PNG', quality=100)
    buf.seek(0)
    return buf.getvalue()


def create_reading_poster_image(title, author, emoji, tags, quote, stats):
    """生成阅读海报图片"""
    # 图片尺寸
    width = 600
    padding = 50

    try:
        font_title = ImageFont.truetype("msyhbd.ttc", 36)
        font_author = ImageFont.truetype("msyh.ttc", 22)
        font_tag = ImageFont.truetype("msyh.ttc", 14)
        font_quote = ImageFont.truetype("msyh.ttc", 24)
        font_number = ImageFont.truetype("msyhbd.ttc", 40)
        font_label = ImageFont.truetype("msyh.ttc", 14)
        font_small = ImageFont.truetype("msyh.ttc", 12)
    except:
        font_title = ImageFont.load_default()
        font_author = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_quote = ImageFont.load_default()
        font_number = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 临时图片用于测量
    temp_img = Image.new('RGB', (width, 100))
    temp_draw = ImageDraw.Draw(temp_img)

    # 计算高度
    title_h = 50
    emoji_h = 80
    author_h = 30
    tags_h = 30
    quote_h = 100
    stats_h = 180

    total_height = padding + emoji_h + title_h + author_h + tags_h + padding + quote_h + padding + stats_h + padding

    # 创建图片
    img = Image.new('RGB', (width, total_height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # 绘制背景
    draw.rectangle([(0, 0), (width, total_height)], fill='#FFFFFF')

    # 顶部区域
    y = padding

    # Emoji
    draw.text((width//2 - 40, y), emoji, font=ImageFont.load_default())
    y += emoji_h

    # 标题
    title_bbox = temp_draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w)//2, y), title, fill='#2D3436', font=font_title)
    y += title_h

    # 作者
    author_bbox = temp_draw.textbbox((0, 0), author, font=font_author)
    author_w = author_bbox[2] - author_bbox[0]
    draw.text(((width - author_w)//2, y), author, fill='#636E72', font=font_author)
    y += author_h + 10

    # 标签
    if tags:
        tag_x = padding
        for tag in tags[:3]:  # 最多3个标签
            tag_bbox = temp_draw.textbbox((0, 0), tag, font=font_tag)
            tag_w = tag_bbox[2] - tag_bbox[0] + 20
            if tag_x + tag_w > width - padding:
                break
            draw.rectangle([(tag_x, y), (tag_x + tag_w, y + 25)], fill='rgba(102, 126, 234, 0.1)', outline='#667eea')
            draw.text((tag_x + 10, y + 3), tag, fill='#667eea', font=font_tag)
            tag_x += tag_w + 10
        y += tags_h + 20

    # 金句区域
    draw.rectangle([(padding, y), (width - padding, y + quote_h)], fill='#F8F9FA', outline='#667eea', width=4)
    y += 15

    # 金句文本（简化处理，只显示前两行）
    quote_lines = quote.split('\n')[:2]
    for i, line in enumerate(quote_lines):
        draw.text((padding + 15, y + i * 30), line, fill='#2D3436', font=font_quote)

    y += quote_h + padding

    # 统计区域
    books_read = stats.get('books_read', 0)
    time_text = stats.get('time_display', '0分钟')

    # 已读书籍
    draw.rectangle([(padding, y), (width - padding, y + 80)], fill='rgba(102, 126, 234, 0.05)', outline='#667eea')
    draw.text((padding + 70, y + 15), str(books_read), fill='#667eea', font=font_number)
    draw.text((padding + 70, y + 50), '已读书籍', fill='#636E72', font=font_label)
    draw.text((padding + 15, y + 25), '📚', font=ImageFont.load_default())

    # 阅读时长
    y += 90
    draw.rectangle([(padding, y), (width - padding, y + 80)], fill='rgba(118, 75, 162, 0.05)', outline='#764ba2')
    draw.text((padding + 70, y + 15), time_text, fill='#764ba2', font=font_number)
    draw.text((padding + 70, y + 50), '阅读时长', fill='#636E72', font=font_label)
    draw.text((padding + 15, y + 25), '⏱️', font=ImageFont.load_default())

    # 底部品牌
    y = total_height - 40
    brand_text = "DeepRead 深读"
    brand_bbox = temp_draw.textbbox((0, 0), brand_text, font=font_author)
    brand_w = brand_bbox[2] - brand_bbox[0]
    draw.text(((width - brand_w)//2, y), brand_text, fill='#667eea', font=font_author)

    tagline = "深度阅读 · 沉浸思考"
    tagline_bbox = temp_draw.textbbox((0, 0), tagline, font=font_small)
    tagline_w = tagline_bbox[2] - tagline_bbox[0]
    draw.text(((width - tagline_w)//2, y + 25), tagline, fill='#636E72', font=font_small)

    # 转换为字节
    buf = BytesIO()
    img.save(buf, format='PNG', quality=95)
    buf.seek(0)
    return buf.getvalue()



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
    if "page_rerun" not in st.session_state:
        st.session_state.page_rerun = 0

    # 阅读统计数据
    if "reading_stats" not in st.session_state:
        st.session_state.reading_stats = {
            "total_books_read": set(),  # 已读过的书名集合
            "total_reading_time": 0,     # 总阅读时长（秒）
            "last_read_time": None       # 最后阅读时间
        }

    # 实践任务追踪数据
    if "practice_tracker" not in st.session_state:
        st.session_state.practice_tracker = {}  # 格式: {book_title: {week: {day: completed}}}


# 书籍数据
BOOKS_DATA = [
    {
        "title": "原子习惯",
        "author": "詹姆斯·克利尔",
        "description": "微小改变如何通过时间的复利，带来人生的巨大转变。每天进步1%，一年后你会进步37倍。",
        "tags": ["个人成长"],
        "available": True,
        "emoji": "📖"
    },
    {
        "title": "思考，快与慢",
        "author": "丹尼尔·卡尼曼",
        "description": "理解人类思维的双系统，认识直觉与理性的真相。系统1快速直觉，系统2缓慢理性。",
        "tags": ["认知提升"],
        "available": True,
        "emoji": "🧠"
    },
    {
        "title": "刻意练习",
        "author": "安德斯·艾利克森",
        "description": "揭秘天才的秘密：卓越不是天赋，而是正确的练习方法。突破1万小时的误区，用刻意练习在任何领域达到顶尖水平。",
        "tags": ["个人成长"],
        "available": True,
        "emoji": "🎯"
    },
    {
        "title": "深度工作",
        "author": "卡尔·纽波特",
        "description": "在分心的世界中，深度专注工作的能力是日益稀缺的资产。掌握深度工作法则，在浮躁的世界创造真正的价值。",
        "tags": ["职场发展"],
        "available": True,
        "emoji": "💼"
    },
    {
        "title": "原则",
        "author": "雷·达里欧",
        "description": "世界最大对冲基金创始人的人生智慧。如何通过原则化思维，在工作和生活中做出更好的决策，实现个人与组织的进化。",
        "tags": ["职场发展"],
        "available": True,
        "emoji": "📐"
    },
    {
        "title": "心流",
        "author": "米哈里·契克森米哈赖",
        "description": "最优体验的秘密。为什么有些人能在艰难困苦中找到乐趣，而有些人在优越环境中却感到空虚？幸福不是外在条件，而是内在秩序的建立。",
        "tags": ["个人成长"],
        "available": True,
        "emoji": "🌊"
    },
    {
        "title": "影响力",
        "author": "罗伯特·西奥迪尼",
        "description": "说服的心理学。为什么有些人能轻松影响他人，而你却总是被说服？掌握互惠、稀缺、社会认同等6大说服原则，既保护自己不被套路，也能道德地影响他人。",
        "tags": ["认知提升"],
        "available": True,
        "emoji": "🎭"
    },
    {
        "title": "终身成长",
        "author": "卡罗尔·德韦克",
        "description": "思维模式的力量。为什么有些人遇到挫折就放弃，而有些人越挫越勇？固定型思维vs成长型思维，这个小小的信念差异，决定了你的一生。",
        "tags": ["个人成长"],
        "available": True,
        "emoji": "🌱"
    }
]


def scroll_to_top():
    """滚动到页面顶部"""
    st.markdown("""
<script>
    // 多种方法确保滚动到顶部
    function scrollToTop() {
        // 方法1：window.scrollTo
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // 方法2：document.documentElement
        document.documentElement.scrollTop = 0;

        // 方法3：document.body
        document.body.scrollTop = 0;

        // 方法4：查找主容器
        const mainElement = document.querySelector('.main');
        if (mainElement) {
            mainElement.scrollTop = 0;
        }
    }

    // 页面加载后立即执行
    scrollToTop();

    // 延迟再次执行（确保渲染完成）
    setTimeout(scrollToTop, 100);
    setTimeout(scrollToTop, 300);
</script>
""", unsafe_allow_html=True)


def render_progress_bar(current_section):
    """
    显示阅读进度条

    current_section: 当前所在部分
    - 'intro': 引言
    - 'insights': 洞察
    - 'practice': 实践
    - 'reflection': 反思
    """
    sections = {
        'intro': {'name': '引言', 'icon': '📖', 'progress': 20},
        'insights': {'name': '洞察', 'icon': '💡', 'progress': 40},
        'practice': {'name': '实践', 'icon': '✅', 'progress': 60},
        'reflection': {'name': '反思', 'icon': '🤔', 'progress': 80}
    }

    # 获取当前部分的进度
    current = sections.get(current_section, sections['intro'])

    # 创建进度条HTML
    progress_bar = f"""
<div style="background: #F7F9FC; padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
        <div style="font-weight: 600; color: #1F2937; font-size: 0.9rem;">阅读进度</div>
        <div style="color: #6B7280; font-size: 0.8rem;">{current['progress']}%</div>
    </div>
    <div style="background: #E5E7EB; height: 8px; border-radius: 4px; overflow: hidden;">
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; width: {current['progress']}%; transition: width 0.3s ease;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
        <div style="font-size: 0.75rem; color: {'#667eea; font-weight: 600;' if current_section == 'intro' else '#9CA3AF'}">📖 引言</div>
        <div style="font-size: 0.75rem; color: {'#667eea; font-weight: 600;' if current_section == 'insights' else '#9CA3AF'}">💡 洞察</div>
        <div style="font-size: 0.75rem; color: {'#667eea; font-weight: 600;' if current_section == 'practice' else '#9CA3AF'}">✅ 实践</div>
        <div style="font-size: 0.75rem; color: {'#667eea; font-weight: 600;' if current_section == 'reflection' else '#9CA3AF'}">🤔 反思</div>
    </div>
</div>
"""

    st.markdown(progress_bar, unsafe_allow_html=True)


def generate_markdown(content, notes):
    """生成Markdown格式的学习笔记"""
    book_title = content["title"]
    author = content["author"]

    # 获取当前日期
    today = datetime.now().strftime("%Y年%m月%d日")

    md = f"""# {book_title} - 学习笔记

**作者**: {author}
**阅读日期**: {today}
**来源**: DeepRead 深度阅读

---

## 📖 引言

### {content["introduction"]["title"]}

{content["introduction"]["subtitle"]}

#### 为什么要读这本书

{content["introduction"]["why_read"]}

---

## 💡 核心洞察

### {content["core_thinking"]["title"]}

{content["core_thinking"]["subtitle"]}

"""

    # 添加每个洞察
    for idx, insight in enumerate(content["core_thinking"]["insights"], 1):
        md += f"""#### {idx}. {insight["title"]}

**核心观点**:
{insight["core_idea"]}

**为什么这很重要**:
{insight["why_matters"]}

"""
        if insight.get("example"):
            md += f"""**现实中的样子**:
{insight["example"]}

"""
        if insight.get("question"):
            md += f"""**想一想**: {insight["question"]}

"""
        md += "---\n\n"

    # 添加实践步骤
    md += f"""## ✅ 实践步骤

### {content["practice"]["title"]}

{content["practice"]["subtitle"]}

"""

    for action in content["practice"]["actions"]:
        md += f"""#### {action["title"]}

{action["description"]}

**步骤**:
"""
        for step in action.get("steps", []):
            md += f"- {step}\n"
        md += "\n"

    # 添加反思和用户笔记
    md += f"""## 🤔 反思与思考

### {content["reflection"]["title"]}

{content["reflection"]["subtitle"]}

"""

    for idx, question in enumerate(content["reflection"]["questions"], 1):
        md += f"""#### 问题 {idx}

{question["text"]}

**提示**: {question["hint"]}

"""
        # 添加用户的笔记
        note_key = f"q{idx}"
        if notes.get(note_key):
            md += f"""**我的思考**:

{notes[note_key]}

"""
        else:
            md += "**我的思考**: *（暂未填写）*\n\n"
        md += "---\n\n"

    # 添加金句
    md += """## 📝 值得记住的话

"""
    for quote in content["quotes"]:
        md += f"""> {quote}

"""

    md += f"""
---

*本笔记由 [DeepRead](https://github.com) 深度阅读工具生成*
"""

    return md


def generate_notes_only(content, notes):
    """只生成用户笔记的Markdown"""
    book_title = content["title"]
    author = content["author"]
    today = datetime.now().strftime("%Y年%m月%d日")

    md = f"""# {book_title} - 我的阅读笔记

**作者**: {author}
**记录日期**: {today}
**来源**: DeepRead 深度阅读

---

## 🤔 我的思考与反思

"""

    has_notes = False
    for idx, question in enumerate(content["reflection"]["questions"], 1):
        note_key = f"q{idx}"
        if notes.get(note_key):
            has_notes = True
            md += f"""### 问题 {idx}

{question["text"]}

**我的答案**:

{notes[note_key]}

---

"""

    if not has_notes:
        md += "*还没有填写任何笔记。回到阅读页面填写问题后，即可导出笔记。*\n\n"

    return md


def render_library():
    """书籍库页面 - 优化版"""
    # 滚动到顶部
    scroll_to_top()

    # 页面头部
    st.markdown("""
<div class="page-header">
    <div class="page-title">🧠 深度阅读</div>
    <div class="page-subtitle">给思考留出时间</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ========== 控制面板：搜索、排序、视图 ==========
    st.markdown('<div class="section-block">', unsafe_allow_html=True)

    # 第一行：搜索框和排序选择
    col_search, col_sort = st.columns([2, 1])

    with col_search:
        search_query = st.text_input(
            "🔍 搜索书籍",
            placeholder="输入书名、作者或关键词...",
            label_visibility="visible",
            key="book_search"
        )

    with col_sort:
        # 初始化排序选项
        if 'sort_option' not in st.session_state:
            st.session_state.sort_option = "默认"

        sort_option = st.selectbox(
            "📊 排序方式",
            ["默认", "书名 A-Z", "书名 Z-A", "作者", "可阅读优先"],
            label_visibility="visible",
            key="sort_select"
        )
        st.session_state.sort_option = sort_option

    st.markdown('</div>', unsafe_allow_html=True)

    # ========== 标签筛选 ==========
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; align-items: baseline; gap: 0.75rem; margin-bottom: 1rem;"><span style="font-size: 1.1rem; font-weight: 600;">🏷️ 按主题浏览</span><span style="font-size: 0.75rem; color: #636E72; font-weight: 400;">点击选择主题，可多选</span></div>', unsafe_allow_html=True)

    # 收集所有标签
    all_tags = set()
    for book in BOOKS_DATA:
        all_tags.update(book['tags'])

    # 标签按钮（横向排列，每行最多4个）
    tags_list = sorted(all_tags)
    num_rows = (len(tags_list) + 3) // 4  # 每行4个标签

    # 存储选中的标签
    if 'selected_tags' not in st.session_state:
        st.session_state.selected_tags = []

    # "全部"按钮和标签筛选状态显示
    col_clear, col_status = st.columns([1, 3])
    with col_clear:
        if st.button("📚 全部清除", key="tag_clear_all", use_container_width=True):
            st.session_state.selected_tags = []
            st.rerun()

    with col_status:
        if st.session_state.selected_tags:
            st.markdown(f'<div style="padding: 0.5rem; background: linear-gradient(145deg, #e8eef2 0%, #dfe6ed 100%); border-radius: 12px; text-align: center; color: #2D3436; font-size: 0.85rem; font-weight: 500;">已选: {", ".join(st.session_state.selected_tags)}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="padding: 0.5rem; background: #F0F3F5; border-radius: 12px; text-align: center; color: #636E72; font-size: 0.85rem;">未选择任何主题</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # 标签按钮（4列网格）
    for row in range(num_rows):
        tag_cols = st.columns(4)
        for col in range(4):
            tag_idx = row * 4 + col
            if tag_idx < len(tags_list):
                tag = tags_list[tag_idx]
                with tag_cols[col]:
                    is_selected = tag in st.session_state.selected_tags
                    if is_selected:
                        st.markdown(f"""
<div style="padding: 0.5rem; background: linear-gradient(145deg, #667eea 0%, #764ba2 100%); border-radius: 12px; text-align: center; color: #ffffff; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: 2px solid rgba(102, 126, 234, 0.3);">
    ✓ {tag}
</div>
""", unsafe_allow_html=True)
                        if st.button(f"取消 {tag}", key=f"tag_{tag}_off", use_container_width=True):
                            st.session_state.selected_tags.remove(tag)
                            st.rerun()
                    else:
                        st.markdown(f"""
<div style="padding: 0.5rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 12px; text-align: center; color: #2D3436; font-size: 0.8rem; font-weight: 500; cursor: pointer; border: 1px solid rgba(102, 126, 234, 0.1);">
    {tag}
</div>
""", unsafe_allow_html=True)
                        if st.button(f"选择 {tag}", key=f"tag_{tag}_on", use_container_width=True):
                            st.session_state.selected_tags.append(tag)
                            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ========== 视图切换 ==========
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    col_view_label, col_view_options = st.columns([1, 2])
    with col_view_label:
        st.markdown('<div style="font-size: 1.1rem; font-weight: 600;">🎨 视图</div>', unsafe_allow_html=True)

    with col_view_options:
        if 'view_mode' not in st.session_state:
            st.session_state.view_mode = "grid_2"  # 默认2列网格

        view_cols = st.columns(3)
        with view_cols[0]:
            if st.button("2列", key="view_2col", use_container_width=True, type="primary" if st.session_state.view_mode == "grid_2" else "secondary"):
                st.session_state.view_mode = "grid_2"
                st.rerun()
        with view_cols[1]:
            if st.button("3列", key="view_3col", use_container_width=True, type="primary" if st.session_state.view_mode == "grid_3" else "secondary"):
                st.session_state.view_mode = "grid_3"
                st.rerun()
        with view_cols[2]:
            if st.button("列表", key="view_list", use_container_width=True, type="primary" if st.session_state.view_mode == "list" else "secondary"):
                st.session_state.view_mode = "list"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    # ============================================

    # 筛选书籍 - 结合搜索和标签
    filtered_books = BOOKS_DATA.copy()

    # 先按标签筛选
    if st.session_state.selected_tags:
        filtered_books = [
            book for book in filtered_books
            if any(tag in book['tags'] for tag in st.session_state.selected_tags)
        ]

    # 再按搜索关键词筛选
    if search_query and search_query.strip():
        search_query = search_query.lower().strip()
        filtered_books = [
            book for book in filtered_books
            if (search_query in book['title'].lower() or
                search_query in book['author'].lower() or
                search_query in book['description'].lower() or
                any(search_query in tag.lower() for tag in book['tags']))
        ]

    # 排序
    if sort_option == "书名 A-Z":
        filtered_books.sort(key=lambda x: x['title'].lower())
    elif sort_option == "书名 Z-A":
        filtered_books.sort(key=lambda x: x['title'].lower(), reverse=True)
    elif sort_option == "作者":
        filtered_books.sort(key=lambda x: x['author'].lower())
    elif sort_option == "可阅读优先":
        filtered_books.sort(key=lambda x: not x['available'])

    # 显示结果数量
    st.markdown(f'<div style="text-align: center; color: #636E72; font-size: 0.8rem; margin: 1rem 0; padding: 0.5rem; background: linear-gradient(145deg, #f8f9fa 0%, #e8eef2 100%); border-radius: 12px; display: inline-block; width: 100%; box-sizing: border-box;">📚 显示 {len(filtered_books)} 本书</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    # ============================================

    # 根据视图模式渲染书籍
    if st.session_state.view_mode == "grid_2":
        # 2列网格
        for i in range(0, len(filtered_books), 2):
            book1 = filtered_books[i]
            book2 = filtered_books[i + 1] if i + 1 < len(filtered_books) else None

            if book2:
                col1, col2 = st.columns(2)
                with col1:
                    render_book_card(book1)
                with col2:
                    render_book_card(book2)
            else:
                render_book_card(book1, center=True)

    elif st.session_state.view_mode == "grid_3":
        # 3列网格
        for i in range(0, len(filtered_books), 3):
            books_in_row = filtered_books[i:i+3]
            cols = st.columns(len(books_in_row))
            for col, book in zip(cols, books_in_row):
                with col:
                    render_book_card(book)

    else:  # list view
        # 列表视图
        for book in filtered_books:
            render_book_card_list(book)


def render_book_card(book, center=False):
    """渲染单本书籍卡片"""
    card_class = "available" if book["available"] else "unavailable"

    # 初始化收藏列表
    if 'favorite_books' not in st.session_state:
        st.session_state.favorite_books = []

    # 检查是否已收藏
    is_favorite = book['title'] in st.session_state.favorite_books
    fav_emoji = "❤️" if is_favorite else "🤍"
    fav_title = "取消收藏" if is_favorite else "收藏"

    # 创建一个容器来包含卡片和按钮
    st.markdown(f'<div style="position: relative;">', unsafe_allow_html=True)

    # 书籍卡片
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

    st.markdown('</div>', unsafe_allow_html=True)

    # 按钮行 - 收藏和阅读
    if book["available"]:
        col_fav, col_read = st.columns([1, 5])

        with col_fav:
            if st.button(fav_emoji, key=f"fav_{book['title']}", help=fav_title):
                if is_favorite:
                    st.session_state.favorite_books.remove(book['title'])
                else:
                    st.session_state.favorite_books.append(book['title'])
                st.rerun()

        with col_read:
            if st.button(f"📖 开始阅读", key=f"read_{book['title']}", use_container_width=True):
                st.session_state.page_rerun += 1
                st.session_state.current_book = book['title']
                st.session_state.current_content = get_book_content(book['title'])
                st.session_state.current_section = "intro"
                st.rerun()
    else:
        st.markdown(f'<div style="text-align: center; color: #636E72; font-size: 0.75rem; font-style: italic; margin-top: 0.5rem;">即将推出</div>', unsafe_allow_html=True)


def render_book_card_list(book):
    """列表视图的书籍卡片"""
    card_class = "available" if book["available"] else "unavailable"

    # 初始化收藏列表
    if 'favorite_books' not in st.session_state:
        st.session_state.favorite_books = []

    # 检查是否已收藏
    is_favorite = book['title'] in st.session_state.favorite_books
    fav_emoji = "❤️" if is_favorite else "🤍"

    # 列表视图 - 横向布局
    st.markdown(f"""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
     border-radius: 16px; padding: 1.25rem; margin-bottom: 1rem;
     border: 1px solid rgba(102, 126, 234, 0.1);
     box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
     transition: all 0.3s ease; display: flex; gap: 1.5rem; align-items: center;">
    <div style="font-size: 3.5rem; text-align: center; min-width: 100px;">
        {book['emoji']}
    </div>
    <div style="flex: 1;">
        <div style="font-family: 'Noto Serif SC', serif; font-size: 1.2rem; font-weight: 700; color: #2D3436; margin-bottom: 0.3rem;">
            {book['title']}
        </div>
        <div style="font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #667eea; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">
            {book['author']}
        </div>
        <div style="font-family: 'Noto Serif SC', serif; font-size: 0.85rem; color: #636E72; line-height: 1.5; margin-bottom: 0.75rem;">
            {book['description']}
        </div>
        <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
            {(' '.join([f'<span class="tag {("highlight" if book["available"] else "")}">{tag}</span>' for tag in book['tags']]))}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # 按钮行
    col_fav, col_read = st.columns([1, 4])

    with col_fav:
        if st.button(fav_emoji, key=f"fav_list_{book['title']}", help="取消收藏" if is_favorite else "收藏"):
            if is_favorite:
                st.session_state.favorite_books.remove(book['title'])
            else:
                st.session_state.favorite_books.append(book['title'])
            st.rerun()

    with col_read:
        if book["available"]:
            if st.button(f"📖 开始阅读", key=f"read_list_{book['title']}", use_container_width=True, type="primary"):
                st.session_state.page_rerun += 1
                st.session_state.current_book = book['title']
                st.session_state.current_content = get_book_content(book['title'])
                st.session_state.current_section = "intro"
                st.rerun()
        else:
            st.markdown(f'<div style="text-align: center; color: #636E72; font-size: 0.75rem; font-style: italic; padding: 0.5rem;">即将推出</div>', unsafe_allow_html=True)


def render_introduction(content):
    """引言页 - 优雅简洁版"""
    intro = content["introduction"]

    # 滚动到顶部
    scroll_to_top()

    # 顶部导航
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← 返回", key="intro_back_library"):
            st.session_state.page_rerun += 1
            st.session_state.current_book = None
            st.session_state.current_content = None
            st.session_state.current_section = "library"
            st.rerun()

    # 阅读进度条
    render_progress_bar("intro")

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
        st.session_state.page_rerun += 1
        st.session_state.current_section = "insights"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_insights(content):
    """核心洞察页 - 优雅简洁版"""
    core = content["core_thinking"]

    # 滚动到顶部
    scroll_to_top()

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 引言", key="insights_back_intro"):
            st.session_state.page_rerun += 1
            st.session_state.current_section = "intro"
            st.rerun()

    st.markdown(f'<div class="section-title">{core["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{core["subtitle"]}</div>', unsafe_allow_html=True)

    # 阅读进度条
    render_progress_bar("insights")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 每个洞察
    for idx, insight in enumerate(core["insights"], 1):
        # 简约线条编号
        st.markdown(f'<div class="insight-number">— {idx:02d} —</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-title">{insight["title"]}</div>', unsafe_allow_html=True)

        # 核心观点 - 简洁优雅
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
            st.session_state.page_rerun += 1
            st.session_state.current_section = "intro"
            st.rerun()

    with col3:
        if st.button("实践 →", key="insights_to_practice"):
            st.session_state.page_rerun += 1
            st.session_state.current_section = "practice"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_practice(content):
    """实践页 - 优化版"""
    practice = content["practice"]

    # 滚动到顶部
    scroll_to_top()

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 洞察", key="practice_back_insights"):
            st.session_state.page_rerun += 1
            st.session_state.current_section = "insights"
            st.rerun()

    st.markdown(f'<div class="section-title">{practice["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{practice["subtitle"]}</div>', unsafe_allow_html=True)

    # 阅读进度条
    render_progress_bar("practice")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 实践步骤 - 优化布局
    for idx, item in enumerate(practice["actions"], 1):
        st.markdown('<div class="section-block">', unsafe_allow_html=True)

        # 添加编号徽章
        st.markdown(f"""
<div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
    <div style="background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
         color: #ffffff; width: 32px; height: 32px; border-radius: 50%;
         display: flex; align-items: center; justify-content: center;
         font-weight: 700; font-size: 0.9rem; flex-shrink: 0;">
        {idx}
    </div>
    <div class="subsection-header" style="margin: 0;">{item["title"]}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown(f'<div class="body-text" style="margin-bottom: 1.25rem; margin-left: 2.5rem;">{item["description"]}</div>', unsafe_allow_html=True)

        if item.get("steps"):
            st.markdown('<div class="step-list" style="margin-left: 2.5rem;">', unsafe_allow_html=True)
            for step in item["steps"]:
                st.markdown(f'<div class="step-item"><div class="step-number">✓</div><div class="step-text">{step}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ========== 30天实践计划入口 ==========
    if content["title"] in PRACTICE_TASKS:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # 检查是否已经开始
        book_title = content["title"]
        has_started = book_title in st.session_state.practice_tracker

        # 优雅的卡片设计
        st.markdown(f"""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
     border-radius: 16px; padding: 2rem; margin: 2rem 0;
     border: 2px solid rgba(102, 126, 234, 0.15);
     box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
     text-align: center; position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px;
         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);"></div>
    <div style="font-size: 1.5rem; font-weight: 700; color: #2D3436; margin-bottom: 0.5rem;">
        🎯 30天实践计划
    </div>
    <div style="font-size: 0.95rem; color: #636E72; margin-bottom: 1.5rem; line-height: 1.6;">
        不只是"知道"，更是"做到"<br/>
        每日任务 · 可追踪 · 成就系统
    </div>
</div>
""", unsafe_allow_html=True)

        if has_started:
            # 已开始，显示继续按钮
            if st.button("📊 继续我的实践计划", key="continue_practice", use_container_width=True, type="primary"):
                st.session_state.current_section = "practice_tasks"
                st.rerun()
        else:
            # 未开始，显示开始按钮
            if st.button("🚀 开始30天挑战", key="start_practice", use_container_width=True, type="primary"):
                # 初始化追踪数据
                st.session_state.practice_tracker[book_title] = {
                    "start_date": datetime.now().strftime("%Y-%m-%d"),
                    "current_day": 1,
                    "completed_days": {},
                    "badges": []
                }
                st.session_state.current_section = "practice_tasks"
                st.rerun()
    # =========================================

    # 底部导航
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 洞察", key="practice_bottom_back"):
            st.session_state.page_rerun += 1
            st.session_state.current_section = "insights"
            st.rerun()

    with col3:
        if st.button("反思 →", key="practice_to_reflection"):
            st.session_state.page_rerun += 1
            st.session_state.current_section = "reflection"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def generate_30day_poster(user_habits, completed_count, consecutive, total_progress, habits_completion, book_title, content):
    """生成30天成就海报"""
    # 计算每个习惯的完成情况
    habits_stats = []
    for habit in user_habits[:3]:
        habit_completed = sum(1 for day_data in habits_completion.values() if day_data.get(habit, False))
        habit_percentage = int((habit_completed / 30) * 100)
        habits_stats.append({"name": habit, "completed": habit_completed, "percentage": habit_percentage})

    # 生成热力图
    heatmap_grid = ""
    for week in range(4):
        heatmap_grid += "<div style='display: flex; gap: 4px; margin-bottom: 4px;'>"
        for day in range(7):
            day_num = week * 7 + day + 1
            if day_num > 30:
                break

            day_str = str(day_num)
            day_habits = habits_completion.get(day_str, {})
            completed_today = sum(day_habits.values())
            percentage = int((completed_today / 3) * 100)

            if percentage == 100:
                color = "#4CAF50"
            elif percentage >= 66:
                color = "#8BC34A"
            elif percentage >= 33:
                color = "#FFC107"
            else:
                color = "#E0E0E0"

            heatmap_grid += f"<div style='width: 28px; height: 28px; background: {color}; border-radius: 4px;'></div>"
        heatmap_grid += "</div>"

    poster_html = f"""
<div style="width: 100%; max-width: 600px; margin: 2rem auto; padding: 0; background: #ffffff; border-radius: 24px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15); overflow: hidden;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; text-align: center; position: relative;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
        <div style="font-size: 2rem; color: #ffffff; font-weight: 700; margin-bottom: 0.5rem;">30天挑战成功！</div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 1rem;">{book_title} · 微习惯养成计划</div>
        <div style="display: flex; justify-content: center; gap: 2rem;">
            <div>
                <div style="font-size: 2rem; color: #ffffff; font-weight: 700;">{completed_count}</div>
                <div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.8);">总打卡</div>
            </div>
            <div>
                <div style="font-size: 2rem; color: #ffffff; font-weight: 700;">{consecutive}</div>
                <div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.8);">连续天数</div>
            </div>
            <div>
                <div style="font-size: 2rem; color: #ffffff; font-weight: 700;">{total_progress}%</div>
                <div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.8);">完成度</div>
            </div>
        </div>
    </div>

    <div style="padding: 2rem;">
        <div style="margin-bottom: 2rem;">
            <div style="font-size: 1rem; color: #2D3436; font-weight: 600; margin-bottom: 1rem; text-align: center;">📊 三个习惯完成情况</div>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                {''.join([f"""
                <div style="flex: 1; text-align: center; padding: 1rem; background: #F8F9FA; border-radius: 12px;">
                    <div style="font-size: 0.8rem; color: #636E72; margin-bottom: 0.5rem;">{stat['name'][:15]}...</div>
                    <div style="font-size: 1.5rem; color: #667eea; font-weight: 700;">{stat['completed']}/30</div>
                    <div style="font-size: 0.9rem; color: #764ba2;">{stat['percentage']}%</div>
                </div>
                """ for stat in habits_stats])}
            </div>
        </div>

        <div style="margin-bottom: 2rem;">
            <div style="font-size: 1rem; color: #2D3436; font-weight: 600; margin-bottom: 1rem; text-align: center;">📅 30天打卡热力图</div>
            <div style="display: flex; justify-content: center;">
                {heatmap_grid}
            </div>
            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; font-size: 0.75rem; color: #636E72;">
                <div style="display: flex; align-items: center; gap: 0.25rem;"><div style="width: 16px; height: 16px; background: #4CAF50; border-radius: 3px;"></div> 全完成</div>
                <div style="display: flex; align-items: center; gap: 0.25rem;"><div style="width: 16px; height: 16px; background: #8BC34A; border-radius: 3px;"></div> 良好</div>
                <div style="display: flex; align-items: center; gap: 0.25rem;"><div style="width: 16px; height: 16px; background: #FFC107; border-radius: 3px;"></div> 一般</div>
                <div style="display: flex; align-items: center; gap: 0.25rem;"><div style="width: 16px; height: 16px; background: #E0E0E0; border-radius: 3px;"></div> 未完成</div>
            </div>
        </div>

        <div style="text-align: center; padding-top: 1.5rem; border-top: 1px solid #E8EEF2;">
            <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 25px; color: #667eea; font-weight: 600; font-size: 0.9rem;">
                <span>🧠</span><span>DeepRead 深读</span>
            </div>
            <div style="font-size: 0.75rem; color: #636E72; margin-top: 0.75rem; font-style: italic;">微习惯 · 大改变</div>
        </div>
    </div>
</div>

<div style="text-align: center; margin: 2rem 0; color: #636E72; font-size: 0.85rem;">
<strong>💡 如何分享：</strong><br/>1. 在电脑上：截图后保存图片<br/>2. 在手机上：长按海报区域保存图片<br/>3. 分享到朋友圈、小红书、微博等社交平台
</div>
"""
    st.markdown(poster_html, unsafe_allow_html=True)


def render_practice_tasks(content):
    """30天实践任务追踪页 - 轻松版本"""
    book_title = content["title"]

    # 检查是否有实践任务
    if book_title not in PRACTICE_TASKS:
        st.error("此书籍暂无实践任务")
        return

    practice_data = PRACTICE_TASKS[book_title]

    # 滚动到顶部
    scroll_to_top()

    # 顶部导航
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← 返回", key="practice_tasks_back"):
            st.session_state.current_section = "practice"
            st.rerun()

    # 获取用户进度数据
    tracker = st.session_state.practice_tracker.get(book_title, {})
    # 新的数据结构：记录每天每个习惯的完成情况
    # habits_completion: { "1": {"habit1": true, "habit2": false, "habit3": true}, ... }
    habits_completion = tracker.get("habits_completion", {})

    # 计算总完成度：3个习惯 × 30天 = 90个可能的打卡
    total_slots = 3 * 30
    completed_count = 0
    for day_data in habits_completion.values():
        completed_count += sum(day_data.values())
    total_progress = int((completed_count / total_slots) * 100)

    # 计算连续天数（以天为单位，当天3个习惯都完成才算）
    consecutive = 0
    for day in range(1, 31):
        day_str = str(day)
        if day_str in habits_completion:
            day_habits = habits_completion[day_str]
            if len(day_habits) == 3 and all(day_habits.values()):
                consecutive += 1
            else:
                break
        else:
            break

    # 让用户选择要养成的3个微习惯
    user_habits = tracker.get("user_habits", [])

    # 检查是否完成了30天挑战（必须100%完成）
    if total_progress >= 100 and user_habits:
        # 显示30天完成庆祝页面
        st.balloons()

        st.markdown(f"""<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; border-radius: 24px; margin-bottom: 2rem; text-align: center; position: relative; overflow: hidden;">
    <div style="position: absolute; top: -80px; right: -80px; width: 200px; height: 200px; background: rgba(255, 255, 255, 0.1); border-radius: 50%;"></div>
    <div style="position: absolute; bottom: -60px; left: -60px; width: 150px; height: 150px; background: rgba(255, 255, 255, 0.08); border-radius: 50%;"></div>

    <div style="position: relative; z-index: 2;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🎉</div>
        <div style="font-size: 2.5rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem;">恭喜你完成了30天挑战！</div>
        <div style="font-size: 1.2rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 2rem;">
            你用坚持证明了：微习惯的力量是巨大的
        </div>

        <div style="display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; font-weight: 700; color: #ffffff;">{completed_count}</div>
                <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.8); margin-top: 0.5rem;">总打卡数</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; font-weight: 700; color: #ffffff;">{consecutive}</div>
                <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.8); margin-top: 0.5rem;">最长连续天数</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; font-weight: 700; color: #ffffff;">{total_progress}%</div>
                <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.8); margin-top: 0.5rem;">完成度</div>
            </div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

        # 30天打卡热力图
        st.markdown("### 📅 30天打卡记录")
        st.markdown("**每一天的坚持，都是向更好的自己迈进**", unsafe_allow_html=True)

        heatmap_data = []
        for day in range(1, 31):
            day_str = str(day)
            day_habits = habits_completion.get(day_str, {})
            completed_today = sum(day_habits.values())
            percentage = int((completed_today / 3) * 100)

            if percentage == 100:
                color = "#4CAF50"
                emoji = "🌟"
            elif percentage >= 66:
                color = "#8BC34A"
                emoji = "✓"
            elif percentage >= 33:
                color = "#FFC107"
                emoji = "○"
            else:
                color = "#E0E0E0"
                emoji = "·"

            heatmap_data.append({"day": day, "color": color, "emoji": emoji, "percentage": percentage})

        # 显示热力图
        weeks_grid = [heatmap_data[i:i+7] for i in range(0, 30, 7)]

        for week_idx, week_data in enumerate(weeks_grid, 1):
            cols = st.columns(7)
            for col_idx, day_data in enumerate(week_data):
                with cols[col_idx]:
                    st.markdown(f"""
<div style="background: {day_data['color']}; padding: 1rem 0.5rem; border-radius: 12px; text-align: center; min-height: 80px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
    <div style="font-size: 1.5rem;">{day_data['emoji']}</div>
    <div style="font-size: 0.75rem; color: rgba(0,0,0,0.6); margin-top: 0.25rem;">第{day_data['day']}天</div>
</div>
""", unsafe_allow_html=True)

        # 反思区域
        st.markdown("---")
        st.markdown("### 💭 写下你的30天感悟")
        st.markdown("**回顾这段旅程，记录你的成长和变化**", unsafe_allow_html=True)

        reflection_key = f"30day_reflection_{book_title}"
        saved_reflection = st.session_state.get(reflection_key, "")

        reflection = st.text_area(
            "我的30天心得...",
            value=saved_reflection,
            placeholder="这30天给我带来的改变是...",
            height=150,
            key="reflection_input"
        )

        col_save_ref1, col_save_ref2, col_save_ref3 = st.columns([1, 2, 1])
        with col_save_ref2:
            if st.button("💾 保存我的感悟", use_container_width=True, type="primary"):
                st.session_state[reflection_key] = reflection
                st.success("✅ 感悟已保存！感谢你的坚持！")
                st.balloons()

        # 下一步建议
        st.markdown("---")
        st.markdown("### 🚀 接下来做什么？")

        suggestion_cols = st.columns(3)
        with suggestion_cols[0]:
            st.markdown("""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.1); text-align: center; min-height: 220px; display: flex; flex-direction: column; justify-content: center;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">🔄</div>
    <div style="font-size: 1.1rem; font-weight: 600; color: #2D3436; margin-bottom: 0.5rem;">继续这3个习惯</div>
    <div style="font-size: 0.85rem; color: #636E72;">习惯已经养成，继续巩固让它成为自动行为</div>
</div>
""", unsafe_allow_html=True)

        with suggestion_cols[1]:
            st.markdown("""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.1); text-align: center; min-height: 220px; display: flex; flex-direction: column; justify-content: center;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">⬆️</div>
    <div style="font-size: 1.1rem; font-weight: 600; color: #2D3436; margin-bottom: 0.5rem;">提升难度</div>
    <div style="font-size: 0.85rem; color: #636E72;">增加时长或强度，让习惯更有挑战性</div>
</div>
""", unsafe_allow_html=True)

        with suggestion_cols[2]:
            st.markdown("""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.1); text-align: center; min-height: 220px; display: flex; flex-direction: column; justify-content: center;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">➕</div>
    <div style="font-size: 1.1rem; font-weight: 600; color: #2D3436; margin-bottom: 0.5rem;">培养新习惯</div>
    <div style="font-size: 0.85rem; color: #636E72;">开启新的30天挑战，养成更多好习惯</div>
</div>
""", unsafe_allow_html=True)

        # 生成30天成就海报按钮
        st.markdown("---")
        st.markdown("### 🖼️ 分享你的成就")
        if st.button("🎨 生成30天成就海报", use_container_width=True, type="primary"):
            generate_30day_poster(user_habits, completed_count, consecutive, total_progress, habits_completion, book_title, content)

        # 重新开始按钮
        if st.button("🔄 重新开始30天挑战", key="restart_30days"):
            if book_title in st.session_state.practice_tracker:
                del st.session_state.practice_tracker[book_title]["habits_completion"]
            st.session_state.selected_week = 1
            st.rerun()

        return

    # 让用户选择要养成的3个微习惯
    user_habits = tracker.get("user_habits", [])
    if not user_habits or len(user_habits) == 0:
        st.markdown("### 🌱 设定你的三个微习惯")
        st.markdown("**选择3个简单的微习惯，用30天养成它们！**", unsafe_allow_html=True)

        st.markdown('<br>', unsafe_allow_html=True)

        # 初始化session state
        if "selected_habits" not in st.session_state:
            st.session_state.selected_habits = []

        # 预设选项
        habit_options = [
            "📚 每天阅读10分钟",
            "🧘 每天冥想5分钟",
            "🏃 每天运动15分钟",
            "✍️ 每天写日记",
            "⏰ 每天早起10分钟",
            "💧 每天喝8杯水",
            "📖 每天背诵5个单词",
            "🏠 每天整理房间10分钟",
            "📵 每天不看手机1小时",
            "🙏 每天感恩3件事",
            "🥗 每天吃一份水果",
            "🌙 每天早睡10分钟",
            "💪 每天做10个深蹲",
            "🎨 每天画画5分钟",
            "🎵 每天听一首新歌"
        ]

        # 显示当前已选择的习惯
        if st.session_state.selected_habits:
            st.markdown("### ✅ 已选择的习惯")
            for idx, habit in enumerate(st.session_state.selected_habits, 1):
                st.markdown(f"**{idx}. {habit}**")

            st.markdown(f"**已选择 {len(st.session_state.selected_habits)}/3 个习惯**")

            if len(st.session_state.selected_habits) >= 3:
                st.success("🎉 已完成选择！")
                if st.button("✓ 确认并开始", type="primary", use_container_width=True):
                    if book_title not in st.session_state.practice_tracker:
                        st.session_state.practice_tracker[book_title] = {"completed_days": {}}
                    st.session_state.practice_tracker[book_title]["user_habits"] = st.session_state.selected_habits[:3]
                    st.success(f"太棒了！你要培养的三个习惯是：**{', '.join(st.session_state.selected_habits[:3])}**")
                    st.rerun()
            else:
                st.info(f"再选择 **{3 - len(st.session_state.selected_habits)}** 个习惯即可开始")

            st.markdown("---")

        st.markdown("### 📋 可选的微习惯")
        st.markdown("点击选择你想要养成的习惯：", unsafe_allow_html=True)

        # 使用3列布局显示选项
        cols = st.columns(3)
        for idx, habit in enumerate(habit_options):
            col_idx = idx % 3
            with cols[col_idx]:
                is_selected = habit in st.session_state.selected_habits
                button_label = f"✓ {habit}" if is_selected else habit

                if st.button(button_label, key=f"habit_{idx}", use_container_width=True):
                    if is_selected:
                        st.session_state.selected_habits.remove(habit)
                    else:
                        if len(st.session_state.selected_habits) < 3:
                            st.session_state.selected_habits.append(habit)
                        else:
                            st.warning("最多只能选择3个习惯，请先取消一个")
                    st.rerun()

        # 自定义输入
        st.markdown("---")
        st.markdown("### ✏️ 或者自定义你的习惯")
        custom_habit = st.text_input(
            "输入自定义习惯（添加emoji会更生动哦）",
            placeholder="例如：🎯 每天练习投篮10次",
            key="custom_habit_input"
        )

        col_cust1, col_cust2, col_cust3 = st.columns([1, 1, 1])
        with col_cust2:
            if st.button("添加自定义习惯", use_container_width=True):
                if custom_habit.strip():
                    if len(st.session_state.selected_habits) < 3:
                        st.session_state.selected_habits.append(custom_habit.strip())
                        st.success(f"已添加：**{custom_habit.strip()}**")
                        st.rerun()
                    else:
                        st.warning("最多只能选择3个习惯，请先取消一个")
                else:
                    st.warning("请输入一个习惯")

        st.markdown('<br>', unsafe_allow_html=True)
        return

    # 显示已选择的三个习惯
    st.markdown("### 🎯 正在培养的三个习惯")
    habits_display = st.columns(3)
    for idx, habit in enumerate(user_habits[:3]):
        with habits_display[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 16px; text-align: center; color: white; box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);">
                <div style="font-size: 1.1rem; font-weight: 600;">{habit}</div>
            </div>
            """, unsafe_allow_html=True)

    # 提供修改习惯的选项
    with st.expander("✏️ 想要更换习惯？"):
        st.write("**当前习惯：**", ", ".join(user_habits[:3]))
        st.warning("更换习惯会重新开始30天挑战哦！")
        if st.button("重新选择习惯", key="change_habits"):
            if book_title in st.session_state.practice_tracker:
                del st.session_state.practice_tracker[book_title]["user_habits"]
            st.session_state.selected_habits = []
            st.rerun()

    st.markdown("---")

    # 温暖的进度卡片 - 简洁清晰的设计

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_a:
        st.metric("连续坚持", f"{consecutive}天")
    with col_c:
        st.metric("完成度", f"{total_progress}%")

    st.markdown(f"**{practice_data['subtitle']}**", unsafe_allow_html=True)
    st.progress(total_progress / 100)
    st.markdown(f"### {completed_count}/{total_slots}个习惯完成", unsafe_allow_html=True)

    # 周选择器 - 轻松的Tab风格
    weeks = [
        {"key": "week_1", "label": "第1周", "emoji": "🌱", "desc": "启动 (1-7天)"},
        {"key": "week_2", "label": "第2周", "emoji": "🌿", "desc": "稳定 (8-14天)"},
        {"key": "week_3", "label": "第3周", "emoji": "🌳", "desc": "成长 (15-21天)"},
        {"key": "week_4", "label": "第4周", "emoji": "🏆", "desc": "达成 (22-30天)"}
    ]

    # 使用session state存储当前选择的周
    if "selected_week" not in st.session_state:
        st.session_state.selected_week = 1

    # 周选择按钮
    st.markdown('<div style="margin: 1.5rem 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 1rem; color: #636E72; margin-bottom: 1rem; text-align: center;">💫 点击切换到其他周</div>', unsafe_allow_html=True)
    week_cols = st.columns(4)

    for idx, week_info in enumerate(weeks):
        with week_cols[idx]:
            is_selected = (st.session_state.selected_week == idx + 1)

            if st.button(
                f"{week_info['emoji']} {week_info['label']}\n{week_info['desc']}",
                key=f"week_{idx+1}",
                use_container_width=True
            ):
                st.session_state.selected_week = idx + 1
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # 获取当前周的任务
    week_key = f"week_{st.session_state.selected_week}"
    current_week_data = practice_data.get(week_key, {})

    if not current_week_data:
        st.warning("本周任务尚未开放")
        return

    # 本周简介 - 轻松风格
    st.markdown(f"""
<div style="background: #F8F9FA; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #667eea;">
    <div style="font-size: 1.1rem; font-weight: 600; color: #2D3436; margin-bottom: 0.5rem;">
        {current_week_data["title"]}
    </div>
    <div style="font-size: 0.95rem; color: #636E72; line-height: 1.6; margin-bottom: 1rem;">
        {current_week_data["objective"]}
    </div>
    <div style="font-size: 0.85rem; color: #667eea; font-style: italic;">
        💡 {current_week_data["focus"]}
    </div>
</div>
""", unsafe_allow_html=True)

    # 显示每日任务 - 卡片式，自由浏览
    # 第三周有path_a和path_b两种路径，默认选择path_a
    daily_tasks = current_week_data.get("daily_tasks", [])
    if not daily_tasks and "path_a" in current_week_data:
        # 如果有路径选择，默认使用path_a
        path_data = current_week_data.get("path_a", {})
        daily_tasks = path_data.get("daily_tasks", [])
        if daily_tasks:
            st.info(f"📍 当前路径：{path_data.get('title', '路径A')} - {path_data.get('condition', '')}")

    # 计算本周的起始和结束天数
    # 第4周特殊处理：显示第22-30天（9天），其他周显示7天
    if st.session_state.selected_week == 4:
        week_start = 22
        week_end = 30
    else:
        week_start = (st.session_state.selected_week - 1) * 7 + 1
        week_end = st.session_state.selected_week * 7

    week_tasks = [task for task in daily_tasks if week_start <= task["day"] <= week_end]

    for task in week_tasks:
        task_day = task["day"]
        day_str = str(task_day)

        # 获取当天3个习惯的完成状态
        day_completion = habits_completion.get(day_str, {})
        completed_count_today = sum(day_completion.values())
        all_completed = (completed_count_today == 3)

        if all_completed:
            card_style = """
                style="
                    background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                    border: none;
                    border-radius: 16px;
                    padding: 1.8rem;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 8px 24px rgba(76, 175, 80, 0.15), 0 2px 8px rgba(76, 175, 80, 0.1);
                    position: relative;
                    overflow: hidden;
                "
            """
        else:
            card_style = """
                style="
                    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
                    border: 1px solid rgba(102, 126, 234, 0.1);
                    border-radius: 16px;
                    padding: 1.8rem;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.05);
                    position: relative;
                    overflow: hidden;
                "
            """

        st.markdown(f"<div {card_style}>", unsafe_allow_html=True)

        # 任务头部
        col_left, col_right = st.columns([3, 2])

        with col_left:
            # 标题
            status_emoji = "✅" if all_completed else "📌"
            title_style = "color: #2D3436;" if not all_completed else "color: #4CAF50;"
            st.markdown(f"<div style='font-size: 1.1rem; font-weight: 600; {title_style} margin-bottom: 0.5rem;'>{status_emoji} 第{task_day}天：{task['task']}</div>", unsafe_allow_html=True)

            # 说明
            st.markdown(f"<div style='font-size: 0.9rem; color: #636E72; line-height: 1.6; margin-bottom: 1rem;'>{task['instruction']}</div>", unsafe_allow_html=True)

            # 如果有行动项，用更自然的方式展示
            if task.get("action_items"):
                with st.expander("📝 具体怎么做", expanded=False):
                    for item in task["action_items"]:
                        st.markdown(f"<div style='color: #636E72; margin: 0.5rem 0;'>• {item}</div>", unsafe_allow_html=True)

            # 如果有示例
            if task.get("examples"):
                with st.expander("💡 参考一下", expanded=False):
                    for key, value in task["examples"].items():
                        st.markdown(f"**{key}**: {value}")

        with col_right:
            # 三个习惯的打卡checkbox
            st.markdown("**今日打卡**", unsafe_allow_html=True)
            st.markdown(f"<small>已完成 {completed_count_today}/3 个习惯</small>", unsafe_allow_html=True)

            for habit_idx, habit in enumerate(user_habits[:3]):
                habit_key = f"day_{task_day}_habit_{habit_idx}"
                is_habit_completed = day_completion.get(habit, False)

                new_status = st.checkbox(
                    habit,
                    key=habit_key,
                    value=is_habit_completed,
                    label_visibility="visible"
                )

                # 只有状态变化时才更新
                if new_status != is_habit_completed:
                    # 确保数据结构存在
                    if "habits_completion" not in st.session_state.practice_tracker[book_title]:
                        st.session_state.practice_tracker[book_title]["habits_completion"] = {}
                    if day_str not in st.session_state.practice_tracker[book_title]["habits_completion"]:
                        st.session_state.practice_tracker[book_title]["habits_completion"][day_str] = {}

                    st.session_state.practice_tracker[book_title]["habits_completion"][day_str][habit] = new_status
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # 成就展示 - 只在有成就时显示
    if tracker.get("badges"):
        st.markdown('<div style="margin: 2rem 0; padding: 1.5rem; background: linear-gradient(135deg, #FFF9E6 0%, #FFF3CD 100%); border-radius: 16px; text-align: center;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 1rem; color: #856404; margin-bottom: 1rem;">🏆 解锁的成就</div>', unsafe_allow_html=True)

        badges_html = '<div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">'
        for badge in tracker["badges"]:
            badges_html += f'<div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #ffffff; padding: 0.5rem 1.25rem; border-radius: 20px; font-weight: 600; font-size: 0.9rem; box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);">{badge}</div>'
        badges_html += '</div>'
        st.markdown(badges_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 实用小贴士 - 使用 Streamlit 原生组件确保对齐
    st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #2D3436; margin-bottom: 1.5rem; text-align: center;">💡 实用小贴士</div>', unsafe_allow_html=True)

    # 使用 expander 展示提示
    tips = [
        {
            "emoji": "📝",
            "title": "每天记录",
            "content": "花1分钟记录今天的实践感受，比如：「今天我按时完成了2分钟阅读，感觉很不错！」"
        },
        {
            "emoji": "🔄",
            "title": "定期回顾",
            "content": "每周日花10分钟回顾这周的完成情况，调整下周计划"
        },
        {
            "emoji": "🎯",
            "title": "关注连续",
            "content": "连续打卡会解锁成就徽章，让习惯养成更有趣"
        }
    ]

    for tip in tips:
        with st.expander(f"{tip['emoji']} {tip['title']}", expanded=False):
            st.markdown(f"<div style='color: #636E72; line-height: 1.6; padding: 0.5rem 0;'>{tip['content']}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 底部快速导航
    st.markdown('<div style="margin: 3rem 0 2rem 0;">', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size: 1.1rem; font-weight: 600; color: #2D3436; margin: 2rem 0 1rem 0; text-align: center;">📅 快速切换周</div>', unsafe_allow_html=True)

    nav_cols = st.columns(4)
    for idx in range(4):
        with nav_cols[idx]:
            week_num = idx + 1
            is_current = (st.session_state.selected_week == week_num)
            emoji = ["🌱", "🌿", "🌳", "🏆"][idx]

            if st.button(
                f"{emoji} 第{week_num}周",
                key=f"nav_week_{week_num}",
                use_container_width=True
            ):
                st.session_state.selected_week = week_num
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def calculate_consecutive_days(completed_days):
    """计算连续完成天数"""
    if not completed_days:
        return 0

    consecutive = 0
    for day in range(1, 32):  # 最多31天
        if str(day) in completed_days and completed_days[str(day)]:
            consecutive += 1
        else:
            break

    return consecutive


def render_reflection(content):
    """反思页 - 优化版"""
    reflection = content["reflection"]

    # 更新阅读统计
    current_book = st.session_state.current_book
    if current_book and current_book not in st.session_state.reading_stats["total_books_read"]:
        st.session_state.reading_stats["total_books_read"].add(current_book)

    # 计算本次阅读时长并累加
    if 'reading_start_time' in st.session_state:
        import time
        elapsed = time.time() - st.session_state.reading_start_time
        st.session_state.reading_stats["total_reading_time"] += int(elapsed)
        st.session_state.reading_stats["last_read_time"] = time.time()

    # 滚动到顶部
    scroll_to_top()

    # 顶部导航
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 实践", key="reflection_back_practice"):
            st.session_state.page_rerun += 1
            st.session_state.current_section = "practice"
            st.rerun()

    st.markdown(f'<div class="section-title">{reflection["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{reflection["subtitle"]}</div>', unsafe_allow_html=True)

    # 阅读进度条
    render_progress_bar("reflection")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 思考题 - 优化布局
    for idx, question in enumerate(reflection["questions"], 1):
        st.markdown(f'<div class="section-block">', unsafe_allow_html=True)

        # 优雅的问题卡片设计
        st.markdown(f"""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
     border-radius: 16px; padding: 1.5rem;
     border: 1px solid rgba(102, 126, 234, 0.1);
     box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
     margin-bottom: 1rem;">
    <div style="display: flex; gap: 1rem; align-items: flex-start;">
        <div style="background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
             color: #ffffff; width: 36px; height: 36px; border-radius: 50%;
             display: flex; align-items: center; justify-content: center;
             font-weight: 700; font-size: 1rem; flex-shrink: 0;">
            {idx}
        </div>
        <div style="flex: 1;">
            <div style="font-size: 1.05rem; color: #2D3436; line-height: 1.7; font-weight: 500; margin-bottom: 0.75rem;">
                {question["text"]}
            </div>
            <div style="font-size: 0.85rem; color: #636E72; line-height: 1.6; font-style: italic;">
                💡 {question["hint"]}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

        # 笔记输入框
        st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
        user_note = st.text_area(
            "笔记",
            key=f"note_{idx}",
            placeholder="在这里记录你的思考，让想法更深刻...",
            height=100,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if user_note:
            st.success("✓ 已记录")
            st.session_state.notes[f"q{idx}"] = user_note

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # 金句回顾 - 优化设计
    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-header">值得记住的话</div>', unsafe_allow_html=True)

    for quote in content["quotes"]:
        st.markdown(f"""
<div style="background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
     border-left: 4px solid #667eea;
     padding: 1.5rem; margin-bottom: 1rem;
     border-radius: 0 12px 12px 0;
     box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);">
    <div style="font-size: 1.1rem; line-height: 1.8; color: #2D3436; font-style: italic; position: relative;">
        {quote}
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ========== 分享功能区域 ==========
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✨ 分享你的阅读</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #636E72; font-size: 0.85rem; margin-bottom: 2rem;">生成精美卡片，分享到朋友圈或社交媒体</div>', unsafe_allow_html=True)

    # 金句选择
    selected_quote = st.selectbox(
        "选择要分享的金句",
        content["quotes"],
        key="share_quote_select"
    )

    # 按钮组 - 垂直布局
    if st.button("🎨 金句卡片", key=f"quote_card_{content['title']}", use_container_width=True):
        # 只处理换行
        quote_display = selected_quote.replace('\n', '<br/>')
        title_display = content['title'].replace('\n', '<br/>')
        author_display = content['author'].replace('\n', '<br/>')

        card_html = f'<div style="width: 100%; max-width: 500px; margin: 2rem auto; padding: 3rem 2rem; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08); text-align: center; position: relative; overflow: hidden; border: 1px solid rgba(102, 126, 234, 0.1);"><div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);"></div><div style="margin-bottom: 2.5rem;"><div style="font-size: 1.1rem; color: #667eea; font-weight: 600; margin-bottom: 0.5rem;">{title_display}</div><div style="font-size: 0.9rem; color: #636E72; font-style: italic;">{author_display}</div></div><div style="background: linear-gradient(145deg, #f8f9fa 0%, #e8eef2 100%); border-radius: 16px; padding: 2rem; margin-bottom: 2.5rem; border: 1px solid rgba(102, 126, 234, 0.1);"><div style="font-size: 1.4rem; line-height: 1.9; color: #2D3436; font-weight: 600; position: relative; display: inline-block;">{quote_display}</div></div><div style="display: flex; flex-direction: column; gap: 0.75rem; align-items: center;"><div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 25px;"><span style="font-size: 1.2rem;">🧠</span><span style="color: #667eea; font-weight: 600; font-size: 0.95rem;">DeepRead 深读</span></div><div style="font-size: 0.75rem; color: #636E72; font-style: italic;">深度阅读 · 沉浸思考</div></div></div>'

        st.markdown(card_html, unsafe_allow_html=True)

        # 下载图片按钮
        img_data = create_quote_card_image(content['title'], content['author'], selected_quote)
        st.download_button(
            label="⬇️ 下载金句卡片图片",
            data=img_data,
            file_name=f"金句卡片_{content['title']}.png",
            mime="image/png",
            use_container_width=True,
            key=f"download_card_{content['title']}"
        )

    # 阅读海报生成
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

    if st.button("📊 阅读海报", key="generate_poster", use_container_width=True):
        # 获取书籍信息
        book_info = next((b for b in BOOKS_DATA if b['title'] == content['title']), None)

        # 计算阅读统计
        stats = st.session_state.reading_stats
        books_read = len(stats["total_books_read"])
        total_hours = stats["total_reading_time"] // 3600
        total_minutes = (stats["total_reading_time"] % 3600) // 60

        if total_hours > 0:
            time_display = f"{total_hours}小时{total_minutes}分钟"
        elif total_minutes > 0:
            time_display = f"{total_minutes}分钟"
        else:
            time_display = "刚刚开始"

        # 生成阅读海报HTML
        quote_display = selected_quote.replace('\n', '<br/>')
        title_display = content['title'].replace('\n', '<br/>')
        author_display = content['author'].replace('\n', '<br/>')
        tags_html = "".join([f'<span style="background: rgba(102, 126, 234, 0.1); color: #667eea; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.75rem;">{tag}</span>' for tag in book_info['tags'] if book_info])
        poster_html = f'''<div style="width: 100%; max-width: 500px; margin: 2rem auto; padding: 0; background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08); overflow: hidden; border: 1px solid rgba(102, 126, 234, 0.1);">
<div style="padding: 3rem 2rem 2rem 2rem; text-align: center; position: relative;">
    <div style="font-size: 5rem; margin-bottom: 1rem;">{book_info['emoji'] if book_info else '📖'}</div>
    <div style="font-size: 1.6rem; color: #2D3436; font-weight: 700; margin-bottom: 0.5rem;">{title_display}</div>
    <div style="font-size: 1rem; color: #636E72; font-weight: 400; margin-bottom: 1rem;">{author_display}</div>
    <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">{tags_html}</div>
</div>
<div style="padding: 2rem;">
    <div style="background: #F8F9FA; border-left: 4px solid #667eea; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
        <div style="font-size: 1.1rem; line-height: 1.8; color: #2D3436; font-style: italic;">{quote_display}</div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 1.5rem; padding: 1.5rem 0;">
        <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(102, 126, 234, 0.05); border-radius: 12px;">
            <div style="background: linear-gradient(145deg, #667eea 0%, #764ba2 100%); color: #ffffff; width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">📚</div>
            <div style="flex: 1;">
                <div style="font-size: 2rem; color: #667eea; font-weight: 700;">{books_read}</div>
                <div style="font-size: 0.85rem; color: #636E72; margin-top: 0.25rem;">已读书籍</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(118, 75, 162, 0.05); border-radius: 12px;">
            <div style="background: linear-gradient(145deg, #764ba2 0%, #667eea 100%); color: #ffffff; width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">⏱️</div>
            <div style="flex: 1;">
                <div style="font-size: 2rem; color: #764ba2; font-weight: 700;">{time_display}</div>
                <div style="font-size: 0.85rem; color: #636E72; margin-top: 0.25rem;">阅读时长</div>
            </div>
        </div>
    </div>
</div>
<div style="text-align: center; margin-top: 1.5rem;">
    <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: rgba(102, 126, 234, 0.1); border-radius: 25px; color: #667eea; font-weight: 600; font-size: 0.9rem;">
        <span>🧠</span><span>DeepRead 深读</span>
    </div>
    <div style="font-size: 0.75rem; color: #636E72; margin-top: 0.75rem; font-style: italic;">深度阅读 · 沉浸思考</div>
</div>
</div>'''
        st.markdown(poster_html, unsafe_allow_html=True)

        # 下载图片按钮
        poster_stats = {
            'books_read': books_read,
            'time_display': time_display
        }
        img_data = create_reading_poster_image(
            content['title'],
            content['author'],
            book_info['emoji'] if book_info else '📖',
            book_info['tags'] if book_info else [],
            selected_quote,
            poster_stats
        )
        st.download_button(
            label="⬇️ 下载阅读海报图片",
            data=img_data,
            file_name=f"阅读海报_{content['title']}.png",
            mime="image/png",
            use_container_width=True,
            key=f"download_poster_{content['title']}"
        )

    # 分享文案
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

    if st.button("📋 分享文案", key="copy_share", use_container_width=True):
        # 生成分享文案
        share_text = f"""📚 {content['title']} - {content['author']}

💡 核心观点：
{selected_quote}

📖 我的思考：
"""
        # 添加用户笔记
        for key, value in st.session_state.notes.items():
            if value:
                share_text += f"\n{value}\n"

        share_text += f"""
🧠 来自 DeepRead 深读
深度阅读 · 沉浸思考

👉 一起读书成长吧！
"""

        st.markdown(f"""
<div style="background: #F8F9FA; border-left: 4px solid #667eea; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
    <div style="font-size: 0.9rem; color: #636E72; margin-bottom: 0.75rem; font-weight: 600;">📋 分享文案（可复制）</div>
    <div style="font-size: 0.85rem; line-height: 1.8; color: #2D3436; white-space: pre-wrap; font-family: 'Noto Serif SC', serif; background: #ffffff; padding: 1rem; border-radius: 6px; border: 1px solid #E8EEF2;">{share_text}</div>
    <div style="font-size: 0.8rem; color: #636E72; margin-top: 0.75rem; font-style: italic;">💡 复制上方文字，分享到朋友圈、微博、小红书等平台</div>
</div>
""", unsafe_allow_html=True)
    # ============================================

    # 导出功能区
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📤 导出学习笔记</div>', unsafe_allow_html=True)

    # 导出选项
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📝 导出我的笔记", key="export_notes", use_container_width=True):
            md_content = generate_notes_only(content, st.session_state.notes)
            filename = f"{content['title']}_我的笔记_{datetime.now().strftime('%Y%m%d')}.md"

            # 提供下载
            st.download_button(
                label="⬇️ 下载笔记文件",
                data=md_content,
                file_name=filename,
                mime="text/markdown",
                key="download_notes"
            )

            st.markdown("""
<div class="export-info">
    <strong>💡 如何导入飞书？</strong><br/>
    1. 下载文件后，打开飞书文档<br/>
    2. 选择"导入" → "Markdown"<br/>
    3. 选择下载的文件即可
</div>
""", unsafe_allow_html=True)

    with col2:
        if st.button("📚 导出完整笔记", key="export_full", use_container_width=True):
            md_content = generate_markdown(content, st.session_state.notes)
            filename = f"{content['title']}_完整学习笔记_{datetime.now().strftime('%Y%m%d')}.md"

            # 提供下载
            st.download_button(
                label="⬇️ 下载完整笔记",
                data=md_content,
                file_name=filename,
                mime="text/markdown",
                key="download_full"
            )

            st.markdown("""
<div class="export-info">
    <strong>💡 完整笔记包含：</strong><br/>
    • 书籍核心内容<br/>
    • 实践步骤<br/>
    • 你的思考笔记<br/>
    • 金句摘录
</div>
""", unsafe_allow_html=True)

    # 完成阅读
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← 返回", key="reflection_back"):
            st.session_state.page_rerun += 1
            st.session_state.current_section = "practice"
            st.rerun()

    with col2:
        if st.button("📚 返回书库", key="reflection_to_library", use_container_width=True):
            st.session_state.page_rerun += 1
            st.session_state.current_book = None
            st.session_state.current_content = None
            st.session_state.current_section = "library"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar():
    """侧边栏 - 简化版（大号emoji）"""
    with st.sidebar:
        # Logo区域 - 大号emoji
        st.markdown("""
<div style="text-align: center; padding: 2.5rem 0 1.5rem 0; border-bottom: 2px solid #E8EEF2;">
    <div style="font-size: 4rem; margin-bottom: 0.75rem;">🧠</div>
    <div style="font-size: 1.5rem; font-weight: 600; color: #2D3436; margin-bottom: 0.5rem; letter-spacing: 0.05em; font-family: 'Noto Serif SC', serif;">DeepRead</div>
    <div style="font-size: 0.85rem; color: #636E72; margin-top: 0.75rem; font-style: italic; letter-spacing: 0.03em;">深度阅读 · 沉浸思考</div>
</div>
""", unsafe_allow_html=True)

        # ========== 阅读统计面板 ==========
        stats = st.session_state.reading_stats
        books_read_count = len(stats["total_books_read"])

        # 计算总阅读时长显示
        total_hours = stats["total_reading_time"] // 3600
        total_minutes = (stats["total_reading_time"] % 3600) // 60

        if total_hours > 0:
            time_display = f"{total_hours}小时{total_minutes}分钟"
        elif total_minutes > 0:
            time_display = f"{total_minutes}分钟"
        else:
            time_display = "0分钟"

        st.markdown('<div style="margin: 1.5rem 0 0.75rem 0;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #636E72; margin-bottom: 0.75rem;">📊 阅读统计</div>', unsafe_allow_html=True)

        st.markdown(f"""
<div style="background: #F0F3F5; padding: 0.875rem; border-radius: 8px; margin-bottom: 0.5rem;">
    <div style="font-size: 0.7rem; color: #636E72; margin-bottom: 0.25rem;">已读书籍</div>
    <div style="font-size: 0.9rem; font-weight: 600; color: #2D3436;">📚 {books_read_count} 本</div>
</div>

<div style="background: #F0F3F5; padding: 0.875rem; border-radius: 8px;">
    <div style="font-size: 0.7rem; color: #636E72; margin-bottom: 0.25rem;">累计阅读时长</div>
    <div style="font-size: 0.9rem; font-weight: 600; color: #2D3436;">⏱️ {time_display}</div>
</div>
""", unsafe_allow_html=True)
        # ==========================================

        # ========== 新功能：收藏书籍 ==========
        if 'favorite_books' not in st.session_state:
            st.session_state.favorite_books = []

        if st.session_state.favorite_books:
            st.markdown('<div style="margin: 1.5rem 0 0.75rem 0;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #636E72; margin-bottom: 0.75rem;">❤️ 我的收藏</div>', unsafe_allow_html=True)

            for fav_book in st.session_state.favorite_books:
                # 获取书籍信息
                book_info = next((b for b in BOOKS_DATA if b['title'] == fav_book), None)
                if book_info:
                    if st.button(f"📖 {fav_book}", key=f"sidebar_fav_{fav_book}", use_container_width=True):
                        st.session_state.page_rerun += 1
                        st.session_state.current_book = fav_book
                        st.session_state.current_content = get_book_content(fav_book)
                        st.session_state.current_section = "intro"
                        st.rerun()
        # ==========================================

        if st.session_state.current_book:
            # 当前阅读
            st.markdown(f"""
<div style="background: #F0F3F5; padding: 0.875rem; border-radius: 8px; margin: 1.25rem 0;">
    <div style="font-size: 0.7rem; color: #636E72; margin-bottom: 0.25rem;">正在阅读</div>
    <div style="font-size: 0.9rem; font-weight: 600; color: #2D3436;">{st.session_state.current_book}</div>
</div>
""", unsafe_allow_html=True)

            # ========== 新功能：阅读时长统计 ==========
            # 记录开始时间
            if 'reading_start_time' not in st.session_state:
                import time
                st.session_state.reading_start_time = time.time()

            # 计算阅读时长
            import time
            elapsed = time.time() - st.session_state.reading_start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)

            # 显示阅读时长
            time_text = f"{minutes}分{seconds}秒" if minutes > 0 else f"{seconds}秒"
            st.markdown(f"""
<div style="background: #F0F3F5; padding: 0.875rem; border-radius: 8px; margin: 1.25rem 0 0.75rem 0;">
    <div style="font-size: 0.7rem; color: #636E72; margin-bottom: 0.25rem;">本次阅读时长</div>
    <div style="font-size: 0.9rem; font-weight: 600; color: #2D3436;">⏱️ {time_text}</div>
</div>
""", unsafe_allow_html=True)
            # ==========================================

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
                        st.session_state.page_rerun += 1
                        st.session_state.current_section = key
                        st.rerun()

            # 30天实践计划入口（如果书籍有）
            if st.session_state.current_book in PRACTICE_TASKS:
                st.markdown('<div style="margin: 1.5rem 0 0.75rem 0;">', unsafe_allow_html=True)

                tracker = st.session_state.practice_tracker.get(st.session_state.current_book, {})
                if tracker:
                    # 已开始，显示进度
                    current_day = tracker.get("current_day", 1)
                    completed_days = len([d for d, completed in tracker.get("completed_days", {}).items() if completed])

                    if st.button(f"🎯 实践计划 ({completed_days}/30)", key="nav_practice_tasks", use_container_width=True):
                        st.session_state.page_rerun += 1
                        st.session_state.current_section = "practice_tasks"
                        st.rerun()
                else:
                    # 未开始，显示开始按钮
                    if st.button("🎯 30天实践计划", key="nav_practice_tasks", use_container_width=True):
                        st.session_state.page_rerun += 1
                        st.session_state.current_section = "practice_tasks"
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

            # 返回按钮
            st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
            if st.button("📚 返回书库", use_container_width=True):
                st.session_state.page_rerun += 1
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
        elif section == "practice_tasks":
            render_practice_tasks(content)
        elif section == "reflection":
            render_reflection(content)


if __name__ == "__main__":
    main()
