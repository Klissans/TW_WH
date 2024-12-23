from whlib.twui import *


def add_timer_to_tickets(xml):
    # language=javascript
    s = '''
        (timeStr = FormatTime((BattleRoot.CaptureLocationManagerContext.TicketsGoal - TicketsRemaining) / TicketsIncomePerSecond)) =>
            {
                GetIfElse(BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiPlayer,
                    TicketsRemaining + "[[img:ui/skins/default/icon_cooldown.png]][[/img]]"
                    + GetIfElse(TicketsIncomePerSecond > 0,
                        GetIfElse(StringStartsWith(timeStr, "0"),
                            StringSubString(timeStr, 1, StringLength(timeStr) - 1),
                            timeStr),
                        "~"),
                 TicketsRemaining)
            }
    '''
    set_context_callback(find_by_id(xml, 'allied_tickets'), 'ContextTextLabel', s)
    set_context_callback(find_by_id(xml, 'enemy_tickets'), 'ContextTextLabel', s)


def remove_zooming_to_reinforcement_point(xml):
    find_by_id(xml, 'button_reinforcements') \
        .find(lambda t: t.has_attr('context_function_id') and 'BattleRoot.ZoomToPosition' in t['context_function_id']) \
        .decompose()
    
    # language=javascript
    s = """
        (x = Component("B31F885A-6C20-4E4E-AAD2E9970B9602E0").CurrentSelection.SelectedObjectList) =>
            { !x.IsEmpty | this.BattleRoot.DoesHaveReinforcementPurchasing | false }
    """
    set_context_callback(find_by_id(xml, 'button_reinforcements'), 'MouseOverMenuCallback', s)


def increase_reinforcement_size(xml):
    find_by_id(xml, 'card_holder').LayoutEngine['itemsperrow'] = 10


def add_dom_ffa_to_custom_battles(xml):
    # language=javascript
    s = '''
        GetIfElse(
            IsLabMode,
            BattleTypeRecordList.Filter(Key == "classic"),
            BattleTypeRecordList + GetIf(!IsMultiplayerLobbyActive, DatabaseRecordsForKeys("CcoBattleTypeRecord", "domination", "free_for_all"))
        )
    '''
    set_context_callback(find_by_id(xml, 'map_type_list'), 'ContextList', s)


def enable_button_ai(xml):
    set_context_callback(find_by_id(xml, 'button_add_ai'), 'ContextVisibilitySetter', '''CanAddPlayerSlot''')


def add_vp_owner_icon(xml):
    elem = read_xml_component('hud_battle_top_bar/vp_owner_icon')
    # language=javascript
    s = '''
        BattleRoot.CaptureLocationManagerContext.TimeUntilAllCapturePointsAvailable == 0 && !IsLocked && !IsNeutral
    '''
    set_context_callback(elem, 'ContextVisibilitySetter', s)
    add_element(xml, elem, "template_capture_point_icon")


def add_capture_weight(xml):
    elem = read_xml_component('hud_battle_top_bar/vp_capture_weight')
    
    # language=javascript
    s = '''
        Abs(ContestingFactorForAlliance(BattleRoot.PlayerAllianceContext.Id)) * 100
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        GetIfElse(ContestingFactorForAlliance(BattleRoot.PlayerAllianceContext.Id) > 0, GetColour("alliance_player"), GetColour("alliance_enemy") )
    '''
    set_context_callback(elem, 'ContextColourSetter', s)
    
    # language=javascript
    s = '''
        Abs(ContestingFactorForAlliance(BattleRoot.PlayerAllianceContext.Id)) > 0
    '''
    set_context_callback(elem, 'ContextVisibilitySetter', s)
    
    add_element(xml, elem, "template_capture_point_icon")


def remove_supplies_in_replays(xml):
    set_context_callback(find_by_id(xml, 'supplies_display'), 'ContextVisibilitySetter', '''HasSupplies && !BattleRoot.IsReplay''')


