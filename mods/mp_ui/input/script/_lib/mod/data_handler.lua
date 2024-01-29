require('helpers')
out("[Battle Data Dumper Mod] loaded")

---@class battle_data_dumper
local battle_data_dumper = {
    _dumps_folder = '_replay_dumps',
    _replay_name = '',
    _is_dump_battle_units_during_battle = false,
    _track_units = {},

    _dump_tables = {
        info = {},
        alliances = {},
        armies = {},
        reinforcement_armies = {},
        units = {},
        battle_alliances = {},
        battle_armies = {},
        battle_units = {},
        -- summary = {},
    }
}

function battle_data_dumper:tracking_callback(f, name)
    self:out('Init callback ' .. name)
    local tm = core:get_static_object("timer_manager")
    local timeout = bm:model_tick_time_ms()
    return function()
        tm:repeat_callback(function()
            f(battle_data_dumper)
        end, timeout, name)
    end
end

function battle_data_dumper:init()
    self:out('Entering init')
    if not bm:is_replay() then
        self:out('not a replay battle')
        return
    end

    local do_dumps_file = "_enable_replay_dumps"
    self:out('Checking if enabling dumps file exists')
    if not is_file_exist(do_dumps_file) then
        self:out(do_dumps_file .. " doesn't exist")
        return
    end

    self._replay_name = self:get_replay_name()

    -- check if marker file exists
    self:out('Checking if dump exists ' .. self._replay_name)
    if is_file_exist(self:get_full_path('')) then
        self:out("Replay Dump already exists " .. self._replay_name)
        return
    end

    self:out("Replay data dumping is enabled")
    self:collecting_static_info();

    bm:register_phase_change_callback("Deployed", self:tracking_callback(battle_data_dumper.track_battle_alliances, "track_alliances_callback"))
    bm:register_phase_change_callback("Deployed", self:tracking_callback(battle_data_dumper.track_battle_armies, "track_armies_callback"))
    bm:register_phase_change_callback("Deployed", self:tracking_callback(battle_data_dumper.track_battle_units, "track_units_callback"))
    bm:register_phase_change_callback("Complete", function()
        battle_data_dumper:dump_all_tables()
    end)
end

function battle_data_dumper:get_replay_name()
    local battleRoot = cco("CcoBattleRoot", "BattleRoot")
    local replay_name = battleRoot:Call('AllianceList.JoinString(ArmyList.JoinString(PlayerName + "(" + FactionContext.Key + ")", "&"), "_vs_") ')
    return replay_name:gsub(' ', '_'):gsub('\\', '_'):gsub('/', '_'):gsub(':', '_'):gsub('*', '_'):gsub('?', '_'):gsub('"', '_'):gsub('<', '_'):gsub('>', '_'):gsub('|', '_')
end

function battle_data_dumper:get_full_path(filename)
    return self._dumps_folder .. '/' .. self._replay_name .. '_' .. filename
end

function battle_data_dumper:dump_all_tables()
    self:out('Dumping tables')
    local table_names = get_key_sorted(self._dump_tables)
    for _, tname in pairs(table_names) do
        if not (self._is_dump_battle_units_during_battle and tname == 'battle_units') then
            self:write_dump(tname)
        end
    end

    -- Create a marker file
    local file = io.open(self:get_full_path(''), "w+")
    io.close(file)

    self:out('Succesfully dumped')
end

function battle_data_dumper:write_dump(table_name)
    local sep = '|'
    local table_to_dump = self._dump_tables[table_name]
    local fpath = self:get_full_path(table_name .. '.csv')
    self:out('DEBUG tname:' .. table_name)
    self:out('DEBUG tsize:' .. table_size(table_to_dump))
    self:out('Writing Dump of ' .. table_name .. ' Rows #' .. table_size(table_to_dump) .. ' Cols #' .. table_size(table_to_dump[1]) .. ' to ' .. fpath)

    local replay_dump_file = io.open(fpath, "w+")
    if not replay_dump_file then
        self:out("FAILED TO CREATE FILE " .. table_name)
        return
    end
    local column_names = get_key_sorted(table_to_dump[1])

    local columns_row = table.concat(column_names, sep)
    self:out(columns_row)
    replay_dump_file:write(columns_row .. '\n')

    for i = 1, #table_to_dump do
        local dump_s = tostring(table_to_dump[i][column_names[1]])
        for k = 2, #column_names do
            local key = column_names[k]
            dump_s = dump_s .. '|' .. tostring(table_to_dump[i][key])
        end
        replay_dump_file:write(dump_s .. '\n')
    end

    replay_dump_file:flush()
    io.close(replay_dump_file)
