--local out = function(t)
--    ModLog("DRUNKFLAMINGO: "..tostring(t).." (T4 Start)")
--end

local function upgrade_home_region(faction)
    if faction:has_home_region() then
        cm:instantly_set_settlement_primary_slot_level(faction:home_region():settlement(), 3)
    end
    if faction:is_allowed_to_capture_territory() == false then -- is horde
    end
end

cm:add_first_tick_callback(function ()
    if cm:model():turn_number() < 2 then
        core:add_listener(
            "CharacterPerformsSettlementOccupationDecisionT4Start",
            "CharacterPerformsSettlementOccupationDecision",
            function(context)
                return true
            end,
            function(context)
                local faction = context:garrison_residence():faction() -- need to define local var before passing it to callback
                cm:callback(function() upgrade_home_region(faction) end, 0.1)
            end,
            true)
    end
end)

cm:add_first_tick_callback_new(function ()
    local faction_list = cm:model():world():faction_list()
    for i = 0, faction_list:num_items() - 1 do
        local faction = faction_list:item_at(i)
        upgrade_home_region(faction)
    end
end)
