

function get_character_coordinates(character)
    return character:logical_position_x(), character:logical_position_y()
end
--cm:treasury_mod('wh3_dlc25_dwf_malakai', -100)

local croot = cco('CcoCampaignRoot', 'CampaignRoot')

-- cco TargettingContext
function get_ritual_key()
    return croot:Call('TargettingContext.RitualContext.RitualContext.Key')
end

function get_target()
    local target_type = croot:Call([=[
        ContextTypeId(TargettingContext.CurrentTargetContext)
    ]=])
    local target_key = croot:Call([=[
        (
            target = TargettingContext.CurrentTargetContext,
            target_type = ContextTypeId(target)
        ) =>
        {
            target_type
                | 'CcoCampaignSettlement' => target.RegionRecordKey
        }
    ]=])
    return target_type, target_key
end

function get_travel_distance()
    local malakai_faction = cm:get_faction('wh3_dlc25_dwf_malakai')
    local mx, my = get_character_coordinates(malakai_faction:faction_leader())
    local target_type, target_key = get_target()
    local tx, ty = get_character_coordinates(cm:get_region(target_key):settlement())
    return math.sqrt(math.pow(math.abs(mx-tx), 2) + math.pow(math.abs(my-ty), 2))
end

function get_ritual_cost()
    local rituals_mapping = { -- append '_ritual'
        ['klissan_malakai_travel_ritual'] = math.ceil(get_travel_distance() * 5)
    }
    return rituals_mapping[get_ritual_key()]
end

function set_ritual_cost()
    local cost = get_ritual_cost()
    local cost_str = tostring(cost)
    local ui_perform_cost = find_uicomponent(core:get_ui_root(), 'tzeentch_changing_of_ways', 'manipulation_info', 'button_perform', 'duration_cost_holder', 'dy_cost')
    console_print(cost_str)
    ui_perform_cost:SetText(cost_str, cost_str)
end

core:get_tm():remove_real_callback('klissan_malakai_set_ritual_cost')
core:get_tm():repeat_real_callback(function() set_ritual_cost() end, 250, 'klissan_malakai_set_ritual_cost')