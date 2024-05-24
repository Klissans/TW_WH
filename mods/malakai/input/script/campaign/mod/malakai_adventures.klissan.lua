
MGSWT.is_creating_support_army = false


function MGSWT:init_adventure_listeners()
	--core:remove_listener(Klissan_CH:get_listener_name('malakai_adventure_activated_grant_units'))
	core:add_listener(
			Klissan_CH:get_listener_name('malakai_adventure_activated_grant_units'),
			"RitualCompletedEvent",
			function (context)
				return context:ritual():ritual_category() == 'MALAKAI_ADVENTURE_ACTIVATE'
			end,
			function(context)
				if MGSWT.is_creating_support_army then
					return -- will trigger event over and over again while we are creating support armies
				end
				MGSWT:debug('111')
				if MGSWT.malakai_support_army_cqi == nil
						or not cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi) then
					MGSWT.is_creating_support_army = true
					MGSWT:debug('creating')
					MGSWT:add_support_army_to_malakai()
					MGSWT.is_creating_support_army = false
					MGSWT:debug('done')
				end
				MGSWT:debug('%d', MGSWT.malakai_support_army_cqi)
				local support_mf = cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi)

				local general_support_army_lookup_str = cm:char_lookup_str(support_mf:general_character())
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
end

cm:add_post_first_tick_callback(function()
    MGSWT:init_adventure_listeners()
end)