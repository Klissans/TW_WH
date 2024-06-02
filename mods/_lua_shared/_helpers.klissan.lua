Klissan_H = {} -- Klissan_Helpers

function Klissan_H:is_file_exist(name)
   local f=io.open(name, "r")
   if f~=nil then io.close(f) return true else return false end
end


function Klissan_H:get_key_sorted(t)
   local keyset={}
   local n=0
   for k,_ in pairs(t) do
      n=n+1
      keyset[n]=k
   end
   table.sort(keyset)
   return keyset
end


function Klissan_H:table_size(T)
   local count = 0
   for _ in pairs(T) do count = count + 1 end
   return count
end

function Klissan_H:minify_bool(b)
   if b then return 1 else return 0 end
end

function Klissan_H:register_function(t)
    setmetatable(t,{__index={is_battle=false, is_campaign=false, is_frontend=false}})
    local func, is_battle, is_campaign, is_frontend =
        t[1],
        t[2] or t.is_battle,
        t[3] or t.is_campaign,
        t[4] or t.is_frontend
    if is_battle and core:is_battle() then -- [string "script\_lib\mod\helpers.lua"]:41: attempt to index global 'core' (a nil value)
        bm:register_phase_change_callback("Deployment", func)
    else
        core:add_ui_created_callback(
                function()
                    if is_campaign and core:is_campaign() then
                        cm:add_post_first_tick_callback(func)
                    elseif is_frontend and core:is_frontend() then
                        func()
                    end
                end
        )
    end
end

function Klissan_H:register_function_everywhere(func)
    Klissan_H:register_function{func, is_battle=true, is_campaign=true, is_frontend=true}
end


--local object -- get your object however you do, cm:get_faction("faction key") for a faction script interface, etc.
function Klissan_H:inspect_object(object, out)
    local mt = getmetatable(object)
    for name, value in pairs(mt) do
        if is_function(value) then
            out("{INSPECTOR} Found: "..name.."()")
        elseif name == "__index" then
            for index_name, index_value in pairs(value) do
                if is_function(index_value) then
                    out("{INSPECTOR} Found: "..index_name.."() in index!")
                end
            end
        end
    end
end


function Klissan_H:get_var_name(var)
    local index = 1
    while true do
        local name, value = debug.getlocal(2, index)
        if not name then break end
        if value == var then
            return name
        end
        index = index + 1
    end
    -- NOT working for manuallycreated globals, import issues?
    for k, v in pairs(_G) do
        if v == var then
            return k
        end
    end
    return nil
end

function Klissan_H:setup_logging(obj, class_name)
    -- todo infer class_name by using get_var_name
    obj.log_to_file = false
    obj.log_file = '_'..class_name:lower()..'.klissan.log'

    obj.out = function(selfe, fmt, ...)
        local str = string.format('[['..class_name:upper()..']] :: '.. fmt, unpack(arg))
        out(str)
        if selfe.log_to_file then -- not efficient but whateever
            local log_file = io.open(selfe.log_file, "a+")
            log_file:write(str .. '\n')
            log_file:flush()
            io.close(log_file)
        end
    end

    obj.debug = function(selfe, fmt, ...)
        selfe:out('(DEBUG) '.. fmt, unpack(arg))
    end

    obj.error = function(selfe, fmt, ...)
        selfe:out('(ERROR) '.. fmt, unpack(arg))
    end

    obj.log_to_file = Klissan_H:is_file_exist(obj.log_file)
    if obj.log_to_file then
        io.open(obj.log_file,"w"):close()
    end

    return obj
end


--   function stringify_table(t)
--     local s = ''
--     for k,v in pairs(t) do
--         s = s .. 
--     end
--     return s
--   end