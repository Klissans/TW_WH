--require('_helpers_klissan')
--KlissanLoadModule('_helpers_klissan', 'script/_lib/mod')

local _kv_rules_table = {
    ["melee_defence_direction_penalty_coefficient_flank"] = { ["key"] = "melee_defence_direction_penalty_coefficient_flank", ["value"] = 0.6 },
    ["melee_defence_direction_penalty_coefficient_rear"] = { ["key"] = "melee_defence_direction_penalty_coefficient_rear", ["value"] = 0.3 }
}

function init_kv_rules_cco_script_values()
    for _, k in pairs(get_key_sorted(_kv_rules_table)) do
        local entry = _kv_rules_table[k]
        local key = '_kv_rules_table.' .. entry['key']
        common:set_context_value(key, entry['value'])
    end
end

register_function_everywhere(init_kv_rules_cco_script_values)



function add_fatigue_effects_component()
    core:get_ui_root():CreateComponent("db_lookup", "ui/mod/db_lookup.twui.xml")
end


register_function_everywhere(add_fatigue_effects_component)

--language=javascript