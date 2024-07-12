from .m4a_file import SimpleMp4File
import os


def check_mp4_header_format(filename: str):
    mf = SimpleMp4File(filename)
    msg = " ".join([x.type for x in mf.children])
    checked = mf.check_moov_is_header()
    print(f"[{checked}]{os.path.basename(filename)}: {msg}")
    return checked
