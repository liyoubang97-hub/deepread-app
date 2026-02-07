# -*- coding: utf-8 -*-
"""
DeepRead V3.7 启动脚本
"""
import subprocess
import sys
import os

# Windows编码修复
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 50)
print("  DeepRead V3.8 - Export Features")
print("=" * 50)
print()
print("Starting...")
print()

# 启动Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "app_v3.8.py"])
