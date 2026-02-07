# -*- coding: utf-8 -*-
"""
批量修复demo_data_v2.py中的中文引号转义问题
"""
import re

# 读取文件
with open('demo_data_v2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 统计修复次数
fix_count = 0

# 修复模式：在双引号字符串中，将 "x" 替换为 \"x\"
# 这个正则会找到形如 "...\"..." 的模式并正确转义

# 方法：逐行处理，找到在字符串中的未转义中文引号
lines = content.split('\n')
fixed_lines = []

in_string = False
string_char = None

for i, line in enumerate(lines, 1):
    fixed_line = []
    j = 0
    while j < len(line):
        char = line[j]

        # 检查是否进入/退出字符串
        if char in ['"', "'"] and (j == 0 or line[j-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
                fixed_line.append(char)
            elif char == string_char:
                in_string = False
                string_char = None
                fixed_line.append(char)
            else:
                fixed_line.append(char)
        elif in_string and string_char == '"' and char == '"':
            # 在双引号字符串中遇到了中文引号，需要转义
            # 检查前后是否是中文或字母
            if j > 0 and j < len(line) - 1:
                prev_char = line[j-1]
                next_char = line[j+1] if j+1 < len(line) else ''
                # 如果前后都是非空格字符，这可能是中文引号
                if prev_char not in [' ', '\t', '(', '[', '{', ':'] and next_char not in [' ', '\t', ',', ')', ']', '}', ':', '?', '！', '。']:
                    fixed_line.append('\\"')
                    fix_count += 1
                else:
                    fixed_line.append(char)
            else:
                fixed_line.append(char)
        else:
            fixed_line.append(char)

        j += 1

    fixed_lines.append(''.join(fixed_line))

# 写回文件
fixed_content = '\n'.join(fixed_lines)
with open('demo_data_v2.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"修复完成！共修复了 {fix_count} 处引号问题")
