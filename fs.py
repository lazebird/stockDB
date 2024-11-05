import json
import os
import pandas as pd

DataDir = os.path.join(".", "data/")


def write_data(d, rpath):
    apath = os.path.join(DataDir, rpath)
    if apath.find(DataDir) == -1:  # add check for path not in DataDir
        raise RuntimeError(f"path '{rpath}' must be in '{DataDir}'")
    dir = os.path.dirname(apath)
    os.makedirs(dir, exist_ok=True)
    with open(apath, "w", encoding="utf8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)


def load_data(rpath, defval={}):
    apath = os.path.join(DataDir, rpath)
    if apath.find(DataDir) == -1:  # add check for path not in DataDir
        raise RuntimeError(f"path '{rpath}' must be in '{DataDir}'")
    if os.path.isfile(apath):
        with open(apath, "r", encoding="utf8") as f:
            return json.load(f)
    return defval


def get_datadir(datestr):
    return os.path.join(DataDir, datestr)


def write_csv(d: list[dict], apath):
    dir = os.path.dirname(apath)
    os.makedirs(dir, exist_ok=True)
    with open(apath, "w", encoding="utf8") as f:
        print(", ".join(d[0].keys()), file=f)
        for e in d:
            print(", ".join(map(lambda x: str(x), e.values())), file=f)


def write_xlsx(d: list[dict], apath):
    dir = os.path.dirname(apath)
    os.makedirs(dir, exist_ok=True)
    pf = pd.DataFrame(d)
    pf.to_excel(apath, sheet_name="data", freeze_panes=[1, 0])
