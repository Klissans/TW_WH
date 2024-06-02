--todo wh3_campaign_grudges.lua

--todo UI progress bar bug

grudge_cycle.cycle_time = 1

grudge_cycle.target_grudge_goal = 50000
grudge_cycle.settled_grudges_total = 0

grudge_cycle.share_reward_prefix = "wh3_dlc25_grudge_cycle_share_"

grudge_cycle.share_thresholds = {5, 10, 20, 40, 80, 101}


--grudge_cycle.unit_rewards.repl_chance_per_age_level = 10
--grudge_cycle.unit_rewards.repl_chance_per_share_level = 10
grudge_cycle.unit_rewards = {
	max_units = 2,
	repl_chance_per_age_level = 5,
	repl_chance_per_share_level = 3,
	last_tier_chance_multiplier = 2,
	max_repl_units = 1,
	recruitment_source_pool = 'wh3_dlc25_dwf_book_of_grudges_mercenary_pool',
	group_to_unit_map = {
		["wh3_dlc25_dwf_grudges_quarrellers_1"] = "wh_main_dwf_inf_quarrellers_1_grudge_reward",
		["wh3_dlc25_dwf_grudges_slayers"] = "wh_main_dwf_inf_slayers_grudge_reward",
		["wh3_dlc25_dwf_grudges_grudge_thrower"] = "wh3_dlc25_dwf_art_grudge_thrower_grudge_reward",
		["wh3_dlc25_dwf_grudges_longbeards_1"] = "wh_main_dwf_inf_longbeards_1_grudge_reward",
		["wh3_dlc25_dwf_grudges_hammerers"] = "wh_main_dwf_inf_hammerers_grudge_reward",
		["wh3_dlc25_dwf_grudges_irondrakes_0"] = "wh_main_dwf_inf_irondrakes_0_grudge_reward",
		["wh3_dlc25_dwf_grudges_gyrocopter_1"] = "wh_main_dwf_veh_gyrocopter_1_grudge_reward",
		["wh3_dlc25_dwf_grudges_flame_cannon"] = "wh_main_dwf_art_flame_cannon_grudge_reward",
	},
	group_tiers = {
		{'wh3_dlc25_dwf_grudges_quarrellers_1',  'wh3_dlc25_dwf_grudges_slayers'},
		{'wh3_dlc25_dwf_grudges_grudge_thrower',  'wh3_dlc25_dwf_grudges_longbeards_1'},
		{'wh3_dlc25_dwf_grudges_hammerers',  'wh3_dlc25_dwf_grudges_irondrakes_0'},
		{'wh3_dlc25_dwf_grudges_gyrocopter_1',  'wh3_dlc25_dwf_grudges_flame_cannon'},
	}
}

grudge_cycle.log_to_file = false
grudge_cycle.log_file = '_grudges.klissan.log'

grudge_cycle.log_to_file = Klissan_H:is_file_exist(grudge_cycle.log_file)
if grudge_cycle.log_to_file then
	io.open(grudge_cycle.log_file,"w"):close()
end

function grudge_cycle:debug(fmt, ...)
	local preformat_str = string.format('[[GRUDGES]] [%d] :: ', cm:turn_number())
    local str = preformat_str .. string.format(fmt, unpack(arg))
    out(str)
    if self.log_to_file then -- not efficient but whateever
        local log_file = io.open(self.log_file, "a+")
        log_file:write(str .. '\n')
        log_file:flush()
        io.close(log_file)
    end
end


