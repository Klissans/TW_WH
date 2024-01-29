def default_value_formatter(value:str) -> str:
    return ' '.join([x.capitalize() for x in value.split('_')])


class Localizator:

#self.loctr.tr('charge_bonus')
#self.loctr.add_auto('ground_effect', affected_group)

    def __init__(self, handler, prefix):
        self.handler = handler
        self.prefix = prefix
        self.tr_tables = {
            'common': {
                's': 's',
                'm': 'm',
                'per': 'per',
                'per_tick': 'per tick',

                'bp_unit_stats': 'Unit Stats',

                'mass': 'Mass',

                'ground_effect': 'Ground Effect',
                'strider': 'Strider',
                'hiding_modifier': 'Hiding Modifier',
                'spot_distance': 'Spot Distance',
                'spot_tree': 'Tree',
                'spot_scrub': 'Scrub',

                'scales_linearly': 'Scales linearly up to',

                'melee_attack': 'Melee Attack',
                'melee_defence': 'Melee Defence',
                'charge_bonus': 'Charge Bonus',

                'melee_weapon': 'Melee Weapon',
                'weapon_length': 'Weapon Length',
                'attack_interval': 'Attack Interval',

                'splash_attack': 'Splash Attack',
                'splash_target_size': 'Target Size',
                'splash_max_attacks': 'Max Targets',
                'splash_power_multiplier': 'Power Multiplier',

                'collision_attack': 'Collision Attack',
                'collision_max_targets': 'Max Targets',
                'collision_refreshes': 'Refreshes',

                'scaling_damage': 'Scaling Damage',
                'building_damage_mult': 'Building Damage Multiplier',

                'missile_weapon': 'Missile Weapon',
                'ammo': 'Ammo',

                'engine': 'Engine',

                'support_weapons': 'Support Weapons',
                'same_as_primary': 'Same as Primary Weapon',

                'contact_effect': 'Contact Effect',

                'shrapnel': 'Shrapnel',
                'amount': 'Amount',

                'explosion': 'Explosion',
                'detonation_radius': 'Detonation Radius',

                'projectile': 'Projectile',
                'projectile_alternative': 'Alternative',
                'projectiles_number': 'Projectiles Number',
                'shots_per_volley': 'Shots per Volley',
                'burst_size': 'Burst Size',
                'shockwave_radius': 'Shockwave Radius',
                'projectile_penetration': 'Penetration',
                'projectile_spread': 'Spread',
                'total_accuracy': 'Total Accuracy',
                'calibration': 'Calibration',
                'calibration_distance': 'Distance',
                'calibration_area': 'Area',
                'effective_range': 'Effective Range',
                'reload_time': 'Reload Time (Base)',

                'projectile_total_dmg': 'Total damage',
                'projectile_dmg_per_wom': 'Damage per',

                'bombardment': 'Bombardment',
                'bombardment_start_time': 'Start Time',
                'bombardment_arrival_window': 'Arrival Window',
                'bombardment_radius_spread': 'Radius Spread',
                'bombardment_amount': 'Amount',

                'vortex': 'Vortex',
                'vortex_delay': 'Delay',
                'vortex_delta': 'Time Delta',
                'vortex_movement_speed': 'Movement Speed',
                'vortex_max_damage': 'Max Damage',
                'vortex_stationary': 'Stationary',
                'vortex_directional': 'Directional',
                'vortex_move_change_freq': 'Move Change Freq',
                'vortex_change_max_angle': 'Change Max Angle',
                'vortex_radius': 'Radius',
                'vortex_detonation_force': 'Detonation Force',

                'summon_unit': 'Summons Unit',

                'update_targets_frame': 'Update Targets Every Frame',
                'update_true': 'True',
                'initial_cooldown': 'Initial Cooldown',
                'cast_time': 'Cast Time',
                'miscast': 'Miscast',

                'max_heal_per_unit': 'Max heal per unit',
                'heals': 'Heals',
                'ressurect': 'Resurrects dead entities',
                'fatigue_total': 'Total is',

                'dd_damage_per_unit': 'Damage per unit',
                'dd_deals': 'Deals',
                'dd_per_entity_every': 'per entity every',
                'dd_effective_vs': 'Effective vs',
                'dd_entities_per_unit': 'entities per unit',
                'dd_wom_eff_per': 'per unit per',

                'mana_recharges': 'Recharges',
                'mana_total': 'for a total of',
                'mana_add': 'Adds',
                'mana_reduce': 'Reduces',
                'mana_to_reserves': 'to reserves',
                'mana_from_reserves': 'from reserves',


            },

            'bugs_and_notes': {
                'note_arcane_surge': "NOTE: Despite the fact that this ability hadn't been working since the game release until the patch 1.3, the power restoration to reserves was NERFED in patch 1.1",
                'bug_dd_extra_tick': "BUG: DD spells have an extra tick of damage when the effect applies to the unit",
                'bug_dd_upper_range': "BUG: The upper range is actually lower by 1 - guess it's a bug in randomization function",
                'bug_dd_lower_range': "BUG: The lower range has a rounding error - game rounds value down and the UI rounds it up",
                'bug_dd_ui': "BUG: UI calculates the lower range incorrectly for max_entities greater than 1",
                'bug_norsca_rage_intensity': "BUG: Unit receives boost to intensity when enters melee after disengaging",
            },

        }

    def tr(self, s:str)-> str:
        return '{{tr:' + s + '}}'



    def add_auto(self, table_name, auto_value, auto_formatter=default_value_formatter):
        formatted_value = auto_value
        if type(auto_formatter) is str:
            formatted_value = auto_formatter
        elif auto_formatter is not None:
            formatted_value = auto_formatter(auto_value)
        tr_table = self.tr_tables.setdefault('auto_' + table_name, dict())
        key = f'{table_name}_{auto_value}'
        tr_table[key] = formatted_value
        return self.tr(key)

    def compile(self):
        loc_prefix = 'ui_text_replacements_localised_text_'
        for table_name, tr_table in self.tr_tables.items():
            prefix = self.prefix+f'_{table_name}__'
            tr_df = self.handler.duplicate_table('ui_text_replacements_tables', prefix=prefix, copy_data=False).data
            tr_loc_df = self.handler.duplicate_table('ui_text_replacements__', prefix=prefix, copy_data=False).data
            for k, v in tr_table.items():
                tr_df.loc[k] = {'key': k}
                tr_loc_df.loc[k] = {'key': loc_prefix + k, 'text': v, 'tooltip': False}
