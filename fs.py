import json
import os

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
