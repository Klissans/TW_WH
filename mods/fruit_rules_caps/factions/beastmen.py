beastmen = {
    'special_rules': {

        'mortis_sr': (
            'Units With Passive Health Draining Ability',
            ['wh2_dlc17_bst_mon_jabberslythe_su'],
            1
        ),
    },


    'same_units': {
        'wh_dlc03_bst_inf_ungor_spearmen_su': ('Ungor Spearmen Herd', ['wh_dlc03_bst_inf_ungor_spearmen_0', 'wh_dlc03_bst_inf_ungor_spearmen_1', 'wh_pro04_bst_inf_ungor_spearmen_ror_0']),
        'wh_dlc03_bst_inf_gor_herd_su': ('Gor Herd', ['wh_dlc03_bst_inf_gor_herd_1', 'wh_pro04_bst_inf_gor_herd_ror_0']),
        'wh_dlc03_bst_inf_bestigor_herd_su': ('Bestigor Herd', ['wh_dlc03_bst_inf_bestigor_herd_0', 'wh_pro04_bst_inf_bestigor_herd_ror_0']),
        'wh_dlc03_bst_inf_centigors_su': ('Centigors', ['wh_dlc03_bst_inf_centigors_0', 'wh_pro04_bst_inf_centigors_ror_0']),
        'wh_dlc03_bst_inf_centigors_throwing_axes_su': ('Centigors (Throwing Axes)', ['wh_dlc03_bst_inf_centigors_1', 'wh2_dlc17_bst_inf_centigors_ror_1']),
        'wh_pro04_bst_inf_minotaurs_ror_shields_su': ('Minotaurs (Shields)', ['wh_dlc03_bst_inf_minotaurs_1', 'wh_pro04_bst_inf_minotaurs_ror_0']),
        'wh_dlc03_bst_inf_cygor_su': ('Cygor', ['wh_dlc03_bst_inf_cygor_0', 'wh_pro04_bst_inf_cygor_ror_0']),
        'wh2_dlc17_bst_mon_jabberslythe_su': ('Jabberslythe', ['wh2_dlc17_bst_mon_jabberslythe_0', 'wh2_dlc17_bst_mon_jabberslythe_ror_0']),
        'wh2_dlc17_bst_mon_ghorgon_su': ('Ghorgon', ['wh2_dlc17_bst_mon_ghorgon_0', 'wh2_dlc17_bst_mon_ghorgon_ror_0']),

        'wh2_dlc17_bst_cav_tuskgor_chariot_mount_su': (
            'Tuskgor Chariot Mount', ['wh2_dlc17_bst_cha_beastlord_2',
                                       'wh2_dlc17_bst_cha_khazrak_one_eye_2',
                                       'wh2_dlc17_bst_cha_bray_shaman_beasts_2',
                                       'wh2_dlc17_bst_cha_bray_shaman_death_2',
                                       'wh2_dlc17_bst_cha_bray_shaman_shadows_2',
                                       'wh2_dlc17_bst_cha_bray_shaman_wild_2',
                                       'wh2_dlc17_bst_cha_wargor_2',
                                       'wh2_twa04_bst_cha_great_bray_shaman_beasts_2',
                                       'wh2_twa04_bst_cha_great_bray_shaman_death_2',
                                       'wh2_twa04_bst_cha_great_bray_shaman_shadows_2',
                                       'wh2_twa04_bst_cha_great_bray_shaman_wild_2']),

        'wh2_dlc17_bst_cav_razorgor_chariot_mount_su': (
            'Razorgor Chariot Mount', ['wh_dlc03_bst_cha_beastlord_1',
                                       'wh_dlc03_bst_cha_khazrak_one_eye_1',
                                       'wh_dlc03_bst_cha_bray_shaman_beasts_1',
                                       'wh_dlc03_bst_cha_bray_shaman_death_1',
                                       'wh_dlc03_bst_cha_bray_shaman_shadows_1',
                                       'wh_dlc03_bst_cha_bray_shaman_wild_1',
                                       'wh2_dlc17_bst_cha_wargor_1',
                                       'wh2_twa04_bst_cha_great_bray_shaman_beasts_1',
                                       'wh2_twa04_bst_cha_great_bray_shaman_death_1',
                                       'wh2_twa04_bst_cha_great_bray_shaman_shadows_1',
                                       'wh2_twa04_bst_cha_great_bray_shaman_wild_1']),
    },

    'variant_units': {
        'wh_dlc03_bst_inf_ungor_spearmen_var': ('Ungor Herd', ['wh_dlc03_bst_inf_ungor_spearmen_su', 'wh_dlc03_bst_inf_ungor_herd_1']),
        'wh_dlc03_bst_inf_gor_herd_var': ('Gor Herd', ['wh_dlc03_bst_inf_gor_herd_su', 'wh_dlc03_bst_inf_gor_herd_0']),
        'wh_dlc03_bst_inf_centigors_var': ('Centigors', ['wh_dlc03_bst_inf_centigors_su', 'wh_dlc03_bst_inf_centigors_2']),
        'wh_dlc03_bst_inf_minotaurs_var': ('Minotaurs', ['wh_pro04_bst_inf_minotaurs_ror_shields_su', 'wh_dlc03_bst_inf_minotaurs_0', 'wh_dlc03_bst_inf_minotaurs_2']),
        'wh_dlc03_bst_inf_chaos_warhounds_var': ('Warhounds', ['wh_dlc03_bst_inf_chaos_warhounds_0', 'wh_dlc03_bst_inf_chaos_warhounds_1']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh_dlc03_bst_inf_ungor_spearmen_su',
        'wh_dlc03_bst_inf_ungor_herd_1',
        'wh_dlc03_bst_inf_gor_herd_su',
        'wh_dlc03_bst_inf_gor_herd_0',
        'wh_dlc03_bst_inf_bestigor_herd_su',
        'wh_dlc03_bst_inf_ungor_raiders_0',
    ],

    'multi_entity_chariots': [
        'wh2_dlc17_bst_cav_tuskgor_chariot_0',
        'wh_dlc03_bst_cav_razorgor_chariot_0',
    ],

    'multi_entity_other': [
        # mon
        'wh_dlc03_bst_inf_minotaurs_0',
        'wh_pro04_bst_inf_minotaurs_ror_shields_su',
        'wh_dlc03_bst_inf_minotaurs_2',
        'wh_dlc03_bst_mon_chaos_spawn_0',

        # cav
        'wh_dlc03_bst_inf_chaos_warhounds_0',
        'wh_dlc03_bst_inf_chaos_warhounds_1',
        'wh_dlc03_bst_inf_razorgor_herd_0',
        'wh_dlc03_bst_inf_centigors_su',
        'wh_dlc03_bst_inf_centigors_2',
        'wh_dlc03_bst_inf_centigors_throwing_axes_su',

        # fly
        'wh_dlc05_bst_mon_harpies_0',

        # art
    ],

    'exempt_single_entities': [
    ],

    'single_entity_all': [
    ],

    'single_entity_rare': [
        'wh2_dlc17_bst_cha_doombull_0',
        'wh_dlc03_bst_cha_gorebull_0',
        'wh2_dlc17_bst_cha_taurox_the_brass_bull_0',

        'wh_dlc03_bst_feral_manticore',
        'wh_dlc03_bst_mon_giant_0',
        'wh2_dlc17_bst_mon_jabberslythe_su',
        'wh2_dlc17_bst_mon_ghorgon_su',
        'wh_dlc03_bst_inf_cygor_su',
    ],

    'superweapon': [
    ],

    #----------------------------------
    # CATEGORIES

    'chariots': [
        'wh2_dlc17_bst_cav_tuskgor_chariot_mount_su',
        'wh2_dlc17_bst_cav_razorgor_chariot_mount_su',
    ],

    'flying_ranged': [
    ],

    'flying': [
        'wh_dlc03_bst_cha_malagor_the_dark_omen_0',

        'wh_dlc05_bst_mon_harpies_0',
        'wh_dlc03_bst_feral_manticore',
    ],

    'ranged_360': [
        'wh_dlc03_bst_inf_centigors_throwing_axes_su',
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
        'wh_dlc03_bst_inf_centigors_throwing_axes_su',
    ],

    # 'campaign_exclusive': [
    # ],


    'ranged_total': [
        #inf
        'wh_dlc03_bst_inf_ungor_raiders_0',

        #mon
        'wh_dlc03_bst_inf_cygor_su',

        #cav

        #cha


        #art
    ],


    # ROR
    'ror': [
        'wh_pro04_bst_inf_ungor_spearmen_ror_0',
        'wh_pro04_bst_inf_gor_herd_ror_0',
        'wh_pro04_bst_inf_bestigor_herd_ror_0',
        'wh_pro04_bst_inf_centigors_ror_0',
        'wh2_dlc17_bst_inf_centigors_ror_1',
        'wh_pro04_bst_inf_minotaurs_ror_0',
        'wh_pro04_bst_inf_cygor_ror_0',
        'wh2_dlc17_bst_mon_jabberslythe_ror_0',
        'wh2_dlc17_bst_mon_ghorgon_ror_0',
    ]

}
