Klissan_ROC = {
    factions = {
        settled_empires = {},
        settled_minors = {},
    },

    dummy_factions_keys = {
        ['wh3_dlc23_chd_conclave'] = true,
        ['wh2_dlc09_tmb_the_sentinels'] = true,
        ['wh3_main_skv_clan_carrion'] = true,
        ['wh_main_grn_necksnappers'] = true,
    },

    first_settlements_mapping_ie = {
        ['wh2_dlc13_emp_golden_order'] = 'wh3_main_combi_region_temple_of_elemental_winds',
        ['wh3_main_ksl_ursun_revivalists'] = 'wh3_main_combi_region_the_tower_of_torment',
        ['wh2_main_def_hag_graef'] = 'wh3_main_combi_region_black_rock',
        ['wh3_main_chs_shadow_legion'] = 'wh3_main_combi_region_konquata',
        ['wh3_main_dae_daemon_prince'] = 'wh3_main_combi_region_volcanos_heart',
        ['wh_main_chs_chaos'] = 'wh3_main_combi_region_the_writhing_fortress',
        ['wh3_dlc20_chs_azazel'] = 'wh3_main_combi_region_the_tower_of_khrakk',
        ['wh3_dlc20_chs_vilitch'] = 'wh3_main_combi_region_red_fortress',
        ['wh3_dlc20_chs_valkia'] = 'wh3_main_combi_region_dagraks_end',
        ['wh3_dlc20_chs_sigvald'] = 'wh3_main_combi_region_fortress_of_the_damned',
        ['wh3_dlc20_chs_kholek'] = 'wh3_main_combi_region_the_challenge_stone',
        ['wh3_main_tze_sarthoraels_watchers'] = 'wh3_main_combi_region_okkams_forever_maze',
    },

    spot_from_settlement = {
        is_on_sea = false,
        is_same_region = true,
        min = 5,
        max_distance_coeff = 0.35,
    },

    settlement_tiers = {
        minor = 2,
        province_capital = 3,
        faction_capital = 4,
        dummy_factions_offset = 1,
    },

    settlement_distance_variety_coeff = 1.15, -- should be greater or equal to 1

    flip_chance = 9,
    desolation_chance = 8,
    plague_chance = 7,
    rebellion_chance = 6,

    turn_number = 1,

    mixer_empire_chance = 25,

}


Klissan_H:setup_logging(Klissan_ROC, 'Klissan_EAW')

-- Random tech (give random techs, research points, or 1 turn tech boost)
-- Random xp to chars (6-9) level
-- random items & squires
-- generate armies for minors?
-- shuffle horde positions?
-- ROC portals?

function Klissan_ROC:get_distance(x_min, y_min, x_max, y_max)
    return math.sqrt(math.pow(math.abs(x_max-x_min), 2) + math.pow(math.abs(y_max-y_min), 2))
end



function Klissan_ROC:generate_vanilla_empires()
    local model_faction_list = cm:model():world():faction_list()
    for i = 0, model_faction_list:num_items() - 1 do
        local faction = model_faction_list:item_at(i)
        local settlement_check = faction:region_list():num_items() > 0
        if faction:can_be_human() and not faction:is_dead() and settlement_check and not Klissan_ROC.dummy_factions_keys[faction:name()]
                or Klissan_ROC.first_settlements_mapping_ie[faction:name()] ~= nil then -- srtha fix
            self.factions.settled_empires[faction:name()] = true
        elseif not faction:can_be_human() and not faction:is_dead() and settlement_check and not Klissan_ROC.dummy_factions_keys[faction:name()] then
            self.factions.settled_minors[faction:name()] = true
        end
    end
end

function Klissan_ROC:generate_mixer_empires()
    local model_faction_list = cm:model():world():faction_list()
    for i = 0, model_faction_list:num_items() - 1 do
        local faction = model_faction_list:item_at(i)
        local settlement_check = faction:region_list():num_items() > 0
        if not faction:is_dead() and not Klissan_ROC.dummy_factions_keys[faction:name()] and settlement_check then
            local empire_roll = cm:random_number()
            if faction:is_human() or empire_roll <= self.mixer_empire_chance then
                self.factions.settled_empires[faction:name()] = true
            else
                self.factions.settled_minors[faction:name()] = true
            end
        end
    end
