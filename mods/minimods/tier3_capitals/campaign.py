import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper

if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    
    MOD_NAME = '!Klissan_campaign'
    OUTPUT_DIR = 'output'
    rpfm = RPFM4Wrapper()
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    os.startfile(r"F:\runcher-v0.7.102-x86_64-pc-windows-msvc\shortcuts\campaign.lnk")