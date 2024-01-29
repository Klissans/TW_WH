import os
import glob
import shutil
import subprocess
import multiprocessing as mp

from .settings import SETTINGS


class RPFMWrapper:

    def __init__(self,
                 rpfm_cli_path:str=SETTINGS['rpfm_path'],
                 game_name:str=SETTINGS['twgame_name'],
                 game_path:str=SETTINGS['twgame_path'],
                 extract_path:str=SETTINGS['extract_path']
                 ):
        self.rpfm_cli_path = rpfm_cli_path
        self.game_name = game_name
        self.game_path = game_path
        self.extract_path = extract_path

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
            print(cli_args)
        if cwd is not None:
            subprocess.run(cli_args, check=True, cwd=cwd)
        else:
            subprocess.run(cli_args, check=True)


    def _update_schema(self):
        try:
            cli_args = ['schema', '-u']
            self._execute_cmd(cli_args, verbose=True)
        except subprocess.CalledProcessError as e:
            print(e)

    def _dump_schema(self):
        cli_args = ['schema', '-j']
        self._execute_cmd(cli_args, verbose=True)

    def extract_data(self):
        shutil.rmtree(self.extract_path, ignore_errors=True)
        for f in glob.glob(f"{self.game_path}/data/data*.pack"):
            pack_name = f.split(os.sep)[-1]
            ex_data_pack_path = os.path.join(self.extract_path, pack_name)
            os.makedirs(ex_data_pack_path, exist_ok=True)
            cli_args = ['-p', f, "packfile", "-E", ex_data_pack_path, "dummy", "db"]
            self._execute_cmd(cli_args)
        locals = ['local_en', 'local_en_3']
        for f in locals:
            ex_local_en_pack_path = os.path.join(self.extract_path, f"{f}.pack")
            os.makedirs(ex_local_en_pack_path, exist_ok=True)
            cli_args = ['-p', f"{self.game_path}/data/{f}.pack", "packfile", "-E", ex_local_en_pack_path, "dummy", "text"]
            self._execute_cmd(cli_args)
        self.extract_data_tables()
        self.extract_loc_tables()

    def extract_data_tables(self):
        pool = mp.Pool(mp.cpu_count()) #
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
        pool.close()

    def make_package(self, pack_name:str, content_path:str, additional_path=None):
        install_path = os.path.join(self.game_path, 'data', f'{pack_name}.pack')
        if additional_path is not None:
            shutil.copytree(additional_path, content_path, dirs_exist_ok=True)
        if os.path.exists(install_path):
            os.remove(install_path)
        cli_args = ['-p', install_path, 'packfile', '-n']
        self._execute_cmd(cli_args)

        pool = mp.Pool(mp.cpu_count())

        install_cmds, append_cmds = [], []
        db_path = os.path.join(content_path, "db")
        for root, dirs, files in os.walk(db_path, topdown=False):
            relroot = os.path.relpath(root, db_path)
            for name in files:
                cli_args = ["-p", install_path, "table", "-i", os.path.join(relroot, name)]
                install_cmds.append(cli_args)
                cli_args = ["-p", install_path, "packfile", "-a", "db", os.path.join(relroot, name[:-4])]
                append_cmds.append(cli_args)
        exec_cmd = lambda cmd: self._execute_cmd(cmd, verbose=True, cwd=db_path)
        pool.map(exec_cmd, install_cmds)
        pool.map(exec_cmd, append_cmds)

        install_cmds, append_cmds = [], []
        loc_path = os.path.join(content_path, "text")
        for root, dirs, files in os.walk(loc_path, topdown=False):
            relroot = os.path.relpath(root, loc_path)
            for name in files:
                cli_args = ["-p", install_path, "table", "-i", os.path.join(relroot, name)]
                install_cmds.append(cli_args)
                cli_args = ["-p", install_path, "packfile", "-a", "text", os.path.join(relroot, name[:-4])]
                append_cmds.append(cli_args)
        exec_cmd = lambda cmd: self._execute_cmd(cmd, verbose=True, cwd=loc_path)
        pool.map(exec_cmd, install_cmds)
        pool.map(exec_cmd, append_cmds)

        pool.close()


        # for root, dirs, files in os.walk(output_path + "/ui", topdown=False):
        #     relroot = os.path.relpath(root, output_path + "/ui")
        #     for name in files:
        #         subprocess.run([rpfmcli_path, "-v", "-g", twgame, "-p", install_path, "packfile", "-a", "ui",
        #                         relroot.replace("\\", "/") + "/" + name], cwd=output_path + "/ui", check=True)

        cli_args = ['-p', install_path, 'packfile', '-l']
        self._execute_cmd(cli_args)
        print(f"Mod package written to: {install_path}")