
---@class cheat_chat
local cheat_chat = {
    _bhc = nil,
    _chat = nil,
    _hotkey_file_name = '_enable_chat_hotkey.txt',
    _hotkey = nil,
    _edited_strings = {},
    _was_chat_opened_after_new_message = true,
}

function cheat_chat:out(s)     
    out('[Cheat Chat]: ' .. tostring(s))
end

function cheat_chat:create_chat()
    if core:is_frontend() then
        local tr = find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr')
        local chat =  UIComponent(tr:CreateComponent("multiplayer_chat", "ui/common ui/multiplayer_chat.twui.xml"))
        return chat
    else
        local chat_holder = find_uicomponent(core:get_ui_root(), "chat_holder")
        local chat = UIComponent(chat_holder:CreateComponent("multiplayer_chat", "ui/common ui/multiplayer_chat.twui.xml"))
        return chat
    end
end

function cheat_chat:destroy_chat()
    if core:is_frontend() then
        find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr', 'multiplayer_chat'):Destroy()
    else
        find_uicomponent(core:get_ui_root(), "chat_holder", 'multiplayer_chat'):Destroy()
    end
end

function cheat_chat:init_chat_hotkey_if_exists()
    local f = io.open(self._hotkey_file_name, "r")
    if not f then
        self:out('No hotkey config')
        return
    end
    local lines = {}
    for line in f:lines() do
        lines[#lines + 1] = line
    end
    io.close(f)

    self._hotkey = 'script_' .. lines[1]
    self:out('Hotkey for chat is ' .. self._hotkey)
end

function cheat_chat:init_battle_or_campaign()
    if not (core:is_battle() and bm:is_multiplayer() or core:is_campaign() and cm:is_multiplayer()) then
        return
    end
    self:init_chat_hotkey_if_exists()
    core:get_tm():repeat_real_callback(function() self:edit_strings() end, 100, 'Klissan_chat_edit_strings')
    local chat_holder = UIComponent(core:get_ui_root():CreateComponent("chat_holder", "ui/templates/empty_frame.twui.xml"))
    UIComponent(chat_holder:CreateComponent("multiplayer_chat", "ui/common ui/multiplayer_chat.twui.xml"))
    local bhc = find_uicomponent(core:get_ui_root(), "menu_bar", "buttongroup", "button_hud_chat")
    bhc:SetVisible(true)
    bhc:SetState("active")
    chat_holder:SetVisible(false)

    core:add_listener(
        "battle_menu_button_chat_clicked",
        "ComponentLClickUp",
        function(context)
            return context.string == "button_hud_chat"
        end,
        function(context)
            local bhc = get_hud_chat_button()
            local chat = get_chat_parent()
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
                local bhc = get_hud_chat_button()
                local chat = get_chat_parent()
                chat:SetVisible(false)
                -- self:destroy_chat()
            end,
            true
    )
end


function cheat_chat:init_frontend()
    if not core:is_frontend() then
        return
    end
    self:init_chat_hotkey_if_exists()
    core:get_tm():repeat_real_callback(function() self:edit_strings() end, 100, 'Klissan_chat_edit_strings')
    local tr = get_chat_parent()
    core:get_tm():repeat_real_callback(function() self:check_if_mp_lobby() end, 250, 'Klissan_frontend_mp_lobby_chat')

    core:add_listener(
        "lobby_button_hud_chat_clicked",
        "ComponentLClickUp",
        function(context)
            return context.string == "button_hud_chat"
        end,
        function(context)
            local bhc = get_hud_chat_button()
            local tr = get_chat_parent()
            -- if tr:Visible() then
            --     self:destroy_chat()
            -- else
            --     self:create_chat()
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
                local tr = get_chat_parent()
                local chat = find_uicomponent(tr, "multiplayer_chat")
                tr:SetVisible(false)
                -- self:destroy_chat()
            end,
            true
    )
end

function get_chat_parent()
    if core:is_frontend() then 
        return find_uicomponent(core:get_ui_root(), "sp_frame", 'frame_tr')
    else
        return find_uicomponent(core:get_ui_root(), "chat_holder")
    end
end

function get_hud_chat_button()
    if core:is_frontend() then 
        return find_uicomponent(core:get_ui_root(), "sp_frame", "button_hud_chat")
    else
        return find_uicomponent(core:get_ui_root(), "menu_bar", "buttongroup", "button_hud_chat")
    end
end


function table_size(T)
    local count = 0
    for _ in pairs(T) do count = count + 1 end
    return count
 end


function cheat_chat:edit_strings()
    local chat_parent = get_chat_parent()
    local strings_parent = find_uicomponent(chat_parent, 'multiplayer_chat', 'chat_listview', 'list_clip', 'list_box')
    local alert =  find_uicomponent(get_hud_chat_button(), 'chat_alert_icon')
    if not strings_parent or strings_parent:ChildCount() == table_size(self._edited_strings) then
        if not self._was_chat_opened_after_new_message and chat_parent:Visible() then
            self._was_chat_opened_after_new_message = true
            alert:SetVisible(false)
        end
        return
    end
    -- new string

    -- set alert_icon_ if chat is hidden
    if not chat_parent:Visible() then
        self._was_chat_opened_after_new_message = false
        alert:SetVisible(true)
    end

    for i = 0, strings_parent:ChildCount() - 1 do
        local string = UIComponent(strings_parent:Find(i))
        if not self._edited_strings[string:Id()] then
            local orig_text = string:GetStateText()
            self:out('New Text: ' .. orig_text)
            local edited_string = edit_string(orig_text, i)
            self:out('Edited Text: ' .. edited_string)
            string:SetText(edited_string, '_todo_db_text_key_')
            self:out('Edited Text: ' .. edited_string)
            self._edited_strings[string:Id()] = true
        end
    end

end

function edit_string(s, i)
    local edited_string = s
    if s:find('/help') and i == 0 then
        edited_string = edited_string .. '\nThe [[col:yellow]]Chat[[/col]][[img:ui/mod/emojis/chat.png]][[/img]] has been resurrected by Klissan for MP community. Enjoy!'
    end
    -- edited_string = edited_string.gsub()
    -- emoji replacer
    edited_string = edited_string:gsub('`(%a+)`', '[[img:ui/mod/emojis/%1.png]][[/img]]')

    -- nickname formatter
    edited_string = format_nickname(edited_string)

    -- random colorizer
    local color_pattern = '~([%w%s]+)~'
    while edited_string:find_lua(color_pattern) do
        i, j, c = edited_string:find_lua(color_pattern)
        local sub = edited_string:sub(i+1, j-1):gsub('(.)', '[[col:__col__]]%1[[/col]]')
        edited_string = edited_string:sub(0, i-1) .. sub .. edited_string:sub(j+1)
    end
    edited_string = randomly_colorize_string(edited_string)
    return edited_string
end

function  randomly_colorize_string(s)
    local colors = {'red', 'green', 'yellow', 'magic'}
    local li = -1
    while s:find('__col__') do
        local ri = nil
        repeat
            ri = math.random(1, #colors)
        until(ri ~= li)
        s = replaceFirstOccurrence(s, '__col__', colors[ri])
        li = ri
    end
    return s
end

function format_nickname(s)
    es = s
    es = es:gsub('^(Klissan)', '[[img:ui/mod/emojis/gsl.png]][[/img]]~%1~[[img:ui/mod/emojis/gsl.png]][[/img]]')
    es = es:gsub('^(Roflan)(Buldiga)', '[[col:yellow]]%1[[/col]][[img:ui/mod/emojis/komar.png]][[/img]][[col:red]]%2[[/col]]')
    es = es:gsub('^(Risum)', '%1[[img:ui/mod/emojis/nerisum.png]][[/img]]')
    es = es:gsub('^(Ahashra) (Riel)', '[[img:ui/mod/emojis/cb.png]][[/img]][[col:yellow]]%1[[/col]][[img:ui/mod/emojis/cb.png]][[/img]][[col:red]]%2[[/col]][[img:ui/mod/emojis/cb.png]][[/img]]')
    es = es:gsub('^(Deobald) (of) (Bretonnia)', '[[img:ui/mod/emojis/deo.png]][[/img]][[col:red]]%1[[/col]] [[col:yellow]]%2[[/col]] [[col:magic]]%3[[/col]][[img:ui/flags/wh_main_brt_bretonnia/mon_64.png]][[/img]]')
    es = es:gsub('^(GapaKtus)', '%1[[img:ui/mod/emojis/q.png]][[/img]]')
    return es
end


function replaceFirstOccurrence(original, pattern, replacement)
    local start_i, end_i = original:find(pattern)
    if start_i then
        local newString = original:sub(1, start_i - 1) .. replacement .. original:sub(end_i + 1)
        return newString
    else
        return original
    end
end



function cheat_chat:check_if_mp_lobby()
    local bhc = get_hud_chat_button()
    local cb = find_uicomponent(core:get_ui_root(), "custom_battle")
    local tr = get_chat_parent()
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

if not core:is_battle() then
	core:add_ui_created_callback(
		function()
			if core:is_campaign() then 
				cm:add_post_first_tick_callback(function()
					cheat_chat:init_battle_or_campaign()
				end)
			elseif core:is_frontend() then
				cheat_chat:init_frontend()
			end
		end
	)
else
	bm:register_phase_change_callback("Deployment", function() cheat_chat:init_battle_or_campaign() end)
end


core:add_listener(
    "chat_refresh_button_clicked",
    "ComponentLClickUp",
    function(context)
        return context.string == "button_lock_chat"
    end,
    function(context)
        cheat_chat:out('Recreating chat')
        cheat_chat:destroy_chat()
        cheat_chat:create_chat()
        cheat_chat._edited_strings = {}
    end,
    true
)

core:add_listener(
    "chat_hotkey_pressed",
    "ShortcutPressed",
    function(context)
        return cheat_chat and cheat_chat._hotkey and cheat_chat._hotkey == context.string
    end,
    function(context)
        if core:is_frontend() then
            local tr = get_chat_parent()
            local chat = find_uicomponent(tr, "multiplayer_chat")
            if chat then
                tr:SetVisible(not tr:Visible())
            end
        else
            local chat = get_chat_parent()
            chat:SetVisible(not chat:Visible())
        end

    end,
    true
)


-- https://discord.com/channels/373745291289034763/1021968669946953758/1022089976168583248
math.randomseed(os.clock())
math.randomseed(os.clock())
math.randomseed(os.clock())
math.randomseed(os.clock())
math.randomseed(os.clock())
math.randomseed(os.clock())
math.randomseed(os.clock())
math.randomseed(os.clock())

for i=1, math.random(math.random(100)) do
    math.random(i)
end