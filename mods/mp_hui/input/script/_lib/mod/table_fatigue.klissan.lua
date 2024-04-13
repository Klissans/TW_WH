local fatigue_effects_table = {
    ["stat_armour"] = {1.00, 1.00, 1.00, 1.00, 0.90, 0.75},
    ["scalar_speed"] = {1.00, 1.00, 0.95, 0.90, 0.85, 0.85},
    ["stat_melee_attack"] = {1.00, 0.95, 0.95, 0.85, 0.75, 0.70},
    ["stat_melee_defence"] = {1.00, 1.00, 1.00, 1.00, 1.00, 0.90},
    ["stat_melee_damage_base"] = {1.00, 1.00, 1.00, 1.00, 1.00, 1.00},
    ["stat_melee_damage_ap"] = {1.00, 1.00, 0.90, 0.90, 0.90, 0.90},
    ["stat_charge_bonus"] = {1.00, 1.00, 1.00, 0.90, 0.75, 0.70},
    ["stat_reload_time"] = {1.00, 1.00, 1.00, 1.00, 1.00, 0.90}, --TODO stat reload in cco script
    ["scalar_missile_damage_base"] = {1.00, 1.00, 1.00, 1.00, 1.00, 1.00},
    ["scalar_missile_damage_ap"] = {1.00, 1.00, 1.00, 1.00, 1.00, 1.00},
    ["scalar_missile_explosion_damage_base"] = {1.00, 1.00, 1.00, 1.00, 1.00, 1.00},
    ["scalar_missile_explosion_damage_ap"] = {1.00, 1.00, 1.00, 1.00, 1.00, 1.00},
}

local fatigue_effects_leadership = {0, 0, 0, 0, -2, -6}

local fatigue_states_table = {
    "fresh",
    "active",
    "winded",
    "tired",
    "very_tired",
    "exhausted",
}

register_function{function()
    common:set_context_value('fatigue_effects', fatigue_effects_table)
end, is_battle=true}

register_function{function()
    common:set_context_value('fatigue_effects_leadership', fatigue_effects_leadership)
end, is_battle=true}

register_function{function()
    common:set_context_value('fatigue_states', fatigue_states_table)
end, is_battle=true}