end

function Klissan_ROC:get_factions_keys(is_playable, with_settlements)
    if is_playable and with_settlements then
        return self.factions.settled_empires
    elseif not is_playable and with_settlements then
        return self.factions.settled_minors
    end
end
--===== End OF Helpers ===--

function Klissan_ROC:move_character_to_random_own_settlement(char)
    if char:is_at_sea() then
        return
    end
    local faction = char:faction()
    local region_roll_i = cm:random_number(faction:region_list():num_items()) - 1
    local region = faction:region_list():item_at(region_roll_i)
    local x_min, y_min, x_max, y_max = region:region_data_interface():get_bounds()
    local region_size = math.ceil(self.spot_from_settlement.max_distance_coeff * Klissan_ROC:get_distance(x_min, y_min, x_max, y_max))
    local distance_roll = cm:random_number(region_size, self.spot_from_settlement.min)
    local target_x, target_y = cm:find_valid_spawn_location_for_character_from_settlement(
        faction:name(),
        region:name(),
        self.spot_from_settlement.is_on_sea,
        self.spot_from_settlement.is_same_region,
        distance_roll
    )
    cm:teleport_to(cm:char_lookup_str(char), target_x, target_y)
    Klissan_ROC:debug('<move_character_to_random_own_settlement> Faction: %s  Character: %d (%s %s) -> %s (%d %d)', faction:name(), char:cqi(), char:get_forename(), char:get_surname(), region:name(), target_x, target_y)
end

--todo move hordes? remember sea raiders
function Klissan_ROC:move_minors_characters_randomly()
    local minor_factions_keys = Klissan_ROC:get_factions_keys(false, true)
    for faction_key, _ in pairs(minor_factions_keys) do
        local faction = cm:get_faction(faction_key)
        for ci = 0, faction:character_list():num_items() - 1 do
            local char = faction:character_list():item_at(ci)
            Klissan_ROC:move_character_to_random_own_settlement(char)
        end
    end
end

function Klissan_ROC:move_majors_characters_randomly()
    local minor_factions_keys = Klissan_ROC:get_factions_keys(true, true)
    for faction_key, _ in pairs(minor_factions_keys) do
        local faction = cm:get_faction(faction_key)
        for ci = 0, faction:character_list():num_items() - 1 do
            local char = faction:character_list():item_at(ci)
            Klissan_ROC:move_character_to_random_own_settlement(char)
        end
    end
end


function Klissan_ROC:global_upgrade_settlements()
    local model_region_list = cm:model():world():region_manager():region_list()
    for i = 0, model_region_list:num_items() - 1 do
        local region = model_region_list:item_at(i)
        if not region:is_abandoned() then
            local offset = self.dummy_factions_keys[region:owning_faction():name()] and self.settlement_tiers.dummy_factions_offset or 0
            local tier = region:is_province_capital() and self.settlement_tiers.province_capital or self.settlement_tiers.minor
            cm:instantly_set_settlement_primary_slot_level(region:settlement(), tier + offset)
        end
    end
end


function Klissan_ROC:get_distances_to_capitals_of_playable_factions(region)
    local min_distance = 999999
    local results = {}
    local x, y = Klissan_CH:get_logical_position(region:settlement())
    local empires_factions_keys = Klissan_ROC:get_factions_keys(true, true)
    for faction_key, _ in pairs(empires_factions_keys) do
        local faction = cm:get_faction(faction_key)
        local xx, yy = Klissan_CH:get_logical_position(faction:home_region():settlement())
        local distance = Klissan_ROC:get_distance(x, y, xx, yy)
        results[faction:name()] = distance
        if distance < min_distance then
            min_distance = distance
        end
    end
    return results, min_distance
end


