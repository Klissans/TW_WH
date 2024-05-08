--todo diplomatic manipulation vs ritual?

--to enable tzeentch ritual's panel:
-- db/ui_features_to_factions_tables

-- RITUALS
-- Bombardment (force, settlement in range of TSoG)
-- Scout (targeted adjacent province or all adjacent regions, hmmm)
-- Deliever Supplies (Target non-hostile Settlement in region) [heal garrison, boost growth]


LISTENER_KLISSAN_MALAKAI_TRAVEL = 'klissan_malakai_travel'
RITUAL_KLISSAN_MALAKAI_TRAVEL = 'klissan_malakai_travel'

core:remove_listener(RITUAL_KLISSAN_MALAKAI_TRAVEL)
core:add_listener(
	LISTENER_KLISSAN_MALAKAI_TRAVEL,
	"RitualCompletedEvent",
	function (context)
        return context:ritual():ritual_category() == "TZEENTCH_RITUAL"
                and context:ritual():ritual_key() == RITUAL_KLISSAN_MALAKAI_TRAVEL
    end,
	function(context)
		local performing_faction = context:performing_faction()
		local ritual = context:ritual() -- ACTIVE_RITUAL_SCRIPT_INTERFACE

        if ritual:ritual_target():target_type() ~= 'REGION' then
            return -- smth went wrong
        end

        local target_x, target_y = cm:find_valid_spawn_location_for_character_from_settlement(
            performing_faction:name(),
            ritual:ritual_target():get_target_region():name(),
            false,
            true,
            5
        )

        local malaki_str = cm:char_lookup_str(performing_faction:faction_leader())
        cm:teleport_to(malaki_str, target_x, target_y) -- todo applies tresspasing wtf
        cm:zero_action_points(malaki_str)
        cm:force_character_force_into_stance(malaki_str, 'MILITARY_FORCE_ACTIVE_STANCE_TYPE_MARCH')
        -- todo add a chance to get lost (travel to random location)
	end,
	true
)


local function edit_travel_button()
    if cm:get_local_faction():name() ~= 'wh3_dlc25_dwf_malakai' then
        return
    end
    local travel_button = find_uicomponent(core:get_ui_root(), 'hud_campaign', 'faction_buttons_docker', 'button_group_management', 'button_changing_of_the_ways')
    local icon_path = 'ui/common ui/unit_category_icons/klissan_grungni_icon.png'
    travel_button:SetImagePath(icon_path)
    local travel_button_tooltip_key = 'land_units_onscreen_name_wh3_dlc25_dwf_veh_thunderbarge_grungni' -- 'unit_description_short_texts_text_wh3_dlc25_unit_short_text_dwf_veh_thunderbarge'
    travel_button:SetTooltipText(common.get_localised_string(travel_button_tooltip_key), travel_button_tooltip_key, true)
end


local function listen_to_malakai_travel_panel_opened()
    core:add_listener(
        "klissan_malakai_travel_panel_opened",
        "PanelOpenedCampaign",
        function(context)
            return cm:get_local_faction():name() == 'wh3_dlc25_dwf_malakai' and context.string == "tzeentch_changing_of_ways"
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
        end,
        true
    )
end



cm:add_ui_created_callback(
    function()
        cm:add_post_first_tick_callback(edit_travel_button)
        cm:add_post_first_tick_callback(listen_to_malakai_travel_panel_opened)
    end
)