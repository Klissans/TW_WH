
function random_int(lower, upper)
    --includes both sides
    return cco('CcoFrontendRoot', 'FrontendRoot'):Call(string.format('RandomInRange(%d, %d)', lower, upper))
end

function random_chance()
    return random_int(1, 100)
end

function if_chance_succeed()
    local r = random_chance()
    local v = common.get_context_value('CcoScriptObject', 'klissan.lucky.build_explainer', 'StringValue')
    local loc_language = cco('CcoFrontendRoot', 'FrontendRoot'):Call('LocLanguage')
    local explain_str = string.format(common.get_localised_string('random_localisation_strings_string_explain_second_char'), r)
    common.set_context_value('klissan.lucky.build_explainer', v .. explain_str)
    return r > 50
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
    -- TODO optimize using cache LIst
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
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
            GetIf(unit_list_size < max_unit_list_size && affordable_units && affordable_units.Size > 0,
                (
                    rand = TrueRandomInRange(0, affordable_units.Size - 1),
                    runit = affordable_units[rand],
                    explain_str = Format(Loc('explain_unit_recruitment'), funds_available, rand+1, affordable_units.Size, runit.UnitContext.CategoryIcon, runit.UnitContext.Name, runit.Cost)
                ) =>
                {
                    Do(
                        pslot.RecruitUnit(runit, pslot.IsRecruitingReinforcements),
                        soc.SetStringValue(soc.StringValue + explain_str)
                    ) + runit.UnitContext.Key
                }
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    local key = froot:Call(cexp)
    if key then
        -- out('picked Unit: '..key)
        key = randomize_unit_skills(key)
    end
    return key
end

function pick_random_char(typee)
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            unit_type = '%s',
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_group_record = DatabaseRecordContext('CcoUiUnitGroupParentRecord', unit_type),
            unit_list = pslot.UnitListForUnitGroupParent(unit_group_record).Filter((x=false, _) => pslot.CanRecruitUnit(x.UnitContext, pslot.IsRecruitingReinforcements)),
            rand = TrueRandomInRange(0, unit_list.Size - 1),
            runit = unit_list[rand],
            explain_str = Format(Loc('explain'), '[[col:red]]' + unit_group_record.OnscreenName + '[[/col]]', rand+1, unit_list.Size, runit.UnitContext.CategoryIcon, runit.UnitContext.Name)
        ) =>
        {
            Do(
                pslot.RecruitUnit(runit, pslot.IsRecruitingReinforcements),
                soc.SetStringValue(soc.StringValue + explain_str)
            ) + runit.UnitContext.Key
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    local key = froot:Call(string.format(cexp, typee))
    -- out('picked character: '..key)
    key = randomize_char_skills(key)
    return key
end

function randomize_char_skills(key)
    -- we will get the last unit expecting it to be a just picked character
    -- category is the first, TODO multi-category support
    key = randomize_category(key)
    -- lore second
    key = randomize_lore(key)
    -- mount third
    key = randomize_mount(key)
    --other doesn't matter - as they do not reset config
    randomize_spells(key)
    randomize_runes(key)
    randomize_abilities(key)
    randomize_items(key)
    randomize_changeling_form(key)
    return key
end


function randomize_unit_skills(key)
    -- we will get the last unit expecting it to be a just picked character
    -- category is the first, TODO multi-category support
    key = randomize_category(key)
    --other doesn't matter - as they do not reset config
    randomize_abilities(key)
    return key
end

function randomize_category(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            unit = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            category_types = unit.UnitTypes.Transform(TypeCategoryContext).Filter(IsHorizontalGroup).Distinct
        ) =>
        {
            GetIfElse(
                category_types && category_types.Size > 0,
                (
                    funds_available = pslot.FundsRemaining(!pslot.IsRecruitingReinforcements),
                    category_type = category_types[0],
                    unit_types = unit.UnitTypes.Filter(TypeCategoryContext == category_type)
                        .Filter(AlternateUnitContext.Cost - unit.UnitRecordContext.Cost <= funds_available)
                        .Filter((x=false, _) => pslot.CanRecruitUnit(x.AlternateUnitContext, unit.IsReinforcement, unit.UnitRecordContext))
                        .Sort(CategoryTypeName).Sort(SortOrder, true),
                    rand = TrueRandomInRange(0, unit_types.Size - 1),
                    unit_type = unit_types[rand],
                    explain_str = Format(Loc('explain'), '[[col:magic]]' + category_type.CategoryName + '[[/col]]', rand+1, unit_types.Size, unit_type.TypeIcon, unit_type.CategoryTypeName)
                ) =>
                {
                    GetIfElse(
                        unit_types.Size > 1,
                        Do(
                            unit.ChangeUnitType(unit_type),
                            soc.SetStringValue(soc.StringValue + explain_str)
                        ) + unit_type.AlternateUnitContext.Key,
                        unit.UnitRecordContext.Key
                    )
                },
                unit.UnitRecordContext.Key
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    local x = froot:Call(string.format(cexp, key))
    -- out('randomized category for '..key)
    return x
end

function randomize_lore(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            character = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            fc = character.UnitTypes.FirstContext(TypeCategoryContext.IsHorizontalGroup == false),
            tcc = GetIf(IsContextValid(fc), fc.TypeCategoryContext),
            lores = GetIf(IsContextValid(tcc), character.UnitTypes.Filter(TypeCategoryContext == tcc))
        ) =>
        {
            GetIfElse(lores && lores.Size > 0,
                (
                    rand = TrueRandomInRange(0, lores.Size - 1),
                    rlore = lores[rand],
                    explain_str = Format(Loc('explain'), '[[col:magic]]' + tcc.CategoryName + '[[/col]]', rand+1, lores.Size,
                        GetIfElse(rlore.TypeIcon.IsEmpty, rlore.AlternateUnitContext.SpecialAbilityGroupList.FirstContext.ButtonIconPath, rlore.TypeIcon),
                        GetIfElse(rlore.CategoryTypeName.IsEmpty, rlore.AlternateUnitContext.SpecialAbilityGroupList.FirstContext.Name, rlore.CategoryTypeName))
                ) =>
                {
                    Do(
                        character.ChangeUnitType(rlore),
                        soc.SetStringValue(soc.StringValue + explain_str)
                    ) + rlore.AlternateUnitContext.Key
                },
                character.UnitRecordContext.Key
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    local x = froot:Call(string.format(cexp, key))
    -- out('randomized lore for '..key)
    return x
end


function randomize_mount(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            character = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            mounts = character.AvailableMountsList
        ) =>
        {
            GetIfElse(
                mounts && mounts.Size > 0,
                (
                    rand = TrueRandomInRange(0, mounts.Size),
                    mount = GetIfElse(rand == 0, false, mounts[rand-1]),
                    mount_icon = GetIfElse(rand == 0, '', mount.IconName),
                    mount_name = GetIfElse(rand == 0, StringGet('uied_component_texts_localised_string_StateText_1da8a240'), mount.MountName),
                    mount_str = StringGet('uied_component_texts_localised_string_header_default_Text_72004c'),
                    explain_str = Format(Loc('explain'), '[[col:magic]]' + mount_str + '[[/col]]', rand, mounts.Size, mount_icon, mount_name)
                ) =>
                {
                    soc.SetStringValue(soc.StringValue + explain_str)
                    + GetIfElse(rand > 0,
                        Do(character.ChangeMount(mount)) + mount.MountedUnitContext.Key,
                        character.UnitRecordContext.Key
                    )
                },
                character.UnitRecordContext.Key
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    local x = froot:Call(string.format(cexp, key))
    -- out('randomized mount for '..key)
    return x
end

function randomize_spells(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            th = 50,
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            character = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            spells = GetIf(character.UnitDetailsContext.HasRandomisedSpells == false, character.AvailableUpgradeList.Filter(IsContextValid(AncillaryContext) == false && AbilityContext.ManaUsed > 0))
        ) =>
        {
            DoIf(spells && spells.Size > 0,
                spells.ForEach(
                    (
                        x,
                        rand = TrueRandomInRange(1, 100),
                        if_success = rand > th,
                        explain_str = Format(Loc('img_f'), IconPath) + GetIfElse(if_success, Format(Loc('col_yd'), rand), rand)
                    ) =>
                    {
                        DoIf(
                            CanAfford,
                            Do(soc.SetStringValue(soc.StringValue + explain_str), DoIf(if_success, ToggleEquipped))
                        )
                    }
                ) + soc.SetStringValue(soc.StringValue + Loc('LF'))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, key))
    -- out('randomized spells for '..key)
end

function randomize_runes(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            th = 50,
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            character = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            runes = character.AvailableUpgradeList.Filter(IsContextValid(AbilityContext.AbilityGroupContext) && AbilityContext.AbilityGroupContext.IsRunicLore)
        ) =>
        {
            DoIf(runes && runes.Size > 0,
                runes.ForEach(
                    (
                        x,
                        rand = TrueRandomInRange(1, 100),
                        if_success = rand > th,
                        explain_str = Format(Loc('img_f'), IconPath) + GetIfElse(if_success, Format(Loc('col_yd'), rand), rand)
                    ) =>
                    {
                        DoIf(
                            CanAfford,
                            Do(soc.SetStringValue(soc.StringValue + explain_str), DoIf(if_success, ToggleEquipped))
                        )
                    }
                ) + soc.SetStringValue(soc.StringValue + Loc('LF'))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, key))
    -- out('randomized runes for '..key)
end


function randomize_abilities(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            th = 50,
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            character = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            abilities = character.AvailableUpgradeList.Filter(IsContextValid(AncillaryContext) == false && AbilityContext.ManaUsed == 0 && (IsContextValid(AbilityContext.AbilityGroupContext) == false || AbilityContext.AbilityGroupContext.IsRunicLore == false))
        ) =>
        {
            DoIf(abilities && abilities.Size > 0,
                abilities.ForEach(
                    (
                        x,
                        rand = TrueRandomInRange(1, 100),
                        if_success = rand > th,
                        explain_str = Format(Loc('img_f'), IconPath) + GetIfElse(if_success, Format(Loc('col_yd'), rand), rand)
                    ) =>
                    {
                        DoIf(
                            CanAfford,
                            Do(soc.SetStringValue(soc.StringValue + explain_str), DoIf(if_success, ToggleEquipped))
                        )
                    }
                ) + soc.SetStringValue(soc.StringValue + Loc('LF'))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, key))
    -- out('randomized abilities for '..key)
end


function randomize_items(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            th = 50,
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            character = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            items = character.AvailableUpgradeList.Filter(IsContextValid(AncillaryContext) && AncillaryContext.CategoryContext.Key != "form")
        ) =>
        {
            DoIf(items && items.Size > 0,
                items.ForEach(
                    (
                        x,
                        rand = TrueRandomInRange(1, 100),
                        if_success = rand > th,
                        explain_str = Format(Loc('img_f'), IconPath) + GetIfElse(if_success, Format(Loc('col_yd'), rand), rand)
                    ) =>
                    {
                        DoIf(
                            CanAfford,
                            Do(soc.SetStringValue(soc.StringValue + explain_str), DoIf(if_success, ToggleEquipped))
                        )
                    }
                ) + soc.SetStringValue(soc.StringValue + Loc('LF'))
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, key))
    -- out('randomized items for '..key)
end

function randomize_changeling_form(key)
    -- we will get the last unit expecting it to be a just picked character
    cexp = [=[
        (
            soc = ScriptObjectContext('klissan.lucky.build_explainer'),
            pslot = Component('recruitment_parent').ContextsList[0],
            unit_list = GetIfElse(pslot.IsRecruitingReinforcements, pslot.ReinforcingUnitList, pslot.UnitList),
            character = unit_list.LastContext(UnitRecordContext.Key == '%s'),
            has_form = character.UnitDetailsContext.AbilityDetailsList.Any(AbilityContext.SpecialAbilityBehaviourGroup == "changeling_transformation")
        ) =>
        {
            DoIf(has_form,
                (
                    unlocked_forms = CustomBattleShapeshiftFormsList.Filter(MainUnitRecordContext.IsOwned),
                    rand = TrueRandomInRange(0, unlocked_forms.Size - 1),
                    chosen_form = unlocked_forms.At(rand),
                    munit = chosen_form.MainUnitRecordContext,
                    explain_str =  Format(Loc('explain'), '[[col:magic]]' + StringGet('uied_component_texts_localised_string_StateText_71eb0ae9') + '[[/col]]', rand+1, unlocked_forms.Size, munit.CategoryIcon, munit.Name)
                ) =>
                {
                    Do(
                        character.SetTransformationUnitOverride(munit),
                        soc.SetStringValue(soc.StringValue + explain_str)
                    )
                }
            )
        }
    ]=]

    local froot = cco('CcoFrontendRoot', 'FrontendRoot')
    froot:Call(string.format(cexp, key))
    -- out('randomized form for '..key)
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
    clear_units()
    common.set_context_value('klissan.lucky.build_explainer', '[[col:yellow]]'..common.get_localised_string('random_localisation_strings_string_main_army') .. ':\n[[/col]]')
    set_is_recruiting_reinforcements(false)
    local key = nil
    key = pick_random_char('commander')
    key = pick_random_char('heroes_agents')
    if if_chance_succeed() then
        key = pick_random_char('heroes_agents')
    end
    for _ = 0, get_unit_slots_left()-1 do
        pick_random_unit()
    end

    if is_using_reinforcements() then
        local v = common.get_context_value('CcoScriptObject', 'klissan.lucky.build_explainer', 'StringValue')
        common.set_context_value('klissan.lucky.build_explainer', v ..'[[col:yellow]]'.. common.get_localised_string('uied_component_texts_localised_string_label_button_default_Text_42000d') .. ':\n[[/col]]')
        set_is_recruiting_reinforcements(true)
        for _ = 0, get_unit_slots_left()-1 do
            pick_random_unit()
        end
    end
    local button_lucky = find_uicomponent(core:get_ui_root(), "custom_battle", "ready_parent", "recruitment_visibility_parent", "recruitment_parent", "roster_holder", "army_roster_parent", "recruited_army_parent", "army_recruitment_parent", "unit_list_holder", "row_header", "button_bar_parent", "button_list", "clear_autogen_parent", "button_lucky")

    button_lucky:SetTooltipText(common.get_context_value('CcoScriptObject', 'klissan.lucky.build_explainer', 'StringValue'), true)
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


--TODO faction random button

-- TODO chat reports
-- TODO snapshots for observers

-- TODO REFACTOR THIUS FUCKIONH LUA