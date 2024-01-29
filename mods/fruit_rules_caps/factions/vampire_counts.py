vampire_counts = {

    'special_rules': {
        'flying_breath_attack_sr': (
            'Flying Units with Breath Attack',
            ['wh_main_vmp_mon_terrorgheist_su',
             'wh_main_vmp_mon_mount_zombie_dragon_su'],
            2
        ),

        'mortis_sr': (
            'Units With Passive Health Draining Ability',
            ['wh_dlc04_vmp_veh_mortis_engine_su',
             'wh_dlc04_vmp_cha_helman_ghorst_1'],
            1
        ),
    },

    'same_units': {
        'wh_main_vmp_inf_zombie_su': ('Zombies', ['wh_main_vmp_inf_zombie', 'wh_dlc04_vmp_inf_tithe_0']),
        'wh_main_vmp_inf_skeleton_warriors_su': ('Skeletons Warriors', ['wh_main_vmp_inf_skeleton_warriors_0', 'wh_dlc04_vmp_inf_konigstein_stalkers_0']),
        'wh_main_vmp_inf_crypt_ghouls_su': ('Exalted', ['wh_main_vmp_inf_crypt_ghouls', 'wh_dlc04_vmp_inf_feasters_in_the_dusk_0']),
        'wh_main_vmp_inf_grave_guard_shields_su': ('Grave Guard (Shields)', ['wh_main_vmp_inf_grave_guard_0', 'wh_dlc04_vmp_inf_sternsmen_0']),
        'wh_main_vmp_cav_black_knights_lances_su': ('Black Knights (Lances & Barding)', ['wh_main_vmp_cav_black_knights_3', 'wh_dlc04_vmp_cav_vereks_reavers_0']),
        'wh_main_vmp_cav_hexwraiths_su': ('Hexwraith', ['wh_main_vmp_cav_hexwraiths', 'wh_dlc04_vmp_cav_chillgheists_0']),
        'wh_main_vmp_mon_dire_wolves_su': ('Dire Wolves', ['wh_main_vmp_mon_dire_wolves', 'wh_dlc04_vmp_mon_direpack_0']),
        'wh_main_vmp_mon_vargheists_su': ('Vargheists', ['wh_main_vmp_mon_vargheists', 'wh_dlc04_vmp_mon_devils_swartzhafen_0']),
        'wh_dlc04_vmp_veh_mortis_engine_su': ('Mortis Engine', ['wh_dlc04_vmp_veh_mortis_engine_0', 'wh_dlc04_vmp_veh_claw_of_nagash_0']),

        'wh_main_vmp_mon_terrorgheist_su': (
        'Terrorgheist', ['wh_main_vmp_mon_terrorgheist', 'wh_dlc04_vmp_cha_strigoi_ghoul_king_1', 'wh2_dlc11_vmp_cha_bloodline_strigoi_lord_1']),

        'wh_main_vmp_mon_mount_zombie_dragon_su': (
        'Zombie Dragon', ['wh_main_vmp_cha_vampire_lord_3', 'wh2_dlc11_vmp_cha_bloodline_blood_dragon_lord_3', 'wh2_dlc11_vmp_cha_bloodline_lahmian_lord_3',
                          'wh2_dlc11_vmp_cha_bloodline_necrarch_lord_3', 'wh2_dlc11_vmp_cha_bloodline_von_carstein_lord_3', 'wh_dlc05_vmp_cha_red_duke_3', 'wh_main_vmp_cha_mannfred_von_carstein_3']),

        'wh_main_vmp_mon_mount_hellsteed_su': (
        'Hellsteed Mount', ['wh_main_vmp_cha_vampire_lord_2', 'wh2_dlc11_vmp_cha_bloodline_blood_dragon_lord_2', 'wh2_dlc11_vmp_cha_bloodline_lahmian_lord_2',
                          'wh2_dlc11_vmp_cha_bloodline_necrarch_lord_2', 'wh2_dlc11_vmp_cha_bloodline_von_carstein_lord_2', 'wh_dlc05_vmp_cha_red_duke_1', 'wh_main_vmp_cha_mannfred_von_carstein_2',
                            'wh_main_vmp_cha_master_necromancer_4', 'wh_pro02_vmp_cha_isabella_von_carstein_2', 'wh_dlc05_vmp_cha_vampire_shadows_2', 'wh_main_vmp_cha_vampire_2']),

        'wh_dlc04_vmp_veh_corpse_cart_su': ('Corpse Cart',
                                             ['wh_dlc04_vmp_veh_corpse_cart_0', 'wh_dlc04_vmp_cha_master_necromancer_1', 'wh_dlc04_vmp_cha_necromancer_1']),

        'wh_dlc04_vmp_veh_corpse_cart_balefire_su': ('Corpse Cart (Balefire)',
                                             ['wh_dlc04_vmp_veh_corpse_cart_1', 'wh_dlc04_vmp_cha_master_necromancer_2', 'wh_dlc04_vmp_cha_necromancer_2']),

        'wh_dlc04_vmp_veh_corpse_cart_unholy_lodestone_su': ('Corpse Cart (Unholy Lodestone)',
                                             ['wh_dlc04_vmp_veh_corpse_cart_2', 'wh_dlc04_vmp_cha_master_necromancer_3', 'wh_dlc04_vmp_cha_necromancer_3']),
    },

    'variant_units': {
        'wh_main_vmp_inf_skeleton_warriors_var': ('Skeletons', ['wh_main_vmp_inf_skeleton_warriors_su', 'wh_main_vmp_inf_skeleton_warriors_1']),
        'wh_main_vmp_inf_grave_guard_var': ('Grave Guard', ['wh_main_vmp_inf_grave_guard_shields_su', 'wh_main_vmp_inf_grave_guard_1']),
        'wh_main_vmp_cav_black_knights_var': ('Black Knights', ['wh_main_vmp_cav_black_knights_0', 'wh_main_vmp_cav_black_knights_lances_su']),
        'wh_dlc04_vmp_veh_corpse_cart_var': ('Corpse Cart', ['wh_dlc04_vmp_veh_corpse_cart_su', 'wh_dlc04_vmp_veh_corpse_cart_balefire_su', 'wh_dlc04_vmp_veh_corpse_cart_unholy_lodestone_su']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh_main_vmp_inf_zombie_su',
        'wh_main_vmp_inf_skeleton_warriors_su',
        'wh_main_vmp_inf_skeleton_warriors_1',
        'wh_main_vmp_inf_crypt_ghouls_su',
        'wh_main_vmp_inf_cairn_wraiths',
        'wh_main_vmp_inf_grave_guard_shields_su',
        'wh_main_vmp_inf_grave_guard_1',

    ],

    'multi_entity_chariots': [
    ],

    'multi_entity_other': [
        # mon
        'wh_main_vmp_mon_crypt_horrors',

        # cav
        'wh_main_vmp_mon_dire_wolves_su',
        'wh_main_vmp_cav_black_knights_0',
        'wh_main_vmp_cav_black_knights_lances_su',
        'wh_dlc02_vmp_cav_blood_knights_0',
        'wh_main_vmp_cav_hexwraiths_su',

        # fly
        'wh_main_vmp_mon_fell_bats',
        'wh_main_vmp_mon_vargheists_su',

        # art
    ],

    #----------------------------------
    # CATEGORIES

    'exempt_single_entities': [
        'wh_dlc04_vmp_veh_corpse_cart_su',
        'wh_dlc04_vmp_veh_corpse_cart_balefire_su',
        'wh_dlc04_vmp_veh_corpse_cart_unholy_lodestone_su',
    ],

    'single_entity_all': [
    ],

    'single_entity_rare': [
        'wh_main_vmp_veh_black_coach',
        'wh_main_vmp_mon_varghulf',
        'wh_main_vmp_mon_terrorgheist',
        'wh_dlc04_vmp_veh_mortis_engine_su',
        'wh_main_vmp_mon_mount_zombie_dragon_su',
    ],

    'superweapon': [
    ],


    'chariots': [
        'wh_main_vmp_veh_black_coach',
        'wh_dlc04_vmp_veh_mortis_engine_su',
    ],

    'flying_ranged': [
    ],

    'flying': [
        'wh_main_vmp_mon_fell_bats',
        'wh_main_vmp_mon_vargheists_su',
        'wh_main_vmp_mon_terrorgheist_su',
        'wh_main_vmp_mon_mount_zombie_dragon_su',
        'wh_main_vmp_mon_mount_hellsteed_su',
    ],

    'ranged_360': [
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        #inf

        #mon

        #cav

        #cha

        #art
    ],


    # ROR
    'ror': [
        'wh_dlc04_vmp_inf_tithe_0',
        'wh_dlc04_vmp_inf_konigstein_stalkers_0',
        'wh_dlc04_vmp_inf_feasters_in_the_dusk_0',
        'wh_dlc04_vmp_inf_sternsmen_0',
        'wh_dlc04_vmp_cav_vereks_reavers_0',
        'wh_dlc04_vmp_cav_chillgheists_0',
        'wh_dlc04_vmp_mon_direpack_0',
        'wh_dlc04_vmp_mon_devils_swartzhafen_0',
        'wh_dlc04_vmp_veh_claw_of_nagash_0',
    ]

}
