import os
import csv
import pandas as pd

class DBTable:

    def __init__(self, tsv_path:str='', read_data=False, from_copy=None):
        if from_copy is not None:
            self.tsv_dir = from_copy['tsv_dir']
            self.table_name = from_copy['table_name']
            self.schema = from_copy['schema']
            self.data = from_copy['data']
            return

        self.tsv_dir = os.path.dirname(tsv_path)

        with open(tsv_path, 'r', encoding='utf-8') as f:
            f.readline()
            schema_line = f.readline().split(';')

        if 'data__' in tsv_path:
            self.table_name = tsv_path.split(os.sep)[-2]
            self.schema = {'type': 'DB', 'name': schema_line[0][1:], 'version': int(schema_line[1]), 'path': schema_line[2]}
        else:
            self.table_name = tsv_path.split(os.sep)[-1].split('.')[0] # + '.loc'
            self.schema = {'type': 'Loc', 'name': schema_line[0][1:], 'version': int(schema_line[1]), 'path': schema_line[2]}

        if read_data:
            self.data = pd.read_csv(tsv_path, sep='\t', encoding='utf-8', skiprows=[1], quoting=csv.QUOTE_NONE, low_memory=False)
        else:
            self.data = pd.read_csv(tsv_path, sep='\t', encoding='utf-8', nrows=0)
        self.data.index.name = self.table_name

    def copy(self, new_name=None, copy_data=False):
        if new_name is None:
            new_name = self.table_name
        if copy_data:
            data = self.data.copy()
        else:
            data = self.data.iloc[0:0].copy()
        return DBTable(from_copy={
            'tsv_dir': self.tsv_dir,
            'table_name': new_name,
            'schema': self.schema,
            'data': data
        })


    def dump(self, output_dir:str):
        output_path = os.path.join(output_dir, self.tsv_dir)
        os.makedirs(output_path, exist_ok=True)
        # if self.table_name == 'special_ability_phases__.loc':
        #     output_path = f"{output_dir}/{self.table_name}.tsv"
        # if self.table_name == 'random_localisation_strings__':
        #     output_path = f"{output_dir}/{self.table_name}.loc.tsv"
        schema_line = None
        if self.schema['type'] == 'DB':
            schema_line = f"#{self.schema['name']};{self.schema['version']};db/{self.schema['name']}/{self.table_name}"
            fn = f"{self.table_name}.tsv"
        if self.schema['type'] == 'Loc':
            schema_line = f"#Loc PackedFile;{self.schema['version']};text/db/{self.table_name}.loc"
            fn = f"{self.table_name}.loc.tsv"

        output_path = os.path.join(output_path, fn)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\t'.join(self.data.columns) + '\n')
            f.write(schema_line+'\n')
            self.data.to_csv(f, sep='\t', header=False, index=False)
        pass