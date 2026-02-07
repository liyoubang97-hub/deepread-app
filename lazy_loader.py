# -*- coding: utf-8 -*-
"""
懒加载器 - 按需加载书籍内容
优化内存占用和启动速度
"""

_book_cache = {}

def get_book_content(title):
    """
    按需获取书籍内容
    第一次调用时加载，之后从缓存中获取
    """
    global _book_cache

    # 如果已缓存，直接返回
    if title in _book_cache:
        return _book_cache[title]

    # 否则加载并缓存
    from demo_data_v2 import BOOK_CONTENTS
    content = BOOK_CONTENTS.get(title)
    if content:
        _book_cache[title] = content

    return content


def clear_cache():
    """清空缓存"""
    global _book_cache
    _book_cache = {}


def get_cache_info():
    """获取缓存信息"""
    global _book_cache
    return {
        "cached_books": len(_book_cache),
        "book_names": list(_book_cache.keys())
    }
