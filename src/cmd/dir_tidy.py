from common.scan import scan_files
from common.checker import check_suffix

import os
from os.path import basename
from alive_progress import alive_it


def g_cmd_dir_tidy(idir: str, r=True) -> list:
    files = scan_files(idir, recursion=r)
    laster = []
    for ifile in files:
        if check_suffix(ifile, ".html"):
            laster.append(ifile)
        if check_suffix(ifile, ".url"):
            laster.append(ifile)
        if check_suffix(ifile, ".txt"):
            if basename(ifile).lower() == "防迷路网址.txt":
                laster.append(ifile)
    for x in alive_it(laster):
        os.remove(x)
