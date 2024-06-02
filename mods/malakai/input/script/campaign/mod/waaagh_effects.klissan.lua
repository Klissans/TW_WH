K_WAAAGH_EFFECTS = {
}

Klissan_H:setup_logging(K_WAAAGH_EFFECTS, 'K_WAAAGH_EFFECTS')

function K_WAAAGH_EFFECTS:init()
end


function K_WAAAGH_EFFECTS:extract_effects_from_bundles(source_army_cqi)
    local skills_str = Klissan_CH:croot():Call(string.format([=[
        (
            army = CampaignRoot.MilitaryForceList.FirstContext(CQI == %d),
            effects = army.EffectBundleUnfilteredList.Transform(EffectsIncludingHiddenList)
                .Filter(EffectScopeContext.Key == 'general_to_force_own' || EffectScopeContext.Key == 'agent_to_parent_army_own'),
            effects_str = effects.JoinString(Format('%%s,%%d', EffectKey, Value), ';')
        ) => effects_str
    ]=], source_army_cqi))
    return skills_str
end


function K_WAAAGH_EFFECTS:extract_characters_skill_effects(source_army_cqi)
    local skills_str = Klissan_CH:croot():Call(string.format([=[
        (
            army = CampaignRoot.MilitaryForceList.FirstContext(CQI == %d),
            chars_skill_effects = army.CharacterList.Transform(SkillList).Transform(EffectUnfilteredList)
                .Filter(EffectScopeContext.Key == 'general_to_force_own' || EffectScopeContext.Key == 'agent_to_parent_army_own' || EffectKey == 'wh_main_effect_agent_movement_range_mod'),
            skill_effects_str = chars_skill_effects.JoinString(Format('%%s,%%d', EffectKey, Value), ';')
        ) => skill_effects_str
    ]=], source_army_cqi))
    return skills_str
end


function K_WAAAGH_EFFECTS:extract_character_trait_effects(source_army_cqi)
    local skills_str = Klissan_CH:croot():Call(string.format([=[
        (
            army = CampaignRoot.MilitaryForceList.FirstContext(CQI == %d),
            chars_skill_effects = army.CharacterList.Transform(TraitsList).Transform(EffectUnfilteredList)
                .Filter(EffectScopeContext.Key == 'general_to_force_own' || EffectScopeContext.Key == 'agent_to_parent_army_own'),
            skill_effects_str = chars_skill_effects.JoinString(Format('%%s,%%d', EffectKey, Value), ';')
        ) => skill_effects_str
    ]=], source_army_cqi))
    return skills_str
end


function K_WAAAGH_EFFECTS:extract_character_background_effects(source_army_cqi)
    local skills_str = Klissan_CH:croot():Call(string.format([=[
        (
            army = CampaignRoot.MilitaryForceList.FirstContext(CQI == %d),
            chars_skill_effects = army.CharacterList.Transform(BackgroundSkillContext.EffectUnfilteredList)
                .Filter(EffectScopeContext.Key == 'general_to_force_own' || EffectScopeContext.Key == 'agent_to_parent_army_own'),
            skill_effects_str = chars_skill_effects.JoinString(Format('%%s,%%d', EffectKey, Value), ';')
        ) => skill_effects_str
    ]=], source_army_cqi))
    return skills_str
end

function K_WAAAGH_EFFECTS:extract_character_ancillary_effects(source_army_cqi)
    local skills_str = Klissan_CH:croot():Call(string.format([=[
        (
            army = CampaignRoot.MilitaryForceList.FirstContext(CQI == %d),
            chars_skill_effects = army.CharacterList.Transform(AncillaryList).Transform(EffectUnfilteredList)
                .Filter(EffectScopeContext.Key == 'general_to_force_own' || EffectScopeContext.Key == 'agent_to_parent_army_own'),
            skill_effects_str = chars_skill_effects.JoinString(Format('%%s,%%d', EffectKey, Value), ';')
        ) => skill_effects_str
    ]=], source_army_cqi))
    return skills_str
end

