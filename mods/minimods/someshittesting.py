import os
import shutil
import glob
from pprint import pprint

from whlib.rpfm_wrapper import RPFMWrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper

from pprint import pprint


# def get_unit_animations(self, animation_key):
#     res = {}
#     anim_files = self.handler.anim_files
#     for bin_fn in glob.glob("animations/database/battle/bin/*.bin", recursive=True):
#         unit_anim_list = anim_files['lookup'][bin_fn]['content'].find_all('animation')
#         for anim in unit_anim_list:
#             for inst in anim.find_all('instance'):
#                 if inst['meta'] == "":
#                     continue
#                 for item in anim_files['lookup'][inst['meta']]['content']['Items']:
#                     if item == 'SPLASH_ATTACK' or item == 'IMPACT_POS'
#
#                     res[key][anim['slot']]['instances'].append({'file_name': inst['meta'], 'meta': meta})
#     return res


def get_unit_animations(handler):
    os.chdir('C:\\Users\\{}\\AssetEditor\\Reports\\MetaDataJsons\\Warhammer III_130')
    anim_files = handler.anim_files
    for fn in glob.glob('animations/battle/*/*/*anm.meta.json', recursive=True):
        fn = fn.replace('\\', '/')[:-5]
        unit_anim_list = anim_files['lookup'][fn]['content']['Items']
        for item in unit_anim_list:
            if item['Name'] == 'SPLASH_ATTACK':
                if item['Version'] >= 10:
                    start_pos = [float(x) for x in item['StartPosition'].split(',')]
                    end_pos = [float(x) for x in item['StartPosition'].split(',')]
                    # if item['AoeShape'] == 0 and 180 < item['AngleForCone'] and item['AngleForCone'] != 360:
                    #     print(fn, 'Aoe: ', item['AoeShape'], '|', item['AngleForCone'])
                    # if abs(start_pos[2]) < 0.001 and abs(end_pos[2]) > 0.001:
                    #     print(fn, 'Aoe: ', item['AoeShape'], '|',  item['StartPosition'], '|',  item['EndPosition'])
                    if abs(start_pos[1]) > 0.001 or abs(end_pos[1]) > 0.001:
                        print(fn, 'Aoe: ', item['AoeShape'], '|',  item['StartPosition'], '|',  item['EndPosition'])
                    # if item['EndTime'] - item['StartTime'] < 0.001:
                    #     continue
                    # print(fn, item['StartTime'], item['EndTime'], item['StartPosition'], item['EndPosition'])

from src.formatter import Formatter
if __name__ == '__main__':
    MOD_NAME = '!ASMR.MOVIE'
    PREFIX = f'{MOD_NAME}_'
    # OUTPUT_DIR = 'output'
    # if os.path.exists(OUTPUT_DIR):
    #     shutil.rmtree(OUTPUT_DIR)
    #     os.mkdir(OUTPUT_DIR)

    rpfm = RPFMWrapper()
    handler = Handler()
    hh = HandlerHelper(handler)
    formatter = Formatter(hh, 'ultra')

    get_unit_animations(handler)


    # x = formatter.get_unit_animation_dev('wh3_main_ksl_inf_tzar_guard_0')
    # print(x)




    # entry = handler.get_entry_by_index('effects_tables', 'wh2_dlc17_effect_ability_enable_bloodgreed')
    # handler.expand_entry_recursively(entry)
    # pprint(entry)
    # entry = handler.get_entry_by_index('land_units_tables', 'wh2_dlc11_cst_mon_necrofex_colossus_ror_0')
    # # pprint(entry)
    # handler.expand_entry_recursively(entry)
    # pprint(entry)
    #
    # hh = HandlerHelper(handler)
    # info = hh.get_melee_info('wh2_dlc17_bst_ghorgon_ror')
    # pprint(info)
    #
    # x = handler.db['abilities_tables'].copy()
    # handler.duplicate_table('land_units_tables', copy_data=True)
    #
    # t = handler.duplicate_table('unit_description_short_texts__', prefix='asmr_', copy_data=True)
    # t.data['text'] = ''
    # handler.dump_mod_tables(OUTPUT_DIR)
    # rpfm.make_package('test', OUTPUT_DIR)
