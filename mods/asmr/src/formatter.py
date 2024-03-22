import math

def _icon(name):
    return f"[[img:ui/skins/default/{name}.png]][[/img]]"

def _icon_battle(name):
    return f"[[img:ui/battle ui/ability_icons/{name}.png]][[/img]]"

def _indentstr(indent:int):
    if indent == 0:
        return ''
    return f"[[col:]]{' '*indent}[[/col]]"


beautify = lambda name: ' '.join([s.capitalize() for s in name.split('_')[2:]])

class Formatter:

    def __init__(self, handler_helper, localizator, army_size: str, debug:bool=False):
        self.endl = '\\\\n'
        self.indent_step = 2

        self.army_size_coeffs = {
            'small': {'direct_dmg': None, 'hp': 0.25},
            'medium': {'direct_dmg': None, 'hp': 0.5},
            'large': {'direct_dmg': 0.92, 'hp': 0.75},
            'ultra': {'direct_dmg': 1.0, 'hp': 1.0},
        }
        self.colors = {'red', 'green', 'blue', 'yellow', 'dark_r', 'dark_g', 'dark_y',
                       'magic',
                       'ancillary_uncommon',
                       'ancillary_crafted',
                       'ancillary_rare'
                       'ancillary_unique',
                       'help_page_link',
                       'fatigue_tired',
                       'fatigue_winded'}
        self.icon = {
            "scalar_bracing": _icon("icon_stat_bracing"),
            "scalar_charge_speed": "[[img:ui/campaign ui/effect_bundles/charge.png]][[/img]]",
            "scalar_dealt_collision_knocked_back_threshold_modifier": "collision_knocked_back_th_mod",
            "scalar_dealt_collision_knocked_down_threshold_modifier": "collision_knocked_down_th_mod",
            "scalar_dealt_collision_knocked_flying_threshold_modifier": "collision_knocked_flying_th_mod",
            "scalar_entity_acceleration_modifier": _icon("icon_stat_speed"),
            "scalar_entity_deceleration_modifier": _icon("icon_stat_speed"),
            "scalar_miscast_chance": "miscast_chance",
            "scalar_missile_damage_ap": _icon("modifier_icon_armour_piercing_ranged"),
            "scalar_missile_damage_base": _icon("icon_stat_ranged_damage_base"),
            "scalar_missile_explosion_damage_ap": _icon("icon_stat_explosive_armour_piercing_damage"),
            "scalar_missile_explosion_damage_base": _icon("icon_explosive_damage"),
            "scalar_missile_range": _icon("icon_stat_range"),
            "scalar_speed": _icon("icon_stat_speed"),
            "scalar_splash_attack_power": "splash_attack_power",
            "stat_accuracy": "[[img:ui/campaign ui/effect_bundles/accuracy_character.png]][[/img]]",
            "stat_armour": _icon("icon_stat_armour"),
            "stat_bonus_vs_cavalry": "bonus_vs_cavalry",
            "stat_bonus_vs_infantry": _icon("modifier_icon_bonus_vs_infantry"),
            "stat_bonus_vs_large": _icon("modifier_icon_bonus_vs_large"),
            "stat_charge_bonus": _icon("icon_stat_charge_bonus"),
            "stat_first_strike": "first_strike",
            "stat_mana": _icon("icon_mana"),
            "stat_melee_attack": _icon("icon_stat_attack"),
            "stat_melee_damage_ap": _icon("modifier_icon_armour_piercing"),
            "stat_melee_damage_base": _icon("icon_stat_damage_base"),
            "stat_melee_defence": _icon("icon_stat_defence"),
            "stat_miscast_additional": "miscast_additional",
            "stat_missile_block_chance": "missile_block_chance",
            "stat_morale": _icon("icon_stat_morale"),
            "stat_num_uses_additional": "num_uses_additional",
            "stat_reloading": _icon("icon_stat_reload_time"),
            "stat_resistance_all": "[[img:ui/campaign ui/effect_bundles/resistance_ward_save.png]][[/img]]",
            "stat_resistance_flame": "[[img:ui/campaign ui/effect_bundles/resistance_fire.png]][[/img]]",
            "stat_resistance_magic": "[[img:ui/campaign ui/effect_bundles/resistance_magic.png]][[/img]]",
            "stat_resistance_missile": "[[img:ui/campaign ui/effect_bundles/resistance_missile.png]][[/img]]",
            "stat_resistance_physical": "[[img:ui/campaign ui/effect_bundles/resistance_physical.png]][[/img]]",
            "stat_shield_armour": "shield_armour",
            "stat_shield_defence": "shield_defence",
            "stat_spotting_forest": "[[img:ui/battle ui/ability_icons/wh2_dlc16_character_abilities_tree_spotting.png]][[/img]]",
            "stat_spotting_scrub": "[[img:ui/battle ui/ability_icons/hide_scrub_and_forest.png]][[/img]]",
            "stat_visibility_sight": "[[img:ui/battle ui/ability_icons/wh_dlc05_lord_passive_sight_beyond_sight.png]][[/img]]",
            "stat_weakness_flame": "[[img:ui/skins/default/modifier_icon_flammable.png]][[/img]]",
            "mass": _icon("icon_stat_mass"),
            "mod_magical": _icon("modifier_icon_magical"),
            "mod_flaming": _icon("modifier_icon_flaming"),

            "cooldown": _icon("icon_cooldown"),
            "buff": _icon(('arrow_increase_1')),
            "debuff": _icon(('arrow_decrease_1')),
            "high_threat": _icon('icon_status_alert_high_24px'),

            'entity_large': _icon('icon_entity_large'),
            'entity_small': _icon('icon_entity_small'),

            'unbinding_stage1': _icon('icon_ability_unbinding_stage1'),
            'unbinding_stage2': _icon('icon_ability_unbinding_stage2'),
            'unbinding_stage3': _icon('icon_ability_unbinding_stage3'),


            'stat_ranged_damage': _icon('icon_stat_ranged_damage'),
            'distance': _icon('icon_distance_to_target'),
            'ammo': _icon('icon_stat_ammo'),
            'resurrect': "[[img:ui/battle ui/ability_icons/undead.png]][[/img]]", #wh_main_spell_light_light_of_battle
            'ignores_shields': _icon('modifier_icon_armour_break'),
            'no_friendly_fire': "[[img:ui/battle ui/ability_icons/wh_dlc07_unit_passive_icon_of_devotion.png]][[/img]]",
            'self_guided': "[[img:ui/battle ui/ability_icons/snipe.png]][[/img]]",


            'mana': _icon('icon_mana'),
            'hp': _icon("icon_stat_health_noframe_16px"),
            "barrier": "[[img:ui/campaign ui/effect_bundles/barrier.png]][[/img]]",
            "fatigue": _icon("fatigue"),
            "engine": _icon('icon_continue_siege'),
            "splash_attack": "[[img:ui/battle ui/ability_icons/wh2_dlc10_lord_passive_blood_frenzy.png]][[/img]]",
            "collision_attack": "[[img:ui/battle ui/ability_icons/wh_dlc03_unit_passive_primal_fury.png]][[/img]]",
            "uses": _icon("icon_uses"),
            "melee_dmg": _icon("icon_stat_damage"),

            'burst_size': _icon('modifier_icon_suppressive_fire'),
            'shots_per_volley': "[[img:ui/battle ui/ability_icons/wh2_main_character_passive_darken_the_skies.png]][[/img]]",
            'n_projectiles': "[[img:ui/battle ui/ability_icons/wh2_dlc11_unit_passive_extra_powder.png]][[/img]]",

            'mp_cost': _icon('icon_income'),
            'many_models': "[[img:ui/campaign ui/stance_icons/military_force_active_stance_type_march.png]][[/img]]",
            'more_stats' : _icon('arrow_increase_2'),

            'infinite_height': "[[img:ui/battle ui/ability_icons/wh2_dlc15_unit_abilities_emberstorm.png]][[/img]]",
        }

        self.hhelper = handler_helper
        self.loctr = localizator
        self.army_size = army_size
        self.debug = debug

        self.contact_effect_map = {}


    def _add_contact_effect_to_map(self, iid, effect_id):
        if not iid in self.contact_effect_map:
            self.contact_effect_map[iid] = set()
        self.contact_effect_map[iid].add(effect_id)

    def _restore_shared_fields(self):
        self.reload_skill = None
        self.primary_melee = None
        self.primary_missile = None
        self.primary_ammo = None
        self.secondary_ammo = None
        self.spawn_unit = None
        self.n_entities = None

    def colorize(self, text, color):
        return f"[[col:{color}]]" + str(text) + "[[/col]]"

    def make_text_white(self, desc):
        if len(desc) == 0:
            return desc
        # if desc[-3:] == self.endl:
        #     desc = desc[:-3]
        return self.colorize(desc, 'white')

    #test if works
    def test_colorize_rgb(self):
        return "" + self.endl \
                + "[[rgba:99:0:0:99]]" + "TEST" + "[[/rgba:99:0:0:99]]" + self.endl \
               + f"[[rgba:99:0:0:99]]" + "TEST" + "[[/rgba]]" + self.endl \
               + f"[[rgb:99:0:0]]" + "TEST" + "[[/rgb:99:0:0]]" + self.endl \
               + f"[[rgb:99:0:0]]" + "TEST" + "[[/rgb]]" + self.endl

    def highlight(self, text):
        return self.colorize(text, 'yellow')

    def title(self, text):
        return self.colorize(text, 'white') #blue


    def _res(self, plus, minus=0):
        res = plus + minus
        if res < 0:
            return self.colorize(abs(res), 'red')
        if res > 0:
            return self.colorize(res, 'green')
        return str(res)

    def _armour_perc(self, armour):
        if armour >= 200:
            return "100"
        if armour <= 100:
            return f"{0.75 * armour:.0f}"
        half = armour * 0.5
        diff = armour - half
        lh, rh = 100 - half, armour - 100
        res = (lh / diff) * (half+100)/2 + (rh / diff) * 100
        return f"{res:.0f}"

    def _get_hp_per_model(self, main_unit, land_unit=None):
        if land_unit is None:
            land_unit = main_unit['land_unit']
        hp = land_unit['man_entity']['hit_points']
        bhp = land_unit['bonus_hit_points']
        articulated_hp = land_unit['articulated_record']['articulated_entity']['hit_points'] if not self.hhelper.handler.isnull(land_unit['articulated_record']) else 0

        mhp = 0
        if not self.hhelper.handler.isnull(land_unit['mount']):
            if land_unit['category'] == 'war_machine':
                engine_hp = land_unit['engine']['battle_entity']['hit_points'] if land_unit['engine'] is not None else 0
                mhp = land_unit['num_mounts'] * land_unit['mount']['entity']['hit_points'] + engine_hp
            else:
                mhp = land_unit['mount']['entity']['hit_points']

        personas_hp = 0
        if land_unit['battle_personalities'] is not None:
            for persona_info in land_unit['battle_personalities']:
                if not self.hhelper.handler.isnull(persona_info['battle_personality']['battle_entity_stats']):
                # if not self.handler.handler.isnull(persona_info['battle_personality']['battle_entity']):
                    personas_hp += persona_info['battle_personality']['battle_entity']['hit_points']

        total_hp = hp + bhp + mhp + articulated_hp + personas_hp
        if main_unit['use_hitpoints_in_campaign']:
            total_hp = math.ceil(total_hp * self.army_size_coeffs[self.army_size]['hp'])
        return str(total_hp)

    def _melee_attack_short(self, land_unit):
        shortener = lambda x: ''.join([e[0].capitalize() for e in x.split('_')])
        melee_weapon = self.hhelper.get_melee_info(land_unit['primary_melee_weapon'])
        attack_vs_inf = f" {self.icon['stat_bonus_vs_infantry']}{land_unit['melee_attack'] + melee_weapon['bonus_v_infantry']}" if melee_weapon['bonus_v_infantry'] != 0 else ""
        attack_vs_large = f" {self.icon['stat_bonus_vs_large']}{land_unit['melee_attack'] + melee_weapon['bonus_v_large']}" if melee_weapon['bonus_v_large'] != 0 else ""
        splash_attack = f" {self.icon['splash_attack']}{self.loctr.add_auto('entity_size_short', melee_weapon['splash_attack_target_size'], auto_formatter=shortener)} {melee_weapon['splash_attack_max_attacks']}" if not str(melee_weapon['splash_attack_target_size']) == 'nan' else ""
        collision_attack = f" {self.icon['collision_attack']}{melee_weapon['collision_attack_max_targets']}{self.icon['uses']}{melee_weapon['collision_attack_max_targets_cooldown']}" if not melee_weapon['collision_attack_max_targets'] == 0 else ""

        desc = f"{self.icon['stat_melee_attack']}{land_unit['melee_attack']}" + \
                attack_vs_inf +\
                attack_vs_large +\
                splash_attack +\
                collision_attack +\
                self.endl
        return desc

    def _melee_dmg(self, melee_weapon):
        melee_weapon = self.hhelper.get_melee_info(melee_weapon)
        base_vs_inf, ap_vs_inf, _ = self._add_bonus(melee_weapon['damage'], melee_weapon['ap_damage'], melee_weapon['bonus_v_infantry'])
        base_vs_large, ap_vs_large, _ = self._add_bonus(melee_weapon['damage'], melee_weapon['ap_damage'], melee_weapon['bonus_v_large'])

        fire_str = f"{self.icon['mod_flaming']}" if melee_weapon['ignition_amount'] > 0 else ""
        magic_str = f"{self.icon['mod_magical']} " if melee_weapon['is_magical'] else ""

        desc = f"{fire_str}{magic_str}"
        if len(desc) != 0:
            desc += ' '
        desc += f"{self.icon['stat_melee_damage_base']}{melee_weapon['damage']}{self.icon['stat_melee_damage_ap']}{melee_weapon['ap_damage']}"

        if melee_weapon['bonus_v_infantry'] != 0:
            if base_vs_inf < 100 and ap_vs_inf < 100:
                desc += f" {self.icon['stat_bonus_vs_infantry']}{self.icon['stat_melee_damage_base']}{base_vs_inf}{self.icon['stat_melee_damage_ap']}{ap_vs_inf}"
            else:
                desc += f" {self.icon['stat_bonus_vs_infantry']}{melee_weapon['bonus_v_infantry']}"
        if melee_weapon['bonus_v_large'] != 0:
            if base_vs_large < 100 and ap_vs_large < 100:
                desc += f" {self.icon['stat_bonus_vs_large']}{self.icon['stat_melee_damage_base']}{base_vs_large}{self.icon['stat_melee_damage_ap']}{ap_vs_large}"
            else:
                desc += f" {self.icon['stat_bonus_vs_large']}{melee_weapon['bonus_v_large']}"
        return desc + self.endl

    def _range_dmg_short(self, projectile):
        explosion = self.hhelper.get_explosion_info(projectile['explosion_type'])
        base_vs_inf, ap_vs_inf, _ = self._add_bonus(projectile['damage'], projectile['ap_damage'], projectile['bonus_v_infantry'])
        base_vs_large, ap_vs_large, _ = self._add_bonus(projectile['damage'], projectile['ap_damage'], projectile['bonus_v_large'])

        fire_str = f"{self.icon['mod_flaming']}" if projectile['ignition_amount'] > 0 else ""
        magic_str = f"{self.icon['mod_magical']} " if projectile['is_magical'] else ""

        desc = f"{fire_str}{magic_str}"
        if len(desc) != 0:
            desc += ' '

        desc += f"{self.icon['scalar_missile_damage_base']}{projectile['damage']}" + \
               f"{self.icon['scalar_missile_damage_ap']}{projectile['ap_damage']}"

        if projectile['bonus_v_infantry'] != 0:
            if True: #base_vs_inf < 100 and ap_vs_inf < 100:
                desc += f" {self.icon['stat_bonus_vs_infantry']}{self.icon['stat_melee_damage_base']}{base_vs_inf}{self.icon['stat_melee_damage_ap']}{ap_vs_inf}"
            else:
                desc += f" {self.icon['stat_bonus_vs_infantry']}{projectile['bonus_v_infantry']}"
        if projectile['bonus_v_large'] != 0:
            if True: #base_vs_large < 100 and ap_vs_large < 100:
                desc += f" {self.icon['stat_bonus_vs_large']}{self.icon['stat_melee_damage_base']}{base_vs_large}{self.icon['stat_melee_damage_ap']}{ap_vs_large}"
            else:
                desc += f" {self.icon['stat_bonus_vs_large']}{projectile['bonus_v_large']}"

        desc += self.endl
        if explosion is not None:
               desc += f" {self.icon['scalar_missile_explosion_damage_base']}{int(explosion['detonation_damage'])}" + \
                       f"{self.icon['scalar_missile_explosion_damage_ap']}{int(explosion['detonation_damage_ap'])}" + \
                       f" {self.icon['distance']}{int(explosion['detonation_radius'])}"

        if projectile['burst_size'] != 1:
               desc += f" {self.icon['burst_size']}{projectile['burst_size']}"

        if projectile['shots_per_volley'] != 1:
               desc += f" {self.icon['shots_per_volley']}{projectile['shots_per_volley']}"

        if projectile['projectile_number'] != 1:
               desc += f" {self.icon['n_projectiles']}{projectile['projectile_number']}"

        if self.reload_skill is not None:
            reload_time = projectile['base_reload_time'] * (100-self.reload_skill) / 100
            reload_time_str = f"{reload_time:.1f}"
            desc += f" {self.icon['stat_reloading']}{reload_time_str}"
        return desc


    def has_scaling_damage(self, unit_info):
        melee_weeapon = self.hhelper.get_melee_info(unit_info['land_unit']['primary_melee_weapon'])
        missile_weeapon = self.hhelper.get_missile_info(unit_info['land_unit']['primary_missile_weapon'])
        projectile = None
        if not self.hhelper.handler.isnull(missile_weeapon):
            projectile = self.hhelper.get_projectile_info(missile_weeapon['default_projectile'])
        # has = melee_weeapon['scaling_damage'] is not None or (projectile is not None and projectile['scaling_damage'] is not None)
        has = not self.hhelper.handler.isnull(melee_weeapon['scaling_damage']) or (projectile is not None and not self.hhelper.handler.isnull(projectile['scaling_damage']))
        return has

    def _engine_str(self, engine):
        engine_str = ''
        if not self.hhelper.handler.isnull(engine):
            ehp = engine['battle_entity']['hit_points']
            if ehp > 8:
                engine_str = f" {self.icon['engine']}{str(ehp)}"
        return engine_str

