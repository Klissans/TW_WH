
function random_int(lower, upper)
    --includes both sides
    return cco('CcoFrontendRoot', 'FrontendRoot'):Call(string.format('RandomInRange(%d, %d)', lower, upper))
end

function random_chance()
    return random_int(1, 100)
end

function if_chance_succeed()
    return random_chance() > 50
end

function set_is_recruiting_reinforcements(is_reinforcement)
    local cexp = [[
        (
            pslot = Component('recruitment_parent').ContextsList[0]
        ) =>
        {
            pslot.SetIsRecruitingReinforcements(%s)
        }
    ]]
    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, tostring(is_reinforcement)))
end


function is_using_reinforcements()
    local cexp = [[
        (
            sc = FrontendRoot.CustomBattleLobbyContext.SettingsContext
        ) =>
        {
            sc.IsUsingReinforcingUnits
        }
    ]]
    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    return froot:Call(cexp)
end

function toggle_storm_of_magic()
    local cexp = [[
        (
            sc = FrontendRoot.CustomBattleLobbyContext.SettingsContext
        ) =>
        {
            DoIf(!sc.IsStormOfMagicEnabled, sc.ToggleStormOfMagic)
        }
    ]]
    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    return froot:Call(cexp)
end


function get_unit_slots_left()
    local cexp = [[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            sc = FrontendRoot.CustomBattleLobbyContext.SettingsContext,
            unit_list_size = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList.Size, pslot.UnitList.Size),
            max_unit_list_size = GetIfElse(pslot.IsRecruitingReinforcements, sc.MaxUnitsCanReinforce(pslot.TeamContext.TeamIndex), sc.MaxUnitsCanRecruit(pslot.TeamContext.TeamIndex))
        ) =>
        {
            max_unit_list_size - unit_list_size
        }
    ]]
    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    return froot:Call(cexp)
end


function clear_units()
    local cexp = [[
        (
            pslot = Component('recruitment_parent').ContextsList[0]
        ) =>
        {
            pslot.ClearUnits
        }
    ]]
    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(cexp)
end

function pick_random_unit()
    cexp = [=[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            sc = FrontendRoot.CustomBattleLobbyContext.SettingsContext,
            is_using_large_armies = sc.IsUsingLargeArmies,
            funds_available = pslot.FundsRemaining(!pslot.IsRecruitingReinforcements),
            unit_list_size = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList.Size, pslot.UnitList.Size),
            max_unit_list_size = GetIfElse(pslot.IsRecruitingReinforcements, sc.MaxUnitsCanReinforce(pslot.TeamContext.TeamIndex), sc.MaxUnitsCanRecruit(pslot.TeamContext.TeamIndex)),
            unit_groups = DefaultDatabaseRecord('CcoUiUnitGroupParentRecord').RecordList.Filter(!Key.Contains('commander') && !Key.Contains('heroes_agents') ),
            faction_units= unit_groups.Transform((x=false, _) => pslot.UnitListForUnitGroupParent(x)),
            available_units = faction_units.Filter((x=false, _) => pslot.CanRecruitUnit(x.UnitContext, pslot.IsRecruitingReinforcements)),
            affordable_units = available_units.Filter(Cost <= funds_available)
        ) =>
        {
            DoIf(unit_list_size < max_unit_list_size && affordable_units && affordable_units.Size > 0,
                pslot.RecruitUnit(affordable_units[RandomInRange(0, affordable_units.Size - 1)], pslot.IsRecruitingReinforcements)
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(cexp)
    --randomize_char_skills()
end

function pick_random_char(typee)
    cexp = [=[
        (
            unit_type = '%s',
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_group_record = DatabaseRecordContext('CcoUiUnitGroupParentRecord', unit_type),
            unit_list = pslot.UnitListForUnitGroupParent(unit_group_record).Filter((x=false, _) => pslot.CanRecruitUnit(x.UnitContext, pslot.IsRecruitingReinforcements)),
            runit = unit_list[RandomInRange(0, unit_list.Size - 1)]
        ) =>
        {
            pslot.RecruitUnit(runit, pslot.IsRecruitingReinforcements)
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, typee))
    --randomize_char_skills()
end

function randomize_char_skills(i)
    -- we will get the last unit expecting it to be a just picked character
    -- lore first
    randomize_lore(i)
    -- mount second
    randomize_mount(i)
    --other doesn't matter - as they do not reset config
    randomize_spells(i)
    randomize_runes(i)
    randomize_abilities(i)
    randomize_items(i)
    -- randomize_form -- I don't have dlc to test
end

function randomize_lore(i)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            character = pslot.UnitList[%d],
            tcc = character.UnitTypes.FirstContext(TypeCategoryContext.IsHorizontalGroup == false).TypeCategoryContext,
            lores = character.UnitTypes.Filter(TypeCategoryContext == tcc)
        ) =>
        {
            DoIf(lores.Size > 0, character.ChangeUnitType(lores[RandomInRange(0, lores.Size - 1)]))
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, i))
end

function randomize_spells(i)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            character = pslot.UnitList[%d],
            spells = GetIf(character.UnitDetailsContext.HasRandomisedSpells == false, character.AvailableUpgradeList.Filter(IsContextValid(AncillaryContext) == false && AbilityContext.ManaUsed > 0))
        ) =>
        {
            DoIf(spells && spells.Size > 0,
                spells.ForEach(DoIf(RandomInRange(1, 100) > 50, ToggleEquipped))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, i))
