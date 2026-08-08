namespace AutoRetainer.UI.NeoUI.Experiments;
public class Notifications : ExperimentUIEntry
{
    public override void Draw()
    {
        ImGui.Checkbox($"当有雇员完成探险时显示复盖层通知", ref C.NotifyEnableOverlay);
        ImGui.Checkbox($"在副本或战斗中不显示复盖层", ref C.NotifyCombatDutyNoDisplay);
        ImGui.Checkbox($"包含其他角色", ref C.NotifyIncludeAllChara);
        ImGui.Checkbox($"忽略未在多重模式中启用的其他角色", ref C.NotifyIgnoreNoMultiMode);
        ImGui.Checkbox($"在游戏聊天栏显示通知", ref C.NotifyDisplayInChatX);
        ImGuiEx.Text($"当游戏处于非活动状态时: (需要安装并启用 NotificationMaster 外挂程式)");
        ImGui.Checkbox($"当雇员可用时发送桌面通知", ref C.NotifyDeskopToast);
        ImGui.Checkbox($"闪烁工作列", ref C.NotifyFlashTaskbar);
        ImGui.Checkbox($"若 AutoRetainer 已启用或多重模式运行中则不通知", ref C.NotifyNoToastWhenRunning);
    }
}
