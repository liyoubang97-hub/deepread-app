# -*- coding: utf-8 -*-
"""
安全地将DeepRead项目移动到D盘
"""
import os
import sys
import shutil
from datetime import datetime

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 源路径
SOURCE = r'c:\Users\黎又榜\每日新闻推送系统\deepread'

# 目标路径
TARGET = r'D:\DeepRead'

def move_project():
    """移动项目到D盘"""

    print("=" * 70)
    print("  DeepRead 项目迁移工具")
    print("=" * 70)
    print()

    # 检查源路径是否存在
    if not os.path.exists(SOURCE):
        print(f"❌ 源路径不存在: {SOURCE}")
        return False

    print(f"源路径: {SOURCE}")
    print(f"目标路径: {TARGET}")
    print()

    # 检查目标路径是否已存在
    if os.path.exists(TARGET):
        print(f"⚠️  目标路径已存在: {TARGET}")
        print()
        choice = input("是否删除现有目标并重新复制？(y/N): ")
        if choice.lower() == 'y':
            print("正在删除现有目标...")
            shutil.rmtree(TARGET)
            print("✓ 已删除")
        else:
            print("操作已取消")
            return False

    print()
    print("开始复制...")
    print()

    try:
        # 复制整个文件夹
        shutil.copytree(SOURCE, TARGET, dirs_exist_ok=False)

        print("✓ 复制完成！")
        print()
        print("=" * 70)
        print(f"✓ 项目已成功移动到: {TARGET}")
        print("=" * 70)
        print()
        print("下一步操作:")
        print("1. 验证新位置的文件是否完整")
        print("2. 确认无误后，可以删除C盘的原始文件")
        print("3. 更新启动路径为: D:\\DeepRead")
        print()

        return True

    except Exception as e:
        print(f"❌ 复制失败: {e}")
        return False

if __name__ == "__main__":
    success = move_project()

    if success:
        # 计算大小
        source_size = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, _, filenames in os.walk(SOURCE)
            for filename in filenames
        )

        print(f"项目大小: {source_size / 1024 / 1024:.2f} MB")
        print()
        print("原始文件仍在C盘，建议确认新位置正常后再删除。")
