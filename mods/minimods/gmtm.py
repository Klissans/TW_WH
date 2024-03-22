import os
import shutil

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper
from src.localizator import Localizator

from src.formatter import Formatter


def generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, unit_key):
    uubpet.loc[unit_key] = {'key':unit_key, 'state': 'very_positive',  'sort_order': 0}
    uubpuot.loc[unit_key] = {'unit_key': unit_key, 'bullet_point': unit_key}

    info = hh.get_unit_info(unit_key)
    luid = info['land_unit']
    full_formatted_info = formatter.get_full_unit_desc(info, luid)
    bp_name = 'ui_unit_bullet_point_enums_onscreen_name_' + unit_key
    bp_tooltip = 'ui_unit_bullet_point_enums_tooltip_' + unit_key

    bp_text_loc.loc[bp_name] = {'key': bp_name, 'text': 'Unit Stats', 'tooltip': True}
    bp_text_loc.loc[bp_tooltip] = {'key': bp_tooltip, 'text': full_formatted_info, 'tooltip': True}


def create_faction(hh):
    handler = hh.handler

    df = handler.duplicate_table('culture_pack_ids_tables', prefix=PREFIX, copy_data=False).data
    culture_pack_ids_tables_key = 'gmtm_subculture'
    df.loc[culture_pack_ids_tables_key] = {'id': culture_pack_ids_tables_key}

    df = handler.duplicate_table('cultures_subcultures_tables', prefix=PREFIX, copy_data=False).data
    cultures_subcultures_tables_key = 'gmtm_subculture'
    df.loc[cultures_subcultures_tables_key] = {'subculture': cultures_subcultures_tables_key, 'culture': 'wh2_main_rogue', 'index': 1771987661}


    df = handler.duplicate_table('culture_packs_tables', prefix=PREFIX, copy_data=False).data
    # df.loc[(culture_pack_ids_tables_key, cultures_subcultures_tables_key)] = {'id': culture_pack_ids_tables_key, 'subculture': cultures_subcultures_tables_key} # multiindex doesn't work?
    df.loc[culture_pack_ids_tables_key] = {'id': culture_pack_ids_tables_key, 'subculture': cultures_subcultures_tables_key}


    df = handler.duplicate_table('factions_tables', prefix=PREFIX, copy_data=False).data
    faction_tables_key = 'gmtm_faction'
    df.loc[faction_tables_key] = handler.db['factions_tables'].data.loc['wh3_main_kho_khorne']
    df.loc[faction_tables_key, 'key'] = faction_tables_key
    df.loc[faction_tables_key, 'index'] = 1031099
    df.loc[faction_tables_key, 'subculture'] = cultures_subcultures_tables_key
    df.loc[faction_tables_key, 'category'] = 'playable'

    df = handler.duplicate_table('custom_battle_factions_tables', prefix=PREFIX, copy_data=False).data
    df.loc[faction_tables_key] = {'faction_key': faction_tables_key, 'sort_order': 999, 'culture_sort_order': 1}


