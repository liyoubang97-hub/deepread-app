# -*- coding: utf-8 -*-
import sys
import io

# Windows编码修复
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import book data
import demo_data_v2

print("=" * 50)
print("  DeepRead V3.9 - 内容库测试")
print("=" * 50)
print()

# Get all books
all_books = list(demo_data_v2.BOOK_CONTENTS.keys())

print(f"总书籍数: {len(all_books)}")
print()

print("所有书籍:")
for i, book_name in enumerate(all_books, 1):
    book = demo_data_v2.BOOK_CONTENTS[book_name]
    print(f"{i}. {book_name} - {book.get('author', '未知作者')}")
    print(f"   核心洞察数: {len(book.get('core_thinking', {}).get('insights', []))}")
    print(f"   实践步骤数: {len(book.get('practice', {}).get('steps', []))}")
    print(f"   反思问题数: {len(book.get('reflection', {}).get('questions', []))}")
    print(f"   金句数: {len(book.get('quotes', []))}")
    print()

print("=" * 50)
print("✅ 所有书籍数据加载成功！")
print("=" * 50)
