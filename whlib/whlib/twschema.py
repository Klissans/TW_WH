import os
import json
import glob

from .settings import SETTINGS
from .dbtable import DBTable
from.utils import read_db_tables


class TWSchema:
    def __init__(self,
                 schema_path: str = os.path.join(SETTINGS['schema_path'], SETTINGS['schema_name']),
                 tables_path: list=SETTINGS['extract_path']
                 ):
        self.schema_path = schema_path
        with open(schema_path, encoding='utf-8') as f:
            self.schema = json.load(f)

        assert self.schema['version'] == 5

        self._db_tables_schemas = {}
        for tname, version_list in self.schema['definitions'].items():
            self._db_tables_schemas[tname] = version_list
            # for version in version_list:
            #     self._db_tables_schemas[tname][version['version']] = version


        db_tables = read_db_tables(tables_path)
        self._set_actual_schemas(db_tables)
        self._fix_references(self.actual_db_tables_schemas)

    def get_schema(self, table_name):
        return self.actual_db_tables_schemas[table_name]

    def get_loc_schema(self):
        return self.schema['versioned_files']['Loc'][0][0]

    def _get_field_by_schema(self, schema, field_name) -> dict:
        for field in schema['fields']:
            if field['name'] == field_name:
                return field

    def get_field_info(self, table_name, field_name) -> dict:
        return self._get_field_by_schema(self.get_schema(table_name), field_name)

    def _get_schema(self, schemas,  version: int):
        for s in schemas:
            if int(s['version']) == version:
                return s
        raise ValueError(f'No schema of the version {version} has been found')

    def _get_key_counts(self, schema):
        return sum(field['is_key'] for field in schema['fields'])

    def _set_default_referenced_by_for_key(self, schema):
        for field in schema['fields']:
            if field['is_key']:
                field['referenced_by'] = []

    def _get_field(self, table_name:str, field_name:str):
        #Invalid ID for table pdlc_tables => so we have to lower
        table_schema = self.actual_db_tables_schemas[table_name]
        for field in table_schema['fields']:
            if field['name'] == field_name.lower():
                return field
        print(f"Invalid {field_name} for table {table_name}")
        raise ValueError(f"Invalid {field_name} for table {table_name}")

    def _fix_references(self, schemas):
        for table_name, info in schemas.items():
            for field in info['fields']:
                if field['is_reference'] is not None:
                    ref_table, ref_column = field['is_reference']
                    if ref_table in schemas:
                        pass
                    elif ref_table + '_tables' in schemas:
                        field['is_reference'][0] = ref_table + '_tables'
                    #     if ref_table + '_junctions_tables' in schemas:
                    #         raise ValueError(f"Multiple references {field['is_reference']}")
                    # elif ref_table + '_junctions_tables' in schemas:
                    #     new_ref_table_name += '_junctions_tables'
                    else:
                        print(f"Unknown reference {field['is_reference']}")

                    #add referenced_by to target table scheme
                    try:
                        target_field = self._get_field(field['is_reference'][0], field['is_reference'][1])
                        target_field['referenced_by'].append((table_name, field['name']))
                    except (KeyError, ValueError) as e:
                        #skip unknown tables
                        field['is_reference'] = None
                        pass


    def _set_actual_schemas(self, db_tables: list):
        self.actual_db_tables_schemas = {}
        for name, table in db_tables.items():
            table_name = table.schema['name']
            table_version = table.schema['version']
            schema_versions = self._db_tables_schemas[table_name]
            actual_schema = self._get_schema(schema_versions, table_version)
            self.actual_db_tables_schemas[table_name] = actual_schema
            self.actual_db_tables_schemas[table_name]['n_keys'] = self._get_key_counts(actual_schema)
            self._set_default_referenced_by_for_key(actual_schema)
        del self._db_tables_schemas


    def check_schema(self):
        for table_name, v in self.actual_db_tables_schemas.items():
            fields = v['fields']
            i = 0
            for f in fields:
                if f['is_reference'] is not None and 'referenced_by' in f and len(f['referenced_by']) > 0:
                    print('Key is a reference being refrenced: ', table_name, f['name'])
                if 'referenced_by' in f and len(f['referenced_by']) > 0:
                    i += 1
            if i > 1:
                print('Many referenced fields: ', table_name)

    def get_graph_nodes(self):
        nodes = []
        for table_name, info in self.actual_db_tables_schemas.items():
            nodes.append(table_name)
        return nodes

    def get_graph_edges(self):
        edges = []
        for table_name, info in self.actual_db_tables_schemas.items():
            for field in info['fields']:
                if field['is_key'] and len(field['referenced_by']) != 0:
                    for (ref_table, ref_column) in field['referenced_by']:
                        edges.append((ref_table, table_name))
        return edges

    def create_cytoscape_nodes(self, graph):
        cy_nodes = []
        gnodes = graph.nodes() # hz why it works this way
        for name in graph.nodes():
            cy_nodes.append(
                {
                    'data': {'id': name, 'label': name, 'degree': graph.degree[name]},
                    'position': {'x': gnodes[name]['x'], 'y': gnodes[name]['y']},
                }
            )
        return cy_nodes

    def create_cytoscape_edges(self, graph):
        cy_edges = []
        for table_name, info in self.actual_db_tables_schemas.items():
            if table_name not in graph.nodes(): # TODO
                continue
            for field in info['fields']:
                if field['is_key'] and len(field['referenced_by']) != 0:
                    for (ref_table, ref_column) in field['referenced_by']:
                        cy_edges.append({'data': {'id': f"{ref_table}_{table_name}", 'source': ref_table, 'target': table_name}})
        return cy_edges