def change_unit_info_kill_count(xml):
    elem_txt = find_by_id(xml, 'dy_kills')
    elem_img = find_by_guid(xml, '4E7A2193-5DEC-443B-865D61B086AB4772')
    find_by_guid(xml, '6C3C4E4E-2E10-4EE0-A6AB409629FD53D7')['disabled'] = 'false'
    find_by_guid(xml, '8057198D-749C-4AA9-9E8494E120C1138E')['disabled'] = 'false'
    find_by_guid(xml, '8057198D-749C-4AA9-9E8494E120C1138E')['interactive'] = 'true'
    
    
    # language=javascript
    s = '''
    (
        reg_key = 'klissan.hui.ui_panel_battle_stat',
        reg_value = GetIfElse(RegistryReadString(reg_key).Length == 0, 'gold', RegistryReadString(reg_key))
    ) =>
        Format('[[col:ui_font_faded_grey_beige]]%d[[/col]]',
            GetIf(reg_value == 'kills', KillCount)
            + GetIf(reg_value == 'damage', BattleUnitContext.BattleResultUnitContext.DamageDealt)
            + GetIf(reg_value == 'gold', BattleUnitContext.BattleResultUnitContext.DamageDealtCost)
        )
    '''
    set_context_callback(elem_txt, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (
            func_get_localization = ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value
        ) =>
        {
            Format(EvaluateExpression(Format(func_get_localization, 'tooltip_kills_ff')), BattleUnitContext.BattleResultUnitContext.NumKillsFriendlies)
            + Format(Loc('tooltip_kills'), KillCount, BattleUnitContext.BattleResultUnitContext.DamageDealt, BattleUnitContext.BattleResultUnitContext.DamageDealtCost)
        }
    '''
    set_context_callback(elem_txt, 'ContextTooltipSetter', s)
    
    # language=javascript
    s = '''
    (
        reg_key = 'klissan.hui.ui_panel_battle_stat',
        reg_value = GetIfElse(RegistryReadString(reg_key).Length == 0, 'gold', RegistryReadString(reg_key))
    ) =>
        GetIf(reg_value == 'kills', 'ui/skins/default/icon_kills.png')
        + GetIf(reg_value == 'damage', 'ui/mod/icons/icon_explosive_damage.png')
        + GetIf(reg_value == 'gold', 'ui/mod/icons/icon_stat_damage_base.png')
    '''
    create_context_callback(elem_img, "ContextImageSetter", "CcoStaticObject", s, {'update_constant': '500'})

    # language=javascript
    s = '''
    (
        reg_key = 'klissan.hui.ui_panel_battle_stat',
        reg_value = GetIfElse(RegistryReadString(reg_key).Length == 0, 'gold', RegistryReadString(reg_key))
    ) =>
    {
        DoIfElse(reg_value == 'kills', RegistryWriteString(reg_key, 'damage'),
            DoIfElse(reg_value == 'damage', RegistryWriteString(reg_key, 'gold'),
                DoIf(reg_value == 'gold', RegistryWriteString(reg_key, 'kills'))
            )
        )
    }
    '''
    create_context_callback(elem_txt, "ContextCommandLeftClick", "CcoStaticObject", s)
    create_context_callback(elem_img, "ContextCommandLeftClick", "CcoStaticObject", s)


def change_unit_health_tooltip(xml):
    # language=javascript
    s = '''
        () =>
        Format(
            GetIfElse(
                MaxHealthPercentCanReplenish < 1,
                Loc('battle_reduced_health_cap'),
                Loc('x_out_of_y_int')
            ),
            RoundFloat(HealthPercent * HealthMax),
            RoundFloat(MinNumericValue(1.0, MaxHealthPercentCanReplenish) * HealthMax)
        ) + GetIf(MaxHealthPercentCanReplenish < 1, Format('(%d)', HealthMax))
    '''
    set_context_callback(find_by_guid(xml, '51FCE0A7-B468-4F61-9FD4B4779F62551A'), 'ContextTextLabel', s)

    # language=javascript
    s = '''
        (
            heal_power = ScriptObjectContext('unit_info_ui.heal_power').NumericValue,
            pcnt = RoundFloat(heal_power * 100),
            pcnt_str = Format('%d%%', pcnt)
        ) =>
        {
            GetIfElse(pcnt < 100, Format('[[col:red]]%s[[/col]]', pcnt_str), GetIfElse(pcnt != 100, Format('[[col:green]]%s[[/col]]', pcnt_str), pcnt_str))
        }
    '''
    set_context_callback(find_by_id(xml, 'dy_healing_power'), 'ContextTextLabel', s)

    # language=javascript
    s = '''
        (
            regen_rate_percent = ScriptObjectContext('unit_info_ui.regen_rate_percent').NumericValue
        ) =>
        {
            Format('%.1f%', regen_rate_percent * 100)
        }
    '''
    set_context_callback(find_by_id(xml, 'dy_regen_rate_percent'), 'ContextTextLabel', s)

    # language=javascript
    s = '''
    (
        heal_power = ScriptObjectContext('unit_info_ui.heal_power').NumericValue,
        regen_rate_absolute = ScriptObjectContext('unit_info_ui.regen_rate_absolute').NumericValue,
        regen_str = Format(Loc('battle_hp_regen'), regen_rate_absolute)
    ) =>
    {
        GetIfElse(heal_power < 1, Format('([[col:red]]%s[[/col]])', regen_str), Format('([[col:green]]%s[[/col]])', regen_str))
    }
    '''
    set_context_callback(find_by_id(xml, 'dy_regen_rate_absolute'), 'ContextTextLabel', s)

    # language=javascript
    s = '''
        ScriptObjectContext('unit_info_ui.heal_rate_explainer').StringValue
    '''
    create_context_callback(find_by_id(xml, 'holder_regen_rate'), 'ContextTooltipSetter', 'CcoBattleUnit', s)


def change_unit_info_hit_points(xml):
    # language=javascript
    s = '''
        (
            is_battle = IsContextValid(BattleRoot),
            buc = BattleUnitContext,
            is_on_fire = BattleUnitContext.StatusList.Any(Key == 'on_fire'),
            heal_power = MaxNumericValue(0, BattleUnitContext.HealingPower + GetIf(is_on_fire, -0.5) ),
            mods_regen_rate = BattleUnitContext.ActiveEffectList.Filter(PhaseRecordContext.HasHealAmount),
            heal_rate_explainer = mods_regen_rate.JoinString(
                (x, t = x.Intensity * x.PhaseRecordContext.HealPercent * (1.0 / x.PhaseRecordContext.HpChangeFrequency)) =>
                Format('%s[[img:%s]][[/img]]%.1f(%f%%)',
                GetIfElse(x.Intensity != 1, Format('[[img:ui/battle ui/ability_icons/spell_mastery.png]][[/img]]%d%%', RoundFloat(x.Intensity * 100)), ''),
                x.IconPath,
                t * buc.HealthMax,
                t * 100
                ), Loc('LF')
            ) + Loc('LF') + Format(' x[[img:ui/skins/default/stat_healing_received.png]][[/img]]%d%%', RoundFloat(heal_power * 100)),
            heal_rate_percent = mods_regen_rate.Sum(Intensity * PhaseRecordContext.HealPercent * (1.0 / PhaseRecordContext.HpChangeFrequency)),
            heal_rate_absolute = BattleUnitContext.HealthMax * heal_rate_percent,
            regen_rate_percent = heal_rate_percent * heal_power,
            regen_rate_absolute = heal_rate_absolute * heal_power,
            set_heal_rate_explainer = ScriptObjectContext('unit_info_ui.heal_rate_explainer').SetStringValue(heal_rate_explainer),
            set_heal_power = ScriptObjectContext('unit_info_ui.heal_power').SetNumericValue(heal_power),
            set_regen_rate_percent = ScriptObjectContext('unit_info_ui.regen_rate_percent').SetNumericValue(regen_rate_percent),
            set_regen_rate_absolute = ScriptObjectContext('unit_info_ui.regen_rate_absolute').SetNumericValue(regen_rate_absolute),
            is_actually_healing = BattleUnitContext.HealthValue != RoundFloat(MinNumericValue(1.0, BattleUnitContext.MaxHealthPercentCanReplenish) * BattleUnitContext.HealthMax)
        ) =>
        GetIfElse(
            IsKnownHp,
            GetIf(is_on_fire, '[[img:ui/skins/default/icon_status_on_fire.png]][[/img]]')
            + HitPoints + GetIf(is_actually_healing && regen_rate_absolute > 0,
                GetIfElse(heal_power < 1, Format('[[col:red]]+%d[[/col]]', RoundFloat(regen_rate_absolute)), Format('[[col:green]]+%d[[/col]]', RoundFloat(regen_rate_absolute)))),
            "??"
        )
    '''
    set_context_callback(find_by_id(xml, 'hit_points'), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        GetIfElse(IsKnownHp,
            BarrierHp
            + GetIf(!BattleUnitContext.IsInMelee && BattleUnitContext.BarrierSecsUntilRecharge > 0,
                Format('[[img:ui/skins/default/icon_cooldown.png]][[/img]]%d ', RoundFloat(BattleUnitContext.BarrierSecsUntilRecharge))
            ),
        '??')
        
    '''
    set_context_callback(find_by_id(xml, 'barrier_hit_points'), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        GetIfElse(
            IsKnownHp,
            Format(
                "InitialHP: [[col:yellow]]%d[[/col]], EntitiesAdjustedMaxHP: [[col:yellow]]%d[[/col]], HealingLeft: %S",
                HitPointsInitial,
                RoundFloat(NumEntities * (HitPointsInitial / NumEntitiesInitial)),
                GetIfElse(!IsBattle, "0",
                    (
                        HealLeftPercent = BattleUnitContext.MaxHealthPercentCanReplenish - HitPointsPercent,
                        HealLeftStr = Format("[[col:yellow]]%d[[/col]]", RoundFloat(HealLeftPercent * HitPointsInitial))
                    ) =>
                    {
                        GetIfElse(NumEntitiesInitial == 1, HealLeftStr,
                            GetIfElse(BattleUnitContext.MaxHealthPercentCanReplenish > 0.99, "undefined", HealLeftStr)
                        )
                    }
                )
            )
            + GetIfElse(
                BarrierMaxHp > 0,
                Format(
                    " [[img:ui/skins/default/icon_barrier_replenish.png]][[/img]]HPAdjustedMaxBP: [[col:magic]]%d[[/col]]",
                    BarrierMaxHp
                ),
                ""
            ),
            "??"
        )
    '''
    # for NumEntitiesInitial == 1 -> MaxHealthPercentCanReplenish == 1.75
    # for NumEntitiesInitial > 1 -> MaxHealthPercentCanReplenish == 1.0 and will drop only after unit has lost 75% of initial (max) HP
    # set_context_callback(find_by_id(xml, 'health_bar'), 'ContextTooltipSetter', s)


def add_unit_info_gold_value(xml):
    elem = read_xml_component('unit_information/gold_value')
    
    # language=javascript
    s = '''
            "[[img:ui/skins/default/icon_income.png]][[/img]]"
                + GetIf(IsBattle, Format('[[col:yellow]]%d[[/col]]', BattleUnitContext.GetGoldValue(true) ))
                + " (" + BattleUnitContext.GetGoldValue(false) + ") "
         '''
    set_context_callback(elem, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
    (
        base_cost = UnitRecordContext.Cost
        + GetIf(UnitRecordContext.Key == 'wh3_dlc24_tze_cha_changeling', AbilityDetailsList.FirstContext(Key == 'wh3_dlc24_lord_abilities_formless_horror').AbilityContext.SpawnedMainUnitRecordContext.Cost)
        + GetIf(UnitRecordContext.Key == 'wh3_dlc24_tze_cha_blue_scribes', 700 + 1500),
        exp_cost = RoundFloat(ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11))
    ) =>
    {
        "[[img:ui/skins/default/icon_income.png]][[/img]]"
        + Format("%d%S%S",
            base_cost,
            GetIf(ExperienceLevel > 0, GetIfElse(UnitRecordContext.IsRenown, "", Format(" [[img:ui/skins/default/experience_%d.png]][[/img]]%d", ExperienceLevel, exp_cost) )),
            GetIf(IsCharacter,
                Format(Loc('LF') + "%S",
                    AbilityDetailsList
                    .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                    .Filter(IsUnitUpgrade)
                    .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                    .JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/skins/default/icon_income.png]][[/img]]%d", BaseRecordContext.IconPath, UnitAbilityContext.Name, RoundFloat(AdditionalMeleeCp + AdditionalMissileCp)), Loc('LF'))
            ))
        )
    }

    '''
    set_context_callback(elem, 'ContextTooltipSetter', s)
    
    add_element(xml, elem, "row_header_stats")


def add_unit_info_fatigue(xml):
    elem = read_xml_component('unit_information/fatigue_status')
    
    # language=javascript
    s = '''GetIf(BattleUnitContext,
            Format("[[col:fatigue_%S]][[img:ui/skins/default/icon_status_fatigue_24px.png]][[/img]][[/col]]",
                     ScriptObjectContext('fatigue_states').TableValue.Value[BattleUnitContext.FatigueState]
                     ) + BattleUnitContext.FatigueName)
                '''
    set_context_callback(elem, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (
            f_state = BattleUnitContext.FatigueState,
            f_state_str = ScriptObjectContext('fatigue_states').TableValue.Value[f_state].Value,
            f_effects = ScriptObjectContext('fatigue_effects').TableValue.Value.Transform(MakePair(Key, Value[f_state].Value)).Filter(Second < 1.0),
            f_effects_str = f_effects.JoinString(Format("[[img:ui/mod/icons/icon_%S.png]][[/img]]-%d%%", First, RoundFloat((1.0-Second) * 100)), ''),
            f_leadership = ScriptObjectContext('fatigue_effects_leadership').TableValue.Value[f_state].Value,
            f_leadership_str = GetIfElse(f_leadership < 0, Format(" [[img:ui/mod/icons/icon_stat_morale.png]][[/img]]%d", RoundFloat(f_leadership)), '')
        ) =>
        {
            Format("[[col:fatigue_%S]]%S[[/col]]", f_state_str, GetIfElse(f_state == 0, '', f_effects_str + f_leadership_str))
        }
    '''
    set_context_callback(elem, 'ContextTooltipSetter', s)
    
    add_element(xml, elem, "row_header_abilities")
    
    # TODO ???
    '''
    -- man unit or mount unit
c = cco('CcoBattleUnit', '1001')
x = c:Call('UnitDetailsContext.UnitRecordContext.UnitLandRecordContext.Key')
console_print(tostring(x))
'''


def add_unit_banner_tier(xml):
    elem = read_xml_component('unit_banner/unit_banner_tier')
    # language=javascript
    s = '''
        (
            id = RoundFloat(ToNumber(self.ParentContext.ParentContext.ParentContext.Id)),
            unit = BattleRoot.UnitList.FirstContext(UniqueUiId == id),
            tier = unit.UnitRecordContext.Tier,
            is_visible = self.StateList.Contains(tier),
            set_state = DoIf(is_visible, self.SetState(tier))
        ) => is_visible
    '''
    set_context_callback(elem, 'ContextVisibilitySetter', s)
    add_element(xml, elem, "cat_docker")

def add_spell_panel_wom_cost(xml):
    elem = read_xml_component('spell_panel/wom_cost')
    # language=javascript
    s = '''
        (
            spell_key = StoredContextFromParent('CcoBattleAbility').SetupAbilityContext.RecordKey.Replace('_upgraded', ''),
            units_holder = Component('cards_panel').ChildContext('review_DY'),
            selected_units = units_holder.ChildList
                .Filter(ChildContext('card_image_holder').ChildContext('battle').ChildContext('smoke_particle_emitter').IsVisible)
                .Transform(ContextsList.FirstContext((x) => ContextTypeId(x) == 'CcoBattleUnit')),
            mana_cost = RoundFloat(selected_units.Sum(AbilityList.FirstContext(RecordKey == spell_key).ManaUsed))
        ) => GetIf(mana_cost > 0, mana_cost)
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "button_spell")
    
    elem = read_xml_component('spell_panel/wom_cost_upgraded')
    # language=javascript
    s = '''
        (
            spell_key = StoredContextFromParent('CcoBattleAbility').SetupAbilityContext.RecordKey.Replace('_upgraded', '') + '_upgraded',
            units_holder = Component('cards_panel').ChildContext('review_DY'),
            selected_units = units_holder.ChildList
                .Filter(ChildContext('card_image_holder').ChildContext('battle').ChildContext('smoke_particle_emitter').IsVisible)
                .Transform(ContextsList.FirstContext((x) => ContextTypeId(x) == 'CcoBattleUnit')),
            mana_cost = RoundFloat(selected_units.Sum(AbilityList.FirstContext(RecordKey == spell_key).ManaUsed)),
            set_mana_cost = self.SetText(mana_cost)
        ) => mana_cost > 0
        '''
    set_context_callback(elem, 'ContextVisibilitySetter', s)
    add_element(xml, elem, "button_spell")


def add_unit_info_resistances(xml):
    elem = read_xml_component('unit_information/resistances_row')
    insert_after_element(xml, elem, "health_parent")
    
    elem = read_xml_component('unit_information/res_ward')
    # language=javascript
    s = '''
        Format("[[img:ui/battle ui/ability_icons/resistance_ward_save.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_ward_save") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]] 0[[/col]]"
                )
            }
        )
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")
    
    elem = read_xml_component('unit_information/res_phys')
    # language=javascript
    s = '''
        Format("[[img:ui/battle ui/ability_icons/resistance_physical.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_physical") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]] 0[[/col]]"
                )
            }
        )
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")
    
    elem = read_xml_component('unit_information/res_spell')
    # language=javascript
    s = '''
        Format("[[img:ui/battle ui/ability_icons/resistance_magic.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_magic") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]] 0[[/col]]"
                )
            }
        )
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")
    
    elem = read_xml_component('unit_information/res_missile')
    # language=javascript
    s = '''
        Format("[[img:ui/battle ui/ability_icons/resistance_missile.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_missile") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]] 0[[/col]]"
                )
            }
        )
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")
    
    elem = read_xml_component('unit_information/res_fire')
    # language=javascript
    s = '''
        Format("[[img:ui/battle ui/ability_icons/resistance_fire.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_fire") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    Format("%S",
                        (w = AbilityDetailsList.FirstContext(Key=="weakness_fire") ) => {
                            GetIfElse(
                                IsContextValid(w),
                                ( us = w.Name.RemoveTextTags, i = us.RFind("-") + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:red]]%S[[/col]]", StringReplace(s, " ", ""))},
                                "[[col:ui_font_faded_grey_beige]] 0[[/col]]"
                            )
                        }
                    )
                )
            }
        )
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")
    
    elem = read_xml_component('unit_information/res_shield')
    # language=javascript
    s = '''
        Format("%S",
            (a = StatList.FirstContext(Key == "stat_armour").ModifierIconList.FirstContext(Icon.Contains('modifier_icon_shield')) ) => {
                GetIfElse(
                    IsContextValid(a),
                    (us = a.Tooltip, li = us.Find("%"), fi = us.RFind(GetIfElse(IsLocChinese, Loc("chinese_shield_prefix"), ' '), li) + 1, uss = us.Substr(fi, li - fi), s = StringSubString(uss, 0) ) => {Format("[[img:%S]][[/img]][[col:green]]%S[[/col]]", a.Icon, StringReplace(s, " ", ""))},
                    ""
                )
            }
        )
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")
    
    elem = read_xml_component('unit_information/entity_hp')
    # language=javascript
    s = '''
        Format("[[img:ui/mod/icons/icon_entity_hp.png]][[/img]]%d", RoundFloat(HitPointsInitial / NumEntitiesInitial))
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")
    
    elem = read_xml_component('unit_information/spell_mastery')
    # language=javascript
    s = '''
        Format("[[img:ui/battle ui/ability_icons/spell_mastery.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="spell_mastery") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringReplace(StringSubString(uss, 0), " ", ""), sm = RoundFloat(ToNumber(s)) ) =>
                    {
                        GetIf(sm == 100, Format("[[col:ui_font_faded_grey_beige]]%d[[/col]]", sm))
                        + GetIf(sm > 100, Format("[[col:green]]%d[[/col]]", sm))
                        + GetIf(sm < 100, Format("[[col:red]]%d[[/col]]", sm))
                    },
                    ''
                )
            }
        )
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    add_element(xml, elem, "resistances_row")


