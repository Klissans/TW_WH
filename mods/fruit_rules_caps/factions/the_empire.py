the_empire = {

    'same_units': {
        'wh_main_emp_inf_swordsmen_su': ('Swordsmen', ['wh_main_emp_inf_swordsmen', 'wh_dlc04_emp_inf_sigmars_sons_0']),
        'wh_dlc04_emp_inf_flagellants_su': ('Flagellants', ['wh_dlc04_emp_inf_flagellants_0', 'wh_dlc04_emp_inf_tattersouls_0']),
        'wh2_dlc13_emp_inf_archers_su': ('Archers', ['wh2_dlc13_emp_inf_archers_0', 'wh2_dlc13_emp_inf_archers_ror_0']),
        'wh_dlc04_emp_inf_free_company_militia_su': ('Free Company Militia', ['wh_dlc04_emp_inf_free_company_militia_0', 'wh_dlc04_emp_inf_stirlands_revenge_0']),
        'wh_main_emp_inf_handgunners_su': ('Handgunners', ['wh_main_emp_inf_handgunners', 'wh_dlc04_emp_inf_silver_bullets_0']),
        'wh2_dlc13_emp_inf_huntsmen_su': ('Huntsmen', ['wh2_dlc13_emp_inf_huntsmen_0', 'wh2_dlc13_emp_inf_huntsmen_ror_0']),
        'wh_main_emp_cav_reiksguard_su': ('Reiksguard', ['wh_main_emp_cav_reiksguard', 'wh_dlc04_emp_cav_zintlers_reiksguard_0']),
        'wh_main_emp_cav_demigryph_knights_halberds_su': ('Demigryph Knights (Halberds)', ['wh_main_emp_cav_demigryph_knights_1', 'wh_dlc04_emp_cav_royal_altdorf_gryphites_0']),
        'wh2_dlc13_emp_veh_war_wagon_art_su': ('War Wagon (Artillery)', ['wh2_dlc13_emp_veh_war_wagon_1', 'wh2_dlc13_emp_veh_war_wagon_ror_0']),
        'wh_main_emp_art_great_cannon_su': ('Great Cannons', ['wh_main_emp_art_great_cannon', 'wh_dlc04_emp_art_hammer_of_the_witches_0']),
        'wh_main_emp_art_helstorm_rocket_battery_su': ('Helstorm Rocket Battery', ['wh_main_emp_art_helstorm_rocket_battery', 'wh_dlc04_emp_art_sunmaker_0']),
        'wh_main_emp_veh_luminark_of_hysh_su': ('Luminark of Hysh', ['wh_main_emp_veh_luminark_of_hysh_0', 'wh_dlc04_emp_veh_templehof_luminark_0']),

        'wh_main_emp_inf_spearmen_su': ('Spearmen', ['wh_main_emp_inf_spearmen_0', 'wh_main_emp_inf_spearmen_1']),

        'wh_main_emp_mount_imperial_pegasus_su': (
            'Imperial Pegasus', ['wh_main_emp_cha_general_2', 'wh_dlc03_emp_cha_boris_todbringer_2',
                              'wh_main_emp_cha_balthasar_gelt_1', 'wh_main_emp_cha_karl_franz_2', 'wh_main_emp_cha_captain_3',
                              'wh_main_emp_cha_wizard_fire_2', 'wh_main_emp_cha_wizard_heavens_2', 'wh_main_emp_cha_wizard_light_2', 'wh_dlc05_emp_cha_wizard_shadows_2', 'wh_dlc05_emp_cha_wizard_life_2',
                              'wh_dlc03_emp_cha_wizard_beasts_4', 'wh2_pro07_emp_cha_wizard_death_2']),

        'wh_main_emp_mont_griffon_su': (
            'Griffon Mount', ['wh_main_emp_cha_general_3', 'wh_dlc03_emp_cha_boris_todbringer_3',
                          'wh_main_emp_cha_karl_franz_1', 'wh_dlc03_emp_cha_wizard_beasts_3']),

    },

    'variant_units': {
        'wh3_main_sla_inf_infmen_var': ('Infmen', ['wh_main_emp_inf_spearmen_su', 'wh_main_emp_inf_swordsmen_su']),
        'wh_main_emp_cav_demigryph_knights_var': ('Demigryph Knights', ['wh_main_emp_cav_demigryph_knights_0', 'wh_main_emp_cav_demigryph_knights_halberds_su']),
        'wh_main_emp_cav_outriders_var': ('Outriders', ['wh_main_emp_cav_outriders_0', 'wh_main_emp_cav_outriders_1']),
        'wh2_dlc13_emp_veh_war_wagon_var': ('War Wagons', ['wh2_dlc13_emp_veh_war_wagon_0', 'wh2_dlc13_emp_veh_war_wagon_art_su']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        'wh_main_emp_inf_spearmen_su',
        'wh_main_emp_inf_swordsmen_su',
        'wh_main_emp_inf_halberdiers',
        'wh_dlc04_emp_inf_flagellants_su',
        'wh_main_emp_inf_greatswords',

        'wh2_dlc13_emp_inf_archers_su',
        'wh_dlc04_emp_inf_free_company_militia_su',
        'wh_main_emp_inf_crossbowmen',
        'wh_main_emp_inf_handgunners_su',
        'wh2_dlc13_emp_inf_huntsmen_su',
    ],

    'multi_entity_chariots': [
        'wh2_dlc13_emp_veh_war_wagon_0',
        'wh2_dlc13_emp_veh_war_wagon_art_su',
    ],

    'multi_entity_other': [
        # mon

        # cav
        'wh_main_emp_cav_empire_knights',
        'wh_main_emp_cav_reiksguard_su',
        'wh_dlc04_emp_cav_knights_blazing_sun_0',
        'wh_main_emp_cav_demigryph_knights_0',
        'wh_main_emp_cav_demigryph_knights_halberds_su',

        'wh_main_emp_cav_pistoliers_1',
        'wh_main_emp_cav_outriders_0',
        'wh_main_emp_cav_outriders_1',

        # fly

        # art
        'wh_main_emp_art_mortar',
        'wh_main_emp_art_great_cannon_su',
        'wh_main_emp_art_helblaster_volley_gun',
        'wh_main_emp_art_helstorm_rocket_battery_su',
    ],

    'exempt_single_entities': [
    ],


    'single_entity_all': [
        'wh_main_emp_veh_luminark_of_hysh_su', # TODO XSE or nor?
    ],

    'single_entity_rare': [
        'wh_dlc04_emp_cha_volkmar_the_grim_1',
        'wh_main_emp_mont_griffon_su',
    ],

    'superweapon': [
        # 'wh_main_emp_veh_steam_tank',
    ],

    #----------------------------------
    # CATEGORIES

    'chariots': [
        'wh_main_emp_veh_steam_tank',
        'wh_dlc04_emp_cha_volkmar_the_grim_1',
    ],

    'flying_ranged': [
    ],

    'flying': [
        'wh_main_emp_mount_imperial_pegasus_su',
        'wh_main_emp_mont_griffon_su',
    ],

    'ranged_360': [
        'wh_dlc04_emp_inf_free_company_militia_su',
        'wh2_dlc13_emp_inf_huntsmen_su',
        'wh_main_emp_cav_pistoliers_1',
        'wh2_dlc13_emp_veh_war_wagon_0',
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
        'wh_main_emp_cav_pistoliers_1',
        'wh_main_emp_cav_outriders_0',
        'wh_main_emp_cav_outriders_1',

        'wh2_dlc13_emp_veh_war_wagon_0',
        'wh2_dlc13_emp_veh_war_wagon_art_su',
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        #inf
        'wh2_dlc13_emp_inf_archers_su',
        'wh_main_emp_inf_crossbowmen',
        'wh_main_emp_inf_handgunners_su',

        #mon

        #cav
        'wh_main_emp_cav_outriders_0',
        'wh_main_emp_cav_outriders_1',

        #cha
        'wh_main_emp_veh_steam_tank',

        #art
        'wh_main_emp_art_mortar',
        'wh_main_emp_art_great_cannon_su',
        'wh_main_emp_art_helblaster_volley_gun',
        'wh_main_emp_art_helstorm_rocket_battery_su',
        'wh_main_emp_veh_luminark_of_hysh_su',
    ],


    # ROR
    'ror': [
        'wh_dlc04_emp_inf_sigmars_sons_0',
        'wh_dlc04_emp_inf_tattersouls_0',
        'wh2_dlc13_emp_inf_archers_ror_0',
        'wh_dlc04_emp_inf_stirlands_revenge_0',
        'wh_dlc04_emp_inf_silver_bullets_0',
        'wh2_dlc13_emp_inf_huntsmen_ror_0',
        'wh_dlc04_emp_cav_zintlers_reiksguard_0',
        'wh_dlc04_emp_cav_royal_altdorf_gryphites_0',
        'wh2_dlc13_emp_veh_war_wagon_ror_0',
        'wh_dlc04_emp_art_hammer_of_the_witches_0',
        'wh_dlc04_emp_art_sunmaker_0',
        'wh_dlc04_emp_veh_templehof_luminark_0',
    ]

}
