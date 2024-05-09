MGSWT.ui_listener_names = {
    travel_panel_opened = Klissan_CH:get_listener_name('malakai_travel_panel_opened'),
    travel_panel_closed = Klissan_CH:get_listener_name('malakai_travel_panel_closed')
}

MGSWT.ui_callback_names = {
    set_ritual_cost = Klissan_CH:get_callback_name('malakai_set_ritual_cost')
}


function MGSWT:edit_travel_button()
    if cm:get_local_faction():name() ~= MGSWT.faction:name() then
        return
    end
    local travel_button = find_uicomponent(core:get_ui_root(), 'hud_campaign', 'faction_buttons_docker', 'button_group_management', 'button_changing_of_the_ways')
    local icon_path = 'ui/common ui/unit_category_icons/klissan_grungni_icon.png'
    travel_button:SetImagePath(icon_path)
    local travel_button_tooltip_key = 'land_units_onscreen_name_wh3_dlc25_dwf_veh_thunderbarge_grungni' -- 'unit_description_short_texts_text_wh3_dlc25_unit_short_text_dwf_veh_thunderbarge'
    travel_button:SetTooltipText(common.get_localised_string(travel_button_tooltip_key), travel_button_tooltip_key, true)
end


function MGSWT:set_ritual_cost()
    local ui_perform_cost = find_uicomponent(core:get_ui_root(), 'tzeentch_changing_of_ways', 'manipulation_info', 'button_perform', 'duration_cost_holder', 'dy_cost')
    local ui_perform_button = find_uicomponent(core:get_ui_root(), 'tzeentch_changing_of_ways', 'manipulation_info', 'button_perform')
    if not self:can_perform_ritual() then
        ui_perform_cost:SetText('0', '0')
        ui_perform_button:SetState('inactive')
        return
    end

    -- has state changed
    local selected_ritual_key = self:get_targeting_ritual_key()
    local target_type, target_key = self:get_targeting_target()
    local cr = self.rituals.current_ritual
    if selected_ritual_key == cr.key and target_type == cr.target_type and target_key == cr.target_key then
        return
    end
    self:debug('AFTER HAS RITUAL CHANGED CHECK')
    cr.key = selected_ritual_key
    cr.target_type = target_type
    cr.target_key = target_key

    --everything is good do our part
    local cost = self:get_ritual_cost()
    local cost_str = tostring(cost)
    self.rituals.current_ritual.currency_type = 'gold'
    self.rituals.current_ritual.value = cost

    -- HAS TO BE DONE THIS WAY OTHERWISE SOMETIME IT DOESN"T SET
    core:get_tm():real_callback(function () ui_perform_cost:SetText(cost_str, cost_str) end, 50, Klissan_CH:get_callback_name('malakai_set_fkn_cost_price'))

    -- do we have enough resources?
    if cost > self.faction:treasury() then
        ui_perform_button:SetState('inactive')
        return
    end
    ui_perform_button:SetState('active')
end

function MGSWT:can_perform_ritual()
    return self:is_target_context_exists() -- todo and target correct
end


function MGSWT:listen_to_malakai_travel_panel_opened()
    core:add_listener(
        MGSWT.ui_listener_names.travel_panel_opened,
        "PanelOpenedCampaign",
        function(context)
            return cm:get_local_faction():name() == MGSWT.faction:name() and context.string == "tzeentch_changing_of_ways"
        end,
        function()
            local travel_panel = find_uicomponent(core:get_ui_root(), 'tzeentch_changing_of_ways', 'tx_header')
            local travel_panel_text_key = 'land_units_onscreen_name_wh3_dlc25_dwf_veh_thunderbarge_grungni'
            travel_panel:SetText(common.get_localised_string(travel_panel_text_key), travel_panel_text_key)

            local travel_panel_button = find_uicomponent(core:get_ui_root(), 'tzeentch_changing_of_ways', 'manipulation_info', 'button_perform', 'button_txt')
            local travel_panel_button_text_key = 'rituals_description_wh3_dlc25_emp_ritual_elspeth_teleport'
            travel_panel_button:SetText(common.get_localised_string(travel_panel_button_text_key), travel_panel_button_text_key)

            local manipulation_list = find_uicomponent(core:get_ui_root(), 'tzeentch_changing_of_ways', 'manipulation_list')
            local travel_option = find_uicomponent(UIComponent(manipulation_list:Find(2)), 'entry', 'button_txt')
            local travel_option_text_key = travel_panel_button_text_key
            travel_option:SetText(common.get_localised_string(travel_option_text_key), travel_option_text_key)

            -- start cost setter
            core:get_tm():repeat_real_callback(function() MGSWT:set_ritual_cost() end, 100, MGSWT.ui_callback_names.set_ritual_cost)
        end,
        true
    )
end

function MGSWT:listen_to_malakai_travel_panel_closed()
    core:add_listener(
        MGSWT.ui_listener_names.travel_panel_closed,
        "PanelClosedCampaign",
        function(context)
            return cm:get_local_faction():name() == MGSWT.faction:name() and context.string == "tzeentch_changing_of_ways"
        end,
        function()
            -- remove cost setter
            core:get_tm():remove_real_callback(MGSWT.ui_callback_names.set_ritual_cost)
        end,
        true
    )
end


cm:add_ui_created_callback(function()
    cm:add_post_first_tick_callback(function()
        MGSWT:edit_travel_button()
        MGSWT:listen_to_malakai_travel_panel_opened()
        MGSWT:listen_to_malakai_travel_panel_closed()
    end)
end)