import tomli
import tomli_w
import os
from .checker import ensure_dir_exist


def load_conf(conf: str):
    with open(conf, "rb") as f:
        data = tomli.load(f)
    return data


def save_conf(data, conf: str):
    ensure_dir_exist(os.path.dirname(conf))
    with open(conf, "wb+") as f:
        tomli_w.dump(data, f)
    return True