end

-- function get_battle_summary()
--     local alliances_table = self._dump_tables['alliances']
--     local alliances = bm:alliances()
--     for i=1, alliances:count() do
--     end
-- end


function battle_data_dumper:out(s)
    out('[Battle Data Dumper Mod]: ' .. s)
end

function battle_data_dumper:collecting_static_info()
    self:out('Collecting static info')
    self:get_battle_info()
    self:iter_over_alliances()

    -- create empty table
    if bm:reinforcements():reinforcement_army_count() == 0 then
        self:out('Emulating table')
        local nilinfo = {}
        for _, k in pairs(get_key_sorted(self._dump_tables['armies'][1])) do
            nilinfo[k] = ''
        end
        table.insert(self._dump_tables['reinforcement_armies'], nilinfo)
        self:out('Emulated reinforcements table')
    end
end

function battle_data_dumper:get_battle_info()
    local cco_br = cco('CcoBattleRoot', 'BattleRoot')
    local info = {}
    info['IsDomination'] = cco_br:Call('IsDomination')
    info['IsSiege'] = cco_br:Call('IsSiege')
    info['IsCampaignBattle'] = cco_br:Call('IsCampaignBattle')
    self:out('Collected battle info')
    table.insert(self._dump_tables['info'], info)
end

function battle_data_dumper:track_battle_alliances()
    self:out("Gathering battle ALLIANCES data " .. ' entries# ' .. table_size(self._dump_tables['battle_alliances']))
    local alliances = bm:alliances()
    for i = 1, alliances:count() do
        self:get_battle_alliance_info(i)
    end
end

function battle_data_dumper:track_battle_armies()
    self:out("Gathering battle ARMIES data " .. ' entries# ' .. table_size(self._dump_tables['battle_armies']))
    local alliances = bm:alliances()
    for i = 1, bm:alliances():count() do
        local armies = bm:alliances():item(i):armies()
        for j = 1, armies:count() do
            local army = armies:item(j)
            self:get_battle_army_info(army)
        end
        for r = 1, bm:reinforcements():reinforcement_army_count() do
            local reinf_army = bm:reinforcements():reinforcement_army(r):army()
            -- self:get_battle_army_info(reinf_army, info)    
        end
    end

end

function battle_data_dumper:track_battle_units()
    self:out("Gathering battle UNITS data " .. ' entries# ' .. table_size(self._dump_tables['battle_units']))
    -- dump armies
    local alliances = bm:alliances()
    for i = 1, bm:alliances():count() do
        local armies = bm:alliances():item(i):armies()
        for j = 1, armies:count() do
            local army = armies:item(j)
            local units = army:units()
            for k = 1, units:count() do
                self:get_battle_unit_info(units:item(k), false)
            end
        end
    end

    --dump reinforcement armies
    for r = 1, bm:reinforcements():reinforcement_army_count() do
        local reinf_army = bm:reinforcements():reinforcement_army(r):army()
        local reinf_units = reinf_army:units()
        for k = 1, reinf_units:count() do
            self:get_battle_unit_info(reinf_units:item(k), true)
        end
    end
end

function battle_data_dumper:iter_over_alliances()
    local cco_br = cco('CcoBattleRoot', 'BattleRoot')
    local alliances_table = self._dump_tables['alliances']
    local alliances = bm:alliances()
    for i = 1, alliances:count() do
        self:out('Collecting Alliance #' .. i)
        local alliance = alliances:item(i)
        local cco_alliance = cco_br:Call('AllianceList.At(' .. i - 1 .. ')')

        local info = {}
        -- info['i'] = i
        info['is_attacker'] = alliance:is_attacker()

        info['NumEntitiesInitial'] = cco_alliance:Call('NumEntitiesInitial()')
        info['NumEntities'] = cco_alliance:Call('NumEntities()')
        info['NumArmies'] = cco_alliance:Call('NumArmies()')
        info['CpKillScore'] = cco_alliance:Call('CpKillScore()')
        info['StartingTickets'] = cco_alliance:Call('StartingTickets()')
        info['TicketsIncomePerSecond'] = cco_alliance:Call('TicketsIncomePerSecond()')
        info['TicketsRemaining'] = cco_alliance:Call('TicketsRemaining()')
        info['Id'] = cco_alliance:Call('Id()')
        info['DoesKeepScore'] = cco_alliance:Call('DoesKeepScore()')
        info['IsPlayersAlliance'] = cco_alliance:Call('IsPlayersAlliance()')
        info['IsDefender'] = cco_alliance:Call('IsDefender()')
        info['WillWinOnTimeout'] = cco_alliance:Call('WillWinOnTimeout()')

        table.insert(alliances_table, info)
        self:iter_over_armies(alliance, info['Id'])
    end
    self:iter_over_reinforcement_armies()
