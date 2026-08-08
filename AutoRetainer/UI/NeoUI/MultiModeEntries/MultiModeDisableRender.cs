using System;
using System.Collections.Generic;
using System.Text;

namespace AutoRetainer.UI.NeoUI.MultiModeEntries;

public class MultiModeDisableRender : NeoUIEntry
{
    public override string Path => "多角色模式/关闭画面渲染";

    public override NuiBuilder Builder => new NuiBuilder()
        .Section("关闭画面渲染")
        .Checkbox("多角色模式下关闭画面渲染", () => ref C.MultiDisableRender, "多角色模式下不再渲染游戏世界，以降低资源占用")
        .Checkbox("只在夜间模式启用", () => ref C.MultiDisableRenderNightModeOnly)
        .Checkbox("仅在游戏窗口非作用中时", () => ref C.MultiDisableRenderOnlyInactive);
}
