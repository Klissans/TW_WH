tomb_kings = {

    'same_units': {
        'wh2_dlc09_tmb_inf_skeleton_spearmen_su': ('Skeleton Spearmen', ['wh2_dlc09_tmb_inf_skeleton_spearmen_0', 'wh2_dlc09_tmb_inf_skeleton_spearmen_ror']),
        'wh2_dlc09_tmb_inf_tomb_guard_su': ('Tomb Guard', ['wh2_dlc09_tmb_inf_tomb_guard_0', 'wh2_dlc09_tmb_inf_tomb_guard_ror']),
        'wh2_dlc09_tmb_inf_skeleton_archers_su': ('Skeleton Archers ', ['wh2_dlc09_tmb_inf_skeleton_archers_0', 'wh2_dlc09_tmb_inf_skeleton_archers_ror']),
        'wh2_dlc09_tmb_mon_ushabti_bow_su': ('Ushabti (Great Bow)', ['wh2_dlc09_tmb_mon_ushabti_1', 'wh2_dlc09_tmb_mon_ushabti_ror']),
        'wh2_dlc09_tmb_mon_sepulchral_stalkers_su': ('Sepulchar Stalkers', ['wh2_dlc09_tmb_mon_sepulchral_stalkers_0', 'wh2_dlc09_tmb_mon_sepulchral_stalkers_ror']),
        'wh2_dlc09_tmb_mon_necrosphinx_su': ('Necrosphinx', ['wh2_dlc09_tmb_mon_necrosphinx_0', 'wh2_dlc09_tmb_mon_necrosphinx_ror']),
        'wh2_dlc09_tmb_veh_khemrian_warsphinx_su': ('Khemrian Warspinx', ['wh2_dlc09_tmb_veh_khemrian_warsphinx_0', 'wh2_dlc09_tmb_cha_tomb_king_3', 'wh2_dlc09_tmb_cha_settra_3']),
        'wh2_dlc09_tmb_art_casket_of_souls_su': ('Casket of Souls', ['wh2_dlc09_tmb_art_casket_of_souls_0', 'wh2_dlc09_tmb_cha_khatep_3']),

        'wh2_dlc09_tmb_veh_skeleton_chariot_mount_su': (
            'Skeleton Chariot Mount', ['wh2_dlc09_tmb_cha_khalida_2',
                                       'wh2_dlc09_tmb_cha_tomb_king_2',
                                       'wh2_dlc09_tmb_cha_khatep_2',
                                       'wh2_dlc09_tmb_cha_arkhan_2',
                                       'wh2_dlc09_tmb_cha_necrotect_1',
                                       'wh2_dlc09_tmb_cha_tomb_prince_2',]),
    },

    'variant_units': {
        'wh2_dlc09_tmb_inf_skeleton_warriors_var': ('Skeletons Warriors', ['wh2_dlc09_tmb_inf_skeleton_warriors_0', 'wh2_dlc09_tmb_inf_skeleton_spearmen_su']),
        'wh2_dlc09_tmb_inf_tomb_guard_var': ('Tomb Guard', ['wh2_dlc09_tmb_inf_tomb_guard_su', 'wh2_dlc09_tmb_inf_tomb_guard_1']),
        'wh2_dlc09_tmb_cav_necropolis_knights_var': ('Necropolis Knights', ['wh2_dlc09_tmb_cav_necropolis_knights_0', 'wh2_dlc09_tmb_cav_necropolis_knights_1']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh2_dlc09_tmb_inf_skeleton_warriors_0',
        'wh2_dlc09_tmb_inf_skeleton_spearmen_su',
        'wh2_dlc09_tmb_inf_nehekhara_warriors_0',
        'wh2_dlc09_tmb_inf_tomb_guard_su',
        'wh2_dlc09_tmb_inf_tomb_guard_1',

        'wh2_dlc09_tmb_inf_skeleton_archers_su',
    ],

    'multi_entity_chariots': [
        'wh2_dlc09_tmb_veh_skeleton_chariot_0',
        'wh2_dlc09_tmb_veh_skeleton_archer_chariot_0',
    ],

    'multi_entity_other': [
        # mon
        'wh2_dlc09_tmb_mon_ushabti_0',
        'wh2_dlc09_tmb_mon_ushabti_bow_su',
        'wh2_dlc09_tmb_mon_sepulchral_stalkers_su',

        # cav
        'wh2_dlc09_tmb_cav_skeleton_horsemen_0',
        'wh2_dlc09_tmb_cav_nehekhara_horsemen_0',
        'wh2_dlc09_tmb_cav_necropolis_knights_0',
        'wh2_dlc09_tmb_cav_necropolis_knights_1',

        'wh2_dlc09_tmb_cav_skeleton_horsemen_archers_0',

        # fly
        'wh2_dlc09_tmb_mon_carrion_0',

        # art
        'wh2_dlc09_tmb_art_screaming_skull_catapult_0',
    ],

    #----------------------------------
    # CATEGORIES

    'exempt_single_entities': [
        'wh2_dlc09_tmb_art_casket_of_souls_su',
    ],

    'single_entity_all': [
    ],

    'single_entity_rare': [
        'wh2_dlc09_tmb_mon_tomb_scorpion_0',
        'wh2_pro06_tmb_mon_bone_giant_0',
        'wh2_dlc09_tmb_veh_khemrian_warsphinx_su',
        'wh2_dlc09_tmb_mon_necrosphinx_su',
        'wh2_dlc09_tmb_mon_heirotitan_0',
        'wh2_dlc09_tmb_cha_settra_2',
    ],

    'superweapon': [
        # 'wh2_dlc09_tmb_mon_heirotitan_0',
    ],

    'chariots': [
        'wh2_dlc09_tmb_veh_skeleton_chariot_mount_su',
    ],

    'flying_ranged': [
    ],

    'flying': [
        'wh2_dlc09_tmb_mon_carrion_0',
    ],

    'ranged_360': [
        'wh2_dlc09_tmb_cav_skeleton_horsemen_archers_0',
        'wh2_dlc09_tmb_veh_skeleton_archer_chariot_0',
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
        'wh2_dlc09_tmb_cav_skeleton_horsemen_archers_0',
        'wh2_dlc09_tmb_veh_skeleton_archer_chariot_0',
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        #inf
        'wh2_dlc09_tmb_inf_skeleton_archers_su',

        #mon
        'wh2_dlc09_tmb_mon_ushabti_bow_su',
        'wh2_dlc09_tmb_mon_sepulchral_stalkers_su',
        'wh2_pro06_tmb_mon_bone_giant_0',

        #cav

        #cha

        #art
        'wh2_dlc09_tmb_art_screaming_skull_catapult_0',
        'wh2_dlc09_tmb_art_casket_of_souls_su',
    ],


    # ROR
    'ror': [
        'wh2_dlc09_tmb_inf_skeleton_spearmen_ror',
        'wh2_dlc09_tmb_inf_tomb_guard_ror',
        'wh2_dlc09_tmb_inf_skeleton_archers_ror',
        'wh2_dlc09_tmb_mon_ushabti_ror',
        'wh2_dlc09_tmb_mon_sepulchral_stalkers_ror',
        'wh2_dlc09_tmb_mon_necrosphinx_ror',
    ]

}
