# -*- coding: utf-8 -*-
"""分析 zh-CN.json 词典与官方源码字符串的匹配情况"""
import json
import os
import re
import sys

ROOT = r"D:\CodeProjects\DalamudPlugins\Demo\AutoRetainer"
DICT = os.path.join(ROOT, "tools", "zh-CN.json")

with open(DICT, encoding="utf-8-sig") as f:
    data = json.load(f)

# 只取有实际翻译的条目（key != value 且 value 含中文）
translated = {k: v for k, v in data.items()
              if k != v and any("\u4e00" <= c <= "\u9fff" for c in v)}
untranslated = {k: v for k, v in data.items() if k not in translated}
print(f"词典总条目: {len(data)}, 有效翻译: {len(translated)}, 未翻译(key==value): {len(untranslated)}")

# 收集源码中的所有字符串字面量（含插值字符串的文本部分）
src_dir = os.path.join(ROOT, "AutoRetainer")
files = []
for root, dirs, fns in os.walk(src_dir):
    dirs[:] = [d for d in dirs if d not in (".git", "bin", "obj")]
    for fn in fns:
        if fn.endswith(".cs"):
            files.append(os.path.join(root, fn))
print(f"源码 .cs 文件数: {len(files)}")

# 字符串字面量提取: "..." 或 $"..." 里的文本片段
pat = re.compile(r'([\$@]*)("(?:\\.|[^"\\])*")')

literal_counts = {}  # 字面量 -> 出现次数
for fp in files:
    with open(fp, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    # 去掉注释（简化处理：行注释和块注释）
    txt = re.sub(r"//[^\n]*", "", txt)
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    for m in pat.finditer(txt):
        prefix, lit = m.group(1), m.group(2)
        content = re.sub(r"\\(.)", r"\1", lit[1:-1])
        if prefix.startswith("$"):
            content = re.sub(r"\{[^}]*\}", "{0}", content)
        if content.strip():
            literal_counts[content] = literal_counts.get(content, 0) + 1

print(f"源码字符串字面量(去重): {len(literal_counts)}")

# 匹配分析
matched = {}
unmatched = {}
for k in translated:
    if k in literal_counts:
        matched[k] = literal_counts[k]
    else:
        unmatched[k] = None

print(f"词典有效翻译中能在源码找到的: {len(matched)}")
print(f"词典有效翻译中源码找不到的(可能是旧版本文本): {len(unmatched)}")

# 反查: 源码中所有字面量里, 哪些不在词典翻译中(可能漏翻)
covered = set(matched.keys())
not_covered = []
for lit, cnt in literal_counts.items():
    if lit not in covered:
        not_covered.append((lit, cnt))
print(f"源码字面量中未被词典覆盖的: {len(not_covered)}")

# 示例: 未被覆盖的、像 UI 文本的（大写开头、含空格、长度>3）
candidates = [(l, c) for l, c in not_covered if len(l) > 3 and l[0].isupper() and " " in l]
candidates.sort(key=lambda x: -x[1])
print(f"其中疑似 UI 文本(大写开头含空格): {len(candidates)}")
for l, c in candidates[:30]:
    print(f"  [{c}] {l!r}")

with open(os.path.join(ROOT, "tools", "_unmatched_report.txt"), "w", encoding="utf-8") as f:
    f.write("=== 词典有翻译但源码未找到(可能是旧版本) ===\n")
    for k in sorted(unmatched.keys()):
        f.write(f"{k!r} => {data[k]!r}\n")
    f.write("\n=== 源码疑似UI文本未被词典覆盖 ===\n")
    for l, c in candidates:
        f.write(f"[{c}] {l!r}\n")
print("报告已写入 tools/_unmatched_report.txt")
