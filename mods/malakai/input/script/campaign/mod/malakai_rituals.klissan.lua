--todo diplomatic manipulation vs ritual?

--to enable tzeentch ritual's panel:
-- db/ui_features_to_factions_tables
-- db/campaign_groups_tables
-- db/campaign_group_members_tables
-- db/campaign_group_members_criteria_cultures_tables
-- db/campaign_features_tables

-- TO ADD RITUAL
-- db/rituals_tables -- completion_payload is REQUIRED
-- db/campaign_group_rituals_tables
-- db/ritual_targets_table -- NOT NECESSARY
-- db/ui_info_ritual_target_criterias -- NOT NECESSARY
-- db/ritual_region_target_critaerias_table -- NOT NECESSARY
-- db/ritual_payloads_table
-- db/campaign_payloads_table
-- db/campaign_payload_basic_value_components_table -- NOT NECESSARY

-- db/resource_costs_tables -- NOT NECESSARY
-- db/resource_costs_pooled_resource_junction

-- db/effect_bonus_value_ritual_junctions_tables  -- NOT NECESSARY


-- RITUALS
-- check if in Grungni range in ui code if needed
-- get ritual cost in ui code
-- execute ritual in listener

MGSWT.rituals = { -- should match db keys
    keys = {
        travel = 'klissan_malakai_travel_ritual',
        scout = 'klissan_malakai_scout_ritual',
        reinforce = 'klissan_malakai_supplies_ritual', -- todo check for borrowed ally army, no military buildings
        bombardment = 'klissan_malakai_bombard_ritual',
        ale = 'klissan_malakai_ale_ritual',
    },
    cost_mapping = nil,
    cost_multipliers = {
        travel_distance = 5,
        reinforce_discount = 0.5,
        region_scout_toll = 150,
        bombardment_cost = 2,
    },

     -- it's set via UI callbacks
    current_ritual = {
        is_valid_target = false, -- should be managed by ui only
        key = nil,
        target_type = nil,
        target_key = nil,
        currency_type = nil,
        value = nil,
    },

    cache = {
        ritual_reinforce = {units_str = nil, cost = nil}
    },

    drink = {
        effects = {
            'wh_main_effect_force_all_campaign_upkeep',
            'wh_main_effect_force_all_campaign_replenishment_rate',
            'wh_main_effect_force_all_campaign_recruitment_cost_all',
            'wh_main_effect_force_all_campaign_post_battle_loot_mod',
            'wh_main_effect_force_all_campaign_captives',
            'wh_main_effect_force_all_campaign_movement_range',
            'wh_main_effect_force_stat_leadership_pct',
            'wh_main_effect_force_stat_melee_attack_pct',
            --'wh_main_effect_force_stat_missile_damage',
            --'wh_main_effect_force_stat_melee_defence',
            'wh_main_effect_force_stat_charge_bonus_pct',
            'wh3_main_effect_force_stat_unit_mass_percentage_mod',
        }
    }
}

function MGSWT:get_rituals_which_need_range_check()
    local rkeys = self.rituals.keys
    local rituals = {}
    rituals[rkeys.reinforce] = true
    rituals[rkeys.bombardment] = true
    return rituals
end


function MGSWT:init_ritual_cost_mapping()
    self.rituals.cost_mapping = {}

    self.rituals.cost_mapping[self.rituals.keys.travel] = function ()
        return math.ceil(self.rituals.cost_multipliers.travel_distance * self:get_travel_distance())
    end

    self.rituals.cost_mapping[self.rituals.keys.reinforce] = function ()
        local units_str, cost = self:get_ritual_reinforce_units_cost_pair()
        self:debug('Reinforce Ritual, units: %s, units_cost: %d', units_str, cost)
        local adjusted_cost = math.ceil(self.rituals.cost_multipliers.reinforce_discount * cost)
        self.rituals.cache.ritual_reinforce.units_str = units_str
        self.rituals.cache.ritual_reinforce.cost = adjusted_cost
        return adjusted_cost
    end

    self.rituals.cost_mapping[self.rituals.keys.scout] = function ()
        local n_regions = cm:get_region(self.rituals.current_ritual.target_key):province():regions():num_items()
        return self.rituals.cost_multipliers.region_scout_toll * n_regions
    end

    self.rituals.cost_mapping[self.rituals.keys.bombardment] = function ()
        -- todo gdp is income we want settlement's valuation
        local region_gdp = cm:get_region(self.rituals.current_ritual.target_key):gdp()
        return self.rituals.cost_multipliers.bombardment_cost * region_gdp
    end

    self.rituals.cost_mapping[self.rituals.keys.ale] = function ()
        return 500
    end

