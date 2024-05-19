from whlib.twui import *

def edit_docker_right_timer(xml):
    # language=javascript
    s = '''
        PlayersFaction.FactionFlagRotated
    '''
    create_context_callback(find_by_id(xml, 'icon_timer'), "ContextImageSetter", "CcoStaticObject", s)
    
    # language=javascript
    s = '''
        (
            players_settled_grudges = PlayersFaction.PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total,
            total_settled_grudges = CampaignRoot.FactionList.Filter(CultureContext.Key == 'wh_main_dwf_dwarfs' && !IsDead).Sum(PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total),
            share = GetIfElse(RoundFloat(total_settled_grudges) == 0, 0, RoundFloat(players_settled_grudges / total_settled_grudges * 100 ))
        ) =>
        {
            Format('%d%%', share)
        }
    '''
    set_context_callback(find_by_id(xml, 'dy_timer'), 'ContextTextLabel', s)
    
    # language=javascript
    s = '''
        (
            LF = StringGet('ui_text_replacements_localised_text_new_line'),
            effect_bundle = PlayersFaction.EffectBundleList.FirstContext(Key.Contains('wh3_dlc25_grudge_cycle_share_')),
            effects = effect_bundle.EffectList.JoinString(Format('[[img:%s]][[/img]]%s', IconPath, LocalisedText), LF),
            effect_str = Format('[[img:icon_grudges]][[/img]]%s', effect_bundle.Name) + LF + effects + LF + LF,
            
            dwarf_factions = CampaignRoot.FactionList.Filter(CultureContext.Key == 'wh_main_dwf_dwarfs' && !IsDead).Sort(PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total),
            total_settled_grudges = dwarf_factions.Sum(PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total),
            formatted_string = dwarf_factions.JoinString(
                (x,
                    faction_points = x.PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total,
                    share = GetIfElse(RoundFloat(total_settled_grudges) == 0, 0, RoundFloat(faction_points / total_settled_grudges * 100))
                ) => Format('%s: %d (%d%%) [[img:icon_grudges]][[/img]]', NameWithIcon, faction_points, share),
                LF
            ),
            
            players_settled_grudges = PlayersFaction.PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total,
            share = GetIfElse(RoundFloat(total_settled_grudges) == 0, 0, RoundFloat(players_settled_grudges / total_settled_grudges * 100)),
            share_string = Format('%d / %d = %d%%', RoundFloat(players_settled_grudges), RoundFloat(total_settled_grudges), share)
        ) =>
        {
            effect_str + '[[img:icon_grudges]][[/img]] ' + share_string + LF + LF + formatted_string
        }
    '''
    create_context_callback(find_by_id(xml, 'docker_right_timer'), "ContextTooltipSetter", "CcoStaticObject", s, {'update_constant': '100'})
    
    # language=javascript
    s = '''
        (
            current = CampaignRoot.FactionList.Filter(CultureContext.Key == 'wh_main_dwf_dwarfs' && !IsDead).Sum(PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total),
            target = ScriptObjectContext('cycle_grudge_target').NumericValue,
            share = GetIfElse(current == 0, 0, RoundFloat(current / target * 100))
        ) =>
        Format('%d%%', share)
    '''
    set_context_callback(find_by_id(xml, 'dy_percentage'), "ContextTextLabel", s)
    
    
def edit_grudges_tooltip(xml):
    find_by_id(xml, 'holder_turns_remaining_in_cycle').decompose()
    
    # language=javascript
    s = '''
        (
            total_settled_grudges = CampaignRoot.FactionList.Filter(CultureContext.Key == 'wh_main_dwf_dwarfs' && !IsDead).Sum(PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total),
            world_grudges = ScriptObjectContext('world_grudge_value').NumericValue
        ) =>
        Format('%d (%d)', RoundFloat(total_settled_grudges), RoundFloat(world_grudges))
        
    '''
    create_context_callback(find_by_id(xml, 'dy_total_grudges'), "ContextTextLabel", "CcoStaticObject", s)
    
    # language=javascript
    s = '''
        (
            current = CampaignRoot.FactionList.Filter(CultureContext.Key == 'wh_main_dwf_dwarfs' && !IsDead).Sum(PooledResourceContext('wh3_dlc25_dwf_grudge_points').Total),
            target = ScriptObjectContext('cycle_grudge_target').NumericValue,
            share = GetIfElse(current == 0, 0, RoundFloat(current / target * 100))
        ) =>
        { Format(Loc('grudge_cycles_grudges_in_current_cycle'), RoundFloat(current), RoundFloat(target), share)}
    '''
    create_context_callback(find_by_id(xml, 'dy_grudges_this_cycle'), "ContextTextLabel", "CcoStaticObject", s)
    
    
    # language=javascript
    s = '''
        (
            tc = TargettingContext,
            ritual = tc.RitualContext,
            ritual_key = ritual.RitualContext.Key,
            target = tc.CurrentTargetContext,
            target_type = ContextTypeId(target)
        ) =>
        {
            target_type
                | 'CcoCampaignSettlement' => 'region:' + target.RegionRecordKey
        }
    '''
    
    
def mod_grudges_ui():
    edit_twui('ui/campaign ui/dlc25_grudge_cycles',
              lambda xml: (
                  edit_docker_right_timer(xml)
              )
              )
    

    edit_twui('ui/campaign ui/tooltip_dlc25_grudge_cycles',
              lambda xml: (
                  edit_grudges_tooltip(xml)
              )
              )