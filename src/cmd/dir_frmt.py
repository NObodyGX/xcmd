from .file_format_text import g_file_format_text


def g_dir_frmt(cdir: str):
    g_file_format_text(ifile=cdir, odir=cdir, merge_short=False)
