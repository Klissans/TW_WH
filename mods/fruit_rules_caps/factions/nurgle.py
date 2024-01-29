nurgle = {

    'special_rules': {
        'mortis_sr': (
            'Units With Passive Health Draining Ability',
            ['wh3_dlc20_nur_cha_festus'],
            1
        ),
    },

    'same_units': {
        'wh3_main_nur_inf_plaguebearers_exalted_su': ('Exalted Plaguebearers', ['wh3_main_nur_inf_plaguebearers_1', 'wh3_twa06_nur_inf_plaguebearers_ror_0']),
        'wh3_main_nur_cav_pox_riders_of_nurgle_su': ('Pox Riders', ['wh3_main_nur_cav_pox_riders_of_nurgle_0', 'wh3_twa07_nur_cav_pox_riders_of_nurgle_ror_0']),
        'wh3_main_nur_mon_great_unclean_one_su': ('Great Unclean One', ['wh3_main_nur_mon_great_unclean_one_0', 'wh3_main_nur_cha_exalted_great_unclean_one_death_0', 'wh3_main_nur_cha_exalted_great_unclean_one_nurgle_0', 'wh3_main_nur_cha_ku_gath_plaguefather_0']),

#--------------------------------------
        'wh3_main_tze_cha_mount_rot_fly_su': ('Rot Fly Mount', ['wh3_main_nur_cha_herald_of_nurgle_death_2',
                                                                                   'wh3_main_nur_cha_herald_of_nurgle_nurgle_2',
                                                                                   'wh3_main_nur_cha_plagueridden_death_2',
                                                                                   'wh3_main_nur_cha_plagueridden_nurgle_2']),
    },

    'variant_units': {
        'wh3_main_nur_cav_plague_drones_var': ('Plague Drones', ['wh3_main_nur_cav_plague_drones_0', 'wh3_main_nur_cav_plague_drones_1']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh3_main_nur_inf_nurglings_0',
        # 'wh3_main_nur_inf_forsaken_0',
        'wh3_main_nur_inf_plaguebearers_0',
        'wh3_main_nur_inf_plaguebearers_exalted_su',

    ],

    'multi_entity_chariots': [
    ],

    'multi_entity_other': [
        # mon
        # 'wh3_main_nur_mon_spawn_of_nurgle_0',

        # cav
        'wh3_main_nur_mon_plague_toads_0',
        'wh3_main_nur_cav_pox_riders_of_nurgle_su',

        # fly
        'wh3_main_nur_inf_chaos_furies_0',
        'wh3_main_nur_mon_rot_flies_0',
        'wh3_main_nur_cav_plague_drones_0',
        'wh3_main_nur_cav_plague_drones_1',

        # art
    ],

    'exempt_single_entities': [
    ],

    'single_entity_all': [
        'wh3_main_nur_mon_beast_of_nurgle_0',
    ],

    'single_entity_rare': [
        'wh3_main_nur_mon_great_unclean_one_su',
        # 'wh3_main_nur_mon_soul_grinder_0',
    ],

    'superweapon': [
    ],

    #----------------------------------
    # CATEGORIES

    'chariots': [
    ],

    'flying_ranged': [
        'wh3_main_nur_cav_plague_drones_1',
    ],

    'flying': [
        'wh3_main_nur_inf_chaos_furies_0',
        'wh3_main_nur_mon_rot_flies_0',
        'wh3_main_nur_cav_plague_drones_0',
        'wh3_main_tze_cha_mount_rot_fly_su',
    ],

    'ranged_360': [
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        #inf
        'wh3_main_nur_inf_plaguebearers_exalted_su',

        #cav

        #cha

        #art
        'wh3_main_nur_mon_soul_grinder_0',
        'wh3_main_nur_cha_ku_gath_plaguefather_0',
    ],


    # ROR
    'ror': [
        'wh3_twa06_nur_inf_plaguebearers_ror_0',
        'wh3_twa07_nur_cav_pox_riders_of_nurgle_ror_0',
    ]

}
