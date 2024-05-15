import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper

from grudges import mod_grudges_ui

if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    mod_grudges_ui()
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    shutil.copy2('../_lua_shared/_helpers.klissan.lua', 'output/script/_lib/mod/')
    shutil.copy2('../_lua_shared/_helpers_campaign.klissan.lua', 'output/script/campaign/mod/')
    
    MOD_NAME = '!Klissan_malakai_worldtour'
    OUTPUT_DIR = 'output'
    rpfm = RPFM4Wrapper()
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    os.startfile(r"F:\runcher-v0.7.102-x86_64-pc-windows-msvc\shortcuts\malakai.lnk")