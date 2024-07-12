from pdf2image import convert_from_path
from os import scandir, makedirs, remove
from os.path import join, basename, splitext, isdir, exists, dirname
from PIL import Image
import shutil


def extract_pdf_from_file(fullname: str, odir: str):
    bname, _ = splitext(basename(fullname))
    nname = bname
    if exists(join(odir, nname)):
        for i in range(1000):
            nname = f"{bname}{i:03d}"
            if not exists(join(odir, nname)):
                break
    ndir = join(odir, nname)
    ntdir = join(ndir, "tmp")
    if not exists(ntdir):
        makedirs(ntdir)
    # 虽然可以默认输出 png，但是速度相对于 ppm 太慢了，而且占用空间也大
    # 这里还是直接输出 ppm 再转 jpg 比较好
    convert_from_path(fullname, output_folder=ntdir)
    files = []
    for entry in scandir(ntdir):
        if not entry.is_file():
            continue
        if not entry.name.lower().endswith(".ppm"):
            continue
        files.append(entry.path)
    length = len(str(len(files)))
    for i, fpath in enumerate(sorted(files)):
        cnt = "{:0{}}".format(i, length)
        image = Image.open(fpath)
        image.save(join(ndir, f"{cnt}.jpg"))
    shutil.rmtree(ntdir)


def g_extract_pdf(ipath: str, odir: str = ""):
    if not isdir(ipath):
        if ipath.lower().endswith(".pdf"):
            extract_pdf_from_file(ipath, odir)
            return
        ipath = dirname(ipath)
    if not odir:
        odir = ipath
    for entry in scandir(ipath):
        if not entry.is_file():
            continue
        if not entry.name.lower().endswith(".pdf"):
            continue
        extract_pdf_from_file(entry.path, odir)


if __name__ == "__main__":
    idir = "C:\\CodeX\\GTools\\utils_toy\\toys"
    g_extract_pdf(idir, idir)
