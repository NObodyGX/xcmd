import os
from os.path import abspath
from natsort import natsorted


def scan_file(idir: str, mode="name"):
    ret = []
    with os.scandir(idir) as ee:
        if mode == "origin":
            entries = ee
        if mode == "name":
            entries = natsorted(ee, key=lambda e: e.name)
        if mode == "name_r":
            entries = natsorted(ee, key=lambda e: e.name, reverse=True)
        if mode == "size":
            entries = sorted(ee, key=lambda e: e.stat().st_size)
        if mode == "size_r":
            entries = sorted(ee, key=lambda e: e.stat().st_size, reverse=True)
        for e in entries:
            if not e.is_file():
                continue
            ret.append(abspath(e.path))
    return ret


def scan_files(idir: str, recursion=False) -> list[str]:
    stack = []
    stack.append(idir)
    ret = []
    while stack:
        tdir = stack.pop(0)
        for entry in os.scandir(tdir):
            if entry.is_dir():
                if recursion:
                    stack.append(entry.path)
                continue
            if not entry.is_file():
                continue
            ret.append(abspath(entry.path))
    return ret


def scan_dir(idir: str, recursion=True) -> list[str]:
    stack = [idir]
    ret = []
    while stack:
        tdir = stack.pop(0)
        for entry in os.scandir(tdir):
            if not entry.is_dir():
                continue
            if recursion:
                stack.append(stack)
            ret.append(abspath(entry.path))
    return ret
