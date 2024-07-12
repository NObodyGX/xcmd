from os.path import exists, join, basename, splitext
import shutil

from alive_progress import alive_bar
from common.checker import check_conf, check_pic
from common.gen import gen_tfile
from common.conf import save_conf, load_conf
from common.scan import scan_files


class GMergWorker(object):
    def __init__(self, idir="", odir="") -> None:
        self.idir = idir
        self.odir = odir
        self.files = []
        self.confs = []
        self.works = []

    def start(self):
        self.title = "merge"
        self._scan()
        self._work()
        self._done()

    def _scan(self):
        files = scan_files(self.idir, recursion=True)
        for ifile in files:
            if check_pic(ifile):
                self.files.append(ifile)
                continue
            if check_conf(ifile):
                self.confs.append(ifile)
                continue
            print(f"{ifile} is not in workround")

    def __load_conf(self, ifile: str):
        try:
            content = load_conf(ifile)
            vid = content.get("video", [])
            if len(vid) != 0:
                return vid
        except Exception as e:
            print(e)
        return []

    def __do_conf(self):
        vids = []
        for conf in self.confs:
            v = self.__load_conf(conf)
            for x in v:
                if x in vids:
                    continue
                vids.append(x)
        if len(vids) == 0:
            return
        content = {
            "title": "merge by gx",
            "image_count": 0,
            "video_count": len(vids),
            "image": [],
            "video": vids,
            "url": "",
        }
        save_conf(join(self.odir, "meta.toml"), content)

    def __do_work(self):
        length = len(str(len(self.files)))
        for i, ifile in enumerate(self.files):
            cnt = "{:0{}}".format(i + 1, length)
            bname, ext = splitext(basename(ifile))
            nname = f"img_{cnt}{ext}"
            ofile = join(self.odir, nname)
            self.works.append((ifile, ofile))

    def _work(self):
        self.__do_conf()
        self.__do_work()

    def _done(self):
        if not len(self.works):
            return
        with alive_bar(len(self.works), title=self.title) as bar:
            later = []
            for item in self.works:
                ifile, ofile = item
                if exists(ofile):
                    tfile = gen_tfile(ifile)
                    later.append(ifile, ofile, tfile)
                    continue
                shutil.move(ifile, ofile)
                bar()
            for item in later:
                ifile, ofile, tfile = item
                shutil.move(ifile, tfile)
            for item in later:
                ifile, ofile, tfile = item
                shutil.move(tfile, ofile)
                bar()


def g_dir_merg(idir, odir=""):
    if not odir:
        odir = idir
    worker = GMergWorker(idir, odir)
    worker.start()