def kv_rules(hh):
    handler = hh.handler

    df = handler.duplicate_table('_kv_rules_tables', prefix=PREFIX, copy_data=False).data
    df.loc['melee_hit_chance_base'] = {'key': 'melee_hit_chance_base', 'value': 0}
    df.loc['melee_hit_chance_max'] = {'key': 'melee_hit_chance_max', 'value': 100}
    df.loc['melee_hit_chance_min'] = {'key': 'melee_hit_chance_min', 'value': 0}
    df.loc['ward_save_max_value'] = {'key': 'ward_save_max_value', 'value': 100}
    df.loc['ward_save_min_value'] = {'key': 'ward_save_min_value', 'value': -100}

    df = handler.duplicate_table('_kv_fatigue_tables', prefix=PREFIX, copy_data=False).data
    df.loc['climbing_ladders'] = {'key': 'climbing_ladders', 'value': 100_000}
    df.loc['climbing_walls'] = {'key': 'climbing_walls', 'value': 100_000}
    df.loc['threshold_fresh'] = {'key': 'threshold_fresh', 'value': 0}
    df.loc['threshold_active'] = {'key': 'threshold_active', 'value': 59996}
    df.loc['threshold_winded'] = {'key': 'threshold_winded', 'value': 59997}
    df.loc['threshold_tired'] = {'key': 'threshold_tired', 'value': 59998}
    df.loc['threshold_very_tired'] = {'key': 'threshold_very_tired', 'value': 59999}
    df.loc['threshold_exhausted'] = {'key': 'threshold_exhausted', 'value': 60000}
    df.loc['threshold_max'] = {'key': 'threshold_max', 'value': 100_000}

    df = handler.duplicate_table('unit_fatigue_effects_tables', prefix=PREFIX, copy_data=False).data
    df.loc['1'] = {'fatigue_level': 'threshold_exhausted', 'stat': 'scalar_speed', 'value': 1}
    df.loc['2'] = {'fatigue_level': 'threshold_exhausted', 'stat': 'stat_armour', 'value': 1}
    df.loc['3'] = {'fatigue_level': 'threshold_exhausted', 'stat': 'stat_charge_bonus', 'value': 0}
    df.loc['4'] = {'fatigue_level': 'threshold_exhausted', 'stat': 'stat_melee_attack', 'value': 1}
    df.loc['5'] = {'fatigue_level': 'threshold_exhausted', 'stat': 'stat_melee_damage_ap', 'value': 0.5}
    df.loc['6'] = {'fatigue_level': 'threshold_exhausted', 'stat': 'stat_melee_defence', 'value': 1}
    df.loc['7'] = {'fatigue_level': 'threshold_exhausted', 'stat': 'stat_reloading', 'value': 0}

    df = handler.duplicate_table('ground_type_to_stat_effects_tables', prefix=PREFIX, copy_data=False).data
    df.loc['1'] = {'ground_type': 'shallow_water', 'affected_stat': 'stat_melee_damage_ap', 'multiplier': 0.7, 'affected_group': 'small'}




