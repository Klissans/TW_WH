import argparse
import json
import subprocess

import networkx as nx

from whlib.rpfm4_wrapper import RPFM4Wrapper
from whlib.twschema import TWSchema


def optimize_graph_layout(fn: str):
    # https://github.com/kwonoh/gephi-cli
    ofn = 'out_'+ fn
    gephi_cmds = [
        'java', '-jar', './utils/gephi-cli.jar', 'force-atlas-2',
        '-i', fn, '-o', ofn,
        '--max-iters=20000',
        '--thread-count=15',
        '--scaling-ratio=15',
        '--outbound-attr-dist=true',
        '--adjust-sizes=true'
    ]
    subprocess.run(gephi_cmds)
    return ofn


def expand_graph_layout(graph, scale_factor=5):
    main_node = graph.nodes['factions_tables']
    x0, y0 = main_node['x'], main_node['y']
    gnodes = graph.nodes()  # hz why it works this way
    for name in graph.nodes():
        node = gnodes[name]
        node['x'] = (node['x'] - x0) * scale_factor
        node['y'] = (node['y'] - y0) * scale_factor
    return graph


def fix_gexf_version(fn):
    replacer = """<gexf version="1.2" 
    xmlns="http://www.gexf.net/1.2draft" 
    xmlns:viz="http://www.gexf.net/1.2/viz" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://www.gexf.net/1.2draft 
    http://www.gexf.net/1.2draft/gexf.xsd">"""
    with open(fn) as f:
        content = f.readlines()
    content[1] = replacer
    with open(fn, 'w') as f:
        f.writelines(content)


def order_graph_layout(graph):
    UG = graph.to_undirected()
    sub_graphs = []
    for i, cc in enumerate(nx.connected_components(UG)):
        if i == 0:
            brc_x = max(UG.nodes[name]['x'] for name in UG.nodes)
            brc_y = min(UG.nodes[name]['y'] for name in UG.nodes)
        else:
            sub_graphs.append(cc)

    offset_x = 10
    offset_y = -500
    for sb in sub_graphs:
        ss_blc_x = min(UG.nodes[name]['x'] for name in sb)
        ss_blc_y = min(UG.nodes[name]['y'] for name in sb)
        for node_name in sb:
            node = graph.nodes[node_name]
            node['x'] = brc_x + offset_x + (node['x'] - ss_blc_x)
            node['y'] = brc_y + offset_y + (node['y'] - ss_blc_y)
        offset_y += 100
    return graph


if __name__ == '__main__':
    # argparser = argparse.ArgumentParser(description='Generates the mod packfile to Documents/TWMods/')
    # argparser.add_argument('path_to_rpfm_cli',
    #                        help='path to rpfm_cli.exe used for extracting and creating mod files')
    # argparser.add_argument('-g', dest='path_to_game', default=twgame_path,
    #                        help=f'path to the main directory of {twgame}(default: {twgame_path})')

    # args = argparser.parse_args()

    rpfm4 = RPFM4Wrapper()
    rpfm4.extract_data()

    twschema = TWSchema()
    twschema.check_schema()

    G = nx.DiGraph()
    G.add_nodes_from(twschema.get_graph_nodes())
    G.add_edges_from(twschema.get_graph_edges())

    fn = "wh3_db_scheme.graphml"
    nx.write_graphml(G, fn)
    ofn = optimize_graph_layout(fn)
    ofn = 'out_' + fn

    optimized_graph = nx.read_graphml(ofn)
    optimized_graph = order_graph_layout(optimized_graph)
    expand_graph_layout(optimized_graph, scale_factor=10)

    cytoscape_elements = twschema.create_cytoscape_nodes(optimized_graph) + twschema.create_cytoscape_edges(optimized_graph)
    with open('../TWWH_db_graph/schema.json', 'w') as f:
        json.dump(twschema.actual_db_tables_schemas, f)
    with open('../TWWH_db_graph/graph.json', 'w') as f:
        json.dump(cytoscape_elements, f)