def mod_postbattle_stat(xml):
    # common_list = find_by_id(xml, 'common_list')
    # common_list['offset'] = "0.00,43.00"

    elem = find_by_guid(xml, 'A8F852C0-5761-4850-AA7CC8469B4D72C8')
    elem['interactive'] = 'true'
    elem['disabled'] = 'false'
    # elem['offset'] = "20.00,27.00"
    # elem['docking'] = 'Bottom Left'
    # elem['dock_offset'] = '20.00,0.00'
    # elem['component_anchor_point'] = '0.00,1.00'
    
    #component image
    find_by_guid(xml, '4DBC2352-AB99-4828-948000457436C956').decompose()
    elem_state = find_by_guid(xml, '58FE73A0-79D1-4C3F-9F3FEF99F862DE40')
    elem_state['width'] = '55'
    elem_state['disabled'] = 'false'
    elem_state.component_text['textxoffset'] = '0.00,0.00'
    elem_state.component_text['texthalign'] = 'Center'
    elem_state.imagemetrics.image['width'] = '60'
    elem_state.imagemetrics.image['offset'] = '0.00,-12.00'
    

    # language=javascript
    s = '''
        (
            reg_key = 'klissan.hui.postbattle_stat',
            reg_value = GetIfElse(RegistryReadString(reg_key).Length == 0, 'gold', RegistryReadString(reg_key)),
            localised_colon_with_space = GetIfElse(IsLocChinese, Loc("chinese_colon"), ":"),
            tooltip = self.CurrentTooltip.Replace('||', Loc('LF')),
            kills_colon = tooltip.Find(localised_colon_with_space) + 1,
            kills_lf = tooltip.Find(Loc('LF')),
            kills_str = '[[img:ui/skins/default/icon_kills.png]][[/img]]' + tooltip.Substr(kills_colon, kills_lf - kills_colon).Replace(' ', ''),
            
            tooltip_dmg = tooltip.Substr(kills_lf + 1),
            dmg_colon = tooltip_dmg.Find(localised_colon_with_space) + 1,
            dmg_lf = tooltip_dmg.Find(Loc('LF')),
            damage_str = '[[img:ui/mod/icons/icon_explosive_damage.png]][[/img]]' + tooltip_dmg.Substr(dmg_colon, dmg_lf - dmg_colon).Replace(' ', ''),
            
            tooltip_value = tooltip_dmg.Substr(dmg_lf + 1),
            value_colon = tooltip_value.Find(localised_colon_with_space) + 1,
            value_lf = tooltip_value.Find(Loc('LF')),
            value_str = '[[img:ui/mod/icons/icon_stat_damage_base.png]][[/img]]' + tooltip_value.Substr(value_colon, value_lf - value_colon).Replace(' ', '')
        ) =>
        {
            GetIf(reg_value == 'kills', kills_str) + GetIf(reg_value == 'damage', damage_str) + GetIf(reg_value == 'gold', value_str)
        }
    '''
    create_context_callback(elem, 'ContextTextLabel','CcoStaticObject', s, {'update_constant': '1000'})

    # RegistryReadString('klissan.hui.postbattle_stat')
    # RegistryWriteString('klissan.hui.postbattle_stat', 'gold')

    # language=javascript
    s = '''
    (
        reg_key = 'klissan.hui.postbattle_stat',
        reg_value = GetIfElse(RegistryReadString(reg_key).Length == 0, 'gold', RegistryReadString(reg_key))
    ) =>
    {
        DoIfElse(reg_value == 'kills', RegistryWriteString(reg_key, 'damage'),
            DoIfElse(reg_value == 'damage', RegistryWriteString(reg_key, 'gold'),
                DoIf(reg_value == 'gold', RegistryWriteString(reg_key, 'kills'))
            )
        )
    }
    '''
    create_context_callback(elem, "ContextCommandLeftClick", "CcoStaticObject", s)
    
    #unit card
    # elem = find_by_guid(xml, '5024E82C-F70D-4A9A-92395C5FB4972019')
    # create_context_callback(elem, "ContextCommandLeftClick", "CcoStaticObject", s)
    
    
def mod_postbattle_stat_campaign(xml):
    elem = find_by_guid(xml, '78D3242B-A88A-4BD7-824F877E7F0B05B0')
    elem['interactive'] = 'true'
    elem['disabled'] = 'false'
    
    # language=javascript
    s = '''
        (
            reg_key = 'klissan.hui.postbattle_stat_campaign',
            reg_value = GetIfElse(RegistryReadString(reg_key).Length == 0, 'gold', RegistryReadString(reg_key)),
            localised_colon_with_space = GetIfElse(IsLocChinese, Loc("chinese_colon"), ":"),
            
            tooltip = self.CurrentTooltip.Replace('||', Loc('LF')),
            kills_colon = tooltip.Find(localised_colon_with_space) + 1,
            kills_lf = tooltip.Find(Loc('LF')),
            kills_str = '[[img:ui/skins/default/icon_kills.png]][[/img]]' + tooltip.Substr(kills_colon, kills_lf - kills_colon).Replace(' ', ''),

            tooltip_dmg = tooltip.Substr(kills_lf + 1),
            dmg_colon = tooltip_dmg.Find(localised_colon_with_space) + 1,
            dmg_lf = tooltip_dmg.Find(Loc('LF')),
            damage_str = '[[img:ui/mod/icons/icon_explosive_damage.png]][[/img]]' + tooltip_dmg.Substr(dmg_colon, dmg_lf - dmg_colon).Replace(' ', ''),

            tooltip_value = tooltip_dmg.Substr(dmg_lf + 1),
            value_colon = tooltip_value.Find(localised_colon_with_space) + 1,
            value_lf = tooltip_value.Find(Loc('LF')),
            value_str = '[[img:ui/mod/icons/icon_stat_damage_base.png]][[/img]]' + tooltip_value.Substr(value_colon, value_lf - value_colon).Replace(' ', '')
        ) =>
        {
            GetIf(reg_value == 'kills', kills_str) + GetIf(reg_value == 'damage', damage_str) + GetIf(reg_value == 'gold', value_str)
        }
    '''
    create_context_callback(elem, 'ContextTextLabel', 'CcoStaticObject', s, {'update_constant': '1000'})
    
    # RegistryReadString('klissan.hui.postbattle_stat')
    # RegistryWriteString('klissan.hui.postbattle_stat', 'gold')
    
    # language=javascript
    s = '''
    (
        reg_key = 'klissan.hui.postbattle_stat_campaign',
        reg_value = GetIfElse(RegistryReadString(reg_key).Length == 0, 'gold', RegistryReadString(reg_key))
    ) =>
    {
        DoIfElse(reg_value == 'kills', RegistryWriteString(reg_key, 'damage'),
            DoIfElse(reg_value == 'damage', RegistryWriteString(reg_key, 'gold'),
                DoIf(reg_value == 'gold', RegistryWriteString(reg_key, 'kills'))
            )
        )
    }
    '''
    create_context_callback(elem, "ContextCommandLeftClick", "CcoStaticObject", s)
    
    # unit card
    # elem = find_by_guid(xml, '5024E82C-F70D-4A9A-92395C5FB4972019')
    # create_context_callback(elem, "ContextCommandLeftClick", "CcoStaticObject", s)
    
    # component image
    find_by_guid(xml, 'D36D75B5-9CFB-43D6-BBAFD42D022E22A4').decompose()
    elem_state = find_by_guid(xml, 'ADD01F82-2A4B-44AD-9BC6D37A2F8F8152')
    elem_state.component_text['textxoffset'] = '-2.00,0.00'
    elem_state['disabled'] = 'false'
    