# entrypoint
    def get_short_unit_desc(self, info):
        self._restore_shared_fields()
        desc = ''
        info['land_unit'] = self.hhelper.get_land_unit_info(info['land_unit'])
        self.reload_skill = info['land_unit']['reload']
        barrier_str = f" {self.icon['barrier']}{round(info['barrier_health'])}" if info['barrier_health'] > 0 else ""
        engine_str = self._engine_str(info['land_unit']['engine'])
        additional_info_str = ""
        if info['land_unit']['battle_personalities_grouped'] is not None or self.has_scaling_damage(info):
            additional_info_str = f" {self.icon['more_stats']}"

        desc += f"{self.icon['mp_cost']}{info['multiplayer_cost']}" + \
                f" {_icon('icon_capture_point')}{round(float(info['land_unit']['score_capture_tier']['power']))}" + \
                f" {self.icon['hp']}{self._get_hp_per_model(info)}" + \
                barrier_str + \
                engine_str + \
                additional_info_str + \
                self.endl

        desc += self._get_resistances(info['land_unit']) + self._format_shield(info['land_unit']['shield']) + self.endl

        desc += self._melee_attack_short(info['land_unit'])
        desc += self._melee_dmg(info['land_unit']['primary_melee_weapon'])

        if not self.hhelper.handler.isnull(info['land_unit']['primary_missile_weapon']):
            missile_weeapon = self.hhelper.get_missile_info(info['land_unit']['primary_missile_weapon'])
            projectile = self.hhelper.get_projectile_info(missile_weeapon['default_projectile'])
            desc += self._range_dmg_short(projectile)
        else:
            if not self.hhelper.handler.isnull(info['land_unit']['engine']) and \
                    not self.hhelper.handler.isnull(info['land_unit']['engine']['missile_weapon']):
                missile_weeapon = self.hhelper.get_missile_info(info['land_unit']['engine']['missile_weapon'])
                projectile = self.hhelper.get_projectile_info(missile_weeapon['default_projectile'])
                desc += self._range_dmg_short(projectile)

        # add empty line
        if self.hhelper.handler.isnull(info['land_unit']['primary_missile_weapon']) and self.hhelper.handler.isnull(info['land_unit']['engine']):
            desc += self.endl

        # if info['land_unit']['officers'] is not None:
        #     personas = info['land_unit']['officers']['additional_personalities']
        #     personas_info = self.handler._group_additional_personalities(personas)
        #     if personas_info is not None:
        #         print('==========', info['unit'])
        #         print(personas_info)
        return self.make_text_white(desc)

    def beatify_unit_id(self, name):
        return ' '.join([s.capitalize() for s in name.split('_')[3:]])

    def _get_resistances(self, info):
        desc = f"{self.icon['stat_resistance_all']}{self._res(info['damage_mod_all'])}" + \
               f" {self.icon['stat_resistance_physical']}{self._res(info['damage_mod_physical'])}" + \
               f" {self.icon['stat_resistance_magic']}{self._res(info['damage_mod_magic'])}" + \
               f" {self.icon['stat_resistance_missile']}{self._res(info['damage_mod_missile'])}" + \
               f" {self.icon['stat_resistance_flame']}{self._res(info['damage_mod_flame'])}" + \
               f" {self.icon['stat_armour']}{self._armour_perc(info['armour']['armour_value'])}"
        return desc

    def __get_unit_size(self, main_unit_info, land_unit_info, get_crew=True):
        size = land_unit_info['man_entity']['size']
        num_men = main_unit_info['num_men']
        if not self.hhelper.handler.isnull(land_unit_info['mount']):
            size = land_unit_info['mount']['entity']['size']
            num_men = land_unit_info['num_mounts']
        if not self.hhelper.handler.isnull(land_unit_info['engine']):
            if land_unit_info['engine']['battle_entity']['hit_points'] == 8 or not get_crew:
                size = land_unit_info['engine']['battle_entity']['size']
                num_men = land_unit_info['num_engines']
            else: # artillery crew
                size = land_unit_info['man_entity']['size']
                num_men = main_unit_info['num_men']
        if main_unit_info['use_hitpoints_in_campaign']:
            num_men = round(num_men * self.army_size_coeffs[self.army_size]['hp'])
        if size in {'very_small', 'small'}:
            icon = self.icon['entity_small']
        if size in {'medium', 'large', 'very_large'}:
            icon = self.icon['entity_large']
        return icon, size, num_men

    def _get_unit_size(self, main_unit_info, land_unit_info):
        icon, size, num_men = self.__get_unit_size(main_unit_info, land_unit_info)
        desc = f" {icon}{self.highlight(self.loctr.add_auto('entity_size', size))} {int(num_men)}"
        return desc

    def _format_mass(self, land_unit_info):
        entity_info = land_unit_info['man_entity']
        mass = entity_info['mass']
        if not self.hhelper.handler.isnull(land_unit_info['mount']):
            mass += land_unit_info['mount']['entity']['mass']
        if not self.hhelper.handler.isnull(land_unit_info['engine']):
            mass += land_unit_info['engine']['battle_entity']['mass']
        mass_str = f"{self.icon['mass']}{self.loctr.tr('mass')}: {self.highlight(round(mass))}"
        return mass_str

    def _format_speed(self, land_unit_info):
        entity_info = land_unit_info['man_entity']
        if not self.hhelper.handler.isnull(land_unit_info['mount']):
            entity_info = land_unit_info['mount']['entity']
        speed_str = f"{self.icon['scalar_speed']}{entity_info['run_speed']} {self.icon['scalar_charge_speed']}{entity_info['charge_speed']}"
        if entity_info['fly_speed'] > 0:
            speed_str += f" {_icon_battle('flying')}{self.icon['scalar_speed']}{entity_info['fly_speed']} {_icon_battle('flying')}{self.icon['scalar_charge_speed']}{entity_info['flying_charge_speed']}"
        return speed_str

    def _has_strider_attr(self, attributes):
        if attributes is None:
            return False
        for attr in attributes:
            if attr['attribute'] == 'strider':
                return True
        return False

    def _format_ground_effects(self, affected_group, has_strider:bool, indent:int=0) -> str:
        if has_strider:
            return _indentstr(indent) + f"{self.loctr.tr('ground_effect')} - {_icon_battle('strider')}{self.highlight(self.loctr.tr('strider'))}" + self.endl
        ground_effects = self.hhelper.get_ground_effects(affected_group)
        ground_str = _indentstr(indent) + f"{self.loctr.tr('ground_effect')} - {self.highlight(self.loctr.add_auto('ground_effect', affected_group))}:"
        for ground_type, stat_effects in ground_effects.items():
            ground_str += self.endl + _indentstr(indent + self.indent_step) + f"{self.loctr.add_auto('ground_type', ground_type)}:"
            for se, mult in stat_effects.items():
                value = str(round((mult - 1) * 100)) + '%'
                value_format = self.colorize('+'+value, 'green') if mult > 1.0 else self.colorize(value, 'red')
                ground_str += f" {self.icon[se]}{value_format}"
        return ground_str + self.endl

    def _format_shield(self, shield_info) -> str:
        mbc = shield_info['missile_block_chance']
        if mbc == 0:
            return ''
        shield_str = ' '
        shield_str += _icon('modifier_icon_shield1') if mbc < 55 else _icon('modifier_icon_shield2')
        shield_str += f"{mbc}"
        return shield_str

    def _format_land_unit_info(self, info, main_unit_info=None, indent=0):
        desc = ''
        barrier_str = f" {self.icon['barrier']}{round(main_unit_info['barrier_health'])}" if main_unit_info['barrier_health'] > 0 else ""
        engine_str = self._engine_str(info['engine'])
        if main_unit_info is not None:
            desc += _indentstr(indent) +  \
                f"{self.icon['mp_cost']}{main_unit_info['multiplayer_cost']}" + \
                self._get_unit_size(main_unit_info, info) + \
                    f" {self.icon['hp']}{self._get_hp_per_model(main_unit_info, info)}" + \
                    barrier_str + engine_str + self.endl

        land_unit = info
        weapon = self.hhelper.get_melee_info(land_unit['primary_melee_weapon'])
        vs_inf = weapon['bonus_v_infantry']
        vs_large = weapon['bonus_v_large']

        desc += _indentstr(indent) + self._get_resistances(info) + self._format_shield(info['shield']) + self.endl
        desc += _indentstr(indent) + self._format_speed(land_unit) + self.endl
        desc += _indentstr(indent) + self._format_mass(land_unit) + self.endl
        desc += _indentstr(indent) + f"{self.icon['stat_melee_attack']}{self.loctr.tr('melee_attack')}: {self.highlight(land_unit['melee_attack'])}"
        if vs_inf > 0:
            desc += f" {self.icon['stat_bonus_vs_infantry']}{self.highlight(land_unit['melee_attack']+vs_inf)}"
        if vs_large > 0:
            desc += f" {self.icon['stat_bonus_vs_large']}{self.highlight(land_unit['melee_attack']+vs_large)}"
        desc += self.endl
        desc += _indentstr(indent) + f"{self.icon['stat_melee_defence']}{self.loctr.tr('melee_defence')}: {self.highlight(land_unit['melee_defence'])}" + self.endl
        desc += _indentstr(indent) + f"{self.icon['stat_charge_bonus']}{self.loctr.tr('charge_bonus')}: {self.highlight(land_unit['charge_bonus'])}" + self.endl
        desc += _indentstr(indent) + f"{_icon('icon_capture_point')}{self.loctr.add_auto('dom_capture_tier', info['score_capture_tier']['__value__'])}: {self.highlight(info['score_capture_tier']['power'])}" + self.endl

        if land_unit['hiding_scalar'] < 1.0:
            desc += _indentstr(indent) + f"{self.loctr.tr('hiding_modifier')}: {self.highlight(round(float(land_unit['hiding_scalar']), 1))}" + self.endl

        if land_unit['spot_dist_tree'] != 60 or land_unit['spot_dist_scrub'] != 80:
            spot_dist_str = f"{self.loctr.tr('spot_distance')}:"
            if land_unit['spot_dist_tree'] != 60:
                spot_dist_str += f" {self.loctr.tr('spot_tree')} {self.highlight(land_unit['spot_dist_tree'])}"
            if land_unit['spot_dist_scrub'] != 80:
                spot_dist_str += f" {self.loctr.tr('spot_scrub')} {self.highlight(land_unit['spot_dist_scrub'])}"
            desc += _indentstr(indent) + spot_dist_str + self.endl

        desc += self._format_ground_effects(info['ground_stat_effect_group'], self._has_strider_attr(info['attribute_group']))
        return desc

    def _get_unit_abilities_icons(self, attributes, abilities, indent=0):
        if abilities is None:
            return ''
        desc = ''
        if attributes is not None:
            for attr in attributes:
                desc += _icon_battle(attr['attribute']) + ' '
        if abilities is not None:
            for abil in abilities:
                info = self.hhelper.get_ability_info(abil['ability'])
                desc += _icon_battle(info['icon_name']) + ' '
        return _indentstr(indent) + desc + self.endl

    def _get_unit_unbinding(self, abilities, indent=0):
        if abilities is None:
            return ''
        strs = []
        for abil in abilities:
            info = self.hhelper.get_ability_info(abil['ability'])
            if str(info['icon_name']) == 'unbinding':
                phases = info['unit_special_abilities_tables']['special_ability_to_special_ability_phase_junctions_tables']
                if phases is not None:
                    for i, phase in enumerate(phases):
                        phase_info = self.hhelper.get_ability_phase_info(phase['phase'])
                        unbinding_icon = self.icon[f"unbinding_stage{i+1}"]
                        strs.append(f"{unbinding_icon}{phase_info['duration']}")
        if len(strs) == 0:
            return ''
        return _indentstr(indent) + '/'.join(strs) + self.endl

    def get_land_unit_desc(self, name, luid, main_unit_info=None, indent=0):
        info = self.hhelper.get_land_unit_info(name)

        if main_unit_info is None:
            try:
                main_unit_info = self.hhelper.get_unit_info(info['key'])
            except KeyError as e:
                pass

        self.reload_skill = info['reload']
        self.primary_ammo = info['primary_ammo']
        self.secondary_ammo = info['secondary_ammo']
        self.n_entities = self.__get_unit_size(main_unit_info, info, get_crew=False)[2]
        desc = ''
        melee_weapon_info = self.hhelper.get_melee_info(info['primary_melee_weapon'])
        missile_weapon_info = self.hhelper.get_missile_info(info['primary_missile_weapon'])
        high_threat_str = f" {self.icon['high_threat']}" if main_unit_info is not None and main_unit_info['is_high_threat'] else ''
        desc += _indentstr(indent) + high_threat_str + self.beatify_unit_id(info['key']) + self.endl
        if self.spawn_unit is not None:
            desc += self._get_unit_unbinding(info['land_units_to_unit_abilites_junctions_tables'], indent=indent)
            desc += self._get_unit_abilities_icons(info['attribute_group'], info['land_units_to_unit_abilites_junctions_tables'], indent=indent)
        desc += self._format_land_unit_info(info, main_unit_info, indent=indent)
        desc += self._get_melee_weapon(melee_weapon_info, luid, indent=indent)
        self.primary_melee = info['primary_melee_weapon']
        desc += self._get_missile_weapon(missile_weapon_info, luid, info['accuracy'], info['reload'], indent=indent)
        self.primary_missile = info['primary_missile_weapon']
        desc += self._get_engine(info['engine'], luid, info['accuracy'], info['reload'], indent=indent)
        desc += self._get_support_weapons(info['battle_personalities_grouped'], luid, info['accuracy'], indent=indent)
        return desc

