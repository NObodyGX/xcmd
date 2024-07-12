from xcmd.dir_tran_video import g_dir_format_video


def g_cmd_dir_tran(idir: str, deleted=False, r=False, easy_mode=False) -> list:
    g_dir_format_video(idir, deleted, r, easy_mode=easy_mode)
