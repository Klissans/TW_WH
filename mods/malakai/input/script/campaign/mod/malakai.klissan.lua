
local function resurrect_kraka_drak(force_coord_x, force_coord_y, malakai_old_enemy)
    local kraka_drak_faction = cm:get_faction('wh_main_dwf_kraka_drak')
    local kraka_drak_region = cm:get_region('wh3_main_combi_region_kraka_drak')

    if kraka_drak_region:owning_faction():name() == kraka_drak_faction:name() then
        return
    end

    cm:set_region_abandoned(kraka_drak_region:name())
    cm:transfer_region_to_faction(kraka_drak_region:name(), kraka_drak_faction:name())
    cm:instantly_set_settlement_primary_slot_level(kraka_drak_region:settlement(), 3)
    cm:instantly_set_settlement_primary_slot_level(kraka_drak_region:settlement(), 3)
    cm:add_building_to_settlement(kraka_drak_region:name(), 'wh_main_dwf_resource_gems_2')
    cm:heal_garrison(kraka_drak_region:cqi())

    local kraka_drak_starting_units = {
        'wh2_dlc10_dwf_inf_giant_slayers',
        'wh_main_dwf_inf_slayers',
        'wh_main_dwf_inf_hammerers',
        'wh_main_dwf_inf_miners_1',
        'wh_main_dwf_inf_miners_1',
        'wh_main_dwf_inf_miners_1',
        'wh_main_dwf_inf_irondrakes_0',
        'wh_main_dwf_inf_irondrakes_0',
        'wh_main_dwf_art_flame_cannon',
    }
    cm:create_force_with_existing_general(
        cm:char_lookup_str(kraka_drak_faction:faction_leader()),
        kraka_drak_faction:name(),
        table.concat(kraka_drak_starting_units,','),
        kraka_drak_region:name(),
        force_coord_x,
        force_coord_y,
        function(cqi) end
    )

    cm:force_declare_war(kraka_drak_faction:name(), malakai_old_enemy:name(), false, false)
end

local function malakai_setup()
    if not (cm:is_new_game()
            and (cm:model():campaign_name_key() ~= "wh3_main_combi"
            or cm:model():campaign_name_key() ~= "cr_combi_expanded")) then
        return
    end
    local old_enemy_faction = cm:get_faction('wh3_main_nur_maggoth_kin')
    local new_ogre_enemy_factions = cm:get_faction('wh3_main_ogr_fulg')
    local malakai_faction = cm:get_faction('wh3_dlc25_dwf_malakai')

    local malakai_x, malakai_y = get_character_coordinates(malakai_faction:faction_leader())
    cm:teleport_military_force_to(malakai_faction:faction_leader():military_force(), 1011, 647)

    cm:force_make_peace(malakai_faction:name(), old_enemy_faction:name())
    cm:force_declare_war(malakai_faction:name(), new_ogre_enemy_factions:name(), false, false)

    local karak_vrag = cm:get_region('wh3_main_combi_region_karak_vrag')
    if not malakai_faction:is_human() then
        cm:transfer_region_to_faction(karak_vrag:name(), malakai_faction:name())
        cm:heal_garrison(karak_vrag:cqi())
    else
        -- TODO Zoom camera to new position
    end
    cm:instantly_set_settlement_primary_slot_level(karak_vrag:settlement(), 3)

    resurrect_kraka_drak(malakai_x, malakai_y, old_enemy_faction)

    cm:reset_shroud(malakai_faction:name())

    -- make agreements and give vision over dawi factions capitals
    local same_culture_factions = malakai_faction:factions_of_same_subculture()
    for i = 0, same_culture_factions:num_items() - 1 do
        local faction = same_culture_factions:item_at(i)
        if not faction:is_dead() then
            cm:make_diplomacy_available(malakai_faction:name(), faction:name())
            cm:force_grant_military_access(malakai_faction:name(), faction:name(), false)
            cm:force_grant_military_access(faction:name(), malakai_faction:name(), false)
            cm:make_region_seen_in_shroud(malakai_faction:name(), faction:home_region():name())
        end
    end
end

cm:add_post_first_tick_callback(function() malakai_setup() end)