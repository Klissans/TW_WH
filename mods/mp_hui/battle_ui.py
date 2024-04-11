from whlib.twui import *


def add_timer_to_tickets(xml):
    # language=javascript
    s = '''
        (timeStr = FormatTime((BattleRoot.CaptureLocationManagerContext.TicketsGoal - TicketsRemaining) / TicketsIncomePerSecond)) =>
            {
                GetIfElse(BattleRoot.IsSpectator || BattleRoot.IsReplay,
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
            BattleTypeRecordList + DatabaseRecordsForKeys("CcoBattleTypeRecord", "domination", "free_for_all")
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
    # language=javascript
    s = '''
        GetIfElse(
            BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer,
            BattleUnitContext.BattleResultUnitContext.DamageDealtCost,
            KillCount
        )
    '''
    set_context_callback(find_by_id(xml, 'dy_kills'), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        Format(Loc("tooltip_kills_ff"), BattleUnitContext.BattleResultUnitContext.NumKillsFriendlies)
        + Format(Loc("tooltip_kills"), KillCount, BattleUnitContext.BattleResultUnitContext.DamageDealt, BattleUnitContext.BattleResultUnitContext.DamageDealtCost)
    '''
    set_context_callback(find_by_id(xml, 'dy_kills'), 'ContextTooltipSetter', s)
    
    # language=javascript
    s = '''
        GetIfElse(
            BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer,
            "ui/skins/default/icon_stat_damage_base.png",
            "ui/skins/default/icon_kills.png"
        )
    '''
    desc = f'''
        <callbackwithcontextlist>
            {create_context_callback_as_string("ContextImageSetter", "CcoStaticObject", s)}
        </callbackwithcontextlist>
    '''  # icon kills
    tag = find_by_guid(xml, '4E7A2193-5DEC-443B-865D61B086AB4772')
    tag.append(replace_escape_characters(desc))


