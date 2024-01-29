norsca = {

    'same_units': {
        'wh_main_nor_inf_chaos_marauders_su': ('Marauders', ['wh_main_nor_inf_chaos_marauders_0', 'wh_pro04_nor_inf_chaos_marauders_ror_0']),
        'wh_dlc08_nor_inf_marauder_berserkers_su': ('Marauders Berserkers', ['wh_dlc08_nor_inf_marauder_berserkers_0', 'wh_pro04_nor_inf_marauder_berserkers_ror_0']),
        'wh_main_nor_mon_chaos_warhounds_su': ('Norscan Warhounds', ['wh_main_nor_mon_chaos_warhounds_0', 'wh_pro04_nor_mon_marauder_warwolves_ror_0']),
        'wh_dlc08_nor_mon_skinwolves_su': ('Skin Wolves', ['wh_dlc08_nor_mon_skinwolves_0', 'wh_dlc08_nor_mon_skinwolves_1', 'wh_pro04_nor_mon_skinwolves_ror_0']),
        'wh_dlc08_nor_mon_fimir_su': ('Fimir Warriors', ['wh_dlc08_nor_mon_fimir_0', 'wh_pro04_nor_mon_fimir_ror_0']),
        'wh_dlc08_nor_mon_frost_wyrm_su': ('Frost-Wyrm', ['wh_dlc08_nor_mon_frost_wyrm_0', 'wh_dlc08_nor_mon_frost_wyrm_ror_0']),
        'wh_dlc08_nor_mon_war_mammoth_su': ('Mammoth', ['wh_dlc08_nor_mon_war_mammoth_0', 'wh_dlc08_nor_mon_war_mammoth_1', 'wh_dlc08_nor_mon_war_mammoth_2', 'wh_pro04_nor_mon_war_mammoth_ror_0',
                                                        'wh_main_nor_cha_marauder_chieftan_3', 'wh_dlc08_nor_cha_wulfrik_3']),

        'wh_dlc08_nor_veh_marauder_chariot_mount_su': (
            'Marauder Chariot Mount', ['wh_main_nor_cha_marauder_chieftan_2',
                                      'wh_dlc08_nor_cha_wulfrik_2',
                                       'wh_dlc08_nor_cha_shaman_sorcerer_death_2',
                                       'wh_dlc08_nor_cha_shaman_sorcerer_fire_2',
                                       'wh_dlc08_nor_cha_shaman_sorcerer_metal_2']),
    },

    'variant_units': {
        'wh3_main_sla_inf_marauders_var': ('Marauders', ['wh_main_nor_inf_chaos_marauders_su', 'wh_main_nor_inf_chaos_marauders_1', 'wh_dlc08_nor_inf_marauder_spearman_0']),
        'wh_dlc08_nor_inf_marauder_hunters_var': ('Marauders Hunters', ['wh_dlc08_nor_inf_marauder_hunters_0', 'wh_dlc08_nor_inf_marauder_hunters_1']),
        'wh_dlc08_nor_inf_marauder_champions_var': ('Marauders Champions', ['wh_dlc08_nor_inf_marauder_champions_0', 'wh_dlc08_nor_inf_marauder_champions_1']),
        'wh_main_nor_cav_marauder_horsemen_var': ('Marauder Horsemen', ['wh_main_nor_cav_marauder_horsemen_0', 'wh_main_nor_cav_marauder_horsemen_1']),
        'wh_main_nor_mon_chaos_warhounds_var': ('Norscan Warhounds', ['wh_main_nor_mon_chaos_warhounds_su', 'wh_main_nor_mon_chaos_warhounds_1']),
        'wh_dlc08_nor_mon_fimir_var': ('Fimir Warriors', ['wh_dlc08_nor_mon_fimir_su', 'wh_dlc08_nor_mon_fimir_1']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh_main_nor_inf_chaos_marauders_su',
        'wh_main_nor_inf_chaos_marauders_1',
        'wh_dlc08_nor_inf_marauder_spearman_0',
        'wh_dlc08_nor_inf_marauder_berserkers_su',
        'wh_dlc08_nor_inf_marauder_champions_0',
        'wh_dlc08_nor_inf_marauder_champions_1',

        'wh_dlc08_nor_inf_marauder_hunters_0',
        'wh_dlc08_nor_inf_marauder_hunters_1',
    ],

    'multi_entity_chariots': [
        'wh_main_nor_cav_chaos_chariot',
        'wh_dlc08_nor_veh_marauder_warwolves_chariot_0',
    ],

    'multi_entity_other': [
        # mon
        'wh_main_nor_mon_chaos_warhounds_su',
        'wh_main_nor_mon_chaos_warhounds_1',
        'wh_dlc08_nor_mon_warwolves_0',
        'wh_main_nor_mon_chaos_trolls',
        'wh_dlc08_nor_mon_norscan_ice_trolls_0',
        'wh_dlc08_nor_mon_skinwolves_su',
        'wh_dlc08_nor_mon_fimir_su',
        'wh_dlc08_nor_mon_fimir_1',

        # cav
        'wh_main_nor_cav_marauder_horsemen_0',
        'wh_main_nor_cav_marauder_horsemen_1',
        'wh_dlc08_nor_cav_marauder_horsemasters_0',

        # fly

        # art
    ],

    # ----------------------------------
    # CATEGORIES

    'exempt_single_entities': [
    ],

    'single_entity_all': [
    ],

    'single_entity_rare': [
        'wh_dlc08_nor_feral_manticore',
        'wh_dlc08_nor_mon_norscan_giant_0',
        'wh_dlc08_nor_mon_war_mammoth_su',
        'wh_dlc08_nor_mon_frost_wyrm_su',
    ],

    'superweapon': [
    ],

    'chariots': [
        'wh_dlc08_nor_veh_marauder_chariot_mount_su',
    ],

    'flying_ranged': [
    ],

    'flying': [
        'wh_dlc08_nor_feral_manticore',
        'wh_dlc08_nor_mon_frost_wyrm_su',
    ],

    'ranged_360': [
        'wh_main_nor_cav_marauder_horsemen_0',
        'wh_main_nor_cav_marauder_horsemen_1',
        'wh_dlc08_nor_cav_marauder_horsemasters_0',
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
        'wh_main_nor_cav_marauder_horsemen_0',
        'wh_main_nor_cav_marauder_horsemen_1',
        'wh_dlc08_nor_cav_marauder_horsemasters_0',
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        # inf
        'wh_dlc08_nor_inf_marauder_hunters_0',
        'wh_dlc08_nor_inf_marauder_hunters_1',

        # mon

        # cav

        # cha

        # art
    ],

    # ROR
    'ror': [
        'wh_pro04_nor_inf_chaos_marauders_ror_0',
        'wh_pro04_nor_inf_marauder_berserkers_ror_0',
        'wh_pro04_nor_mon_marauder_warwolves_ror_0',
        'wh_pro04_nor_mon_skinwolves_ror_0',
        'wh_pro04_nor_mon_fimir_ror_0',
        'wh_pro04_nor_mon_war_mammoth_ror_0',
        'wh_dlc08_nor_mon_frost_wyrm_ror_0',
    ]

}
