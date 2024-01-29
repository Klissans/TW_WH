import os
import re
import shutil

from bs4 import BeautifulSoup

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper

soupFactory = BeautifulSoup("<b></b>", 'html.parser')


def find_by_name(xml, name):
    r = xml.find_all(lambda t: t.name == name)
    if len(r) == 0:
        raise Exception(f'Name {name} is missing')
    if len(r) > 1:
        raise Exception(f'Name {name} is not unique')
    return r[0]


def find_by(xml, attr_name: str, value: str):
    fn = lambda t: t.has_attr(attr_name) and t[attr_name] == value
    r = xml.find_all(fn)
    if len(r) == 0:
        raise Exception(f'{attr_name} {value} is missing')
    if len(r) > 1:
        raise Exception(f'{attr_name} {value} is not unique')
    return r[0]


def find_by_id(xml, id: str):
    return find_by(xml, 'id', id)


def find_by_guid(xml, guid: str):
    return find_by(xml, 'uniqueguid', guid)


def find_by_callback_id(xml, callback_id: str):
    return find_by(xml, 'callback_id', callback_id)


def replace_escape_characters(s: str):
    return s.replace('&lt;', '%%lt%%').replace('&gt;', '%%gt%%').replace('&quot;', '%%quot%%').replace('&amp;', '%%amp%%')


def read_twui(fp: str, is_custom=False):
    path = f'xmls/twui/{fp}.twui.xml' if is_custom else f'../../data/{fp}.twui.xml'
    with open(path) as f:
        text = replace_escape_characters(f.read())
    
    pattern = r'&[^;]+;'
    matches = re.findall(pattern, text)
    print(set(matches))
    return text


def read_xml_component(fp: str):
    with open(f'xmls/components/{fp}.xml') as f:
        text = replace_escape_characters(f.read())
    elem = BeautifulSoup(text, 'lxml-xml').contents[0]
    return elem


def write(fp: str, xml):
    output = f'output/{fp}.twui.xml'
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.write(xml.prettify(formatter=None).replace('%%lt%%', '&lt;').replace('%%gt%%', '&gt;').replace('%%quot%%',
                                                                                                         '&quot;').replace(
            '%%amp%%', '&amp;'))


def edit_twui(fp: str, fn):
    is_custom = '/mod/' in fp
    xml = BeautifulSoup(read_twui(fp, is_custom), 'lxml-xml')
    fn(xml)
    write(fp, xml)


def format_str(s: str):
    return s.replace('<', '%%lt%%').replace('>', '%%gt%%').replace('"', '%%quot%%').replace('&', '%%amp%%')


def add_element(xml, elem, where):
    find_by_name(xml.layout.hierarchy, where).append(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)


def insert_after_element(xml, elem, where):
    find_by_name(xml.layout.hierarchy, where).insert_after(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)

def add_element_from_string(xml, desc, where):
    elem = BeautifulSoup(desc, 'lxml-xml').contents[0]
    find_by_name(xml.layout.hierarchy, where).append(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)


def insert_after_element_from_string(xml, desc, where):
    elem = BeautifulSoup(desc, 'lxml-xml').contents[0]
    find_by_name(xml.layout.hierarchy, where).insert_after(soupFactory.new_tag(elem.name, this=elem["this"]))
    xml.layout.components.append(elem)


def set_context_callback(elem, callback_id: str, context_function: str):
    tag = find_by_callback_id(elem, callback_id)
    tag['context_function_id'] = format_str(context_function)
    return tag


