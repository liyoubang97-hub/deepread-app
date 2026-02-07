# -*- coding: utf-8 -*-
"""
移动到D盘的Projects文件夹
"""
import os
import sys
import shutil
import subprocess
import time

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SOURCE = r'c:\Users\黎又榜\每日新闻推送系统\deepread'
TARGET = r'D:\Projects\DeepRead'

print("=" * 70)
print("  DeepRead 项目迁移工具 v3")
print("=" * 70)
print()

# 检查源路径
if not os.path.exists(SOURCE):
    print(f"❌ 源路径不存在: {SOURCE}")
    sys.exit(1)

print(f"源路径: {SOURCE}")
print(f"目标路径: {TARGET}")
print()

# 创建Projects目录（如果不存在）
target_parent = os.path.dirname(TARGET)
if not os.path.exists(target_parent):
    print(f"创建目录: {target_parent}")
    os.makedirs(target_parent)

# 如果目标存在，删除
if os.path.exists(TARGET):
    print(f"⚠️  目标路径已存在，正在删除...")
    try:
        def remove_readonly(func, path, excinfo):
            os.chmod(path, 0o777)
            func(path)
        shutil.rmtree(TARGET, onerror=remove_readonly)
        print("✓ 已删除旧文件")
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        print("尝试使用robocopy...")
        # 使用robocopy
        result = subprocess.run([
            'robocopy', SOURCE, target_parent,
            'deepread', '/E', '/R:0', '/W:0', '/NFL', '/NDL', '/NJH', '/NJS'
        ], capture_output=True)
        if result.returncode in [0, 1, 7]:  # robocopy成功代码
            print("✓ Robocopy复制成功")
            print(f"✓ 项目已移动到: {TARGET}")
            sys.exit(0)
        else:
            sys.exit(1)

print()
print("开始复制...")
print()

try:
    start_time = time.time()
    shutil.copytree(SOURCE, TARGET)
    elapsed = time.time() - start_time

    print()
    print("=" * 70)
    print("✓ 复制完成！")
    print(f"  耗时: {elapsed:.2f} 秒")
    print("=" * 70)
    print()

    # 验证大小
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

    if abs(source_size - target_size) < 1000:
        print("✓ 文件大小匹配，复制成功！")
    else:
        print("⚠️  文件大小不匹配，请检查")

    print()
    print("=" * 70)
    print("🎉 项目已成功移动到 D:\\Projects\\DeepRead")
    print("=" * 70)
    print()
    print("下一步:")
    print("  1. 新位置: D:\\Projects\\DeepRead")
    print("  2. 启动命令:")
    print("     cd D:\\Projects\\DeepRead")
    print("     python launch.py")
    print("  3. 或者创建快捷方式")

except Exception as e:
    print(f"❌ 复制失败: {e}")
    import traceback
    traceback.print_exc()
