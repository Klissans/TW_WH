return
local malakai_faction = MGSWT.faction
local mx, my = Klissan_CH:get_logical_position(malakai_faction:faction_leader())
local tx, ty = Klissan_CH:get_logical_position(cm:get_region('wh3_main_combi_region_worlds_edge_archway'):settlement())
local distance = math.sqrt(math.pow(math.abs(mx-tx), 2) + math.pow(math.abs(my-ty), 2))

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

--- chain's Level is 0-based even in UI it's 1-based
[=[
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
        units_from_primary_str = primary_unit.Key + GetIfElse(extra_unit != '', ',' + extra_unit.Key, '')
        military_level_slots = malakai_horde.BuildingSlotList
            .Filter(BuildingContext.BuildingLevelRecordContext.BuildingChainRecordContext.BuildingSetContext.Key == 'wh3_dlc25_set_dwarf_spirit_of_grungni_recruitment')
            .Transform(BuildingContext.BuildingLevelRecordContext),
        selected_units = military_level_slots
            .Transform((x, ul = x.UnitList(malakai), r = TrueRandomInRange(0, ul.Size-1)) => {ul[r]}),
        total_cost = selected_units.Sum(Cost),
        result_str = Format('%S%S|%d', units_from_primary_str, selected_units.JoinString(Key, ','), RoundFloat(total_cost + primary_unit.Cost + GetIf(extra_unit != '', extra_unit.Cost))
    ) => result_str
]=]