def add_content(hh,formatter):
    handler = hh.handler
    unique_unit_index = handler.db['main_units_tables'].data['unique_index'].max() + 1000
    unique_ability_id = handler.db['unit_special_abilities_tables'].data['unique_id'].max() + 1000

    mut = handler.duplicate_table('main_units_tables', prefix=PREFIX, copy_data=False).data
    lut = handler.duplicate_table('land_units_tables', prefix=PREFIX, copy_data=False).data
    # ctbatt = handler.duplicate_table('culture_to_battle_animation_tables_tables', prefix=PREFIX, copy_data=False).data
    uvt = handler.duplicate_table('unit_variants_tables', prefix=PREFIX, copy_data=False).data
    ucbpt = handler.duplicate_table('units_custom_battle_permissions_tables', prefix=PREFIX, copy_data=False).data

    bet = handler.duplicate_table('battle_entities_tables', prefix=PREFIX, copy_data=False).data
    bfet = handler.duplicate_table('battlefield_engines_tables', prefix=PREFIX, copy_data=False).data
    melee_wt = handler.duplicate_table('melee_weapons_tables', prefix=PREFIX, copy_data=False).data
    missile_wt = handler.duplicate_table('missile_weapons_tables', prefix=PREFIX, copy_data=False).data
    pt = handler.duplicate_table('projectiles_tables', prefix=PREFIX, copy_data=False).data
    pet = handler.duplicate_table('projectiles_explosions_tables', prefix=PREFIX, copy_data=False).data

    uat = handler.duplicate_table('unit_abilities_tables', prefix=PREFIX, copy_data=False).data
    usat = handler.duplicate_table('unit_special_abilities_tables', prefix=PREFIX, copy_data=False).data
    lutuajt = handler.duplicate_table('land_units_to_unit_abilites_junctions_tables', prefix=PREFIX, copy_data=False).data
    satsapjt = handler.duplicate_table('special_ability_to_special_ability_phase_junctions_tables', prefix=PREFIX, copy_data=False).data
    sapt = handler.duplicate_table('special_ability_phases_tables', prefix=PREFIX, copy_data=False).data
    sapset = handler.duplicate_table('special_ability_phase_stat_effects_tables', prefix=PREFIX, copy_data=False).data

    lu_loc = handler.duplicate_table('land_units__', prefix=PREFIX, copy_data=False).data

    uubpet = handler.duplicate_table('ui_unit_bullet_point_enums_tables', prefix=PREFIX, copy_data=False).data
    uubpuot = handler.duplicate_table('ui_unit_bullet_point_unit_overrides_tables', prefix=PREFIX, copy_data=False).data
    bp_text_loc = handler.duplicate_table('ui_unit_bullet_point_enums__', prefix=PREFIX, copy_data=False).data

    def copy_unit(mut_base_key: str, new_key: str):
        nonlocal unique_unit_index
        main_unit = handler.db['main_units_tables'].data.loc[mut_base_key].to_dict()
        land_unit = handler.db['land_units_tables'].data.loc[main_unit['land_unit']].to_dict()

        # Not needed for wh3
        # if land_unit['man_animation'] not in ctbatt:
        #     ctbatt.loc[land_unit['man_animation']] = {'culture_pack': 'gmtm_subculture', 'battle_animations_table': land_unit['man_animation']}

        df = handler.db['unit_variants_tables'].data
        unit_variant = df[df['unit'] == land_unit['key']].iloc[0].to_dict()
        unit_variant['name'] = new_key
        unit_variant['unit'] = new_key
        uvt.loc[new_key] = unit_variant

        df = handler.db['units_custom_battle_permissions_tables'].data
        unit_permission = df[df['unit'] == main_unit['unit']].iloc[0].to_dict()
        unit_permission['unit'] = new_key
        unit_permission['faction'] = 'gmtm_faction'
        ucbpt.loc[new_key] = unit_permission

        land_unit['key'] = new_key
        lut.loc[new_key] = land_unit

        main_unit['unit'] = new_key
        main_unit['land_unit'] = land_unit['key']
        main_unit['unique_index'] = unique_unit_index
        unique_unit_index += 1
        mut.loc[new_key] = main_unit
        lu_loc.loc[new_key] = {'key': 'land_units_onscreen_name_'+new_key, 'text': new_key, 'tooltip': False}
        return lut.loc[new_key]

    def copy_battle_entity(bet_base_key: str, new_key: str):
        battle_entity = handler.db['battle_entities_tables'].data.loc[bet_base_key].to_dict()
        battle_entity['key'] = new_key
        bet.loc[new_key] = battle_entity

    def copy_melee_weapon(base_key: str, new_key: str):
        melee_weapon = handler.db['melee_weapons_tables'].data.loc[base_key].to_dict()
        melee_weapon['key'] = new_key
        melee_wt.loc[new_key] = melee_weapon

    def copy_engine(base_key: str, new_key: str):
        engine = handler.db['battlefield_engines_tables'].data.loc[base_key].to_dict()
        copy_missile_weapon(engine['missile_weapon'], new_key)
        engine['key'] = new_key
        engine['missile_weapon'] = new_key
        bfet.loc[new_key] = engine

    def copy_missile_weapon(base_key: str, new_key: str):
        missile_weapon = handler.db['missile_weapons_tables'].data.loc[base_key].to_dict()
        projectile = handler.db['projectiles_tables'].data.loc[missile_weapon['default_projectile']].to_dict()
        projectile['key'] = new_key
        pt.loc[new_key] = projectile
        missile_weapon['key'] = new_key
        missile_weapon['default_projectile'] = projectile['key']
        missile_wt.loc[new_key] = missile_weapon

    def copy_projectile_explosion(base_key: str, new_key: str):
        pexp = handler.db['projectiles_explosions_tables'].data.loc[base_key].to_dict()
        pexp['key'] = new_key
        pet.loc[new_key] = pexp

    def copy_ability(base_key: str, new_key: str):
        nonlocal unique_ability_id
        ability = handler.db['unit_abilities_tables'].data.loc[base_key].to_dict()
        sability = handler.db['unit_special_abilities_tables'].data.loc[base_key].to_dict()

        jdf = handler.db['special_ability_to_special_ability_phase_junctions_tables'].data
        for i, e in enumerate(jdf[jdf['special_ability'] == sability['key']].iterrows()):
            phase_key = f'{new_key}_{i}'
            join = e[1]
            phase = handler.db['special_ability_phases_tables'].data.loc[join['phase']].to_dict()
            phase['id'] = phase_key
            sapt.loc[phase_key] = phase
            join['special_ability'] = new_key
            join['phase'] = phase_key
            satsapjt.loc[phase_key] = join

        ability['key'] = new_key
        uat.loc[new_key] = ability

        sability['key'] = new_key
        sability['unique_id'] = unique_ability_id
        unique_ability_id += 1
        usat.loc[new_key] = sability


    #DUMMY LORD
    key = 'gmtm_dummy_lord'
    copy_unit('wh3_main_cth_cha_lord_magistrate_0', key)
    copy_battle_entity('wh_main_infantry_standard_hero_blood_dismembers', key)
    lut.loc[key, 'man_entity'] = key
    lut.loc[key, 'melee_attack'] = 0
    lut.loc[key, 'melee_defence'] = 0
    bet.loc[key, 'walk_speed'] = 0.0
    bet.loc[key, 'run_speed'] = 0.0
    bet.loc[key, 'charge_speed'] = 0.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    #FATIGUE TESTING LORD
    key = 'gmtm_fatigue_lord'
    unit = copy_unit('wh3_main_ksl_cha_boyar_0', key)
    lut.loc[key, 'melee_attack'] = 100
    lut.loc[key, 'melee_defence'] = 100
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'very_small'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets_cooldown'] = 0
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    # Bonus VS TESTING LORD
    key = 'gmtm_bonus_vs_lord'
    unit = copy_unit('wh3_main_ksl_cha_boyar_0', key)
    lut.loc[key, 'melee_attack'] = 0
    lut.loc[key, 'melee_defence'] = 100
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'very_small'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets_cooldown'] = 0
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 100
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    akey = 'gmtm_ability_flat_ap_buff'
    copy_ability('wh3_main_character_abilities_ursuns_roar', akey)
    lutuajt.loc[akey] = {'land_unit': key, 'ability': akey}
    usat.loc[akey, 'active_time'] = 20
    usat.loc[akey, 'recharge_time'] = 1
    phase_key = akey+'_0'
    sapset.loc[phase_key] = {'phase': phase_key, 'stat': 'stat_melee_damage_ap', 'value': 200, 'how': 'add'}

    akey = 'gmtm_ability_flat_ap_debuff'
    copy_ability('wh3_main_character_abilities_ursuns_roar', akey)
    lutuajt.loc[akey] = {'land_unit': key, 'ability': akey}
    usat.loc[akey, 'active_time'] = 20
    usat.loc[akey, 'recharge_time'] = 1
    phase_key = akey+'_0'
    sapset.loc[phase_key] = {'phase': phase_key, 'stat': 'stat_melee_damage_ap', 'value': -200, 'how': 'add'}

    akey = 'gmtm_ability_perc_ap_buff'
    copy_ability('wh3_main_character_abilities_ursuns_roar', akey)
    lutuajt.loc[akey] = {'land_unit': key, 'ability': akey}
    usat.loc[akey, 'active_time'] = 20
    usat.loc[akey, 'recharge_time'] = 1
    phase_key = akey+'_0'
    sapset.loc[phase_key] = {'phase': phase_key, 'stat': 'stat_melee_damage_ap', 'value': 1.5, 'how': 'mult'}

    akey = 'gmtm_ability_perc_ap_debuff'
    copy_ability('wh3_main_character_abilities_ursuns_roar', akey)
    lutuajt.loc[akey] = {'land_unit': key, 'ability': akey}
    usat.loc[akey, 'active_time'] = 20
    usat.loc[akey, 'recharge_time'] = 1
    phase_key = akey+'_0'
    sapset.loc[phase_key] = {'phase': phase_key, 'stat': 'stat_melee_damage_ap', 'value': 0.5, 'how': 'mult'}

    akey = 'gmtm_ability_fatigue'
    copy_ability('wh_main_character_abilities_foe_seeker', akey)
    lutuajt.loc[akey] = {'land_unit': key, 'ability': akey}
    usat.loc[akey, 'active_time'] = 20
    usat.loc[akey, 'recharge_time'] = 1
    phase_key = akey+'_0'
    sapt.loc[phase_key, 'fatigue_change_ratio'] = 0.10



    # RESISTANCE UNITS
    key = 'gmtm_res_nores'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 0
    lut.loc[key, 'damage_mod_physical'] = 0
    lut.loc[key, 'damage_mod_magic'] = 0
    lut.loc[key, 'damage_mod_flame'] = 0
    lut.loc[key, 'damage_mod_missile'] = 0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_res_allres'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 90
    lut.loc[key, 'damage_mod_physical'] = 0
    lut.loc[key, 'damage_mod_magic'] = 0
    lut.loc[key, 'damage_mod_flame'] = 0
    lut.loc[key, 'damage_mod_missile'] = 0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_res_allres_barrier'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 90
    lut.loc[key, 'damage_mod_physical'] = 0
    lut.loc[key, 'damage_mod_magic'] = 0
    lut.loc[key, 'damage_mod_flame'] = 0
    lut.loc[key, 'damage_mod_missile'] = 0
    mut.loc[key, 'barrier_health'] = 10_000
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_res_physres'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 0
    lut.loc[key, 'damage_mod_physical'] = 90
    lut.loc[key, 'damage_mod_magic'] = 0
    lut.loc[key, 'damage_mod_flame'] = 0
    lut.loc[key, 'damage_mod_missile'] = 0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_res_spellres'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 0
    lut.loc[key, 'damage_mod_physical'] = 0
    lut.loc[key, 'damage_mod_magic'] = 90
    lut.loc[key, 'damage_mod_flame'] = 0
    lut.loc[key, 'damage_mod_missile'] = 0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)


    key = 'gmtm_res_flameres'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 0
    lut.loc[key, 'damage_mod_physical'] = 0
    lut.loc[key, 'damage_mod_magic'] = 0
    lut.loc[key, 'damage_mod_flame'] = 90
    lut.loc[key, 'damage_mod_missile'] = 0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_res_misres'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 0
    lut.loc[key, 'damage_mod_physical'] = 0
    lut.loc[key, 'damage_mod_magic'] = 0
    lut.loc[key, 'damage_mod_flame'] = 0
    lut.loc[key, 'damage_mod_missile'] = 90
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_res_combined'
    copy_unit('wh3_main_ogr_mon_giant_0', key)
    lut.loc[key, 'bonus_hit_points'] = 9992
    lut.loc[key, 'damage_mod_all'] = 10
    lut.loc[key, 'damage_mod_physical'] = 10
    lut.loc[key, 'damage_mod_magic'] = 10
    lut.loc[key, 'damage_mod_flame'] = 10
    lut.loc[key, 'damage_mod_missile'] = 10
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)


    # DIFFERENT TYPE OF ATTACK
    key = 'gmtm_modattack_regular'
    copy_unit('wh3_main_kho_veh_skullcannon_0', key)
    unit = lut.loc[key]
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    copy_missile_weapon(unit['primary_missile_weapon'], key)
    lut.loc[key, 'primary_missile_weapon'] = key
    pt.loc[key, 'damage'] = 0
    pt.loc[key, 'ap_damage'] = 1000
    pt.loc[key, 'bonus_v_infantry'] = 0
    pt.loc[key, 'bonus_v_large'] = 0
    pt.loc[key, 'calibration_area'] = 0.5
    pt.loc[key, 'explosion_type'] = None
    pt.loc[key, 'ignition_amount'] = 0
    pt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_modattack_flaming'
    copy_unit('wh3_main_kho_veh_skullcannon_0', key)
    unit = lut.loc[key]
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 1
    melee_wt.loc[key, 'is_magical'] = False
    copy_missile_weapon(unit['primary_missile_weapon'], key)
    lut.loc[key, 'primary_missile_weapon'] = key
    pt.loc[key, 'damage'] = 0
    pt.loc[key, 'ap_damage'] = 1000
    pt.loc[key, 'bonus_v_infantry'] = 0
    pt.loc[key, 'bonus_v_large'] = 0
    pt.loc[key, 'calibration_area'] = 0.5
    pt.loc[key, 'explosion_type'] = None
    pt.loc[key, 'ignition_amount'] = 1
    pt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_modattack_magical'
    copy_unit('wh3_main_kho_veh_skullcannon_0', key)
    unit = lut.loc[key]
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = True
    copy_missile_weapon(unit['primary_missile_weapon'], key)
    lut.loc[key, 'primary_missile_weapon'] = key
    pt.loc[key, 'damage'] = 0
    pt.loc[key, 'ap_damage'] = 1000
    pt.loc[key, 'bonus_v_infantry'] = 0
    pt.loc[key, 'bonus_v_large'] = 0
    pt.loc[key, 'calibration_area'] = 0.5
    pt.loc[key, 'explosion_type'] = None
    pt.loc[key, 'ignition_amount'] = 0
    pt.loc[key, 'is_magical'] = True
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_modattack_flaming_magical'
    copy_unit('wh3_main_kho_veh_skullcannon_0', key)
    unit = lut.loc[key]
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 1
    melee_wt.loc[key, 'is_magical'] = True
    copy_missile_weapon(unit['primary_missile_weapon'], key)
    lut.loc[key, 'primary_missile_weapon'] = key
    pt.loc[key, 'damage'] = 0
    pt.loc[key, 'ap_damage'] = 1000
    pt.loc[key, 'bonus_v_infantry'] = 0
    pt.loc[key, 'bonus_v_large'] = 0
    pt.loc[key, 'calibration_area'] = 0.5
    pt.loc[key, 'explosion_type'] = None
    pt.loc[key, 'ignition_amount'] = 1
    pt.loc[key, 'is_magical'] = True
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    # MISSILE ATTACK EXPLOSION ONLY
    key = 'gmtm_modattack_explosion_regular'
    copy_unit('wh3_main_kho_veh_skullcannon_0', key)
    unit = lut.loc[key]
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 0
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    copy_missile_weapon(unit['primary_missile_weapon'], key)
    lut.loc[key, 'primary_missile_weapon'] = key
    pt.loc[key, 'damage'] = 0
    pt.loc[key, 'ap_damage'] = 1
    pt.loc[key, 'bonus_v_infantry'] = 0
    pt.loc[key, 'bonus_v_large'] = 0
    pt.loc[key, 'calibration_area'] = 0.5
    pt.loc[key, 'ignition_amount'] = 0
    pt.loc[key, 'is_magical'] = False
    copy_projectile_explosion(pt.loc[key, 'explosion_type'], key)
    pt.loc[key, 'explosion_type'] = key
    pet.loc[key, 'detonation_radius'] = 5
    pet.loc[key, 'detonation_damage'] = 0
    pet.loc[key, 'detonation_damage_ap'] = 1000
    pet.loc[key, 'ignition_amount'] = 0
    pet.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)


    # POISON MORTARS
    key = 'gmtm_poison_wind_mortar_0'
    copy_unit('wh2_dlc14_skv_inf_poison_wind_mortar_0', key)
    unit = lut.loc[key]
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 0
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    copy_missile_weapon(unit['primary_missile_weapon'], key)
    lut.loc[key, 'primary_missile_weapon'] = key
    pt.loc[key, 'damage'] = 0
    pt.loc[key, 'ap_damage'] = 1
    pt.loc[key, 'bonus_v_infantry'] = 0
    pt.loc[key, 'bonus_v_large'] = 0
    pt.loc[key, 'calibration_area'] = 0.5
    pt.loc[key, 'ignition_amount'] = 0
    pt.loc[key, 'is_magical'] = False
    copy_projectile_explosion(pt.loc[key, 'explosion_type'], key)
    pt.loc[key, 'explosion_type'] = key
    pet.loc[key, 'detonation_radius'] = 5
    pet.loc[key, 'detonation_damage'] = 0
    pet.loc[key, 'detonation_damage_ap'] = 0
    pet.loc[key, 'ignition_amount'] = 0
    pet.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)


    # ARK OF SOTEK
    key = 'gmtm_ark_of_sotek'
    copy_unit('wh2_dlc12_lzd_mon_bastiladon_3', key)
    unit = lut.loc[key]
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 0
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    lutuajt.loc[key] = {'land_unit': key, 'ability': 'wh2_dlc12_unit_abilities_ark_of_sotek'}
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    #ACCURACY
    accuracy_base_unit_key = 'wh_main_emp_art_mortar'

    accuracy_keys = []

    for accuracy in range(9, 80, 10):
        akey = f'gmtm_ability_accuracy_{accuracy}'
        copy_ability('wh_dlc05_unit_abilities_the_shadows_coil', akey)
        phase_key = akey+'_0'
        sapset.loc[phase_key] = {'phase': phase_key, 'stat': 'stat_accuracy', 'value': accuracy, 'how': 'add'}
        accuracy_keys.append(akey)


    key = 'gmtm_accuracy_base'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 0
    pt.loc[key, 'calibration_area'] = 40
    pt.loc[key, 'calibration_distance'] = 400
    pt.loc[key, 'effective_range'] = 400
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_acc_10_mm_10'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 10
    pt.loc[key, 'marksmanship_bonus'] = 10
    pt.loc[key, 'calibration_area'] = 40
    pt.loc[key, 'calibration_distance'] = 400
    pt.loc[key, 'effective_range'] = 400
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    # for akey in accuracy_keys:
    #     lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_area_10'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 0
    pt.loc[key, 'calibration_area'] = 10
    pt.loc[key, 'calibration_distance'] = 400
    pt.loc[key, 'effective_range'] = 400
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_area_100'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 0
    pt.loc[key, 'calibration_area'] = 100
    pt.loc[key, 'calibration_distance'] = 400
    pt.loc[key, 'effective_range'] = 400
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_distance_100'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 0
    pt.loc[key, 'calibration_area'] = 40
    pt.loc[key, 'calibration_distance'] = 100
    pt.loc[key, 'effective_range'] = 400
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_distance_1000'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 0
    pt.loc[key, 'calibration_area'] = 40
    pt.loc[key, 'calibration_distance'] = 1000
    pt.loc[key, 'effective_range'] = 400
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_range_300'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 0
    pt.loc[key, 'calibration_area'] = 40
    pt.loc[key, 'calibration_distance'] = 400
    pt.loc[key, 'effective_range'] = 300
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_range_1200'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 0
    pt.loc[key, 'calibration_area'] = 40
    pt.loc[key, 'calibration_distance'] = 400
    pt.loc[key, 'effective_range'] = 1200
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}

    key = 'gmtm_accuracy_mmbonus_49'
    unit = copy_unit(accuracy_base_unit_key, key)
    copy_engine(unit['engine'], key)
    lut.loc[key, 'engine'] = key
    lut.loc[key, 'accuracy'] = 1
    pt.loc[key, 'marksmanship_bonus'] = 49
    pt.loc[key, 'calibration_area'] = 40
    pt.loc[key, 'calibration_distance'] = 400
    pt.loc[key, 'effective_range'] = 400
    pt.loc[key, 'base_reload_time'] = 8.0
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)
    for akey in accuracy_keys:
        lutuajt.loc[key + '_' + akey] = {'land_unit': key, 'ability': akey}


    #SPLASH ATTACK
    key = 'gmtm_splash_attack'
    copy_unit('wh3_main_cth_mon_terracotta_sentinel_0', key)
    unit = lut.loc[key]
    lut.loc[key, 'melee_attack'] = 200
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'medium'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 10
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False


    #COLLISION_DAMAGE
    key = 'gmtm_collision_damage'
    copy_unit('wh3_main_sla_veh_exalted_seeker_chariot_0', key)
    unit = lut.loc[key]
    lut.loc[key, 'melee_attack'] = 0
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'medium'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets_cooldown'] = 0
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 0
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    #COLLISION_ATTACK
    key = 'gmtm_collision_attack_0_dmg'
    copy_unit('wh3_main_ogr_mon_stonehorn_0', key)
    unit = lut.loc[key]
    lut.loc[key, 'melee_attack'] = 200
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'medium'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets'] = 4
    melee_wt.loc[key, 'collision_attack_max_targets_cooldown'] = 4
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 0
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_collision_attack_default'
    copy_unit('wh3_main_ogr_mon_stonehorn_0', key)
    unit = lut.loc[key]
    lut.loc[key, 'melee_attack'] = 200
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'medium'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_collision_attack_high_cooldown'
    copy_unit('wh3_main_ogr_mon_stonehorn_0', key)
    unit = lut.loc[key]
    lut.loc[key, 'melee_attack'] = 200
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'medium'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets'] = 4
    melee_wt.loc[key, 'collision_attack_max_targets_cooldown'] = 10
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)

    key = 'gmtm_collision_attack_low_cooldown'
    copy_unit('wh3_main_ogr_mon_stonehorn_0', key)
    unit = lut.loc[key]
    lut.loc[key, 'melee_attack'] = 200
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'medium'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets'] = 4
    melee_wt.loc[key, 'collision_attack_max_targets_cooldown'] = 1
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 1000
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)


    #CHARGE BONUS
    key = 'gmtm_charge_bonus'
    copy_unit('wh3_main_ksl_cha_patriarch_1', key)
    unit = lut.loc[key]
    lut.loc[key, 'melee_attack'] = 0
    lut.loc[key, 'charge_bonus'] = 0
    copy_melee_weapon(unit['primary_melee_weapon'], key)
    lut.loc[key, 'primary_melee_weapon'] = key
    melee_wt.loc[key, 'splash_attack_target_size'] = 'medium'
    melee_wt.loc[key, 'splash_attack_max_attacks'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets'] = 0
    melee_wt.loc[key, 'collision_attack_max_targets_cooldown'] = 0
    melee_wt.loc[key, 'damage'] = 0
    melee_wt.loc[key, 'ap_damage'] = 0
    melee_wt.loc[key, 'bonus_v_infantry'] = 0
    melee_wt.loc[key, 'bonus_v_large'] = 0
    melee_wt.loc[key, 'ignition_amount'] = 0
    melee_wt.loc[key, 'is_magical'] = False
    akey = 'gmtm_ability_flat_charge_bonus'
    copy_ability('wh3_main_character_abilities_ursuns_roar', akey)
    lutuajt.loc[key] = {'land_unit': key, 'ability': akey}
    usat.loc[akey, 'active_time'] = 20
    usat.loc[akey, 'recharge_time'] = 5
    phase_key = akey+'_0'
    sapset.loc[phase_key] = {'phase': phase_key, 'stat': 'stat_charge_bonus', 'value': 300, 'how': 'add'}
    generate_unit_bullet_point(hh, formatter, uubpet, uubpuot, bp_text_loc, key)


    # KAiros MAX MANA TEST
    phase_key = 'wh3_main_item_abilities_scroll_of_destiny'
    sability = handler.db['unit_special_abilities_tables'].data.loc[phase_key].to_dict()
    sability['active_time'] = 1
    sability['recharge_time'] = 1
    sability['num_uses'] = -1
    usat.loc[phase_key] = sability
    phase = handler.db['special_ability_phases_tables'].data.loc[phase_key].to_dict()
    phase['duration'] = 1
    phase['mana_max_depletion_mod'] = 1.1
    sapt.loc[phase_key] = phase




if __name__ == '__main__':
    MOD_NAME = 'Klissan_GMTM'
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

    create_faction(hh)
    kv_rules(hh)
    add_content(hh, formatter)

    handler.dump_mod_tables(OUTPUT_DIR)
    rpfm.make_package(MOD_NAME, OUTPUT_DIR)
    pass