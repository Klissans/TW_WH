import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper

if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    shutil.copy2('../../_lua_shared/_helpers.klissan.lua', 'output/script/_lib/mod/')
    shutil.copy2('../../_lua_shared/_helpers_campaign.klissan.lua', 'output/script/campaign/mod/')
    
    MOD_NAME = '!Klissan_roc_beta'
    OUTPUT_DIR = 'output'
    rpfm = RPFM4Wrapper()
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    