function is_file_exist(name)
   local f=io.open(name, "r")
   if f~=nil then io.close(f) return true else return false end
end


function get_key_sorted(t)
   local keyset={}
   local n=0
   for k,_ in pairs(t) do
      n=n+1
      keyset[n]=k
   end
   table.sort(keyset)
   return keyset
end


function table_size(T)
   local count = 0
   for _ in pairs(T) do count = count + 1 end
   return count
end

function minify_bool(b)
   if b then return 1 else return 0 end
end


function register_function_everywhere(func)
    register_function{func, is_battle=true, is_campaign=true, is_frontend=true}
end

function register_function(t)
    setmetatable(t,{__index={is_battle=false, is_campaign=false, is_frontend=false}})
    local func, is_battle, is_campaign, is_frontend =
        t[1],
        t[2] or t.is_battle,
        t[3] or t.is_campaign,
        t[4] or t.is_frontend
    if is_battle and core:is_battle() then
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



--   function stringify_table(t)
--     local s = ''
--     for k,v in pairs(t) do
--         s = s .. 
--     end
--     return s
--   end