end

function MGSWT:get_ritual_cost()
    local ritual_cost = 0
    local ritual_key = self:get_targeting_ritual_key() -- :gsub('_ritual$', '') -- appended in cco
    self:debug('Querying cost for ritual %s', ritual_key)
    local ritual_cost_func = self.rituals.cost_mapping[ritual_key]
    if ritual_cost_func == nil then
        self:debug('Query failed for %s', ritual_key)
        return ritual_cost
    end
    ritual_cost = ritual_cost_func()
    self:debug('Ritual cost %s is %d', ritual_key, ritual_cost)
    return ritual_cost
end

--'wh3_dlc25_dwf_spirit_of_grungni_beer_hall'
--'wh3_dlc25_dwf_spirit_of_grungni_cargo_hold'
--'wh3_dlc25_dwf_spirit_of_grungni_army_ability_2'
--'wh3_dlc25_dwf_spirit_of_grungni_engines'
--'wh3_dlc25_dwf_spirit_of_grungni_support_radius'
function MGSWT:get_horde_building_level(building_chain_key)
    local level = Klissan_CH:croot():Call(string.format([=[
        (
            building_chain_key = '%s',
            malakai_faction = CampaignRoot.FactionList.FirstContext(FactionRecordContext.Key == 'wh3_dlc25_dwf_malakai'),
            malakai = malakai_faction.FactionLeaderContext,
            malakai_army = malakai.MilitaryForceContext,
            malakai_horde = malakai_army.HordeContext,
            building_slot = malakai_horde.BuildingSlotList
                .FirstContext(PlayerVariantBuildingChainContext.Key == building_chain_key),
            building_level = GetIfElse(IsContextValid(building_slot), building_slot.BuildingContext.BuildingLevelRecordContext.PrimarySlotBuildingLevelRequirement, -1)
        ) => building_level
    ]=], building_chain_key))
    return level + 1 -- +1 to scale to [0, 5] range
end


function MGSWT:get_ritual_reinforce_units_cost_pair()
    local result_str =  Klissan_CH:croot():Call([=[
        (
            malakai_faction = CampaignRoot.FactionList.FirstContext(FactionRecordContext.Key == 'wh3_dlc25_dwf_malakai'),
            malakai = malakai_faction.FactionLeaderContext,
            malakai_army = malakai.MilitaryForceContext,
            malakai_horde = malakai_army.HordeContext,
            primary_level_building = malakai_horde.PrimarySlotContext.BuildingContext.BuildingLevelRecordContext,
            primary_level = primary_level_building.Level,
            primary_unit = GetIfElse(primary_level < 3,
                (ul = primary_level_building.UnitList(malakai), r = TrueRandomInRange(0, ul.Size-1)) => {ul[r]},
                (bcl = primary_level_building.BuildingChainRecordContext.LevelsList.FirstContext(Level == 2), ul = bcl.UnitList(malakai), r = TrueRandomInRange(0, ul.Size-1)) => {ul[r]}
                ),
            extra_unit = GetIfElse(primary_level > 2, (bcl = primary_level_building.BuildingChainRecordContext.LevelsList.FirstContext(Level == primary_level - 3), ul = bcl.UnitList(malakai), r = TrueRandomInRange(0, ul.Size-1)) => {ul[r]}, ''),
            units_from_primary_str = primary_unit.Key + ',' + GetIfElse(extra_unit != '',extra_unit.Key + ',', ''),
            military_level_slots = malakai_horde.BuildingSlotList
                .Filter(BuildingContext.BuildingLevelRecordContext.BuildingChainRecordContext.BuildingSetContext.Key == 'wh3_dlc25_set_dwarf_spirit_of_grungni_recruitment')
                .Transform(BuildingContext.BuildingLevelRecordContext),
            selected_units = military_level_slots
                .Transform((x, ul = x.UnitList(malakai), r = TrueRandomInRange(0, ul.Size-1)) => {ul[r]}),
            total_cost = selected_units.Sum(Cost),
            result_str = Format('%S%S|%d', units_from_primary_str, selected_units.JoinString(Key, ','), RoundFloat(total_cost + primary_unit.Cost + GetIf(extra_unit != '', extra_unit.Cost)))
        ) => result_str
    ]=])
    local split = string.split(result_str, '|')
    local units_str, cost = split[1], math.ceil(split[2])
    return units_str, cost
