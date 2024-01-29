import os
import shutil

from whlib.settings import SETTINGS
from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper

from src.utils import Utils
from pprint import pprint

from factions.beastmen import beastmen
from factions.bretonnia import bretonnia
from factions.daemons_of_chaos import daemons_of_chaos
from factions.dark_elves import dark_elves
from factions.dwarfs import dwarfs
from factions.grand_cathay import grand_cathay
from factions.greenskins import greenskins
from factions.high_elves import high_elves
from factions.khorne import khorne
from factions.kislev import kislev
from factions.lizardmen import lizardmen
from factions.norsca import norsca
from factions.nurgle import nurgle
from factions.ogre_kingdoms import ogre_kingdoms
from factions.skaven import skaven
from factions.slaanesh import slaanesh
from factions.the_empire import the_empire
from factions.tomb_kings import tomb_kings
from factions.tzeentch import tzeentch
from factions.vampire_coast import vampire_coast
from factions.vampire_counts import vampire_counts
from factions.warriors_of_chaos import warriors_of_chaos
from factions.wood_elves import wood_elves

if __name__ == '__main__':
    typee = 'Workshop'

    if typee == 'Workshop':
        MOD_NAME = '!Klissan_EntLadder_Limits'
    PREFIX = f'{MOD_NAME}_'
    OUTPUT_DIR = 'output'
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    rpfm = RPFM4Wrapper()
    handler = Handler()
    hh = HandlerHelper(handler)

    utils = Utils(handler, PREFIX)


    all_list = utils.get_faction_units('wh2_main_def_dark_elves')
    cha_list = set() #set([x for x in all_list if '_cha_' in x])
    l = list(set(all_list) - cha_list)

    pprint(sorted(l))
    # pprint(utils.get_faction_units('wh_main_chs_chaos'))


    # pprint(utils.get_faction_units('wh3_main_tze_tzeentch'))
    # pprint(utils.get_faction_units('wh3_main_sla_slaanesh'))
    # pprint(utils.get_faction_units('wh3_main_nur_nurgle'))
    # pprint(utils.get_faction_units('wh3_main_kho_khorne'))


    factions_list = [
        beastmen,
        bretonnia,
        daemons_of_chaos,
        dark_elves,
        dwarfs,
        grand_cathay,
        greenskins,
        high_elves,
        khorne,
        kislev,
        lizardmen,
        norsca,
        nurgle,
        ogre_kingdoms,
        skaven,
        slaanesh,
        the_empire,
        tomb_kings,
        tzeentch,
        vampire_coast,
        vampire_counts,
        warriors_of_chaos,
        wood_elves,
    ]
    for faction_limits in factions_list:
        utils.add_faction_limits(faction_limits)



    handler.dump_mod_tables(OUTPUT_DIR)
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    pass
