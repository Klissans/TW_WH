def beautify(s):
    return ' '.join([x.capitalize() for x in s.split('_')])

endl = '\\\\n'


def colorize(text, color):
    return f"[[col:{color}]]" + str(text) + "[[/col]]"

def highlight(text):
    return colorize(text, 'yellow')

def hmagic(text):
    return colorize(text, 'magic')

def _icon(name):
    return f"[[img:ui/skins/default/{name}.png]][[/img]]"

def _icon_ucat(name):
    return f"[[img:ui/common ui/unit_category_icons/{name}.png]][[/img]]"


def _icon_abil(name):
    return f"[[img:ui/battle ui/ability_icons/{name}.png]][[/img]]"

icost = _icon('icon_income')

class Utils:

    def __init__(self, handler, prefix):
        self.handler = handler

        self.mut_df = self.handler.db['main_units_tables'].data
        # self.lut_df = self.handler.db['land_units_tables'].data
        self.lu_loc = self.handler.locs['land_units__'].data
        self.ust_loc = self.handler.duplicate_table('unit_set_to_mp_unit_caps__', prefix=prefix, copy_data=False).data
        k = 'unit_set_to_mp_unit_caps_localised_name_mp_cap_group_extended_roster_chaos_marked_unitswh_main_sc_chs_chaos'
        self.ust_loc.loc[k] = {
            'key': k,
            'text': f"{_icon_abil('mark_khorne')}{_icon_abil('mark_nurgle')} {highlight('Units with a Mark of Chaos')} {_icon_abil('mark_slaanesh')}{_icon_abil('mark_tzeentch')}",
            'tooltip': False
        }
        self._datacore_tables()

        self.ust_df = self.handler.duplicate_table('unit_sets_tables', prefix=prefix, copy_data=False).data
        self.ustmuct_df = self.handler.duplicate_table('unit_set_to_mp_unit_caps_tables', prefix=prefix, copy_data=False).data
        self.ustujt_df = self.handler.duplicate_table('unit_set_to_unit_junctions_tables', prefix=prefix, copy_data=False).data

        #remove loc strings
        rls_core_df = self.handler.duplicate_table('random_localisation_strings__', prefix=prefix, copy_data=False).data
        k = 'random_localisation_strings_string_custom_battle_unit_tooltip_recruit'
        rls_core_df.loc[k] = {'key': k, 'text': '', 'tooltip': False}
        k = 'random_localisation_strings_string_left_click_pin'
        rls_core_df.loc[k] = {'key': k, 'text': '', 'tooltip': False}


        self.mp_price_caps = {
            'multi_entity_infantry': [(0, 5), (900, 4), (1100, 3)],
            'multi_entity_chariots': [(0, 3), (1200, 2)],
            'multi_entity_other': [(0, 4), (1200, 3)],
        }
