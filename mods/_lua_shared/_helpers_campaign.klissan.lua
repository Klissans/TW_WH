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