end

function battle_data_dumper:get_battle_alliance_info(i)
    local cco_br = cco('CcoBattleRoot', 'BattleRoot')
    local alliance = bm:alliances():item(i)
    local cco_alliance = cco_br:Call('AllianceList.At(' .. i - 1 .. ')')

    local info = {}
    info['time'] = bm:time_elapsed_ms()
    info['NumEntities'] = cco_alliance:Call('NumEntities()')
    info['CpKillScore'] = cco_alliance:Call('CpKillScore()')
    info['TicketsIncomePerSecond'] = cco_alliance:Call('TicketsIncomePerSecond()')
    info['TicketsRemaining'] = cco_alliance:Call('TicketsRemaining()')
    info['Id'] = cco_alliance:Call('Id()')

    table.insert(self._dump_tables['battle_alliances'], info)
end

function battle_data_dumper:save_reinforcement_army_info(army, alliance_id)
    self:out("SAving reinforcemet army info")
    local reinforcement_armies_table = self._dump_tables['reinforcement_armies']
    local info = {}
    -- info['i'] = i
    info['faction_key'] = army:faction_key()
    info['subculture_key'] = army:subculture_key()
    info['flag_path'] = army:flag_path()
    -- info['is_rebel'] = army:is_rebel()
    -- info['is_player_controlled'] = army:is_player_controlled()
    -- info['army_handicap'] = army:army_handicap()
    info['is_reinforcement_army'] = army:is_reinforcement_army()
    info['num_reinforcement_units'] = army:num_reinforcement_units()
    info['unique_id'] = army:unique_id()
    info['alliance_id'] = alliance_id
    table.insert(reinforcement_armies_table, info)
    self:out("SAving reinforcemet army info - Complete")
end

