bretonnia = {

    'same_units': {
        'wh_dlc07_brt_inf_men_at_arms_su': ('Men-At-Arms', ['wh_dlc07_brt_inf_men_at_arms_1', 'wh_dlc07_brt_inf_men_at_arms_2']),
        'wh_main_brt_inf_spearmen_at_arms_su': ('Spearmen-At-Arms', ['wh_main_brt_inf_spearmen_at_arms', 'wh_dlc07_brt_inf_spearmen_at_arms_1']),
        'wh_dlc07_brt_inf_battle_pilgrims_su': ('Battle Pilgrims', ['wh_dlc07_brt_inf_battle_pilgrims_0', 'wh_pro04_brt_inf_battle_pilgrims_ror_0']),
        'wh_dlc07_brt_inf_foot_squires_su': ('Foot Squires', ['wh_dlc07_brt_inf_foot_squires_0', 'wh_pro04_brt_inf_foot_squires_ror_0']),
        'wh_dlc07_brt_cav_knights_errant_su': ('Knights Errant', ['wh_dlc07_brt_cav_knights_errant_0', 'wh_pro04_brt_cav_knights_errant_ror_0']),
        'wh_main_brt_cav_knights_of_the_realm_su': ('Knights Of The Realm', ['wh_main_brt_cav_knights_of_the_realm', 'wh_pro04_brt_cav_knights_of_the_realm_ror_0']),
        'wh_dlc07_brt_cav_questing_knights_su': ('Questing Knights', ['wh_dlc07_brt_cav_questing_knights_0', 'wh_pro04_brt_cav_questing_knights_ror_0']),
        'wh_main_brt_cav_mounted_yeomen_su': ('Mounted Yeomen Archers', ['wh_main_brt_cav_mounted_yeomen_1', 'wh_pro04_brt_cav_mounted_yeomen_ror_0']),

        'wh_main_brt_mount_royal_pegasus': ('Royal Pegasus Mount',
                                         ['wh_main_brt_cha_lord_3', 'wh_dlc07_brt_cha_alberic_bordeleaux_2',
                                          'wh_main_brt_cha_king_louen_leoncoeur_3', 'wh_main_brt_cha_paladin_3',
                                          'wh_dlc07_brt_cha_prophetess_beasts_3', 'wh_dlc07_brt_cha_prophetess_heavens_3', 'wh_dlc07_brt_cha_prophetess_3']),

        'wh_main_brt_mount_hyppogriph': ('Hyppogryph Mount', ['wh_main_brt_cha_lord_2', 'wh_dlc07_brt_cha_alberic_bordeleaux_3', 'wh_main_brt_cha_king_louen_leoncoeur_1', 'wh_main_brt_cha_king_louen_leoncoeur_4', 'wh2_dlc14_brt_cha_henri_le_massif_3',]),
    },

    'variant_units': {
        'wh_dlc07_brt_inf_men_at_arms_var': ('Men-At-Arms', ['wh_dlc07_brt_inf_men_at_arms_su', 'wh_main_brt_inf_spearmen_at_arms_su']),
        'wh_dlc07_brt_inf_peasant_bowmen_var': ('Peasant Bowmen', ['wh_main_brt_inf_peasant_bowmen', 'wh_dlc07_brt_inf_peasant_bowmen_1', 'wh_dlc07_brt_inf_peasant_bowmen_2']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh_dlc07_brt_peasant_mob_0',
        'wh_dlc07_brt_inf_men_at_arms_su',
        'wh_main_brt_inf_spearmen_at_arms_su',
        'wh_main_brt_inf_men_at_arms', #halberds
        'wh_dlc07_brt_inf_battle_pilgrims_su',
        'wh_dlc07_brt_inf_foot_squires_su',

        'wh_dlc07_brt_inf_grail_reliquae_0', # XSE / SR

        'wh_main_brt_inf_peasant_bowmen',
        'wh_dlc07_brt_inf_peasant_bowmen_1',
        'wh_dlc07_brt_inf_peasant_bowmen_2',
    ],

    'multi_entity_chariots': [
    ],

    'multi_entity_other': [
        # mon

        # cav
        'wh_dlc07_brt_cav_knights_errant_su',
        'wh_main_brt_cav_knights_of_the_realm_su',
        'wh_dlc07_brt_cav_questing_knights_su',
        'wh_main_brt_cav_mounted_yeomen_0',
        'wh_main_brt_cav_mounted_yeomen_su',
        'wh_main_brt_cav_grail_knights',
        'wh_dlc07_brt_cav_grail_guardians_0',

        # fly
        'wh_main_brt_cav_pegasus_knights',
        'wh_dlc07_brt_cav_royal_pegasus_knights_0',
        'wh_dlc07_brt_cav_royal_hippogryph_knights_0',

        # art
        'wh_main_brt_art_field_trebuchet',
        'wh_dlc07_brt_art_blessed_field_trebuchet_0',
        ],

        'exempt_single_entities': [
        ],

    'single_entity_all': [
    ],

    'single_entity_rare': [
        'wh_main_brt_mount_hyppogriph',
    ],

    'superweapon': [
    ],

    #----------------------------------
    # CATEGORIES

    'chariots': [
    ],

    'flying_ranged': [
    ],

    'flying': [
        'wh_main_brt_cav_pegasus_knights',
        'wh_dlc07_brt_cav_royal_pegasus_knights_0',
        'wh_dlc07_brt_cav_royal_hippogryph_knights_0',
        'wh_main_brt_mount_royal_pegasus',
        'wh_main_brt_mount_hyppogriph',
    ],

    'ranged_360': [
        'wh_main_brt_cav_mounted_yeomen_su',
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
        'wh_main_brt_cav_mounted_yeomen_su',
    ],

    # 'campaign_exclusive': [
    # ],


    'ranged_total': [
        #inf
        'wh_main_brt_inf_peasant_bowmen',
        'wh_dlc07_brt_inf_peasant_bowmen_1',
        'wh_dlc07_brt_inf_peasant_bowmen_2',

        #mon

        #cav

        #cha

        #art
        'wh_main_brt_art_field_trebuchet',
        'wh_dlc07_brt_art_blessed_field_trebuchet_0',
    ],


    # ROR
    'ror': [
        'wh_pro04_brt_inf_battle_pilgrims_ror_0',
        'wh_pro04_brt_inf_foot_squires_ror_0',
        'wh_pro04_brt_cav_knights_errant_ror_0',
        'wh_pro04_brt_cav_knights_of_the_realm_ror_0',
        'wh_pro04_brt_cav_questing_knights_ror_0',
        'wh_pro04_brt_cav_mounted_yeomen_ror_0',

    ]

}