end

function randomize_runes(i)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            character = pslot.UnitList[%d],
            runes = character.AvailableUpgradeList.Filter(IsContextValid(AbilityContext.AbilityGroupContext) && AbilityContext.AbilityGroupContext.IsRunicLore)
        ) =>
        {
            DoIf(runes && runes.Size > 0,
                runes.ForEach(DoIf(RandomInRange(1, 100) > 50, ToggleEquipped))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, i))
end


function randomize_abilities(i)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            character = pslot.UnitList[%d],
            abilities = character.AvailableUpgradeList.Filter(IsContextValid(AncillaryContext) == false && AbilityContext.ManaUsed == 0 && (IsContextValid(AbilityContext.AbilityGroupContext) == false || AbilityContext.AbilityGroupContext.IsRunicLore == false))
        ) =>
        {
            DoIf(abilities && abilities.Size > 0,
                abilities.ForEach(DoIf(RandomInRange(1, 100) > 50, ToggleEquipped))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, i))
end


function randomize_items(i)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            character = pslot.UnitList[%d],
            items = character.AvailableUpgradeList.Filter(IsContextValid(AncillaryContext) && AncillaryContext.CategoryContext.Key != "form")
        ) =>
        {
            DoIf(items && items.Size > 0,
                items.ForEach(DoIf(RandomInRange(1, 100) > 50, ToggleEquipped))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, i))
end


function randomize_mount(i)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            pslot = Component('recruitment_parent').ContextsList[0],
            character = pslot.UnitList[%d],
            mounts = character.AvailableMountsList
        ) =>
        {
            DoIf(mounts && mounts.Size > 0, character.ChangeMount(mounts[RandomInRange(0, mounts.Size - 1)]))
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, i))
end


function lucky_priority_lock()
    local NON_LOCK_PRIORITY = 888
    local LOCK_PRIORITY = -111
    local army_roster_parent = find_uicomponent(core:get_ui_root(), "custom_battle", "ready_parent", "recruitment_visibility_parent", "recruitment_parent", "roster_holder", "army_roster_parent")
    local unit_list_holder = find_uicomponent(army_roster_parent, "recruited_army_parent", "army_recruitment_parent", "unit_list_holder")
    local vslider = find_uicomponent(army_roster_parent, "recruitable_list_parent", "listview", "vslider")
    local listview = find_uicomponent(army_roster_parent, "recruitable_list_parent", "listview")
    local unit_list = find_uicomponent(unit_list_holder, "unit_list")
    local reinforcing_list_holder = find_uicomponent(army_roster_parent, "recruited_army_parent", "army_recruitment_parent", "reinforcing_list_holder")
    local reinforcing_unit_list = find_uicomponent(reinforcing_list_holder, "reinforcing_unit_list")

    local upgrades_and_recruitment_holder = find_uicomponent(army_roster_parent, "recruitable_list_parent", "listview", "list_clip", "list_box", "upgrades_and_recruitment_holder")
    local customisation_options_holder = find_uicomponent(upgrades_and_recruitment_holder, "unit_upgrades_parent", "unit_upgrades_collapsible", "custom_battle_unit_upgrades", "upgrades_holder", "customisation_options_holder")

    local spell_browser_parent = find_uicomponent(unit_list_holder, "row_header", "button_bar_parent", "button_list", "spell_browser_parent")
    local button_save_parent = find_uicomponent(unit_list_holder, "row_header", "button_bar_parent", "button_list", "load_save_parent", "button_save_preset")
    local clear_autogen_parent = find_uicomponent(unit_list_holder, "row_header", "button_bar_parent", "button_list", "clear_autogen_parent")
    local button_clear = find_uicomponent(clear_autogen_parent, "button_clear")
    local button_autogen = find_uicomponent(clear_autogen_parent, "button_autogen")
    local button_lucky = find_uicomponent(clear_autogen_parent, "button_lucky")

    local button_clear_reinforcement = find_uicomponent(reinforcing_list_holder, "row_header", "clear_autogen_reinforcement_parent", "button_clear_reinforcements")


    army_roster_parent:PropagatePriority(LOCK_PRIORITY)
    spell_browser_parent:PropagatePriority(NON_LOCK_PRIORITY)
    unit_list:PropagatePriority(NON_LOCK_PRIORITY)
    reinforcing_unit_list:PropagatePriority(NON_LOCK_PRIORITY)
    button_clear:PropagatePriority(NON_LOCK_PRIORITY)
    button_clear_reinforcement:PropagatePriority(NON_LOCK_PRIORITY)
    button_save_parent:PropagatePriority(NON_LOCK_PRIORITY)
    listview:PropagatePriority(NON_LOCK_PRIORITY)
    upgrades_and_recruitment_holder:PropagatePriority(LOCK_PRIORITY)
    if button_lucky then
        button_lucky:PropagatePriority(NON_LOCK_PRIORITY)
    end
    army_roster_parent:LockPriority(LOCK_PRIORITY + 1)
