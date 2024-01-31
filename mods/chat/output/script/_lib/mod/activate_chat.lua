
---@class cheat_chat
local cheat_chat = {
    _bhc = nil,
    _chat = nil,
}

function cheat_chat:out(s)     
    out('[Cheat Chat]: ' .. tostring(s))
end

function cheat_chat:create_chat(is_fe)
    if is_fe then
        local tr = find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr')
        local chat =  UIComponent(tr:CreateComponent("multiplayer_chat", "ui/common ui/multiplayer_chat.twui.xml"))
        return chat
    else
        local chat_holder = find_uicomponent(core:get_ui_root(), "chat_holder")
        local chat = UIComponent(chat_holder:CreateComponent("multiplayer_chat", "ui/common ui/multiplayer_chat.twui.xml"))
        return chat
    end
end

function cheat_chat:destroy_chat(is_fe)
    if is_fe then
        find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr', 'multiplayer_chat'):Destroy()
    else
        find_uicomponent(core:get_ui_root(), "chat_holder", 'multiplayer_chat'):Destroy()
    end
end

function cheat_chat:init_battle()
    local chat_holder = UIComponent(core:get_ui_root():CreateComponent("chat_holder", "ui/templates/empty_frame.twui.xml"))
    UIComponent(chat_holder:CreateComponent("multiplayer_chat", "ui/common ui/multiplayer_chat.twui.xml"))
    local bhc = find_uicomponent(core:get_ui_root(), "menu_bar", "buttongroup", "button_hud_chat")
    bhc:SetVisible(true)
    bhc:SetState("active")

    core:add_listener(
        "battle_menu_button_chat_clicked",
        "ComponentLClickUp",
        function(context)
            return context.string == "button_hud_chat"
        end,
        function(context)
            local bhc = find_uicomponent(core:get_ui_root(), "menu_bar", "buttongroup", "button_hud_chat")
            local chat = find_uicomponent(core:get_ui_root(), "chat_holder")
            -- if chat:Visible() then
            --     self:destroy_chat()
            -- else
            --     self:create_chat()
            -- end
            chat:SetVisible(not chat:Visible())
        end,
        true
    )

    core:add_listener(
            "chat_button_toggle_chat_clicked",
            "ComponentLClickUp",
            function(context)
                return context.string == "button_toggle_chat"
            end,
            function(context)
                local bhc = find_uicomponent(core:get_ui_root(), "menu_bar", "buttongroup", "button_hud_chat")
                local chat = find_uicomponent(core:get_ui_root(), "chat_holder")
                chat:SetVisible(false)
                -- self:destroy_chat()
            end,
            true
    )
end


function cheat_chat:init_frontend()
    local tr = find_uicomponent(core:get_ui_root(), "sp_frame", "frame_tr")
    core:get_tm():repeat_real_callback(function() self:check_if_mp_lobby() end, 250, 'Klissan_frontend_mp_lobby_chat')

    core:add_listener(
        "lobby_button_hud_chat_clicked",
        "ComponentLClickUp",
        function(context)
            return context.string == "button_hud_chat"
        end,
        function(context)
            local bhc = find_uicomponent(core:get_ui_root(), "sp_frame", "button_hud_chat")
            local tr = find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr')
            -- if tr:Visible() then
            --     self:destroy_chat(true)
            -- else
            --     self:create_chat(true)
            -- end
            tr:SetVisible(not tr:Visible())
        end,
        true
    )

    core:add_listener(
            "chat_button_toggle_chat_clicked",
            "ComponentLClickUp",
            function(context)
                return context.string == "button_toggle_chat"
            end,
            function(context)
                local tr = find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr')
                local chat = find_uicomponent(tr, "multiplayer_chat")
                tr:SetVisible(false)
                -- self:destroy_chat(true)
            end,
            true
    )
end



function cheat_chat:check_if_mp_lobby()
    local bhc = find_uicomponent(core:get_ui_root(), "sp_frame", "button_hud_chat")
    local cb = find_uicomponent(core:get_ui_root(), "custom_battle")
    local tr = find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr')
    local chat = find_uicomponent(tr, "multiplayer_chat")

    if cb and find_uicomponent(cb, 'ready_parent', 'title_plaque', 'tx_header'):CurrentState() == "mp" 
            or find_uicomponent(core:get_ui_root(), 'mp_grand_campaign') then

        -- self:out('Making chat button visible')
        if not chat then
            -- self:out('Creating chat')
            UIComponent(tr:CreateComponent("multiplayer_chat", "ui/common ui/multiplayer_chat.twui.xml"))
        end
        bhc:SetVisible(true)
        bhc:SetDisabled(false)
        return
    end

    -- not mp environment
    if chat then
        -- self:out('Destroying chat')
        chat:Destroy()
    end
    -- self:out('Hiding chat button')
    tr:SetVisible(false)
    bhc:SetVisible(false)
    bhc:SetDisabled(true)
    bhc:SetState('down_off')
end



if core:is_battle() and bm:is_multiplayer() then
    core:get_tm():real_callback(function() cheat_chat:init_battle() end, 1000, 'Klissan_init_chat_battle_rc')
end

if core:is_campaign() and cm:is_multiplayer() then
    core:get_tm():real_callback(function() cheat_chat:init_battle() end, 1000, 'Klissan_init_chat_campaign_rc')
end



if core:is_frontend() then
    core:get_tm():real_callback(function() cheat_chat:init_frontend() end, 1000, 'Klissan_init_chat_rc')
end



core:add_listener(
    "chat_refresh_button_clicked",
    "ComponentLClickUp",
    function(context)
        return context.string == "button_lock_chat"
    end,
    function(context)
        cheat_chat:out('Recreating chat')
        cheat_chat:destroy_chat(core:is_frontend())
        cheat_chat:create_chat(core:is_frontend())
    end,
    true
)