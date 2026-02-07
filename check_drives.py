# -*- coding: utf-8 -*-
import os
import sys
import shutil

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_drive_space(drive):
    """获取驱动器空间信息"""
    try:
        usage = shutil.disk_usage(drive)
        return {
            "total": usage.total / (1024**3),  # GB
            "used": usage.used / (1024**3),    # GB
            "free": usage.free / (1024**3)     # GB
        }
    except:
        return None

print("=" * 70)
print("  磁盘空间检查")
print("=" * 70)
print()

drives = ["C:\\", "D:\\", "E:\\"]
for drive in drives:
    space = get_drive_space(drive)
    if space:
        print(f"{drive}盘:")
        print(f"  总容量: {space['total']:.2f} GB")
        print(f"  已用:   {space['used']:.2f} GB")
        print(f"  剩余:   {space['free']:.2f} GB")
        print()

print("=" * 70)
