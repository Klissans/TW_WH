tzeentch = {

    'same_units': {
        'wh3_main_tze_inf_pink_horrors_exalted_su': ('Exalted Pink Horrors', ['wh3_main_tze_inf_pink_horrors_1', 'wh3_twa06_tze_inf_pink_horrors_ror_0']),
        'wh3_main_tze_cav_doom_knights_su': ('Doom Knights', ['wh3_main_tze_cav_doom_knights_0', 'wh3_twa07_tze_cav_doom_knights_ror_0']),
        'wh3_main_tze_mon_lord_of_change_su': ('Lord of Change', ['wh3_main_tze_mon_lord_of_change_0',
                                                                  'wh_main_chs_cha_lord_of_change_0',
                                                                  'wh3_main_tze_cha_exalted_lord_of_change_metal_0',
                                                                  'wh3_main_tze_cha_exalted_lord_of_change_tzeentch_0',
                                                                  'wh3_main_tze_cha_kairos_fateweaver_custom_battle_0']),

        'wh3_main_tze_veh_burning_chariot_su': ('Burning Chariot', ['wh3_main_tze_veh_burning_chariot_0',
                                                                    'wh3_main_tze_cha_herald_of_tzeentch_metal_2',
                                                                    'wh3_main_tze_cha_herald_of_tzeentch_tzeentch_2',
                                                                    'wh3_main_tze_cha_iridescent_horror_metal_2',
                                                                    'wh3_main_tze_cha_iridescent_horror_tzeentch_2']),


#--------------------------------------
        'wh3_main_tze_cha_herald_horror_of_tzeentch_su': ('Herald/Horror on foot', ['wh3_main_tze_cha_herald_of_tzeentch_metal_0',
                                                                                   'wh3_main_tze_cha_herald_of_tzeentch_tzeentch_0',
                                                                                   'wh3_main_tze_cha_iridescent_horror_metal_0',
                                                                                   'wh3_main_tze_cha_iridescent_horror_tzeentch_0']),

        'wh3_main_tze_cha_herald_horror_of_tzeentch_on_disk_su': ('Herald/Horror on disk', ['wh3_main_tze_cha_herald_of_tzeentch_metal_1',
                                                                                           'wh3_main_tze_cha_herald_of_tzeentch_tzeentch_1',
                                                                                           'wh3_main_tze_cha_iridescent_horror_metal_1',
                                                                                           'wh3_main_tze_cha_iridescent_horror_tzeentch_1']),

    },

    'variant_units': {
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh3_main_tze_inf_blue_horrors_0',
        'wh3_main_tze_inf_pink_horrors_0',
        'wh3_main_tze_inf_pink_horrors_exalted_su',
        # 'wh3_main_tze_inf_forsaken_0',
    ],

    'multi_entity_chariots': [
    ],

    'multi_entity_other': [
        # mon
        'wh3_main_tze_mon_flamers_0',
        # 'wh3_main_tze_mon_spawn_of_tzeentch_0',

        # cav
        # 'wh3_main_tze_cav_chaos_knights_0',

        # fly
        'wh3_main_tze_inf_chaos_furies_0',
        'wh3_main_tze_mon_screamers_0',
        'wh3_main_tze_cav_doom_knights_su',

        # art
    ],

    # ----------------------------------
    # CATEGORIES
    'exempt_single_entities': [
    ],

    'single_entity_all': [
        'wh3_main_tze_veh_burning_chariot_su',
        'wh3_main_tze_mon_exalted_flamers_0',
    ],

    'single_entity_rare': [
        'wh3_main_tze_mon_lord_of_change_su',
        # 'wh3_main_tze_mon_soul_grinder_0',
    ],

    'superweapon': [
    ],

    'chariots': [
        # 'wh3_main_tze_veh_burning_chariot_su', # doesn't have collision attacks
    ],

    'flying_ranged': [
        'wh3_main_tze_cha_herald_horror_of_tzeentch_on_disk_su',
        'wh3_main_tze_veh_burning_chariot_su',
    ],

    'flying': [
        'wh3_main_tze_inf_chaos_furies_0',
        'wh3_main_tze_mon_screamers_0',
        'wh3_main_tze_cav_doom_knights_su',
        'wh3_main_tze_mon_lord_of_change_su',
    ],

    'ranged_360': [
        'wh3_main_tze_cha_herald_horror_of_tzeentch_su',
        'wh3_main_tze_cha_herald_horror_of_tzeentch_on_disk_su',
        'wh3_main_tze_veh_burning_chariot_su',
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        # inf
        'wh3_main_tze_inf_blue_horrors_0',
        'wh3_main_tze_inf_pink_horrors_0',
        'wh3_main_tze_inf_pink_horrors_exalted_su',

        # mon
        'wh3_main_tze_mon_flamers_0',
        'wh3_main_tze_mon_exalted_flamers_0',

        # cav

        # cha

        # art
    ],

    # ROR
    'ror': [
        'wh3_twa06_tze_inf_pink_horrors_ror_0',
        'wh3_twa07_tze_cav_doom_knights_ror_0',
    ]

}
