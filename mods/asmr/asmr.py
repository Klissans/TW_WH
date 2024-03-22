import math
import os.path
import shutil

import pandas as pd
from whlib.settings import SETTINGS
from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper
from src.localizator import Localizator
from src.formatter import Formatter, _indentstr, _icon_battle

from datetime import datetime
from pprint import pprint


def _prepare_ui_effects_juncs_tables(handler:Handler):
    dst = 'unit_abilities_to_additional_ui_effects_juncs_tables'

    # data coring to remove explicit abilities' bullet points
    core_df = handler.duplicate_table(dst, new_name='data__', copy_data=True).data
    bp_to_remove = ['wh_dlc07_spell_ignores_ap', 'wh3_main_spell_redirects_projectiles', 'wh3_main_spell_melee_damage_reflection', 'wh2_dlc11_all_replenish_ammo', 'wh_main_all_replenish', 'wh_main_all_replenish_high', 'wh2_main_all_flanking', 'wh2_main_all_hiding', 'wh2_main_spell_absorb_hp', 'wh_main_all_resurrect', 'wh_dlc05_spell_trigger_when_casting', 'wh2_main_spell_friendly_fire_explosion', 'wh3_main_ability_intensity_kills', 'wh2_main_ability_range_30m']
    bp_to_remove += core_df[core_df.effect.str.contains('summon')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('magical')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('flaming')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('vortex')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('wind')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('bombardment')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('aoe')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('direct_damage')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('poor_vs')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('good_vs')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('good_against')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('strong_against')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('weak_against')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('projectile')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('armour_piercing')].effect.tolist()
    bp_to_remove += core_df[core_df.effect.str.contains('defend_vs_charge')].effect.tolist()

    bp_to_remove_set = set(bp_to_remove) - set(core_df[core_df.effect.str.contains('upgraded')].effect.tolist() + ['wh3_main_projectile_requires_line_of_sight'])
    core_df.drop(core_df[core_df.effect.isin(bp_to_remove_set)].index, inplace=True)

    src_t = handler.db['unit_abilities_tables']
    dst_t = handler.duplicate_table(dst, prefix=PREFIX)

    add_df = dst_t.data.iloc[0:0].copy()
    add_df = add_df.reindex(index=src_t.data.index)
    add_df['ability'] = src_t.data['key']
    add_df['effect'] = src_t.data['key']
    handler.append(dst_t.table_name, add_df)

    dst = 'unit_abilities_additional_ui_effects_tables'
    src_t = handler._find_mod_table(f'{PREFIX}unit_abilities_to_additional_ui_effects_juncs_tables')
    dst_t = handler.duplicate_table(dst, prefix=PREFIX)

    add_df = dst_t.data.iloc[0:0].copy()
    add_df = add_df.reindex(index=src_t.data.index)
    add_df['key'] = src_t.data['effect']
    add_df['sort_order'] = 8888
    handler.append(dst_t.table_name, add_df)


def generate_ability_phases_descs(hh, formatter):
    handler = hh.handler
    ability_phase_loc = handler.duplicate_table('special_ability_phases__', prefix=PREFIX)

    for phase_id in handler.db['special_ability_phases_tables'].data.index:
        formatted_info = formatter.get_ability_phase_desc(phase_id)
        name = 'special_ability_phases_onscreen_name_' + phase_id
        if name in ability_phase_loc.data.index:
            print('REPEATED APID: ', phase_id)
            continue
        ability_phase_loc.data.loc[name] = {'key': name, 'text': formatted_info, 'tooltip': True}

def generate_ability_descs(hh, formatter):
    handler = hh.handler
    unit_abilities_ui_loc = handler.duplicate_table('unit_abilities_additional_ui_effects__', prefix=PREFIX, copy_data=False)
    unit_abilities_loc = handler.duplicate_table('unit_abilities__', prefix=PREFIX)
    # overwrite vanilla ui bullets with empty strings
    # unit_abilities_ui_loc.data['text'] = ''
    for ability_id in handler.db['unit_abilities_tables'].data.index:
        info = hh.get_ability_info(ability_id)
        formatted_info_short = formatter.get_short_ability_desc(info, ability_id)
        formatted_info = formatter.get_ability_desc(info, ability_id)
        name = 'unit_abilities_tooltip_text_' + ability_id
        ui_name = 'unit_abilities_additional_ui_effects_localised_text_' + ability_id
        if name in unit_abilities_loc.data.index:
            print('REPEATED UAID: ', ability_id)
            continue
        unit_abilities_loc.data.loc[name] = {'key': name, 'text': formatted_info, 'tooltip': True}
        unit_abilities_ui_loc.data.loc[ui_name] = {'key': ui_name, 'text': formatted_info_short, 'tooltip': True}

    # manual fixes
    ability_mapping = {
        'wh2_dlc15_unit_passive_rubble_and_ruin_tier_1': 'wh2_dlc15_unit_passive_rubble_and_ruin_tier_1_bombardment',
        'wh2_dlc15_unit_passive_rubble_and_ruin_tier_2': 'wh2_dlc15_unit_passive_rubble_and_ruin_tier_2_bombardment',
        'wh2_dlc15_unit_passive_rubble_and_ruin_tier_3': 'wh2_dlc15_unit_passive_rubble_and_ruin_tier_3_bombardment'
    }
    for k, v in ability_mapping.items():
        unit_abilities_loc.data.loc['unit_abilities_tooltip_text_' + k, 'text'] += unit_abilities_loc.data.loc['unit_abilities_tooltip_text_' + v, 'text']
        unit_abilities_ui_loc.data.loc['unit_abilities_additional_ui_effects_localised_text_' + k, 'text'] += unit_abilities_ui_loc.data.loc['unit_abilities_additional_ui_effects_localised_text_' + v, 'text']