def change_unit_info_hit_points(xml):
    # language=javascript
    s = '''
        GetIfElse(
            IsKnownHp,
            HitPoints
            + GetIf(
                BarrierMaxHp > 0,
                " [[img:ui/skins/default/icon_barrier_replenish.png]][[/img]]" + BarrierHp
            ),
            "??"
        )
    '''
    set_context_callback(find_by_id(xml, 'hit_points'), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        GetIfElse(
            IsKnownHp,
            Format(
                "EntityHP: [[col:yellow]]%d[[/col]], InitialHP: [[col:yellow]]%d[[/col]], EntitiesAdjustedMaxHP: [[col:yellow]]%d[[/col]], HealingLeft: %S",
                RoundFloat(HitPointsInitial / NumEntitiesInitial),
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
    set_context_callback(find_by_id(xml, 'health_bar'), 'ContextTooltipSetter', s)


def add_unit_info_gold_value(xml):
    elem = read_xml_component('unit_information/gold_value')
    
    # language=javascript
    s = '''
        (
        exp_cost = GetIfElse(UnitRecordContext.IsRenown, 0, ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11)),
        al = GetIf(IsCharacter,
            AbilityDetailsList
                .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                .Filter(IsUnitUpgrade)
                .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                .Sum(AdditionalMeleeCp + AdditionalMissileCp))
        ) =>
        {
            "[[img:ui/skins/default/icon_income.png]][[/img]]"
                + GetIf(IsBattle, RoundFloat( (UnitRecordContext.Cost + exp_cost + al) * BattleUnitContext.HealthPercent ))
                + " (" + RoundFloat(UnitRecordContext.Cost + exp_cost + al) + ") "
        } '''
    set_context_callback(elem, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
    (
        exp_cost = RoundFloat(ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11))
    ) =>
    {
        "[[img:ui/skins/default/icon_income.png]][[/img]]"
        + Format("%d%S%S",
            UnitRecordContext.Cost,
            GetIf(ExperienceLevel > 0, GetIfElse(UnitRecordContext.IsRenown, "", Format(" [[img:ui/skins/default/experience_%d.png]][[/img]]%d", ExperienceLevel, exp_cost) )),
            GetIf(IsCharacter,
                Format(" %S",
                    AbilityDetailsList
                    .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                    .Filter(IsUnitUpgrade)
                    .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                    .JoinString(Format("[[img:%S]][[/img]]%d", BaseRecordContext.IconPath.ToLower, RoundFloat(AdditionalMeleeCp + AdditionalMissileCp)), " ")
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
                     "" + GetIf(BattleUnitContext.FatigueState == 0, "fresh")
                     + GetIf(BattleUnitContext.FatigueState == 1, "active")
                     + GetIf(BattleUnitContext.FatigueState == 2, "winded")
                     + GetIf(BattleUnitContext.FatigueState == 3, "tired")
                     + GetIf(BattleUnitContext.FatigueState == 4, "very_tired")
                     + GetIf(BattleUnitContext.FatigueState == 5, "exhausted")
                     ) + BattleUnitContext.FatigueName)
                '''
    set_context_callback(elem, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        Loc(Format("tooltip_fatigue_effects_%d", BattleUnitContext.FatigueState))
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


def add_unit_info_resistances(xml):
    elem = read_xml_component('unit_information/resistances_row')
    # language=javascript
    s = '''
        Format("[[img:ui/battle ui/ability_icons/resistance_ward_save.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_ward_save") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]]0[[/col]]"
                )
            }
        ) +
        Format("[[img:ui/battle ui/ability_icons/resistance_physical.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_physical") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]]0[[/col]]"
                )
            }
        ) +
        Format("[[img:ui/battle ui/ability_icons/resistance_magic.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_magic") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]]0[[/col]]"
                )
            }
        ) +
        Format("[[img:ui/battle ui/ability_icons/resistance_missile.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_missile") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "[[col:ui_font_faded_grey_beige]]0[[/col]]"
                )
            }
        ) +
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
                                "[[col:ui_font_faded_grey_beige]]0[[/col]]"
                            )
                        }
                    )
                )
            }
        ) +
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
    # 遠程抗性：40% - trd chineese &#xff1a; us.RFind("&#xff1a;") \uff1a
    set_context_callback(elem, 'ContextTextLabel', s)
    
    insert_after_element(xml, elem, "health_parent")


