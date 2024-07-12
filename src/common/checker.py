import re
import os
import subprocess


def ensure_dir_exist(idir: str):
    if not os.path.exists(idir):
        os.makedirs(idir)
        return False
    return True


def check_chinese(words):
    pattern = re.compile(r"[^\u4e00-\u9fa5]")
    return not pattern.search(words)


def check_suffix(fname: str, isuffix: str, ignore_case=True):
    name = fname.lower() if ignore_case else fname
    if name.endswith(isuffix):
        return True
    return False


def check_suffixs(fname: str, isuffixs: str, ignore_case=True):
    if isinstance(isuffixs, str):
        raise RuntimeError("failed type")
    name = fname.lower() if ignore_case else fname
    for suffix in isuffixs:
        if name.endswith(suffix):
            return True
    return False


def check_conf(fname):
    return check_suffix(fname, ".toml")


def check_pic(fname):
    return check_suffixs(fname, [".jpg", ".jpeg", ".png", ".gif", ".webp", ".apng"])


def check_vip_pic(fname):
    if fname in ("_cover.jpg", "_avator.jpg", "avator.jpg"):
        return True
    return False


def check_vid(fname):
    return check_suffixs(
        fname, [".mp4", ".m4v", ".ts", ".avi", ".mkv", ".mov", ".rmvb"]
    )


def check_mp4(fname):
    return check_suffix(fname, ".mp4")


def check_vid_support_copy(fname):
    return check_suffixs(fname, [".avi", ".mkv", ".m4v"])


def check_vid_unsupport_copy(fname):
    return check_suffixs(fname, [".ts", ".rmvb", ".mov", ".rmvb"])


def check_vid_tran_ret(ifile: str, ofile: str):
    # 不存在输出文件
    if not os.path.exists(ofile):
        return False
    # 输出文件大小异常
    size1 = os.stat(ifile).st_size
    size2 = os.stat(ofile).st_size
    if size2 < 5 * 1024:  # 5k
        return False
    if size2 < size1 * 0.3 or size2 > size1 * 2:
        return False
    return True


def check_vid_cut_ret(ofile):
    # 不存在输出文件
    if not os.path.exists(ofile):
        return False
    # 输出文件大小异常
    osize = os.stat(ofile).st_size
    if osize < 5 * 1024:  # 5k
        return False
    return True


def check_vid_codec(ifile: str):
    # codec_name=h264
    support_codecs = ("h264", "h265", "hevc")
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1 {ifile}"
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    code = p.stdout.decode("utf-8")
    length = len("codec_name=")
    if len(code) <= length:
        return False
    codec = code[length:].strip()
    print(f"[codec]{os.path.basename(ifile)}: {codec}")
    if codec.lower() in support_codecs:
        return True
    return False