end

-- LISTENERS

function MGSWT:init_ritual_listeners()
    -- todo check if army moved
    core:remove_listener(Klissan_CH:get_listener_name(MGSWT.rituals.keys.travel)) -- todo remove?
    core:add_listener(
            Klissan_CH:get_listener_name(MGSWT.rituals.keys.travel),
            "RitualCompletedEvent",
            function (context)
                return context:ritual():ritual_category() == "TZEENTCH_RITUAL"
                        and context:ritual():ritual_key() == MGSWT.rituals.keys.travel
            end,
            function(context)
                MGSWT:debug('Performing ritual %s', context:ritual():ritual_key())
                local performing_faction = context:performing_faction()
                local ritual = context:ritual() -- ACTIVE_RITUAL_SCRIPT_INTERFACE

                local target_x, target_y = cm:find_valid_spawn_location_for_character_from_settlement(
                        performing_faction:name(),
                        ritual:ritual_target():get_target_region():name(),
                        false,
                        true,
                        5
                )

                local malaki_str = cm:char_lookup_str(performing_faction:faction_leader())
                cm:teleport_to(malaki_str, target_x, target_y)
                cm:force_character_force_into_stance(malaki_str, 'MILITARY_FORCE_ACTIVE_STANCE_TYPE_MARCH') -- todo can switch stances??
                cm:zero_action_points(malaki_str)
                local engines_level = MGSWT:get_horde_building_level('wh3_dlc25_dwf_spirit_of_grungni_engines')
                local replenish_chance = engines_level * 20
                local roll =cm:random_number()
                MGSWT:debug('Chance to restore action points %d / %d', roll, replenish_chance)
                if roll <= replenish_chance then
                    cm:replenish_action_points(malaki_str)
                    MGSWT:debug('Action points replenished')
                end
                -- todo add a chance to get lost (travel to random location)

                -- subtract ritual cost
                Klissan_CH:faction_resource_mod(performing_faction:name(), MGSWT.rituals.current_ritual.currency_type, -MGSWT.rituals.current_ritual.value)
                MGSWT:debug('Ritual %s completed', context:ritual():ritual_key())
            end,
            true
    )


    core:remove_listener(Klissan_CH:get_listener_name(MGSWT.rituals.keys.reinforce)) -- todo remove?
    core:add_listener(
            Klissan_CH:get_listener_name(MGSWT.rituals.keys.reinforce),
            "RitualCompletedEvent",
            function (context)
                return context:ritual():ritual_category() == "TZEENTCH_RITUAL"
                        and context:ritual():ritual_key() == MGSWT.rituals.keys.reinforce
            end,
            function(context)
                MGSWT:debug('Performing ritual %s', context:ritual():ritual_key())
                local performing_faction = context:performing_faction()
                local ritual = context:ritual() -- ACTIVE_RITUAL_SCRIPT_INTERFACE
                local target_char = cm:char_lookup_str(ritual:ritual_target():get_target_force():general_character())
                MGSWT:debug('Ritual %s target_char %s', context:ritual():ritual_key(), target_char)
                local unit_keys = string.split(MGSWT.rituals.cache.ritual_reinforce.units_str, ',')
                for i=1, #unit_keys do
                    MGSWT:debug('Ritual %s unit  %s', context:ritual():ritual_key(), unit_keys[i])
                    cm:grant_unit_to_character(target_char, unit_keys[i])
                end
                Klissan_CH:faction_resource_mod(performing_faction:name(), MGSWT.rituals.current_ritual.currency_type, -MGSWT.rituals.current_ritual.value)
                MGSWT:debug('Ritual %s completed', context:ritual():ritual_key())
            end,
            true
    )


    core:remove_listener(Klissan_CH:get_listener_name(MGSWT.rituals.keys.scout)) -- todo remove?
    core:add_listener(
            Klissan_CH:get_listener_name(MGSWT.rituals.keys.scout),
            "RitualCompletedEvent",
            function (context)
                return context:ritual():ritual_category() == "TZEENTCH_RITUAL"
                        and context:ritual():ritual_key() == MGSWT.rituals.keys.scout
            end,
            function(context)
                MGSWT:debug('Performing ritual %s', context:ritual():ritual_key())
                local performing_faction = context:performing_faction()
                local ritual = context:ritual() -- ACTIVE_RITUAL_SCRIPT_INTERFACE
                local target_province = ritual:ritual_target():get_target_region():province()
                local scout_building_level = MGSWT:get_horde_building_level('wh3_dlc25_dwf_spirit_of_grungni_support_radius')
                for i=0, target_province:regions():num_items()-1 do
                    local region = target_province:regions():item_at(i)
                    MGSWT:debug('Ritual %s revealing region %s', context:ritual():ritual_key(), region:name())
                    cm:make_region_visible_in_shroud(performing_faction:name(), region:name())
                    if scout_building_level == 4 then
                        cm:apply_effect_bundle_to_region('klissan_malakai_reveal_hidden_armies', region:name(), 1 + 1)
                        MGSWT:debug('Reveling hidden armies in the region as building requirements is satisfied')
                    end
                end
                Klissan_CH:faction_resource_mod(performing_faction:name(), MGSWT.rituals.current_ritual.currency_type, -MGSWT.rituals.current_ritual.value)
                MGSWT:debug('Ritual %s completed', context:ritual():ritual_key())
            end,
            true
    )

    core:remove_listener(Klissan_CH:get_listener_name(MGSWT.rituals.keys.bombardment)) -- todo remove?
    core:add_listener(
            Klissan_CH:get_listener_name(MGSWT.rituals.keys.bombardment),
            "RitualCompletedEvent",
            function (context)
                return context:ritual():ritual_category() == "TZEENTCH_RITUAL"
                        and context:ritual():ritual_key() == MGSWT.rituals.keys.bombardment
            end,
            function(context)
                -- thanks to Zarathustra_the_Godless who showed me how to damage buildings via script
                MGSWT:debug('Performing ritual %s', context:ritual():ritual_key())
                local performing_faction = context:performing_faction()
                local ritual = context:ritual() -- ACTIVE_RITUAL_SCRIPT_INTERFACE
                local target_region = ritual:ritual_target():get_target_region()
                local slot_list = target_region:settlement():slot_list()
                local damage_health_percent = 20 + 15 * MGSWT:get_horde_building_level('wh3_dlc25_dwf_spirit_of_grungni_army_ability_2')
                for i = 0, slot_list:num_items() - 1 do
                    local slot = slot_list:item_at(i)
                    if slot:has_building() then
                        local randomized_damage = cm:random_number(damage_health_percent, math.floor(damage_health_percent / 2))
                        local damaged = math.max(slot:building():percent_health() - randomized_damage, 1)
                        cm:instant_set_building_health_percent(target_region:name(), slot:building():name(), damaged)
                        MGSWT:debug('Target damage %d', damaged)
                    end
                end
                Klissan_CH:faction_resource_mod(performing_faction:name(), MGSWT.rituals.current_ritual.currency_type, -MGSWT.rituals.current_ritual.value)
                MGSWT:debug('Ritual %s completed', context:ritual():ritual_key())
            end,
            true
    )


    core:remove_listener(Klissan_CH:get_listener_name(MGSWT.rituals.keys.ale)) -- todo remove?
    core:add_listener(
            Klissan_CH:get_listener_name(MGSWT.rituals.keys.ale),
            "RitualCompletedEvent",
            function (context)
                return context:ritual():ritual_category() == "TZEENTCH_RITUAL"
                        and context:ritual():ritual_key() == MGSWT.rituals.keys.ale
            end,
            function(context)
                MGSWT:debug('Performing ritual %s', context:ritual():ritual_key())
                local performing_faction = context:performing_faction()
                local ritual = context:ritual() -- ACTIVE_RITUAL_SCRIPT_INTERFACE
                local beer_level = MGSWT:get_horde_building_level('wh3_dlc25_dwf_spirit_of_grungni_beer_hall')
                local strength_level = MGSWT:get_horde_building_level('wh3_dlc25_dwf_spirit_of_grungni_cargo_hold')

                local n_effects = 1 + beer_level
                local custom_bundle = cm:create_new_custom_effect_bundle('klissan_malakai_drink')
                custom_bundle:set_duration(1)
                local drink_effects = MGSWT.rituals.drink.effects
                cm:shuffle_table(drink_effects)
                for i=1, n_effects do
                    local chance_positive = cm:random_number() - 50 -- todo take into account effect pos/neg state+ strength_level * 10
                    local sign = chance_positive >= 0 and 1 or -1
                    local base_random_value = cm:random_number(5) + strength_level
                    custom_bundle:add_effect(drink_effects[i], 'force_to_force_own', sign * base_random_value)
                    MGSWT:debug('Drink effect %s, chance %d, value %d', drink_effects[i], chance_positive, sign * base_random_value)
                end
                cm:apply_custom_effect_bundle_to_force(custom_bundle, context:performing_faction():faction_leader():military_force())
                if MGSWT.malakai_support_army_cqi ~= nil and cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi) then
					cm:apply_custom_effect_bundle_to_force(custom_bundle, cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi))
				end

                Klissan_CH:faction_resource_mod(performing_faction:name(), MGSWT.rituals.current_ritual.currency_type, -MGSWT.rituals.current_ritual.value)
                MGSWT:debug('Ritual %s completed', context:ritual():ritual_key())
            end,
            true
    )

