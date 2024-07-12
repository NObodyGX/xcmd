import shutil
from os.path import exists, basename, splitext
from common.gen import gen_nfile


def g_file_add_suffix(
    ifile: str, suffix: str = "rar", extra_suffix=("7z", "zip", "rar", "tar")
):
    if not exists(ifile):
        return False
    if not suffix:
        return False
    suffix = suffix.lstrip(".")

    _, ext = splitext(basename(ifile))
    nfile = gen_nfile(ifile, suffix)
    for x in extra_suffix:
        if ext.find(x) > -1:
            nfile = gen_nfile(ifile, x)
            break
    shutil.move(ifile, nfile)
    return True
