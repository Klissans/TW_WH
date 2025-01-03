MGSWT = { -- MALAKAI_GRUDGE_SETTLING_WORLD_TOUR
    faction_name = 'wh3_dlc25_dwf_malakai',

    malakai_support_army_cqi = nil,

    -- The Spirit of Grungni's circle of influence base radius measured in logical coordinates --27,
    tsog_base_radius = 27, -- spirit_of_grungni.radius_size,
}

Klissan_H:setup_logging(MGSWT, 'MGSWT')

function MGSWT:init()
    self.faction = cm:get_faction(self.faction_name)
    --cm:set_character_excluded_from_trespassing(self.faction:faction_leader(), true)
end


function MGSWT:resurrect_kraka_drak(force_coord_x, force_coord_y, malakai_old_enemy)
    local kraka_drak_faction = cm:get_faction('wh_main_dwf_kraka_drak')
    local kraka_drak_region = nil
    if cm:model():campaign_name_key() == 'wh3_main_chaos' then
        kraka_drak_region = cm:get_region('wh3_main_chaos_region_kraka_drak')
        cm:set_region_abandoned(cm:get_region('wh3_main_chaos_region_kraka_dorden'):name())
    else
        kraka_drak_region = cm:get_region('wh3_main_combi_region_kraka_drak')
    end

    if kraka_drak_region:owning_faction():name() == kraka_drak_faction:name() then
        return
    end

    cm:set_region_abandoned(kraka_drak_region:name())
    cm:transfer_region_to_faction(kraka_drak_region:name(), kraka_drak_faction:name())
    cm:instantly_set_settlement_primary_slot_level(kraka_drak_region:settlement(), 2)
    cm:instantly_set_settlement_primary_slot_level(kraka_drak_region:settlement(), 2)
    cm:add_building_to_settlement(kraka_drak_region:name(), 'wh_main_dwf_resource_gems_2')
    cm:heal_garrison(kraka_drak_region:cqi())

    local kraka_drak_starting_units = {
        'wh2_dlc10_dwf_inf_giant_slayers',
        'wh_main_dwf_inf_slayers',
        'wh_main_dwf_inf_hammerers',
        'wh_main_dwf_inf_miners_1',
        'wh_main_dwf_inf_miners_1',
        'wh_main_dwf_inf_miners_1',
        'wh_main_dwf_inf_irondrakes_0',
        'wh_main_dwf_inf_irondrakes_0',
        'wh_main_dwf_art_flame_cannon',
    }
    cm:create_force_with_existing_general(
        cm:char_lookup_str(kraka_drak_faction:faction_leader()),
        kraka_drak_faction:name(),
        table.concat(kraka_drak_starting_units,','),
        kraka_drak_region:name(),
        force_coord_x,
        force_coord_y,
        function(cqi) end
    )
    cm:force_declare_war(kraka_drak_faction:name(), malakai_old_enemy:name(), false, false)
end

function MGSWT:ie_campaign_setup()
    local old_enemy_faction = cm:get_faction('wh3_main_nur_maggoth_kin')
    local new_ogre_enemy_factions = cm:get_faction('wh3_main_ogr_fulg')
    local malakai_faction = self.faction

    cm:teleport_military_force_to(malakai_faction:faction_leader():military_force(), 1011, 647)

    --remove thunderes as we give him slayer-pirates via support army
    cm:remove_unit_from_character(cm:char_lookup_str(malakai_faction:faction_leader()), 'wh_main_dwf_inf_thunderers_0')

    cm:force_declare_war(malakai_faction:name(), new_ogre_enemy_factions:name(), false, false)
    cm:force_make_peace(malakai_faction:name(), old_enemy_faction:name())

    local karak_vrag = cm:get_region('wh3_main_combi_region_karak_vrag')
    local karak_vrag_level = nil
    if not malakai_faction:is_human() then
        cm:transfer_region_to_faction(karak_vrag:name(), malakai_faction:name())
        cm:heal_garrison(karak_vrag:cqi())
        karak_vrag_level = 2
    else
        -- TODO Zoom camera to new position
        karak_vrag_level = 3 -- after capturing it'll became 2
    end
    cm:instantly_set_settlement_primary_slot_level(karak_vrag:settlement(), karak_vrag_level)
    return old_enemy_faction
