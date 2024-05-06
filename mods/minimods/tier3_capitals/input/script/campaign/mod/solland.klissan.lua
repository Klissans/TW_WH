local function resurrect_solland()
    if not (cm:is_new_game()
            and (cm:model():campaign_name_key() ~= "wh3_main_combi"
            or cm:model():campaign_name_key() ~= "cr_combi_expanded")) then
        return
    end
    return -- need to implement a faction actually
    if not vfs.exists("script/frontend/mod/mixer_frontend.lua") then
        return
    end

    local solland_faction = cm:get_faction('mixer_emp_solland')
    local pfeildorf_region = cm:get_region("wh3_main_combi_region_pfeildorf")
    local black_venom_faction = cm:get_faction('wh_main_grn_black_venom')
    local court_of_the_night_faction = cm:get_faction('wh3_dlc25_vmp_the_court_of_night')

    if pfeildorf_region:owning_faction():name() == solland_faction:name() then
        return
    end

    cm:transfer_region_to_faction(pfeildorf_region:name(), solland_faction:name())
    cm:heal_garrison(pfeildorf_region:cqi())

    local solland_starting_units = {
        'wh_main_emp_inf_swordsmen',
        'wh_main_emp_inf_swordsmen',
        'wh_main_emp_inf_swordsmen',
        'wh_main_emp_inf_spearmen_1',
        'wh_main_emp_inf_spearmen_1',
        'wh_main_emp_inf_spearmen_1',
        'wh_main_emp_inf_crossbowmen',
        'wh_main_emp_inf_crossbowmen',
        'wh_main_emp_cav_empire_knights',
    }
    cm:create_force_with_existing_general(
        cm:char_lookup_str(solland_faction:faction_leader()),
        solland_faction:name(),
        table.concat(solland_starting_units,','),
        pfeildorf_region:name(),
        pfeildorf_region:settlement():logical_position_x() + 1,
        pfeildorf_region:settlement():logical_position_y() + 1,
        function(cqi) end
    )

    cm:force_declare_war(solland_faction:name(), black_venom_faction:name(), false, false)
    cm:force_declare_war(solland_faction:name(), court_of_the_night_faction:name(), false, false)
end

cm:add_post_first_tick_callback(function() resurrect_solland() end)