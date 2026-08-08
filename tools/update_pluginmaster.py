# -*- coding: utf-8 -*-
"""
更新 exloser123/DalamudPlugins 仓库中的 pluginmaster.json（AutoRetainer 条目）。
CI 调用：python tools/update_pluginmaster.py <pm_repo_path> <version> <download_url> <changelog>
"""
import json
import os
import sys
import time

def main():
    if len(sys.argv) < 5:
        print("用法: update_pluginmaster.py <pm_repo_path> <version> <download_url> <changelog>")
        sys.exit(1)
    pm_dir, version, download_url, changelog = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    pm = os.path.join(pm_dir, "pluginmaster.json")

    with open(pm, encoding="utf-8-sig") as f:
        data = json.load(f)

    entry = None
    for e in data:
        if e.get("InternalName") == "AutoRetainer":
            entry = e
            break
    if entry is None:
        entry = {
            "Author": "kawaii, NightmareXIV（汉化: exloser123）",
            "Name": "AutoRetainer (自动雇员)",
            "Punchline": "躺在床上就能收取并指派你的雇员冒险委托。",
            "Description": "躺在床上就能收取并指派你的雇员冒险委托。\n\n主要功能：\n\t- 一键指派/重新指派雇员冒险委托，自动处理繁琐的确认弹窗\n\t- 一键部署远征探险（飞空艇/潜水艇）\n\t- 创建出售列表，自动清理垃圾物品\n\t- 创建存放列表，将贵重物品存入雇员以节省背包空间",
            "Tags": ["Retainer", "Venture", "Submarine", "Chinese"],
            "InternalName": "AutoRetainer",
            "RepoUrl": "https://github.com/PunishXIV/AutoRetainer",
            "DownloadCount": 0,
            "ApplicableVersion": "any",
            "DalamudApiLevel": "15",
            "IconUrl": "https://gh.atmoomen.top/https://puni.sh/api/plugins/icon/24",
        }
        data.append(entry)

    entry["AssemblyVersion"] = version
    entry["LastUpdate"] = int(time.time())
    entry["DownloadLinkInstall"] = download_url
    entry["DownloadLinkUpdate"] = download_url
    entry["DownloadLinkTesting"] = download_url
    entry["Changelog"] = changelog

    with open(pm, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"pluginmaster.json 已更新: AutoRetainer {version}")


if __name__ == "__main__":
    main()