function grudge_cycle:setup()
	local faction_list = cm:get_factions_by_culture(self.cultures.dwarf)
	local world = cm:model():world()
	local campaign_name = cm:get_campaign_name()
	local starting_grudge_level = 1
	local historical_legendary_region_list = world:lookup_regions_from_region_group(self.historical_region_prefix.."legendary_"..campaign_name)
	local historical_holds_region_list = world:lookup_regions_from_region_group(self.historical_region_prefix.."holds_"..campaign_name)
	local historical_other_region_list = world:lookup_regions_from_region_group(self.historical_region_prefix.."other_"..campaign_name)

	self.historical_regions.legendary = unique_table:region_list_to_unique_table(historical_legendary_region_list):to_table()
	self.historical_regions.holds = unique_table:region_list_to_unique_table(historical_holds_region_list):to_table()
	self.historical_regions.other = unique_table:region_list_to_unique_table(historical_other_region_list):to_table()

	-- Grant starting historical region grudges
	for type, region_list in pairs(self.historical_regions) do
		for _, region_key in ipairs(region_list) do
			local region = cm:get_region(region_key)

			if region:owning_faction():culture() ~= self.cultures.dwarf then
				self:assign_grudges(region, self.factors.historical_settlement[type], self.values.historical_settlement[type], true)
			end
		end
	end

	-- assign starting effect_bundle
	for _, faction in ipairs(faction_list) do
		local faction_name = faction:name()
		if faction:can_be_human() and not faction:is_dead() and not faction:is_rebel() then
			self.cycle_grudges[faction_name] = 0
			self.faction_times[faction_name] = self.cycle_time

			cm:apply_effect_bundle(self.reward_prefix..starting_grudge_level, faction_name, self.cycle_time + 1)
			cm:apply_effect_bundle(self.share_reward_prefix..self:get_faction_settled_grudges_share_level(faction_name), faction_name, self.cycle_time + 1)

			if cm:get_local_faction_name(true) == faction_name then
				common.set_context_value("cycle_grudge_value", self.cycle_grudges[faction_name])
			end
		end
	end


	-- throw starting grudges to various targets
	for faction_key, value in pairs(self.starting_grudges[campaign_name]) do
		local faction = cm:get_faction(faction_key)
		self:assign_grudges(faction, self.factors.faction_actions, value, true)
	end

	for _, faction in ipairs(faction_list) do
		--self:debug('Setting grudge target for %s', faction:name())
		self:set_grudge_target(faction)
		--self:debug('[success] Setting grudge target for %s', faction:name())
	end
	--self:debug('Setting world_grudge_value COntext value')
	common.set_context_value("world_grudge_value", self:get_world_grudges())
end

function grudge_cycle:get_faction_settled_grudges_share(faction_name)
	if self.settled_grudges_total == 0 then
		return 0
	end
	return self.cycle_grudges[faction_name] / self.settled_grudges_total
end


-- returns int in [0, 5]
function grudge_cycle:get_faction_settled_grudges_share_level(faction_name)
	local value = self:get_faction_settled_grudges_share(faction_name) * 100
	for i, th in ipairs(self.share_thresholds) do
		if not (th <= value) then
			return i-1
		end
	end
end

-- TODO remove accumulated grudges of DAWI faction dead if not implemented yet
function grudge_cycle:set_grudge_target(faction, previous_level, value_override)
	local faction_name = faction:name()
	if not self.target_grudge_value[faction_name] then
		self.target_grudge_value[faction_name] = 0
	end

	-- TODO CAn it be different because we update world grudges on each faction turn?
	--self:debug('Setting target for %s ', faction_name)
	self.target_grudge_value[faction_name] = math.max(self.target_grudge_value[faction_name], self:get_world_grudges())
	--self:debug('Target %d is set for faction %s ', self.target_grudge_value[faction_name], faction_name)

	if faction:is_human() then
		if cm:get_local_faction_name(true) == faction_name then
			common.set_context_value("cycle_grudge_target", self.target_grudge_value[faction_name])
			common.set_context_value("cycle_grudge_value", self.cycle_grudges[faction_name])
		end
	end
	--self:debug('Returning from grudge_cycle:set_grudge_target for faction %s ', faction_name)
end


function grudge_cycle:update_settled_grudges_total()
	local accumulated_grudges = 0
	for _, k in pairs(Klissan_H:get_key_sorted(self.cycle_grudges)) do
		local faction = cm:get_faction(k)
		if not faction:is_dead() and not faction:is_rebel() then
			accumulated_grudges = accumulated_grudges + self.cycle_grudges[k]
		end
	end
	self.settled_grudges_total = accumulated_grudges
	return accumulated_grudges
end


function grudge_cycle:update_cycle_tracker(faction_name)
	self:update_settled_grudges_total()
	local percentage = 0
	if self.cycle_grudges[faction_name] then

		if self.target_grudge_value[faction_name] > 0 then
			percentage = math.floor(self.settled_grudges_total / self.target_grudge_value[faction_name] * 100)
		end

		out.design(faction_name.." - "..self.settled_grudges_total.." / "..self.target_grudge_value[faction_name].." - Setting grudge % to: "..percentage)

		-- reset the % to 0 to the min value of 0 before assigning the updated value.
		cm:faction_add_pooled_resource(faction_name, self.resources.cycle_percent, self.factors.settled, -100)
		cm:faction_add_pooled_resource(faction_name, self.resources.cycle_percent, self.factors.settled, percentage)

		if self.cycle_grudges[cm:get_local_faction_name(true)] then
			common.set_context_value("cycle_grudge_value", self.cycle_grudges[cm:get_local_faction_name(true)])
			common.set_context_value("world_grudge_value", self:get_world_grudges())
		end
	end
	return percentage
end


