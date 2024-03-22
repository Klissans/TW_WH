import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper
from src.localizator import Localizator
from src.formatter import Formatter



def generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, unit_key):
    uubpet.loc[unit_key] = {'key':unit_key, 'state': 'very_positive',  'sort_order': 0}
    uubpuot.loc[unit_key] = {'unit_key': unit_key, 'bullet_point': unit_key}

    info = hh.get_unit_info(unit_key)
    luid = info['land_unit']
    full_formatted_info = formatter.get_full_unit_desc(info, luid)
    bp_name = 'ui_unit_bullet_point_enums_onscreen_name_' + unit_key
    bp_tooltip = 'ui_unit_bullet_point_enums_tooltip_' + unit_key

    bp_text_loc.loc[bp_name] = {'key': bp_name, 'text': 'Unit Stats', 'tooltip': True}
    bp_text_loc.loc[bp_tooltip] = {'key': bp_tooltip, 'text': full_formatted_info, 'tooltip': True}



def do_stuff(hh, formatter):
    handler = hh.handler
    unique_unit_index = handler.db['main_units_tables'].data['unique_index'].max() + 8888

    mut = handler.duplicate_table('main_units_tables', prefix=PREFIX, copy_data=False).data
    lut = handler.duplicate_table('land_units_tables', prefix=PREFIX, copy_data=False).data
    uvt = handler.duplicate_table('unit_variants_tables', prefix=PREFIX, copy_data=False).data
    ucbpt = handler.duplicate_table('units_custom_battle_permissions_tables', prefix=PREFIX, copy_data=False).data

    melee_wt = handler.duplicate_table('melee_weapons_tables', prefix=PREFIX, copy_data=False).data

    lu_loc = handler.duplicate_table('land_units__', prefix=PREFIX, copy_data=False).data

    uubpet = handler.duplicate_table('ui_unit_bullet_point_enums_tables', prefix=PREFIX, copy_data=False).data
    uubpuot = handler.duplicate_table('ui_unit_bullet_point_unit_overrides_tables', prefix=PREFIX, copy_data=False).data
    bp_text_loc = handler.duplicate_table('ui_unit_bullet_point_enums__', prefix=PREFIX, copy_data=False).data

    def copy_unit(mut_base_key: str, new_key: str):
        nonlocal unique_unit_index
        main_unit = handler.db['main_units_tables'].data.loc[mut_base_key].to_dict()
        land_unit = handler.db['land_units_tables'].data.loc[main_unit['land_unit']].to_dict()

        df = handler.db['unit_variants_tables'].data
        unit_variant = df[df['unit'] == land_unit['key']].iloc[0].to_dict()
        unit_variant['name'] = new_key
        unit_variant['unit'] = new_key
        uvt.loc[new_key] = unit_variant

        df = handler.db['units_custom_battle_permissions_tables'].data
        for index, row in df[df['unit'] == main_unit['unit']].iterrows():
            unit_permission = row.to_dict()
            unit_permission['unit'] = new_key
            ucbpt.loc[new_key + '_' + row['faction']] = unit_permission

        land_unit['key'] = new_key
        lut.loc[new_key] = land_unit

        main_unit['unit'] = new_key
        main_unit['land_unit'] = land_unit['key']
        main_unit['unique_index'] = unique_unit_index
        unique_unit_index += 1
        mut.loc[new_key] = main_unit
        lu_loc.loc[new_key] = {'key': 'land_units_onscreen_name_'+new_key, 'text': new_key, 'tooltip': False}
        return new_key


    def copy_melee_weapon(base_key: str, new_key: str):
        melee_weapon = handler.db['melee_weapons_tables'].data.loc[base_key].to_dict()
        melee_weapon['key'] = new_key
        melee_wt.loc[new_key] = melee_weapon
        return new_key


    mut_orig_df = handler.db['main_units_tables'].data
    lut_orig_df = handler.db['land_units_tables'].data
    mwt_orig_df = handler.db['melee_weapons_tables'].data
    perm_df = handler.db['units_custom_battle_permissions_tables'].data

    for index, row in mut_orig_df.iterrows():
        mu_id = row['unit']
        lu_id = row['land_unit']
        mw_id = lut_orig_df.loc[lu_id]['primary_melee_weapon']
        melee_weapon = mwt_orig_df.loc[mw_id]
        if melee_weapon['collision_attack_max_targets'] > 0:

            if not (perm_df['unit'] == mu_id).any():
                print(mu_id)
                continue

            splash_wpn = copy_melee_weapon(mw_id, mw_id + '_splash')
            melee_wt.loc[splash_wpn, 'collision_attack_max_targets'] = 0
            melee_wt.loc[splash_wpn, 'collision_attack_max_targets_cooldown'] = 0
            lu_splash = copy_unit(mu_id, mu_id + '_splash')
            lut.loc[lu_splash, 'primary_melee_weapon'] = splash_wpn
            generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, lu_splash)

            collision_wpn = copy_melee_weapon(mw_id, mw_id + '_collision')
            melee_wt.loc[collision_wpn, 'splash_attack_target_size'] = None
            melee_wt.loc[collision_wpn, 'splash_attack_max_attacks'] = 0
            lu_collision = copy_unit(mu_id, mu_id + '_collision')
            lut.loc[lu_collision, 'primary_melee_weapon'] = collision_wpn
            generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, lu_collision)




if __name__ == '__main__':
    MOD_NAME = '!Klissan_melee_attacks_test'
    PREFIX = f'{MOD_NAME}_'
    OUTPUT_DIR = 'output'
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    rpfm = RPFM4Wrapper()
    handler = Handler()

    hh = HandlerHelper(handler)
    localizator = Localizator(handler, PREFIX)
    formatter = Formatter(hh, localizator, 'ultra')

    rules_df = handler.duplicate_table('_kv_rules_tables', prefix=PREFIX, copy_data=False).data
    k = 'collision_damage_maximum'
    rules_df.loc[k] = {'key': k, 'value': 0}

    do_stuff(hh, formatter)

    handler.dump_mod_tables(OUTPUT_DIR)
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    pass