local function move_info_panel()
    local info_panel = find_uicomponent(core:get_ui_root(), 'hud_campaign', 'unit_info_panel_adopter', 'unit_information_parent', 'unit_info_panel_holder')
    local x, y = core:get_screen_resolution()
    if y > 1000 then
        info_panel:SetDockOffset(10, - math.floor(y / 10))
    else
        info_panel:SetDockOffset(10, 0)
    end
end

cm:add_ui_created_callback(function()
    cm:add_post_first_tick_callback(
        move_info_panel
    )
end)