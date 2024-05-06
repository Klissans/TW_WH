local function get_character_coordinates(character)
    return character:logical_position_x(), character:logical_position_y()
end

local function swap_characters(first, second)
    local offset = 1 -- offset needed as this tile is occupied
    local x1, y1 = get_character_coordinates(first)
    local x2, y2 = get_character_coordinates(second)
    cm:teleport_to(cm:char_lookup_str(first), x2 + offset, y2 + offset)
    cm:teleport_to(cm:char_lookup_str(second), x1 + offset, y1 + offset)
end

local function transfer_all_regions(region_list, target_faction)
    for i = 0, region_list:num_items() - 1 do
        local region = region_list:item_at(i)
        cm:transfer_region_to_faction(region:name(), target_faction:name())
        cm:heal_garrison(region:cqi())
    end
end

local function swap_oxyotl_epidemius()
    if not (cm:is_new_game()
            and (cm:model():campaign_name_key() ~= "wh3_main_combi"
            or cm:model():campaign_name_key() ~= "cr_combi_expanded")) then
        return
    end
    out('!Klissan Campaign: Swapping Oxyotl - Epidemius')
    local oxyotl_faction = cm:get_faction('wh2_dlc17_lzd_oxyotl')
    local epidemius_faction = cm:get_faction('wh3_dlc25_nur_epidemius')
    local oxyotl_enemy_faction = oxyotl_faction:factions_at_war_with():item_at(0)
    local epidemius_enemy_faction = epidemius_faction:factions_at_war_with():item_at(0)

    local n_characters = 2
    for i = 0, n_characters - 1 do
        swap_characters(
                oxyotl_faction:character_list():item_at(i),
                epidemius_faction:character_list():item_at(i)
        )
    end

    -- presave before exchanging
     local oxyotl_regions = oxyotl_faction:region_list()
     local epidemius_regions = epidemius_faction:region_list()
     transfer_all_regions(oxyotl_regions, epidemius_faction)
     transfer_all_regions(epidemius_regions, oxyotl_faction)

     cm:force_make_peace(oxyotl_faction:name(), oxyotl_enemy_faction:name())
     cm:force_make_peace(epidemius_faction:name(), epidemius_enemy_faction:name())
     cm:force_declare_war(oxyotl_faction:name(), epidemius_enemy_faction:name(), false, false)
     cm:force_declare_war(epidemius_faction:name(), oxyotl_enemy_faction:name(), false, false)

     cm:reset_shroud(oxyotl_faction:name())
     cm:reset_shroud(epidemius_faction:name())
    out('!Klissan Campaign: Swapped Oxyotl - Epidemius')
end

cm:add_post_first_tick_callback(function() swap_oxyotl_epidemius() end)