from os import makedirs, rename
from os.path import exists, join, dirname, normpath, abspath, isabs
import shutil
from alive_progress import alive_bar, alive_it

dirs_includes_data = []


def g_dir_gen(cdir: str):
    if exists(join(cdir, "💢💢💢")):
        return
    for x in alive_it(dirs_includes_data):
        dname = join(cdir, x)
        if not exists(dname):
            makedirs(dname)


def _regular_name(name: str):
    fdit = {"#0": "™️", "#1": "❤️", "#2": "❣️", "#3": "♨️", "#4": "✈️"}
    for k, v in fdit.items():
        name = name.replace(k, v)
    return name


def g_dir_make(cdir: str, name: str):
    if not isabs(cdir):
        cdir = f"./{cdir}"
    cdir = normpath(abspath(cdir))
    name = _regular_name(name)
    path = join(cdir, name)
    if not exists(path):
        makedirs(name)
    with alive_bar(1, title="make") as bar:
        bar()


def g_dir_move(idir: str, name: str):
    if not exists(idir):
        print(f"[error] {idir} is not exists.")

    def format_dir(mdir: str):
        if not isabs(mdir):
            mdir = f"./{mdir}"
        return normpath(abspath(mdir))

    idir = format_dir(idir)
    mdir = dirname(idir)
    name = _regular_name(name)
    path = join(mdir, name)
    if exists(idir) and not exists(path):
        shutil.move(idir, path)
    with alive_bar(1, title="move") as bar:
        bar()
