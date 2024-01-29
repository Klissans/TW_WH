ogre_kingdoms = {

    'same_units': {
        'wh3_main_ogr_inf_maneaters_pistol_su': ('Maneaters (Ogre Pistol)', ['wh3_main_ogr_inf_maneaters_3', 'wh3_twa06_ogr_inf_maneaters_ror_0']),
        'wh3_main_ogr_cav_crushers_gw_su': ('Crushers (Great Weapons)', ['wh3_main_ogr_cav_crushers_1', 'wh3_twa07_ogr_cav_crushers_ror_0']),

        #Exception from rules
        'wh3_main_ogr_mon_stonehorn_su': ('Stonehorn', ['wh3_main_ogr_mon_stonehorn_0', 'wh3_main_ogr_mon_stonehorn_1', 'wh3_main_ogr_cha_hunter_1']),
    },

    'variant_units': {
        'wh3_main_ogr_inf_gnoblars_var': ('Gnoblars', ['wh3_main_ogr_inf_gnoblars_0', 'wh3_main_ogr_inf_gnoblars_1']),
        'wh3_main_ogr_inf_ogres_var': ('Ogre Bulls', ['wh3_main_ogr_inf_ogres_0', 'wh3_main_ogr_inf_ogres_1', 'wh3_main_ogr_inf_ogres_2']),
        'wh3_main_ogr_inf_maneaters_var': ('Maneaters', ['wh3_main_ogr_inf_maneaters_0', 'wh3_main_ogr_inf_maneaters_1', 'wh3_main_ogr_inf_maneaters_2', 'wh3_main_ogr_inf_maneaters_pistol_su']),
        'wh3_main_ogr_cav_mournfang_cavalry_var': ('Mournfang Cavalry', ['wh3_main_ogr_cav_mournfang_cavalry_0', 'wh3_main_ogr_cav_mournfang_cavalry_1', 'wh3_main_ogr_cav_mournfang_cavalry_2']),
        'wh3_main_ogr_cav_crushers_var': ('Crushers', ['wh3_main_ogr_cav_crushers_0', 'wh3_main_ogr_cav_crushers_gw_su']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh3_main_ogr_inf_gnoblars_0',
        'wh3_main_ogr_inf_gnoblars_1',
    ],

    'multi_entity_chariots': [
    ],

    'multi_entity_other': [
        # mon
        'wh3_main_ogr_inf_ogres_0',
        'wh3_main_ogr_inf_ogres_1',
        'wh3_main_ogr_inf_ogres_2',
        'wh3_main_ogr_inf_maneaters_0',
        'wh3_main_ogr_inf_maneaters_1',
        'wh3_main_ogr_inf_maneaters_2',
        'wh3_main_ogr_inf_maneaters_pistol_su',
        'wh3_main_ogr_inf_ironguts_0',
        'wh3_main_ogr_mon_gorgers_0',
        'wh3_main_ogr_inf_leadbelchers_0',

        # cav
        'wh3_main_ogr_mon_sabretusk_pack_0',
        'wh3_main_ogr_cav_mournfang_cavalry_0',
        'wh3_main_ogr_cav_mournfang_cavalry_1',
        'wh3_main_ogr_cav_mournfang_cavalry_2',
        'wh3_main_ogr_cav_crushers_0',
        'wh3_main_ogr_cav_crushers_gw_su',

        # fly

        # art

    ],

    'exempt_single_entities': [
    ],

    'single_entity_all': [
        'wh3_main_ogr_veh_gnoblar_scraplauncher_0',
    ],

    'single_entity_rare': [
        'wh3_main_ogr_mon_giant_0',
        'wh3_main_ogr_veh_ironblaster_0',
        'wh3_main_ogr_mon_stonehorn_su',
    ],

    'superweapon': [
    ],

    #----------------------------------
    # CATEGORIES

    'chariots': [
        'wh3_main_ogr_veh_gnoblar_scraplauncher_0',
        'wh3_main_ogr_veh_ironblaster_0',
    ],

    'flying_ranged': [
    ],

    'flying': [
    ],

    'ranged_360': [
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        #inf
        'wh3_main_ogr_inf_gnoblars_1',

        #mon
        'wh3_main_ogr_inf_maneaters_pistol_su',
        'wh3_main_ogr_inf_leadbelchers_0',
        'wh3_main_ogr_mon_stonehorn_1',
        'wh3_main_ogr_cha_hunter_1',

        #cav

        #cha
        'wh3_main_ogr_veh_gnoblar_scraplauncher_0',
        'wh3_main_ogr_veh_ironblaster_0',

        #fly

        #art
    ],


    # ROR
    'ror': [
        'wh3_twa06_ogr_inf_maneaters_ror_0',
        'wh3_twa07_ogr_cav_crushers_ror_0',
    ]

}