def mod_stats_fatigue(xml):
    # language=javascript
    s = '''
    (
        db_lookup = RootComponent.ChildContext("db_lookup"),
        is_battle = IsContextValid(BattleRoot),
        ud = StoredContextFromParent("CcoUnitDetails"),
        buc = ud.BattleUnitContext,
        f_state = GetIf(is_battle, Format("%d", buc.FatigueState)),
        cmp = GetIf(is_battle, db_lookup.ChildContext("fatigue_effects").ChildContext(Key)),
        fatigue_coeff = GetIfElse(is_battle, ToNumber(cmp.GetProperty(f_state)), 1.0),

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
                mass = RoundFloat(ud.Mass),
                mass_str = Format("[[img:ui/mod/icons/icon_stat_mass.png]][[/img]][[col:ui_font_faded_grey_beige]]%d[[/col]]", mass),
                r_armour = DisplayedValue,
                f_armour = RoundFloat(fatigue_coeff * r_armour),
                f_armour_str = Format("[[img:ui/mod/icons/icon_stat_armour.png]][[/img]]%d", f_armour),
                avg_armour_res = GetIf(f_armour <= 100, RoundFloat(0.75 * f_armour))
                    + GetIf(100 < f_armour && f_armour < 200,
                        (
                            half=0, _t1 = 0.5 * f_armour,
                            diff=0, _t2 = f_armour - half,
                            lh=0, _t3 = 100 - half,
                            rh=0, _t4 = f_armour - 100
                        ) => { RoundFloat((lh / diff) * (half + 100) / 2 + (rh / diff) * 100) }
                    )
                    + GetIf(f_armour >= 200, 100)
            ) =>
            {
                Format("%S %S [%d%] ", mass_str, f_armour_str, avg_armour_res)
            }
        ) +
        GetIf(Key == "stat_morale", Format("[[img:ui/mod/icons/icon_stat_morale.png]][[/img]]%d ", RoundFloat(DisplayedValue))) +
        GetIf(Key == "scalar_speed", Format("[[img:ui/mod/icons/icon_stat_speed.png]][[/img]]%d ", RoundFloat(fatigue_coeff * DisplayedValue)) ) +
        GetIf(Key == "stat_melee_attack",
            (
                r_ma = DisplayedValue,
                f_ma = RoundFloat(fatigue_coeff * r_ma),
                f_ma_str = Format("[[img:ui/mod/icons/icon_stat_melee_attack.png]][[/img]]%d", f_ma),
                f_ma_BvL = f_ma + BvL,
                f_ma_BvL_str = GetIfElse(has_BvL, Format("[[img:ui/skins/default/modifier_icon_bonus_vs_large.png]][[/img]]%d", f_ma_BvL), ""),
                f_ma_Bvi = f_ma + Bvi,
                f_ma_Bvi_str = GetIfElse(has_Bvi, Format("[[img:ui/skins/default/modifier_icon_bonus_vs_infantry.png]][[/img]]%d", f_ma_Bvi), "")
            ) =>
            {
                Format("  %S%S %S ", f_ma_BvL_str, f_ma_Bvi_str, f_ma_str)
            }
        ) +
        GetIf(Key == "stat_melee_defence",
            (
                r_md = DisplayedValue,
                f_md = RoundFloat(fatigue_coeff * r_md),
                f_md_str = Format("[[img:ui/mod/icons/icon_stat_defence.png]][[/img]]%d", f_md),
                flank_md = RoundFloat(f_md * ScriptObjectContext('_kv_rules_table.melee_defence_direction_penalty_coefficient_flank').NumericValue),
                flank_md_str = Format("[[img:ui/mod/icons/icon_stat_defence_flank.png]][[/img]]%d", flank_md),
                rear_md = RoundFloat(f_md * ScriptObjectContext('_kv_rules_table.melee_defence_direction_penalty_coefficient_rear').NumericValue),
                rear_md_str = Format("[[img:ui/mod/icons/icon_stat_defence_rear.png]][[/img]]%d", rear_md)
            ) =>
            {
                Format("%S %S %S ", rear_md_str, flank_md_str, f_md_str)
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

                bwd_fatigue_coeff = GetIfElse(is_battle, ToNumber(db_lookup.ChildContext("fatigue_effects").ChildContext("stat_melee_damage_base").GetProperty(f_state)), 1.0),
                f_bwd = RoundFloat(bwd_fatigue_coeff * bwd),
                f_bwd_str = Format("[[img:ui/skins/default/icon_stat_damage_base.png]][[/img]]%d", f_bwd),
                apwd_fatigue_coeff = GetIfElse(is_battle, ToNumber(db_lookup.ChildContext("fatigue_effects").ChildContext("stat_melee_damage_ap").GetProperty(f_state)), 1.0),
                f_apwd = RoundFloat(apwd_fatigue_coeff * apwd),
                f_apwd_str = Format("[[img:ui/skins/default/modifier_icon_armour_piercing.png]][[/img]]%d", f_apwd),

                BvL_str = GetIfElse(has_BvL, Format("[[img:ui/skins/default/modifier_icon_bonus_vs_large.png]][[/img]]%d", BvL), ""),
                Bvi_str = GetIfElse(has_Bvi, Format("[[img:ui/skins/default/modifier_icon_bonus_vs_infantry.png]][[/img]]%d", Bvi), ""),
                
                set_total_wd = ScriptObjectContext('unit_info_ui.total_weapon_damage').SetNumericValue(f_bwd + f_apwd)
            ) =>
            {
                Format("  %S%S %S%S ", BvL_str, Bvi_str, f_bwd_str, f_apwd_str)
            }
        ) +
        GetIf(Key == "stat_charge_bonus",
            (
                stat_morale_tp = ud.StatContextFromKey("stat_morale").Tooltip.Replace('||', ''),
                charging_png_i = stat_morale_tp.RFind("[[img:ui/skins/default/icon_stat_charge_bonus.png"),
                is_charging = charging_png_i > 0,
                charging_half_str = GetIf(is_charging, stat_morale_tp.Substr(charging_png_i-1)),
                charging_colon_i = GetIf(is_charging, charging_half_str.Find(": ")),
                charging_str = GetIfElse(is_charging, charging_half_str.Substr(1, charging_colon_i - 1), ""),

                r_cb = DisplayedValue,
                f_cb = RoundFloat(fatigue_coeff * DisplayedValue),
                f_cb_str = Format("%S  [[img:ui/mod/icons/icon_stat_charge_bonus.png]][[/img]]%d ", charging_str, f_cb)
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
                rt_str = Format("[[img:ui/skins/default/icon_stat_reload_time.png]][[/img]][[col:ui_font_faded_grey_beige]]%f[[/col]]", rt),
                
                total_ammo = bs + nop + spv,
                set_total_ammo = ScriptObjectContext('unit_info_ui.total_ammo').SetNumericValue(GetIf(total_ammo > 0, total_ammo, 1))
            ) =>
            {
                Format("  %S%S%S %S %S ", bs_str, nop_str, spv_str, rt_str, ammo_str)
            }
        ) +
        GetIf(Key == "scalar_missile_range", Format("[[img:ui/mod/icons/icon_distance_to_target.png]][[/img]]%d ", RoundFloat(DisplayedValue))) +
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
                mBvL = GetIf(has_mBvL, RoundFloat(ToNumber(mBvL_s))),

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
                mBvi = GetIf(has_mBvi, RoundFloat(ToNumber(mBvi_s))),

                fe = db_lookup.ChildContext("fatigue_effects"),

                mdb_fatigue_coeff = GetIfElse(is_battle, ToNumber(fe.ChildContext("scalar_missile_damage_base").GetProperty(f_state)), 1.0),
                f_mdb = RoundFloat(mdb_fatigue_coeff * mdb),
                f_mdb_str = Format("[[img:ui/skins/default/icon_stat_ranged_damage_base.png]][[/img]]%d", f_mdb),

                mdap_fatigue_coeff = GetIfElse(is_battle, ToNumber(fe.ChildContext("scalar_missile_damage_ap").GetProperty(f_state)), 1.0),
                f_mdap = RoundFloat(mdap_fatigue_coeff * mdap),
                f_mdap_str = Format("[[img:ui/skins/default/modifier_icon_armour_piercing_ranged.png]][[/img]]%d", f_mdap),

                medb_fatigue_coeff = GetIfElse(is_battle, ToNumber(fe.ChildContext("scalar_missile_explosion_damage_base").GetProperty(f_state)), 1.0),
                f_medb = GetIf(has_medb, RoundFloat(medb_fatigue_coeff * medb)),
                f_medb_str = GetIfElse(has_medb, Format(" [[img:ui/skins/default/icon_explosive_damage.png]][[/img]]%d", f_medb), ""),

                medap_fatigue_coeff = GetIfElse(is_battle, ToNumber(fe.ChildContext("scalar_missile_explosion_damage_ap").GetProperty(f_state)), 1.0),
                f_medap = GetIf(has_medap, RoundFloat(medap_fatigue_coeff * medap)),
                f_medap_str = GetIfElse(has_medap, Format("[[img:ui/skins/default/icon_stat_explosive_armour_piercing_damage.png]][[/img]]%d", f_medap), ""),

                mBvL_str = GetIfElse(has_mBvL, Format("[[img:ui/skins/default/modifier_icon_bonus_vs_large.png]][[/img]]%d", mBvL), ""),
                mBvi_str = GetIfElse(has_mBvi, Format("[[img:ui/skins/default/modifier_icon_bonus_vs_infantry.png]][[/img]]%d", mBvi), ""),
                
                set_total_rwd = ScriptObjectContext('unit_info_ui.total_ranged_weapon_damage').SetNumericValue(f_mdb + f_mdap + f_medb + f_medap)
            ) =>
            {
                Format("  %S%S %S%S%S%S ", mBvL_str, mBvi_str, f_mdb_str, f_mdap_str, f_medb_str, f_medap_str)
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
            md_flank = ScriptObjectContext('_kv_rules_table.melee_defence_direction_penalty_coefficient_flank').NumericValue,
            md_rear = ScriptObjectContext('_kv_rules_table.melee_defence_direction_penalty_coefficient_rear').NumericValue,
            md_flank_red = RoundFloat((1 - md_flank) * 100),
            md_rear_red = RoundFloat((1 - md_rear) * 100)
        ) =>
        Tooltip
        + GetIf(Key == "stat_armour", Loc('tooltip_unit_stat_armour'))
        + GetIf(Key == "stat_melee_defence", Format(Loc('tooltip_unit_stat_md'), md_rear_red, md_flank_red))
        + Format(Loc('tooltip_unit_stat_ui'), RoundFloat(ValueBase), RoundFloat(DisplayedValue))
        + GetIf(Key == "stat_weapon_damage", Format(Loc('tooltip_unit_stat_dmg_per_hit'), RoundFloat(ScriptObjectContext('unit_info_ui.total_weapon_damage').NumericValue)))
        + GetIf(Key == "stat_missile_damage_over_time", Format(Loc('tooltip_unit_stat_dmg_per_shot'), RoundFloat(ScriptObjectContext('unit_info_ui.total_ammo').NumericValue * ScriptObjectContext('unit_info_ui.total_ranged_weapon_damage').NumericValue)))
    '''
    set_context_callback(find_by_id(xml, 'template_stat'), 'ContextTooltipSetter', s)