function Klissan_ROC:settlement_transfer(region)
    local distances, min_distance = self:get_distances_to_capitals_of_playable_factions(region)
    local valid_distances = {}
    local distance_allowance = min_distance * self.settlement_distance_variety_coeff
    for faction_key, distance in pairs(distances) do
        if distance < distance_allowance then
            table.insert(valid_distances, faction_key)
        end
    end
    local roll_i = cm:random_number(#valid_distances)
    local rolled_faction_key = valid_distances[roll_i]
    self:debug('<settlement_transfer> Region %s -> Faction %s (choices: %d)', region:name(), rolled_faction_key, #valid_distances)
    cm:force_declare_war(rolled_faction_key, region:owning_faction():name(), false, false)
    cm:transfer_region_to_faction(region:name(), rolled_faction_key)
    cm:heal_garrison(region:cqi())
end


function Klissan_ROC:global_settlements_transfer()
    local minor_factions_keys = Klissan_ROC:get_factions_keys(false, true)
    local model_region_list = cm:model():world():region_manager():region_list()
    for i = 0, model_region_list:num_items() - 1 do
        local region = model_region_list:item_at(i)
        if not region:is_abandoned() and minor_factions_keys[region:owning_faction():name()] and not self.dummy_factions_keys[region:owning_faction():name()] then
            self:settlement_transfer(region)
        end
    end
end

-- todo climate considirations?
function Klissan_ROC:move_capitals()
    local empires_factions_keys = Klissan_ROC:get_factions_keys(true, true)
    for faction_key, _ in pairs(empires_factions_keys) do
        local faction =cm:get_faction(faction_key)
        local home_region = faction:home_region()
        if not home_region:is_province_capital() then
            if home_region:province():capital_region():owning_faction():name() == faction:name() then
                self:debug('<move_capitals> Change Capital of %s (%s -> %s) in same province', faction:name(), home_region:name(),home_region:province():capital_region():name())
                cm:change_home_region_of_faction(faction, home_region:province():capital_region())
            else -- find any other province capital settlement
                for j = 0, faction:region_list():num_items() - 1 do
                    local region = faction:region_list():item_at(j)
                    if region:is_province_capital() then
                        self:debug('<move_capitals> Found Province capital for %s -> %s', faction:name(), region:name())
                        cm:change_home_region_of_faction(faction, region)
                        break
                    end
                end
                self:debug('<move_capitals> Found none Province capitals for %s', faction:name())
            end
        end
    end
end

function Klissan_ROC:upgrade_playable_factions_capitals()
    local empires_factions_keys = Klissan_ROC:get_factions_keys(true, true)
    for faction_key, _ in pairs(empires_factions_keys) do
        local faction =cm:get_faction(faction_key)
        local home_region = faction:home_region()
        cm:instantly_set_settlement_primary_slot_level(home_region:settlement(), self.settlement_tiers.faction_capital)
    end
end

--todo move to cco file
function Klissan_ROC:get_random_allowed_buildings_for_region(region_key)
    local result_str = Klissan_CH:croot():Call(string.format([=[
        (
            region_key = '%s',
            settlement = CampaignRoot.SettlementList.FirstContext(RegionRecordKey == region_key),
            settlement_level = settlement.BuildingSlotList.FirstContext(IsPrimary).BuildingContext.BuildingLevelRecordContext.Level,
            slot = settlement.BuildingSlotList.FirstContext(!IsPrimary && !IsPort),
            result = slot.PossibleBuildingChainsList
                .Filter(!LevelsList.All(PrimarySlotBuildingLevelRequirement > settlement_level))
                .Transform((x, flist = x.LevelsList.Filter(PrimarySlotBuildingLevelRequirement <= settlement_level), i = TrueRandomInRange(0, flist.Size - 1)) => flist[i])
                .Filter(!IsEpisodicRestricted && RequiredTechnologiesList.Size == 0 && !DoesBuildingExceedCap(slot)
                    && !IsRedundantDuplicate(settlement) && !BuildingChainRecordContext.LevelsList[0].IsRedundantDuplicate(settlement)
                    && HasEnoughDevelopmentPoints(settlement) && BuildingChainRecordContext.LevelsList[0].HasEnoughDevelopmentPoints(settlement))
        ) => result.JoinString(Key, '|')
    ]=], region_key))
    return string.split(result_str, '|')
end

--todo does it change treasury when dismantle?
function Klissan_ROC:develop_cities()
    local model_region_list = cm:model():world():region_manager():region_list()
    for i = 0, model_region_list:num_items() - 1 do
        local region = model_region_list:item_at(i)
        if not region:is_abandoned() then
            local possible_buildings = Klissan_ROC:get_random_allowed_buildings_for_region(region:name())
            cm:shuffle_table(possible_buildings)
            local pbi = 1
            for s = 0, region:slot_list():num_items() - 1 do
                local slot = region:slot_list():item_at(s)
                if slot:type() ~= 'primary' and slot:type() ~= 'port' then
                    if slot:has_building() then
                        cm:instantly_dismantle_building_in_region(slot)
                    end
                    if slot:active() then
                        cm:instantly_upgrade_building_in_region(slot, possible_buildings[pbi])
                        pbi = pbi + 1
                    end
                end
            end
        end
    end
end


--todo move to cco file
function Klissan_ROC:get_recruitable_units_with_tiers_for_faction(faction_key)
    local result_str = Klissan_CH:croot():Call(string.format([=[
        (
            faction = CampaignRoot.FactionList.FirstContext(FactionRecordContext.Key == '%s'),
            unit_level_pair = faction.SettlementList
                .Transform(BuildingSlotList).Filter(!IsEmpty && !IsPrimary)
                .Transform((slot, levels = slot.BuildingContext.BuildingLevelRecordContext.BuildingChainRecordContext.LevelsList) =>
                    levels.Filter((x) => x.PrimarySlotBuildingLevelRequirement <= slot.BuildingContext.BuildingLevelRecordContext.PrimarySlotBuildingLevelRequirement).Transform((x) => MakePair(slot.SettlementContext, x)))
                .Distinct(Second.Key).Filter((pair, stl = pair.First, blevel = pair.Second) => blevel.UnitList(stl, faction).Size > 0)
                .Transform((pair, stl = pair.First, blevel = pair.Second) => blevel.UnitList(stl, faction).Transform((x) => MakePair(blevel.PrimarySlotBuildingLevelRequirement, x)))
        ) => unit_level_pair.JoinString(First + ';' + Second.Key, '|')
    ]=], faction_key))
    return string.split(result_str, '|')
end


function Klissan_ROC:generate_armies()
    local empires_factions_keys = Klissan_ROC:get_factions_keys(true, true)
    for faction_key, _ in pairs(empires_factions_keys) do
        local faction = cm:get_faction(faction_key)
        local unit_tiers = self:get_recruitable_units_with_tiers_for_faction(faction_key)

        local ram = random_army_manager
        local ram_key = "empires_at_war_"..faction_key
        ram:remove_force(ram_key)
        ram:new_force(ram_key)
        for _, value in pairs(unit_tiers) do
            local split = string.split(value, ';')
            local unit_tier, unit_key = tonumber(split[1]), split[2]
            ram:add_unit(ram_key, unit_key, 6 - unit_tier)
        end

        local n_armies = math.ceil(faction:region_list():num_items() / 3.0)
        for i=1, n_armies do
            local army_size = cm:random_number(9, 6)
            local unit_list = ram:generate_force(ram_key, army_size, false)
            local pos_x, pos_y = cm:find_valid_spawn_location_for_character_from_settlement(faction_key, faction:home_region():name(), false, true, 11)
            cm:create_force(faction_key, unit_list, faction:home_region():name(), pos_x, pos_y, true, function(cqi)  end)
        end
    end
end


function Klissan_ROC:flip_regions()
    local model_region_list = cm:model():world():region_manager():region_list()
    local model_region_list_keys = {}
    for i = 0, model_region_list:num_items() - 1 do
        table.insert(model_region_list_keys, model_region_list:item_at(i):name())
    end
    cm:shuffle_table(model_region_list_keys)
    for i = 1, #model_region_list_keys do
        local region = cm:get_region(model_region_list_keys[i])
        local flip_roll = cm:random_number()
        local flip_chance = self.flip_chance
        if cm:is_new_game() then -- make it more volatile at the start of the game to force more empire wars
            flip_chance = 2 * flip_chance
        end
        if region:is_abandoned() then
            local adj_empires_factions = {}
            for j=0, region:adjacent_region_list():num_items() - 1 do
                local adj_region = region:adjacent_region_list():item_at(j)
                local fname = adj_region:owning_faction():name()
                adj_empires_factions[fname] = true
            end
            local adj_empires_factions_keys = Klissan_H:get_key_sorted(adj_empires_factions)
            local roll_i = cm:random_number(#adj_empires_factions_keys)
            local rolled_faction_key = adj_empires_factions_keys[roll_i]
            self:debug('<flip_regions> [%d] Abandoned region %s -> %s', flip_roll, region:name(), rolled_faction_key)
            cm:transfer_region_to_faction(region:name(), rolled_faction_key)
        else
            if flip_roll <= flip_chance and not region:is_province_capital() and (region:name() ~= region:owning_faction():home_region():name())
                            and not self.dummy_factions_keys[region:owning_faction():name()] then
                local original_owner = region:owning_faction():name()
                local adj_empires_factions = {}
                for j=0, region:adjacent_region_list():num_items() - 1 do
                    local adj_region = region:adjacent_region_list():item_at(j)
                    local fname = adj_region:owning_faction():name()
                    if original_owner ~= fname and not self.dummy_factions_keys[fname] then
                        adj_empires_factions[fname] = true
                    end
                end
                if Klissan_H:table_size(adj_empires_factions) > 0 then
                    local adj_empires_factions_keys = Klissan_H:get_key_sorted(adj_empires_factions)
                    local roll_i = cm:random_number(#adj_empires_factions_keys)
                    local rolled_faction_key = adj_empires_factions_keys[roll_i]
                    self:debug('<flip_regions> [%d] Region %s (%s) -> %s', flip_roll, region:name(), region:owning_faction():name(),  rolled_faction_key)
                    cm:force_declare_war(rolled_faction_key, region:owning_faction():name(), false, false)
                    cm:transfer_region_to_faction(region:name(), rolled_faction_key)
                end
            end
        end
    end
end


function Klissan_ROC:declare_random_wars_between_empires()
    local empires_factions_keys = Klissan_ROC:get_factions_keys(true, true)
    for faction_key, _ in pairs(empires_factions_keys) do
        local faction = cm:get_faction(faction_key)
        local met_factions = faction:factions_met()
        for i = 0, met_factions:num_items() - 1 do
            local another_faction = met_factions:item_at(i)
            local war_roll = cm:random_number()
            if war_roll <= self.flip_chance and empires_factions_keys[another_faction:name()] then
                cm:force_declare_war(faction_key, another_faction:name(), false, false)
                self:debug('<declare_random_wars_between_empires> %s -> %s', faction_key, another_faction:name())
            end
        end
    end
end

function Klissan_ROC:desolation()
    local model_region_list = cm:model():world():region_manager():region_list()
    for i = 0, model_region_list:num_items() - 1 do
        local region = model_region_list:item_at(i)
        local desoroll = cm:random_number()
        local destroll = cm:random_number()
        if not region:is_abandoned() then
            if desoroll <= self.desolation_chance and not region:is_province_capital() and region:name() ~= region:owning_faction():home_region():name() then
                self:debug('<desolation> Rolled a chance %d for region %s (%s) to be razed', desoroll, region:name(), region:owning_faction():name())
                cm:set_region_abandoned(region:name())
            elseif (desoroll <= self.desolation_chance and region:is_province_capital() or destroll <= self.desolation_chance) or cm:is_new_game() then -- damage buildings
                for s = 0, region:slot_list():num_items() - 1 do
                    local slot = region:slot_list():item_at(s)
                    if slot:has_building() then
                        local disroll = cm:random_number()
                        if disroll <= self.desolation_chance and region:is_province_capital() and (slot:type() ~= 'primary' and slot:type() ~= 'port') and not cm:is_new_game() then
                            self:debug('<desolation> Destroyed building %s building in region %s', slot:building():name(), region:name())
                            cm:instantly_dismantle_building_in_region(slot)
                        else
                            local building = slot:building()
                            local damaged_coeff = 1 - cm:random_number(math.pow(self.desolation_chance, 2), self.desolation_chance) / 100.0
                            if not region:owning_faction():is_human() then -- so ai is not broke
                                damaged_coeff = 1 - cm:random_number(self.desolation_chance) / 100.0
                            end
                            local percent_health = math.ceil(damaged_coeff * building:percent_health())
                            cm:instant_set_building_health_percent(region:name(), building:name(), percent_health)
                            self:debug('<desolation> Earthquaking region %s (%s) building %s (%d)', region:name(), region:owning_faction():name(), building:name(), percent_health)
                        end
                    end
                end
            end
        end
    end
end


function Klissan_ROC:pests()
    local pest_factions = cm:get_factions_by_culture('wh3_main_nur_nurgle') -- todo should we check for dead factions?
    local model_region_list = cm:model():world():region_manager():region_list()
    for i = 0, model_region_list:num_items() - 1 do
        local region = model_region_list:item_at(i)
        local pestroll = cm:random_number()
        if not region:is_abandoned() then
            if pestroll <= self.plague_chance then
                local plague_choice = 'wh3_dlc25_nur_random_plague_'..cm:random_number(5)
                local nugrgle_faction = pest_factions[cm:random_number(#pest_factions)]
                self:debug('<pests> Rolled a chance %d for region %s (%s) to be plagued by %s (%s)', pestroll, region:name(), region:owning_faction():name(), plague_choice, nugrgle_faction:name())
                cm:spawn_plague_at_settlement(nugrgle_faction, region:settlement(), plague_choice)
            end
        end
    end

    local faction_list = cm:model():world():faction_list()
    for i = 0, faction_list:num_items() - 1 do
        local faction = faction_list:item_at(i)
        for j = 0, faction:military_force_list():num_items() - 1 do
            local military_force = faction:military_force_list():item_at(j)
            -- todo set non-embedded characters health
            local pestroll = cm:random_number()
            if (pestroll <= self.plague_chance) or cm:is_new_game() then
                for h = 0, military_force:unit_list():num_items() - 1 do
                    local unit = military_force:unit_list():item_at(h)
                    local health_damage_coeff = cm:random_number(math.pow(self.plague_chance, 2), self.plague_chance) / 100.0
                    if faction:region_list():num_items() == 0 then -- less attrition for regionless forces
                        health_damage_coeff = 1 - health_damage_coeff
                    end
                    local hp = health_damage_coeff * unit:percentage_proportion_of_full_strength() / 100.0
                    cm:set_unit_hp_to_unary_of_maximum(unit, hp)
                    --self:debug('<pests> damaging %f * %f unit %s of %s (%s)', health_damage_coeff, unit:percentage_proportion_of_full_strength(), unit:unit_key(), character:get_forename(), faction:name())
                end
            end
        end
    end
end

function Klissan_ROC:rebels()
    local model_region_list = cm:model():world():region_manager():region_list()
    for i = 0, model_region_list:num_items() - 1 do
        local region = model_region_list:item_at(i)
        local slaaroll = cm:random_number()
        if not region:is_abandoned() then
            if slaaroll <= self.rebellion_chance then
                local n_armies = cm:random_number(self.rebellion_chance)
                for k=1, n_armies do
                    local max_units = cm:random_number(self.rebellion_chance)
                    local xx, yy = Klissan_CH:get_logical_position(region:settlement())
                    cm:force_rebellion_in_region(region:name(), max_units, xx, yy, false)
                end
                self:debug('<rebels> forcing rebellion in %s (%s) with %d armies', region:name(), region:owning_faction():name(), n_armies)
            end
        end
    end
end

function Klissan_ROC:hinder_player_movement()
    local faction_list = cm:model():world():faction_list()
    for i = 0, faction_list:num_items() - 1 do
        local faction = faction_list:item_at(i)
        if faction:is_human() then
            local character_list = faction:character_list()
            for j = 0, character_list:num_items() - 1 do
                local character = character_list:item_at(j)
                cm:replenish_action_points(cm:char_lookup_str(character), cm:random_number() / 100.0)
            end
        end
    end
end


function Klissan_ROC:lucky_money()
    local empires_factions_keys = Klissan_ROC:get_factions_keys(true, true)
    for faction_key, _ in pairs(empires_factions_keys) do
        local faction = cm:get_faction(faction_key)
        if not faction:is_human() then
            local money = cm:random_number(9999, 6666)
            cm:treasury_mod(faction:name(), money)
            self:debug('<lucky_money> %s - %d', faction:name(), money)
        end
    end
end


function Klissan_ROC:setup_IE()
    for faction_key, region_key in pairs(self.first_settlements_mapping_ie) do
        local faction = cm:get_faction(faction_key)
        local region = cm:get_region(region_key)
        if faction:region_list():num_items() == 0 or faction_key == 'wh3_main_tze_sarthoraels_watchers' then
            cm:transfer_region_to_faction(region_key, faction_key)
            cm:change_home_region_of_faction(faction, region)
        end
    end
end

function Klissan_ROC:chaos_gods()
    self:debug('<chaos_gods> Starting...')
    local tzeentch_roll = cm:random_number()
    self:debug('<chaos_gods> rolled %d for <flip_regions> on turn %d', tzeentch_roll, cm:model():turn_number())
    if tzeentch_roll <= self.flip_chance or cm:is_new_game() then
        self:flip_regions()
    end
    local khorn_roll = cm:random_number()
    self:debug('<chaos_gods> rolled %d for <desolation> on turn %d', khorn_roll, cm:model():turn_number())
    if khorn_roll <= self.desolation_chance or cm:is_new_game() then
        self:desolation()
    end
    local nurgle_roll = cm:random_number()
    self:debug('<chaos_gods> rolled %d for <pests> on turn %d', nurgle_roll, cm:model():turn_number())
    if nurgle_roll <= self.plague_chance or cm:is_new_game() then
        self:pests()
    end
    local slaanesh_roll = cm:random_number()
    self:debug('<chaos_gods> rolled %d for <rebels> on turn %d', slaanesh_roll, cm:model():turn_number())
    if slaanesh_roll <= self.rebellion_chance or cm:is_new_game() then
        self:rebels()
    end
end


function Klissan_ROC:setup()
    self:move_minors_characters_randomly()
    self:debug('SETUP DONE: <move_minors_characters_randomly>')
    self:global_upgrade_settlements()
    self:debug('SETUP DONE: <global_upgrade_settlements>')
    self:global_settlements_transfer()
    self:debug('SETUP DONE: <global_settlements_transfer>')
    self:move_capitals()
    self:debug('SETUP DONE: <move_capitals>')
    self:upgrade_playable_factions_capitals()
    self:debug('SETUP DONE: <upgrade_playable_factions_capitals>')
    self:develop_cities()
    self:debug('SETUP DONE: <develop_cities>')
    self:generate_armies()
    self:debug('SETUP DONE: <generate_armies>')
    self:move_majors_characters_randomly()
    self:debug('SETUP DONE: <move_majors_characters_randomly>')
    self:lucky_money()
    self:debug('SETUP DONE: <lucky_money>')
    self:declare_random_wars_between_empires()
    self:debug('SETUP DONE: <declare_random_wars_between_empires>')

    self:chaos_gods()
    self:debug('SETUP DONE: <chaos_gods>')
end

function Klissan_ROC:init_chaos_gods_listener()
    local event_name = 'FactionTurnStart'

    core:add_listener(
        Klissan_CH:get_listener_name('empire_at_wars_chaos_gods_'..event_name),
        event_name,
        function(context)
            return cm:model():turn_number() > Klissan_ROC.turn_number
        end,
        function(context)
            Klissan_ROC:chaos_gods()
            Klissan_ROC.turn_number = Klissan_ROC.turn_number + 1
        end,
        true
    )
end

function Klissan_ROC:init_hinder_player_movement_listener()
    local event_name = 'FactionTurnStart'

    core:add_listener(
        Klissan_CH:get_listener_name('empire_at_wars_hinder_player_movement_'..event_name),
        event_name,
        function(context)
            return cm:model():turn_number() == 1 and context:faction():is_human()
        end,
        function(context)
            self:hinder_player_movement()
            self:debug('SETUP DONE: <hinder_player_movement>')
        end,
        true
    )
end

cm:add_post_first_tick_callback(
    function ()
        Klissan_ROC.turn_number = cm:model():turn_number()
        if not cm:is_new_game() then
            return
        end

        if cm:model():campaign_name_key() == "wh3_main_combi" or cm:model():campaign_name_key() == "cr_combi_expanded" then
            Klissan_ROC:setup_IE()
        end

        if common.vfs_exists('script/_lib/mod/mixer_lib.lua') then
            Klissan_ROC:generate_mixer_empires()
        else
            Klissan_ROC:generate_vanilla_empires()
        end

        Klissan_ROC:setup()

        Klissan_ROC:init_chaos_gods_listener()
        Klissan_ROC:init_hinder_player_movement_listener()
    end
)