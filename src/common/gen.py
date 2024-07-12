from os.path import splitext, basename, dirname, join, exists
import time
from hashlib import md5


def gen_tfile(ifile, keep_name=False):
    tdir = dirname(ifile)
    if keep_name:
        bname = basename(ifile)
        if bname.startswith("__"):
            return ifile
        return join(tdir, f"__{bname}")

    tname = md5(ifile.encode("utf-8")).hexdigest()
    tfile = join(tdir, tname + ".tmp")
    if not exists(tfile):
        return tfile
    return join(tdir, str(int(time.time())) + ".tmp")


def gen_nfile(ifile: str, suffix: str = ""):
    bname, ext = splitext(basename(ifile))
    if bname.startswith("__"):
        bname = bname.lstrip("_")
    if not suffix:
        suffix = ext
    if not suffix.startswith("."):
        suffix = f".{suffix}"
    cdir = dirname(ifile)
    nfile = join(cdir, bname + suffix)
    if not exists(nfile):
        return nfile

    for i in range(10000):
        nfile = join(cdir, bname + f"{i+1:03d}{suffix}")
        if not exists(nfile):
            return nfile
    return join(cdir, f"{int(time.time())}{suffix}")
