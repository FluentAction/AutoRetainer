# -*- coding: utf-8 -*-
"""将 zh-TW.json 词典的繁体中文值转换为简体中文，覆盖写入 zh-CN.json（保留 key 不变，保留 key==value 占位）"""
import json
import os
from opencc import OpenCC

ROOT = r"D:\CodeProjects\DalamudPlugins\Demo\AutoRetainer"
DICT = os.path.join(ROOT, "tools", "zh-CN.json")

cc = OpenCC("t2s")

with open(DICT, encoding="utf-8-sig") as f:
    data = json.load(f)

new = {}
converted = 0
for k, v in data.items():
    if k != v and any("\u4e00" <= c <= "\u9fff" for c in v):
        v2 = cc.convert(v)
        if v2 != v:
            converted += 1
        new[k] = v2
    else:
        new[k] = v

with open(DICT, "w", encoding="utf-8") as f:
    json.dump(new, f, ensure_ascii=False, indent=2)

print(f"总条目: {len(data)}, 发生简繁转换的条目: {converted}")
# 抽查
for k in ["General", "RetainerSense", "Enable", "Retainers", "Unknown", "Abort {0} tasks"]:
    print(f"  {k!r} => {new.get(k)!r}")