function battle_data_dumper:save_army_info(army, alliance_id)
    local armies_table = self._dump_tables['armies']

    local cco_br = cco('CcoBattleRoot', 'BattleRoot')
    local cco_army = nil
    -- if army:is_reinforcement_army() then
    --     cco_army = cco_br:Call('ReinforcementArmyList.FirstContext(UniqueID=="' .. army:unique_id() .. '")')
    -- else
    cco_army = cco_br:Call('ArmyList.FirstContext(UniqueID==' .. army:unique_id() .. ')')
    local cco_faction = cco_army:Call('FactionContext')

    local info = {}
    -- info['i'] = i
    info['faction_key'] = army:faction_key()
    info['subculture_key'] = army:subculture_key()
    info['flag_path'] = army:flag_path()
    -- info['is_rebel'] = army:is_rebel()
    -- info['is_player_controlled'] = army:is_player_controlled()
    -- info['army_handicap'] = army:army_handicap()
    info['is_reinforcement_army'] = army:is_reinforcement_army()
    info['num_reinforcement_units'] = army:num_reinforcement_units()
    info['unique_id'] = army:unique_id()
    info['alliance_id'] = alliance_id
    --army:has_currency(string currency type)
    --army:currency_amount(string currency type)

    -- info['UniqueID'] = cco_army:Call('UniqueID()')
    -- info['IsHuman'] = cco_army:Call('IsHuman()')
    info['NumUnits'] = cco_army:Call('NumUnits()')
    -- info['FactionContext'] = cco_army:Call('FactionContext()')
    info['HasReignOfChaos'] = cco_army:Call('HasReignOfChaos()')
    -- info['MaxUnitsCanControl'] = cco_army:Call('MaxUnitsCanControl()')
    -- info['WindsOfMagicPoolContext'] = cco_army:Call('WindsOfMagicPoolContext()')
    info['NumEntitiesInitial'] = cco_army:Call('NumEntitiesInitial()')
    info['NumEntities'] = cco_army:Call('NumEntities()')
    info['CanPerformCataclysmAbility'] = cco_army:Call('CanPerformCataclysmAbility()')
    -- info['NumTotalUnits'] = cco_army:Call('NumTotalUnits()')
    -- info['ArmyAbilitiesList'] = cco_army:Call('ArmyAbilitiesList()')
    -- info['AiStatsModifier'] = cco_army:Call('AiStatsModifier()')
    -- info['NumReinforcements'] = cco_army:Call('NumReinforcements()')
    -- info['FormationList'] = cco_army:Call('FormationList()')
    info['HasDaemonFeature'] = cco_army:Call('HasDaemonFeature()')
    info['PrimaryColour'] = cco_army:Call('PrimaryColour()')
    info['MurderousProwessThresh'] = cco_army:Call('MurderousProwessThresh()')
    -- info['ArmyWideEffects'] = cco_army:Call('ArmyWideEffects()')
    info['AllianceColour'] = cco_army:Call('AllianceColour()')
    info['PlayerName'] = cco_army:Call('PlayerName()')
    info['ArmyAbilityCurrency'] = cco_army:Call('ArmyAbilityCurrency()')
    info['FactionName'] = cco_army:Call('FactionName()')
    info['GlobalCurrency'] = cco_army:Call('GlobalCurrency()')
    info['HasWaaagh'] = cco_army:Call('HasWaaagh()')
    info['HasMurderousProwess'] = cco_army:Call('HasMurderousProwess()')
    info['ArmyName'] = cco_army:Call('ArmyName()')
    info['CurrentArmyAbilityThreshold'] = cco_army:Call('HasCurrentArmyAbilityThresholdWaaagh()')
    info['HasRealmOfSouls'] = cco_army:Call('HasRealmOfSouls()')
    info['FactionFlagDir'] = cco_army:Call('FactionFlagDir()')

    info['Faction.Key'] = cco_faction:Call('Key')
    info['Faction.PrimaryColour'] = cco_faction:Call('PrimaryColour')
    info['Faction.FactionSkin'] = cco_faction:Call('FactionSkin')
    -- info['Faction.MechanicList'] = cco_faction:Call('MechanicList')
    info['Faction.Subculture.Key'] = cco_faction:Call('SubcultureContext.Key')
    info['Faction.Subculture.Name'] = cco_faction:Call('SubcultureContext.Name')

    table.insert(armies_table, info)
end

function battle_data_dumper:iter_over_armies(alliance, alliance_id)
    local armies = alliance:armies()
    for i = 1, armies:count() do
        self:out('Army #' .. i)
        local army = armies:item(i)
        self:save_army_info(army, alliance_id)
        self:iter_over_units(army, false)
        -- local reinf_army = bm:reinforcements():reinforcement_army_for_army(army) -- not working?????
    end
end
function battle_data_dumper:iter_over_reinforcement_armies()
    for r = 1, bm:reinforcements():reinforcement_army_count() do
        self:out('Reinforcement Army #' .. r)
        local reinf_army = bm:reinforcements():reinforcement_army(r):army()
        local alliance_id = bm:reinforcements():reinforcement_army(r):target_army():unique_id(); -- Points to target army id, not alliance id in this case
        self:out('reinforcemnt army ' .. reinf_army:unique_id())
        self:save_reinforcement_army_info(reinf_army, alliance_id)
        self:out('reinforcemnt army ' .. reinf_army:unique_id() .. ' succesfully saved army info')
        self:iter_over_units(reinf_army, true)
        self:out('reinforcemnt army ' .. reinf_army:unique_id() .. ' succesfully saved unit info')
    end
end

