core:add_listener(
    "Klissan_cve_hotkey_pressed",
    "ShortcutPressed",
    function(context)
        return context.string == 'script_F2'
    end,
    function(context)
        local r = find_uicomponent(core:get_ui_root())
        cv = UIComponent(r:CreateComponent("context_viewer", "ui/dev_ui/context_viewer.twui.xml"))
        cv:SetVisible(true)
    end,
    true
);