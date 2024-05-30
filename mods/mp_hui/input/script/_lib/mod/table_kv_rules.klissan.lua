local _kv_rules_table = {
    ["melee_defence_direction_penalty_coefficient_flank"] = 0.6,
    ["melee_defence_direction_penalty_coefficient_rear"] = 0.3,
    ['armour_roll_lower_cap'] = 0.5,
}

Klissan_H:register_function_everywhere(function()
    common:set_context_value('_kv_rules', _kv_rules_table)
end)