function battle_data_dumper:get_battle_army_info(army)
    local cco_br = cco('CcoBattleRoot', 'BattleRoot')
    local cco_army = cco_br:Call('ArmyList.FirstContext(UniqueID==' .. army:unique_id() .. ')')

    local info = {}
    info['time'] = bm:time_elapsed_ms()
    info['is_commander_alive'] = army:is_commander_alive()
    info['is_commander_invincible'] = army:is_commander_invincible()
    -- info['is_player_controlled'] = army:is_player_controlled()
    -- info['army_handicap'] = army:army_handicap()
    info['winds_of_magic_remaining_recharge_rate'] = army:winds_of_magic_remaining_recharge_rate()
    info['winds_of_magic_reserve'] = army:winds_of_magic_reserve()
    info['winds_of_magic_current'] = army:winds_of_magic_current()
    info['is_reinforcement_army'] = army:is_reinforcement_army()
    info['num_reinforcement_units'] = army:num_reinforcement_units()
    info['unique_id'] = army:unique_id()
    --army:has_currency(string currency type)
    --army:currency_amount(string currency type)

    info['IsAlive'] = cco_army:Call('IsAlive()')
    info['NumMenDied'] = cco_army:Call('NumMenDied()')
    info['NumUnits'] = cco_army:Call('NumUnits()')
    info['CurrentWaaaghPercent'] = cco_army:Call('CurrentWaaaghPercent()')
    -- info['FactionContext'] = cco_army:Call('FactionContext()')
    info['CurrentWaaaghThreshold'] = cco_army:Call('CurrentWaaaghThreshold()')
    -- info['MaxUnitsCanControl'] = cco_army:Call('MaxUnitsCanControl()')
    -- info['WindsOfMagicPoolContext'] = cco_army:Call('WindsOfMagicPoolContext()')
    info['NumEntitiesInitial'] = cco_army:Call('NumEntitiesInitial()')
    info['CurrentWaaaghPoints'] = cco_army:Call('CurrentWaaaghPoints()')
    info['NumEntities'] = cco_army:Call('NumEntities()')
    info['CanPerformCataclysmAbility'] = cco_army:Call('CanPerformCataclysmAbility()')
    info['RealmOfSoulsPercent'] = cco_army:Call('RealmOfSoulsPercent()')
    -- info['NumTotalUnits'] = cco_army:Call('NumTotalUnits()')
    -- info['ArmyAbilitiesList'] = cco_army:Call('ArmyAbilitiesList()')
    -- info['AiStatsModifier'] = cco_army:Call('AiStatsModifier()')
    -- info['NumReinforcements'] = cco_army:Call('NumReinforcements()')
    -- info['FormationList'] = cco_army:Call('FormationList()')
    info['MurderousProwessPercent'] = cco_army:Call('MurderousProwessPercent()')
    info['MurderousProwessThresh'] = cco_army:Call('MurderousProwessThresh()')
    -- info['ArmyWideEffects'] = cco_army:Call('ArmyWideEffects()')
    info['MurderousProwessScore'] = cco_army:Call('MurderousProwessScore()')
    info['ArmyAbilityCurrency'] = cco_army:Call('ArmyAbilityCurrency()')
    info['GlobalCurrency'] = cco_army:Call('GlobalCurrency()')
    info['CurrentArmyAbilityThreshold'] = cco_army:Call('HasCurrentArmyAbilityThresholdWaaagh()')
    info['GlobalScore'] = cco_army:Call('GlobalScore()')
    info['Score'] = cco_army:Call('Score()')

    table.insert(self._dump_tables['battle_armies'], info)
end

function battle_data_dumper:iter_over_units(army, is_reinforcement)
    local units = army:units()
    for i = 1, units:count() do
        local unit = units:item(i)
        self:out('Unit #' .. unit:unique_ui_id())
        self:save_unit_static(unit, is_reinforcement, false)
    end
end

