import subprocess
import os
import shutil
from os.path import join, dirname, basename, exists, relpath, abspath
from common.checker import (
    check_mp4,
    check_vid_support_copy,
    check_vid_unsupport_copy,
    check_vid_tran_ret,
    check_vid_codec,
)
from extern.mp4analyser import check_mp4_header_format
from common.gen import gen_tfile, gen_nfile
from common.scan import scan_files


class GTranVidWorker(object):
    def __init__(self, idir: str, odir: str, d=True, r=False, m=False) -> None:
        self.idir = idir
        self.odir = odir
        self.vid1 = []
        self.vid2 = []
        self.vid3 = []
        self.confs = []
        self.works = []
        self.d_flag = d
        self.r_flag = r
        self.m_flag = m

    def start(self):
        self.title = "tran"
        self._scan()
        self._work()
        self._done()

    def _scan(self):
        files = scan_files(self.idir, recursion=self.r_flag)
        for ifile in files:
            if check_mp4(ifile):
                self.vid1.append(ifile)
                continue
            if check_vid_support_copy(ifile):
                self.vid2.append(ifile)
                continue
            if check_vid_unsupport_copy(ifile):
                self.vid3.append(ifile)
                continue

    def __do_real_tran(self, cmd: str, ifile: str, ofile: str, meta=True):
        cdir = dirname(ifile)
        tfile = gen_tfile(ifile, keep_name=True)
        if ifile != tfile:
            shutil.move(ifile, tfile)

        cmds = [
            "ffmpeg -hide_banner",
            f"-i {tfile}",
            "-movflags faststart" if meta else "",
            cmd,
            f"{relpath(ofile, cdir)}",
        ]
        print(" ".join(cmds))
        subprocess.run(" ".join(cmds), cwd=f"{cdir}")
        if not check_vid_tran_ret(tfile, ofile):
            print(f"[tran]{ifile} error")
            # 将 tfile 移动到 ovids 里
            ddir = join(cdir, ".ovids")
            if not exists(ddir):
                os.makedirs(ddir)
            shutil.move(tfile, join(ddir, basename(ifile)))
            return False
        if self.d_flag:
            os.remove(tfile)
            return True
        ddir = join(cdir, ".ovids")
        if not exists(ddir):
            os.makedirs(ddir)
        shutil.move(tfile, join(ddir, basename(ifile)))
        return True

    def __move_head_for_mp4(self, ifile: str, ofile: str, meta=True):
        cmd = "-c:v copy -c:a copy"
        return self.__do_real_tran(cmd, ifile, ofile, meta=meta)

    def __hevc_vslow_tran(self, ifile, ofile):
        cmds = [
            "-c:a copy -c:v hevc",
            "-x265-params min-keyint=5:scenecut=50:open-gop=0:rc-lookahead=40:lookahead-slices=0:subme=3:merange=57:ref=4:max-merge=3:no-strong-intra-smoothing=1:no-sao=1:selective-sao=0:deblock=-2,-2:ctu=32:rdoq-level=2:psy-rdoq=1.0:crf=18",
            "-preset medium",
        ]
        return self.__do_real_tran(" ".join(cmds), ifile, ofile)

    def __hevc_slow_tran(self, ifile, ofile):
        cmd = "-vcode hevc -preset slow"
        return self.__do_real_tran(cmd, ifile, ofile)

    def __do_vid1(self):
        for ifile in self.vid1:
            if check_mp4_header_format(ifile):
                continue
            self.__move_head_for_mp4(ifile, ifile)

    def __do_vid2(self):
        for ifile in self.vid2:
            ofile = gen_nfile(ifile, ".mp4")
            if check_vid_codec(ifile):
                self.__move_head_for_mp4(ifile, ofile, meta=False)
                continue
            if self.m_flag:
                self.__move_head_for_mp4(ifile, ofile)
                continue
            self.__hevc_vslow_tran(ifile, ofile)

    def __do_vid3(self):
        for ifile in self.vid3:
            ofile = gen_nfile(ifile, ".mp4")
            if self.m_flag:
                self.__hevc_slow_tran(ifile, ofile)
                continue
            self.__hevc_vslow_tran(ifile, ofile)

    def _work(self):
        self.__do_vid2()
        self.__do_vid3()
        self.__do_vid1()

    def _done(self):
        pass


def g_dir_format_video(idir="", deleted=False, r=False, easy_mode=False):
    worker = GTranVidWorker(idir, idir, d=deleted, r=r, m=easy_mode)
    worker.start()
