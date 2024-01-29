import os
import glob
import json
from functools import partial
import multiprocessing as mp
from bs4 import BeautifulSoup

from .dbtable import DBTable
from .settings import SETTINGS


def read_db_tables(extract_path, read_data=False):
    old_cwd = os.getcwd()
    # os.chdir(os.path.join(extract_path,'data.pack'))
    os.chdir(extract_path)
    db_tables = {}
    for path in glob.glob(os.path.join('db', '**', '*.tsv')):
        table = DBTable(path, read_data)
        db_tables[table.table_name] = table
    os.chdir(old_cwd)
    return db_tables


def read_loc_tables(extract_path, read_data=False):
    old_cwd = os.getcwd()
    # os.chdir(os.path.join(extract_path,'local_en.pack'))
    os.chdir(extract_path)
    subdir_path = os.path.join('text', 'db')
    db_tables = {}
    for path in glob.glob(os.path.join(subdir_path, '*.tsv')):
        table = DBTable(path, read_data)
        db_tables[table.table_name] = table
    os.chdir(old_cwd)
    return db_tables


def _read_meta_file(path):
    relpath = os.path.relpath(path, SETTINGS['assed_extract_path']).replace('\\', '/')
    ext = relpath.split('.')[-1]
    typee = 'None'
    if 'json' == ext:
        with open(path, 'r') as f:
            file_content = json.load(f)
        if 'header' in relpath:
            typee = 'anim.header'
            relpath = relpath.replace(f'.header.{ext}', '')
        elif 'anm.meta' in relpath:
            typee = 'anm.meta'
            relpath = relpath.replace(f'.{ext}', '')
        elif 'snd.meta' in relpath:
            typee = 'snd.meta'
            relpath = relpath.replace(f'.{ext}', '')
        elif 'meta' in relpath:
            typee = 'meta'
            relpath = relpath.replace(f'.{ext}', '')

    elif 'xml' == ext:
        typee = 'bin'
        with open(path, 'r') as f:
            file_content = f.read()
        relpath = relpath.replace(f'.{ext}', '')

    lookup = relpath
    return (typee, lookup, relpath, ext, file_content)

def read_meta_files():
    old_cwd = os.getcwd()
    os.chdir(SETTINGS['assed_extract_path'])
    meta_files = {'lookup': {}, 'bin': [], 'snd.meta': [], 'anm.meta': [], 'anim.header': [], 'meta': []}

    pool = mp.Pool(mp.cpu_count())
    pathes = glob.glob(os.path.join(SETTINGS['assed_extract_path'], '**', '*'), recursive=True)
    pathes = list(filter(lambda x: '.json' in x or '.xml' in x, pathes))
    results = pool.map(_read_meta_file, pathes)
    pool.close()
    os.chdir(old_cwd)
    for (typee, lookup, relpath, ext, file_content) in results:
        meta_files[typee].append(relpath)
        content = BeautifulSoup(file_content, 'lxml') if ext == 'xml' else file_content
        meta_files['lookup'][lookup] = {'type': ext, 'content': content}
    return meta_files