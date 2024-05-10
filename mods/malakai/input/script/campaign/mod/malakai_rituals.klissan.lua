--todo diplomatic manipulation vs ritual?

--to enable tzeentch ritual's panel:
-- db/ui_features_to_factions_tables
-- db/campaign_groups_tables
-- db/campaign_group_members_tables
-- db/campaign_group_members_criteria_cultures_tables
-- db/campaign_features_tables

-- TO ADD RITUAL
-- db/rituals_tables
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
        reinforce = 'klissan_malakai_supplies_ritual',
        bombardment = 'klissan_malakai_bombard_ritual',
        ale = 'klissan_malakai_ale_ritual',
    },
    cost_mapping = nil,
    cost_multipliers = {
        travel_distance = 5,
        reinforce_discount = 0.5
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


function MGSWT:get_ritual_reinforce_units_cost_pair()
    local result_str =  self.croot:Call([=[
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
        cm:teleport_to(malaki_str, target_x, target_y) -- todo applies tresspasing wtf
        cm:zero_action_points(malaki_str)
        cm:force_character_force_into_stance(malaki_str, 'MILITARY_FORCE_ACTIVE_STANCE_TYPE_MARCH') -- todo can switch stances??
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


-- INIT
cm:add_post_first_tick_callback(function()
    MGSWT:init_ritual_cost_mapping()
end)