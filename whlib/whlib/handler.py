import pandas as pd

from .settings import SETTINGS
from .twschema import TWSchema
from .utils import read_db_tables, read_loc_tables, read_meta_files


class Handler:

    def __init__(self, settings=SETTINGS):
        self._table_name_keyword = '__table_name__'
        self._value_keyword = '__value__'
        self.twschema = TWSchema()
        self.db = read_db_tables(settings['extract_path'], read_data=True)
        self.moddb = {}
        self.locs = read_loc_tables(settings['extract_path'], read_data=True)
        self.modlocs = {}
        self._set_keys()
        self.anim_files = read_meta_files()

    def isnull(self, key):
        return pd.isnull(key)

    def _set_keys(self):
        for k, schema in self.twschema.actual_db_tables_schemas.items():
            if k == 'dilemmas_tables':  # TODO
                continue
            key_fields = self._get_schema_keys(schema['fields'])
            self.db[k].data.set_index(key_fields, drop=False, inplace=True)
            self.db[k].data.index.name = self.db[k].table_name

        for k, v in self.locs.items():
            if v.schema['name'] == 'Loc':
                key_fields = ['key']
            else:
                raise ValueError(v.schema['name'])
            # key_fields = self._get_schema_keys(schema['localised_fields'])
            v.data.set_index(key_fields, drop=False, inplace=True)
            v.data.index.name = v.table_name

    def _get_schema_keys(self, schema_fields):
        key_fields = []
        for field in schema_fields:
            if field['is_key']:
                key_fields.append(field['name'])
        return key_fields

    def get_mod_table(self, orig_table_name, mod_table_name):
        if orig_table_name in self.moddb.keys():
            return self.moddb[orig_table_name][mod_table_name]
        if orig_table_name in self.modlocs.keys():
            return self.modlocs[orig_table_name][mod_table_name]

    def _find_mod_table(self, mod_table_name):
        for orig_table_name in self.moddb.keys():
            if mod_table_name in self.moddb[orig_table_name].keys():
                return self.moddb[orig_table_name][mod_table_name]
        for orig_table_name in self.modlocs.keys():
            if mod_table_name in self.modlocs[orig_table_name].keys():
                return self.modlocs[orig_table_name][mod_table_name]
        raise KeyError(mod_table_name)

    def get_entry_by_index(self, table_name:str, index) -> dict:
        if self.isnull(index):
            return None
        res = None
        if index in self.db[table_name].data.index:
            res = self.db[table_name].data.loc[index].to_dict()
        elif table_name in self.moddb.keys():
            for mod_table_name in self.moddb[table_name].keys():
                if index in self.moddb[table_name][mod_table_name].data.index:
                    res = self.moddb[table_name][mod_table_name].data.loc[index].to_dict()
                    break
        if res is None:
            return None
        res[self._table_name_keyword] = table_name
        res[self._value_keyword] = index
        return res


    def get_entries_by_value(self, table_name:str, field_name:str, value:str) -> dict:
        t = self.db[table_name].data
        res_array = t[t[field_name] == value].to_dict('records')
        if len(res_array) == 0:
            return None
        for record in res_array:
            record[self._table_name_keyword] = table_name
            record[self._value_keyword] = value
        return res_array

    def _resolve_key(self, entry:dict, ref_field:str):
        table_name = entry[self._table_name_keyword]
        field_value = entry[ref_field]
        if type(field_value) is dict:
            return field_value
        if pd.isnull(field_value):
            return None
        # src_schema = self.twschema.get_schema(table_name)
        src_field_info = self.twschema.get_field_info(table_name, ref_field)
        if src_field_info['is_reference'] is None:
            raise ValueError('Reference is None')

        dst_table_name, dst_field_name = src_field_info['is_reference']
        dst_schema = self.twschema.get_schema(dst_table_name)
        dst_ref_field_info = self.twschema.get_field_info(dst_table_name, dst_field_name)

        ref_data = None
        if dst_schema['n_keys'] == 1:
            if dst_ref_field_info['is_key']:
                ref_data = self.get_entry_by_index(dst_table_name, field_value)
            else:
                raise ValueError('Reference is not a key in single index table')
        else:
            if dst_ref_field_info['is_key']:
                ref_data = self.get_entries_by_value(dst_table_name, dst_field_name, field_value)
            else:
                raise ValueError('Reference is not a key in multi index table')

        entry[ref_field] = ref_data
        return entry[ref_field]

    def expand_entry(self, entry:dict):
        schema = self.twschema.get_schema(entry[self._table_name_keyword])
        for field in schema['fields']:
            if field['is_reference'] is not None:
                self._resolve_key(entry, field['name'])
        pass

    def expand_entry_recursively(self, entry:dict):
        self.expand_entry(entry)
        for k, v in entry.items():
            if type(v) is dict:
                self.expand_entry_recursively(v)
            elif type(v) is list:
                for e in v:
                    self.expand_entry_recursively(e)
        pass

    def _resolve_key_array(self, entry:dict, path:list):
        if len(path) == 0:
            return
        ref_field = path.pop(0)
        ret = self._resolve_key(entry, ref_field)
        if ret is None:
            return
        if type(ret) is dict:
            self._resolve_key_array(entry[ref_field], path)
        if type(ret) is list:
            for e in ret:
                self._resolve_key_array(e, path)

    def duplicate_table(self, table_name, copy_data=False, new_name=None, prefix=None):
        if new_name is None:
            new_name = table_name
        if prefix is not None:
            new_name = prefix + new_name
        if table_name in self.db:
            self.moddb.setdefault(table_name, {})
            self.moddb[table_name][new_name] = self.db[table_name].copy(copy_data=copy_data, new_name=new_name)
            return self.moddb[table_name][new_name]
        if table_name in self.locs:
            self.modlocs.setdefault(table_name, {})
            self.modlocs[table_name][new_name] = self.locs[table_name].copy(copy_data=copy_data, new_name=new_name)
            return self.modlocs[table_name][new_name]

    def append(self, table_name, new_df):
        table = self._find_mod_table(table_name)
        if table.schema['type'] == 'DB':
            table_schema = self.twschema.get_schema(table.schema['name'])
        elif table.schema['type'] == 'Loc':
            table_schema = self.twschema.get_loc_schema()
        key_fields = self._get_schema_keys(table_schema['fields'])
        new_df.set_index(key_fields, drop=False, inplace=True)
        table.data = pd.concat([table.data, new_df])

    def dump_mod_tables(self, output_dir:str):
        for key, mod_tables in self.moddb.items():
            for name, table in mod_tables.items():
                table.dump(output_dir)
        for key, mod_tables in self.modlocs.items():
            for name, table in mod_tables.items():
                table.dump(output_dir)
