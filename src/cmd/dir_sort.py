from os import scandir, rename
from os.path import exists, join, basename, splitext

from random import choices
from alive_progress import alive_it, alive_bar
from common.checker import (
    check_suffix,
    check_chinese,
    check_vip_pic,
    check_pic,
    check_vid,
)
from common.gen import gen_tfile
from common.scan import scan_dir, scan_file


class Sdir(object):
    dot1 = "-"
    dot2 = "™️"
    dot3 = "#TM#"

    def __init__(self, index, bname, extra, total) -> None:
        self.index = index
        self.bname = bname
        self.extra = extra
        self.total = total

    def nname(self, index):
        return f"{index:04d}{Sdir.dot1}{self.bname}{Sdir.dot2}{self.extra}"

    def __repr__(self) -> str:
        return f"{self.index}{self.dot1}{self.bname}{self.dot2}{self.extra}"


def _sort_special_dir(cdir, preview=False):
    in_dirs = []  # type: list[Sdir]
    un_dirs = []  # type: list[str]
    total_dirs = scan_dir(cdir)
    for idir in total_dirs:
        dname = basename(idir)
        if not dname.count(Sdir.dot1) > 0:
            un_dirs.append(idir)
            continue
        if not (dname.count(Sdir.dot2) > 0 or dname.count(Sdir.dot3)):
            un_dirs.append(idir)
            continue
        sp = Sdir.dot2 if dname.count(Sdir.dot2) > 0 else Sdir.dot3
        index = int(dname[: dname.find(Sdir.dot1)])
        bname = dname[dname.find(Sdir.dot1) + 1 : dname.find(sp)]
        extra = dname[dname.find(sp) + 2 :].replace(Sdir.dot2, "").strip()
        in_dirs.append(Sdir(index, bname, extra, dname))
    in_dirs.sort(key=lambda x: x.index)
    index = 0
    cn = -1
    on = -2
    for item in alive_it(in_dirs):
        cn = item.index // 1000
        if cn == on:
            index += 1
        else:
            index = 0
        on = cn
        nname = item.nname(cn * 1000 + index)
        if item.total != nname and not exists(nname):
            _do_rename(join(cdir, item.total), join(cdir, nname))
    print(f"undeal dir: {un_dirs}")


def _scan_dir(cdir: str, mode="", skip_chinese=False):
    files = scan_file(cdir, mode=mode)
    pic = {}
    vid = {}
    for ifile in files:
        bname = basename(ifile)
        if skip_chinese and check_chinese(bname):
            continue
        if check_vip_pic(bname):
            continue
        if check_pic(bname):
            _, ext = splitext(bname)
            ext = ext.lower()
            if ext not in pic:
                pic[ext] = []
            pic[ext].append(ifile)
        if check_vid(bname):
            _, ext = splitext(bname)
            if ext not in vid:
                vid[ext] = []
            vid[ext].append(ifile)
    return pic, vid


def _born_works(cdir: str, items: dict, name: str, start: int, symbol="_", gap=1):
    index = start
    count = max(99, sum([len(v) for v in items.values()]))
    length = len(str(count))
    oname = f"{name}{symbol}" if name.count("#1") <= 0 else name.replace("#1", {symbol})
    works = []
    for k, v in items.items():
        for ifile in v:
            k = ".jpg" if k == ".jpeg" else k
            cnt = "{:0{}}".format(index, length)
            nname = f"{oname}{cnt}{k}"
            ofile = join(cdir, nname)
            works.append((ifile, ofile))
            index += gap
    return works


def _do_rename(oname, nname, preview=False):
    if preview:
        msg = f"{basename(oname)} >>> {basename(nname)}"
        print(msg)
        return
    rename(oname, nname)


def _done_works(works, title="", preview=False):
    if not len(works):
        return
    if preview:
        for item in works:
            ifile, ofile = item
            _do_rename(ifile, ofile, preview=True)
        return
    with alive_bar(len(works), title=title) as bar:
        later = []
        # 重命名普通文件
        for item in works:
            ifile, ofile = item
            if exists(ofile):
                tfile = gen_tfile(ifile)
                later.append((ifile, ofile, tfile))
                continue
            _do_rename(ifile, ofile)
            bar()
        # 重命名冲突文件
        for item in later:
            ifile, ofile, tfile = item
            _do_rename(ifile, tfile)
        for item in later:
            ifile, ofile, tfile = item
            _do_rename(tfile, ofile)
            bar()


def g_dir_sort(
    cdir: str,
    name="",
    start=1,
    mode="",
    gap=1,
    preview=False,
    skip_ch=False,
):

    pic, vid = _scan_dir(cdir, mode, skip_chinese=skip_ch)
    if sum([len(v) for v in pic.values()] + [len(v) for v in vid.values()]) == 0:
        _sort_special_dir(cdir, preview=preview)
        return
    # pics
    pic_works = _born_works(cdir, pic, name, start, symbol="_", gap=gap)
    _done_works(pic_works, title="image", preview=preview)
    # vids
    vid_works = _born_works(cdir, vid, name, start, symbol="#", gap=gap)
    _done_works(vid_works, title="video", preview=preview)


def _show_dir_files(cdir: str, count=0):
    flist = []
    for e in scandir(cdir):
        if not e.is_file():
            continue
        flist.append(e.name)
    if count != 0:
        for x in choices(flist, k=count):
            print(x)
        return
    for x in flist:
        print(x)


def g_ask_dir_sort(cdir: str, start=1, mode="", skip_chinese=False):
    sk = skip_chinese
    for e in scandir(cdir):
        if not e.is_dir():
            print(f"[skip] file: {e.name}")
            continue
        print(">>>>>>>>>>>>>>>>>>>>>>>>>")
        tdir = join(cdir, e.name)
        _show_dir_files(tdir, count=3)
        print(f"[check] start: {e.name}")
        name = input("enter a name to rename, null to skip:\n")
        if name.strip() == "":
            print("========================")
            continue
        if name.strip() in ("q", "quit", "exit"):
            print("exit.")
            print("========================")
            return
        g_dir_sort(join(cdir, e.name), name, start=start, mode=mode, skip_ch=sk)
        _show_dir_files(tdir)
        print("========================")