function grudge_cycle:get_mecenary_count_in_reward_pool(faction_key, main_unit_key)
	    local ucount = cco('CcoCampaignRoot', 'CampaignRoot'):Call(string.format([=[
        (
            faction = CampaignRoot.FactionList.FirstContext(FactionRecordContext.Key == '%s'),
            pool = faction.MercenaryPoolContext,
            unit = pool.MercenaryPoolUnitList.FirstContext(MainUnitRecordContext.Key == '%s')
        ) => unit.AvailableUnitCount
    ]=], faction_key, main_unit_key))
    return ucount
end
-- common_level gives rewards from 1 to 4 with 5 doubling chances
-- tier - reward tiers matching common_level when available
-- share_level - [0, 5] flat bonus to chance based on particular dawi faction performance
function grudge_cycle:get_reward_chance(common_level, share_level, tier)
	local chance_per_tier = self.unit_rewards.repl_chance_per_age_level * (common_level == 5 and self.unit_rewards.last_tier_chance_multiplier or 1)
	local share_chance = share_level * self.unit_rewards.repl_chance_per_share_level
	local repl_chance = (common_level - tier + 1) * chance_per_tier + share_chance
	return repl_chance
end


function grudge_cycle:get_current_grudge_level(faction_key)
	local faction = cm:get_faction(faction_key)
	local grudge_cycle_value = faction:pooled_resource_manager():resource(self.resources.cycle_percent):value() -- self.settled_grudges_total --
	for level, ranges in ipairs(self.ranges) do
		if grudge_cycle_value >= ranges.min and grudge_cycle_value <= ranges.max then
			return level
		end
	end
end

-- main loop
function grudge_cycle:cycle_timer()
	core:remove_listener('GrudgeCycleCounter')
	core:add_listener(
		"GrudgeCycleCounter",
		"FactionTurnStart",
		function(context)
			local faction = context:faction()
			return faction:culture() == self.cultures.dwarf and faction:can_be_human() and not faction:is_dead() and not faction:is_rebel()
		end,
		function(context)
			local faction = context:faction()
			local faction_key = faction:name()

			self:update_settled_grudges_total()
			self:set_grudge_target(faction)
			local percentage = self:update_cycle_tracker(faction_key)

			local level = self:get_current_grudge_level(faction_key)
			local share_level = self:get_faction_settled_grudges_share_level(faction_key)
			for i = 0, 5 do
				cm:remove_effect_bundle(self.reward_prefix..i, faction_key)
				cm:remove_effect_bundle(self.share_reward_prefix..i, faction_key)
			end
			-- effect bundle duration comes through as 1 less than the cycle time when applied so adding
			cm:apply_effect_bundle(self.reward_prefix..level, faction_key, self.cycle_time + 1)
			cm:apply_effect_bundle(self.share_reward_prefix..share_level, faction_key, self.cycle_time + 1)

			-- in this implementation all dawi start at 1 common level
			for tier = 1, #self.unit_rewards.group_tiers do
				for _, group_reward_key in ipairs(self.unit_rewards.group_tiers[tier]) do
					local unit_key = self.unit_rewards.group_to_unit_map[group_reward_key]
					local repl_chance = 0
					if tier <= level then
						repl_chance = self:get_reward_chance(level, share_level, tier)
					end
					local current_count = self:get_mecenary_count_in_reward_pool(faction_key, unit_key)
					local new_count = math.min(current_count + ((cm:random_number() <= repl_chance) and 1 or 0), self.unit_rewards.max_units)
					cm:add_unit_to_faction_mercenary_pool(
							faction, unit_key, self.unit_rewards.recruitment_source_pool,
							new_count, repl_chance, self.unit_rewards.max_units, self.unit_rewards.max_repl_units,
							faction:name(), faction:subculture(), '', false, group_reward_key)
				end
			end

			--local cycle_grudges_str = ''
			--for _, k in pairs(Klissan_H:get_key_sorted(self.cycle_grudges)) do
			--	cycle_grudges_str = cycle_grudges_str.. ' | '..k..' : '..self.cycle_grudges[k]
			--end
			--self:debug(cycle_grudges_str)
			self:debug('Cycle for %s | FCG=%s, SGT=%s, WG=%s, TG=%s | lvls %s/%s | FS=%s, TS=%s',
					faction_key,
					tostring(self.cycle_grudges[faction_key]), tostring(self.settled_grudges_total), tostring(self:get_world_grudges()), tostring(self.target_grudge_value[faction_key]),
					tostring(level), tostring(share_level),
					tostring(self:get_faction_settled_grudges_share(faction_key)),  tostring(percentage/100.0))
		end,
		true
	)
end