end


function MGSWT:roc_campaign_setup()
    local old_enemy_faction = cm:get_faction('wh_main_nor_baersonling')
    local new_ogre_enemy_factions = cm:get_faction('wh3_main_ogr_blood_guzzlers')
    local malakai_faction = self.faction

    local target_region = cm:get_region('wh3_main_chaos_region_bloodpeak')

    local target_x, target_y = cm:find_valid_spawn_location_for_character_from_settlement(
        malakai_faction:name(),
        target_region:name(),
        false,
        true,
        7
    )

    cm:teleport_military_force_to(malakai_faction:faction_leader():military_force(), target_x, target_y)

    --remove thunderes as we give him slayer-pirates via support army
    cm:remove_unit_from_character(cm:char_lookup_str(malakai_faction:faction_leader()), 'wh_main_dwf_inf_thunderers_0')

    cm:force_declare_war(malakai_faction:name(), new_ogre_enemy_factions:name(), false, false)
    cm:force_make_peace(malakai_faction:name(), old_enemy_faction:name())

    local target_region_level = nil
    if not malakai_faction:is_human() then
        cm:transfer_region_to_faction(target_region:name(), malakai_faction:name())
        cm:heal_garrison(target_region:cqi())
        target_region_level = 2
    else
        -- TODO Zoom camera to new position
        target_region_level = 3 -- after capturing it'll became 2
    end
    cm:instantly_set_settlement_primary_slot_level(target_region:settlement(), target_region_level)
    return old_enemy_faction
end


function MGSWT:campaign_setup()
    if not cm:is_new_game() then
        return
    end

    local campaign_key = cm:model():campaign_name_key()
    local malakai_faction = self.faction
    local malakai_x, malakai_y = Klissan_CH:get_logical_position(malakai_faction:faction_leader())
    local old_enemy_faction = nil
    if campaign_key == 'wh3_main_combi' or campaign_key == 'cr_combi_expanded' then
        old_enemy_faction = self:ie_campaign_setup()
    elseif campaign_key == 'wh3_main_chaos' then
        old_enemy_faction = self:roc_campaign_setup()
    else
        return
    end

    self:resurrect_kraka_drak(malakai_x, malakai_y, old_enemy_faction)

    cm:reset_shroud(malakai_faction:name())

    -- make agreements and give vision over dawi factions capitals
    local same_culture_factions = malakai_faction:factions_of_same_subculture()
    for i = 0, same_culture_factions:num_items() - 1 do
        local faction = same_culture_factions:item_at(i)
        if not faction:is_dead() then
            cm:make_diplomacy_available(malakai_faction:name(), faction:name())
            --cm:force_grant_military_access(malakai_faction:name(), faction:name(), false)
            --cm:force_grant_military_access(faction:name(), malakai_faction:name(), false)
            if not faction:home_region():is_null_interface() then
                cm:make_region_seen_in_shroud(malakai_faction:name(), faction:home_region():name())
            end
        end
    end
end

-- cco TargettingContext
function MGSWT:get_targeting_ritual_key()
    return Klissan_CH:croot():Call('TargettingContext.RitualContext.RitualContext.Key')
end
--CommandingCharacterContext .AgentSubtypeRecordContext.Key

function MGSWT:get_targeting_target()
    local target_type, target_key = false, false
    target_type = Klissan_CH:croot():Call([=[
        ContextTypeId(TargettingContext.CurrentTargetContext)
    ]=])
    target_key = Klissan_CH:croot():Call([=[
        (
            target = TargettingContext.CurrentTargetContext,
            target_type = ContextTypeId(target)
        ) =>
        {
            target_type
                | 'CcoCampaignSettlement' => target.RegionRecordKey
                | 'CcoCampaignMilitaryForce' => target.CommandingCharacterContext.CQI
        }
    ]=])
    -- do not log here as it's used in repeat callback
    --if target_type then
    --    self:debug('Targetting target: '..target_type..','..target_key)
    --end
    return target_type, target_key
