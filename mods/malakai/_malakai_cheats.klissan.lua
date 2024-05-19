return
local malakai_faction = MGSWT.faction
local mx, my = Klissan_CH:get_logical_position(malakai_faction:faction_leader())
local tx, ty = Klissan_CH:get_logical_position(cm:get_region('wh3_main_combi_region_worlds_edge_archway'):settlement())
local distance = math.sqrt(math.pow(math.abs(mx-tx), 2) + math.pow(math.abs(my-ty), 2))


---
---CCO IsTransportedArmy
--- ForceType == 'SUPPORT_ARMY'


---


--local payload_builder = cm:create_payload()
--local transported_force_key, is_removal = 'malakai_support_army', false
--payload_builder:transported_military_force(transported_force_key, is_removal)



-----
-- no way to enable upkeep w/o breaking waagh?
-- this only adds this army ro supply lines (supposedly)
local upkeep_penalty_effect_bundle_key = "wh3_main_bundle_force_additional_army_upkeep"
local upkeep_value = 1 -- easy
if cm:model():campaign_name_key() == "wh3_main_chaos" then
	if difficulty == 0 then
		upkeep_value = 1 -- normal
	elseif difficulty == -1 then
		upkeep_value = 2 -- hard
	elseif difficulty == -2 then
		upkeep_value = 4 -- very hard
	elseif difficulty == -3 then
		upkeep_value = 4 -- legendary
	end;
end
local effect_bundle = cm:create_new_custom_effect_bundle(upkeep_penalty_effect_bundle_key)
effect_bundle:set_duration(0)
effect_bundle:add_effect("wh_main_effect_force_all_campaign_upkeep_hidden", "force_to_force_own_factionwide", upkeep_value)
current_mf = cm:get_character_by_cqi(993):military_force()
cm:apply_custom_effect_bundle_to_force(effect_bundle, current_mf)

------

local mf = cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi)
cm:kill_character(cm:char_lookup_str(mf:general_character()), false) -- ctd on support army
cm:embed_agent_in_force(cm:get_character_by_cqi(996), mf)
console_print(''..mf:general_character():command_queue_index())
cm:spawn_agent_at_military_force(MGSWT.faction, mf, 'engineer', 'wh_main_dwf_master_engineer')
local char = cm:replace_general_in_force(mf, 'wh_dlc06_dwf_runelord') -- 'wh_main_dwf_master_engineer'
console_print('is_failed?'..tostring(char:is_null_interface()))





--to do how to log characters (name) command_queue_index
--self:debug('Travel Distance -> (%s,%s) = %f', target_type, target_key, distance)
--console_print(''..MGSWT:get_travel_distance())


-- CcoCampaignBuildingSlot has BuildingCOntext for *constructed* Building and ConstructionItemContext for Building being constructed in this slot
'wh3_dlc25_dwf_spirit_of_grungni_support_radius'
[=[
    (
        malakai_faction = CampaignRoot.FactionList.FirstContext(FactionRecordContext.Key == 'wh3_dlc25_dwf_malakai'),
        malakai = malakai_faction.FactionLeaderContext,
        malakai_army = malakai.MilitaryForceContext,
        malakai_horde = malakai_army.HordeContext,
        building_chain_key = 'wh3_dlc25_dwf_spirit_of_grungni_support_radius',
        slot_with_desired_building_chain = malakai_horde.BuildingSlotList.FirstContext(BuildingContext.BuildingLevelRecordContext.BuildingChainRecordContext.Key == building_chain_key),
        building = slot_with_desired_building_chain.BuildingContext,
        radius_effect = building.EffectList.FirstContext(EffectKey == 'wh3_dlc25_effect_force_stat_support_radius')
    ) => GetIfElse(IsContextValid(radius_effect), radius_effect.Value, 0)
]=]

--ContextList
--CcoBuildingLevelRecord
--UnitList(Buildings.StoredSettlementOrCharacter, PlayersFaction)
--(meta-event) CampaignLocalFactionChanged

--ContextList
--CcoBuildingLevelRecord
--AgentList


-- BuildingChainRecordContext.TechnologyCategory == 'military' is true for non-recruitment buildings
cm:grant_unit_to_character(cm:char_lookup_str(cm:get_local_faction():faction_leader()), 'wh_main_dwf_cha_master_engineer_0') -- will be spawned as  unit not hero
console_print(cm:char_lookup_str(cm:get_local_faction():faction_leader()))

cm:grant_unit_to_character('character_cqi:195', 'wh_main_dwf_cha_master_engineer_0')
cm:join_garrison('character_cqi:992', 'wh3_main_combi_region_the_lost_palace')
--- chain's Level is 0-based even in UI it's 1-based



----------------


    local ritual_key = 'klissan_malakai_support_army_ritual'
    local faction = cm:get_faction('wh3_main_tze_oracles_of_tzeentch')
    local ritual_setup = cm:create_new_ritual_setup(faction, ritual_key)
    local ritual_target = ritual_setup:target()
    ritual_target:set_target_force(faction:military_force_list():item_at(0))
    console_print(tostring(ritual_target:is_force_valid_target()))
    cm:perform_ritual_with_setup(ritual_setup)

'MILITARY_FORCE_ACTIVE_STANCE_TYPE_TUNNELING'
cm:force_character_force_into_stance(cm:char_lookup_str(cm:get_character_by_cqi(895)), 'MILITARY_FORCE_ACTIVE_STANCE_TYPE_TUNNELING')




		local general_support_army_lookup_str = cm:char_lookup_str(cm:get_military_force_by_cqi(103):general_character())
cm:grant_unit_to_character(general_support_army_lookup_str, 'wh_main_dwf_cha_master_engineer_0')


console_print(''..bm:reinforcements():reinforcement_army_count())

local rarmy = bm:reinforcements():reinforcement_army(1):army()
local unit = rarmy:units():item(1)
unit:deploy_reinforcement(true)

local sunit = script_unit:new(unit, 'runit')
sunit:deploy_reinforcement()
sunit:respawn_in_start_location()
sunit:teleport_to_location(battle_vector:new(0,0,0), 1, 1)

local ruc = rarmy:create_unit_controller()
ruc:add_units(unit)
ruc:take_control()
ruc:teleport_to_location(battle_vector:new(0,0,0), 1, 1)
console_print(''..unit:unique_ui_id())

local armies = bm:alliances():item(1):armies()
for i=0, armies:count()-1 do
	local army = armies:item(i+1)
	console_print(tostring(army:is_reinforcement_army()))
	console_print(army:get_reinforcement_target_army():is_reinforcement_army())
end






