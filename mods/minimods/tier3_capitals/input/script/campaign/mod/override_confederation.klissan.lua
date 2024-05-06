-- cache the current global version
local vanilla_force_confederation = cm.force_confederation

-- overwrite the global version with my own
function cm:force_confederation(proposing_faction_key, target_faction_key)
    cm:force_make_vassal(proposing_faction_key, target_faction_key)
end


---------
local NORSCA_CONFEDERATE_DILEMMA_CONFEDERATE_OPTION = 0


local function Override_Norsca_Confed_DilemmaChoiceMadeEvent(target_faction_key)
	-- Confederation via Defeat Leader
	core:add_listener(
		"Confed_Norsca_Confed_DilemmaChoiceMadeEvent",
		"DilemmaChoiceMadeEvent",
		function(context)
            return context:dilemma() == NORSCA_CONFEDERATE_DILEMMA or context:dilemma() == NORSCA_CONFEDERATE_FOR_LLS_DILEMMA
        end,
		function(context)
			if context:choice() == NORSCA_CONFEDERATE_DILEMMA_CONFEDERATE_OPTION then
                cm:force_make_vassal(context:faction():name(), target_faction_key)
			end
		end,
		false
	)
end

-- cache the current global version
local vanilla_trigger_dilemma_with_targets = cm.trigger_dilemma_with_targets

-- overwrite the global version with my own
function cm:trigger_dilemma_with_targets(
        faction_cqi,
        dilemma_key,
        target_faction_cqi,
        secondary_faction_cqi,
        character_cqi,
        military_force_cqi,
        region_cqi,
        settlement_cqi,
        lambda
)
    local function_override = lambda

    --console_print(''..','..faction_cqi..','..dilemma_key..','..target_faction_cqi..','..secondary_faction_cqi..','..character_cqi..','..military_force_cqi..','..region_cqi..','..settlement_cqi)
    if dilemma_key == NORSCA_CONFEDERATE_DILEMMA or dilemma_key == NORSCA_CONFEDERATE_FOR_LLS_DILEMMA then
        function_override = function()
            Override_Norsca_Confed_DilemmaChoiceMadeEvent(cm:model():faction_for_command_queue_index(target_faction_cqi):name())
            lambda()
        end
    end

    vanilla_trigger_dilemma_with_targets(cm, faction_cqi, dilemma_key, target_faction_cqi, secondary_faction_cqi, character_cqi, military_force_cqi, region_cqi, settlement_cqi, function_override)
end
