# -*- coding: utf-8 -*-
"""修正词典中的台版用语为大陆简体习惯，并补充缺失 key"""
import json
import os

ROOT = r"D:\CodeProjects\DalamudPlugins\Demo\AutoRetainer"
DICT = os.path.join(ROOT, "tools", "zh-CN.json")

# 台版用语 -> 大陆用语（长词优先，按顺序替换）
TERM_MAP = [
    ("远航探索", "远征探险"),
    ("登入覆盖介面", "登录覆盖界面"),
    ("用户介面", "用户界面"),
    ("介面", "界面"),
    ("设定", "设置"),
    ("贩售", "出售"),
    ("伺服器", "服务器"),
    ("模组", "模块"),
    ("萤幕", "屏幕"),
    ("网路", "网络"),
    ("汇入", "导入"),
    ("汇出", "导出"),
    ("档案", "文件"),
    ("搜寻", "搜索"),
    ("进阶", "高级"),
    ("执行绪", "线程"),
    ("数位", "数字"),
    ("频宽", "带宽"),
    ("连结", "链接"),
    ("品质", "质量"),
    ("影格", "帧"),
    ("状态列", "状态栏"),
    ("视窗", "窗口"),
    ("资讯", "信息"),
    ("工具列", "工具栏"),
    ("除错", "调试"),
    ("回覆", "回复"),
    ("物件", "对象"),
    ("类別", "类别"),
    ("登入", "登录"),
    ("启用", "启用"),
    ("停用", "禁用"),
]

# 补充缺失 key
EXTRA = {
    "Inventory Management": "库存管理",
    "Inventory Cleanup": "库存清理",
    "Protection List": "保护列表",
    "Fast Addition and Removal": "快速添加与移除",
    "Character Configuration": "角色配置",
    "Grand Company Delivery": "军需交付",
    "Exchange Lists": "兑换列表",
    "Experiments": "实验",
    "Notifications": "通知",
    "Character Sync": "角色同步",
    "Account Whitelist": "账号白名单",
    "Expert": "专家",
    "Misc": "杂项",
    "General Settings": "常规设置",
    "Entrust Manager": "委托管理",
    "Search characters...": "搜索角色...",
    "Selected {}": "已选择 {}",
    "{} selected": "已选择 {}",
    "Selected": "已选择",
}

with open(DICT, encoding="utf-8-sig") as f:
    data = json.load(f)

fixed = 0
for k in list(data.keys()):
    v = data[k]
    if k != v and any("\u4e00" <= c <= "\u9fff" for c in v):
        nv = v
        for a, b in TERM_MAP:
            nv = nv.replace(a, b)
        if nv != v:
            data[k] = nv
            fixed += 1

added = 0
for k, v in EXTRA.items():
    if k not in data or data[k] == k:
        data[k] = v
        added += 1

with open(DICT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"用语修正: {fixed}, 补充 key: {added}, 总条目: {len(data)}")
