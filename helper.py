import os
from typing import List,Tuple,Dict
from json import load
from uncertainties import ufloat_fromstr


f_max = "$f_\\mathrm{max}$ "
delta_nu = "Delta nu"

full_background = "Full Background result"

class cd:
    """
    Directory changer. can change the directory using the 'with' keyword, and returns to the previous path
    after leaving intendation. Example:

    with cd("some/path/to/go"): # changing dir
        foo()
        ...
        bar()
    #back to old dir
    """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def load_results(path : str,ignore_list : List[str] = None,ignore_ignore = False,all = False) -> List[Tuple[str,Dict,Dict]]:
    """
    Loads result files and conf files for a given path
    :param path: input path
    :return: List containing this values
    """
    res_list = []
    cnt = 0
    for path,sub_path,files in  os.walk(path):
        if ('results.json' not in files and not all) or 'conf.json' not in files:
            continue

        cnt +=1

        if "ignore.txt" in files and not ignore_ignore and not all:
            continue

        try:
            if len([i for i in ignore_list if i in files]) != 0 and not all:
                continue
        except:
            pass

            try:
                with open(f"{path}/results.json") as f:
                    result = load(f)
            except:
                result = None

            try:
                with open(f"{path}/conf.json") as f:
                    conf = load(f)
            except:
                conf = None

        res_list.append((path,result,conf))

    print(f"Total: {cnt}")
    return res_list


def get_val(dictionary: dict, key: str, default_value=None):
    if key in dictionary.keys():
        try:
            return ufloat_fromstr(dictionary[key])
        except (ValueError, AttributeError) as e:
            return dictionary[key]
    else:
        return default_value