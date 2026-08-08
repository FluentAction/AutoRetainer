# -*- coding: utf-8 -*-
"""第二批补充翻译：GCDelivery 长帮助文本、CharacterSync 说明"""
import json
import os

ROOT = r"D:\CodeProjects\DalamudPlugins\Demo\AutoRetainer"
DICT = os.path.join(ROOT, "tools", "zh-CN.json")

EXTRA2 = {
    "\n            Select the items to be purchased automatically during Grand Company Expert Delivery operations.\n            Purchase Logic:\n            - The system will attempt to purchase the first available item from the list.\n            - Purchases will continue until the quantity of that item in your inventory reaches the specified target amount.\n            If no listed items are available for purchase, or they cannot fit into your inventory:\n            - The system will purchase Ventures instead.\n            - Venture purchases will continue until your Venture count reaches 65,000.\n            Once the Venture cap is reached and no other purchases are possible:\n            - Any excess Grand Company Seals will be discarded.\n            ":
        "\n            选择在大国防联军专家交付操作期间自动购买的物品。\n            购买逻辑:\n            - 系统将尝试从列表中购买第一个可用的物品。\n            - 购买将持续到该物品在你的背包中的数量达到指定的目标数量。\n            如果没有可购买的列表物品，或它们无法放入你的背包:\n            - 系统将改为购买冒险委托。\n            - 委托购买将持续到你的委托数量达到 65,000。\n            一旦达到委托上限且无法再进行其他购买:\n            - 多余的军票将被丢弃。\n            ",
    "\n            When Expert Delivery Continuation is enabled:\n            - The plugin will automatically spend available Grand Company Seals to purchase items from the configured Exchange List.\n            - If the Exchange List is empty, only Ventures will be purchased.\n            - Make sure that ":
        "\n            启用专家交付续传后:\n            - 插件将自动消耗可用的军票，从配置的兑换列表中购买物品。\n            - 如果兑换列表为空，将只购买冒险委托。\n            - 请确保 ",
    " is not set to ": " 未设置为 ",
    " in ": " 在 ",
    " section\n\n            After seals have been spent:\n            - Expert Delivery will resume automatically.\n            - The process will repeat until there are no eligible items left to deliver or no seals remaining.\n            ":
        " 部分中。\n\n            军票用完后:\n            - 专家交付将自动恢复。\n            - 该过程将重复，直到没有符合条件的物品可交付或没有剩余军票。\n            ",
    "\n        When enabled:\n        - Characters with teleportation enabled will automatically deliver items for expert delivery and buy items according to exchange plan, if their rank is sufficient, during multi mode.\n        ":
        "\n        启用后:\n        - 启用传送的角色将在多角色模式下自动交付专家交付物品，并根据兑换计划购买物品（如果其军衔足够）。\n        ",
    "\n            1. Create a backup by typing /justbackup, ensure it has succeeded and saved into a secure location.\n            2. Open your character list on FFXIV Lodestone.\n            ":
        "\n            1. 输入 /justbackup 创建备份，确保备份成功并保存到安全位置。\n            2. 在 FFXIV 官方角色页（Lodestone）打开你的角色列表。\n            ",
}

with open(DICT, encoding="utf-8-sig") as f:
    data = json.load(f)

added = 0
for k, v in EXTRA2.items():
    if k in data and data[k] != k:
        print(f"跳过(已有): {k[:50]!r}")
        continue
    data[k] = v
    added += 1

with open(DICT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"新增: {added}")
