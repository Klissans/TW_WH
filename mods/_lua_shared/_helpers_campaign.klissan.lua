Klissan_CH = { -- KLISSAN_CAMPAIGN_HELPERS
    croot_cco = nil
}


function Klissan_CH:get_listener_name(str)
    return 'klissan_listener_'..str
end


function Klissan_CH:get_callback_name(str)
    return 'klissan_callback_'..str
end


function Klissan_CH:get_logical_position(character)
    return character:logical_position_x(), character:logical_position_y()
end


function Klissan_CH:faction_resource_mod(faction_name, currency_type, value)
    if currency_type == 'gold' then
        cm:treasury_mod(faction_name, value)
    end
end

function Klissan_CH:croot()
    if self.croot_cco == nil then
        self.croot_cco = cco('CcoCampaignRoot', 'CampaignRoot')
    end
    return self.croot_cco
end


function Klissan_CH:parse_effects_string(effects_str)
    local effects_table = {}
    local effect_value_pairs = string.split(effects_str, ';')
    for i=1, #effect_value_pairs do
        if effect_value_pairs[i]:len() ~= 0 then
            local effect_value = string.split(effect_value_pairs[i], ',')
            local effect_key, value = effect_value[1], math.floor(tonumber(effect_value[2]))
            if effects_table[effect_key] ~= nil then
                effects_table[effect_key] = effects_table[effect_key] + value
            else
                effects_table[effect_key] = value
            end
        end
    end
    local force_movement_key = 'wh_main_effect_force_all_campaign_movement_range'
    local agent_movement_key = 'wh_main_effect_agent_movement_range_mod'
    if effects_table[agent_movement_key] ~= nil then
        if effects_table[force_movement_key] == nil then
            effects_table[force_movement_key] = 0
        end
        effects_table[force_movement_key] = effects_table[force_movement_key] + effects_table[agent_movement_key]
        effects_table[agent_movement_key] = nil
    end
    return effects_table
end


function Klissan_CH:get_army_effects(source_army_cqi)
    local skills_str = Klissan_CH:croot():Call(string.format([=[
        (
            army = CampaignRoot.MilitaryForceList.FirstContext(CQI == %d)
        ) => army.GetAllEffectsAsString()
    ]=], source_army_cqi))
    return Klissan_CH:parse_effects_string(skills_str)
end
