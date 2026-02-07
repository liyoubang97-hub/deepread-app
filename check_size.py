# -*- coding: utf-8 -*-
import os
import sys

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_folder_size(path):
    """计算文件夹大小"""
    total_size = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
                file_count += 1
            except:
                pass
    return total_size, file_count

# 检查deepread文件夹
deepread_path = r'c:\Users\黎又榜\每日新闻推送系统\deepread'
size, files = get_folder_size(deepread_path)

print("=" * 60)
print("  DeepRead 项目空间占用")
print("=" * 60)
print()
print(f"文件数量: {files}")
print(f"总大小: {size / 1024 / 1024:.2f} MB")
print(f"        {size / 1024:.2f} KB")
print()

# 检查Python缓存
cache_size = 0
cache_files = 0
for dirpath, dirnames, filenames in os.walk(deepread_path):
    for dirname in dirnames:
        if dirname == '__pycache__':
            cache_path = os.path.join(dirpath, dirname)
            cs, cf = get_folder_size(cache_path)
            cache_size += cs
            cache_files += cf

if cache_files > 0:
    print(f"Python缓存文件: {cache_files} 个")
    print(f"缓存大小: {cache_size / 1024 / 1024:.2f} MB")
    print()

print("=" * 60)
