--- fix for legendary grudges
function legendary_grudges:setup_destroy_factions_mission_condition(mission_manager, target_faction_list, add_to_primary)
	local add_to_primary = add_to_primary or nil
	mission_manager:add_new_objective("DESTROY_FACTION", add_to_primary)
	for _,v in ipairs(target_faction_list) do
		mission_manager:add_condition("faction " .. v);
	end
	mission_manager:add_condition("confederation_valid")
end