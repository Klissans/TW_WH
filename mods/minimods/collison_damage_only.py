import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler


if __name__ == '__main__':
    MOD_NAME = '!!Klissan_collision_damage_test'
    PREFIX = f'{MOD_NAME}_'
    OUTPUT_DIR = 'output'
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    rpfm = RPFM4Wrapper()
    handler = Handler()

    mwt_df = handler.duplicate_table('melee_weapons_tables', prefix=PREFIX, copy_data=True).data
    mwt_df['damage'] = 0
    mwt_df['ap_damage'] = 0
    mwt_df['bonus_v_infantry'] = 0
    mwt_df['bonus_v_large'] = 0
    mwt_df['collision_attack_max_targets'] = 0
    mwt_df['collision_attack_max_targets_cooldown'] = 0
    mwt_df['splash_attack_target_size'] = None
    mwt_df['splash_attack_max_attacks'] = 0

    lut_df = handler.duplicate_table('land_units_tables', prefix=PREFIX, copy_data=True).data
    lut_df['charge_bonus'] = 0



    handler.dump_mod_tables(OUTPUT_DIR)
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    pass