def mod_stats_fatigue(xml):
    # language=javascript
    s = '''
    (
        kv_rules = ScriptObjectContext('_kv_rules').TableValue,
        is_battle = IsContextValid(BattleRoot),
        ud = StoredContextFromParent("CcoUnitDetails"),
        buc = ud.BattleUnitContext,
        main_unit_record = ud.UnitRecordContext,
        land_unit_record = main_unit_record.UnitLandRecordContext,
        entity_record = land_unit_record.ManEntityContext,
        mount_record = land_unit_record.MountRecordContext,
        engine_record = land_unit_record.EngineRecordContext,
        articulated_record = land_unit_record.ArticulatedRecordContext,
        actual_entity_record = GetIfElse(IsContextValid(articulated_record), articulated_record.ArticulatedEntityContext,
            GetIfElse(IsContextValid(engine_record), engine_record.BattleEntityContext,
                GetIfElse(IsContextValid(mount_record), mount_record.Entity,
                    entity_record
                )
            )
        ),
        f_state = GetIf(is_battle, buc.FatigueState),
        cmp = GetIf(is_battle, ScriptObjectContext('fatigue_effects').TableValue.ValueForKey(Key)),
        is_valid_battle_context = is_battle && IsContextValid(buc),
        fatigue_coeff = GetIfElse(is_valid_battle_context, cmp[f_state].Value, 1.0),
        func_get_localization = ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value,

        stat_ws_tp = ud.StatContextFromKey("stat_weapon_damage").Tooltip.Replace('||', ''),
        rest_pattern = "]][[/img]]",

        BvL_png_pattern = "vs_large.png",
        BvL_png_i = stat_ws_tp.RFind(BvL_png_pattern) + BvL_png_pattern.Length + rest_pattern.Length,
        has_BvL = BvL_png_i > (BvL_png_pattern.Length + rest_pattern.Length),
        BvL_png_str = GetIf(has_BvL, stat_ws_tp.Substr(BvL_png_i)),
        BvL_colon_i = GetIf(has_BvL, BvL_png_str.Find(":") + 1),
        BvL_colon_str = GetIf(has_BvL, BvL_png_str.Substr(BvL_colon_i)),
        BvL_LF_i = GetIf(has_BvL, BvL_colon_str.Find(Loc("LF"))),
        BvL_EoL_i = GetIf(has_BvL, GetIfElse(BvL_LF_i > 0, BvL_LF_i, BvL_colon_str.Length)),
        BvL_uss = GetIf(has_BvL, BvL_colon_str.Substr(0, BvL_EoL_i)),
        BvL_s = GetIf(has_BvL, StringSubString(BvL_uss, 0).RemoveLeadingWhitespace),
        BvL = GetIf(has_BvL, RoundFloat(ToNumber(BvL_s))),

        Bvi_png_pattern = "vs_infantry.png",
        Bvi_png_i = stat_ws_tp.RFind(Bvi_png_pattern) + Bvi_png_pattern.Length + rest_pattern.Length,
        has_Bvi = Bvi_png_i > (Bvi_png_pattern.Length + rest_pattern.Length),
        Bvi_png_str = GetIf(has_Bvi, stat_ws_tp.Substr(Bvi_png_i)),
        Bvi_colon_i = GetIf(has_Bvi, Bvi_png_str.Find(":") + 1),
        Bvi_colon_str = GetIf(has_Bvi, Bvi_png_str.Substr(Bvi_colon_i)),
        Bvi_LF_i = GetIf(has_Bvi, Bvi_colon_str.Find(Loc("LF"))),
        Bvi_EoL_i = GetIf(has_Bvi, GetIfElse(Bvi_LF_i > 0, Bvi_LF_i, Bvi_colon_str.Length)),
        Bvi_uss = GetIf(has_Bvi, Bvi_colon_str.Substr(0, Bvi_EoL_i)),
        Bvi_s = GetIf(has_Bvi, StringSubString(Bvi_uss, 0).RemoveLeadingWhitespace),
        Bvi = GetIf(has_Bvi, RoundFloat(ToNumber(Bvi_s)))
    ) =>
    {
        GetIf(Key == "stat_armour",
            (
                mass_record = RoundFloat(actual_entity_record.Mass),
                mass = RoundFloat(ud.Mass),
                mass_color = GetIfElse(mass > mass_record, 'green', GetIfElse(mass < mass_record, 'red', 'ui_font_faded_grey_beige')),
                mass_str = Format("[[img:ui/mod/icons/icon_stat_mass.png]][[/img]][[col:%s]]%d[[/col]]", mass_color, mass),
                r_armour = DisplayedValue,
                f_armour = RoundFloat(r_armour),
                f_armour_str = Format("[[img:ui/mod/icons/icon_stat_armour.png]][[/img]]%d", f_armour),
                armour_roll_lower_cap = kv_rules.ValueForKey('armour_roll_lower_cap'),
                avg_armour_res = GetIf(f_armour <= 100, RoundFloat((1 + armour_roll_lower_cap) / 2 * f_armour))
                    + GetIf(100 < f_armour && f_armour < 200,
                        (
                            half = armour_roll_lower_cap * f_armour,
                            diff = f_armour - half,
                            lh = 100 - half,
                            rh = f_armour - 100
                        ) => { RoundFloat((lh / diff) * (half + 100) / 2 + (rh / diff) * 100) }
                    )
                    + GetIf(f_armour >= 200, 100)
            ) =>
            {
                Format("%S %S [%d%]  ", mass_str, f_armour_str, avg_armour_res)
            }
        ) +
        GetIf(Key == "stat_morale",
             GetIfElse(buc.CapturePower > 0, Format("[[img:ui/skins/default/icon_capture_point.png]][[/img]][[col:ui_font_faded_grey_beige]]%.1f[[/col]] ", buc.CapturePower), "") + Format("[[img:ui/mod/icons/icon_stat_morale.png]][[/img]]%d  ", RoundFloat(DisplayedValue) )
        ) +
        GetIf(Key == "scalar_speed", Format("[[img:ui/mod/icons/icon_stat_speed.png]][[/img]]%d  ", RoundFloat(DisplayedValue)) ) +
        GetIf(Key == "stat_melee_attack",
            (
                r_ma = DisplayedValue,
                f_ma = RoundFloat(r_ma),
                f_ma_str = Format("[[img:ui/mod/icons/icon_stat_melee_attack.png]][[/img]]%d", f_ma),
                f_ma_BvL = f_ma + BvL,
                f_ma_BvL_str = GetIfElse(has_BvL, Format("[[img:ui/mod/icons/modifier_icon_bonus_vs_large.png]][[/img]]%d", f_ma_BvL), ""),
                f_ma_Bvi = f_ma + Bvi,
                f_ma_Bvi_str = GetIfElse(has_Bvi, Format("[[img:ui/mod/icons/modifier_icon_bonus_vs_infantry.png]][[/img]]%d", f_ma_Bvi), "")
            ) =>
            {
                Format(" %S%S %S  ", f_ma_BvL_str, f_ma_Bvi_str, f_ma_str)
            }
        ) +
        GetIf(Key == "stat_melee_defence",
            (
                r_md = DisplayedValue,
                f_md = RoundFloat(r_md),
                f_md_str = Format("[[img:ui/mod/icons/icon_stat_defence.png]][[/img]]%d", f_md),
                has_flanking_immune = IsContextValid(ud.AbilityDetailsList.FirstContext(Key == 'flanking_immune')),
                flank_md_coeff = GetIfElse(has_flanking_immune, 1.0, kv_rules.ValueForKey('melee_defence_direction_penalty_coefficient_flank')),
                flank_md = RoundFloat(f_md * flank_md_coeff),
                flank_md_str = Format("[[img:ui/mod/icons/icon_stat_defence_flank.png]][[/img]]%d", flank_md),
                rear_md = RoundFloat(f_md * kv_rules.ValueForKey('melee_defence_direction_penalty_coefficient_rear')),
                rear_md_str = Format("[[img:ui/mod/icons/icon_stat_defence_rear.png]][[/img]]%d", rear_md)
            ) =>
            {
                Format("%S %S %S  ", rear_md_str, flank_md_str, f_md_str)
            }
        ) +
        GetIf(Key == "stat_weapon_damage",
            (
                bwd_png_pattern = "stat_damage_base.png",
                bwd_png_i = stat_ws_tp.RFind(bwd_png_pattern) + bwd_png_pattern.Length + rest_pattern.Length,
                has_bwd = bwd_png_i > (bwd_png_pattern.Length + rest_pattern.Length),
                bwd_png_str = GetIf(has_bwd, stat_ws_tp.Substr(bwd_png_i)),
                bwd_colon_i = GetIf(has_bwd, bwd_png_str.Find(":") + 1),
                bwd_colon_str = GetIf(has_bwd, bwd_png_str.Substr(bwd_colon_i)),
                bwd_LF_i = GetIf(has_bwd, bwd_colon_str.Find(Loc("LF"))),
                bwd_EoL_i = GetIf(has_bwd, GetIfElse(bwd_LF_i > 0, bwd_LF_i, bwd_colon_str.Length)),
                bwd_uss = GetIf(has_bwd, bwd_colon_str.Substr(0, bwd_EoL_i)),
                bwd_s = GetIf(has_bwd, StringSubString(bwd_uss, 0).RemoveLeadingWhitespace),
                bwd = GetIf(has_bwd, RoundFloat(ToNumber(bwd_s))),

                apwd_png_pattern = "icon_armour_piercing.png",
                apwd_png_i = stat_ws_tp.RFind(apwd_png_pattern) + apwd_png_pattern.Length + rest_pattern.Length,
                has_apwd = apwd_png_i > (apwd_png_pattern.Length + rest_pattern.Length),
                apwd_png_str = GetIf(has_apwd, stat_ws_tp.Substr(apwd_png_i)),
                apwd_colon_i = GetIf(has_apwd, apwd_png_str.Find(":") + 1),
                apwd_colon_str = GetIf(has_apwd, apwd_png_str.Substr(apwd_colon_i)),
                apwd_LF_i = GetIf(has_apwd, apwd_colon_str.Find(Loc("LF"))),
                apwd_EoL_i = GetIf(has_apwd, GetIfElse(apwd_LF_i > 0, apwd_LF_i, apwd_colon_str.Length)),
                apwd_uss = GetIf(has_apwd, apwd_colon_str.Substr(0, apwd_EoL_i)),
                apwd_s = GetIf(has_apwd, StringSubString(apwd_uss, 0).RemoveLeadingWhitespace),
                apwd = GetIf(has_apwd, RoundFloat(ToNumber(apwd_s))),

                bwd_fatigue_coeff = GetIfElse(is_valid_battle_context, ScriptObjectContext('fatigue_effects').TableValue.ValueForKey('stat_melee_damage_base')[f_state].Value, 1.0),
                f_bwd = RoundFloat(bwd_fatigue_coeff * bwd),
                f_bwd_str = Format("[[img:ui/mod/icons/icon_stat_damage_base.png]][[/img]]%d", f_bwd),
                apwd_fatigue_coeff = GetIfElse(is_valid_battle_context, ScriptObjectContext('fatigue_effects').TableValue.ValueForKey('stat_melee_damage_ap')[f_state].Value, 1.0),
                f_apwd = RoundFloat(apwd_fatigue_coeff * apwd),
                f_apwd_str = Format("[[img:ui/mod/icons/icon_stat_melee_damage_ap.png]][[/img]]%d", f_apwd),

                BvL_str = GetIfElse(has_BvL, Format("[[img:ui/mod/icons/modifier_icon_bonus_vs_large.png]][[/img]]%d", BvL), ""),
                Bvi_str = GetIfElse(has_Bvi, Format("[[img:ui/mod/icons/modifier_icon_bonus_vs_infantry.png]][[/img]]%d", Bvi), ""),
                
                mwc = ud.UnitRecordContext.UnitLandRecordContext.PrimaryMeleeWeaponContext,
                total_db_dmg = mwc.DamageContext.Value + mwc.ApDamageContext.Value,
                ap_ratio = mwc.ApDamageContext.Value / total_db_dmg,
                ap_ratio_set = ScriptObjectContext('unit_info_ui.melee_ap_ratio').SetStringValue(Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_ap_ratio')), ap_ratio)),
                
                f_BvL_bwd = GetIf(has_BvL, f_bwd + RoundFloat(BvL * (1.0 - ap_ratio))),
                f_BvL_apwd = GetIf(has_BvL, f_apwd + RoundFloat(BvL * ap_ratio)),
                f_BvL_wd_str = GetIfElse(has_BvL, Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_melee_dmg_bonus')), 'large', f_BvL_bwd, f_BvL_apwd, f_BvL_bwd + f_BvL_apwd), ''),
                set_f_BvL_wd_str = ScriptObjectContext('unit_info_ui.melee_damage_BvL').SetStringValue(f_BvL_wd_str),
                
                f_Bvi_bwd = GetIf(has_Bvi, f_bwd + RoundFloat(Bvi * (1.0 - ap_ratio))),
                f_Bvi_apwd = GetIf(has_Bvi, f_apwd + RoundFloat(Bvi * ap_ratio)),
                f_Bvi_wd_str = GetIfElse(has_Bvi, Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_melee_dmg_bonus')), 'infantry', f_Bvi_bwd, f_Bvi_apwd, f_Bvi_bwd + f_Bvi_apwd), ''),
                set_f_Bvi_wd_str = ScriptObjectContext('unit_info_ui.melee_damage_Bvi').SetStringValue(f_Bvi_wd_str),
                
                set_total_wd = ScriptObjectContext('unit_info_ui.total_weapon_damage').SetNumericValue(f_bwd + f_apwd)
            ) =>
            {
                Format(" %S%S %S%S  ", BvL_str, Bvi_str, f_bwd_str, f_apwd_str)
            }
        ) +
        GetIf(Key == "stat_charge_bonus",
            (
                stat_morale_tp = ud.StatContextFromKey("stat_morale").Tooltip.Replace('||', ''),
                charging_png_i = stat_morale_tp.RFind("[[img:ui/skins/default/icon_stat_charge_bonus.png"),
                is_charging = charging_png_i > 0,
                charging_half_str = GetIf(is_charging, stat_morale_tp.Substr(charging_png_i-1)),
                charging_colon_i = GetIf(is_charging, charging_half_str.Find(": ")),
                charging_str = Format('[[col:ui_font_faded_grey_beige]]%S[[/col]]', GetIfElse(is_charging, EvaluateExpression(Format(func_get_localization, 'charging_str')), '')),
                braced = ud.BattleUnitContext.StatusList.FirstContext(Key == 'braced'),
                bracing_str = GetIfElse(IsContextValid(braced), Format('[[img:%S]][[/img]][[col:ui_font_faded_grey_beige]]%S[[/col]]', braced.IconPath, braced.Tooltip), ''),

                r_cb = DisplayedValue,
                f_cb = RoundFloat(DisplayedValue),
                f_cb_str = Format("%S%S [[img:ui/mod/icons/icon_stat_charge_bonus.png]][[/img]]%d  ", charging_str, bracing_str, f_cb)
            ) =>
            {
                f_cb_str
            }
        ) +
        GetIf(Key == "stat_ammo",
            (
                stat_mdot_tp = ud.StatContextFromKey("stat_missile_damage_over_time").Tooltip.Replace('||', ''),

                rt_png_pattern = "icon_stat_reload_time.png",
                rt_png_i = stat_mdot_tp.RFind(rt_png_pattern),
                has_rt = rt_png_i > 0,
                rt_png_str = GetIf(has_rt, stat_mdot_tp.Substr(rt_png_i)),
                rt_colon_i = GetIf(has_rt, rt_png_str.Find(":") + 1),
                rt_colon_str = GetIf(has_rt, rt_png_str.Substr(rt_colon_i)),
                rt_LF_i = GetIf(has_rt, rt_colon_str.Find(" ")),
                rt_EoL_i = GetIf(has_rt, GetIfElse(rt_LF_i > 0, rt_LF_i, rt_colon_str.Length)),
                rt_uss = GetIf(has_rt, rt_colon_str.Substr(0, rt_EoL_i)),
                rt_s = GetIf(has_rt, StringSubString(rt_uss, 0).RemoveLeadingWhitespace),
                rt = GetIf(has_rt, ToNumber(rt_s)),

                bs_png_pattern = "burst_size.png",
                bs_png_i = stat_mdot_tp.RFind(bs_png_pattern),
                has_bs = bs_png_i > 0,
                bs_png_str = GetIf(has_bs, stat_mdot_tp.Substr(bs_png_i)),
                bs_colon_i = GetIf(has_bs, bs_png_str.Find(":") + 1),
                bs_colon_str = GetIf(has_bs, bs_png_str.Substr(bs_colon_i)),
                bs_LF_i = GetIf(has_bs, bs_colon_str.Find(Loc("LF"))),
                bs_EoL_i = GetIf(has_bs, GetIfElse(bs_LF_i > 0, bs_LF_i, bs_colon_str.Length)),
                bs_uss = GetIf(has_bs, bs_colon_str.Substr(0, bs_EoL_i)),
                bs_s = GetIf(has_bs, StringSubString(bs_uss, 0).RemoveLeadingWhitespace),
                bs = GetIf(has_bs, RoundFloat(ToNumber(bs_s))),

                nop_png_pattern = "number_of_projectiles.png",
                nop_png_i = stat_mdot_tp.RFind(nop_png_pattern),
                has_nop = nop_png_i > 0,
                nop_png_str = GetIf(has_nop, stat_mdot_tp.Substr(nop_png_i)),
                nop_colon_i = GetIf(has_nop, nop_png_str.Find(":") + 1),
                nop_colon_str = GetIf(has_nop, nop_png_str.Substr(nop_colon_i)),
                nop_LF_i = GetIf(has_nop, nop_colon_str.Find(Loc("LF"))),
                nop_EoL_i = GetIf(has_nop, GetIfElse(nop_LF_i > 0, nop_LF_i, nop_colon_str.Length)),
                nop_uss = GetIf(has_nop, nop_colon_str.Substr(0, nop_EoL_i)),
                nop_s = GetIf(has_nop, StringSubString(nop_uss, 0).RemoveLeadingWhitespace),
                nop = GetIf(has_nop, RoundFloat(ToNumber(nop_s))),

                spv_png_pattern = "shots_per_volley.png",
                spv_png_i = stat_mdot_tp.RFind(spv_png_pattern),
                has_spv = spv_png_i > 0,
                spv_png_str = GetIf(has_spv, stat_mdot_tp.Substr(spv_png_i)),
                spv_colon_i = GetIf(has_spv, spv_png_str.Find(":") + 1),
                spv_colon_str = GetIf(has_spv, spv_png_str.Substr(spv_colon_i)),
                spv_LF_i = GetIf(has_spv, spv_colon_str.Find(Loc("LF"))),
                spv_EoL_i = GetIf(has_spv, GetIfElse(spv_LF_i > 0, spv_LF_i, spv_colon_str.Length)),
                spv_uss = GetIf(has_spv, spv_colon_str.Substr(0, spv_EoL_i)),
                spv_s = GetIf(has_spv, StringSubString(spv_uss, 0).RemoveLeadingWhitespace),
                spv = GetIf(has_spv, RoundFloat(ToNumber(spv_s))),

                bs_str = GetIfElse(has_bs, Format("[[img:ui/mod/icons/burst_size.png]][[/img]][[col:ui_font_faded_grey_beige]]%d[[/col]]", bs), ""),
                nop_str = GetIfElse(has_nop, Format("[[img:ui/mod/icons/number_of_projectiles.png]][[/img]][[col:ui_font_faded_grey_beige]]%d[[/col]]", nop), ""),
                spv_str = GetIfElse(has_spv, Format("[[img:ui/mod/icons/shots_per_volley.png]][[/img]][[col:ui_font_faded_grey_beige]]%d[[/col]]", spv), ""),

                ammo_str = Format("[[img:ui/mod/icons/icon_stat_ammo.png]][[/img]]%d", RoundFloat(DisplayedValue)),
                rt_str = Format("[[img:ui/mod/icons/icon_stat_reload_time.png]][[/img]][[col:ui_font_faded_grey_beige]]%.1f[[/col]]", rt),
                
                total_ammo = bs + nop + spv,
                set_total_ammo = ScriptObjectContext('unit_info_ui.total_ammo').SetNumericValue(GetIfElse(total_ammo > 0, total_ammo, 1))
            ) =>
            {
                Format(" %S%S%S %S %S  ", bs_str, nop_str, spv_str, rt_str, ammo_str)
            }
        ) +
        GetIf(Key == "scalar_missile_range", Format("[[img:ui/mod/icons/icon_distance_to_target.png]][[/img]]%d  ", RoundFloat(DisplayedValue))) +
        GetIf(Key == "stat_missile_damage_over_time",
            (
                tp = Tooltip.Replace('||', ''),

                mdb_png_pattern = "icon_stat_ranged_damage_base.png",
                mdb_png_i = tp.RFind(mdb_png_pattern),
                has_mdb = mdb_png_i > 0,
                mdb_png_str = GetIf(has_mdb, tp.Substr(mdb_png_i)),
                mdb_colon_i = GetIf(has_mdb, mdb_png_str.Find(":") + 1),
                mdb_colon_str = GetIf(has_mdb, mdb_png_str.Substr(mdb_colon_i)),
                mdb_LF_i = GetIf(has_mdb, mdb_colon_str.Find(Loc("LF"))),
                mdb_EoL_i = GetIf(has_mdb, GetIfElse(mdb_LF_i > 0, mdb_LF_i, mdb_colon_str.Length)),
                mdb_uss = GetIf(has_mdb, mdb_colon_str.Substr(0, mdb_EoL_i)),
                mdb_s = GetIf(has_mdb, StringSubString(mdb_uss, 0).RemoveLeadingWhitespace),
                mdb = GetIf(has_mdb, RoundFloat(ToNumber(mdb_s))),

                mdap_png_pattern = "modifier_icon_armour_piercing_ranged.png",
                mdap_png_i = tp.RFind(mdap_png_pattern),
                has_mdap = mdap_png_i > 0,
                mdap_png_str = GetIf(has_mdap, tp.Substr(mdap_png_i)),
                mdap_colon_i = GetIf(has_mdap, mdap_png_str.Find(":") + 1),
                mdap_colon_str = GetIf(has_mdap, mdap_png_str.Substr(mdap_colon_i)),
                mdap_LF_i = GetIf(has_mdap, mdap_colon_str.Find(Loc("LF"))),
                mdap_EoL_i = GetIf(has_mdap, GetIfElse(mdap_LF_i > 0, mdap_LF_i, mdap_colon_str.Length)),
                mdap_uss = GetIf(has_mdap, mdap_colon_str.Substr(0, mdap_EoL_i)),
                mdap_s = GetIf(has_mdap, StringSubString(mdap_uss, 0).RemoveLeadingWhitespace),
                mdap = GetIf(has_mdap, RoundFloat(ToNumber(mdap_s))),

                medb_png_pattern = "icon_explosive_damage.png",
                medb_png_i = tp.RFind(medb_png_pattern),
                has_medb = medb_png_i > 0,
                medb_png_str = GetIf(has_medb, tp.Substr(medb_png_i)),
                medb_colon_i = GetIf(has_medb, medb_png_str.Find(":") + 1),
                medb_colon_str = GetIf(has_medb, medb_png_str.Substr(medb_colon_i)),
                medb_LF_i = GetIf(has_medb, medb_colon_str.Find(Loc("LF"))),
                medb_EoL_i = GetIf(has_medb, GetIfElse(medb_LF_i > 0, medb_LF_i, medb_colon_str.Length)),
                medb_uss = GetIf(has_medb, medb_colon_str.Substr(0, medb_EoL_i)),
                medb_s = GetIf(has_medb, StringSubString(medb_uss, 0).RemoveLeadingWhitespace),
                medb = GetIf(has_medb, RoundFloat(ToNumber(medb_s))),

                medap_png_pattern = "icon_stat_explosive_armour_piercing_damage.png",
                medap_png_i = tp.RFind(medap_png_pattern),
                has_medap = medap_png_i > 0,
                medap_png_str = GetIf(has_medap, tp.Substr(medap_png_i)),
                medap_colon_i = GetIf(has_medap, medap_png_str.Find(":") + 1),
                medap_colon_str = GetIf(has_medap, medap_png_str.Substr(medap_colon_i)),
                medap_LF_i = GetIf(has_medap, medap_colon_str.Find(Loc("LF"))),
                medap_EoL_i = GetIf(has_medap, GetIfElse(medap_LF_i > 0, medap_LF_i, medap_colon_str.Length)),
                medap_uss = GetIf(has_medap, medap_colon_str.Substr(0, medap_EoL_i)),
                medap_s = GetIf(has_medap, StringSubString(medap_uss, 0).RemoveLeadingWhitespace),
                medap = GetIf(has_medap, RoundFloat(ToNumber(medap_s))),

                mBvL_png_pattern = "vs_large.png",
                mBvL_png_i = tp.RFind(mBvL_png_pattern),
                has_mBvL = mBvL_png_i > 0,
                mBvL_png_str = GetIf(has_mBvL, tp.Substr(mBvL_png_i)),
                mBvL_colon_i = GetIf(has_mBvL, mBvL_png_str.Find(":") + 1),
                mBvL_colon_str = GetIf(has_mBvL, mBvL_png_str.Substr(mBvL_colon_i)),
                mBvL_LF_i = GetIf(has_mBvL, mBvL_colon_str.Find(Loc("LF"))),
                mBvL_EoL_i = GetIf(has_mBvL, GetIfElse(mBvL_LF_i > 0, mBvL_LF_i, mBvL_colon_str.Length)),
                mBvL_uss = GetIf(has_mBvL, mBvL_colon_str.Substr(0, mBvL_EoL_i)),
                mBvL_s = GetIf(has_mBvL, StringSubString(mBvL_uss, 0).RemoveLeadingWhitespace),
                mBvL = GetIfElse(has_mBvL, RoundFloat(ToNumber(mBvL_s)), 0),
                set_BvL = ScriptObjectContext('unit_info_ui.range_BvL').SetNumericValue(mBvL),

                mBvi_png_pattern = "vs_infantry.png",
                mBvi_png_i = tp.RFind(mBvi_png_pattern),
                has_mBvi = mBvi_png_i > 0,
                mBvi_png_str = GetIf(has_mBvi, tp.Substr(mBvi_png_i)),
                mBvi_colon_i = GetIf(has_mBvi, mBvi_png_str.Find(":") + 1),
                mBvi_colon_str = GetIf(has_mBvi, mBvi_png_str.Substr(mBvi_colon_i)),
                mBvi_LF_i = GetIf(has_mBvi, mBvi_colon_str.Find(Loc("LF"))),
                mBvi_EoL_i = GetIf(has_mBvi, GetIfElse(mBvi_LF_i > 0, mBvi_LF_i, mBvi_colon_str.Length)),
                mBvi_uss = GetIf(has_mBvi, mBvi_colon_str.Substr(0, mBvi_EoL_i)),
                mBvi_s = GetIf(has_mBvi, StringSubString(mBvi_uss, 0).RemoveLeadingWhitespace),
                mBvi = GetIfElse(has_mBvi, RoundFloat(ToNumber(mBvi_s)), 0),
                set_Bvi = ScriptObjectContext('unit_info_ui.range_Bvi').SetNumericValue(mBvi),

                fe = db_lookup.ChildContext("fatigue_effects"),

                mdb_fatigue_coeff = GetIfElse(is_valid_battle_context, ScriptObjectContext('fatigue_effects').TableValue.ValueForKey('scalar_missile_damage_base')[f_state].Value, 1.0),
                f_mdb = RoundFloat(mdb_fatigue_coeff * mdb),
                f_mdb_str = Format("[[img:ui/mod/icons/icon_stat_ranged_damage_base.png]][[/img]]%d", f_mdb),
                set_f_mdb = ScriptObjectContext('unit_info_ui.range_damage_base').SetNumericValue(f_mdb),

                mdap_fatigue_coeff = GetIfElse(is_valid_battle_context, ScriptObjectContext('fatigue_effects').TableValue.ValueForKey('scalar_missile_damage_ap')[f_state].Value, 1.0),
                f_mdap = RoundFloat(mdap_fatigue_coeff * mdap),
                f_mdap_str = Format("[[img:ui/mod/icons/modifier_icon_armour_piercing_ranged.png]][[/img]]%d", f_mdap),
                set_f_mdap = ScriptObjectContext('unit_info_ui.range_damage_ap').SetNumericValue(f_mdap),

                medb_fatigue_coeff = GetIfElse(is_valid_battle_context, ScriptObjectContext('fatigue_effects').TableValue.ValueForKey('scalar_missile_explosion_damage_base')[f_state].Value, 1.0),
                f_medb = GetIfElse(has_medb, RoundFloat(medb_fatigue_coeff * medb), 0),
                f_medb_str = GetIfElse(has_medb, Format("[[img:ui/mod/icons/icon_explosive_damage.png]][[/img]]%d", f_medb), ""),
                set_f_medb = ScriptObjectContext('unit_info_ui.range_damage_explosion_base').SetNumericValue(f_medb),

                medap_fatigue_coeff = GetIfElse(is_valid_battle_context, ScriptObjectContext('fatigue_effects').TableValue.ValueForKey('scalar_missile_explosion_damage_ap')[f_state].Value, 1.0),
                f_medap = GetIfElse(has_medap, RoundFloat(medap_fatigue_coeff * medap), 0),
                f_medap_str = GetIfElse(has_medap, Format("[[img:ui/mod/icons/icon_stat_explosive_armour_piercing_damage.png]][[/img]]%d", f_medap), ""),
                set_f_medap = ScriptObjectContext('unit_info_ui.range_damage_explosion_ap').SetNumericValue(f_medap),

                mBvL_str = GetIfElse(has_mBvL, Format("[[img:ui/mod/icons/modifier_icon_bonus_vs_large.png]][[/img]]%d", mBvL), ""),
                mBvi_str = GetIfElse(has_mBvi, Format("[[img:ui/mod/icons/modifier_icon_bonus_vs_infantry.png]][[/img]]%d", mBvi), ""),
                
                mwc = ud.UnitRecordContext.UnitLandRecordContext.PrimaryMissileWeaponContext.ProjectileContextList[0] + Do('TODO: use actual projectile?, Check if engine has projectile'),
                total_db_dmg = mwc.DamageContext.Value + mwc.ApDamageContext.Value,
                ap_ratio = mwc.ApDamageContext.Value / total_db_dmg,
                ap_ratio_set = ScriptObjectContext('unit_info_ui.range_ap_ratio').SetNumericValue(ap_ratio)
            ) =>
            {
                Format("%S%S%S%S%S%S  ", mBvL_str, mBvi_str, f_mdb_str, f_mdap_str, f_medb_str, f_medap_str)
            }
        )
    }
    '''
    cb = set_context_callback(find_by_guid(xml, 'F0F1DC3F-6E56-4627-81284E05CEE668E7'), 'ContextNumberFormatter', s)
    cb['callback_id'] = 'ContextTextLabel'
    
    # language=javascript
    s = '''
        GetIf(Key == "stat_armour", ModifierIconList.Filter(!Icon.Contains('icon_shield')) ) +
        GetIf(Key == "stat_morale", ModifierIconList) +
        GetIf(Key == "scalar_speed", ModifierIconList) +
        GetIf(Key == "stat_melee_attack", ModifierIconList) +
        GetIf(Key == "stat_melee_defence", ModifierIconList) +
        GetIf(Key == "stat_weapon_damage", ModifierIconList.Filter( !(Icon.Contains('armour_piercing') || Icon.Contains('vs_large') || Icon.Contains('vs_infantry') ) )) +
        GetIf(Key == "stat_charge_bonus", ModifierIconList) +
        GetIf(Key == "stat_ammo", ModifierIconList) +
        GetIf(Key == "scalar_missile_range", ModifierIconList) +
        GetIf(Key == "stat_missile_damage_over_time", ModifierIconList.Filter( !(Icon.Contains('armour_piercing') || Icon.Contains('vs_large') || Icon.Contains('vs_infantry') ) ))
    '''
    set_context_callback(find_by_id(xml, 'mod_icon_list'), 'ContextList', s)
    
    set_context_callback(find_by_id(xml, 'stat_name'), 'ContextTextLabel', '""')

    # language=javascript
    s = '''
        (
            kv_rules = ScriptObjectContext('_kv_rules').TableValue,
            md_flank = kv_rules.ValueForKey('melee_defence_direction_penalty_coefficient_flank'),
            md_rear = kv_rules.ValueForKey('melee_defence_direction_penalty_coefficient_rear'),
            md_flank_red = RoundFloat((1 - md_flank) * 100),
            md_rear_red = RoundFloat((1 - md_rear) * 100),
            ud = StoredContextFromParent("CcoUnitDetails"),
            main_unit_record = ud.UnitRecordContext,
            land_unit_record = main_unit_record.UnitLandRecordContext,
            entity_record = land_unit_record.ManEntityContext,
            mount_record = land_unit_record.MountRecordContext,
            engine_record = land_unit_record.EngineRecordContext,
            articulated_record = land_unit_record.ArticulatedRecordContext,
            actual_entity_record = GetIfElse(IsContextValid(articulated_record), articulated_record.ArticulatedEntityContext,
                GetIfElse(IsContextValid(engine_record), engine_record.BattleEntityContext,
                    GetIfElse(IsContextValid(mount_record), mount_record.Entity,
                        entity_record
                    )
                )
            ),
            func_get_localization = ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value
        ) =>
        Tooltip
        + GetIf(Key == "stat_armour",
            Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_armour')), kv_rules.ValueForKey('armour_roll_lower_cap'))
            + Loc('LF')
            + GetIf(IsContextValid(entity_record), Format('Entity: %d' + Loc('LF'), RoundFloat(entity_record.Mass)))
            + GetIf(IsContextValid(mount_record), Format('Mount: %d' + Loc('LF'), RoundFloat(mount_record.Entity.Mass)))
            + GetIf(IsContextValid(engine_record), Format('Engine: %d' + Loc('LF'), RoundFloat(engine_record.BattleEntityContext.Mass)))
            + GetIf(IsContextValid(articulated_record), Format('Articulated: %d' + Loc('LF'), RoundFloat(articulated_record.ArticulatedEntityContext.Mass)))
        )
         + GetIf(Key == "scalar_speed", 
            + Loc('LF') 
            + Loc('LF') 
            + Format('Base Walk Speed: %f' + Loc('LF'), actual_entity_record.WalkSpeed) 
            + Format('Base Charge Speed: %f' + Loc('LF'), actual_entity_record.ChargeSpeed) 
            + Format('Base Fly Speed: %f' + Loc('LF'), actual_entity_record.FlySpeed) 
            + Format('Base Fly Charge Speed: %f' + Loc('LF'), actual_entity_record.FlyingChargeSpeed) 
            + Format('Base Acceleration: %f' + Loc('LF'), actual_entity_record.Acceleration) 
            + Format('Base Deceleration: %f' + Loc('LF'), actual_entity_record.Deceleration)
            + Format('Base Turn Speed: %f' + Loc('LF'), actual_entity_record.TurnSpeed) 
            + Format('Base Strafe Speed: %f' + Loc('LF'), actual_entity_record.StrafeSpeed)
            + Format('Base Speed Context: %f' + Loc('LF'), actual_entity_record.RunSpeedContext.ValueBase)
            + Format('Base Speed DB: %f' + Loc('LF'),  DatabaseRecordContext("CcoBattleEntityRecord", actual_entity_record.Key).RunSpeedContext.ValueBase)
        )
        + GetIf(Key == "stat_melee_attack",
            (
                mwc = ud.UnitRecordContext.UnitLandRecordContext.PrimaryMeleeWeaponContext,
                sama = mwc.SplashAttackMaxAttacks,
                sats = mwc.SplashAttackTargetSize + '[[col:yellow]]CA pls fix[[/col]]',
                camt = mwc.CollisionAttackMaxTargets,
                camtc = mwc.CollisionAttackMaxTargetsCooldown,
                splash_str = GetIfElse(sama > 0, Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_melee_attack_splash')), sats, sama), ''),
                collision_str = GetIfElse(camt > 0, Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_melee_attack_collision')), camt, camtc), '')
            ) => {Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_melee_attack')), mwc.WeaponLength, splash_str, collision_str)}
        )
        + GetIf(Key == "stat_melee_defence", Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_melee_defence')), md_rear_red, md_flank_red))
        + Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_ui')), RoundFloat(ValueBase), RoundFloat(DisplayedValue))
        + GetIf(Key == "stat_weapon_damage",
            Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_dmg_per_hit')), RoundFloat(ScriptObjectContext('unit_info_ui.total_weapon_damage').NumericValue))
            + ScriptObjectContext('unit_info_ui.melee_ap_ratio').StringValue
            + ScriptObjectContext('unit_info_ui.melee_damage_BvL').StringValue
            + ScriptObjectContext('unit_info_ui.melee_damage_Bvi').StringValue
        )
        + GetIf(Key == "stat_missile_damage_over_time",
            (
                ap_ratio = ScriptObjectContext('unit_info_ui.range_ap_ratio').NumericValue,
                mBvL = RoundFloat(ScriptObjectContext('unit_info_ui.range_BvL').NumericValue),
                mBvi = RoundFloat(ScriptObjectContext('unit_info_ui.range_Bvi').NumericValue),
                has_mBvL = mBvL > 0,
                has_mBvi = mBvi > 0,
                f_mdb = RoundFloat(ScriptObjectContext('unit_info_ui.range_damage_base').NumericValue),
                f_mdap = RoundFloat(ScriptObjectContext('unit_info_ui.range_damage_ap').NumericValue),
                f_medb = RoundFloat(ScriptObjectContext('unit_info_ui.range_damage_explosion_base').NumericValue),
                f_medap = RoundFloat(ScriptObjectContext('unit_info_ui.range_damage_explosion_ap').NumericValue),
                tammo = RoundFloat(ScriptObjectContext('unit_info_ui.total_ammo').NumericValue),
                n_entities = ud.NumEntities,
                n_entities_ammo = n_entities * tammo,
                
                projectile_dmg = f_mdb + f_mdap + f_medb + f_medap,
                projectile_dmg_BvL = f_mdb + f_mdap + f_medb + f_medap + mBvL,
                projectile_dmg_Bvi = f_mdb + f_mdap + f_medb + f_medap + mBvi,
                
                shot_dmg = projectile_dmg * tammo,
                shot_dmg_BvL = projectile_dmg_BvL * tammo,
                shot_dmg_Bvi = projectile_dmg_Bvi * tammo,
                
                volley_dmg = shot_dmg * n_entities,
                volley_dmg_BvL = shot_dmg_BvL * n_entities,
                volley_dmg_Bvi = shot_dmg_Bvi * n_entities,
                
                func_format_range_damage_string = ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('format_range_damage_string').Value
            ) =>
            {
                Format(EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_ap_ratio')), ap_ratio)
                + EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_projectile_damage'))
                + EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, '', 0, f_mdb, f_mdap, f_medb, f_medap, projectile_dmg))
                + GetIf(has_mBvL, EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, 'large', mBvL, f_mdb, f_mdap, f_medb, f_medap, projectile_dmg_BvL)))
                + GetIf(has_mBvi, EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, 'infantry', mBvi, f_mdb, f_mdap, f_medb, f_medap, projectile_dmg_Bvi)))
                + GetIf(
                    tammo > 1,
                    EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_entity_shot_damage'))
                    + EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, '', 0, f_mdb * tammo, f_mdap * tammo, f_medb * tammo, f_medap * tammo, projectile_dmg * tammo))
                    + GetIf(has_mBvL, EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, 'large', mBvL * tammo, f_mdb * tammo, f_mdap * tammo, f_medb * tammo, f_medap * tammo, projectile_dmg_BvL * tammo)))
                    + GetIf(has_mBvi, EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, 'infantry', mBvi * tammo, f_mdb * tammo, f_mdap * tammo, f_medb * tammo, f_medap * tammo, projectile_dmg_Bvi * tammo)))
                )
                + GetIf(
                    n_entities > 1,
                    EvaluateExpression(Format(func_get_localization, 'tooltip_unit_stat_volley_damage'))
                    + EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, '', 0, f_mdb * n_entities_ammo, f_mdap * n_entities_ammo, f_medb * n_entities_ammo, f_medap * n_entities_ammo, projectile_dmg * n_entities_ammo))
                    + GetIf(has_mBvL, EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, 'large', mBvL * n_entities_ammo, f_mdb * n_entities_ammo, f_mdap * n_entities_ammo, f_medb * n_entities_ammo, f_medap * n_entities_ammo, projectile_dmg_BvL * n_entities_ammo)))
                    + GetIf(has_mBvi, EvaluateExpression(Format(func_format_range_damage_string, ap_ratio, 'infantry', mBvi * n_entities_ammo, f_mdb * n_entities_ammo, f_mdap * n_entities_ammo, f_medb * n_entities_ammo, f_medap * n_entities_ammo, projectile_dmg_Bvi * n_entities_ammo)))
                )
            }
        )
    '''
    set_context_callback(find_by_id(xml, 'template_stat'), 'ContextTooltipSetter', s)

    # find_by_id(xml, 'mod_icon_list')['dimensions'] = '24.00,24.00'
    # find_by_id(xml, 'template_modifier_icon')['dimensions'] = '24.00,24.00'