#{_icon('icon_entity_large')}
        self.single_entity_total_key = self.add_unit_set('mp_single_entity_total', 5, f"{_icon_ucat('monstrous_infantry')}{highlight('SEU (Total)')}")

        self.single_entity_each_limit = 2
        self.ror_each_limit = 1
        # self.superweapon_key = self.add_unit_set('mp_superweapon', 1, f"{_icon_ucat('wh2_dlc11_cst_missile_monster')}{highlight('Superweapon')}")
        self.superweapon_limit_each = 1

        self.variants_limit = 8
        self.named_character_limit = 1

        self.chariots_key = self.add_unit_set('mp_chariots', 3, f"{_icon_ucat('chariot')}{highlight('Chariots')}")
        self.flying_ranged_key = self.add_unit_set('mp_flying_ranged', 4, f"{_icon_ucat('wh_dlc05_wef_hawk_riders')}{highlight('Ranged Flying Units')}")
        self.flying_key = self.add_unit_set('mp_flying', 6, f"{_icon_ucat('wh2_dlc09_tmb_carrion')}{highlight('Flying Units')}")
        self.ranged_360_key = self.add_unit_set('mp_ranged_360', 6, f"{_icon_ucat('wh2_dlc10_hef_handmaiden')}{highlight('Ranged Units 360')}")
        t = f"Ranged {_icon_ucat('missile_cavalry_bow')}Cavalry and {_icon_ucat('missile_chariot')}Chariots (MEU)"
        self.multi_entity_ranged_cavalry_and_chariots_key = self.add_unit_set('mp_multi_entity_ranged_cavalry_and_chariots', 6, f"{highlight(t)}")
        self.campaign_exclusive_key = self.add_unit_set('mp_campaign_exclusive', 0, f"{highlight('Campaign Exclusive')}")
        self.hero_key = self.add_unit_set('mp_heroes', 2, f"{_icon_ucat('hero')}{highlight('Heroes')}")
        self.single_entity_rare_army_key = self.add_unit_set('mp_single_entity_rare_army', 3, f"{_icon_ucat('wh_dlc03_bst_cygor')}{highlight('Rare SEU (Army)')}")
        self.ranged_total_key = self.add_unit_set('mp_ranged_total', 12, f"{_icon_ucat('missile_infantry_bow')}{highlight('Total Ranged Units')}")

        self.rare_seu_price_cap = self.add_unit_set('mp_rare_seu_price_cap', 3, f"{_icon_ucat('wh_dlc03_bst_cygor')}{highlight('Chariots')}")

        self.limit_heroes()
        self.limit_single_entites_total_lord_and_heroes()
        self.limit_named_characters()

        # hef avelorn trees
        self.hef_avelorn_trees = self.add_unit_set('mp_hef_avelorn_trees', 0, f"HE Avelorn trees", subculture='wh2_main_sc_hef_high_elves')
        unit_keys = ['wh2_dlc10_hef_inf_dryads_0', 'wh2_dlc10_hef_mon_treekin_0', 'wh2_dlc10_hef_mon_treeman_0']
        for su_key in unit_keys:
            self.add_unit_to_set(su_key, self.hef_avelorn_trees)


    def add_faction_limits(self, limits_definition):
        same_units = limits_definition['same_units']
        if 'special_rules' in limits_definition:
            for sr_key, (loc, unit_keys, limit) in limits_definition['special_rules'].items():
                self.add_unit_set(sr_key, limit,  f"{highlight(loc)} {hmagic('[Special Rule]')}")
                for unit_key in unit_keys:
                    if unit_key in same_units:
                        loc, unit_keys = same_units[unit_key]
                        for su_key in unit_keys:
                            self.add_unit_to_set(su_key, sr_key)
                    else:
                        self.add_unit_to_set(unit_key, sr_key)

        self.add_price_limits(limits_definition)
        self.add_variant(limits_definition['variant_units'], limits_definition['same_units'])

        single_entity_all_list = list(set(limits_definition['single_entity_all'] + limits_definition['single_entity_rare']) - set(limits_definition['exempt_single_entities']))
        self.add_by_unit_to_set(single_entity_all_list, self.single_entity_total_key, limits_definition['same_units'])

        # self.add_by_unit_to_set(limits_definition['superweapon'], self.superweapon_key, limits_definition['same_units'])

        l = list(set(limits_definition['chariots'] + limits_definition['multi_entity_chariots']))
        self.add_by_unit_to_set(l, self.chariots_key, limits_definition['same_units'])

        self.add_by_unit_to_set(limits_definition['flying_ranged'], self.flying_ranged_key, limits_definition['same_units'])

        self.add_by_unit_to_set(limits_definition['flying'] + limits_definition['flying_ranged'], self.flying_key, limits_definition['same_units'])

        self.add_by_unit_to_set(limits_definition['ranged_360'], self.ranged_360_key, limits_definition['same_units'])

        self.add_by_unit_to_set(limits_definition['multi_entity_ranged_cavalry_and_chariots'], self.multi_entity_ranged_cavalry_and_chariots_key, limits_definition['same_units'])

        # self.add_by_unit_to_set(limits_definition['campaign_exclusive'], self.campaign_exclusive_key, limits_definition['same_units'])

        self.add_by_unit_to_set(limits_definition['single_entity_rare'], self.single_entity_rare_army_key, limits_definition['same_units'])

        l = list(set(limits_definition['ranged_total'] + limits_definition['flying_ranged'] + limits_definition['ranged_360']))
        self.add_by_unit_to_set(l, self.ranged_total_key, limits_definition['same_units'])

        l = list(set(single_entity_all_list + limits_definition['exempt_single_entities'])) # - set(limits_definition['superweapon'])
        self.add_single_entity_each(l, limits_definition['same_units'])

        self.add_ror(limits_definition['ror'])
        self.add_superweapon(limits_definition['superweapon'], limits_definition['same_units'])


    def _get_cheapest_price(self, unit_keys):
        min_price = 99999
        for uk in unit_keys:
            unit_price = self.mut_df.loc[uk, 'multiplayer_cost']
            if unit_price < min_price:
                min_price = unit_price
        return min_price

    def _get_unit_price(self, key):
        return self.mut_df.loc[key, 'multiplayer_cost']

    def _unit_name_lookup(self, key):
        return self.lu_loc.loc[f"land_units_onscreen_name_{self.mut_df.loc[key, 'land_unit']}", 'text']

    # Shielded units are considered the same unit as their unshielded variants when they cost more.
    def add_price_limits(self, limits_definition):
        unit_types_map = {
            'multi_entity_infantry': 'MEU-Infantry',
            'multi_entity_chariots': 'MEU-Chariots',
            'multi_entity_other': 'MEU-Other',
            'single_entity_all': 'SEU-All',
        }
        for unit_type in self.mp_price_caps.keys():
            price_caps_reversed = self.mp_price_caps[unit_type][::-1]
            for unit_key in limits_definition[unit_type]:
                if unit_key in limits_definition['same_units']:
                    loc, unit_keys = limits_definition['same_units'][unit_key]
                    cheapest_price = self._get_cheapest_price(unit_keys)
                    #add cap for the same units based on the cheapest (should be first in the list) unit
                    for i, (price_th, cap) in enumerate(price_caps_reversed):
                        if cheapest_price > price_th:
                            if i == 0:
                                t = f"{highlight(loc)} {hmagic('[Same Unit]')}{endl}({unit_types_map[unit_type]} {icost}{price_th+1}+)"
                            else:
                                t = f"{highlight(loc)} {hmagic('[Same Unit]')}{endl}({unit_types_map[unit_type]} {icost}{price_th+1}-{price_caps_reversed[i-1][0]})"
                            self.add_unit_set(unit_key, cap, t)
                            for su_key in unit_keys:
                                self.add_unit_to_set(su_key, unit_key)
                            break

                    #add cap for each unit in same unit group based on their own price
                    for su_key in unit_keys:
                        unit_price = self._get_unit_price(su_key)
                        for i, (price_th, cap) in enumerate(price_caps_reversed):
                            if unit_price > price_th:
                                if i == 0:
                                    t = f"{highlight(self._unit_name_lookup(su_key))}{endl}({unit_types_map[unit_type]} {icost}{price_th+1}+)"
                                else:
                                    t = f"{highlight(self._unit_name_lookup(su_key))}{endl}({unit_types_map[unit_type]} {icost}{price_th+1}-{price_caps_reversed[i-1][0]})"
                                self.add_unit_to_set(su_key, self.add_unit_set(su_key, cap, t))
                                break
                else:
                    for i, (price_th, cap) in enumerate(price_caps_reversed):
                        unit_price = self._get_unit_price(unit_key)
                        if unit_price > price_th:
                            if i == 0:
                                t = f"{highlight(self._unit_name_lookup(unit_key))}{endl}({unit_types_map[unit_type]} {icost}{price_th+1}+)"
                            else:
                                t = f"{highlight(self._unit_name_lookup(unit_key))}{endl}({unit_types_map[unit_type]} {icost}{price_th+1}-{price_caps_reversed[i-1][0]})"
                            self.add_unit_to_set(unit_key, self.add_unit_set(unit_key, cap, t))
                            break

    # Units with minor variations like added armor or different weapon types are classified as variants.
    def add_variant(self, variant_keys, same_units):
        for var_key, (var_loc, unit_list) in variant_keys.items():
            self.add_unit_set(var_key, self.variants_limit, f"{highlight(var_loc)} {hmagic('[Variants]')}")
            for unit_key in unit_list:
                if unit_key in same_units:
                    loc, unit_keys = same_units[unit_key]
                    for su_key in unit_keys:
                        self.add_unit_to_set(su_key, var_key)
                else:
                    self.add_unit_to_set(unit_key, var_key)


    def add_by_unit_to_set(self, unit_keys, set_key, same_units):
        for k in unit_keys:
            if k in same_units:
                loc, unit_keys = same_units[k]
                for su_key in unit_keys:
                    self.add_unit_to_set(su_key, set_key)
            else:
                self.add_unit_to_set(k, set_key)

    def add_single_entity_each(self, keys, same_units):
        for k in keys:
            if k in same_units:
                loc, unit_keys = same_units[k]
                self.add_unit_set(k, self.single_entity_each_limit,
                                  f"{highlight(loc)} SEU (Each)")
                for su_key in unit_keys:
                    self.add_unit_to_set(su_key, k)
            else:
                self.add_unit_set(k, self.single_entity_each_limit,
                                  f"{highlight(self._unit_name_lookup(k))} SEU (Each)")
                self.add_unit_to_set(k, k)

    def add_ror(self, ror_keys):
        for k in ror_keys:
            self.add_unit_set(k, self.ror_each_limit, f"{highlight(self._unit_name_lookup(k))}{hmagic('[RoR]')}")
            self.add_unit_to_set(k, k)

    def add_superweapon(self, keys, same_units):
        for k in keys:
            if k in same_units:
                loc, unit_keys = same_units[k]
                usk = self.add_unit_set('superweapon_' + k, self.superweapon_limit_each, f"{_icon_ucat('wh2_dlc11_cst_missile_monster')}{highlight(loc)} {hmagic('[Superweapon]')}")
                for su_key in unit_keys:
                    self.add_unit_to_set(su_key, usk)
            else:
                usk = self.add_unit_set('superweapon_' + k, self.superweapon_limit_each, f"{_icon_ucat('wh2_dlc11_cst_missile_monster')}{highlight(self._unit_name_lookup(k))} {hmagic('[Superweapon]')}")
                self.add_unit_to_set(k, usk)

    def _datacore_tables(self):
        df = self.handler.db['unit_set_to_mp_unit_caps_tables'].data
        vanilla_mp_sets = set(df['unit_set'].tolist()) - \
                          set(df[df['unit_set'].str.contains('extended_roster')]['unit_set'].tolist()) - \
                          set(df[df['unit_set'].str.contains('marked_units')]['unit_set'].tolist())
        # remove all vanilla mp caps
        ustmuct_core_df = self.handler.duplicate_table('unit_set_to_mp_unit_caps_tables', new_name='data__', copy_data=True).data
        ustmuct_core_df.drop(ustmuct_core_df[ustmuct_core_df.unit_set.isin(vanilla_mp_sets)].index, inplace=True)

        core_df = self.handler.duplicate_table('banners_permitted_unit_sets_tables', new_name='data__', copy_data=True).data
        core_df.drop(core_df[core_df.unit_set.isin(vanilla_mp_sets)].index, inplace=True)

        core_df = self.handler.duplicate_table('effect_bonus_value_ids_unit_sets_tables', new_name='data__', copy_data=True).data
        core_df.drop(core_df[core_df.unit_set.isin(vanilla_mp_sets)].index, inplace=True)

        core_df = self.handler.duplicate_table('unit_set_special_ability_phase_junctions_tables', new_name='data__', copy_data=True).data
        core_df.drop(core_df[core_df.unit_set.isin(vanilla_mp_sets)].index, inplace=True)

        core_df = self.handler.duplicate_table('unit_set_unit_ability_junctions_tables', new_name='data__', copy_data=True).data
        core_df.drop(core_df[core_df.unit_set.isin(vanilla_mp_sets)].index, inplace=True)

        core_df = self.handler.duplicate_table('unit_set_unit_attribute_junctions_tables', new_name='data__', copy_data=True).data
        core_df.drop(core_df[core_df.unit_set.isin(vanilla_mp_sets)].index, inplace=True)

        ust_core_df = self.handler.duplicate_table('unit_sets_tables', new_name='data__', copy_data=True).data
        ust_core_df.drop(ust_core_df[ust_core_df.key.isin(vanilla_mp_sets)].index, inplace=True)

        ustujt_core_df = self.handler.duplicate_table('unit_set_to_unit_junctions_tables', new_name='data__', copy_data=True).data
        ustujt_core_df.drop(ustujt_core_df[ustujt_core_df.unit_set.isin(vanilla_mp_sets)].index, inplace=True)
        ustujt_core_df.drop(ustujt_core_df[ustujt_core_df.unit_record.isin(['wh2_dlc10_hef_inf_dryads_0', 'wh2_dlc10_hef_mon_treekin_0', 'wh2_dlc10_hef_mon_treeman_0'])].index, inplace=True)


    def add_unit_set(self, key, cap, desc, subculture=None):
        self.ust_df.loc[key] = {
            'key': key,
            'use_unit_exp_level_range': False,
            'min_unit_exp_level_inclusive': -1,
            'max_unit_exp_level_inclusive': -1,
            'special_category': None
        }
        self.ustmuct_df.loc[key] = {
            'unit_set': key,
            'cap': cap,
            'subculture': subculture,
        }
        self.ust_loc.loc[key] = {
            'key': 'unit_set_to_mp_unit_caps_localised_name_' + key,
            'text': desc,
            'tooltip': False
        }
        return key

    def add_unit_to_set(self, unit_key, set_key):
        # (set_key, unit_key, None, None, None)
        self.ustujt_df.loc[set_key + unit_key] = {
            'unit_set': set_key,
            'unit_record': unit_key,
            'unit_caste': None,
            'unit_category': None,
            'unit_class': None,
            'exclude': False
        }


    def limit_single_entites_total_lord_and_heroes(self):
        for index, data in self.mut_df[(self.mut_df['caste'] == 'hero') | (self.mut_df['caste'] == 'lord')].iterrows():
            self.add_unit_to_set(data['unit'], self.single_entity_total_key)


    def limit_named_characters(self):
        named_characters = {
            'wh2_pro08_neu_cha_gotrek': ('Gotrek', ['wh2_pro08_neu_cha_gotrek']),
            'wh2_pro08_neu_cha_felix': ('Felix', ['wh2_pro08_neu_cha_felix']),
            'wh2_dlc17_dwf_cha_thane_ghost_2': ('Hans Valhirsson', ['wh2_dlc17_dwf_cha_thane_ghost_2']),
            'wh_dlc07_brt_cha_green_knight_0': ('The Green Knight', ['wh_dlc07_brt_cha_green_knight_0']),
            'wh2_dlc14_brt_cha_henri_le_massif': ('Henri le Massif', ['wh2_dlc14_brt_cha_henri_le_massif_0', 'wh2_dlc14_brt_cha_henri_le_massif_3', 'wh2_dlc14_brt_cha_henri_le_massif_4']),
            'wh2_dlc12_lzd_lzd_cha_kroak_0': ('Lord Kroak', ['wh2_dlc12_lzd_lzd_cha_kroak_0']),
            'wh2_dlc16_skv_cha_ghoritch_0': ('Ghoritch', ['wh2_dlc16_skv_cha_ghoritch_0']),
            'mp_cap_hero_ariel': ('Ariel', ['wh2_dlc16_wef_cha_ariel_0']),
        }
        for set_k, (loc, unit_ks) in named_characters.items():
            self.add_unit_set(set_k, self.named_character_limit, f"{highlight(loc)} {hmagic('[Named Character]')}")
            for unit_k in unit_ks:
                self.add_unit_to_set(unit_k, set_k)

    def limit_heroes(self):
        for index, data in self.mut_df[self.mut_df['caste'] == 'hero'].iterrows():
            self.add_unit_to_set(data['unit'], self.hero_key)

        l = ['wh_dlc08_nor_cha_skin_wolf_werekin_0']
        for k in l:
            self.add_unit_to_set(k, self.hero_key)


    def get_faction_units(self, faction_id:str):
        ucbpt_orig_df = self.handler.db['units_custom_battle_permissions_tables'].data
        return ucbpt_orig_df[ucbpt_orig_df['faction'] == faction_id]['unit'].tolist()