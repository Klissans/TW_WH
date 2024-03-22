import pandas as pd
from whlib.settings import SETTINGS
from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper
from src.localizator import Localizator
from src.formatter import Formatter, _indentstr, _icon_battle


def compare_unit(pre_hh, post_hh, unit_id):
    if not unit_id in pre_hh.handler.db['main_units_tables'].data.index:
        print(f"New unit: {unit_id}")



def process_main_units(pre_hh, post_hh):
    post_handler = post_hh.handler

    for unit_id in post_handler.db['main_units_tables'].data.index:
        # info = hh.get_unit_info(unit_id)
        compare_unit(pre_hh, post_hh, unit_id)

        # formatted_info = formatter.get_short_unit_desc(info)
        # full_formatted_info = formatter.get_full_unit_desc(info, luid)
        # name = 'unit_description_short_texts_text_' + luid
        # historical_name = 'unit_description_historical_texts_text_' + luid
        # bp_name = 'ui_unit_bullet_point_enums_onscreen_name_' + unit_id
        # bp_tooltip = 'ui_unit_bullet_point_enums_tooltip_' + unit_id
        #
        # bp_text_loc.data.loc[bp_name] = {'key': bp_name, 'text': formatter.loctr.tr('bp_unit_stats'), 'tooltip': True}
        # bp_text_loc.data.loc[bp_tooltip] = {'key': bp_tooltip, 'text': full_formatted_info, 'tooltip': True}




if __name__ == '__main__':
    pre_settings = SETTINGS.copy()
    pre_settings['extract_path'] = "C:\\Users\\{}\\PycharmProjects\\TW_WH\\data_221"
    pre_handler = Handler(pre_settings)
    pre_hh = HandlerHelper(pre_handler)

    post_handler = Handler()
    post_hh = HandlerHelper(post_handler)

    process_main_units(pre_hh, post_hh)
    pass
