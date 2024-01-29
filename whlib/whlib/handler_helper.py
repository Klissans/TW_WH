import pprint


class HandlerHelper:

    def __init__(self, handler):
        self.handler = handler

    def _group_additional_personalities(self, personas):
        # will return only usefull (with stats)
        res = None
        if personas is not None:
            res = {}
            for persona in personas:
                persona['battle_personality'] = self.get_battle_personality_info(persona['battle_personality'])
                stats = persona['battle_personality']['battle_entity_stats']
                if not self.handler.isnull(stats):
                    key = stats['key']
                    if key not in res:
                        res[key] = {}
                        res[key]['primary_melee_weapon'] = self.get_melee_info(stats['primary_melee_weapon']) if \
                            not self.handler.isnull(stats['primary_melee_weapon']) else None
                        res[key]['primary_missile_weapon'] = self.get_missile_info(stats['primary_missile_weapon']) if \
                            not self.handler.isnull(stats['primary_missile_weapon']) else None
                        res[key]['count'] = 1
                    else:
                        res[key]['count'] += 1
            if len(res) == 0:
                res = None
        return res

    def get_ground_effects(self, name):
        records = self.handler.get_entries_by_value('ground_type_to_stat_effects_tables', 'affected_group', name)
        # group by Ground Type
        records.sort(key=lambda item: item['affected_stat'])
        records.sort(key=lambda item: item['ground_type'])

        ground_types = set([r['ground_type'] for r in records])
        res = {}
        for gt in ground_types:
            if gt == 'sharp_stones':
                continue
            res[gt] = {}
            for r in records:
                if r['ground_type'] == gt:
                    res[gt][r['affected_stat']] = r['multiplier']
        return res

    def get_battle_personality_info(self, name):
        info = self.handler.get_entry_by_index('battle_personalities_tables', name)
        if info is None:
            return None
        self.handler._resolve_key_array(info, ['battle_entity'])
        self.handler._resolve_key_array(info, ['battle_entity_stats'])
        return info

    def get_melee_info(self, name):
        info = self.handler.get_entry_by_index('melee_weapons_tables', name)
        if info is None:
            return None
        self.handler._resolve_key_array(info, ['scaling_damage'])
        return info

    def get_missile_info(self, name):
        info = self.handler.get_entry_by_index('missile_weapons_tables', name)
        if info is None:
            return None
        # should check manually
        info['alternate_missile_weapon'] = self.handler.get_entries_by_value('missile_weapons_to_projectiles_tables', 'missile_weapon', info['key'])
        return info

    def get_projectile_info(self, name):
        info = self.handler.get_entry_by_index('projectiles_tables', name)
        if info is None:
            return None
        self.handler._resolve_key_array(info, ['homing_params'])
        self.handler._resolve_key_array(info, ['scaling_damage'])
        self.handler._resolve_key_array(info, ['projectile_penetration'])
        return info

    def get_explosion_info(self, name):
        info = self.handler.get_entry_by_index('projectiles_explosions_tables', name)
        if info is None:
            return None
        self.handler._resolve_key_array(info, ['shrapnel'])
        return info

    def get_vortex_info(self, name):
        info = self.handler.get_entry_by_index('battle_vortexs_tables', name)
        if info is None:
            return None
        # self.handler._resolve_key_array(info, ['contact_effect'])
        return info

    def get_land_unit_info(self, name):
        info = self.handler.get_entry_by_index('land_units_tables', name)
        if info is None:
            return None
        info['attribute_group'] = self.handler.get_entries_by_value('unit_attributes_to_groups_junctions_tables', 'attribute_group', info['attribute_group'])
        info['battle_personalities'] = self.handler.get_entries_by_value('land_units_to_battle_personalities_junctions_tables', 'land_unit', info['key'])
        self.handler._resolve_key_array(info, ['score_capture_tier'])
        self.handler._resolve_key_array(info, ['armour'])
        self.handler._resolve_key_array(info, ['man_entity'])
        self.handler._resolve_key_array(info, ['mount', 'entity'])
        self.handler._resolve_key_array(info, ['articulated_record', 'articulated_entity'])
        self.handler._resolve_key_array(info, ['shield'])
        self.handler._resolve_key_array(info, ['engine', 'battle_entity'])

        info['land_units_to_unit_abilites_junctions_tables'] = self.handler.get_entries_by_value('land_units_to_unit_abilites_junctions_tables', 'land_unit', info['key'])

        info['battle_personalities_grouped'] = None
        if info['battle_personalities'] is not None:
            info['battle_personalities_grouped'] = self._group_additional_personalities(info['battle_personalities'])
        return info

    def get_unit_info(self, name):
        info = self.handler.get_entry_by_index('main_units_tables', name)
        if info is None:
            return None
        return info

    def get_unit_animations(self, animation_key):
        res = {}
        anim_files = self.handler.anim_files
        try:
            unit_anim_list = anim_files['lookup'][f"animations/database/battle/bin/{animation_key}.bin"]['content'].find_all('animation')
        except KeyError as e:
            print(f'Missing bin: {e}')
            return None
        for anim in unit_anim_list:
            if 'attack' not in anim['slot'].lower() and 'charge' not in anim['slot'].lower():
                continue
            key = anim['slot']
            if 'attack' in anim['slot'].lower():
                key = '_'.join(anim['slot'].split('_')[:-1])
            res.setdefault(key, {})[anim['slot']] = {'blend_id': anim['blendid'], 'selection_weight': anim['selectionweight'], 'instances': []}
            for inst in anim.find_all('instance'):
                if inst['meta'] == "":
                    continue
                try:
                    meta = anim_files['lookup'][inst['meta']]['content']['Items']
                    res[key][anim['slot']]['instances'].append({'file_name': inst['meta'], 'meta': meta})
                except KeyError as e:
                    print(f"bin: {animation_key}, slot: {anim['slot']}, missing meta key: {e}")
        return res

    def get_ability_info(self, name):
        info = self.handler.get_entry_by_index('unit_abilities_tables', name)
        if info is None:
            return None
        info['unit_special_abilities_tables'] = self.handler.get_entry_by_index('unit_special_abilities_tables', info['key'])
        info['special_ability_intensity_settings_tables'] = self.handler.get_entry_by_index('special_ability_intensity_settings_tables', info['key'])
        self.handler._resolve_key_array(info, ['unit_special_abilities_tables', 'bombardment'])
        self.handler._resolve_key_array(info, ['unit_special_abilities_tables', 'vortex'])

        phases = None
        if info['unit_special_abilities_tables'] is not None:
            info['unit_special_abilities_tables']['special_ability_to_special_ability_phase_junctions_tables'] = \
                self.handler.get_entries_by_value('special_ability_to_special_ability_phase_junctions_tables', 'special_ability', info['unit_special_abilities_tables']['key'])
            phases = info['unit_special_abilities_tables'][
                'special_ability_to_special_ability_phase_junctions_tables']
        # reorder
        if phases is not None:
            phases.sort(key=lambda x: x['order'])
            info['unit_special_abilities_tables'][
                'special_ability_to_special_ability_phase_junctions_tables'] = phases
        return info

    def get_ability_phase_info(self, name):
        def sanitize(s):
            i0, i1 = s.find('[['), s.find(']]')
            while i0 != -1 and i1 != -1:
                s = s[:i0] + s[i1 + 2:]
                i0, i1 = s.find('[['), s.find(']]')
            return '_'.join([x.lower() for x in s.split(' ')]).replace("'", '').replace('"', '').replace('`', '').replace('!', '').replace(':', '').replace('&', '').replace('(', '').replace(')', '').replace('.', '').replace(',', '').replace('-', '_')

        info = self.handler.get_entry_by_index('special_ability_phases_tables', name)
        if info is None:
            return None
        info['special_ability_phase_stat_effects_tables'] = self.handler.get_entries_by_value('special_ability_phase_stat_effects_tables', 'phase', info['id'])
        info['special_ability_phase_attribute_effects_tables'] = self.handler.get_entries_by_value('special_ability_phase_attribute_effects_tables', 'phase', info['id'])

        # infer name
        sapt_j = self.handler.db['special_ability_to_special_ability_phase_junctions_tables'].data
        sel = sapt_j['phase'] == name
        if sel.any():
            ability_id = sapt_j[sel]['special_ability'].values[0]
            info['raw_name'] = self.handler.locs['unit_abilities__'].data.loc['unit_abilities_onscreen_name_' + ability_id]['text']#.values[0]
            info['sanitized_name'] = ability_id
        else:
            text = self.handler.locs['special_ability_phases__'].data.loc['special_ability_phases_onscreen_name_' + name]['text']
            info['raw_name'] = name if type(text) is float else text.split('\\\\n')[0]
            info['sanitized_name'] = name
        # info['sanitized_name'] = sanitize(info['raw_name'])
        return info

    def get_power_recharge(self):
        return self.handler.db['_kv_winds_of_magic_params_tables'].data.loc['restored_points_base', 'value']