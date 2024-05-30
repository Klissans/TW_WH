---@class battle_ui
local battle_ui = {
    _name = nil,
    _uic = nil,
    _shortcuts_tele = {
        script_F2 = "button_attack_brush",
        script_F3 = "button_default_brush",
        script_F4 = "button_defend_brush",
    }
}


function battle_ui:init()

    local parent_uic = find_uicomponent(core:get_ui_root(), "hud_battle", "battle_orders", "battle_orders_pane", "orders_parent", "reinforcement_hud_parent", "spawn_toggle_parent", "button_reinforcements", "parent_reinforcement_purchase");
    self._uic = parent_uic;
    --self._uic:SetDockOffset(0,-400);
    -- --core:get_ui_root():Adopt(parent_uic:Address());
    self._uic_el = find_uicomponent(self._uic, "hud_battle_reinforcement_purchase", "elements_list");
    -- self._uic_rutl = find_uicomponent(self._uic, "reinforcement_purchase", "reinforcement_unit_type_list");

    --self._uic:SetDockingPoint(0);
    --self._uic:SetDockOffset(0,0);

    --find_uicomponent(self._uic_el, "header"):SetInteractive(false);
    --find_uicomponent(self._uic_el, "footer"):SetInteractive(false);
    --self._uic_el:SetMoveable(true);

    self:init_listeners();
    self:init_listener_tele();

    local mp_team_list = find_uicomponent(core:get_ui_root(), "mp_team_list");
    if mp_team_list then
        mp_team_list:Destroy()
    end

    local menu_bar = find_uicomponent(core:get_ui_root(), "menu_bar");
    menu_bar:CreateComponent("mod_team_list", "ui/mod/mod_team_list.twui.xml");
    find_uicomponent(menu_bar, "mod_team_list"):SetInteractive(false);
    find_uicomponent(menu_bar, "buttongroup", "button_player_list"):SetVisible(true);

    if common.get_context_value("CcoBattleRoot", 'BattleRoot', "IsDomination") then
        find_uicomponent(self._uic_el, "footer"):CreateComponent("reinf_panel_supplies", "ui/mod/reinf_panel_supplies.twui.xml")
    end
    -- uic_ping_marker:SetContextObject(cco("CcoBattleRoot", self.unit:unique_ui_id()));


    --     local battle = empire_battle:new();
    --     if battle:is_replay() then
    --         parent_uic = find_uicomponent(core:get_ui_root(), "hud_battle", "battle_orders", "battle_orders_pane", "orders_parent", "reinforcement_hud_parent", "spawn_toggle_parent", "button_reinforcements", "parent_reinforcement_purchase");
    --         find_uicomponent(core:get_ui_root(), "hud_battle", "battle_orders"):SetVisible(true)
    --         local tm = core:get_static_object("timer_manager")
    --         tm:real_callback(
    --             function()
    --                 find_uicomponent(core:get_ui_root(), "hud_battle", "battle_orders", "battle_orders_pane", "orders_parent", "reinforcement_hud_parent", "spawn_toggle_parent", "button_reinforcements"):SimulateLClick()
    --             end,
    --             500, "replay_reinf_panel")
    --     end

end

function battle_ui:init_listener_tele()

    out('Entering init')
    if not bm:is_replay() then
        out('not a replay battle')
        return
    end

    local do_dumps_file = "_enable_telestration_hotkeys.mpui"
    out('Checking if enabling dumps file exists')
    if not Klissan_H:is_file_exist(do_dumps_file) then
        out(do_dumps_file .. " doesn't exist")
        return
    end
    core:add_listener(
            "mpui_telestration_hotkey_pressed",
            "ShortcutPressed",
            function(context)
                return self._shortcuts_tele[context.string]
            end,
            function(context)
                local brush_button = find_uicomponent(core:get_ui_root(), "hud_battle", "under_menu_bar_list_parent", "telestration_controls", self._shortcuts_tele[context.string]);
                brush_button:SimulateLClick();
            end,
            true
    );
end

function battle_ui:init_listeners()

    --core:add_listener(
    --	"reinforcement_panel_moved",
    --	"ComponentMoved",
    --	function(context)
    --		return context.string == reinforcement_panel._uic_el:Id()
    --	end,
    --	function(context)
    --		local uic = UIComponent(context.component)
    --		local w,h = reinforcement_panel._uic_rutl:Dimensions()
    --        local tx, ty = uic:Position()
    --        if self._uic_rutl:Visible() then  ty = ty - h end
    --
    --        local function f() reinforcement_panel._uic:MoveTo(tx, ty) end
    --		local tm = core:get_static_object("timer_manager")
    --        local timeout = 5
    --		tm:real_callback(f, timeout, "refresh_reinf_panel")
    --
    --	end,
    --	true
    --)

    core:add_listener(
            "telestration_controls_clicked",
            "ComponentLClickUp",
            function(context)
                return context.string == "button_telestration"
            end,
            function(context)
                local button_telestration = UIComponent(context.component);
                if button_telestration:Visible() then
                    local bg = find_uicomponent(core:get_ui_root(), "menu_bar", "buttongroup");
                    local mbx, mby = bg:Position();
                    local mbw, mbh = bg:Dimensions();
                    local telestration_controls = find_uicomponent(core:get_ui_root(), "hud_battle", "under_menu_bar_list_parent", "telestration_controls");
                    telestration_controls:MoveTo(mbx + mbw + 90, 0);
                end
            end,
            true
    )

end

local function init_save_replay_listener()

    core:add_listener(
            "mod_save_replay_button_clicked",
            "ComponentLClickUp",
            function(context)
                return context.string == "button_save_replay"
            end,
            function(context)
                local function f()
                    local c = cco("CcoBattleRoot", "BattleRoot");
                    local replay_name = os.date("%Y-%m-%d %H-%M ") .. c:Call("AllianceList.JoinString(ArmyList.JoinString(PlayerName + '(' +ArmyName + ')', '&'), ' vs ') ");
                    local input_field = find_uicomponent(core:get_ui_root(), "requester", "input_name");
                    input_field:SetText(replay_name, '_todo_db_loc_key_');
                end
                local tm = core:get_static_object("timer_manager")
                local timeout = 250
                tm:real_callback(f, timeout, "set_replay_name")
            end,
            true
    )
end

if core:is_battle() then
    bm:register_phase_change_callback("Deployment", function()
        battle_ui:init()
    end)
    bm:register_phase_change_callback("Complete", init_save_replay_listener)
end