def split_abilities(xml):
    # language=javascript
    s = '''
        AbilityDetailsList.Filter(CategoryStateName == "passives" && Key != "weakness_fire")
    '''
    cb = set_context_callback(find_by_id(xml, 'ability_list'), 'ContextList', s)
    cb.child_m_user_properties.append('''<property name="hide_if_empty" value=""/>''')
    
    # IsShowingExpandedUnitInfo == false
    
    elem = read_xml_component('unit_information/spells_abilities_list')
    # language=javascript
    s = '''
        AbilityDetailsList.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities")
    '''
    set_context_callback(elem, 'ContextList', s)
    add_element(xml, elem, "list")
    
    # TODO can I reuse existing template?
    elem = read_xml_component('unit_information/template_spell_ability')
    add_element(xml, elem, "spells_abilities_list")
    
    find_by_id(xml, 'unit_information').animations.show_stats.find_all('triggers').append(
        """
            <trigger
            trigger_component="854991D1-D51D-40AC-9053C46DF54FSS00"
            trigger_property="Visibility true"/>
        """
    )
    
    find_by_id(xml, 'unit_information').animations.show_abilities.find_all('triggers').append(
        """
            <trigger
            trigger_component="854991D1-D51D-40AC-9053C46DF54FSS00"
            trigger_property="Visibility false"/>
        """
    )
    
    find_by_guid(xml, 'A05D6E49-54C8-403A-A721A4F49B3B2D53').find_all('transition_m_triggers').append(  # down
        """
            <trigger
            trigger_component="854991D1-D51D-40AC-9053C46DF54FSS00"
            trigger_property="Visibility true"/>
        """
    )
    
    find_by_guid(xml, '4AB18355-1C3E-4DF3-B8F02F0BC731D452').find_all('transition_m_triggers').append(  # selected_down
        """
            <trigger
            trigger_component="854991D1-D51D-40AC-9053C46DF54FSS00"
            trigger_property="Visibility false"/>
        """
    )
    
    find_by_guid(xml, 'A43EC7EC-75C5-4705-AF915151B9ADD6FC').find_all('transition_m_triggers').append(  # down
        """
            <trigger
                trigger_component="854991D1-D51D-40AC-9053C46DF54FSS00"
                trigger_property="Visibility false"/>
        """
    )
    
    find_by_guid(xml, '40096869-49EB-465E-99AAB23A4A8C13E1').find_all('transition_m_triggers').append(  # selected_down
        """
        <trigger
            trigger_component="854991D1-D51D-40AC-9053C46DF54FSS00"
            trigger_property="Visibility true"/>
        """
    )
    
    offset = 38 + 34
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
        DoIfElse(RootComponent.Dimensions.y < 1000, self.SetDockOffset(10, -270), self.SetDockOffset(10, -338))
    '''
    tag['context_function_id'] = format_str(s)
    
    tag = find_by_callback_id(find_by_id(xml, 'info_panel_parent'), 'ContextCommandEvent')
    
    # language=javascript
    s = '''
        DoIfElse(RootComponent.Dimensions.y < 1000, self.SetDockOffset(10, -270), self.SetDockOffset(10, -338))
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
    
    elem_id = "gold_value"
    # language=javascript
    s = '''
        RoundFloat(
            UnitList.Filter(IsAlive && !IsShattered).Sum(
                (
                    exp_cost = GetIfElse(UnitRecordContext.IsRenown, 0, ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11) ),
                    al = GetIf(
                        IsCharacter,
                        UnitDetailsContext.AbilityDetailsList
                            .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                            .Filter(IsUnitUpgrade)
                            .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                            .Sum(AdditionalMeleeCp + AdditionalMissileCp)
                    )
                ) =>
                {HealthPercent * (UnitRecordContext.Cost + exp_cost + al)}
            )
        )

    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
    elem_id = "label_score"
    # language=javascript
    s = '''
        RoundFloat(UnitList.Sum(BattleResultUnitContext.DamageDealtCost))
    '''  # In Domination summoned units from reinforcements are moved from reinf pool to army list and stay there
    set_context_callback(find_by_id(xml, elem_id), 'ContextTextLabel', s)
    
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
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextTooltipSetter', s)
    
    elem_id = "icon_clan"
    # language=javascript
    s = '''
        GetIf(PlayerName.StartsWith("VM.") || PlayerName.StartsWith("V_M") || PlayerName.StartsWith("VM ") || PlayerName.StartsWith("VM_"), "ui/mod/images/clans/vm.png")
        + GetIf(PlayerName.StartsWith("-CB-") || PlayerName.StartsWith("CB "), "ui/mod/images/clans/cb.png")
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
        (BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer)
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
                  move_info_panel_higher(xml)
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
    
    edit_twui('ui/frontend ui/custom_battle_map_settings', add_dom_ffa_to_custom_battles)
    
    edit_twui('ui/common ui/unit_information',
              lambda xml: (
                  change_unit_info_kill_count(xml),
                  change_unit_info_hit_points(xml),
                  add_unit_info_gold_value(xml),
                  add_unit_info_fatigue(xml),
                  mod_stats_fatigue(xml),
                  split_abilities(xml),
                  add_unit_info_resistances(xml)
              )
              )
    edit_twui('ui/common ui/special_ability_tooltip',
              lambda xml: (
                  add_ability_gold_value(xml),
              )
              )
    
    edit_twui('ui/templates/custom_battle_team_entry', enable_button_ai)
    
    edit_twui('ui/mod/reinf_panel_supplies', prepare_reinf_panel_supplies)
    edit_twui('ui/mod/mod_team_list', prepare_mod_team_list)