import os.path
import shutil

import pandas as pd
from whlib.settings import SETTINGS
from whlib.rpfm_wrapper import RPFMWrapper
from whlib.handler import Handler
from whlib.handler_helper import HandlerHelper
from src.formatter import Formatter

from pprint import pprint
import yaml

import re

if __name__ == '__main__':
    pattern = "\[\[[^\[\]/]*\]\]|\{\{[^\{\}/]*\}\}"
    # pattern = "\[\[[^\[\]/]*\]\]"
    # print(re.search(pattern, "add [[sss:zzz]] [[aaa]]\\n")[0])
    # exit()

    rpfm = RPFMWrapper()
    handler = Handler()

    res = {}

    for loc_name, loc_table in handler.locs.items():
        df = loc_table.data
        matches = df['text'].str.findall(pattern)
        for match_array in matches:
            if type(match_array) is not list:
                continue
            for str_match in match_array:
                k = str_match
                w = None
                if ':' in str_match:
                    split = str_match.split(':')
                    k = split[0]
                    w = ':'.join(split[1:])
                key_set = res.setdefault(k, set())
                key_set.add(w)

    # print(res.keys())
    # pprint(res)
    for k, v in res.items():
        res[k] = list(v)
    with open('loc_keywords.yaml', 'w') as f:
        yaml.safe_dump(res, f)
    pass