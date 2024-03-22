import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler


if __name__ == '__main__':
    MOD_NAME = '!Klissan_trainier'
    PREFIX = f'{MOD_NAME}_'
    OUTPUT_DIR = 'output'
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    rpfm = RPFM4Wrapper()
    handler = Handler()

    usat_df = handler.duplicate_table('unit_special_abilities_tables', prefix=PREFIX, copy_data=True).data
    k = 'mana_cost'
    usat_df.loc[usat_df[k] > 0, k] = 1
    k = 'recharge_time'
    usat_df.loc[usat_df[k] > 0, k] = 0

    kvm_df = handler.duplicate_table('_kv_winds_of_magic_params_tables', prefix=PREFIX, copy_data=True).data
    kvm_df.loc['custom_battle_pool_initial_amount', 'value'] = 999
    kvm_df.loc['custom_battle_pool_initial_mana_available_ratio', 'value'] = 1.0
    kvm_df.loc['pool_max_amount', 'value'] = 999

    handler.dump_mod_tables(OUTPUT_DIR)
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    pass