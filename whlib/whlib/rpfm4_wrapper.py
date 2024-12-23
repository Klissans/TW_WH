import os
import glob
import shutil
import subprocess
import multiprocessing as mp

from .settings import SETTINGS


class RPFM4Wrapper:

    def __init__(self,
                 rpfm_cli_path:str=SETTINGS['rpfm4_path'],
                 game_name:str=SETTINGS['twgame_name'],
                 game_path:str=SETTINGS['twgame_path'],
                 extract_path:str=SETTINGS['extract_path']
                 ):
        self.rpfm_cli_path = rpfm_cli_path
        self.game_name = game_name
        self.game_path = game_path
        self.extract_path = extract_path
        self.schema_path = os.path.join(SETTINGS['schema_path'], SETTINGS['schema_name'].replace('json', 'ron'))

        self.ex_data_pack_path = os.path.join(self.extract_path, 'data.pack')
        self.ex_local_en_pack_path = os.path.join(self.extract_path, 'local_en.pack')
        
        self._update_schema()
        self._dump_schema()
        pass

    def _execute_cmd(self, command: list, verbose=True, cwd=None):
        cli_args = [self.rpfm_cli_path, '-g', self.game_name]
        if verbose:
            cli_args.append('-v')
        cli_args.extend(command)
        if verbose:
            print(' '.join(cli_args))
        if cwd is not None:
            subprocess.run(cli_args, check=True, cwd=cwd)
        else:
            subprocess.run(cli_args, check=True)


    def _update_schema(self):
        try:
            cli_args = ['schemas', 'update', '--schema-path', SETTINGS['schema_path']]
            self._execute_cmd(cli_args, verbose=True)
        except subprocess.CalledProcessError as e:
            print(e)

    def _dump_schema(self):
        cli_args = ['schemas', 'to-json', '--schemas-path', SETTINGS['schema_path']]
        self._execute_cmd(cli_args, verbose=True)

    def extract_data(self):
        shutil.rmtree(self.extract_path, ignore_errors=True)
        pathes = glob.glob(f"{self.game_path}/data/*.pack")
        data_pathes = [x for x in pathes if ('db.pack' in x.split('\\')[-1] or 'data' in x.split('\\')[-1])]
        for pf in data_pathes:
            pack_name = f"{pf.split(os.sep)[-1]}"
            ex_data_pack_path = self.extract_path #os.path.join(self.extract_path, pack_name)
            os.makedirs(ex_data_pack_path, exist_ok=True)

            ex_data_pack_path_str = f"{';'.join(['db', ex_data_pack_path])}"
            cli_args = ['pack', 'extract', '-t', self.schema_path, '-p', pf,  '-F', ex_data_pack_path_str]
            self._execute_cmd(cli_args)

            ex_data_pack_path_str = f"{';'.join(['ui', ex_data_pack_path])}"
            cli_args = ['pack', 'extract', '-t', self.schema_path, '-p', pf,  '-F', ex_data_pack_path_str]
            self._execute_cmd(cli_args)

            ex_data_pack_path_str = f"{';'.join(['script', ex_data_pack_path])}"
            cli_args = ['pack', 'extract', '-t', self.schema_path, '-p', pf,  '-F', ex_data_pack_path_str]
            self._execute_cmd(cli_args)

        locals = ['local_en', 'local_en_3']
        for f in locals:
            # ex_local_en_pack_path = os.path.join(self.extract_path, f"{f}.pack")
            ex_local_en_pack_path = self.extract_path
            os.makedirs(ex_local_en_pack_path, exist_ok=True)
            pf = f"{self.game_path}/data/{f}.pack"
            ex_local_en_pack_path_str = f"{';'.join(['text', ex_local_en_pack_path])}"
            cli_args = ['pack', 'extract', '-t', self.schema_path, '-p', pf,  '-F', ex_local_en_pack_path_str]
            self._execute_cmd(cli_args)
        # self.extract_data_tables()
        # self.extract_loc_tables()

    def extract_file(self, pack_file,  path_in_pack, extract_folder):
        pf = f"{self.game_path}/data/{pack_file}.pack"
        cli_args = ['pack', 'extract', '-p', pf,  '-f', ','.join([path_in_pack, extract_folder])]
        self._execute_cmd(cli_args)

    def extract_data_tables(self):
        pool = mp.Pool(mp.cpu_count())
        cmd_list, paths = [], []
        for path in glob.glob(os.path.join(self.extract_path, 'data*', 'db', '*')):
            cli_args = ["table", "-e", os.path.join(path, 'data__')]
            cmd_list.append(cli_args)
            paths.append(os.path.join(path, 'data__'))
        pool.map(self._execute_cmd, cmd_list)
        pool.map(os.remove, paths)

    def extract_loc_tables(self):
        pool = mp.Pool(mp.cpu_count())
        cmd_list, paths = [], []
        for loc_path in glob.glob(os.path.join(self.extract_path, 'local*', 'text', 'db', '*.loc')):
            cli_args = ["table", "-e", loc_path]
            cmd_list.append(cli_args)
            paths.append(loc_path)
        pool.map(self._execute_cmd, cmd_list)
        pool.map(os.remove, paths)
        
    def rename_cco_files(self, content_path):
        for path in glob.glob(os.path.join(content_path, 'ui', 'cco', '*.js')):
            os.rename(path, path.replace('.js', '.cco'))
        pass

    def make_package(self, pack_name:str, content_path:str, additional_path=None):
        install_path = os.path.join(self.game_path, 'data', f'{pack_name}.pack')
        self.rename_cco_files(content_path)
        if additional_path is not None:
            shutil.copytree(additional_path, content_path, dirs_exist_ok=True)
        if os.path.exists(install_path):
            os.remove(install_path)
            print("Old mod deleted", install_path)
        cli_args = ['pack', 'create', '-p', install_path]
        self._execute_cmd(cli_args)

        db_path = os.path.join(content_path, "db")
        for root, dirs, files in os.walk(db_path, topdown=False):
            relroot = os.path.relpath(root, db_path)
            for name in files:
                tsv_name = os.path.join(relroot, name)
                cli_args = ['pack', 'add', '-p', install_path, '-f', ';'.join([tsv_name, 'db']), '-t', self.schema_path]
                self._execute_cmd(cli_args, verbose=True, cwd=db_path)
                os.remove(os.path.join(db_path, tsv_name))

        loc_path = os.path.join(content_path, "text")
        for root, dirs, files in os.walk(loc_path, topdown=False):
            relroot = os.path.relpath(root, loc_path)
            for name in files:
                tsv_name = os.path.join(relroot, name)
                cli_args = ['pack', 'add', '-p', install_path, '-f', ';'.join([tsv_name, 'db']), '-t', self.schema_path]
                self._execute_cmd(cli_args, verbose=True, cwd=loc_path)
                os.remove(os.path.join(loc_path, tsv_name))

        cli_args = ['pack', 'add', '-p', install_path, '-F', content_path]
        self._execute_cmd(cli_args, verbose=True)

        cli_args = [ 'pack', 'list', '-p', install_path]
        self._execute_cmd(cli_args)
        print(f"Mod package written to: {install_path}")