function battle_data_dumper:save_unit_static(unit, is_reinforcement, is_appeared_mid_battle)
    local cco_unit = nil
    self:out('DEBUG :: Static Units :: is reinf:' .. tostring(is_reinforcement))
    if is_reinforcement then
        local cco_br = cco('CcoBattleRoot', 'BattleRoot')
        cco_unit = cco_br:Call('ReinforcementArmyList.Filter(UnitList.Any(UniqueUiId==' .. unit:unique_ui_id() .. ')).At(0).UnitList.FirstContext(UniqueUiId==' .. unit:unique_ui_id() .. ')')
    else
        cco_unit = cco('CcoBattleUnit', tostring(unit:unique_ui_id()))
    end
    self:out('DEBUG :: Static Units :: cco_main_unit:Init UnitRecordContext')
    local cco_main_unit = cco_unit:Call('UnitRecordContext')
    local units_table = self._dump_tables['units']

    self:out('DEBUG :: Static Units :: Init Info')
    local info = {}
    info['unique_ui_id'] = unit:unique_ui_id()
    info['is_reinforcement'] = is_reinforcement
    info['is_appeared_mid_battle'] = is_appeared_mid_battle
    info['alliance_index'] = unit:alliance_index()
    -- info['army_index'] = unit:army_index()
    info['ArmyID'] = cco_unit:Call('ArmyContext.UniqueID')
    info['name'] = unit:name()
    info['type'] = unit:type()
    info['unit_class'] = unit:unit_class()
    info['is_infantry'] = unit:is_infantry()
    info['is_anti_cavalry_infantry'] = unit:is_anti_cavalry_infantry()
    info['is_cavalry'] = unit:is_cavalry()
    info['is_lancers'] = unit:is_lancers()
    info['is_chariot'] = unit:is_chariot()
    info['is_war_beasts'] = unit:is_war_beasts()
    info['is_artillery'] = unit:is_artillery()
    info['is_war_machine'] = unit:is_war_machine()
    info['can_fly'] = unit:can_fly()
    info['starting_ammo'] = unit:starting_ammo()

    self:out('DEBUG :: Static Units :: cco_unit')
    info['CanGuerrillaDeploy'] = cco_unit:Call('CanGuerrillaDeploy')
    info['IconPath'] = cco_unit:Call('IconPath')
    info['IsCharacter'] = cco_unit:Call('IsCharacter')
    info['IsUnspottable'] = cco_unit:Call('IsUnspottable')
    info['NumEntitiesInitial'] = cco_unit:Call('NumEntitiesInitial')
    info['HealthMax'] = cco_unit:Call('HealthMax')
    info['IsRenown'] = cco_unit:Call('IsRenown')
    info['IsGeneral'] = cco_unit:Call('IsGeneral')
    info['Name'] = cco_unit:Call('Name')

    self:out('DEBUG :: Static Units :: cco_main_unit')
    info['UnitRecord.Key'] = cco_main_unit:Call('Key')
    self:out('DEBUG :: Static Units :: Cost')
    info['UnitRecord.Cost'] = cco_main_unit:Call('Cost')
    self:out('DEBUG :: Static Units :: Tier')
    info['UnitRecord.Tier'] = cco_main_unit:Call('Tier')
    self:out('DEBUG :: Static Units :: CategoryName')
    info['UnitRecord.CategoryName'] = cco_main_unit:Call('CategoryName')
    self:out('DEBUG :: Static Units :: ClassName')
    info['UnitRecord.ClassName'] = cco_main_unit:Call('ClassName')

    self:out('DEBUG :: Static Units :: inserting')
    table.insert(units_table, info)

    self._track_units[unit:unique_ui_id()] = true
    self:out('DEBUG :: Static Units :: inserted')
end

function battle_data_dumper:encode_fatigue_states(state)
    map = {}
    map['threshold_fresh'] = 0
    map['threshold_active'] = 1
    map['threshold_winded'] = 2
    map['threshold_tired'] = 3
    map['threshold_very_tired'] = 4
    map['threshold_exhausted'] = 5
    return map[state]
end