end


function MGSWT:alcoholism()
    core:add_listener(
        Klissan_CH:get_listener_name(MGSWT.rituals.keys.ale),
        "FactionTurnStart",
        function (context)
            return context:faction():name() == MGSWT.faction_name and performing_faction:faction_leader():has_military_force()
        end,
        function(context)
            MGSWT:debug('Drinking!')
            local performing_faction = cm:get_faction(MGSWT.faction_name)
            local beer_level = MGSWT:get_horde_building_level('wh3_dlc25_dwf_spirit_of_grungni_beer_hall')
            local strength_level = MGSWT:get_horde_building_level('wh3_dlc25_dwf_spirit_of_grungni_cargo_hold')

            local n_effects = 1 + beer_level
            local custom_bundle = cm:create_new_custom_effect_bundle('klissan_malakai_drink')
            --custom_bundle:set_duration(1)
            local drink_effects = MGSWT.rituals.drink.effects
            cm:shuffle_table(drink_effects)
            for i=1, n_effects do
                local chance_positive = cm:random_number() - 50 -- todo take into account effect pos/neg state+ strength_level * 10
                local sign = chance_positive >= 0 and 1 or -1
                local base_random_value = cm:random_number(5) + strength_level
                custom_bundle:add_effect(drink_effects[i], 'force_to_force_own', sign * base_random_value)
                MGSWT:debug('Drink effect %s, chance %d, value %d', drink_effects[i], chance_positive, sign * base_random_value)
            end
            local malakai_force = performing_faction:faction_leader():military_force()
            cm:remove_effect_bundle_from_force(custom_bundle:key(), malakai_force:command_queue_index()) -- todo crash?
            cm:apply_custom_effect_bundle_to_force(custom_bundle, malakai_force)

            -- todo make sure effects don't apply twice to support army (via effect copying)
            if MGSWT.malakai_support_army_cqi ~= nil and cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi) then
                cm:remove_effect_bundle_from_force(custom_bundle:key(), MGSWT.malakai_support_army_cqi)
                cm:apply_custom_effect_bundle_to_force(custom_bundle, cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi))
            end
            MGSWT:debug('Drinking completed!')
        end,
        true
    )
end

-- not triggered when loading into it
--core:add_listener(
--	Klissan_CH:get_listener_name('GarrisonAttackedEvent'),
--	"GarrisonAttackedEvent",
--	function (context)
--        return true
--    end,
--	function(context)
--        Klissan_H:inspect_object(context, out)
--	end,
--	true
--)


-- INIT
cm:add_post_first_tick_callback(function()
    MGSWT:init_ritual_cost_mapping()
    MGSWT:init_ritual_listeners()
    MGSWT:alcoholism()
end)


-- todo add new ritual (population boost) using malakai's?