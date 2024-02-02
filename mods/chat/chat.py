import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.twui import *


def remove_obsolete_elements(xml):
    # rank
    destroy_element(xml, '46917C9E-BA63-4CC8-8557D9F3BF21998C')
    # player profile
    destroy_element(xml, '83C3055C-A12F-4642-B45E0CC0674AFB49')
    # enabling drag & drop support
    find_by_id(xml, 'frame_tr').LayoutEngine.decompose()


def add_chat_alert_icon_fe(xml):
    elem = read_xml_component('chat_alert_icon')
    add_element(xml, elem, "button_hud_chat")


def add_callbacks_to_chat(xml):
    # TODO add drag & drop support in minimized mode
    cb_shd = create_context_callback_as_string("SelfHandleDropCallback")
    cb_vs = create_context_callback_as_string("ContextVisibilitySetter", "CcoStaticObject", 'true', {'update_constant': ''})
    cb_tm = create_context_callback_as_string("TopmostObjectCallback", "CcoStaticObject", 'true', {'update_constant': ''})
    tag = find_by_id(xml, 'multiplayer_chat')
    tag.callbackwithcontextlist.append(replace_escape_characters(cb_shd))
    tag.callbackwithcontextlist.append(replace_escape_characters(cb_vs))
    tag.callbackwithcontextlist.append(replace_escape_characters(cb_tm))


# .Replace(':gsl:', '[[img:ui/mod/images/grudge_sl.png]][[/img]]')
# .Replace(':rb:', '[[img:ui/mod/images/roflanbuldiga.png]][[/img]]')

def remove_lock_visibility_button(xml):
    # button_lock_chat
    # destroy_element(xml, '8C931C2A-64A1-47D0-81D746F7F0BA03A4')
    blc = find_by_id(xml, 'button_lock_chat')
    # zero index is '\n'
    blc.component_image_uniqueguids.contents[1]['name'] = 'ui/skins/default/dev/icon_refresh.png'
    blc.override_images.contents[1]['value'] = 'ui/skins/default/dev/icon_refresh.png'
    lt = blc.localised_texts.contents[1]
    lt['tooltip_label'] = 'button_refresh_chat_Tooltip_11005e'
    lt['tooltip_text'] = 'Refresh chat'


def add_chat_name(xml):
    find_by_id(xml, 'TabGroup')['offset'] = "455.00,6.00"
    elem = read_xml_component('chat_name')
    add_element(xml, elem, "tabgroup")


# TODO notifications of new messages when chat is hidden via counting chat strings while chat is hidden and compare to the prev value when chat was opened

if __name__ == '__main__':
    if os.path.exists('output'):
        shutil.rmtree('output')
    
    rpfm = RPFM4Wrapper()
    
    'ui/frontend ui/sp_frame.twui.xml'
    
    edit_twui('ui/common ui/multiplayer_chat',
              lambda xml: (
                  add_callbacks_to_chat(xml),
                  remove_lock_visibility_button(xml),
                  add_chat_name(xml)
              )
              )
    edit_twui('ui/frontend ui/sp_frame',
              lambda xml: (
                  remove_obsolete_elements(xml),
                  add_chat_alert_icon_fe(xml)
              )
              )
    
    shutil.copytree('input', 'output', dirs_exist_ok=True)
    
    MOD_NAME = '!Klissan_cheat_chat'
    OUTPUT_DIR = 'output'
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
