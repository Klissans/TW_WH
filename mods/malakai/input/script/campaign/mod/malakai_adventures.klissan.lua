


core:add_listener(
	Klissan_CH:get_listener_name('malakai_adventure_activated_grant_units'),
	"RitualCompletedEvent",
	function (context)
        return context:ritual():ritual_category() == 'MALAKAI_ADVENTURE_ACTIVATE'
    end,
	function(context)
		local general_support_army_lookup_str = cm:char_lookup_str(cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi):general_character())
		local ritual_key = context:ritual():ritual_key()
		local result_str = MGSWT.croot:Call(string.format([=[
			(
				key = '%s',
				payload = DatabaseRecordContext('CcoRitualRecord', key).CompletionPayloadContext.CampaignPayloadContext,
				res = payload.UnitComponents.JoinString(UnitContext.Key + ',' + Amount, ';')
			) => res
		]=], ritual_key))
    	local unit_components = string.split(result_str, ';')
		for i=1, #unit_components do
			local unit = string.split(unit_components[i], ',')
			local unit_key, unit_amount = unit[1], tonumber(unit[2])
			for _=1,unit_amount do
				cm:grant_unit_to_character(general_support_army_lookup_str, unit_key)
			end
		end
	end,
	true
)