function battle_data_dumper:get_battle_unit_info(unit, is_reinforcement)
    if is_reinforcement then
        return -- do we need to keep track of reinforcements?
    end
    if is_reinforcement then
        local cco_br = cco('CcoBattleRoot', 'BattleRoot')
        cco_unit = cco_br:Call('(uiid=' .. unit:unique_ui_id() .. ') => {ReinforcementArmyList.FirstContext(UnitList.Any(UniqueUiId==uiid)).UnitList.FirstContext(UniqueUiId==uiid)}')
    else
        cco_unit = cco('CcoBattleUnit', tostring(unit:unique_ui_id()))
    end

    -- if unit is not present in units table - add it (spawned unit)
    if not self._track_units[unit:unique_ui_id()] then
        self:out('New unit has apperead id: ' .. unit:unique_ui_id())
        self:out('Setting up callback ' .. unit:unique_ui_id())
        -- Doing via delayed callback because UnitRecordContext is not initialised yet if call immediately
        -- Set to true immediately - to not create many delayed callbacks for one unit
        self._track_units[unit:unique_ui_id()] = true

        local function f()
            -- battle_data_dumper.out(battle_data_dumper, 'Callback Fired 3')
            battle_data_dumper:out('Callback Fired ' .. unit:unique_ui_id())
            battle_data_dumper:save_unit_static(unit, is_reinforcement, true)
        end

        local timeout = bm:model_tick_time_ms() * 10
        bm:callback(f, timeout)
        self:out('Callback Set Up ' .. unit:unique_ui_id())
    end

    -- out_data_handler('dUMP uNIT CALLED')
    --https://chadvandy.github.io/tw_modding_resources/WH3/battle/battle_unit.html#class:battle_unit
    local info = {}
    info['time'] = bm:time_elapsed_ms()
    info['unique_ui_id'] = unit:unique_ui_id()
    info['is_reinforcement'] = minify_bool(is_reinforcement)
    -- dynamic stats
    info['is_currently_flying'] = minify_bool(unit:is_currently_flying())
    --Location and Movement
    local pos = unit:position()
    -- info['position'] = table.concat({pos:get_x(), pos:get_y(), pos:get_z()}, ',')
    info['is_moving_fast'] = minify_bool(unit:is_moving_fast())
    info['is_idle'] = minify_bool(unit:is_idle())
    info['is_leaving_battle'] = minify_bool(unit:is_leaving_battle())
    --Visibility
    info['is_hidden'] = minify_bool(unit:is_hidden())
    --Combat
    info['is_under_missile_attack'] = minify_bool(unit:is_under_missile_attack())
    info['is_in_melee'] = minify_bool(unit:is_in_melee())
    --Unit Strength
    info['number_of_enemies_killed'] = unit:number_of_enemies_killed() --?
    -- out_data_handler('Morale and Fatigue')
    --Morale and Fatigue
    info['is_wavering'] = minify_bool(unit:is_wavering())
    info['is_routing'] = minify_bool(unit:is_routing())
    info['is_invulnerable'] = minify_bool(unit:is_invulnerable())
    info['is_rampaging'] = minify_bool(unit:is_rampaging())
    info['is_shattered'] = minify_bool(unit:is_shattered())
    -- doesn't exist? info['is_crumbling'] = unit:is_crumbling()
    -- doesn't exist? info['is_unstable'] = unit:is_unstable()
    info['is_left_flank_threatened'] = minify_bool(unit:is_left_flank_threatened())
    info['is_right_flank_threatened'] = minify_bool(unit:is_right_flank_threatened())
    info['is_rear_flank_threatened'] = minify_bool(unit:is_rear_flank_threatened())
    info['left_flank_threat'] = unit:left_flank_threat()
    info['right_flank_threat'] = unit:right_flank_threat()
    info['rear_threat'] = unit:rear_threat()
    info['current_target'] = unit:current_target()
    info['is_deployed'] = minify_bool(unit:is_deployed()) --?
    info['fatigue_state'] = self.encode_fatigue_states(unit:fatigue_state())
    -- out_data_handler('Ammunition and Range')
    --Ammunition and Range
    info['ammo_left'] = unit:ammo_left()
    -- info['missile_range'] = unit:missile_range()
    -- Special Abilities
    -- info['owned_passive_special_abilities'] = table.concat(unit:owned_passive_special_abilities(), ';') -- TODO use map?
    -- info['owned_non_passive_special_abilities'] = table.concat(unit:owned_non_passive_special_abilities(), ';') -- TODO use map?
    -- info['owned_special_abilities'] = table.concat(unit:owned_special_abilities(), ';') -- TODO use map?
    info['can_use_magic'] = minify_bool(unit:can_use_magic())


    -- self:out('DEBUG :: Dynamic Units :: cco_unit')
    -- info['StatusList'] = cco_unit:Call('StatusList.JoinString(Key, ",")') -- TODO use map?
    info['IsWalking'] = minify_bool(cco_unit:Call('IsWalking'))
    info['HasHarmonyEffect'] = minify_bool(cco_unit:Call('HasHarmonyEffect'))
    info['HealthPercent'] = cco_unit:Call('HealthPercent')
    -- info['IsUndead'] = cco_unit:Call('IsUndead')
    info['IsIdle'] = minify_bool(cco_unit:Call('IsIdle'))
    info['IsCapturing'] = minify_bool(cco_unit:Call('IsCapturing'))
    -- info['IsWalking'] = cco_unit:Call('IsWalking')
    info['BarrierMaxHp'] = cco_unit:Call('BarrierMaxHp')
    info['IsWithdrawing'] = minify_bool(cco_unit:Call('IsWithdrawing'))
    info['BarrierCapPercent'] = cco_unit:Call('BarrierCapPercent')
    info['IsInLastStand'] = minify_bool(cco_unit:Call('IsInLastStand'))
    info['IsBarrierCharging'] = minify_bool(cco_unit:Call('IsBarrierCharging'))
    info['IsFiringMissiles'] = minify_bool(cco_unit:Call('IsFiringMissiles'))
    info['DelayedBarrierHpPercent'] = cco_unit:Call('DelayedBarrierHpPercent')
    info['BarrierHp'] = cco_unit:Call('BarrierHp')
    info['IsTerrified'] = minify_bool(cco_unit:Call('IsTerrified'))
    info['BarrierHpPercent'] = cco_unit:Call('BarrierHpPercent')
    info['IsAlive'] = minify_bool(cco_unit:Call('IsAlive'))
    info['IsShattered'] = minify_bool(cco_unit:Call('IsShattered'))
    info['IsAwaitingOrderAfterRally'] = minify_bool(cco_unit:Call('IsAwaitingOrderAfterRally'))
    -- info['IsWounded'] = cco_unit:Call('IsWounded')
    info['IsTakingDamage'] = minify_bool(cco_unit:Call('IsTakingDamage'))
    info['IsUnderMissileAttack'] = minify_bool(cco_unit:Call('IsUnderMissileAttack'))
    info['IsRouting'] = minify_bool(cco_unit:Call('IsRouting'))
    info['NumKills'] = cco_unit:Call('NumKills')
    info['IsInMelee'] = minify_bool(cco_unit:Call('IsInMelee'))
    info['IsWavering'] = minify_bool(cco_unit:Call('IsWavering'))
    info['MaxHealthPercentCanReplenish'] = cco_unit:Call('MaxHealthPercentCanReplenish')
    info['FatigueState'] = cco_unit:Call('FatigueState')
    info['IsVisible'] = minify_bool(cco_unit:Call('IsVisible'))

    -- self:out('DEBUG :: Dynamic Units :: cco_unit 2222')
    -- info['PercentCasualtiesRecently'] = cco_unit:Call('PercentCasualtiesRecently')
    -- info['PercentHpLostRecently'] = cco_unit:Call('PercentHpLostRecently')
    -- info['ActiveEffectState'] = cco_unit:Call('ActiveEffectState')
    info['IsOutOfControl'] = minify_bool(cco_unit:Call('IsOutOfControl'))
    info['MoraleState'] = cco_unit:Call('MoraleState')
    info['IsHidden'] = minify_bool(cco_unit:Call('IsHidden'))
    -- info['IsOrderable'] = cco_unit:Call('IsOrderable')
    info['IsSelected'] = minify_bool(cco_unit:Call('IsSelected'))
    info['ExperienceLevel'] = cco_unit:Call('ExperienceLevel')
    info['MoralePercent'] = cco_unit:Call('MoralePercent')
    info['IsSelectable'] = minify_bool(cco_unit:Call('IsSelectable'))
    info['IsFlying'] = minify_bool(cco_unit:Call('IsFlying'))
    -- info['SecondsLeftToTeleport'] = cco_unit:Call('SecondsLeftToTeleport')
    -- info['ExperiencePercent'] = cco_unit:Call('ExperiencePercent')
    info['NumEntities'] = cco_unit:Call('NumEntities')
    -- info['IsForceRampage'] = cco_unit:Call('IsForceRampage')
    info['IsTeleportWithdrawing'] = minify_bool(cco_unit:Call('IsTeleportWithdrawing'))
    info['IsFiringAtWill'] = minify_bool(cco_unit:Call('IsFiringAtWill'))
    -- info['DamageInflictedRecently'] = cco_unit:Call('DamageInflictedRecently')
    info['IsBuffedByHarmony'] = minify_bool(cco_unit:Call('IsBuffedByHarmony'))
    -- info['IsRunning'] = cco_unit:Call('IsRunning')
    info['HealthValue'] = cco_unit:Call('HealthValue')

    info['BattleResult.DamageDealtCost'] = cco_unit:Call('BattleResultUnitContext.DamageDealtCost')
    info['BattleResult.DamageDealt'] = cco_unit:Call('BattleResultUnitContext.DamageDealt')
    info['BattleResult.NumHitPoints'] = cco_unit:Call('BattleResultUnitContext.NumHitPoints')
    info['BattleResult.NumKillsFriendlies'] = cco_unit:Call('BattleResultUnitContext.NumKillsFriendlies')

    table.insert(self._dump_tables['battle_units'], info)
end

if core:is_battle() then
    bm:register_phase_change_callback("Deployment", function()
        battle_data_dumper:init()
    end)
end