def split_abilities(xml):
    # language=javascript
    s = '''
        AbilityDetailsList.Filter((CategoryStateName == 'attributes' || CategoryStateName == "additional_stats") && Key != "weakness_fire")
    '''
    elem = find_by_id(xml, 'ability_list')
    elem.states.newstate['height'] = '28'
    cb = set_context_callback(elem, 'ContextList', s)
    cb.child_m_user_properties.append('''<property name="hide_if_empty" value=""/>''')
    
    # IsShowingExpandedUnitInfo == false
    
    elem = read_xml_component('unit_information/passives_list')
    # language=javascript
    s = '''
        AbilityDetailsList.Filter(CategoryStateName == "passives")
    '''
    set_context_callback(elem, 'ContextList', s)
    add_element(xml, elem, "list")
    
    elem = read_xml_component('unit_information/abilities_list')
    # language=javascript
    s = '''
        AbilityDetailsList.Filter(CategoryStateName == "abilities")
    '''
    set_context_callback(elem, 'ContextList', s)
    add_element(xml, elem, "list")
    
    elem = read_xml_component('unit_information/spells_list')
    # language=javascript
    s = '''
        GetIfElse(UnitRecordContext.Key == 'wh3_dlc24_tze_cha_blue_scribes', AbilityDetailsList.Filter(CategoryStateName == "none"), AbilityDetailsList.Filter(CategoryStateName == "spells"))
    '''
    set_context_callback(elem, 'ContextList', s)
    add_element(xml, elem, "list")
    
    # TODO can I reuse existing template?
    elem = read_xml_component('unit_information/template_passive')
    add_element(xml, elem, "passives_list")
    elem = read_xml_component('unit_information/template_ability')
    add_element(xml, elem, "abilities_list")
    elem = read_xml_component('unit_information/template_spell')
    add_element(xml, elem, "spells_list")
    offset = 2*28 + 24 + 8
    info_panel = find_by_id(xml, 'info_panel')
    info_panel.states.blank['height'] = str(int(info_panel.states.blank['height']) + offset)
    info_panel.states.wh3['height'] = str(int(info_panel.states.wh3['height']) + offset)
    find_by_guid(info_panel, '18418123-6531-42A5-B2FD2913D89943FC')['height'] = str(int(find_by_guid(info_panel, '18418123-6531-42A5-B2FD2913D89943FC')['height']) + offset)
    find_by_guid(info_panel, '7AD94D1C-7783-469E-8749A53D3321CB5F')['height'] = str(int(find_by_guid(info_panel, '7AD94D1C-7783-469E-8749A53D3321CB5F')['height']) + offset)