end


function go_lucky()
    --toggle_storm_of_magic()
    clear_units()
    set_is_recruiting_reinforcements(false)
    pick_random_char('commander')
    randomize_char_skills(0)
    pick_random_char('heroes_agents')
    randomize_char_skills(1)
    if if_chance_succeed() then
        pick_random_char('heroes_agents')
        -- do for two characters cuz we cannot rely on order of adding as UnitList sorted by value?
        randomize_char_skills(1)
        randomize_char_skills(2)
    end
    for _ = 0, get_unit_slots_left()-1 do
        pick_random_unit()
        -- haven't implemented unit skill randomization
    end

    if is_using_reinforcements() then
        set_is_recruiting_reinforcements(true)
        for _ = 0, get_unit_slots_left()-1 do
            pick_random_unit()
            -- haven't implemented unit skill randomization
        end
    end
end


--init_custom_battle_for_random_builds()

function lucky_check_if_mp_lobby()
    local cb = find_uicomponent(core:get_ui_root(), "custom_battle")
    if cb then
        local checkbox_parent =  find_uicomponent(cb, "ready_parent", "settings_parent", "custom_battle_map_settings", "settings_parent", "checkbox_parent")
        find_uicomponent(checkbox_parent, "checkbox_storm_of_magic"):SetVisible(checkbox_parent:Visible())

        local army_roster_parent = find_uicomponent(cb, "ready_parent", "recruitment_visibility_parent", "recruitment_parent", "roster_holder", "army_roster_parent")
        local unit_list_holder = find_uicomponent(army_roster_parent, "recruited_army_parent", "army_recruitment_parent", "unit_list_holder")
        local clear_autogen_parent = find_uicomponent(unit_list_holder, "row_header", "button_bar_parent", "button_list", "clear_autogen_parent")
        local button_lucky = find_uicomponent(clear_autogen_parent, "button_lucky")
        if not button_lucky then
            out('Creating Lucky button')
            button_lucky = UIComponent(clear_autogen_parent:CreateComponent("button_lucky", 'ui/templates/square_small_button.twui.xml')) --"ui/mod/button_lucky.twui.xml"
            local icon = find_uicomponent(button_lucky, "icon")
            local icon_path = 'ui/mod/dices.png'
            button_lucky:SetImagePath(icon_path)
            icon:SetImagePath(icon_path)
            button_lucky:Resize(36, 36)
            icon:Resize(36, 36)
            button_lucky:SetVisible(true)
            button_lucky:SetDisabled(false)
        end

        local title = find_uicomponent(cb, 'ready_parent', 'title_plaque', 'tx_header'):CurrentState()
        if title == "mp" then
            --out('Lucky propagate lock')
            lucky_priority_lock()
        end
    end
end


function klissan_lucky_button_init_frontend()
    core:get_tm():repeat_real_callback(function() lucky_check_if_mp_lobby() end, 250, 'Klissan_lucky_check_custom_battle')

    core:add_listener(
            "chat_button_toggle_chat_clicked",
            "ComponentLClickUp",
            function(context)
                return context.string == "button_lucky"
            end,
            function(context)
                go_lucky()
            end,
            true
    )
end

if not core:is_battle() then
	core:add_ui_created_callback(
		function()
			if core:is_frontend() then
				klissan_lucky_button_init_frontend()
			end
		end
	)
end