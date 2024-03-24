import json
import os
import shutil
import pandas as pd

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper
from whlib.twui import *


def create_random_army_abilities_for_all_units(hh):
    handler = hh.handler
    #################
    # Random army abilities
    #################
    FACTION_PREFIX = 'Klissan_all_the_units__'
    faction_group_key = f'{FACTION_PREFIX}faction_group_key'
    
    df = handler.duplicate_table('faction_groups_tables', prefix=PREFIX, copy_data=False).data
    df.loc[faction_group_key] = {'key': faction_group_key, 'effect_bundle': '', 'order': 0}
    
    df = handler.duplicate_table('battle_secondary_currency_sources_links_tables', prefix=PREFIX, copy_data=False).data
    df.loc[faction_group_key] = {"currency_type": "army_ability_bar_fill", "faction": "", "faction_group": faction_group_key, "source_type": "army_losses", "battle_type": "",
                                 "excluded_battle_type": "", "battle_set_pieces": "", "battles": "", "source_unitary_value": 1, "attacker": True, "defender": True}
    
    army_abilities = {f'{FACTION_PREFIX}army_ability_tier_0': 250, f'{FACTION_PREFIX}army_ability_tier_1': 500, f'{FACTION_PREFIX}army_ability_tier_2': 750, f'{FACTION_PREFIX}army_ability_tier_3': 1500}
    df = handler.duplicate_table('army_special_abilities_tables', prefix=PREFIX, copy_data=False).data
    start_index = 7456384
    for i, (army_ability_key, army_ability_cost) in enumerate(army_abilities.items()):  # order is not guaranteed
        df.loc[army_ability_key] = {'army_special_ability': army_ability_key, 'unit_special_ability': army_ability_key, 'unique_id': start_index + i, 'enables_siege_assault': False}
    
    df = handler.duplicate_table('battle_currency_army_special_abilities_cost_values_tables', prefix=PREFIX, copy_data=False).data
    for army_ability_key, army_ability_cost in army_abilities.items():
        df.loc[army_ability_key] = {'item_type': army_ability_key, 'cost_value': army_ability_cost, 'currency_type': 'army_ability_bar_fill'}
    
    df = handler.duplicate_table('army_special_abilities_for_faction_junctions_tables', prefix=PREFIX, copy_data=False).data
    with open('all_units_faction_keys.json') as file:
        faction_keys = json.load(file)
    for ab in army_abilities:
        for fkey in faction_keys:
            df.loc[ab + fkey] = {'army_special_ability': ab, 'faction': fkey}
    # TODO copy factions (and subculture) from all_the_units mod
    # df: pd.DataFrame = handler.duplicate_table('factions_tables', prefix=PREFIX, copy_data=False).data
    # df[~df['subculture'].str.contains('wh2_main_rogue')]
    # handler.db['factions_tables'].data.loc['wh3_dlc23_hero_abilities_crooked_dice']
    
    #################


if __name__ == '__main__':
    MOD_NAME = '!Klissan_Roflan_Buildiga'
    PREFIX = f'{MOD_NAME}_'
    OUTPUT_DIR = 'output'
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)
        
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    
    handler = Handler()
    hh = HandlerHelper(handler)
    create_random_army_abilities_for_all_units(hh)
    handler.dump_mod_tables(OUTPUT_DIR)
    
    rpfm = RPFM4Wrapper()
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    
    os.startfile(r"F:\runcher-v0.7.102-x86_64-pc-windows-msvc\shortcuts\lucky_test.lnk")
    