def move_info_panel_higher(xml):
    # part of split_abilities
    tag = find_by_callback_id(find_by_id(xml, 'info_panel_parent'), 'ContextCommandGiverOnCreate')
    
    # language=javascript
    s = '''
        DoIfElse(RootComponent.Dimensions.y < 1000, self.SetDockOffset(10, -270), self.SetDockOffset(10, -385))
    '''
    tag['context_function_id'] = format_str(s)
    
    tag = find_by_callback_id(find_by_id(xml, 'info_panel_parent'), 'ContextCommandEvent')
    
    # language=javascript
    s = '''
        DoIfElse(RootComponent.Dimensions.y < 1000, self.SetDockOffset(10, -270), self.SetDockOffset(10, -385))
    '''
    tag['context_function_id'] = format_str(s)


def add_ability_gold_value(xml):
    elem = read_xml_component('special_ability_tooltip/gold_value')
    
    # language=javascript
    s = '''
        "[[img:ui/skins/default/icon_income.png]][[/img]]"
        + RoundFloat( (sar = DatabaseRecordContext("CcoUnitSpecialAbilityRecord", RecordKey)) => {sar.AdditionalMeleeCp + sar.AdditionalMissileCp})
    '''
    set_context_callback(elem, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        DatabaseRecordContext("CcoUnitAbilityRecord", RecordKey).IsUnitUpgrade
    '''
    set_context_callback(elem, 'ContextVisibilitySetter', s)
    
    add_element(xml, elem, "header")
    
    
def edit_ability_info(xml):
    # language=javascript
    s = '''
        (
            n_entities = MaxDamagedEntities,
            ticks_per_sec = DamagePerSecond / ToNumber(DamageAmount * n_entities),
            ticks = GetIfElse(Duration == -1, ticks_per_sec, Duration * ticks_per_sec + 1),
            dmg = ToNumber(IntensifiedValueText(DamageAmount, '%f')),
            bottom_range_entity = Floor(dmg / 2.0),
            top_range_entity = Floor((dmg - 1)),
            bottom_range_unit = bottom_range_entity * n_entities * ticks_per_sec,
            top_range_unit =  top_range_entity * n_entities * ticks_per_sec,
            expected_dmg = RoundFloat((bottom_range_unit + top_range_unit) / ticks_per_sec / 2.0 * ticks)
        ) =>
        {
            Format('%d-%d (~%d)', RoundFloat(bottom_range_unit), RoundFloat(top_range_unit), expected_dmg)
        }
    '''
    set_context_callback(find_by_id(xml, "value_damage"), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (
            ticks = Duration / HpChangeFrequency + 1,
            heal = ToNumber(IntensifiedValueText(HealPercent, '%f')),
            hps = heal * 1.0 / HpChangeFrequency,
            expected_heal = heal * ticks
        ) =>
        {
            Format('%+.2f%% (~%.2f%%)', hps * 100, expected_heal * 100)
        }
    '''
    set_context_callback(find_by_id(xml, "value_heal"), 'ContextTextLabel', s)


def prepare_reinf_panel_supplies(xml):
    # language=javascript
    s = '''
        Ceiling(
            Clamp(
                BattleRoot.BattleCurrencyManagerContext.GetArmyCurrencyForType(BattleRoot.PlayerArmyContext, "supplies_currency"),
                0,
                999999
            )
        )
    '''
    set_context_callback(find_by_id(xml, "dy_supplies"), 'ContextTextLabel', s)
    
    
def unit_info_desc_visibility_toggle(xml):
    # language=javascript
    s = '''
        PrefAsBool('hui_unit_info_desc_visible')
    '''
    create_context_callback(find_by_id(xml, 'descr_holder'), "ContextVisibilitySetter", "CcoStaticObject", s, {'update_constant': '100'})
    
    
    # language=javascript
    s = '''
        TogglePrefBool('hui_unit_info_desc_visible')
    '''
    create_context_callback(find_by_id(xml, 'custom_name_display'), "ContextCommandRightClick", "CcoStaticObject", s)
    
def unit_info_short_desc_asmr(xml):
    # language=javascript
    s = '''
        Do(
            TogglePrefBool('hui_unit_info_short_desc_asmr'),
            self.SetText(GetIfElse(
                PrefAsBool('hui_unit_info_short_desc_asmr'),
                StringGet('unit_description_short_texts_text_asmr_' + UnitRecordContext.UnitLandRecordContext.Key),
                UnitRecordContext.Description
            ))
    )
    '''
    create_context_callback(find_by_id(xml, 'short_description'), "ContextCommandLeftClick", "CcoUnitDetails", s)
    
    # language=javascript
    s = '''
        GetIfElse(
            PrefAsBool('hui_unit_info_short_desc_asmr'),
            StringGet('unit_description_short_texts_text_asmr_' + UnitRecordContext.UnitLandRecordContext.Key),
            UnitRecordContext.Description
        )
    '''
    set_context_callback(find_by_id(xml, 'short_description'), "ContextTextLabel", s)
    
def spell_browser_unit_historical_desc_asmr(xml):
    elem = find_by_id(xml, 'descr_textview')
    # language=javascript
    s = '''
    (
        cbpr = self.ChildContext('dy_text').ContextsList[0]
    ) =>
        Do(
            TogglePrefBool('hui_spell_browser_unit_historical_desc_asmr'),
            self.ChildContext('dy_text').SetText(GetIfElse(
                PrefAsBool('hui_spell_browser_unit_historical_desc_asmr'),
                StringGet('unit_description_historical_texts_text_asmr_' + cbpr.UnitContext.UnitLandRecordContext.Key),
                cbpr.UnitContext.HistoricalDescription
            ))
    )
    '''
    create_context_callback(find_by_id(xml, 'clip'), "ContextCommandLeftClick", "CcoStaticObject", s)
    
    # language=javascript
    s = '''
        GetIfElse(
            PrefAsBool('hui_spell_browser_unit_historical_desc_asmr'),
            StringGet('unit_description_historical_texts_text_asmr_' + UnitContext.UnitLandRecordContext.Key),
            UnitContext.HistoricalDescription
        )
    '''
    set_context_callback(find_by_id(xml, 'dy_text'), "TextviewText", s)


def prepare_mod_team_list(xml):
    # language=javascript
    s = '''
        (ccoBA = this) =>
        {
            UnitList
            .Sum(ActiveEffectList)
            .Filter(AbilityContext.EffectRange == -1 && (AbilityContext.MaxAffectedAllyCount == -1 || AbilityContext.MaxAffectedEnemyCount == -1))
            .Filter( !(BattleRoot.IsMultiplayer && ccoBA.AllianceContext.Id != BattleRoot.PlayerAllianceContext.Id && PhaseRecordContext.EffectType == "positive") )
            .Distinct(AbilityContext.RecordKey)
            .Sort(ContextObjectId(this))
        }
    '''
    set_context_callback(find_by_id(xml, "active_effect_list"), 'ContextList', s)
    
    elem_id = "daemon_army_ability"
    # language=javascript
    s = '''
        RoundFloat(
            MinNumericValue(
                CurrentPercentToArmyAbility(0),
                1
            ) * 100
        )
        + "%/"
        + RoundFloat(
            MinNumericValue(
                CurrentPercentToArmyAbility(1),
                1
            ) * 100
        )
        + "%/"
         + RoundFloat(
            MinNumericValue(
                CurrentPercentToArmyAbility(2),
                1
            ) * 100
        )
        + "%"
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer) &&
    (HasDaemonFeature || (FactionContext.SubcultureContext.Key == "wh3_main_sc_ogr_ogre_kingdoms"))
    '''  # Ogres use daemonic system
    set_context_callback(find_by_id(xml, elem_id), 'ContextVisibilitySetter', s)
    
    elem_id = "murderous_prowess_ability"
    # language=javascript
    s = '''
        RoundFloat(MinNumericValue(MurderousProwessPercent, 1) * 100) + "%"
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer) && HasMurderousProwess
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextVisibilitySetter', s)
    
    elem_id = "waaagh_ability"
    # language=javascript
    s = '''
        RoundFloat(MinNumericValue(CurrentWaaaghPercent, 1) * 100) + "%"
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer) && HasWaaagh
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextVisibilitySetter', s)
    
    elem_id = "tomb_kings_ability"
    # language=javascript
    s = '''
        RoundFloat(MinNumericValue(RealmOfSoulsPercent, 1) * 100) + "%"
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer) && (HasRealmOfSouls && FactionContext.SubcultureContext.Key == "wh2_dlc09_sc_tmb_tomb_kings")
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextVisibilitySetter', s)
    
    
    elem_id = "label_supplies"
    # language=javascript
    s = '''
        StringGet('uied_component_texts_localised_string_label_supplies_Tooltip_4f8f1a10')
        + GetIf((BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer || this.AllianceContext.Id == BattleRoot.PlayerAllianceContext.Id),
            Loc('LF') +
            BattleRoot.BattleReinforcementPoolContext.UnitsForArmy(
                this,
                BattleRoot.SpawnZoneList.FirstContext(!IsVanguardOnly && IsAvailableToAlliance(this.AllianceIndex)).UniqueID
            ).JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/skins/default/icon_supplies_18px.png]][[/img]]%d", UnitContext.UnitRecordContext.CategoryIcon, UnitContext.UnitRecordContext.Name, RoundFloat(CostPerUnit(this.ArmyIndex))), Loc('LF'))
        )
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    
    elem_id = "gold_value"
    # language=javascript
    s = '''
        RoundFloat( UnitList.Filter(IsAlive && !IsShattered).Sum(GetGoldValue(true) ) )
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    # language=javascript
    s = '''
        EvaluateExpression(Format(ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value, 'mod_team_list_army_gold_value')) + Loc('LF') +
        UnitList
            .Filter(IsAlive && !IsShattered)
            .JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/skins/default/icon_income.png]][[/img]]%d", UnitRecordContext.CategoryIcon, UnitRecordContext.Name, GetGoldValue(true)), Loc('LF'))
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    elem_id = "heal_value"
    # language=javascript
    s = '''
    (
        heal_cap = 0.75,
        meu_undefined = UnitList.Filter(NumEntitiesInitial > 1).Filter(MaxHealthPercentCanReplenish > 0.999),
        units_can_be_calculated = UnitList.Filter( ((NumEntitiesInitial > 1) && (MaxHealthPercentCanReplenish < 1.0)) || (NumEntitiesInitial == 1) ),
        heal_value = units_can_be_calculated.Sum(GetGoldValue(false) * (heal_cap - (MaxHealthPercentCanReplenish - HealthPercent)) ),
        str = GetIf(meu_undefined.Size > 0, '[[img:ui/mod/icons/greater_approx.png]][[/img]]') + Format("%d", RoundFloat(heal_value))
    ) =>
    {str}
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    # language=javascript
    s = '''
    (
        heal_cap = 0.75,
        str = UnitList
            .JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/mod/icons/icon_stat_health_gold_value.png]][[/img]]%S", UnitRecordContext.CategoryIcon, UnitRecordContext.Name,
                    GetIfElse((NumEntitiesInitial > 1) && (MaxHealthPercentCanReplenish > 0.999), 'N/A', '' + RoundFloat(GetGoldValue(false) * (heal_cap - (MaxHealthPercentCanReplenish - HealthPercent))))
                ), Loc('LF'))
    ) =>
    {EvaluateExpression(Format(ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value, 'mod_team_list_army_heal_value')) + Loc('LF') + str}
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    elem_id = "label_score"
    # language=javascript
    s = '''
        RoundFloat(UnitList.Sum(BattleResultUnitContext.DamageDealtCost))
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)

    # language=javascript
    s = '''
        StringGet('uied_component_texts_localised_string_label_score_Tooltip_e40781bb') + Loc('LF') +
        UnitList
            .Transform(BattleResultUnitContext)
            .JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/skins/default/icon_stat_damage_base.png]][[/img]]%d", UnitRecordContext.CategoryIcon, UnitRecordContext.Name, DamageDealtCost), Loc('LF'))
    '''
    create_context_callback(find_by_id(xml, elem_id), "ContextTooltipSetter", "CcoBattleArmy", s, {'update_constant': '100'})
    
    
    elem_id = "killed_entities"
    # language=javascript
    s = '''
        EvaluateExpression(Format(ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value, 'mod_team_list_killed_enemy_entities')) + Loc('LF') +
        UnitList
            .JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/skins/default/icon_kills.png]][[/img]]%d", UnitRecordContext.CategoryIcon, UnitRecordContext.Name, NumKills), Loc('LF'))
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    
    elem_id = "friendly_fire"
    # language=javascript
    s = '''
        EvaluateExpression(Format(ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value, 'mod_team_list_killed_friendly_entities')) + Loc('LF') +
        UnitList
            .Transform(BattleResultUnitContext)
            .JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/battle ui/ability_icons/wh_dlc07_unit_passive_icon_of_devotion.png]][[/img]]%d", UnitRecordContext.CategoryIcon, UnitRecordContext.Name, NumKillsFriendlies), Loc('LF'))
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    
    elem_id = "dead_entities"
    # language=javascript
    s = '''
        EvaluateExpression(Format(ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('get_localization').Value, 'mod_team_list_dead_entities'))
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    #  +
    #         UnitList
    #             .JoinString(Format("[[img:%S]][[/img]]%S [[img:ui/skins/warhammer3/khorne_skull_icon.png]][[/img]]%d", UnitRecordContext.CategoryIcon, UnitRecordContext.Name, NumMenDied), Loc('LF'))
    
    
    elem_id = "wom_current"
    # language=javascript
    s = '''
        WindsOfMagicPoolContext.CurrentWind + "(" + 1 / WindsOfMagicPoolContext.CurrentRechargePerSecond + ")"
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    elem_id = "wom_reserves"
    # language=javascript
    s = '''
        WindsOfMagicPoolContext.ReserveWind + GetIf(WindsOfMagicPoolContext.DepletionModifierPhaseList.Size > 0, "(" + WindsOfMagicPoolContext.DepletionModifierPhaseList.Sum(ManaMaxDepletionMod) + ")")
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    elem_id = "icon_player"
    # language=javascript
    s = '''
        GetIf(PlayerName.Contains("RoflanBuldiga"), "ui/mod/images/players/roflanbuldiga.png")
        + GetIf(PlayerName.Contains("Lord_Leaver"), "ui/mod/images/players/lord_leaver.png")
        + GetIf(PlayerName.Contains("BERRSERK"), "ui/mod/images/players/berrserk.png")
        + GetIf(PlayerName.Contains("VoinS"), "ui/mod/images/players/voins.png")
        + GetIf(PlayerName.Contains("GapaKtus"), "ui/mod/images/players/gapaktus.png")
        + GetIf(PlayerName.Contains("komerdinner12"), "ui/mod/images/players/komerdinner.png")
        + GetIf(PlayerName.Contains("Crabling"), "ui/mod/images/players/crabling.png")
        + GetIf(PlayerName.Contains("Risum"), "ui/mod/images/players/nerisum.png")
        + GetIf(PlayerName.Contains("akkeinn"), "ui/mod/images/players/akkeinn.png")
        + GetIf(PlayerName.Contains("Exul et ignotus"), "ui/mod/images/players/exul_et_ignotus.png")
        + GetIf(PlayerName.Contains("lunacy"), "ui/mod/images/players/cb2.png")
        + GetIf(PlayerName.Contains("Not Alpharius"), "ui/mod/images/players/not_alpharius.png")
        + GetIf(PlayerName.Contains("Helmuskar"), "ui/mod/images/players/helmuskar.png")
        + GetIf(PlayerName.Contains("Ahzek Ahrimem"), "ui/mod/images/players/ahzek.png")
        + GetIf(PlayerName.Contains("Chained Soldier"), "ui/mod/images/players/chained.png")
        + GetIf(PlayerName.Contains("leavePls."), "ui/mod/images/players/sham.png")
        + GetIf(PlayerName.Contains("Karadok"), "ui/mod/images/players/karadok.png")
        + GetIf(PlayerName.EndsWith("Drago"), "ui/mod/images/players/drago.png")
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextImageSetter', s)
    # language=javascript
    s = '''
        GetIf(PlayerName.Contains("RoflanBuldiga"), Loc("player_roflanbuldiga"))
        + GetIf(PlayerName.Contains("Lord_Leaver"), Loc("player_lord_leaver"))
        + GetIf(PlayerName.Contains("BERRSERK"), Loc("player_berrserk"))
        + GetIf(PlayerName.Contains("VoinS"), Loc("player_voins"))
        + GetIf(PlayerName.Contains("GapaKtus"), Loc("player_gapaktus"))
        + GetIf(PlayerName.Contains("komerdinner12"), Loc("player_komerdinner"))
        + GetIf(PlayerName.Contains("Crabling"), Loc("player_crabling"))
        + GetIf(PlayerName.Contains("Risum"), Loc("player_risum"))
        + GetIf(PlayerName.Contains("akkeinn"), Loc("player_akkeinn"))
        + GetIf(PlayerName.Contains("Exul et ignotus"), Loc("player_exul_et_ignotus"))
        + GetIf(PlayerName.Contains("lunacy"), Loc("player_lunacy"))
        + GetIf(PlayerName.Contains("Not Alpharius"), Loc("player_not_alpharius"))
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    elem_id = "icon_clan"
    # language=javascript
    s = '''
        GetIf(PlayerName.StartsWith("VM.") || PlayerName.StartsWith("V_M") || PlayerName.StartsWith("VM ") || PlayerName.StartsWith("VM_"), "ui/mod/images/clans/vm.png")
        + GetIf(PlayerName.StartsWith("-CB-") || PlayerName.StartsWith("CB "), "ui/mod/images/clans/cb.png")
        + GetIf(PlayerName.Contains("RoflanBuldiga"), "ui/mod/images/clans/komariga.png")
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextImageSetter', s)
    # language=javascript
    s = '''
        GetIf(PlayerName.StartsWith("VM.") || PlayerName.StartsWith("V_M") || PlayerName.StartsWith("VM ") || PlayerName.StartsWith("VM_"), Loc("clan_vm"))
        + GetIf(PlayerName.StartsWith("-CB-") || PlayerName.StartsWith("CB "), Loc("clan_cb"))
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    elem_id = "label_supplies"
    # language=javascript
    s = '''
        (BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer || this.AllianceContext.Id == BattleRoot.PlayerAllianceContext.Id)
        | Ceiling(
            BattleRoot.BattleCurrencyManagerContext.GetArmyCurrencyForType(this, "supplies_currency")
        )
        | "-"
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    
def mod_battle_ui():
    edit_twui('ui/battle ui/hud_battle',
              lambda xml: (
                  remove_zooming_to_reinforcement_point(xml),
                  move_info_panel_higher(xml),
                  add_spell_panel_wom_cost(xml)
              )
              )
    edit_twui('ui/battle ui/hud_battle_top_bar',
              lambda xml: (
                  add_timer_to_tickets(xml),
                  add_vp_owner_icon(xml),
                  add_capture_weight(xml),
                  remove_supplies_in_replays(xml)
              )
              )
    edit_twui('ui/battle ui/hud_battle_reinforcement_purchase', increase_reinforcement_size)
    
    edit_twui('ui/battle ui/unit_banner',
              lambda xml: (
                  add_unit_banner_tier(xml),
              )
              )
    
    # edit_twui('ui/frontend ui/custom_battle_map_settings', add_dom_ffa_to_custom_battles)
    
    edit_twui('ui/common ui/unit_information',
              lambda xml: (
                  change_unit_info_kill_count(xml),
                  change_unit_info_hit_points(xml),
                  add_unit_info_gold_value(xml),
                  add_unit_info_fatigue(xml),
                  mod_stats_fatigue(xml),
                  split_abilities(xml),
                  add_unit_info_resistances(xml),
                  unit_info_short_desc_asmr(xml)
                  # unit_info_desc_visibility_toggle(xml)
              )
              )
    edit_twui('ui/common ui/special_ability_tooltip',
              lambda xml: (
                  add_ability_gold_value(xml)
              )
              )
    edit_twui('ui/templates/phase_effect',
              lambda xml: (
                  edit_ability_info(xml)
              )
              )
    edit_twui('ui/common ui/tooltip_unit_health',
              lambda xml: (
                  change_unit_health_tooltip(xml),
              )
              )
    
    edit_twui('ui/common ui/spell_browser',
              lambda xml: (
                  spell_browser_unit_historical_desc_asmr(xml)
              )
              )
    
    edit_twui('ui/loading_ui/postbattle',
              lambda xml: (
                  mod_postbattle_stat(xml)
              )
              )
    
    edit_twui('ui/common ui/land_unit_card',
              lambda xml: (
                  mod_postbattle_stat_campaign(xml)
              )
              )
    
    # edit_twui('ui/templates/custom_battle_team_entry', enable_button_ai)
    
    edit_twui('ui/mod/reinf_panel_supplies', prepare_reinf_panel_supplies)
    edit_twui('ui/mod/mod_team_list', prepare_mod_team_list)