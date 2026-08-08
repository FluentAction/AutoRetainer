using AutoRetainer.Internal;
using AutoRetainer.Scheduler.Tasks;
using Dalamud.Utility;
using ECommons.Automation.NeoTaskManager.Tasks;
using ECommons.ExcelServices;
using ECommons.ExcelServices.TerritoryEnumeration;
using ECommons.GameHelpers;
using ECommons.Reflection;
using FFXIVClientStructs.FFXIV.Client.Game.UI;
using FFXIVClientStructs.FFXIV.Client.UI.Agent;
using Lumina.Excel.Sheets;

namespace AutoRetainer.UI.NeoUI.AdvancedEntries.DebugSection;

internal unsafe class DebugMulti : DebugSectionBase
{
    public override void Draw()
    {
        ImGui.Checkbox("关闭画面渲染", ref P.TestRenderDisable);
        if(ImGui.CollapsingHeader("已排序数据"))
        {
            ImGuiEx.Text($"{MultiMode.GetRetainerSortedOfflineDatas(true).Where(x => !x.ExcludeRetainer).Select(x => $"{x.Name}@{x.World}").Print("\n")}");
        }
        if(ImGui.CollapsingHeader("NeoHET"))
        {
            if(ImGui.Button("入队 HET")) TaskNeoHET.Enqueue(null);
            if(ImGui.Button("入队工坊")) TaskNeoHET.TryEnterWorkshop(() => DuoLog.Error("失败"));
            ImGuiEx.Text($"""
                Can enter workshop: {Lifestream.CanMoveToWorkshop()}
                """);
        }
        if(ImGui.CollapsingHeader("任务"))
        {
            if(ImGui.Button("TestAutomoveTask")) P.TaskManager.EnqueueTask(NeoTasks.ApproachObjectViaAutomove(() => Svc.Targets.FocusTarget));
            if(ImGui.Button("TestInteractTask")) P.TaskManager.EnqueueTask(NeoTasks.InteractWithObject(() => Svc.Targets.FocusTarget));
            if(ImGui.Button("TestBoth"))
            {
                P.TaskManager.EnqueueTask(NeoTasks.ApproachObjectViaAutomove(() => Svc.Targets.FocusTarget));
                P.TaskManager.EnqueueTask(NeoTasks.InteractWithObject(() => Svc.Targets.FocusTarget));
            }
        }
        ImGui.Checkbox("不登出", ref C.DontLogout);
        ImGui.Checkbox("启用", ref MultiMode.Enabled);
        ImGuiEx.Text($"Expected: {MultiMode.ExpectedCharacter}");
        if(ImGui.Button("强制不匹配")) MultiMode.ExpectedCharacter = ("AAAAAAAA", "BBBBBBB");
        if(ImGui.Button("模拟无剩余"))
        {
            MultiMode.Relog(null, out var error, RelogReason.MultiMode);
        }
        if(ImGui.Button($"模拟自动启动"))
        {
            MultiMode.PerformAutoStart();
        }
        if(ImGui.Button("删除已加载数据"))
        {
            DalamudReflector.DeleteSharedData("AutoRetainer.WasLoaded");
        }
        ImGuiEx.Text($"Moving: {AgentMap.Instance()->IsPlayerMoving}");
        ImGuiEx.Text($"Occupied: {IsOccupied()}");
        ImGuiEx.Text($"Casting: {Player.Object?.IsCasting}");
        ImGuiEx.TextCopy($"CID: {Player.CID}");
        ImGuiEx.Text($"{Svc.Data.GetExcelSheet<Addon>()?.GetRow(115).Text.ToDalamudString().GetText()}");
        ImGuiEx.Text($"Server time: {CSFramework.GetServerTime()}");
        ImGuiEx.Text($"PC time: {DateTimeOffset.Now.ToUnixTimeSeconds()}");
        if(ImGui.CollapsingHeader("HET"))
        {
            ImGuiEx.Text($"Nearest entrance: {Utils.GetNearestEntrance(out var d)}, d={d}");
            if(ImGui.Button("进入房屋"))
            {
                TaskNeoHET.Enqueue(null);
            }
        }
        if(ImGui.CollapsingHeader("房屋领地"))
        {
            ImGuiEx.Text(ResidentalAreas.List.Select(x => GenericHelpers.GetTerritoryName(x)).Join("\n"));
            ImGuiEx.Text($"In residental area: {ResidentalAreas.List.Contains((ushort)Svc.ClientState.TerritoryType)}");
        }
        ImGuiEx.Text($"Is in sanctuary: {TerritoryInfo.Instance()->InSanctuary}");
        ImGuiEx.Text($"Is in sanctuary ExcelTerritoryHelper: {ExcelTerritoryHelper.IsSanctuary(Svc.ClientState.TerritoryType)}");
        ImGui.Checkbox($"跳过安全区检查", ref C.BypassSanctuaryCheck);
        if(Svc.ClientState.LocalPlayer != null && Svc.Targets.Target != null)
        {
            ImGuiEx.Text($"Distance to target: {Vector3.Distance(Svc.ClientState.LocalPlayer.Position, Svc.Targets.Target.Position)}");
            ImGuiEx.Text($"Target hitbox: {Svc.Targets.Target.HitboxRadius}");
            ImGuiEx.Text($"Distance to target's hitbox: {Vector3.Distance(Svc.ClientState.LocalPlayer.Position, Svc.Targets.Target.Position) - Svc.Targets.Target.HitboxRadius}");
        }
        if(ImGui.CollapsingHeader("CharaSelect"))
        {
            foreach(var x in Utils.GetCharacterNames())
            {
                ImGuiEx.Text($"{x.Name}@{x.World}");
            }
        }
    }
}