end


function MGSWT:is_target_context_exists()
    return Klissan_CH:croot():Call([=[
        IsContextValid(TargettingContext.CurrentTargetContext)
    ]=])
end


function MGSWT:get_grungni_radius()
    local radius_modifier = Klissan_CH:croot():Call([=[
        (
            malakai_faction = CampaignRoot.FactionList.FirstContext(FactionRecordContext.Key == 'wh3_dlc25_dwf_malakai'),
            malakai = malakai_faction.FactionLeaderContext,
            malakai_army = malakai.MilitaryForceContext,
            malakai_horde = malakai_army.HordeContext,
            building_chain_key = 'wh3_dlc25_dwf_spirit_of_grungni_support_radius',
            slot_with_desired_building_chain = malakai_horde.BuildingSlotList.FirstContext(BuildingContext.BuildingLevelRecordContext.BuildingChainRecordContext.Key == building_chain_key),
            building = slot_with_desired_building_chain.BuildingContext,
            radius_effect = building.EffectList.FirstContext(EffectKey == 'wh3_dlc25_effect_force_stat_support_radius')
        ) => GetIfElse(IsContextValid(radius_effect), radius_effect.Value, 0)
    ]=]) / 100.0
    return self.tsog_base_radius * (radius_modifier + 1.0)
end

function MGSWT:apply_effect_bundle_to_support_army(source_army_cqi, target_army_cqi)
    if MGSWT.malakai_support_army_cqi == nil or not cm:get_military_force_by_cqi(target_army_cqi) then
        return
    end
    self:debug('Creating an effect bundle for malakai support army')
    local bundle_key = 'klissan_malakai_support_army_bonuses'
    local custom_bundle = cm:create_new_custom_effect_bundle(bundle_key)
    local effects = Klissan_CH:get_army_effects(source_army_cqi)
    -- add +10 missing movement
    local force_movement_key = 'wh_main_effect_force_all_campaign_movement_range'
    if effects[force_movement_key] == nil then
        effects[force_movement_key] = 10
    else
        effects[force_movement_key] = effects[force_movement_key] + 10
    end
    for key, value in pairs(effects) do
        self:debug('Adding effect to support army: %s %d', key, value)
        custom_bundle:add_effect(key, 'force_to_force_own', value)
    end
    cm:remove_effect_bundle_from_force(custom_bundle:key(), target_army_cqi)
    cm:apply_custom_effect_bundle_to_force(custom_bundle, cm:get_military_force_by_cqi(target_army_cqi))
    self:debug('Effect bundle applied to support army')
end

function MGSWT:is_target_in_range()
    local radius = self:get_grungni_radius()
    local distance_to_target = self:get_travel_distance()
    self:debug('Grungni Range: %f, Distance to Target: %f', radius, distance_to_target)
    return distance_to_target < radius
end

--MGSWT:apply_effect_bundle_to_support_army(67, 1012)

-- todo rename to get distance to targeting
function MGSWT:get_travel_distance()
    local malakai_faction = self.faction
    local mx, my = Klissan_CH:get_logical_position(malakai_faction:faction_leader())
    local target_type, target_key = self:get_targeting_target()
    if not target_key then
        return -1
    end
    local target = nil
    if target_type == 'CcoCampaignSettlement' then
        target = cm:get_region(target_key):settlement()
    elseif target_type == 'CcoCampaignMilitaryForce' then
        target = cm:get_character_by_cqi(target_key)
    end
    local tx, ty = Klissan_CH:get_logical_position(target)
    local distance = math.sqrt(math.pow(math.abs(mx-tx), 2) + math.pow(math.abs(my-ty), 2))
    --to do how to log characters (name) command_queue_index
    self:debug('Travel Distance -> (%s,%s) = %f', target_type, target_key, distance)
    return distance