#entrypoint
    def get_full_unit_desc(self, info, luid, spawn=False, indent=0):
        self._restore_shared_fields()
        if spawn:
            self.spawn_unit = True
        desc = ''
        desc += self.get_land_unit_desc(luid, luid, main_unit_info=info, indent=indent)
        # here we have all contatc effects in map
        return  self.make_text_white(desc)




    # entrypoint - animations
    def get_unit_animation(self, animation_key, indent=0):
        def format_tag(tag, indent):

            def format_time(start, end):
                if start == end:
                    return f'{self.highlight(round(start, 2))}'
                # print(start, end)
                return f'{self.highlight(round(start, 2))}-{self.highlight(round(end, 2))}'

            info = f"{str.lower(tag['Name'])}|"

            if tag['Name'] == 'IMPACT_POS':
                if tag['Version'] >= 10:
                    info += f"{format_time(tag['StartTime'], tag['EndTime'])}"

            if tag['Name'] == 'IMPACT_SPEED':
                if tag['Version'] >= 10:
                    info += f"{format_time(tag['StartTime'], tag['EndTime'])}"
                    info += f"|{tag['Speed']}"

            if tag['Name'] == 'SPLASH_ATTACK':
                if tag['Version'] >= 10:
                    shape = 'None'
                    shape = f"Cone({tag['AngleForCone']})" if tag['AoeShape'] == 0 else shape
                    shape = f"Corridor({round(tag['WidthForCorridor'], 2)})" if tag['AoeShape'] == 1 else shape
                    info += f"{format_time(tag['StartTime'], tag['EndTime'])}|{shape}|{self.icon['mass']}{tag['ImpactMassInKg']}{self.icon['scalar_speed']}{tag['ImpactSpeed']}"
                if tag['Version'] >= 11:
                    info += ''

            res = _indentstr(indent) + info + self.endl
            return res

        exclude_tags = {'EFFECT', 'FACE_POSE','RHAND_POSE', 'LHAND_POSE', 'WEAPON_RHAND', 'WEAPON_LHAND', 'DOCK_EQPT_LHAND', 'DOCK_EQPT_RHAND', 'SOUND_TRIGGER', 'FIRE_POS',
                        'DISABLE_PERSISTENT', 'DISABLE_PERSISTENT_VFX', 'DISABLE_HEAD_TRACKING', 'CAMERA_SHAKE_SCALE', 'CAMERA_SHAKE_POS', 'SHADER_PARAMETER', 'TRANSFORM', 'SPLICE', 'SPLICE_OVERRIDE', 'ANIMATED_PROP'}
        # self._restore_shared_fields()
        animation_types = self.hhelper.get_unit_animations(animation_key)
        if animation_types is None:
            return ''
        desc = animation_key + self.endl
        for slot_type, animations in animation_types.items():
            desc += _indentstr(indent) + f"{slot_type}:" + self.endl
            indent += 2
            for slot_name, slot_info in animations.items():
                desc += _indentstr(indent) + f"{slot_name} weight={self.highlight(slot_info['selection_weight'])}:" + self.endl
                indent += 2
                for i, meta_dict in enumerate(slot_info['instances']):
                    meta_name, meta = meta_dict['file_name'].split('/')[-1].split('.')[0], meta_dict['meta']
                    desc += _indentstr(indent) + f"#{i} {meta_name}:" + self.endl
                    indent += 2
                    for tag in meta:
                        if tag['Name'] in exclude_tags or 'DOCK' in tag['Name'] or 'EQPT' in tag['Name'] or 'BLEND' in tag['Name']:
                            continue
                        desc += format_tag(tag, indent)
                    indent -= 2
                indent -= 2
            indent -= 2
        return self.make_text_white(desc)

    def get_unit_animation_dev(self, luid):
        import json
        animation_types = self.hhelper.get_unit_animations(luid)
        if animation_types is None:
            return None
        return json.dumps(animation_types, indent=4)

    def _test_colors(self):
        desc = ""
        desc += self.endl + self.colorize('test', 'dark_r')
        desc += self.endl + self.colorize('test', 'magic')
        desc += self.endl + self.colorize('test', 'ancillary_uncommon')
        desc += self.endl + self.colorize('test', 'ancillary_crafted')
        desc += self.endl + self.colorize('test', 'ancillary_rare')
        desc += self.endl + self.colorize('test', 'ancillary_unique')
        desc += self.endl + self.colorize('test', 'help_page_link')
        desc += self.endl + self.colorize('test', 'fatigue_winded')
        desc += self.endl + self.colorize('test', 'fatigue_tired')
        return desc + self.endl

    def _add_bonus(self, base, ap, bonus):
        total_dmg = base + ap
        if base == 0 and ap == 0:
            ap_ratio = 0
        else:
            ap_ratio = ap / total_dmg

        total_base = base + (1-ap_ratio)*bonus
        total_ap = ap + ap_ratio*bonus
        return int(round(total_base)), int(round(total_ap)), ap_ratio

    def _format_dmg(self, typee, base, ap, vs_inf=0, vs_large=0, is_flaming=False, is_magic=False, is_spell=False, n=1):
        base, ap, vs_inf, vs_large = int(base), int(ap), int(vs_inf), int(vs_large)
        fire_str = f"{self.icon['mod_flaming']}" if is_flaming else ''
        magic_str = f"{self.icon['mod_magical']}" if is_magic else ''
        # fire_str = f"{self.icon['stat_resistance_flame']}" if is_flaming else ''
        # magic_str = f"{self.icon['stat_resistance_physical']}" if not is_magic else ''
        spell_str = f"{self.icon['stat_resistance_magic']}" if is_spell else ''

        if typee == 'melee':
            base_dmg_icon = self.icon['stat_melee_damage_base']
            ap_dmg_icon = self.icon['stat_melee_damage_ap']
        if typee == 'projectile':
            base_dmg_icon = self.icon['scalar_missile_damage_base']
            ap_dmg_icon = self.icon['scalar_missile_damage_ap']
        if typee == 'explosion':
            base_dmg_icon = self.icon['scalar_missile_explosion_damage_base']
            ap_dmg_icon = self.icon['scalar_missile_explosion_damage_ap']

        base_dmg_str = f"{base_dmg_icon}{base}"
        ap_dmg_str = f"{ap_dmg_icon}{ap}"
        base_vs_inf, ap_vs_inf, _ = self._add_bonus(base, ap, vs_inf)
        base_vs_large, ap_vs_large, _ = self._add_bonus(base, ap, vs_large)
        base_vs_inf_str = f"{base_dmg_icon}{base_vs_inf}" if vs_inf > 0 else ""
        ap_vs_inf_str = f"{ap_dmg_icon}{ap_vs_inf}" if vs_inf > 0 else ""
        base_vs_large_str = f"{base_dmg_icon}{base_vs_large}" if vs_large > 0 else ""
        ap_vs_large_str = f"{ap_dmg_icon}{ap_vs_large}" if vs_large > 0 else ""

        dmg_str = f"{base_dmg_str}{ap_dmg_str}"
        vs_inf_dmg_str = f" {self.icon['stat_bonus_vs_infantry']}{vs_inf}{base_vs_inf_str}{ap_vs_inf_str}" if vs_inf > 0 else ""
        vs_large_dmg_str = f" {self.icon['stat_bonus_vs_large']}{vs_large}{base_vs_large_str}{ap_vs_large_str}" if vs_large > 0 else ""

        all_dmg_str = f"{dmg_str}{vs_inf_dmg_str}{vs_large_dmg_str}"
        mod_str = f"{fire_str}{magic_str}{spell_str}"
        if len(mod_str) != 0:
            mod_str += ' '
        res = f"{mod_str}{all_dmg_str}"
        return res


    def _format_splash_attack(self, info, indent=0):
        if self.hhelper.handler.isnull(info['splash_attack_target_size']):
            return ''
        target_size = self.highlight(self.loctr.add_auto('entity_size', info['splash_attack_target_size']))
        desc = _indentstr(indent) + f"{self.icon['splash_attack']}{self.loctr.tr('splash_attack')}:" + self.endl
        desc += _indentstr(indent+self.indent_step) + f"{self.loctr.tr('splash_target_size')}: {target_size}" + self.endl
        desc += _indentstr(indent+self.indent_step) + f"{self.loctr.tr('splash_max_attacks')}: {self.highlight(info['splash_attack_max_attacks'])}" + self.endl
        if not math.isclose(info['splash_attack_power_multiplier'], 1.0, abs_tol=1e-5):
            desc += _indentstr(indent+self.indent_step) + f"{self.loctr.tr('splash_power_multiplier')}: {self.highlight(round(float(info['splash_attack_power_multiplier']), 2))}" + self.endl
        return desc

    def _format_collision_attack(self, info, indent=0):
        if info['collision_attack_max_targets'] == 0:
            return ''
        desc = _indentstr(indent) + f"{self.icon['collision_attack']}{self.loctr.tr('collision_attack')}:" + self.endl
        desc += _indentstr(indent+self.indent_step) + f"{self.loctr.tr('collision_max_targets')}: {self.highlight(info['collision_attack_max_targets'])}" + self.endl
        desc += _indentstr(indent+self.indent_step) + f"{self.loctr.tr('collision_refreshes')}: {self.highlight(info['collision_attack_max_targets_cooldown'])}" + self.endl
        return desc

    def _format_scaling_damage(self, info, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        max_dm = self.highlight(info['max_damage_multiplier'])
        min_dm = self.highlight(info['min_damage_multiplier'])
        max_hr = self.colorize(f"{round(info['max_health_ratio']*100)}%{self.icon['hp']}", 'green')
        min_hr = self.colorize(f"{round(info['min_health_ratio']*100)}%{self.icon['hp']}", 'green')
        desc = _indentstr(indent) + f"{self.loctr.tr('scaling_damage')}:{self.endl}"
        desc += _indentstr(indent) + f"{max_dm}@{max_hr} -> {min_dm}@{min_hr}"
        return desc + self.endl

    def _format_building_damage(self, multiplier, indent=0):
        multiplier = float(multiplier)
        if math.isclose(multiplier, 1.0, abs_tol=1e-5):
            return ''
        desc = _indentstr(indent) + f"{_icon_battle('can_siege')}{self.loctr.tr('building_damage_mult')}: {self.highlight(round(multiplier, 2))}" + self.endl
        return desc

    def _get_melee_weapon(self, info, luid, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        desc = _indentstr(indent) + f"{self.icon['melee_dmg']}{self.title(self.loctr.tr('melee_weapon'))}:" + self.endl
        indent += self.indent_step

        if info['__value__'] != self.primary_melee:
            dmg_str = self._format_dmg('melee', info['damage'], info['ap_damage'], info['bonus_v_infantry'], info['bonus_v_large'], info['ignition_amount'] > 0, info['is_magical'], info['is_spell'])
            desc += _indentstr(indent) + dmg_str + self.endl
            desc += self._format_building_damage(info['building_damage_multiplier'], indent)
            desc += self._format_scaling_damage(info['scaling_damage'], indent)
            desc += _indentstr(indent) + f"{self.loctr.tr('weapon_length')}: {self.highlight(info['weapon_length'])}" + self.endl
            desc += _indentstr(indent) + f"{self.loctr.tr('attack_interval')}: {self.highlight(info['melee_attack_interval'])}" + self.endl
            desc += self._format_splash_attack(info, indent)
            desc += self._format_collision_attack(info, indent)
            desc += self._get_contact_effect(info['contact_phase'], luid, indent)
        else:
            desc += _indentstr(indent) + f"{self.highlight(self.loctr.tr('same_as_primary'))}" + self.endl
        return desc

    def _get_ammo(self, is_secondary_ammo):
        if is_secondary_ammo:
            return self.secondary_ammo
        return self.primary_ammo

    def _get_missile_weapon(self, info, luid, accuracy=None, reload=0, is_support=False, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        desc = _indentstr(indent) + f"{self.icon['stat_ranged_damage']}{self.title(self.loctr.tr('missile_weapon'))}:" + self.endl
        indent += self.indent_step

        # if not is_support or is_support and info['use_secondary_ammo_pool']:
        if not is_support or is_support and info['__value__'] != self.primary_missile:
            desc += _indentstr(indent) + f"{self.icon['ammo']}{self.loctr.tr('ammo')}: {self.highlight(self._get_ammo(info['use_secondary_ammo_pool']))}" + self.endl
            desc += self._get_projectile(info['default_projectile'], luid, accuracy=accuracy, reload=reload, indent=indent)
        else:
            desc += _indentstr(indent) + f"{self.highlight(self.loctr.tr('same_as_primary'))}" + self.endl

        if info['alternate_missile_weapon'] is not None:
            for alt_projectile in info['alternate_missile_weapon']:
                desc += self._get_projectile(alt_projectile['projectile'], luid, accuracy=accuracy, reload=reload, alternate=True, indent=indent)
        return desc

    def _get_engine(self, engine_info, luid, accuracy=None, reload=0, indent=0):
        if self.hhelper.handler.isnull(engine_info):
            return ''

        desc = ''
        if engine_info['missile_weapon'] is not None and engine_info['missile_weapon'] != self. primary_missile:
            desc = _indentstr(indent) + f"{self.title(self.loctr.tr('engine'))}:" + self.endl
            indent += self.indent_step
            missile_weapon_info = self.hhelper.get_missile_info(engine_info['missile_weapon'])
            desc += self._get_missile_weapon(missile_weapon_info, luid, accuracy=accuracy, reload=reload, is_support=True, indent=indent)
        return desc

    def _get_support_weapons(self, info, luid, accuracy=None, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        desc = _indentstr(indent) + f"{self.title(self.loctr.tr('support_weapons'))}:" + self.endl
        indent += self.indent_step

        for k, stat_info in info.items():
            desc += _indentstr(indent) + f"{self.highlight(stat_info['count'])} x { self.loctr.add_auto('support_team', k, auto_formatter=self.beatify_unit_id)}:" + self.endl
            desc += self._get_melee_weapon(stat_info['primary_melee_weapon'], luid, indent=indent+self.indent_step)
            desc += self._get_missile_weapon(stat_info['primary_missile_weapon'], luid, accuracy=accuracy, is_support=True, indent=indent+self.indent_step)
        return desc


    def _get_contact_effect(self, info, luid, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        info = self.hhelper.get_ability_phase_info(info)
        self._add_contact_effect_to_map(luid, info['id'])
        if info['effect_type'] == 'positive':
            color = 'green'
        if info['effect_type'] == 'negative':
            color = 'red'
        if info['effect_type'] == 'neutral':
            color = 'white'
        effect_str = f" {self.loctr.add_auto('contact_effect', info['sanitized_name'], auto_formatter=lambda x: info['raw_name'])}"
        if info['duration'] > 0:
            effect_str += f" ({info['duration']}{self.loctr.tr('s')})"
        desc = _indentstr(indent) + f"{self.title(self.loctr.tr('contact_effect'))}:{self.colorize(effect_str, color)}" + self.endl
        indent += self.indent_step
        return desc

    def _get_shrapnel(self, info, luid, accuracy, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        desc = _indentstr(indent) + f"{self.title(self.loctr.tr('shrapnel'))}:" + self.endl
        indent += self.indent_step

        n_projectiles = info['amount']
        desc += _indentstr(indent) + f"{self.icon['n_projectiles']}{self.loctr.tr('amount')}: {self.highlight(n_projectiles)}" + self.endl
        desc += self._get_projectile(info['projectile'], luid, accuracy=accuracy, indent=indent)
        return desc

    def _get_explosion(self, info, luid, accuracy=None, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''

        explosion = self.hhelper.get_explosion_info(info)
        no_ff = f"{self.icon['no_friendly_fire']}" if not explosion['affects_allies'] else ""
        desc = _indentstr(indent) + f"{self.title(self.loctr.tr('explosion'))}{no_ff}:" + self.endl
        indent += self.indent_step

        dmg_str = self._format_dmg('explosion', explosion['detonation_damage'], explosion['detonation_damage_ap'], 0, 0, explosion['ignition_amount'] > 0, explosion['is_magical'], explosion['is_spell'])
        desc += _indentstr(indent) + dmg_str + self.endl
        if self.debug:
            desc += _indentstr(indent) + f"{self.icon['distance']}{explosion['detonation_radius']} {self.icon['cooldown']}{explosion['detonation_duration']} {self.icon['scalar_speed']}{explosion['detonation_speed']}" + self.endl
        else:
            desc += _indentstr(indent) + f"{self.icon['distance']}{self.loctr.tr('detonation_radius')}: {self.highlight(explosion['detonation_radius'])}" + self.endl
        desc += self._get_contact_effect(explosion['contact_phase_effect'], luid, indent=indent)
        desc += self._get_shrapnel(explosion['shrapnel'], luid, accuracy=accuracy, indent=indent)
        return desc

    def _get_projectile(self, info, luid, accuracy=None, alternate=False, reload=None, wom_cost=0, n_projectiles_bombardment=None, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        projectile = self.hhelper.get_projectile_info(info)
        rules_df = self.hhelper.handler.db['_kv_morale_tables'].data
        alternate_str = f"[{self.loctr.tr('projectile_alternative')}]" if alternate else ''
        guided_str = f"{self.icon['self_guided']}" if not self.hhelper.handler.isnull(projectile['homing_params']) else ''
        no_ff_str = f"{self.icon['no_friendly_fire']}" if not projectile['can_damage_allies'] else ''
        cant_air_str = f"{_icon_battle('cant_target_flying')}" if not projectile['can_target_airborne'] else ''
        ignores_shields_str = ''
        leadership_debuff_str = f"{self.icon['stat_morale']}{self.colorize(round(float(rules_df.loc['ume_concerned_attacked_by_projectile', 'value'])), 'red')}"
        if projectile['category'] in {'artillery', 'misc'}:
            ignores_shields_str = f"{self.icon['ignores_shields']}"
            if projectile['category'] == 'artillery':
                leadership_debuff_str = f"{self.icon['stat_morale']}{self.colorize(round(float(rules_df.loc['ume_concerned_damaged_by_artillery', 'value'])), 'red')}"
        title = f"{self.loctr.tr('projectile')}"
        desc = _indentstr(indent) + f"{self.title(title)}{alternate_str}{leadership_debuff_str}{ignores_shields_str}{guided_str}{no_ff_str}{cant_air_str}:" + self.endl
        indent += self.indent_step

        if projectile['projectile_number'] != 1:
               desc += _indentstr(indent) + f"{self.icon['n_projectiles']}{self.loctr.tr('projectiles_number')}: {self.highlight(projectile['projectile_number'])}" + self.endl
        if projectile['shots_per_volley'] != 1:
               desc += _indentstr(indent) + f"{self.icon['shots_per_volley']}{self.loctr.tr('shots_per_volley')}: {self.highlight(projectile['shots_per_volley'])}" + self.endl
        if projectile['burst_size'] != 1:
               desc += _indentstr(indent) + f"{self.icon['burst_size']}{self.loctr.tr('burst_size')}: {self.highlight(projectile['burst_size'])}" + self.endl

        dmg_str = self._format_dmg('projectile', projectile['damage'], projectile['ap_damage'], projectile['bonus_v_infantry'], projectile['bonus_v_large'], projectile['ignition_amount'] > 0, projectile['is_magical'], projectile['is_spell'])
        desc += _indentstr(indent) + dmg_str + self.endl
        if projectile['can_damage_buildings']:
            desc += self._format_building_damage(projectile['building_damage_multiplier'], indent)
        desc += self._format_scaling_damage(projectile['scaling_damage'], indent)
        if projectile['shockwave_radius'] > 0:
            desc += _indentstr(indent) + f"{self.icon['distance']}{self.loctr.tr('shockwave_radius')}: {self.highlight(projectile['shockwave_radius'])}" + self.endl

        if not self.hhelper.handler.isnull(projectile['projectile_penetration']):
            if type(projectile['projectile_penetration']['entity_size_cap']) is float:
                projectile['projectile_penetration']['entity_size_cap'] = ''
            desc += _indentstr(indent) + f"{self.loctr.tr('projectile_penetration')}: {self.highlight(projectile['projectile_penetration']['key'])} ({self.loctr.add_auto('entity_size', projectile['projectile_penetration']['entity_size_cap'])})" + self.endl

        if projectile['spread'] > 0:
            spread = round(float(projectile['spread']), 2)
            desc += _indentstr(indent) + f"{self.icon['stat_accuracy']}{self.loctr.tr('projectile_spread')}: {self.highlight(spread)}" + self.endl

        marksmanship_bonus = round(float(projectile['marksmanship_bonus']))
        _accuracy = accuracy
        if _accuracy is None:
            _accuracy = 0
        desc += _indentstr(indent) + f"{self.icon['stat_accuracy']}{self.loctr.tr('total_accuracy')}: {self.highlight(_accuracy + marksmanship_bonus)} ({_accuracy}+{marksmanship_bonus})" + self.endl
        desc += _indentstr(indent) + f"{self.icon['stat_accuracy']}{self.loctr.tr('calibration')}:"
        calibration_distance = round(float(projectile['calibration_distance']))
        desc += f" {self.loctr.tr('calibration_distance')} {self.highlight(calibration_distance)}"
        calibration_area = round(float(projectile['calibration_area']), 1)
        desc += f" {self.loctr.tr('calibration_area')} {self.highlight(calibration_area)}" + self.endl
        desc += _indentstr(indent) + f"{self.icon['distance']}{self.loctr.tr('effective_range')}: {self.highlight(projectile['effective_range'])}" + self.endl

        if self.reload_skill is not None:
            reload_time = projectile['base_reload_time'] * (100-self.reload_skill) / 100
            reload_time_str = f"{reload_time:.1f}"
            base_reload_str = f"{projectile['base_reload_time']:.1f}"
            desc += _indentstr(indent) + f"{self.icon['stat_reloading']}{self.loctr.tr('reload_time')}: {self.highlight(reload_time_str)} ({self.highlight(base_reload_str)})" + self.endl

        desc += self._get_contact_effect(projectile['contact_stat_effect'], luid, indent=indent)
        desc += self._get_explosion(projectile['explosion_type'], luid, accuracy=accuracy, indent=indent)

        n = 1 if n_projectiles_bombardment is None else n_projectiles_bombardment
        if self.n_entities is not None:
            n = self.n_entities
        n *= projectile['projectile_number'] * projectile['shots_per_volley'] * projectile['burst_size']
        full_dmg_str = _indentstr(indent) + \
                       self._format_dmg('projectile',
                                        n * projectile['damage'],
                                        n * projectile['ap_damage'],
                                        n * projectile['bonus_v_infantry'],
                                        n * projectile['bonus_v_large'],
                                        projectile['ignition_amount'] > 0,
                                        projectile['is_magical'],
                                        projectile['is_spell']
                                        ) + self.endl
        desc += _indentstr(indent - self.indent_step) + 'Volley dmg:' + self.endl + full_dmg_str

        explosion = self.hhelper.get_explosion_info(projectile['explosion_type'])
        if explosion is not None:
            exp_dmg, exp_dmg_ap = explosion['detonation_damage'], explosion['detonation_damage_ap']
            full_dmg_str = _indentstr(indent) + \
                            self._format_dmg('explosion',
                                             n * exp_dmg,
                                             n * exp_dmg_ap,
                                             0,
                                             0,
                                             explosion['ignition_amount'] > 0,
                                             explosion['is_magical'],
                                             explosion['is_spell']
                                             ) + self.endl
            desc += full_dmg_str

            explosion = self.hhelper.get_explosion_info(projectile['explosion_type'])
            dmg_str = self._format_dmg('projectile',
                                       n * (projectile['damage'] + explosion['detonation_damage']),
                                       n * (projectile['ap_damage'] + explosion['detonation_damage_ap']),
                                       n * (projectile['bonus_v_infantry']),
                                       n * (projectile['bonus_v_large']),
                                       False, False, False)
            desc += _indentstr(indent - self.indent_step) + f"{self.loctr.tr('projectile_total_dmg')}:" + self.endl
            desc += _indentstr(indent) + dmg_str + self.endl

        vortex = self.hhelper.get_vortex_info(projectile['spawned_vortex'])
        desc += self._get_vortex(vortex, luid, indent=indent - self.indent_step)

        if wom_cost > 0:
            dmg_str = self._format_dmg('projectile',
                                       round(n * (projectile['damage'] + explosion['detonation_damage']) / wom_cost),
                                       round(n * (projectile['ap_damage'] + explosion['detonation_damage_ap']) / wom_cost),
                                       round(n * (projectile['bonus_v_infantry']) / wom_cost),
                                       round(n * (projectile['bonus_v_large']) / wom_cost),
                                       False, False, False)
            desc += _indentstr(indent - self.indent_step) + f"{self.loctr.tr('projectile_dmg_per_wom')} {self.colorize(1, 'magic')}{self.icon['mana']}:" + self.endl
            desc += _indentstr(indent) + dmg_str + self.endl

        return desc


    def _get_bombardment(self, info, luid, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''
        desc = _indentstr(indent) + f"{self.title(self.loctr.tr('bombardment'))}:" + self.endl
        indent += self.indent_step

        desc += _indentstr(indent) + f"{self.icon['cooldown']}{self.loctr.tr('bombardment_start_time')}: {self.highlight(info['start_time'])}" + self.endl
        desc += _indentstr(indent) + f"{self.icon['cooldown']}{self.loctr.tr('bombardment_arrival_window')}: {self.highlight(info['arrival_window'])}" + self.endl

        desc += _indentstr(indent) + f"{self.icon['distance']}{self.loctr.tr('bombardment_radius_spread')}: {self.highlight(info['radius_spread'])}" + self.endl
        n_projectiles = info['num_projectiles']
        desc += _indentstr(indent) + f"{self.icon['n_projectiles']}{self.loctr.tr('bombardment_amount')}: {self.highlight(n_projectiles)}" + self.endl
        desc += self._get_projectile(info['projectile_type'], luid, indent=indent, n_projectiles_bombardment=n_projectiles)
        return desc

    def _get_vortex(self, info, luid, indent=0):
        if self.hhelper.handler.isnull(info):
            return ''

        many_v_str = f" x {self.highlight(info['num_vortexes'])}" if info['num_vortexes'] > 1 else ''
        no_ff = f"{self.icon['no_friendly_fire']}" if not info['affects_allies'] else ''
        ih_str = f"{self.icon['infinite_height']}" if info['infinite_height'] else ''
        desc = _indentstr(indent) + f"{self.title(self.loctr.tr('vortex'))}{ih_str}{no_ff}{many_v_str}:" + self.endl
        indent += self.indent_step

        desc += _indentstr(indent) + f"{self.icon['cooldown']}{self.loctr.tr('vortex_delay')}: {self.highlight(info['delay'])}" + self.endl
        if info['num_vortexes'] > 1:
            desc += _indentstr(indent) + f"{self.icon['cooldown']}{self.loctr.tr('vortex_delta')}: {self.highlight(info['delay_between_vortexes'])}" + self.endl

        dmg_str = self._format_dmg('explosion', info['damage'], info['damage_ap'], 0, 0, info['ignition_amount'] > 0, info['is_magical'], info['is_spell'])
        desc += _indentstr(indent) + dmg_str + self.endl

        if info['movement_speed'] > 0:
            desc += _indentstr(indent) + f"{self.icon['scalar_speed']}{self.loctr.tr('vortex_movement_speed')}: {self.highlight(info['movement_speed'])}" + self.endl
        else:
            dmg_str = self._format_dmg('explosion', info['damage'] * (info['duration']), info['damage_ap'] * (info['duration']), 0, 0, info['ignition_amount'] > 0, info['is_magical'], info['is_spell'])
            desc += _indentstr(indent) + f"{self.loctr.tr('vortex_max_damage')}: " + dmg_str + self.endl
            desc += _indentstr(indent) + f"{self.colorize(self.loctr.tr('vortex_stationary'), 'green')}" + self.endl

        if info['move_change_freq'] > 0:
            desc += _indentstr(indent) + f"{self.icon['scalar_speed']}{self.loctr.tr('vortex_move_change_freq')}: {self.highlight(info['move_change_freq'])}" + self.endl
            if info['change_max_angle'] > 0:
                desc += _indentstr(indent) + f"{self.icon['scalar_speed']}{self.loctr.tr('vortex_change_max_angle')}: {self.highlight(info['change_max_angle'])}" + self.endl
        else:
            desc += _indentstr(indent) + f"{self.colorize(self.loctr.tr('vortex_directional'), 'green')}" + self.endl

        desc += _indentstr(indent) + f"{self.icon['distance']}{self.loctr.tr('vortex_radius')}: {self.highlight(info['start_radius'])} -> {self.highlight(info['goal_radius'])} {self.icon['scalar_speed']}{self.highlight(info['expansion_speed'])}" + self.endl

        if info['detonation_force'] > 0:
            desc += _indentstr(indent) + f"{self.loctr.tr('vortex_detonation_force')}: {self.highlight(info['detonation_force'])}" + self.endl

        desc += self._get_contact_effect(info['contact_effect'], luid, indent=indent)
        return desc

    def _get_spawned_unit(self, luid, indent=0):
        if self.hhelper.handler.isnull(luid):
            return ''
        self.spawn_unit = True
        # info = self.handler.get_land_unit_info(luid)
        desc = _indentstr(indent) + f"{self.title(self.loctr.tr('summon_unit'))}:" + self.endl
        indent += self.indent_step
        desc += self.get_full_unit_desc(None, luid, spawn=True, indent=indent)
        return desc


#entrypoint
    def get_short_ability_desc(self, info, ability_id, indent=0):
        self._restore_shared_fields()
        desc = ''
        if info['unit_special_abilities_tables'] is None:
            return desc
        usat = info['unit_special_abilities_tables']
        if self.hhelper.handler.isnull(usat):  # ???
            print('None special table', info['key'])
            return ''


        if usat['update_targets_every_frame']:
            desc += _indentstr(indent) + f"{self.loctr.tr('update_targets_frame')}: {self.highlight(self.loctr.tr('update_true'))}" + self.endl
        # duration = usat['active_time']
        # cooldown = usat['recharge_time']
        start_cooldown = round(float(usat['initial_recharge']))
        if start_cooldown > 0:
            desc += _indentstr(indent) + f"{_icon('icon_ability_unbinding_stage3')}{self.loctr.tr('initial_cooldown')}: {self.highlight(start_cooldown)}" + self.endl
        cast_time = round(float(usat['wind_up_time']))
        if cast_time > 0:
            desc += _indentstr(indent) + f"{self.icon['cooldown']}{self.loctr.tr('cast_time')}: {self.highlight(cast_time)}" + self.endl

        if info['special_ability_intensity_settings_tables'] is not None:
            intensity_type = info['special_ability_intensity_settings_tables']['intensity_type']
            if intensity_type == 'linear_multiplier':
                max_amount = info['special_ability_intensity_settings_tables']['max_amount']
                intensity_source = info['special_ability_intensity_settings_tables']['intensity_source']
                desc += _indentstr(indent) + f"{self.loctr.tr('scales_linearly')} {self.highlight(max_amount)} {self.loctr.add_auto('intensity_source', intensity_source)}" + self.endl
                if intensity_source == 'time_in_melee':
                    desc += _indentstr(indent) + self.highlight(self.loctr.tr('bug_norsca_rage_intensity')) + self.endl

        if type(usat['behaviour']) is not float:
            desc += _indentstr(indent) + f"{self.loctr.add_auto('behaviour', usat['behaviour'])}" + self.endl

        desc += self._get_projectile(usat['activated_projectile'], ability_id, wom_cost=info['unit_special_abilities_tables']['mana_cost'], indent=indent)
        desc += self._get_bombardment(usat['bombardment'], ability_id, indent=indent)
        desc += self._get_vortex(usat['vortex'], ability_id, indent=indent)
        desc += self._get_spawned_unit(usat['spawned_unit'], indent=indent)

        if info['unit_special_abilities_tables']['special_ability_to_special_ability_phase_junctions_tables'] is not None:
            for ph in info['unit_special_abilities_tables']['special_ability_to_special_ability_phase_junctions_tables']:
                desc += self.get_ability_phase_desc(ph['phase'], wom_cost=usat['mana_cost'])

        if usat['miscast_chance'] > 0:
            desc += _indentstr(indent) + f"{self.title(self.loctr.tr('miscast')+':')}" + self.endl
            desc += self._get_explosion(usat['miscast_explosion'], ability_id, indent=indent + self.indent_step)
        return self.make_text_white(desc)

#entrypoint
    def get_ability_desc(self, info, luid, indent=0):
        self._restore_shared_fields()
        desc = ''#info['key']
        if luid in self.contact_effect_map:
            effects = self.contact_effect_map[luid]
            for effect in effects:
                desc += self.get_ability_phase_desc(effect, True, indent=indent)
                # desc += self.get_ability_phase_desc(effect, False, indent=indent)
        return self.make_text_white(desc)


    def _heal_str(self, info, wom_cost=None):
        duration = info['duration']
        freq = info['hp_change_frequency']
        freq_str = self.colorize(str(freq)+'s', 'green')
        heal = info['heal_amount']
        heal_str = self.colorize(heal, 'green')
        str_per_tick = f" {self.loctr.tr('per_tick')}"
        ticks_count = 1
        if not math.isclose(duration, -1.0):
            str_per_tick = ""
            ticks_count = int(duration * 1000) // int(freq * 1000)
        max_heal = round(ticks_count * heal * 100, 2)
        max_heal_str = f"{self.loctr.tr('max_heal_per_unit')}{str_per_tick}: {self.icon['hp']}{self.colorize(max_heal, 'green')}% ({self.icon['mod_flaming']}{self.colorize(round(max_heal/2, 2), 'green')}%)"

        # desc = f"Heals {self.icon['hp']}{heal_str} every {freq_str}" + self.endl


        str_wom_eff = ""
        if wom_cost:
            str_wom_eff = self.endl + f"{self.loctr.tr('heals')} {self.icon['hp']}~{self.colorize(round(float(max_heal/wom_cost), 2), 'green')}% {self.loctr.tr('dd_wom_eff_per')} {self.colorize(1, 'magic')}{self.icon['mana']}"

        desc = max_heal_str + str_wom_eff
        if info['resurrect']:
            desc += self.endl + f"{self.icon['resurrect']}" + self.colorize(self.loctr.tr('ressurect'), 'green')
        return desc

    def _fatigue_str(self, info):
        duration = info['duration']
        freq = info['fatigue_change_ratio']
        desc = ''
        if math.isclose(duration, -1.0):
            return desc
        else:
            total_fatigue_perc = round(duration * freq * 100)
            color = 'green' if freq < 0 else 'red'
            desc += f"{self.loctr.tr('fatigue_total')} "
            fth = 200
            if abs(total_fatigue_perc) > fth:
                desc += f'> {self.colorize(fth, color)}%'
            else:
                desc += f'{self.colorize(total_fatigue_perc, color)}%'
        desc += f"{self.icon['fatigue']}"
        return desc

    def _direct_dmg_str(self, info, wom_cost=None):
        # dmg = math.floor(info['damage_amount'] * self.army_size_coeffs[self.army_size]['direct_dmg']) if info['damage_amount'] != 1 else info['damage_amount']
        dmg = info['damage_amount'] - 1 # because of the bug
        dmg_low_th = math.floor(info['damage_amount'] / 2)
        avg_dmg_per_ent = int((dmg_low_th + dmg) / 2)
        dmg_str = f"~{self.colorize(avg_dmg_per_ent, 'red')} ({self.colorize(dmg_low_th, 'red')}-{self.colorize(dmg, 'red')})"
        freq = self.colorize(str(info['hp_change_frequency'])+self.loctr.tr('s'), 'red')
        max_ents = self.colorize(info['max_damaged_entities'], 'red')
        duration = info['duration']
        ticks_count = 1
        str_per_tick = f" {self.loctr.tr('per_tick')}"
        if not math.isclose(duration, -1.0):
            str_per_tick = ""
            ticks_count = int(duration * 1000) // int(info['hp_change_frequency'] * 1000)
            ticks_count += 1
        dmg_min = int(ticks_count * info['max_damaged_entities'] * dmg_low_th)
        dmg_max = int(ticks_count * info['max_damaged_entities'] * dmg)
        avg_dmg = int((dmg_min + dmg_max) / 2)
        str_expected_damage = f"{self.loctr.tr('dd_damage_per_unit')}{str_per_tick}: ~{self.colorize(avg_dmg, 'red')} ({self.colorize(dmg_min, 'red')}-{self.colorize(dmg_max, 'red')})"

        str_wom_eff = ""
        if wom_cost:
            str_wom_eff = self.endl + f"{self.loctr.tr('dd_deals')} ~{self.colorize(round(float(avg_dmg/wom_cost)), 'red')} {self.loctr.tr('dd_wom_eff_per')} {self.colorize(1, 'magic')}{self.icon['mana']}"

        effective_unit_size = self.colorize(math.ceil(info['max_damaged_entities']), 'red')
        desc = f"{self.loctr.tr('dd_deals')} {self.icon['mod_magical']}{self.icon['stat_resistance_magic']}{self.icon['stat_melee_damage_ap']} {dmg_str} "+ f"{self.loctr.tr('dd_per_entity_every')} {freq}" + self.endl + \
                f"{self.loctr.tr('dd_effective_vs')} {effective_unit_size} {self.loctr.tr('dd_entities_per_unit')}" + self.endl + \
                str_expected_damage + str_wom_eff
        return desc

    def _mana_regen(self, value, duration):
        base_power_recharge = self.hhelper.get_power_recharge()
        mana_regen_abs = round(base_power_recharge*value, 3)
        mana_regen_str = f"{mana_regen_abs}"
        value_str = '+' + mana_regen_str if value > 0 else mana_regen_str
        duration_str = ''
        s_str = f"1{self.loctr.tr('s')}"
        if value > 0:
            desc = f"{self.loctr.tr('mana_recharges')} {self.colorize(value_str, 'magic')}{self.icon['mana']} {self.loctr.tr('per')} {self.colorize(s_str , 'magic')}"
        else:
            desc = f"{self.loctr.tr('mana_recharges')} {self.colorize(value_str, 'magic')}{self.icon['mana']} {self.loctr.tr('per')} {self.colorize(s_str, 'magic')}"
        if duration > 0:
            total_mana = round(mana_regen_abs*duration, 2)
            desc += self.endl + _indentstr(self.indent_step) + f"{self.loctr.tr('mana_total')} {self.colorize(total_mana, 'magic')}{self.icon['mana']}"
        return desc

    def _mana_pool(self, value, duration):
        total_mana = round(value, 2)
        if duration > 0:
            total_mana = round(value*duration, 2)
        if value > 0:
            desc = f"{self.loctr.tr('mana_add')} {self.colorize(total_mana, 'magic')}{self.icon['mana']} {self.loctr.tr('mana_to_reserves')}"
        else:
            desc = f"{self.loctr.tr('mana_reduce')} {self.colorize(total_mana, 'magic')}{self.icon['mana']} {self.loctr.tr('mana_from_reserves')}"
        return desc + self.endl

    def get_full_phase_stats(self, info, indent=0):
        desc = ''
        if info['special_ability_phase_stat_effects_tables'] is not None:
            for stat in info['special_ability_phase_stat_effects_tables']:
                value = stat['value']
                value_str = f"{value}"
                if stat['how'] == 'mult':
                    value = (value - 1) * 100
                    value_str = f"{round(value)}%"
                color = 'red'
                if value > 0:
                    value_str = '+' + value_str
                    color = 'green'
                get_name = lambda x: ' '.join([s.capitalize() for s in x.split('_')[1:]])
                text = f"{value_str} {self.icon[stat['stat']]}{self.loctr.add_auto('stat_name', stat['stat'], auto_formatter=get_name)}"
                desc += self.endl + f"{self.colorize(text, color)}"

        if info['special_ability_phase_attribute_effects_tables'] is not None:
            for attr in info['special_ability_phase_attribute_effects_tables']:
                color = self._get_effect_color(attr['attribute_type'])
                desc += self.endl + f"{self.colorize(attr['attribute'], color)}"
        return desc

    def _get_effect_color(self, effect_type):
        color = None
        if effect_type == 'positive':
            color = 'green'
        if effect_type == 'negative':
            color = 'red'
        if effect_type == 'neutral':
            color = 'white'
        return color

#entrypoint
    def get_ability_phase_desc(self, phase_id, full_stats=False, wom_cost=None, indent=0):
        self._restore_shared_fields()
        info = self.hhelper.get_ability_phase_info(phase_id)
        desc = ''
        color = self._get_effect_color(info['effect_type'])
        name = f"{self.loctr.add_auto('phase_name', info['sanitized_name'], auto_formatter=lambda x: info['raw_name'])}"
        name = self.colorize(name, color)
        desc += name
        if info['damage_amount'] > 0:
            desc += self.endl + self._direct_dmg_str(info, wom_cost=wom_cost)
        if info['heal_amount'] > 0:
            desc += self.endl + self._heal_str(info, wom_cost=wom_cost)
        if info['fatigue_change_ratio'] != 0:
            desc += self.endl + self._fatigue_str(info)

        if not math.isclose(info['mana_regen_mod'], 0):
            desc += self.endl + self._mana_regen(info['mana_regen_mod'], info['duration'])
        if not math.isclose(info['mana_max_depletion_mod'], 0):
            desc += self.endl + self._mana_pool(info['mana_max_depletion_mod'], info['duration'])

        if not math.isclose(info['replenish_ammo'], 0):
            value = info['replenish_ammo']
            value = value * 100
            value_str = f"{round(value)}%"
            color = 'red'
            if value > 0:
                value_str = '+' + value_str
                color = 'green'
            text = f"{value_str} {self.icon['ammo']}{self.loctr.tr('ammo')}"
            desc += self.endl + f"{self.colorize(text, color)}"

        # if info['duration'] > -0.5:
        #     desc += self.endl

        if full_stats:
            desc += self.get_full_phase_stats(info)
        return self.make_text_white(desc + self.endl)