def create_context_callback_as_string(id, object, function):
    desc = f'''
        <callback_with_context
            callback_id="{id}"
            context_object_id="{object}"
            context_function_id="{format_str(function)}">
        </callback_with_context>
    '''
    return desc


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
    s = '''"[[img:ui/skins/default/icon_income.png]][[/img]]"
                + RoundFloat(UnitRecordContext.Cost
                    + GetIfElse(UnitRecordContext.IsRenown, 0, ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11) )
                    + GetIfElse(
                        IsCharacter,
                        AbilityDetailsList
                            .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                            .Filter(IsUnitUpgrade)
                            .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                            .Sum(AdditionalMeleeCp + AdditionalMissileCp),
                        0
                    )
                )
                + GetIf(IsBattle, " [" +
                    RoundFloat( (UnitRecordContext.Cost
                        + GetIfElse(UnitRecordContext.IsRenown, 0, ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11))
                        + GetIfElse(
                            IsCharacter,
                            AbilityDetailsList
                                .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                                .Filter(IsUnitUpgrade)
                                .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                                .Sum(AdditionalMeleeCp + AdditionalMissileCp),
                            0
                        )
                    ) * BattleUnitContext.HealthPercent )
                + "]")
                '''
    set_context_callback(elem, 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        "[[img:ui/skins/default/icon_income.png]][[/img]]"
        + Format("%d%S%S",
            UnitRecordContext.Cost,
            GetIf(ExperienceLevel > 0, GetIfElse(UnitRecordContext.IsRenown, "", Format(" [[img:ui/skins/default/experience_%d.png]][[/img]]%d", ExperienceLevel, RoundFloat(ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11)) ) )),
            GetIf(IsCharacter,
                Format(" %S",
                    AbilityDetailsList
                    .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                    .Filter(IsUnitUpgrade)
                    .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                    .JoinString(Format("[[img:%S]][[/img]]%d", BaseRecordContext.IconPath.ToLower, RoundFloat(AdditionalMeleeCp + AdditionalMissileCp)), " ")
            ))
        )
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
                    "0"
                )
            }
        ) +
        Format("[[img:ui/battle ui/ability_icons/resistance_physical.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_physical") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "0"
                )
            }
        ) +
        Format("[[img:ui/battle ui/ability_icons/resistance_magic.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_magic") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "0"
                )
            }
        ) +
        Format("[[img:ui/battle ui/ability_icons/resistance_missile.png]][[/img]]%S ",
            (a = AbilityDetailsList.FirstContext(Key=="resistance_missile") ) => {
                GetIfElse(
                    IsContextValid(a),
                    ( us = a.Name, i = GetIfElse(IsLocChinese, us.RFind(Loc("chinese_colon")), us.RFind(":")) + 1, uss = us.Substr(i, us.RFind('%') - i), s = StringSubString(uss, 0) ) => {Format("[[col:green]]%S[[/col]]", StringReplace(s, " ", ""))},
                    "0"
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
                                "0"
                            )
                        }
                    )
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
        FormatNumber(DisplayedValue) +
            GetIf(Key == "stat_melee_attack" && StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState > 0, " | " + FormatNumber(DisplayedValue * (
                GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 1, 0.95)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 2, 0.95)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 3, 0.85)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 4, 0.75)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 5, 0.70)
                ))) +
            GetIf(Key == "scalar_speed" && StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState > 1, " | " + FormatNumber( DisplayedValue * (
                GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 2, 0.95)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 3, 0.90)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 4, 0.85)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 5, 0.85)
                ))) +
            GetIf(Key == "stat_charge_bonus" && StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState > 2, " | " + FormatNumber( DisplayedValue * (
                GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 3, 0.90)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 4, 0.75)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 5, 0.70)
                ))) +
            GetIf(Key == "stat_armour" && StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState > 3, " | " + FormatNumber( DisplayedValue * (
                GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 0, 1)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 1, 1)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 2, 1)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 3, 1)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 4, 0.90)
                + GetIf(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 5, 0.75)
                ))) +
            GetIf(Key == "stat_melee_defence" && StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState > 4, " | " + FormatNumber( DisplayedValue * (
                GetIfElse(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 5, 0.90, 1.00)
                ))) +
            GetIf(Key == "stat_missile_damage_over_time" && StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState > 4, " | " + FormatNumber( DisplayedValue * (
                GetIfElse(StoredContextFromParent("CcoUnitDetails").BattleUnitContext.FatigueState == 5, 0.90, 1.00)
                )))
    '''
    cb = set_context_callback(find_by_guid(xml, 'F0F1DC3F-6E56-4627-81284E05CEE668E7'), 'ContextNumberFormatter', s)
    cb['callback_id'] = 'ContextTextLabel'


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
        (BattleRoot.IsSpectator || BattleRoot.IsReplay || !BattleRoot.IsMultiplayer) && HasRealmOfSouls
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextVisibilitySetter', s)
    
    elem_id = "gold_value"
    # language=javascript
    s = '''
        RoundFloat(
            UnitList.Filter(IsAlive && !IsShattered)
                .Sum(HealthPercent *
                    (UnitRecordContext.Cost
                    + GetIfElse(UnitRecordContext.IsRenown, 0, ExperienceLevel * (3 * UnitRecordContext.Cost / 100.0 + 11) )
                    + GetIfElse(
                        IsCharacter,
                        UnitDetailsContext.AbilityDetailsList
                            .Transform(DatabaseRecordContext("CcoUnitAbilityRecord", Key))
                            .Filter(IsUnitUpgrade)
                            .Transform(DatabaseRecordContext("CcoUnitSpecialAbilityRecord", Key))
                            .Sum(AdditionalMeleeCp + AdditionalMissileCp),
                        0
                    )
                    )
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
    
    elem_id = "icon_player"
    # language=javascript
    s = '''
        GetIf(PlayerName == "RoflanBuldiga", "ui/mod/images/roflanbuldiga.png")
    '''
    set_context_callback(find_by_id(xml, elem_id), 'ContextImageSetter', s)
    
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


if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    rpfm = RPFM4Wrapper()
    
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
                  add_capture_weight(xml)
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
    
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    
    MOD_NAME = '!Klissan_DOM_patch'
    OUTPUT_DIR = 'output'
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    
    """
   <!-- AbilityIconList.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities")
    ===WORKS===
    (al = AbilityIconList, x =  AbilityIconList.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x }
    (al = AbilityIconList, x =  al.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x }

    ==DOES NOT WORK==
    (al = AbilityIconList; x =  AbilityIconList.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x }
    (al = AbilityIconList, x =  al.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { al; x }
    (al = AbilityIconList, x =  al.Filter(CategoryStateName == "spells" || CategoryStateName == "abilities") ) => { x, x }
    (al = AbilityIconList, f = (x) => { x.Filter(CategoryStateName == "spells") } ) => { f(al) }
    -->
"""