import os
import shutil
import json

import pandas as pd

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper
from whlib.twui import *


def create_faction(hh):
    handler = hh.handler

    # df = handler.duplicate_table('cultures_tables', prefix=PREFIX, copy_data=False).data
    # culture_key = 'all_units_subculture'
    # df.loc[culture_key] = {'index': 999888666}
    
    # df = handler.duplicate_table('culture_pack_ids_tables', prefix=PREFIX, copy_data=False).data
    # culture_pack_ids_tables_key = 'all_units_subculture'
    # df.loc[culture_pack_ids_tables_key] = {'id': culture_pack_ids_tables_key}

    df = handler.duplicate_table('cultures_subcultures_tables', prefix=PREFIX, copy_data=False).data
    cultures_subcultures_tables_key = 'Klissan_all_units_subculture'  # wh3_main_sc_dae_daemons
    df.loc[cultures_subcultures_tables_key] = {'subculture': cultures_subcultures_tables_key, 'culture': 'wh2_main_rogue', 'index': 1771987881} # requires wh3_main_dae_daemons in order to chaos of reign to be assigned

    # df = handler.duplicate_table('culture_packs_tables', prefix=PREFIX, copy_data=False).data
    # # df.loc[(culture_pack_ids_tables_key, cultures_subcultures_tables_key)] = {'id': culture_pack_ids_tables_key, 'subculture': cultures_subcultures_tables_key} # multiindex doesn't work?
    # df.loc[culture_pack_ids_tables_key] = {'id': culture_pack_ids_tables_key, 'subculture': cultures_subcultures_tables_key}

    df: pd.DataFrame = handler.duplicate_table('factions_tables', prefix=PREFIX, copy_data=True).data
    drop_index = df[~df['subculture'].str.contains('wh2_main_rogue')].index
    df.drop(drop_index, inplace=True)
    # idx = pd.Series([x[0] not in x[1] for x in zip(df['key'], df['flags_path'])], index=df.index)
    # print(df[idx])
    # df[idx]['flags_path'] = df[idx]['key'].apply(lambda x: f'ui\\flags\\{x}')
    df.drop_duplicates(subset='flags_path', inplace=True)
    
    # same
    # ui/flags/wh2_dlc09_rogue_dwellers_of_zardok
    nonunique_flags = [
        'wh2_dlc09_rogue_black_creek_raiders',
        'wh2_dlc09_rogue_eyes_of_the_jungle',
        'wh2_dlc09_rogue_pilgrims_of_myrmidia'
    ]
    nu_idx = df['flags_path'].apply(lambda x: any([fpath in x for fpath in nonunique_flags]))
    df.drop(df[nu_idx].index, inplace=True)
    
    FACTION_PREFIX = 'Klissan_all_the_units__'
    
    df.loc['wh3_main_rogue_the_pleasure_tide', 'flags_path'] = r'ui\flags\wh3_main_rogue_the_pleasure_tide'
    df.loc['wh3_main_rogue_the_putrid_swarm', 'flags_path'] = r'ui\flags\wh3_main_rogue_the_putrid_swarm'
    df.loc['wh3_main_rogue_the_fluxion_host', 'flags_path'] = r'ui\flags\wh3_main_rogue_the_fluxion_host'
    df.loc['wh3_main_rogue_the_bloody_harvest', 'flags_path'] = r'ui\flags\wh3_main_rogue_the_bloody_harvest'
    df.loc['wh3_main_rogue_shadow_legion', 'flags_path'] = r'ui\flags\wh3_main_chs_shadow_legion'
    df.loc[:, 'key'] = FACTION_PREFIX + df['key']
    df.loc[:, 'index'] += 1
    df.loc[:, 'subculture'] = cultures_subcultures_tables_key
    df.loc[:, 'category'] = 'playable'
    
    main_faction_tables_key = df.iloc[0]['key']
    faction_keys = df['key'].values.tolist()
    with open('../random_build/all_units_faction_keys.json', 'w') as f:
        json.dump(faction_keys, f)

    factions_loc_df = handler.locs['factions__'].data
    loc_df = handler.duplicate_table('factions__', prefix=PREFIX, copy_data=False).data
    df = handler.duplicate_table('custom_battle_factions_tables', prefix=PREFIX, copy_data=False).data
    for i, fkey in enumerate(faction_keys):
        df.loc[fkey] = {'faction_key': fkey, 'sort_order': i, 'culture_sort_order': 1}
        loc_text = None
        okey = fkey[len(FACTION_PREFIX):]
        try:
            loc_text = factions_loc_df.loc[f'factions_screen_name_{okey}', 'text']
        except KeyError as e:
            beautify = lambda name: ' '.join([s.capitalize() for s in name.split('_')[2:]])
            loc_text = beautify(okey)
        loc_df.loc[f'factions_screen_name_{fkey}'] = {'key': f'factions_screen_name_{fkey}', 'text': loc_text, 'tooltip': True}
        
    #################
    # Random army abilities
    #################
    faction_group_key = f'{FACTION_PREFIX}faction_group_key'
    
    df = handler.duplicate_table('faction_groups_tables', prefix=PREFIX, copy_data=False).data
    df.loc[faction_group_key] = {'key': faction_group_key, 'effect_bundle': '', 'order': 0}
    
    #################
    
    df = handler.duplicate_table('faction_to_faction_groups_junctions_tables', prefix=PREFIX, copy_data=False).data
    for i, fkey in enumerate(faction_keys):
        df.loc[fkey] = {'faction_key': fkey, 'faction_group_key': faction_group_key}
        
    return main_faction_tables_key


