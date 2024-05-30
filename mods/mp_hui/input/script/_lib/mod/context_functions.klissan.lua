local format_range_damage_string = [=[
            (
                ap_ratio = %f,
                bonus_vs_type = '%s',
                bonus_vs = %d,
                has_bonus = bonus_vs > 0,
                f_mdb = %d,
                f_mdap = %d,
                f_medb = %d,
                f_medap = %d,
                total_dmg = %d,

                f_bonus_mbwd = f_mdb + RoundFloat(bonus_vs * (1.0 - ap_ratio)),
                f_bonus_mapwd = f_mdap + RoundFloat(bonus_vs * ap_ratio),

                str_prefix = 'random_localisation_strings_string_',

                fmt_exp = GetIfElse(
                    f_medb + f_medap > 0,
                    Format(StringGet(str_prefix + 'tooltip_unit_stat_range_dmg_exp'), f_medb, f_medap),
                    ''
                ),
                fmt_dmg = Format(StringGet(str_prefix + 'tooltip_unit_stat_range_dmg'), f_bonus_mbwd, f_bonus_mapwd),
                fmt_bonus = GetIfElse(
                    has_bonus,
                    Format(StringGet(str_prefix + 'tooltip_unit_stat_range_dmg_bonus'), bonus_vs_type),
                    ''
                )
            ) =>
            {
                Loc('LF') + Format('%S%S%S ([[col:yellow]]%d[[/col]])', fmt_bonus, fmt_dmg, fmt_exp, total_dmg)
            }
]=]

local get_localization = [=[
    (
        loc_key = '%s',
        local = LocLanguage(),
        loc = StringGet('random_localisation_strings_string_' + loc_key + '_' + local),
        fallback_loc = StringGet('random_localisation_strings_string_' + loc_key + '_EN')
    ) =>
    {
        GetIfElse(loc.Length > 0, loc, fallback_loc)
    }
]=]


local context_functions_table = {
    ["format_range_damage_string"] = format_range_damage_string,
    ["get_localization"] = get_localization
}

--common:set_context_value('hui_context_functions', context_functions_table)

Klissan_H:register_function_everywhere(function()
    common:set_context_value('hui_context_functions', context_functions_table)
end)

--(f= ScriptObjectContext('hui_context_functions').TableValue.ValueForKey('format_range_damage_string').Value) => EvaluateExpression(Format(f, 0.5, '', 0, 1, 2, 3, 4, 5))