end


-- malakai can only be recruited, not replace the other lord cuz of bound horde
-- so we should execute it only on game start when malakai recruited (also remove other support armioes)
-- disband via cco MF
-- todo remove reinf time or give tzeentch's factionwide trait to malakai (lord)
function MGSWT:add_support_army_to_malakai()
    -- add support armies for all
    local ritual_key = 'klissan_malakai_support_army_ritual'
    local faction = MGSWT.faction
    local ritual_setup = cm:create_new_ritual_setup(faction, ritual_key)
    local ritual_target = ritual_setup:target()
    ritual_target:set_target_force(faction:faction_leader():military_force())
    cm:perform_ritual_with_setup(ritual_setup)

    -- remove support armies from other lords
    local mfs = MGSWT.faction:military_force_list()
    local x, y = Klissan_CH:get_logical_position(MGSWT.faction:faction_leader())
    for i=0, mfs:num_items()-1 do
        local mf = mfs:item_at(i)
        local char = mf:general_character()
        local xx, yy = Klissan_CH:get_logical_position(char)
        if mf:force_type():key() == 'KLISSAN_MALAKAI_SUPPORT_ARMY' and x ~= xx and y ~= yy then
            cm:kill_character(cm:char_lookup_str(char), true)
        end
    end

    self:update_malakai_support_army_cqi()
end

function MGSWT:update_malakai_support_army_cqi()
    -- there should be only one army left which is bound to malaki
    local mfl = MGSWT.faction:military_force_list()
    for i = 0, mfl:num_items() - 1 do
        local mf = mfl:item_at(i)
        if mf:force_type():key() == 'KLISSAN_MALAKAI_SUPPORT_ARMY' then
            MGSWT.malakai_support_army_cqi = mf:command_queue_index()
        end
    end
end

function MGSWT:init_malakai_force_created_listener()
    core:add_listener(
        Klissan_CH:get_listener_name('malakai_force_created'),
        "MilitaryForceCreated",
        function(context)
            -- done via get_faction cuz sometimes .faction is nil. Event triggered before inititalisation completed?
            return not cm:get_faction(MGSWT.faction_name):is_dead() and context:military_force_created():general_character():command_queue_index() == cm:get_faction(MGSWT.faction_name):faction_leader():command_queue_index()
        end,
        function(context)
            MGSWT:add_support_army_to_malakai()
        end,
        true
    )
end


function MGSWT:init_update_malakai_support_army_effects_listeners()
    local events = {
        'FactionTurnStart',
        'FactionTurnEnd',
    }

    for i=1,#events do
        local event_name = events[i]

        core:add_listener(
            Klissan_CH:get_listener_name('malakai_update_support_army_effects_'..event_name),
            event_name,
            function(context)
                return context:faction():name() == MGSWT.faction_name
                        and not cm:get_faction(MGSWT.faction_name):is_dead()
                        and cm:get_faction(MGSWT.faction_name):faction_leader():has_military_force()
                        and (MGSWT.malakai_support_army_cqi ~= nil and cm:get_military_force_by_cqi(MGSWT.malakai_support_army_cqi))
            end,
            function(context)
                local source_army_cqi = cm:get_faction(MGSWT.faction_name):faction_leader():military_force():command_queue_index()
                local target_army_cqi = MGSWT.malakai_support_army_cqi
                MGSWT:apply_effect_bundle_to_support_army(source_army_cqi, target_army_cqi)
            end,
            true
        )

    end
end


-- INIT
cm:add_post_first_tick_callback(function()
    MGSWT:init()
    MGSWT:campaign_setup()
    if cm:is_new_game() then
        MGSWT:add_support_army_to_malakai()
    end
    MGSWT:update_malakai_support_army_cqi() -- always update on game load as we don't store it
    MGSWT:init_malakai_force_created_listener()
    MGSWT:init_update_malakai_support_army_effects_listeners()
end)
