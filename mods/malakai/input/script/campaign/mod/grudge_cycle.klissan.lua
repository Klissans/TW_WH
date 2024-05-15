--todo wh3_campaign_grudges.lua

--todo UI progress bar bug

grudge_cycle.cycle_time = 1

grudge_cycle.target_grudge_goal = 50000
grudge_cycle.settled_grudges_total = 0
grudge_cycle.unit_roll_base_chance = 5

grudge_cycle.share_reward_prefix = "wh3_dlc25_grudge_cycle_"


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
		if faction:can_be_human() then
			self.cycle_grudges[faction_name] = 0
			self.faction_times[faction_name] = self.cycle_time

			cm:apply_effect_bundle(self.reward_prefix..starting_grudge_level, faction_name, self.cycle_time + 1)
			cm:apply_effect_bundle(self.reward_prefix..self:get_faction_settled_grudges_share_level(faction_name), faction_name, self.cycle_time + 1)

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
		self:set_grudge_target(faction)
	end
	common.set_context_value("world_grudge_value", self:get_world_grudges())
end

function grudge_cycle:get_faction_settled_grudges_share(faction_name)
	if self.settled_grudges_total == 0 then
		return 0
	end

	return self.cycle_grudges[faction_name] / self.settled_grudges_total
end

function grudge_cycle:get_faction_settled_grudges_share_level(faction_name)
	return math.floor(self:get_faction_settled_grudges_share(faction_name) * 100 / 20)
end

-- TODO remove accumulated grudges of DAWI faction dead if not implemented yet
function grudge_cycle:set_grudge_target(faction, previous_level, value_override)
	local faction_name = faction:name()
	if not self.target_grudge_value[faction_name] then
		self.target_grudge_value[faction_name] = 0
	end

	-- TODO CAn it be different because we update world grudges on each faction turn?
	self.target_grudge_value[faction_name] = math.max(self.target_grudge_value[faction_name], self:get_world_grudges())

	if faction:is_human() then
		if cm:get_local_faction_name(true) == faction_name then
			common.set_context_value("cycle_grudge_target", self.target_grudge_value[faction_name])
			common.set_context_value("cycle_grudge_value", self.cycle_grudges[faction_name])
		end
	end
end


function grudge_cycle:update_settled_grudges_total()
	local accumulated_grudges = 0
	for _, k in pairs(Klissan_H:get_key_sorted(self.cycle_grudges)) do
		accumulated_grudges = accumulated_grudges + self.cycle_grudges[k]
	end
	self.settled_grudges_total = accumulated_grudges
	return accumulated_grudges
end



function grudge_cycle:update_cycle_tracker(faction_name)
	if self.cycle_grudges[faction_name] then
		local percentage = 0

		if self.target_grudge_value[faction_name] > 0 then
			percentage = math.floor(self.settled_grudges_total / self.target_grudge_value[faction_name] * 100)
		end

		out.design(faction_name.." - "..self.cycle_grudges[faction_name].." / "..self.target_grudge_value[faction_name].." - Setting grudge % to: "..percentage)

		-- reset the % to 0 to the min value of 0 before assigning the updated value.
		cm:faction_add_pooled_resource(faction_name, self.resources.cycle_percent, self.factors.settled, -100)
		cm:faction_add_pooled_resource(faction_name, self.resources.cycle_percent, self.factors.settled, percentage)

		if self.cycle_grudges[cm:get_local_faction_name(true)] then
			common.set_context_value("cycle_grudge_value", self.cycle_grudges[cm:get_local_faction_name(true)])
			common.set_context_value("world_grudge_value", self:get_world_grudges())
		end
	end
end


-- main loop
function grudge_cycle:cycle_timer()
	core:add_listener(
		"GrudgeCycleCounter",
		"FactionTurnStart",
		function(context)
			local faction = context:faction()
				if faction:culture() == self.cultures.dwarf and faction:can_be_human() then
					return true
				end
			return false
		end,
		function(context)
			local faction = context:faction()
			local faction_key = faction:name()

			if not faction:can_be_human() then
				return
			end

			self:update_settled_grudges_total()
			local level = self:get_current_grudge_level(faction_key)
			local share_level = self:get_faction_settled_grudges_share_level(faction_name)
			for i = 0, 5 do
				cm:remove_effect_bundle(self.reward_prefix..i, faction_key)
				cm:remove_effect_bundle(self.share_reward_prefix..i, faction_key)
			end
			-- effect bundle duration comes through as 1 less than the cycle time when applied so adding
			cm:apply_effect_bundle(self.reward_prefix..level, faction_key, self.cycle_time + 1)
			cm:apply_effect_bundle(self.share_reward_prefix..share_level, faction_key, self.cycle_time + 1)

			self:set_grudge_target(faction, level)

			for i = 0, level do
				-- todo fix this, failed on campaign start
				for k, unit in ipairs(self.settler_units[i]) do
					local random_roll = cm:random_number()
					-- TODO it seems units are in each pool so we can just use base chance
					if random <= (level - i + 1) * self.unit_roll_base_chance then
						cm:add_units_to_faction_mercenary_pool(faction:command_queue_index(), unit, 1)
					end
				end
			end

			self:update_cycle_tracker(faction_key) -- needed?
		end,
		true
	)
end