def generate_unit_stats(hh, formatter, is_generate_animations=True):
    handler = hh.handler

    udstt = handler.duplicate_table('unit_description_short_texts_tables', prefix=PREFIX, copy_data=False)
    udstt.data = udstt.data.reindex(index=handler.db['land_units_tables'].data.index)
    udstt.data['key'] = udstt.data.index

    udhtt = handler.duplicate_table('unit_description_historical_texts_tables', prefix=PREFIX, copy_data=False)
    udhtt.data = udhtt.data.reindex(index=handler.db['land_units_tables'].data.index)
    udhtt.data['key'] = udhtt.data.index

    lut = handler.duplicate_table('land_units_tables', prefix=PREFIX, copy_data=True)
    lut.data['short_description_text'] = lut.data.index
    lut.data['historical_description_text'] = lut.data.index

    #fix ordering
    add_df = handler.db['ui_unit_bullet_point_enums_tables'].data.iloc[:].copy()
    add_df.drop(add_df[add_df['sort_order'] >= 3].index, inplace=True)
    add_df['sort_order'] = 3

    uubpet = handler.duplicate_table('ui_unit_bullet_point_enums_tables', prefix=PREFIX, copy_data=False)
    uubpet.data = uubpet.data.reindex(index=handler.db['main_units_tables'].data.index)
    uubpet.data['key'] = handler.db['main_units_tables'].data['unit']
    uubpet.data['state'] = 'very_positive'
    uubpet.data['sort_order'] = 0
    handler.append(uubpet.table_name, add_df)

    # data coring to remove explicit unit's bullet points
    core_df = handler.duplicate_table('ui_unit_bullet_point_unit_overrides_tables', new_name='data__', copy_data=True).data
    bp_to_remove = ['aura_of_transmutation', 'attuned_to_magic', 'always_flying', 'anti_infantry', 'anti_large', 'armour_piercing', 'armour_piercing_melee', 'armour_piercing_ranged', 'armour_sundering', 'armoured', 'armoured_and_shielded','ballistics_expert', 'battle_prayers', 'barrier', 'beam_of_chotec', 'can_attack_walls', 'can_fly', 'collision_attacks','concealment_bombs', 'charmed_attacks', 'charge_reflector', 'charge_reflector_vs_large', 'cursed_ammunition','dragon_breath_noxious', 'dragon_breath_star', 'dragon_breath_sun', 'dragon_breath_moon', 'dragon_breath_hydra', 'deflect_shots', 'dodge','defender','daemon_prince', 'death_from_above', 'damage_dealer', 'death_globe', 'decent_melee', 'duellist', 'ethereal', 'evocation_of_death', 'expendable', 'frost_breath_hydra', 'fast_dwarf', 'fire_whilst_moving', 'flaming_attacks', 'frenzy', 'frostbite', 'gnoblar_traps', 'good_range', 'goblin_mangonel','hybrid', 'living_saints', 'low_rate_of_fire','mass_regeneration',  'madness_of_khaine', 'master_ambusher', 'magic_harvester', 'master_of_sacred_places', 'magical_aura', 'meat_shield', 'melee_expert', 'murderous_mastery', 'light_of_death', 'ogre_charge','old_grumblers', 'ogr_ironfist', 'primal_instincts', 'perfect_vigour', 'plagueclaw_contagion', 'poison', 'poison_wind_globes', 'poor_accuracy', 'poor_morale', 'rampage', 'ranged_attack', 'revivification_crystal', 'rebirth','regeneration', 'runic_magic', 'scaly_skin', 'shieldbreaker','shielded', 'soporific_musk', 'spellcaster', 'stalk', 'sniping', 'terror', 'torch_of_bogenhafen', 'unbreakable', 'vanguard_deployment', 'very_fast', 'warpaint', 'warpflame', 'warpfire', 'weeping_blade', 'weak_anti_armour', 'whirling_axes', 'yin', 'yang', 'zzzzap']
    bp_to_remove += ['sea_dragon_cloak', 'bigger_harder', 'armed_to_da_teef', 'guided_projectile', 'exploding_spores', 'da_great_green_wallop', 'dragon_armour', 'martial_mastery', 'bows_of_avelorn', 'lion_cloak', 'lion_pelt', 'reaver_bows', 'chameleon', 'plague_censer', 'snare_net', 'too_horrible_to_die', 'dlc17_blazing_sun_extra_cost', 'swiftshiver_shards', 'stockpiles', 'no_friendly_fire', 'multishot', 'river_troll']
    bp_to_remove += ['scaling_damage', 'wardance', 'magic_armour', 'magic_disruption'] # + ['aquatic', 'forest_spirit', 'forest_stalker', 'forest_strider', 'large_bst']
    core_df.drop(core_df[core_df.bullet_point.isin(bp_to_remove)].index, inplace=True)

    uubpuot = handler.duplicate_table('ui_unit_bullet_point_unit_overrides_tables', prefix=PREFIX, copy_data=False)
    uubpuot.data = uubpuot.data.reindex(index=handler.db['main_units_tables'].data.index)
    uubpuot.data['unit_key'] = handler.db['main_units_tables'].data['unit']
    uubpuot.data['bullet_point'] = handler.db['main_units_tables'].data['unit']

    if is_generate_animations:
        uubpet_anim = handler.duplicate_table('ui_unit_bullet_point_enums_tables', prefix=PREFIX+'ANIM_', copy_data=False)
        uubpet_anim.data = uubpet_anim.data.reindex(index=handler.db['main_units_tables'].data.index)
        uubpet_anim.data['key'] = handler.db['main_units_tables'].data['unit'] + '_anim'
        uubpet_anim.data['state'] = 'very_positive'
        uubpet_anim.data['sort_order'] = 1

        uubpuot_anim = handler.duplicate_table('ui_unit_bullet_point_unit_overrides_tables', prefix=PREFIX+'ANIM_', copy_data=False)
        uubpuot_anim.data = uubpuot_anim.data.reindex(index=handler.db['main_units_tables'].data.index)
        uubpuot_anim.data['unit_key'] = handler.db['main_units_tables'].data['unit']
        uubpuot_anim.data['bullet_point'] = handler.db['main_units_tables'].data['unit'] + '_anim'

    #data coring loc tables to remove vanilla's descriptions - doesn't work
    # tname = 'unit_description_short_texts__'
    # handler.duplicate_table(tname, new_name=tname, copy_data=False)
    # tname = 'unit_description_historical_texts__'
    # handler.duplicate_table(tname, new_name=tname, copy_data=False)

    short_text_loc = handler.duplicate_table('unit_description_short_texts__', prefix=PREFIX, copy_data=False)
    historical_text_loc = handler.duplicate_table('unit_description_historical_texts__', prefix=PREFIX, copy_data=False)
    bp_text_loc = handler.duplicate_table('ui_unit_bullet_point_enums__', prefix=PREFIX, copy_data=False)

    for unit_id in handler.db['main_units_tables'].data.index:
        info = hh.get_unit_info(unit_id)
        luid = info['land_unit']
        # if '_shp_' in luid or 'flesh_lab' in luid or 'imperial_supply' in luid or 'nakai' in luid or 'black_ark' in luid:
        #     continue
        formatted_info = formatter.get_short_unit_desc(info)
        full_formatted_info = formatter.get_full_unit_desc(info, luid)
        name = 'unit_description_short_texts_text_' + luid
        historical_name = 'unit_description_historical_texts_text_' + luid
        bp_name = 'ui_unit_bullet_point_enums_onscreen_name_' + unit_id
        bp_tooltip = 'ui_unit_bullet_point_enums_tooltip_' + unit_id

        bp_text_loc.data.loc[bp_name] = {'key': bp_name, 'text': formatter.loctr.tr('bp_unit_stats'), 'tooltip': True}
        bp_text_loc.data.loc[bp_tooltip] = {'key': bp_tooltip, 'text': full_formatted_info, 'tooltip': True}

        if is_generate_animations:
            bp_name = 'ui_unit_bullet_point_enums_onscreen_name_' + unit_id + '_anim'
            bp_tooltip = 'ui_unit_bullet_point_enums_tooltip_' + unit_id + '_anim'
            lu_info = hh.handler.get_entry_by_index('land_units_tables', luid)
            if lu_info is None:
                 raise Exception(f"Land unit is None - {unit_id}")
            animations_info = formatter.get_unit_animation(lu_info['man_animation'])

            bp_text_loc.data.loc[bp_name] = {'key': bp_name, 'text': 'Unit Animations', 'tooltip': True}
            bp_text_loc.data.loc[bp_tooltip] = {'key': bp_tooltip, 'text': animations_info, 'tooltip': True}

            mount_key = lu_info['mount']
            if not hh.handler.isnull(mount_key):
                mount_animation_key = hh.handler.get_entry_by_index('mounts_tables', mount_key)['animation']
                mount_animations_info = formatter.get_unit_animation(mount_animation_key)


                bp_key = unit_id+'_anim_mount'
                uubpet_anim.data.loc[bp_key] = {'key': bp_key, 'state': 'very_positive', 'sort_order': 2}
                uubpuot_anim.data.loc[bp_key] = {'unit_key': unit_id, 'bullet_point': bp_key}
                bp_name = 'ui_unit_bullet_point_enums_onscreen_name_' + bp_key
                bp_tooltip = 'ui_unit_bullet_point_enums_tooltip_' + bp_key
                bp_text_loc.data.loc[bp_name] = {'key': bp_name, 'text': 'Mount Animations', 'tooltip': True}
                bp_text_loc.data.loc[bp_tooltip] = {'key': bp_tooltip, 'text': mount_animations_info, 'tooltip': True}

        if name not in short_text_loc.data.index:
            short_text_loc.data.loc[name] = {'key': name, 'text': formatted_info, 'tooltip': True}
            historical_text_loc.data.loc[name] = {'key': historical_name, 'text': full_formatted_info, 'tooltip': True}
        else:
            # print('REPEATED LUID: ', luid)
            pass



def modify_spell_icons(handler):
    import cv2

    def add_mana_cost_to_image(img, manacost, is_upgrade=False):
        text = str(int(manacost))

        font = cv2.FONT_HERSHEY_PLAIN
        fontScale = 1.5
        fontColor = (0, 0, 0, 255)
        thickness = 3
        lineType = 1

        w_offset = 15
        if is_upgrade:
            w_offset *= -1

        text_width, text_height = cv2.getTextSize(text, font, fontScale, lineType)[0]
        cc_w = int(img.shape[1] / 2) - int(text_width / 2) - w_offset
        cc_h = int(img.shape[0] / 2) + int(text_height / 2)

        cv2.putText(img, text,
                    (cc_w, cc_h),
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

        fontColor = (255, 255, 255, 255)
        thickness = 1

        cv2.putText(img, text,
                    (cc_w, cc_h),
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)


    uat_df = handler.db['unit_abilities_tables'].data
    usat_df = handler.db['unit_special_abilities_tables'].data

    rel_path = os.path.join('ui', 'battle ui', 'ability_icons')
    input_path = os.path.join('input', rel_path)
    output_path = os.path.join('output', rel_path)
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join('output', 'ui', 'skins', 'default'), exist_ok=True)
    shutil.copy(os.path.join('input', 'ui', 'skins', 'default', 'icon_invalid.png'), os.path.join('output', 'ui', 'skins', 'default', 'icon_invalid.png'))
    shutil.copy(os.path.join('input', rel_path, 'cant_target_flying.png'), os.path.join('output', rel_path, 'cant_target_flying.png'))

    filter = (usat_df['mana_cost'] > 0) & ~usat_df['key'].str.contains('_upgraded') & ~usat_df['key'].str.contains('_branchwraith') & ~usat_df['key'].str.contains('_kihar')
    for key, row in usat_df[filter].iterrows():
        img_name = uat_df.loc[key, 'icon_name']
        img_path = os.path.join(input_path, img_name + '.png')

        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            # rpfm.extract_file('data', os.path.join(rel_path, img_name + '.png'), 'input')
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

        add_mana_cost_to_image(img, row['mana_cost'])

        key_upgraded = key + '_upgraded'
        if key_upgraded in usat_df.index:
            add_mana_cost_to_image(img, usat_df.loc[key_upgraded, 'mana_cost'], is_upgrade=True)

        img_path = os.path.join(output_path, img_name + '.png')
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite(img_path, img)
    pass


def modify_campaign_tooltips(hh, formatter):
    from src.formatter import _icon
    roundf = lambda x: round(float(x))
    endl = formatter.endl
    icon = formatter.icon
    highlight = formatter.highlight
    handler = hh.handler
    loctr = formatter.loctr
    rules_df = handler.db['_kv_rules_tables'].data
    morale_df = handler.db['_kv_morale_tables'].data
    rsl_orig_df = handler.locs['random_localisation_strings__'].data
    tname = 'random_localisation_strings__'
    rls_df = handler.get_mod_table(tname, PREFIX + tname).data

    colorize_ai = lambda x, colour: formatter.colorize('+' + str(x) + '%', colour) if x > 0 else formatter.colorize(str(x)+'%', colour)
    colorize_ai_ml = lambda x, colour: formatter.colorize('+' + str(x) , colour) if x > 0 else formatter.colorize(str(x), colour)
    colorize_pl_ml = lambda x, colour: formatter.colorize( str(x), colour) if x < 0 else formatter.colorize('+' +str(x), colour)


    difficulties = ['easy', '', 'hard', 'very_hard']
    colours = ['fresh', 'active', 'tired', 'very_tired']
    for level in range(1, 5):
        if level == 2:
            continue
        c = 'fatigue_' + colours[level-1]
        key = f'random_localisation_strings_string_difficulty_level_{level}_description_battle'
        rls_df.loc[key] = rsl_orig_df.loc[key]
        ma = round((float(rules_df.loc[f'difficulty_mod_ai_{difficulties[level-1]}_melee_attack', 'value']) - 1) * 100)
        md = round((float(rules_df.loc[f'difficulty_mod_ai_{difficulties[level-1]}_melee_defence', 'value']) - 1) * 100)
        mdmg = round((float(rules_df.loc[f'difficulty_mod_ai_{difficulties[level-1]}_melee_damage', 'value']) - 1) * 100)
        cb = round((float(rules_df.loc[f'difficulty_mod_ai_{difficulties[level-1]}_charge_bonus', 'value']) - 1) * 100)
        rs = round(float(rules_df.loc[f'difficulty_mod_ai_{difficulties[level-1]}_missile_reload_additional', 'value']))
        morale_ai = round(float(morale_df.loc[f'difficulty_modifier_ai_{difficulties[level-1]}', 'value']))
        morale_pl = round(float(morale_df.loc[f'difficulty_modifier_player_{difficulties[level-1]}', 'value']))
        rls_df.loc[key, 'text'] = ''
        rls_df.loc[key, 'text'] += f"{endl}{_icon('icon_ai')}: {icon['stat_melee_attack']}{colorize_ai(ma, c)} {icon['stat_melee_defence']}{colorize_ai(md, c)} {icon['stat_melee_damage_base']}{icon['stat_melee_damage_ap']}{colorize_ai(mdmg, c)} {icon['stat_charge_bonus']}{colorize_ai(cb, c)} {icon['stat_reloading']}{colorize_ai(rs, c)} {icon['stat_morale']}{colorize_ai_ml(morale_ai, c)}"
        rls_df.loc[key, 'text'] += f"{endl}{_icon('icon_player')}: {icon['stat_morale']}{colorize_pl_ml(morale_pl,c)}"



