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
-- Bombardment (force, settlement in range of TSoG)
-- Scout (targeted adjacent province or all adjacent regions, hmmm)
-- Deliever Supplies (Target non-hostile Settlement in region) [heal garrison, boost growth]

MGSWT.rituals = { -- should match db keys
    keys = {
        travel = 'klissan_malakai_travel_ritual'
    },
    cost_mapping = nil,
    cost_multipliers = {
        travel_distance = 5
    },

     -- it's set via UI callbacks
    current_ritual = {
        is_valid_target = false, -- should be managed by ui only
        key = nil,
        target_type = nil,
        target_key = nil,
        currency_type = nil,
        value = nil,
    }
}


function MGSWT:init_ritual_cost_mapping()
    self.rituals.cost_mapping = {}
    self.rituals.cost_mapping[self.rituals.keys.travel] = function ()
        return math.ceil(self.rituals.cost_multipliers.travel_distance * self:get_travel_distance())
    end
end


function MGSWT:get_ritual_cost()
    local ritual_key = self:get_targeting_ritual_key() -- :gsub('_ritual$', '') -- appended in cco
    local ritual_cost = self.rituals.cost_mapping[ritual_key]()
    self:debug('Ritual cost %s is %d', ritual_key, ritual_cost)
    return ritual_cost
end


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

        if ritual:ritual_target():target_type() ~= 'REGION' then
            MGSWT:error('Wrong target for ritual : ' .. context:ritual():ritual_key())
            return
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
        cm:force_character_force_into_stance(malaki_str, 'MILITARY_FORCE_ACTIVE_STANCE_TYPE_MARCH') -- todo can switch stances??
        -- todo add a chance to get lost (travel to random location)

        -- subtract ritual cost
        Klissan_CH:faction_resource_mod(performing_faction:name(), MGSWT.rituals.current_ritual.currency_type, -MGSWT.rituals.current_ritual.value)
        MGSWT:debug('Ritual %s completed', context:ritual():ritual_key())
	end,
	true
)


-- INIT
cm:add_post_first_tick_callback(function()
    MGSWT:init_ritual_cost_mapping()
end)