function K_WAAAGH_EFFECTS:add_effects_to_table(bundle_table, effects_str)
    local effect_value_pairs = string.split(effects_str, ';')
    for i=1, #effect_value_pairs do
        local effect_value = string.split(effect_value_pairs[i], ',')
        local effect_key, value = effect_value[1], math.floor(tonumber(effect_value[2]))
        if bundle_table[effect_key] ~= nil then
            bundle_table[effect_key] = bundle_table[effect_key] + value
        else
            bundle_table[effect_key]= value
        end
    end
    return bundle_table
end

function K_WAAAGH_EFFECTS:create_effects_table_for_army(source_army_cqi)
    local effects = {}
    self:add_effects_to_table(effects, self:extract_effects_from_bundles(source_army_cqi))
    self:add_effects_to_table(effects, self:extract_characters_skill_effects(source_army_cqi))
    self:add_effects_to_table(effects, self:extract_character_trait_effects(source_army_cqi))
    self:add_effects_to_table(effects, self:extract_character_background_effects(source_army_cqi))
    self:add_effects_to_table(effects, self:extract_character_ancillary_effects(source_army_cqi))
    return effects
end

function K_WAAAGH_EFFECTS:apply_effect_bundle_to_support_army(source_army_cqi, target_army_cqi)
    self:debug('Copying effects from army %d (cqi) to waaagh_army %d (cqi)', source_army_cqi, target_army_cqi)
    local bundle_key = 'klissan_waaagh_effects'
    local custom_bundle = cm:create_new_custom_effect_bundle(bundle_key)
    --custom_bundle:set_duration(2)
    local effects = self:create_effects_table_for_army(source_army_cqi)
    for key, value in pairs(effects) do
        self:debug(' - adding effect to waaagh army: %s %d', key, value)
        custom_bundle:add_effect(key, 'force_to_force_own', value)
    end
    cm:remove_effect_bundle_from_force(custom_bundle:key(), target_army_cqi)
    cm:apply_custom_effect_bundle_to_force(custom_bundle, cm:get_military_force_by_cqi(target_army_cqi))
    self:debug('[DONE] Copying effects from army %d (cqi) to waaagh_army %d (cqi)', source_army_cqi, target_army_cqi)
end


function K_WAAAGH_EFFECTS:find_match_for_waaagh_army(faction, waaagh_mf)
    local mfs = faction:military_force_list()
    local x, y = Klissan_CH:get_logical_position(waaagh_mf:general_character())
    for i=0, mfs:num_items()-1 do
        local mf = mfs:item_at(i)
        local char = mf:general_character()
        local xx, yy = Klissan_CH:get_logical_position(char)
        if mf:force_type():key() ~= 'SUPPORT_ARMY' and x == xx and y == yy then
            return mf:command_queue_index()
        end
    end
end

function K_WAAAGH_EFFECTS:update_waaagh_armies_effects(faction)
    -- there should be only one army left which is bound to malaki
    local mfl = faction:military_force_list()
    for i = 0, mfl:num_items() - 1 do
        local mf = mfl:item_at(i)
        if mf:force_type():key() == 'SUPPORT_ARMY' then
            local target_army_cqi = mf:command_queue_index()
            local source_army_cqi = self:find_match_for_waaagh_army(faction, mf)
            K_WAAAGH_EFFECTS:apply_effect_bundle_to_support_army(source_army_cqi, target_army_cqi)
        end
    end
end

function K_WAAAGH_EFFECTS:init_update_waaagh_army_effects_listeners()
    local events = {
        'FactionTurnStart',
        'FactionTurnEnd',
    }

    for i=1,#events do
        local event_name = events[i]

        core:add_listener(
            Klissan_CH:get_listener_name('update_waaagh_army_effects_'..event_name),
            event_name,
            function(context)
                return context:faction():culture() == 'wh_main_grn_greenskins'
            end,
            function(context)
                K_WAAAGH_EFFECTS:debug('Updating waaaghs for %s if any on %s', context:faction():name(), event_name)
                K_WAAAGH_EFFECTS:update_waaagh_armies_effects(context:faction())
                K_WAAAGH_EFFECTS:debug('[DONE] Updating waaaghs for %s if any on %s', context:faction():name(), event_name)
            end,
            true
        )

    end
end

cm:add_post_first_tick_callback(function()
    K_WAAAGH_EFFECTS:init()
    K_WAAAGH_EFFECTS:init_update_waaagh_army_effects_listeners()
end)


--todo refactor logging, croot
--todo campaign movement bug?