def modify_unit_tooltip(hh, formatter):
    from src.formatter import _icon
    roundf = lambda x, r=None: round(float(x), r)
    endl = formatter.endl
    icon = formatter.icon
    highlight = formatter.highlight
    handler = hh.handler
    loctr = formatter.loctr
    rules_df = handler.db['_kv_rules_tables'].data
    morale_df = handler.db['_kv_morale_tables'].data
    kv_unit_df = handler.db['_kv_unit_ability_scaling_rules_tables'].data
    bscslt_df = handler.db['battle_secondary_currency_sources_links_tables'].data
    bcasacv_df = handler.db['battle_currency_army_special_abilities_cost_values_tables'].data
    usl_orig_df = handler.locs['unit_stat_localisations__'].data
    usl_df = handler.duplicate_table('unit_stat_localisations__', prefix=PREFIX, copy_data=False).data
    dabd_orig_df = handler.locs['daemon_ability_bar_descriptions__'].data
    dabd_df = handler.duplicate_table('daemon_ability_bar_descriptions__', prefix=PREFIX, copy_data=False).data
    uied_orig_df = handler.locs['uied_component_texts__'].data
    uied_df = handler.duplicate_table('uied_component_texts__', prefix=PREFIX, copy_data=False).data
    rsl_orig_df = handler.locs['random_localisation_strings__'].data
    rls_df = handler.duplicate_table('random_localisation_strings__', prefix=PREFIX, copy_data=False).data

    uab_df = handler._find_mod_table(PREFIX+'unit_abilities__').data
    uaaue_df = handler._find_mod_table(PREFIX+'unit_abilities_additional_ui_effects__').data


    #Experience
    uebt_orig_df = handler.db['unit_experience_bonuses_tables'].data
    uett_orig_df = handler.db['unit_experience_thresholds_tables'].data

    key = 'random_localisation_strings_string_increase_experience'
    rls_df.loc[key] = rsl_orig_df.loc[key]
    text = ''
    prev_exp = 0
    for i in range(1, 10):
        exp_th = uett_orig_df.loc[f'land_level_0{i}', 'value']
        exp_required = exp_th - prev_exp
        prev_exp = exp_th
        morale = round( i * float(uebt_orig_df.loc['stat_morale', 'growth_scalar']))
        accuracy = round( i * float(uebt_orig_df.loc['stat_accuracy', 'growth_scalar']))
        reload = round( i * float(uebt_orig_df.loc['stat_reloading', 'growth_scalar']))
        text += f"{_icon(f'experience_{i}')}{exp_required:4d} {icon['stat_morale']}{morale:2d} {icon['stat_accuracy']}{accuracy:2d} {icon['stat_reloading']}{reload:2d}{endl}"
    tr_value = loctr.add_auto('chunks', key+'_table', auto_formatter=text)
    text = f"Increase experience {icon['mp_cost']}"
    tr_value += loctr.add_auto('chunks', key, auto_formatter=text)
    rls_df.loc[key, 'text'] = loctr.add_auto('overrides', key, auto_formatter=tr_value)

    #BARRIER
    key = 'random_localisation_strings_string_barrier_description'

    tr_value = loctr.add_auto('value', 'barrier_replenishment_delay', auto_formatter=highlight(roundf(rules_df.loc['barrier_replenishment_delay', 'value'])))
    text = f"{endl}{loctr.add_auto('chunks', rules_df.loc['barrier_replenishment_delay', 'key'])}: {tr_value}"

    tr_value = loctr.add_auto('value', 'barrier_replenishment_rate', auto_formatter=highlight(roundf(rules_df.loc['barrier_replenishment_rate', 'value'])))
    text += f"{endl}{loctr.add_auto('chunks', rules_df.loc['barrier_replenishment_rate', 'key'])}: {tr_value}"

    rls_df.loc[key] = rsl_orig_df.loc[key]
    rls_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    #STATS
    key = 'unit_stat_localisations_tooltip_text_stat_armour'
    tr_value = loctr.add_auto('value', 'armour_roll_lower_cap', auto_formatter=str(roundf(rules_df.loc['armour_roll_lower_cap', 'value'], 2)))
    tr_text = f"||Blocks a random % in range [{tr_value}*armour, armour] (max 100%) of incoming:{endl}"
    text = loctr.add_auto('chunks', 'stat_armour_0', auto_formatter=tr_text)
    k, v = usl_orig_df.loc['unit_stat_localisations_onscreen_name_stat_melee_damage_base', 'key'], usl_orig_df.loc['unit_stat_localisations_onscreen_name_stat_melee_damage_base', 'text']
    text += f"{loctr.add_auto('chunks', k, auto_formatter=v)}{endl}"
    k, v = usl_orig_df.loc['unit_stat_localisations_onscreen_name_scalar_missile_damage_base', 'key'], usl_orig_df.loc['unit_stat_localisations_onscreen_name_scalar_missile_damage_base', 'text']
    text += f"{loctr.add_auto('chunks', k, auto_formatter=v)}{endl}"
    k, v = usl_orig_df.loc['unit_stat_localisations_onscreen_name_scalar_missile_explosion_damage_base', 'key'], usl_orig_df.loc['unit_stat_localisations_onscreen_name_scalar_missile_explosion_damage_base', 'text']
    text += f"{loctr.add_auto('chunks', k, auto_formatter=v)}{endl}"

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_stat_localisations_tooltip_text_stat_morale'
    tr_text = f"||Leadership Modifiers:{endl}"
    text = loctr.add_auto('chunks', 'stat_morale_title', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'general_aura_radius', auto_formatter=highlight(roundf(morale_df.loc['general_aura_radius', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'general_inspire_effect_amount_max', auto_formatter=formatter.colorize(roundf(morale_df.loc['general_inspire_effect_amount_max', 'value']), 'green'))
    tr_text = f"Lord's aura ({tr_value_0}m radius): {tr_value_1}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_lord', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'routing_unit_effect_distance_front', auto_formatter=formatter.highlight(roundf(morale_df.loc['routing_unit_effect_distance_front', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'routing_unit_effect_distance_flank', auto_formatter=formatter.highlight(roundf(morale_df.loc['routing_unit_effect_distance_flank', 'value'])))
    tr_text = f"Routing effects (distance from front/flank: {tr_value_0}/{tr_value_1}):{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_routing', auto_formatter=tr_text)

    enemies_rout = '/'.join([loctr.add_auto('value', f'routing_enemies_effect_weighting_{i}', auto_formatter=formatter.colorize(math.ceil(i * float(morale_df.loc['routing_enemies_effect_weighting', 'value'])), 'green')) for i in range(1, roundf(morale_df.loc['max_routing_enemies_to_consider', 'value']) + 1)])
    tr_text = f"{_indentstr(formatter.indent_step)}Enemies: {enemies_rout}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_routing_enemies', auto_formatter=tr_text)

    friends_rout = '/'.join([loctr.add_auto('value', f'routing_friends_effect_weighting_{i}', auto_formatter=formatter.colorize(math.ceil(i * float(morale_df.loc['routing_friends_effect_weighting', 'value'])), 'green')) for i in range(1, roundf(morale_df.loc['max_routing_friends_to_consider', 'value']) + 1)])
    tr_text = f"{_indentstr(formatter.indent_step)}Friends: {friends_rout}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_routing_friends', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'winning_combat_slightly', auto_formatter=formatter.colorize(roundf(morale_df.loc['winning_combat_slightly', 'value']), 'green'))
    tr_value_1 = loctr.add_auto('value', 'winning_combat', auto_formatter=formatter.colorize(roundf(morale_df.loc['winning_combat', 'value']), 'green'))
    tr_value_2 = loctr.add_auto('value', 'winning_combat_significantly', auto_formatter=formatter.colorize(roundf(morale_df.loc['winning_combat_significantly', 'value']), 'green'))
    tr_text = f"Winning combat (slightly/confidently/significantly): {tr_value_0}/{tr_value_1}/{tr_value_2}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_winning', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'losing_combat', auto_formatter=formatter.colorize(roundf(morale_df.loc['losing_combat', 'value']), 'red'))
    tr_value_1 = loctr.add_auto('value', 'losing_combat_significantly', auto_formatter=formatter.colorize(roundf(morale_df.loc['losing_combat_significantly', 'value']), 'red'))
    tr_text = f"Losing combat (confidently/significantly): {tr_value_0}/{tr_value_1}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_losing', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'was_attacked_in_front', auto_formatter=formatter.colorize(roundf(morale_df.loc['was_attacked_in_front', 'value']), 'red'))
    tr_value_1 = loctr.add_auto('value', 'was_attacked_in_flank', auto_formatter=formatter.colorize(roundf(morale_df.loc['was_attacked_in_flank', 'value']), 'red'))
    tr_value_2 = loctr.add_auto('value', 'was_attacked_in_rear', auto_formatter=formatter.colorize(roundf(morale_df.loc['was_attacked_in_rear', 'value']), 'red'))
    tr_text = f"Was attacked in (front/flank/rear){highlight('*')}: {tr_value_0}/{tr_value_1}/{tr_value_2}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_attacked_in', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'enemy_morale_penalty_value_min', auto_formatter=formatter.colorize(roundf(morale_df.loc['was_attacked_in_front', 'value']), 'red'))
    tr_value_1 = loctr.add_auto('value', 'enemy_morale_penalty_value_max', auto_formatter=formatter.colorize(roundf(morale_df.loc['enemy_morale_penalty_value_max', 'value']), 'red'))
    tr_text = f"Faster and stronger enemies nearby: min {tr_value_0} max {tr_value_1}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_faster', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'ume_concerned_general_fled_recently', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_general_fled_recently', 'value']), 'red'))
    tr_value_1 = loctr.add_auto('value', 'ume_concerned_general_dead', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_general_dead', 'value']), 'red'))
    tr_value_2 = loctr.add_auto('value', 'ume_concerned_general_died_recently', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_general_died_recently', 'value']), 'red'))
    tr_text = f"General fled recently/died(recently): {tr_value_0}/{tr_value_1}({tr_value_2}){endl}"
    text += loctr.add_auto('chunks', 'stat_morale_fled', auto_formatter=tr_text)

    tr_text = f"Melee Contact: ???{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_contact', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'open_flanks_effect_range', auto_formatter=highlight(roundf(morale_df.loc['open_flanks_effect_range', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'ume_encouraged_on_the_hill', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_encouraged_on_the_hill', 'value']), 'green'))
    tr_value_2 = loctr.add_auto('value', 'ume_encouraged_flanks_secure', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_encouraged_flanks_secure', 'value']), 'green'))
    tr_value_3 = loctr.add_auto('value', 'ume_concerned_flanks_exposed_single', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_flanks_exposed_single', 'value']), 'red'))
    tr_value_4 = loctr.add_auto('value', 'ume_concerned_flanks_exposed_multiple', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_flanks_exposed_multiple', 'value']), 'red'))
    tr_text = f"Flanks ({tr_value_0}m range) high ground/secure/exposed 1/exposed 2: {tr_value_1}/{tr_value_2}/{tr_value_3}/{tr_value_4}{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_flanks', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'recent_casualties_time_', auto_formatter=highlight(4))
    tr_text = f"Recent casualties ({tr_value_0}s) @ {icon['hp']}% loss:{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_recent', auto_formatter=tr_text)

    strs = []
    values = morale_df[morale_df['key'].str.contains('recent_casualties_penalty_')]
    for i, e in enumerate(values.sort_values(by='key', key=lambda k: k.str.split('_').str[-1].astype(int)).iterrows()):
        tr_value = loctr.add_auto('value', f'recent_casualties_penalty_value_{i}', auto_formatter=formatter.colorize(roundf(e[1]['value']), 'red'))
        tr_key_value = loctr.add_auto('value', f'recent_casualties_penalty_key_{i}', auto_formatter=highlight(e[1]['key'].split('_')[-1]))
        strs.append(f"{tr_value}:{tr_key_value}")
    tr_text = '|'.join(strs) + f'{endl}'
    text += loctr.add_auto('chunks', 'stat_morale_recent_0', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'extended_casualties_time_', auto_formatter=highlight(60))
    tr_text = f"Extended casualties ({tr_value_0}s) @ {icon['hp']}% loss:{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_extended', auto_formatter=tr_text)

    strs = []
    values = morale_df[morale_df['key'].str.contains('extended_casualties_penalty_')]
    for i, e in enumerate(values.sort_values(by='key', key=lambda k: k.str.split('_').str[-1].astype(int)).iterrows()):
        tr_value = loctr.add_auto('value', f'extended_casualties_penalty_value_{i}', auto_formatter=formatter.colorize(roundf(e[1]['value']), 'red'))
        tr_key_value = loctr.add_auto('value', f'extended_casualties_penalty_key_{i}', auto_formatter=highlight(e[1]['key'].split('_')[-1]))
        strs.append(f"{tr_value}:{tr_key_value}")
    tr_text = '|'.join(strs) + f'{endl}'
    text += loctr.add_auto('chunks', 'stat_morale_extended_0', auto_formatter=tr_text)

    tr_text = f"Total casualties @ {icon['hp']}% loss:{endl}"
    text += loctr.add_auto('chunks', 'stat_morale_total', auto_formatter=tr_text)

    strs = []
    values = morale_df[morale_df['key'].str.contains('total_casualties_penalty_')]
    for i, e in enumerate(values.sort_values(by='key', key=lambda k: k.str.split('_').str[-1].astype(int)).iterrows()):
        tr_value = loctr.add_auto('value', f'total_casualties_penalty_value_{i}', auto_formatter=formatter.colorize(roundf(e[1]['value']), 'red'))
        tr_key_value = loctr.add_auto('value', f'total_casualties_penalty_key_{i}', auto_formatter=highlight(e[1]['key'].split('_')[-1]))
        strs.append(f"{tr_value}:{tr_key_value}")
    tr_text = '|'.join(strs) + f'{endl}'
    text += loctr.add_auto('chunks', 'stat_morale_total_0', auto_formatter=tr_text)

    tr_text = f"||{highlight('*')}Submodifiers do stack"
    text += loctr.add_auto('chunks', 'stat_morale_submods', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_scalar_speed'
    tr_value_0 = loctr.add_auto('value', 'collision_damage_normaliser', auto_formatter=highlight(rules_df.loc['collision_damage_normaliser', 'value']))
    tr_value_1 = loctr.add_auto('value', 'collision_damage_modifier', auto_formatter=highlight(rules_df.loc['collision_damage_modifier', 'value']))
    collision_power_f = f"({icon['entity_large']}{icon['scalar_speed']}+{icon['entity_small']}{icon['scalar_speed']}) * {icon['entity_large']}{icon['mass']}/{icon['entity_small']}{icon['mass']}"
    tr_text = f"||{icon['entity_large']}Large entity deals {highlight('Collision Damage')} when collides with {icon['entity_small']}small entity using formula:{endl}" \
                               f"({loctr.add_auto('chunks', 'collision_power_f', auto_formatter=collision_power_f)})^{tr_value_0} * {tr_value_1}{endl}"\
                               f"Don't confuse {highlight('Collision Damage')} with {highlight('Collision Attack')}. They are different concepts.{endl}"
    text = loctr.add_auto('chunks', 'scalar_speed_0', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'bracing_calibration_ranks_multiplier', auto_formatter=highlight(roundf(rules_df.loc['bracing_calibration_ranks_multiplier', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'bracing_calibration_ranks', auto_formatter=highlight(roundf(rules_df.loc['bracing_calibration_ranks', 'value'])))
    tr_text = f"||When infantry is standing still and facing the enemy, they will get a {icon['scalar_bracing']}{highlight('Bracing')} multiplier to their {icon['mass']}mass.{endl}"\
                f"Max bracing multiplier is {tr_value_0} for being in a full {tr_value_1} ranks deep formation."
    text += loctr.add_auto('chunks', 'scalar_speed_1', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'collision_damage_maximum', auto_formatter=highlight(roundf(rules_df.loc['collision_damage_maximum', 'value'])))
    tr_text = f"{endl}Collision Damage Maximum: {tr_value_0}"
    text += loctr.add_auto('chunks', 'scalar_speed_cd_max', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_stat_melee_attack'
    tr_value_0 = loctr.add_auto('value', 'melee_hit_chance_base', auto_formatter=highlight(roundf(rules_df.loc['melee_hit_chance_base', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'melee_hit_chance_min', auto_formatter=highlight(roundf(rules_df.loc['melee_hit_chance_min', 'value'])))
    tr_value_2 = loctr.add_auto('value', 'melee_hit_chance_max', auto_formatter=highlight(roundf(rules_df.loc['melee_hit_chance_max', 'value'])))
    tr_text = f"||Melee Hit Chance Base: {tr_value_0}%{endl}" \
                f"Melee Hit Chance Min: {tr_value_1}%{endl}" \
                f"Melee Hit Chance Max: {tr_value_2}%"
    text = loctr.add_auto('chunks', 'stat_melee_attack_chances', auto_formatter=tr_text)

    tr_text = f"{endl}||{highlight(loctr.tr('weapon_length'))} - relevant for pikes, cav refusal distances and close proximity. The latter picks between this and 1m + entity radius, whatever is longer, to determine weapon 'reach'. Chariot riders use this to check if enemies are within reach."
    text += loctr.add_auto('chunks', 'stat_melee_attack_weapon_length', auto_formatter=tr_text)

    tr_text = f"{endl}{highlight(loctr.tr('attack_interval'))} - min interval between the start of each attack animation."
    text += loctr.add_auto('chunks', 'stat_melee_attack_interval', auto_formatter=tr_text)

    tr_text = f"{endl}{formatter.icon['splash_attack']}{highlight(loctr.tr('splash_attack'))} - TODO"
    text += loctr.add_auto('chunks', 'stat_melee_splash_attack', auto_formatter=tr_text)

    tr_text = f"{endl}{highlight(loctr.tr('splash_target_size'))} - do splash attacks when fighting up to this size."
    text += loctr.add_auto('chunks', 'stat_melee_splash_target_size', auto_formatter=tr_text)

    tr_text = f"{endl}{highlight(loctr.tr('splash_max_attacks'))} - max entities to attack per splash attack animation. Weapon Damage is splitted equally among all selected targets in the AOE. Note that 'High Threat/Priority' targets ({formatter.icon['high_threat']}[mod]) always get treated focused damage."
    text += loctr.add_auto('chunks', 'stat_melee_splash_max_attacks', auto_formatter=tr_text)

    tr_text = f"{endl}{highlight(loctr.tr('splash_power_multiplier'))} - multiplier to knock power in splash attack metadata."
    text += loctr.add_auto('chunks', 'stat_melee_splash_power_multiplier', auto_formatter=tr_text)

    tr_text = f"{endl}||{formatter.icon['collision_attack']}{highlight(loctr.tr('collision_attack'))} - TODO"
    text += loctr.add_auto('chunks', 'stat_melee_collision_attack', auto_formatter=tr_text)

    tr_text = f"{endl}{highlight(loctr.tr('collision_max_targets'))} - max targets damaged by collision attack. This cap is refreshed by 'Refreshes'."
    text += loctr.add_auto('chunks', 'stat_melee_collision_max_targets', auto_formatter=tr_text)

    tr_text = f"{endl}{highlight(loctr.tr('collision_refreshes'))} - each second, this amount of targets will be removed from the max targets list, enabling the collision attacker to deal more attacks."
    text += loctr.add_auto('chunks', 'stat_melee_collision_refreshes', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_stat_melee_defence'
    tr_value_0 = loctr.add_auto('value', 'melee_defence_direction_penalty_coefficient_flank', auto_formatter=formatter.colorize(roundf(100*(rules_df.loc['melee_defence_direction_penalty_coefficient_flank', 'value']-1)), 'red'))
    tr_value_1 = loctr.add_auto('value', 'melee_defence_direction_penalty_coefficient_rear', auto_formatter=formatter.colorize(roundf(100*(rules_df.loc['melee_defence_direction_penalty_coefficient_rear', 'value']-1)), 'red'))
    tr_text = f"||Attacked from the flank penalty: {tr_value_0}%{endl}" \
               f"Attacked from the rear penalty: {tr_value_1}%"
    text = loctr.add_auto('chunks', 'stat_melee_defence_penalties', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_stat_weapon_damage'
    tr_value_0 = loctr.add_auto('value', 'melee_height_damage_modifier_max_coefficient', auto_formatter=formatter.highlight(roundf(100*rules_df.loc['melee_height_damage_modifier_max_coefficient', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'melee_height_damage_modifier_max_difference', auto_formatter=highlight(roundf(rules_df.loc['melee_height_damage_modifier_max_difference', 'value'])))
    tr_text = f"{endl}||Height modifier max bonus: +/-{tr_value_0}%{endl}" \
            f"Max height modifier difference: +/-{tr_value_1}m"
    text = loctr.add_auto('chunks', 'stat_weapon_damage_height', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_stat_charge_bonus'
    tr_value_0 = loctr.add_auto('value', 'charge_decay_duration', auto_formatter=highlight(roundf(rules_df.loc['charge_decay_duration', 'value'])))
    tr_text = f"||The charge bonus coefficient linearly declines from 1 to 0 over {tr_value_0}s after unit started charging{endl}" \
                               f"Charge bonus modifiers will have effect until the coefficient reaches 0."
    text = loctr.add_auto('chunks', 'stat_charge_bonus_0', auto_formatter=tr_text)
    tr_value_1 = loctr.add_auto('value', 'charge_bonus', auto_formatter=formatter.colorize('+'+str(roundf(morale_df.loc['charge_bonus', 'value'])), 'green'))
    tr_text = f"{endl}{tr_value_1}{icon['stat_morale']} while charging."
    text += loctr.add_auto('chunks', 'stat_charge_bonus_1', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'pursuit_charge_bonus_modifier', auto_formatter=highlight(roundf(rules_df.loc['pursuit_charge_bonus_modifier', 'value'], 1)))
    tr_text = f"{endl}Pursuit Bonus: {tr_value_0}"
    text += loctr.add_auto('chunks', 'stat_charge_bonus_pursuit', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_stat_ammo'
    tr_text = f"||{usl_orig_df.loc['unit_stat_localisations_onscreen_name_stat_reloading', 'text']} is a percentage reduction of projectile base reload time:{endl}" \
                               f"Actual Reload Time = (100 - Reload Skill)% * Base Reload Time"
    text = loctr.add_auto('chunks', 'stat_ammo_reload', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'ume_concerned_attacked_by_projectile', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_attacked_by_projectile', 'value']), 'red'))
    tr_value_1 = loctr.add_auto('value', 'artillery_near_miss_distance_squared', auto_formatter=highlight(roundf(math.sqrt(morale_df.loc['artillery_near_miss_distance_squared', 'value']))))
    tr_value_2 = loctr.add_auto('value', 'ume_concerned_damaged_by_artillery', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_damaged_by_artillery', 'value']), 'red'))
    tr_value_3 = loctr.add_auto('value', 'ume_concerned_attacked_by_artillery', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_attacked_by_artillery', 'value']), 'red'))
    tr_text = f"{endl}Under missile fire: {icon['stat_morale']}{tr_value_0}" \
              f"{endl}Damaged by artillery (near miss {tr_value_1}m radius): {icon['stat_morale']}{tr_value_2} ({tr_value_3})"
    text += loctr.add_auto('chunks', 'stat_ammo_morale', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['ignores_shields']}[mod] - ignores shields."
    text += loctr.add_auto('chunks', 'stat_ammo_shield', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['self_guided']}[mod] - self-guided."
    text += loctr.add_auto('chunks', 'stat_ammo_guided', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['no_friendly_fire']}[mod] - no friendly fire."
    text += loctr.add_auto('chunks', 'stat_ammo_ff', auto_formatter=tr_text)

    tr_text = f"{endl}{_icon_battle('cant_target_flying')}[mod] - can't target flying unit."
    text += loctr.add_auto('chunks', 'stat_ammo_target_flying', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_scalar_missile_range'

    tr_text = f"||{endl}{icon['stat_accuracy']}{highlight(loctr.tr('projectile_spread'))} - TODO."
    text = loctr.add_auto('chunks', 'stat_missile_spread', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['stat_accuracy']}{highlight(loctr.tr('total_accuracy'))} - a sum of unit's accuracy and projectile's marksmanship bonus."
    text += loctr.add_auto('chunks', 'stat_missile_total_accuracy', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['stat_accuracy']}{highlight('Accuracy')} - accuracy inherent to unit. Reduces size of calibration area together with a projectile's marksmanship bonus."
    text += loctr.add_auto('chunks', 'stat_missile_unit_accuracy', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['stat_accuracy']}{highlight('Marksmanship Bonus')} - bonus to accuracy inherent to projectile. Reduces size of calibration area together with a unit's accuracy."
    text += loctr.add_auto('chunks', 'stat_missile_projectile_mm_bonus', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['stat_accuracy']}{highlight('Calibration Distance')} - the distance from the unit to the center of the calibration area at which the calibration area is at 100%."
    text += loctr.add_auto('chunks', 'stat_missile_projectile_cal_distance', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['stat_accuracy']}{highlight('Calibration Area')} - the area within which the projectile can land when fired. Scales according to actual distance and is reduced further by total accuracy."
    text += loctr.add_auto('chunks', 'stat_missile_projectile_cal_area', auto_formatter=tr_text)

    tr_text = f"{endl}{icon['distance']}{highlight(loctr.tr('effective_range'))} - max distance the unit can shoot at."
    text += loctr.add_auto('chunks', 'stat_missile_projectile_effective_range', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    key = 'unit_stat_localisations_tooltip_text_stat_missile_strength'
    tr_value_0 = loctr.add_auto('value', 'missile_height_damage_modifier_max_coefficient', auto_formatter=highlight(roundf(100*rules_df.loc['missile_height_damage_modifier_max_coefficient', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'missile_height_damage_modifier_max_difference', auto_formatter=highlight(roundf(rules_df.loc['missile_height_damage_modifier_max_difference', 'value'])))
    tr_text = f"{endl}||Height modifier max bonus: +/-{tr_value_0}%{endl}" \
                    f"Max height modifier difference: +/-{tr_value_1}m"
    text = loctr.add_auto('chunks', 'stat_missile_strength_height', auto_formatter=tr_text)

    s = highlight("Projectile's Shockwave Radius")
    tr_text = f"{endl}{icon['distance']}{s} - the radius of the projectile where it deals full damage. All projectiles are affected by {icon['stat_resistance_missile']}"
    text += loctr.add_auto('chunks', 'stat_missile_shockwave', auto_formatter=tr_text)

    tr_text = f"{endl}{highlight('Penetration')} - how good the projectile at penetrating entities (see the mod's description on Steam for more info)."
    text += loctr.add_auto('chunks', 'stat_missile_penetration', auto_formatter=tr_text)

    s = highlight("Explosion's Detonation Radius")
    tr_text = f"{endl}{icon['distance']}{s} - the radius from the center of the projectile where explosion deals full damage. Resisted by {icon['stat_resistance_missile']}"
    text += loctr.add_auto('chunks', 'stat_missile_detonation', auto_formatter=tr_text)

    usl_df.loc[key] = usl_orig_df.loc[key]
    usl_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    # ATTRIBUTES
    ua_orig_df = handler.locs['unit_attributes__'].data
    ua_df = handler.duplicate_table('unit_attributes__', prefix=PREFIX, copy_data=False).data

    key = 'unit_attributes_bullet_text_causes_fear'
    tr_value_0 = loctr.add_auto('value', 'ume_concerned_unit_frightened', auto_formatter=formatter.colorize(roundf(morale_df.loc['ume_concerned_unit_frightened', 'value']), 'red'))
    tr_value_1 = loctr.add_auto('value', 'fear_effect_range', auto_formatter=highlight(roundf(morale_df.loc['fear_effect_range', 'value'])))
    tr_text = f"||{tr_value_0}{icon['stat_morale']} in {tr_value_1}m radius"
    text = loctr.add_auto('chunks', 'attr_causes_fear', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_causes_terror'
    tr_value_0 = loctr.add_auto('value', 'morale_shock_terror_morale_threshold_long', auto_formatter=highlight(roundf(morale_df.loc['morale_shock_terror_morale_threshold_long', 'value'])))
    tr_value_1 = loctr.add_auto('value', 'terror_effect_range', auto_formatter=highlight(roundf(morale_df.loc['terror_effect_range', 'value'])))
    tr_value_2 = loctr.add_auto('value', 'morale_shock_rout_timer_long', auto_formatter=highlight(roundf(morale_df.loc['morale_shock_rout_timer_long', 'value'])))
    tr_value_3 = loctr.add_auto('value', 'morale_shock_rout_immunity_timer', auto_formatter=highlight(roundf(morale_df.loc['morale_shock_rout_immunity_timer', 'value'])))
    tr_text = f"||Terror-routs units with {usl_orig_df.loc['unit_stat_localisations_onscreen_name_stat_morale', 'text']} < {tr_value_0} in {tr_value_1}m radius for {tr_value_2}s{endl}" \
                              f"Immune to terror-rout for {tr_value_3}s after being terror-routed"
    text = loctr.add_auto('chunks', 'attr_causes_terror', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_charge_reflection'
    tr_value_0 = loctr.add_auto('value', 'bracing_charge_reflector_bonus', auto_formatter=highlight(roundf(rules_df.loc['bracing_charge_reflector_bonus', 'value'])))
    tr_text = f"||Bracing Charge Reflector Bonus: {tr_value_0}"
    text = loctr.add_auto('chunks', 'attr_charge_reflection', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_ogre_charge'
    tr_value_0 = loctr.add_auto('value', 'ogre_charge_factor', auto_formatter=highlight(roundf(rules_df.loc['ogre_charge_factor', 'value'])))
    tr_text = f"||Ogre Charge Factor: {tr_value_0}"
    text = loctr.add_auto('chunks', 'attr_ogre_charge', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_devastating_flanker'
    tr_value_0 = loctr.add_auto('value', 'devastating_flanker_charge_multiplier', auto_formatter=highlight(roundf(rules_df.loc['devastating_flanker_charge_multiplier', 'value'])))
    tr_text = f"||Devastating Flanker Charge Multiplier: {tr_value_0}"
    text = loctr.add_auto('chunks', 'attr_devastating_flanker', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_spell_mastery'
    tr_value_0 = loctr.add_auto('value', 'spell_mastery_per_unit_modifier', auto_formatter=formatter.colorize(f"+{roundf(rules_df.loc['spell_mastery_per_unit_modifier', 'value']*100)}", 'green'))
    tr_value_1 = loctr.add_auto('value', 'spell_mastery_max_modifier', auto_formatter=formatter.colorize(f"+{roundf((rules_df.loc['spell_mastery_max_modifier', 'value']-1)*100)}", 'green'))
    tr_text = f"||Each unit increases {highlight('Power Intensity')} by {tr_value_0}% up to {tr_value_1}%"
    text = loctr.add_auto('chunks', 'attr_spell_mastery', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_hide_forest'
    tr_value_0 = loctr.add_auto('value', 'attr_hide_forest', auto_formatter=highlight(80))
    tr_text = f"||Default Hidden Unit Reveal Distance (Forest): {tr_value_0}"
    text = loctr.add_auto('chunks', 'attr_hide_forest', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_stalk'
    tr_value_0 = loctr.add_auto('value', 'attr_stalk', auto_formatter=highlight(60))
    tr_text = f"||Default Stalk Unit Reveal Distance (Scrub): {tr_value_0}"
    text = loctr.add_auto('chunks', 'attr_stalk', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'unit_attributes_bullet_text_unspottable'
    tr_value_0 = loctr.add_auto('value', 'unspottable_unit_reveal_distance', auto_formatter=highlight(roundf(rules_df.loc['unspottable_unit_reveal_distance', 'value'])))
    tr_text = f"||Unspottable Unit Reveal Distance: {tr_value_0}"
    text = loctr.add_auto('chunks', 'attr_unspottable', auto_formatter=tr_text)
    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    def army_ability_format(key, source_type, source_to_currency_rate, ability_names):
        tr_st = loctr.add_auto('currency_source_type', source_type)
        tr_value_0 = loctr.add_auto('value', key+'_source_to_currency_rate', auto_formatter=highlight(source_to_currency_rate))
        tr_value_1 = loctr.add_auto('value', key+'_source_to_currency_rate_inv', auto_formatter=highlight(1/source_to_currency_rate))
        tr_text = f"{endl}{highlight('1')} {tr_st} == {tr_value_0} point(s){endl}" \
                                    f"{highlight('1')} point == {tr_value_1} {tr_st}"

        text = loctr.add_auto('chunks', key, auto_formatter=tr_text)
        dabd_df.loc[key] = dabd_orig_df.loc[key]
        dabd_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

        for ab in ability_names:
            cost_value = bcasacv_df.loc[('army_ability_bar_fill', ab)]['cost_value']
            key = 'unit_abilities_tooltip_text_' + ab
            tr_value_0 = loctr.add_auto('value', key+'_cost_value', auto_formatter=highlight(cost_value))
            tr_value_1 = loctr.add_auto('value', key+'_cost_value_inv', auto_formatter=highlight(cost_value/source_to_currency_rate))
            tr_text = f"Costs {tr_value_0} points ({tr_value_1} {tr_st})"

            text = loctr.add_auto('chunks', f'army_ability_cost_{ab}', auto_formatter=tr_text)
            uab_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)


    # ARMY ABILITIES
    #daemons
    row = bscslt_df[bscslt_df['faction_group'] == 'wh3_main_fact_group_daemons'].iloc[0]
    source_type = 'damage as gold' #row['source_type']
    source_to_currency_rate = row['source_unitary_value']
    key = 'daemon_ability_bar_descriptions_bar_description_faction_set_culture_daemons'
    tr_value_0 = loctr.add_auto('value', key+'_source_to_currency_rate', auto_formatter=highlight(source_to_currency_rate))
    tr_value_1 = loctr.add_auto('value', key+'_source_to_currency_rate_inv', auto_formatter=highlight(1/source_to_currency_rate))
    tr_text = f"{endl}{highlight('1')} {source_type} == {tr_value_0} point(s){endl}" \
                                f"{highlight('1')} point == {tr_value_1} {source_type}"
    text = loctr.add_auto('chunks', key, auto_formatter=tr_text)
    dabd_df.loc[key] = dabd_orig_df.loc[key]
    dabd_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    key = 'uied_component_texts_localised_string_label_bonuses_NewState_Text_a994acf4'
    tr_value_10 = loctr.add_auto('value', key+'_cost_value_1', auto_formatter=highlight(100))
    tr_value_11 = loctr.add_auto('value', key+'_cost_value_inv_1', auto_formatter=highlight(100/source_to_currency_rate))
    tr_value_20 = loctr.add_auto('value', key+'_cost_value_1', auto_formatter=highlight(200))
    tr_value_21 = loctr.add_auto('value', key+'_cost_value_inv_1', auto_formatter=highlight(200/source_to_currency_rate))
    tr_value_30 = loctr.add_auto('value', key+'_cost_value_1', auto_formatter=highlight(300))
    tr_value_31 = loctr.add_auto('value', key+'_cost_value_inv_1', auto_formatter=highlight(300/source_to_currency_rate))
    tr_text = f"{endl}||1st ability requires {tr_value_10} Glory Points ({tr_value_11})" \
                                f"{endl}2nd ability requires {tr_value_20} Glory Points ({tr_value_21})" \
                                f"{endl}3rd ability requires {tr_value_30} Glory Points ({tr_value_31})"

    text = loctr.add_auto('chunks', f'dae_daemons_costs', auto_formatter=tr_text)
    uied_df.loc[key] = uied_orig_df.loc[key]
    uied_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    # Khorne
    row = bscslt_df[bscslt_df['faction_group'] == 'wh3_main_fact_group_khorne'].iloc[0]
    source_type = row['source_type']
    source_to_currency_rate = row['source_unitary_value']
    key = 'daemon_ability_bar_descriptions_bar_description_khornate_factions'
    ability_names = ['wh3_main_army_abilities_horn_of_khorne', 'wh3_main_army_abilities_relentless_rage', 'wh3_main_army_abilities_blade_of_khorne']
    army_ability_format(key, source_type, source_to_currency_rate, ability_names)

    # Nurgle
    row = bscslt_df[bscslt_df['faction_group'] == 'wh3_main_fact_group_nurgle'].iloc[0]
    source_type = row['source_type']
    source_to_currency_rate = row['source_unitary_value']
    key = 'daemon_ability_bar_descriptions_bar_description_nurglish_factions'
    ability_names = ['wh3_main_army_abilities_curse_of_the_slug', 'wh3_main_army_abilities_fecundity', 'wh3_main_army_abilities_rot_glorious_rot']
    army_ability_format(key, source_type, source_to_currency_rate, ability_names)

    # Slaanesh
    row = bscslt_df[bscslt_df['faction_group'] == 'wh3_main_fact_group_slaanesh'].iloc[0]
    source_type = row['source_type']
    source_to_currency_rate = row['source_unitary_value']
    key = 'daemon_ability_bar_descriptions_bar_description_slaaneshi_factions'
    ability_names = ['wh3_main_army_abilities_fascination', 'wh3_main_army_abilities_narcissism', 'wh3_main_army_abilities_sweet_sorrow']
    army_ability_format(key, source_type, source_to_currency_rate, ability_names)

    # Tzeentch
    row = bscslt_df[bscslt_df['faction_group'] == 'wh3_main_fact_group_tzeentch'].iloc[0]
    source_type = row['source_type']
    source_to_currency_rate = row['source_unitary_value']
    key = 'daemon_ability_bar_descriptions_bar_description_tzeentchian_factions'
    ability_names = ['wh3_main_army_abilities_arcane_surge', 'wh3_main_army_abilities_bolt_of_change', 'wh3_main_army_abilities_storm_of_fire']
    army_ability_format(key, source_type, source_to_currency_rate, ability_names)

    # Ogres
    row = bscslt_df[bscslt_df['faction_group'] == 'wh3_main_fact_group_ogre_kingdoms'].iloc[0]
    source_type = row['source_type']
    source_to_currency_rate = row['source_unitary_value']
    key = 'daemon_ability_bar_descriptions_bar_description_faction_set_culture_ogres'
    ability_names = ['wh3_main_prisoners_dismember', 'wh3_main_prisoners_massacre', 'wh3_main_prisoners_butcher']
    army_ability_format(key, source_type, source_to_currency_rate, ability_names)


    def col_fat(x):
        return formatter.colorize(' '.join([e.capitalize() for e in x[8:].split('_')]), x)


    ufet_df = handler.db['unit_fatigue_effects_tables'].data
    def fa(key):
        entry = ufet_df.loc[key]
        t = f"-{roundf((1-entry[2])*100)}"
        return formatter.colorize(t, 'fatigue_'+key[0][10:])

    tr_value_fresh = loctr.add_auto('fatigues', 'fatigue_fresh', auto_formatter=col_fat)
    tr_value_active = loctr.add_auto('fatigues', 'fatigue_active', auto_formatter=col_fat)
    tr_value_winded = loctr.add_auto('fatigues', 'fatigue_winded', auto_formatter=col_fat)
    tr_value_tired = loctr.add_auto('fatigues', 'fatigue_tired', auto_formatter=col_fat)
    tr_value_very_tired = loctr.add_auto('fatigues', 'fatigue_very_tired', auto_formatter=col_fat)
    tr_value_exhausted = loctr.add_auto('fatigues', 'fatigue_exhausted', auto_formatter=col_fat)


    key = 'unit_attributes_bullet_text_fatigue_immune'
    ua_df.loc[key] = ua_orig_df.loc[key]
    tr_text = f"{endl}||Fatigue effects({highlight('%')}, scalar for {icon['stat_morale']}):{endl}" \
        f"{_icon('fatigue')}|{tr_value_active}|{tr_value_winded}|{tr_value_tired}|{tr_value_very_tired}|{tr_value_exhausted}{endl}"
    text = loctr.add_auto('chunks', 'fatigue_table_header', auto_formatter=tr_text)

    s = 'stat_melee_attack'
    tr_text = f"{icon[s]}|{' '*3+fa(('threshold_active', s))+' '*3}|{' '*4+fa(('threshold_winded', s))+' '*4}|{' '*2+fa(('threshold_tired', s))+' '*2}|{' '*5+fa(('threshold_very_tired', s))+' '*5}|{' '*5+fa(('threshold_exhausted', s))}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)
    s = 'scalar_speed'
    tr_text = f"{icon[s]}|{' '*9}|{' '*4+fa(('threshold_winded', s))+' '*4}|{' '*2+fa(('threshold_tired', s))+' '*2}|{' '*5+fa(('threshold_very_tired', s))+' '*5}|{' '*5+fa(('threshold_exhausted', s))}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)
    s = 'stat_melee_damage_ap'
    tr_text = f"{icon[s]}|{' '*9}|{' '*3+fa(('threshold_winded', s))+' '*3}|{' '*2+fa(('threshold_tired', s))+' '*2}|{' '*5+fa(('threshold_very_tired', s))+' '*5}|{' '*5+fa(('threshold_exhausted', s))}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)
    s = 'stat_charge_bonus'
    tr_text = f"{icon[s]}|{' '*9}|{' '*11}|{' '*2+fa(('threshold_tired', s))+' '*2}|{' '*5+fa(('threshold_very_tired', s))+' '*5}|{' '*5+fa(('threshold_exhausted', s))}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)
    s = 'stat_armour'
    tr_text = f"{icon[s]}|{' '*9}|{' '*11}|{' '*9}|{' '*5+fa(('threshold_very_tired', s))+' '*5}|{' '*5+fa(('threshold_exhausted', s))}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)
    s = 'stat_melee_defence'
    tr_text = f"{icon[s]}|{' '*9}|{' '*11}|{' '*9}|{' '*15}|{' '*5+fa(('threshold_exhausted', s))}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)
    s = 'stat_reloading'
    tr_text = f"{icon[s]}|{' '*9}|{' '*11}|{' '*9}|{' '*15}|{' '*5+fa(('threshold_exhausted', s))}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)
    s = 'stat_morale'
    tr_text = f"{icon[s]}|{' '*9}|{' '*11}|{' '*9}|{' '*6 +formatter.colorize(roundf(morale_df.loc['ume_concerned_very_tired', 'value']), 'red')+ ' '*6}|{' '*5+formatter.colorize(roundf(morale_df.loc['ume_concerned_exhausted', 'value']), 'red')}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_table_body_'+s, auto_formatter=tr_text)

    tr_text = f"||The fatigue modifier applies after all other modifiers:{endl}" \
            f"( {formatter.colorize('base', 'white')} + sum({highlight('scalar_mods')}) + sum({highlight('perc_mods')} * {formatter.colorize('base', 'white')}) ) * {highlight('stamina_mod')}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_formula', auto_formatter=tr_text)

    kv_ft = handler.db['_kv_fatigue_tables'].data
    rrf = lambda x: formatter.colorize('+' + str(roundf(kv_ft.loc[x, 'value'])), 'red')
    grf = lambda x: formatter.colorize(roundf(kv_ft.loc[x, 'value']), 'green')
    hrf = lambda x: highlight(roundf(x))

    tr_text = f"||Fatigue thresholds (share/threshold):{endl}" \
        f"{tr_value_fresh}: {hrf(kv_ft.loc['threshold_fresh', 'value'])} - {hrf(kv_ft.loc['threshold_active', 'value'])} ({hrf((kv_ft.loc['threshold_active', 'value']-kv_ft.loc['threshold_fresh', 'value'])/kv_ft.loc['threshold_max', 'value']*100)}%/{hrf(kv_ft.loc['threshold_active', 'value']/kv_ft.loc['threshold_max', 'value']*100)}%){endl}" \
        f"{tr_value_active}: {hrf(kv_ft.loc['threshold_active', 'value'])} - {hrf(kv_ft.loc['threshold_winded', 'value'])} ({hrf((kv_ft.loc['threshold_winded', 'value']-kv_ft.loc['threshold_active', 'value'])/kv_ft.loc['threshold_max', 'value']*100)}%/{hrf(kv_ft.loc['threshold_winded', 'value']/kv_ft.loc['threshold_max', 'value']*100)}%){endl}" \
        f"{tr_value_winded}: {hrf(kv_ft.loc['threshold_winded', 'value'])} - {hrf(kv_ft.loc['threshold_tired', 'value'])} ({hrf((kv_ft.loc['threshold_tired', 'value']-kv_ft.loc['threshold_winded', 'value'])/kv_ft.loc['threshold_max', 'value']*100)}%/{hrf(kv_ft.loc['threshold_tired', 'value']/kv_ft.loc['threshold_max', 'value']*100)}%){endl}" \
        f"{tr_value_tired}: {hrf(kv_ft.loc['threshold_tired', 'value'])} - {hrf(kv_ft.loc['threshold_very_tired', 'value'])} ({hrf((kv_ft.loc['threshold_very_tired', 'value']-kv_ft.loc['threshold_tired', 'value'])/kv_ft.loc['threshold_max', 'value']*100)}%/{hrf(kv_ft.loc['threshold_very_tired', 'value']/kv_ft.loc['threshold_max', 'value']*100)}%){endl}" \
        f"{tr_value_very_tired}: {hrf(kv_ft.loc['threshold_very_tired', 'value'])} - {hrf(kv_ft.loc['threshold_exhausted', 'value'])} ({hrf((kv_ft.loc['threshold_exhausted', 'value']-kv_ft.loc['threshold_very_tired', 'value'])/kv_ft.loc['threshold_max', 'value']*100)}%/{hrf(kv_ft.loc['threshold_exhausted', 'value']/kv_ft.loc['threshold_max', 'value']*100)}%){endl}" \
        f"{tr_value_exhausted}: {hrf(kv_ft.loc['threshold_exhausted', 'value'])} - {hrf(kv_ft.loc['threshold_max', 'value'])} ({hrf((kv_ft.loc['threshold_max', 'value']-kv_ft.loc['threshold_exhausted', 'value'])/kv_ft.loc['threshold_max', 'value']*100)}%/{hrf(100)}%){endl}"
    text += loctr.add_auto('chunks', 'fatigue_thresholds', auto_formatter=tr_text)

    tr_text = f"||Fatigue actions:{endl}"
              # f"Walking non-artillery/artillery/horse_artillery: {grf('walking')}/{rrf('walking_horse_artillery')}/{rrf('walking_artillery')}{endl}" \
    text += loctr.add_auto('chunks', 'fatigue_actions', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'fatigue_actions_idle_idle', auto_formatter=grf('idle'))
    tr_value_1 = loctr.add_auto('value', 'fatigue_actions_idle_in_building', auto_formatter=grf('idle_in_building'))
    tr_value_2 = loctr.add_auto('value', 'fatigue_actions_idle_rain', auto_formatter=grf('idle_rain'))
    tr_value_3 = loctr.add_auto('value', 'fatigue_actions_idle_snow', auto_formatter=grf('idle_snow'))
    tr_text = f"Idle (normal/in building/rain/snow): {tr_value_0}/{tr_value_1}/{tr_value_2}/{tr_value_3}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_actions_idle', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'fatigue_actions_ready', auto_formatter=grf('ready'))
    tr_text = f"Ready: {tr_value_0}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_actions_ready', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'fatigue_actions_walking', auto_formatter=grf('walking'))
    tr_value_1 = loctr.add_auto('value', 'fatigue_actions_running', auto_formatter=rrf('running'))
    tr_text = f"Walking/running: {tr_value_0}/{tr_value_1}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_actions_walking', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'fatigue_actions_shooting', auto_formatter=rrf('shooting'))
    tr_value_1 = loctr.add_auto('value', 'fatigue_actions_combat', auto_formatter=rrf('combat'))
    tr_value_2 = loctr.add_auto('value', 'fatigue_actions_charging', auto_formatter=rrf('charging'))
    tr_text = f"Shooting/combat/charging: {tr_value_0}/{tr_value_1}/{tr_value_2}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_actions_combat', auto_formatter=tr_text)

    tr_value_0 = loctr.add_auto('value', 'fatigue_actions_shallow', auto_formatter=hrf(kv_ft.loc['gradient_shallow_movement_multiplier', 'value']))
    tr_value_1 = loctr.add_auto('value', 'fatigue_actions_steep', auto_formatter=hrf(kv_ft.loc['gradient_steep_movement_multiplier', 'value']))
    tr_value_2 = loctr.add_auto('value', 'fatigue_actions_very_steep', auto_formatter=hrf(kv_ft.loc['gradient_very_steep_movement_multiplier', 'value']))
    tr_text = f"Gradient movement multiplier (shallow/steep/very steep): {tr_value_0}/{tr_value_1}/{tr_value_2}{endl}"
    text += loctr.add_auto('chunks', 'fatigue_actions_gradient', auto_formatter=tr_text)



    def fatigue_exp():
        import numpy as np
        t = ''
        df = handler.db['unit_stats_land_experience_bonuses_tables'].data
        fatigs = np.sort(pd.unique(df['fatigue']))[::-1]
        for fm in fatigs:
            s = f"{hrf(fm)} "
            sub_df = df[df['fatigue'] == fm]
            for k, v in sub_df.iterrows():
                xp = roundf(v['xp_level'])
                if xp == 0:
                    continue
                s += _icon(f"experience_{xp}")
            t += s + endl
        return t

    tr_text = f"||Experienced units have fatigue action modifiers{endl} (RoR don't count as experienced units):{endl}"+fatigue_exp()
    text += loctr.add_auto('chunks', 'fatigue_experienced', auto_formatter=tr_text)

    ua_df.loc[key] = ua_orig_df.loc[key]
    ua_df.loc[key, 'text'] += loctr.add_auto('overrides', key, auto_formatter=text)

    # ABILITY TYPES
    uat_orig_df = handler.locs['unit_ability_types__'].data
    uat_df = handler.duplicate_table('unit_ability_types__', prefix=PREFIX, copy_data=False).data

    # uat_df.loc[key, 'text'] += f"||Resisted by {icon['stat_resistance_all']} + {icon['stat_resistance_magic']}"


    # key = 'unit_ability_types_localised_description_wh_type_vortex'
    # uat_df.loc[key] = uat_orig_df.loc[key]
    # uat_df.loc[key, 'text'] += f"||Resisted by {icon['stat_resistance_all']} + {icon['stat_resistance_magic']}"
    #
    # key = 'unit_ability_types_localised_description_wh_type_explosion'
    # uat_df.loc[key] = uat_orig_df.loc[key]
    # uat_df.loc[key, 'text'] += f"||Resisted by {icon['stat_resistance_all']} + {icon['stat_resistance_magic']}"
    #
    # key = 'unit_ability_types_localised_description_wh_type_breath'
    # uat_df.loc[key] = uat_orig_df.loc[key]
    # uat_df.loc[key, 'text'] += f"||Resisted by {icon['stat_resistance_all']} + {icon['stat_resistance_magic']}"
    #
    # key = 'unit_ability_types_localised_description_wh_type_wind'
    # uat_df.loc[key] = uat_orig_df.loc[key]
    # uat_df.loc[key, 'text'] += f"||Resisted by {icon['stat_resistance_all']} + {icon['stat_resistance_magic']}"

    tprefix = 'unit_ability_types_localised_description_wh_type_'

    tr_text = f"||Resisted by {icon['stat_resistance_all']} + {icon['stat_resistance_missile']} ( + {icon['stat_resistance_magic']}) ( + {icon['stat_resistance_flame']})"
    text = loctr.add_auto('chunks', 'magic_missile_res', auto_formatter=tr_text)
    for k in ['magic_missile', 'magic_missiles', 'bombardment']:
        key = tprefix + k
        uat_df.loc[key] = uat_orig_df.loc[key]
        uat_df.loc[key, 'text'] += text

    tr_text = f"||Resisted by {icon['stat_resistance_all']} + {icon['stat_resistance_magic']}"
    text = loctr.add_auto('chunks', 'direct_damage_res', auto_formatter=tr_text)
    for k in ['direct_damage', 'area_of_direct_damage', 'chain_direct_damage']:
        key = tprefix + k
        uat_df.loc[key] = uat_orig_df.loc[key]
        uat_df.loc[key, 'text'] += text

    tr_text = f"||Augments of unit stats are affected by fatigue effects (look at {highlight('Perfect Vigour')} for more info)"
    text = loctr.add_auto('chunks', 'augments_fatigue', auto_formatter=tr_text)
    for k in ['augment', 'area_of_augments', 'chain_augment']:
        key = tprefix + k
        uat_df.loc[key] = uat_orig_df.loc[key]
        uat_df.loc[key, 'text'] += text

    tr_text = f"||Hexes of unit stats are affected by fatigue effects (look at {highlight('Perfect Vigour')} for more info)"
    text = loctr.add_auto('chunks', 'hexes_fatigue', auto_formatter=tr_text)
    for k in ['hex', 'area_of_hexes', 'chain_hex']:
        key = tprefix + k
        uat_df.loc[key] = uat_orig_df.loc[key]
        uat_df.loc[key, 'text'] += text


    key = tprefix + 'bombardment'
    tr_text = f"{endl}||{icon['cooldown']}{highlight(loctr.tr('bombardment_arrival_window'))} - a time window during which projectiles are spawning evenly."
    tr_text += f"{endl}{icon['distance']}{highlight(loctr.tr('bombardment_radius_spread'))} - a radius of the circle in which projectiles will land."
    text = loctr.add_auto('chunks', 'bombardment_desc', auto_formatter=tr_text)
    uat_df.loc[key, 'text'] += text

    key = tprefix + 'vortex'
    tr_text = f"{endl}||{icon['cooldown']}{highlight(loctr.tr('vortex_delta'))} - a time interval between spawning vortexes."
    tr_text += f"{endl}{highlight(loctr.tr('vortex_detonation_force'))} - TODO."
    tr_text += f"{endl}{icon['infinite_height']}[mod] - the vortex is an infinite cylinder and will damage flying units. Note: the vortex is a sphere by default and it can still damage flying units if the radius is long enough."
    text = loctr.add_auto('chunks', 'vortex_desc', auto_formatter=tr_text)
    uat_df.loc[key] = uat_orig_df.loc[key]
    uat_df.loc[key, 'text'] += text


    tr_value_0 = loctr.add_auto('value', 'healing_percentage_cap', auto_formatter=highlight(roundf(kv_unit_df.loc['healing_percentage_cap', 'value']*100)))
    tr_text = f"||Healing Percentage Cap: {tr_value_0}%"
    text = loctr.add_auto('chunks', 'heal_cap', auto_formatter=tr_text)
    for k in ['regeneration', 'area_of_regeneration', 'chain_regeneration']:
        key = tprefix + k
        uat_df.loc[key] = uat_orig_df.loc[key]
        uat_df.loc[ key, 'text'] += text


    # ABILITIES
    text = endl + f"{formatter.icon['scalar_missile_range']}{highlight(90)} -> {highlight(117)}" + endl
    text += f"{formatter.icon['scalar_missile_range']}{highlight(130)} -> {highlight(169)}" + endl
    text += f"{formatter.icon['scalar_missile_range']}{highlight(140)} -> {highlight(182)}" + endl
    text += f"{formatter.icon['scalar_missile_range']}{highlight(160)} -> {highlight(208)}" + endl
    text += f"{formatter.icon['scalar_missile_range']}{highlight(450)} -> {highlight(585)}"
    key = 'unit_abilities_additional_ui_effects_localised_text_wh3_main_spell_tempest_gust_of_true_flight'
    uaaue_df.loc[key, 'text'] += text
    key = 'unit_abilities_additional_ui_effects_localised_text_wh3_main_spell_tempest_gust_of_true_flight_upgraded'
    uaaue_df.loc[key, 'text'] += text

    text = endl + f"{formatter.icon['scalar_missile_range']}{highlight(120)} -> {highlight(144)}"
    key = 'unit_abilities_additional_ui_effects_localised_text_wh2_dlc17_lord_abilities_master_predator'
    uaaue_df.loc[key, 'text'] += text


    # BUGS
    key = 'unit_abilities_additional_ui_effects_localised_text_wh3_main_army_abilities_arcane_surge'
    uaaue_df.loc[key, 'text'] += f"||{highlight(loctr.tr('note_arcane_surge'))}"

    for k in ['direct_damage', 'area_of_direct_damage', 'chain_direct_damage']:
        key = 'unit_ability_types_localised_description_wh_type_' + k
        uat_df.loc[key, 'text'] += f"||{highlight(loctr.tr('bug_dd_extra_tick'))}"
        uat_df.loc[key, 'text'] += f"||{highlight(loctr.tr('bug_dd_upper_range'))}"
        uat_df.loc[key, 'text'] += f"||{highlight(loctr.tr('bug_dd_lower_range'))}"
        uat_df.loc[key, 'text'] += f"||{highlight(loctr.tr('bug_dd_ui'))}"

    # key = 'unit_ability_types_localised_description_wh_type_direct_damage'
    # text = "NOTE (patch 1.3): Direct damage spells now deal magical (non-physical) damage, meaning that Physical Resistance will no longer serve as a layer of defence as it did previously (since the TW:WH3 release)."
    # uat_df.loc[key, 'text'] += f"||{highlight(text)}"
    pass


if __name__ == '__main__':
    typee = 'Workshop'
    # typee = 'MP_release_movie'

    if typee == 'Workshop':
        MOD_NAME = 'Klissan_ASMR'
    if  typee == 'MP_release_movie':
        MOD_NAME = f"!Klissan_ASMR_{datetime.today().strftime('%Y_%m_%d')}.MOVIE"
    PREFIX = f'{MOD_NAME}_'
    OUTPUT_DIR = 'output'
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    rpfm = RPFM4Wrapper()
    handler = Handler()
    hh = HandlerHelper(handler)
    localizator = Localizator(handler, PREFIX)
    formatter = Formatter(hh, localizator, 'ultra')

    _prepare_ui_effects_juncs_tables(handler)
    generate_ability_phases_descs(hh, formatter)
    generate_unit_stats(hh, formatter, is_generate_animations=False)
    generate_ability_descs(hh, formatter)

    modify_unit_tooltip(hh, formatter)
    # modify_campaign_tooltips(hh, formatter)

    modify_spell_icons(handler)

    localizator.compile()
    handler.dump_mod_tables(OUTPUT_DIR)
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    pass
