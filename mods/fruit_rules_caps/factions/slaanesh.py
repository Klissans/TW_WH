slaanesh = {

    'special_rules': {
        'mortis_sr': (
            'Units With Passive Health Draining Ability',
            ['wh3_main_sla_cha_exalted_keeper_of_secrets_shadow_0',
             'wh3_main_sla_cha_exalted_keeper_of_secrets_slaanesh_0',
             'wh3_main_sla_cha_nkari_0'],
            1
        ),
    },

    'same_units': {
        'wh3_main_sla_inf_daemonette_exalted_su': ('Exalted Daemonettes', ['wh3_main_sla_inf_daemonette_1', 'wh3_twa06_sla_inf_daemonette_ror_0']),
        'wh3_main_sla_cav_heartseekers_of_slaanesh_su': ('Heartseekers', ['wh3_main_sla_cav_heartseekers_of_slaanesh_0',
                                                                          'wh3_twa07_sla_cav_heartseekers_of_slaanesh_ror_0']),

        'wh3_main_sla_veh_exalted_seeker_chariot_su': ('Exalted Seekers Chariot',
                                                       ['wh3_main_sla_veh_exalted_seeker_chariot_0',
                                                        'wh3_main_sla_cha_alluress_shadow_3',
                                                        'wh3_main_sla_cha_alluress_slaanesh_3',
                                                        'wh3_main_sla_cha_herald_of_slaanesh_shadow_3',
                                                        'wh3_main_sla_cha_herald_of_slaanesh_slaanesh_3']),

        'wh3_main_sla_mon_keeper_of_secrets_su': ('Keeper of Secrets', ['wh3_main_sla_mon_keeper_of_secrets_0',
                                                                        'wh3_main_sla_cha_exalted_keeper_of_secrets_shadow_0',
                                                                        'wh3_main_sla_cha_exalted_keeper_of_secrets_slaanesh_0',
                                                                        'wh3_main_sla_cha_nkari_0']),
    },

    'variant_units': {
        'wh3_main_sla_inf_marauders_var': (
        'Marauders', ['wh3_main_sla_inf_marauders_0', 'wh3_main_sla_inf_marauders_1', 'wh3_main_sla_inf_marauders_2']),
        'wh3_main_sla_cav_hellstriders_var': (
        'Hellstriders', ['wh3_main_sla_cav_hellstriders_0', 'wh3_main_sla_cav_hellstriders_1']),
    },

    # ARMY LIMITS
    'multi_entity_infantry': [
        # 'wh3_main_sla_inf_marauders_0',
        # 'wh3_main_sla_inf_marauders_1',
        # 'wh3_main_sla_inf_marauders_2',
        'wh3_main_sla_inf_daemonette_0',
        'wh3_main_sla_inf_daemonette_exalted_su',
    ],

    'multi_entity_chariots': [
        'wh3_main_sla_veh_hellflayer_0',
        'wh3_main_sla_veh_seeker_chariot_0',
    ],

    'multi_entity_other': [
        # mon
        # 'wh3_main_sla_mon_spawn_of_slaanesh_0',
        'wh3_main_sla_mon_fiends_of_slaanesh_0',

        # cav
        'wh3_main_sla_cav_seekers_of_slaanesh_0',
        'wh3_main_sla_cav_heartseekers_of_slaanesh_su',
        'wh3_main_sla_cav_hellstriders_0',
        'wh3_main_sla_cav_hellstriders_1',

        # fly
        'wh3_main_sla_inf_chaos_furies_0',

        # art

    ],

    'exempt_single_entities': [
    ],

    'single_entity_all': [
        'wh3_main_sla_veh_exalted_seeker_chariot_su',
    ],

    'single_entity_rare': [
        'wh3_main_sla_mon_keeper_of_secrets_su',
        'wh3_dlc20_sla_cha_azazel',
        # 'wh3_main_sla_mon_soul_grinder_0',
    ],

    'superweapon': [
    ],

    # ----------------------------------
    # CATEGORIES

    'chariots': [
        'wh3_main_sla_veh_exalted_seeker_chariot_su',
    ],

    'flying_ranged': [
    ],

    'flying': [
        'wh3_main_sla_inf_chaos_furies_0',
        'wh3_dlc20_sla_cha_azazel',
    ],

    'ranged_360': [
    ],

    'multi_entity_ranged_cavalry_and_chariots': [
    ],

    # 'campaign_exclusive': [
    # ],

    'ranged_total': [
        # inf

        # mon

        # cav

        # cha

        # fly

        # art
    ],

    # ROR
    'ror': [
        'wh3_twa06_sla_inf_daemonette_ror_0',
        'wh3_twa07_sla_cav_heartseekers_of_slaanesh_ror_0',
    ]

}
