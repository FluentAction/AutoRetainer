# -*- coding: utf-8 -*-
"""检查未覆盖文本在词典中的状态，输出待翻译清单（分两类：词典占位 / 完全缺失）"""
import json
import re
import os

ROOT = r"D:\CodeProjects\DalamudPlugins\Demo\AutoRetainer"
DICT = os.path.join(ROOT, "tools", "zh-CN.json")

with open(DICT, encoding="utf-8-sig") as f:
    data = json.load(f)

SKIP_PATTERNS = [
    r"^\{+\}*$",             # 纯占位符
    r"^[{}:\-/\. ]+$",        # 纯符号
    r"^loading ",            # 图片名
    r"^\.png$",
    r"^About\d$",            # ID
    r"^uf[0-9a-f]{3}$",      # icon 代码
    r"^\{.*\}$",             # 仅表达式
    r"^[0-9]+$",
    r"^/[a-z]",              # 命令
]

def skip(key):
    for p in SKIP_PATTERNS:
        if re.match(p, key):
            return True
    return False

placeholder = []   # 词典中存在但 key==value（未翻译）
missing = []       # 词典中完全不存在
skip_list = []

for line in open(os.path.join(ROOT, "tools", "_ui_missing.txt"), encoding="utf-8"):
    line = line.strip()
    m = re.match(r"\[(\d+)\] (.*?)  # (.*)", line)
    if not m:
        continue
    cnt, key, files = m.group(1), m.group(2), m.group(3)
    # 还原 repr
    try:
        key = eval(key)
    except Exception:
        continue
    if skip(key):
        skip_list.append((cnt, key, files))
        continue
    if key in data:
        placeholder.append((cnt, key, data[key], files))
    else:
        missing.append((cnt, key, files))

with open(os.path.join(ROOT, "tools", "_to_translate.txt"), "w", encoding="utf-8") as f:
    f.write(f"=== 词典存在但未翻译(key==value): {len(placeholder)} 条 ===\n")
    for cnt, key, val, files in sorted(placeholder, key=lambda x: -int(x[0])):
        f.write(f"[{cnt}] {key!r}  # {files}\n")
    f.write(f"\n=== 词典完全缺失: {len(missing)} 条 ===\n")
    for cnt, key, files in sorted(missing, key=lambda x: -int(x[0])):
        f.write(f"[{cnt}] {key!r}  # {files}\n")

print(f"占位(需补): {len(placeholder)}  缺失(需新增): {len(missing)}  跳过: {len(skip_list)}")
print("清单写入 tools/_to_translate.txt")
