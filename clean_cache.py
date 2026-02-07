# -*- coding: utf-8 -*-
"""
清理Python缓存和临时文件
释放磁盘空间
"""
import os
import sys
import shutil

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def clean_pycache(path):
    """清理__pycache__文件夹"""
    count = 0
    size = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            if dirname == '__pycache__':
                cache_path = os.path.join(dirpath, dirname)
                try:
                    # 计算大小
                    folder_size = sum(
                        os.path.getsize(os.path.join(dirpath, f))
                        for dirpath, _, filenames in os.walk(cache_path)
                        for f in filenames
                    )
                    # 删除文件夹
                    shutil.rmtree(cache_path)
                    count += 1
                    size += folder_size
                except Exception as e:
                    print(f"删除失败 {cache_path}: {e}")

    return count, size

def clean_pyc_files(path):
    """清理.pyc文件"""
    count = 0
    size = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.pyc'):
                file_path = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    count += 1
                    size += file_size
                except Exception as e:
                    print(f"删除失败 {file_path}: {e}")

    return count, size

if __name__ == "__main__":
    print("=" * 60)
    print("  DeepRead 缓存清理工具")
    print("=" * 60)
    print()

    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("正在清理...")
    print()

    # 清理__pycache__
    cache_count, cache_size = clean_pycache(current_dir)
    if cache_count > 0:
        print(f"✓ 删除了 {cache_count} 个 __pycache__ 文件夹")
        print(f"  释放空间: {cache_size / 1024:.2f} KB")
    else:
        print("○ 没有找到 __pycache__ 文件夹")

    print()

    # 清理.pyc文件
    pyc_count, pyc_size = clean_pyc_files(current_dir)
    if pyc_count > 0:
        print(f"✓ 删除了 {pyc_count} 个 .pyc 文件")
        print(f"  释放空间: {pyc_size / 1024:.2f} KB")
    else:
        print("○ 没有找到 .pyc 文件")

    print()
    print("=" * 60)

    total_size = cache_size + pyc_size
    if cache_count > 0 or pyc_count > 0:
        print(f"✓ 清理完成！共释放 {total_size / 1024:.2f} KB")
    else:
        print("✓ 已经很干净了，无需清理")

    print("=" * 60)
