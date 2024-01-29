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


--   function stringify_table(t)
--     local s = ''
--     for k,v in pairs(t) do
--         s = s .. 
--     end
--     return s
--   end