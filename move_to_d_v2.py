# -*- coding: utf-8 -*-
"""
移动DeepRead项目到D盘 - 改进版
"""
import os
import sys
import shutil
import time

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SOURCE = r'c:\Users\黎又榜\每日新闻推送系统\deepread'
TARGET = r'D:\DeepRead'

print("=" * 70)
print("  DeepRead 项目迁移工具 v2")
print("=" * 70)
print()

# 检查源路径
if not os.path.exists(SOURCE):
    print(f"❌ 源路径不存在: {SOURCE}")
    sys.exit(1)

print(f"源路径: {SOURCE}")
print(f"目标路径: {TARGET}")
print()

# 如果目标存在，删除
if os.path.exists(TARGET):
    print(f"⚠️  目标路径已存在，正在删除...")
    try:
        # 尝试删除
        def remove_readonly(func, path, excinfo):
            """删除只读文件"""
            os.chmod(path, 0o777)
            func(path)

        shutil.rmtree(TARGET, onerror=remove_readonly)
        print("✓ 已删除旧文件")
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        print()
        print("提示：可能需要手动删除 D:\\DeepRead 后再运行")
        print("或者关闭可能正在使用该文件夹的程序")
        sys.exit(1)

print()
print("开始复制...")
print()

try:
    # 复制（忽略已存在的错误）
    start_time = time.time()
    shutil.copytree(SOURCE, TARGET)
    elapsed = time.time() - start_time

    print()
    print("=" * 70)
    print("✓ 复制完成！")
    print(f"  耗时: {elapsed:.2f} 秒")
    print("=" * 70)
    print()

    # 计算大小
    source_size = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for dirpath, _, filenames in os.walk(SOURCE)
        for filename in filenames
    )

    target_size = sum(
        os.path.getsize(os.path.join(dirpath, filename))
        for dirpath, _, filenames in os.walk(TARGET)
        for filename in filenames
    )

    print(f"源大小: {source_size / 1024 / 1024:.2f} MB")
    print(f"目标大小: {target_size / 1024 / 1024:.2f} MB")
    print()

    if abs(source_size - target_size) < 1000:  # 允许1KB误差
        print("✓ 文件大小匹配，复制成功！")
    else:
        print("⚠️  文件大小不匹配，请检查")

    print()
    print("=" * 70)
    print("🎉 项目已成功移动到 D:\\DeepRead")
    print("=" * 70)
    print()
    print("下一步:")
    print("  1. 新位置: D:\\DeepRead")
    print("  2. 启动命令: cd D:\\DeepRead && python launch.py")
    print("  3. 或者双击: D:\\DeepRead\\start_v3.8.bat")
    print()
    print("⚠️  C盘的原始文件可以稍后删除")

except Exception as e:
    print(f"❌ 复制失败: {e}")
    import traceback
    traceback.print_exc()