# def add_army_ability_tier_1(hh, army_ability_key):
#     handler = hh.handler
#
#     uat_item = handler.db['unit_abilities_tables'].data.loc['wh3_dlc23_hero_abilities_crooked_dice']
#     uat_item['icon_name'] = 'ui/battle ui/ability_icons/wh3_dlc23_hero_passive_crooked_dice_1_2.png'
#     uat_item['is_unit_upgrade'] = False
#
#     df = handler.duplicate_table('unit_abilities_tables', prefix=PREFIX, copy_data=False).data
#     df[army_ability_key] = uat_item
#
#     df = handler.duplicate_table('unit_abilities_tables', prefix=PREFIX, copy_data=False).data
#     df[army_ability_key] = uat_item


def change_template_unit_group(xml):
    # language=javascript
    s = '''
        FactionRecordContext.Key == 'klissan_all_the_units_faction' ||
        !UnitListForUnitGroupParent(StoredContextRequired('CcoUiUnitGroupParentRecord')).IsEmpty
    '''
    set_context_callback(find_by_id(xml, 'template_unit_group'), 'ContextVisibilitySetter', s)
    
    
def change_unit_list(xml):
    # language=javascript
    s = '''
        GetIfElse(
            StoredContextFromParent('CcoCustomBattlePlayerSlot').FactionRecordContext.Key == 'klissan_all_the_units_faction',
            UnitList.Transform(CustomBattlePermissionsContext),
            StoredContextFromParent('CcoCustomBattlePlayerSlot').UnitListForUnitGroupParent(this).Reverse
        )
    ''' #
    set_context_callback(find_by_guid(xml, '644ED00C-B0E9-4438-93803CF58BCD572E'), 'ContextList', s)
    
    
def change_inactive_state_unit_card(xml):
    # language=javascript
    s = '''
        true
    '''
    set_context_callback(find_by_id(xml, 'unit_card'), 'ContextInactiveStateSetter', s)


if __name__ == '__main__':
    MOD_NAME = '!Klissan_All_The_Units'
    PREFIX = f'{MOD_NAME}_'
    OUTPUT_DIR = 'output'
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)
        
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    
    rpfm = RPFM4Wrapper()
    handler = Handler()
    hh = HandlerHelper(handler)

    # main_faction_tables_key = 'klissan_all_the_units_faction'
    main_faction_tables_key = create_faction(hh)
    
    # edit_twui('ui/frontend ui/custom_battle',
    #     lambda xml: (
    #         change_template_unit_group(xml),
    #         change_unit_list(xml),
    #         change_inactive_state_unit_card(xml)
    #     )
    # )

    core_df = handler.duplicate_table('units_custom_battle_permissions_tables', prefix=PREFIX, copy_data=True).data
    core_df.drop_duplicates('unit', inplace=True)
    core_df['faction'] = main_faction_tables_key

    handler.dump_mod_tables(OUTPUT_DIR)
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    