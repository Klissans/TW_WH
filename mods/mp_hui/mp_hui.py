import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper

from battle_ui import mod_battle_ui



if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    mod_battle_ui()
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    
    MOD_NAME = '!Klissan_DOM_patch'
    OUTPUT_DIR = 'output'
    rpfm = RPFM4Wrapper()
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    os.startfile(r"F:\runcher-v0.7.102-x86_64-pc-windows-msvc\shortcuts\dev.lnk")
    
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