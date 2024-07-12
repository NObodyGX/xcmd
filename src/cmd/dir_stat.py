from os import scandir
from os.path import exists


def convert_bytes(num):
    if num <= 0:
        return "empty"
    if num < 1024:
        t = round(num / 1024, 2)
        return f"{t:3.1f}KB"
    for x in ["b ", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return f"{num:3.1f}{x}"
        num /= 1024.0
    return f"{num}"


def convert_gb(num):
    if num <= 0:
        return "empty"
    if num < 1024:
        return "0.01GB"
    return f"{num / 1024 / 1024 / 1024:3.2f}GB"


class GEntry(object):
    total = 0
    length = 0
    count = 0

    def __init__(self, kind="", name="", size=0):
        self.name = name
        self.size = size
        self.kind = kind

    def __str__(self):
        return f"{convert_bytes(self.size):>{GEntry.length}} : {self.kind} {self.name}"

    @staticmethod
    def format_total(dlist=None) -> str:
        if dlist:
            total = sum([d.size for d in dlist])
            return "\n".join(
                [
                    "========================",
                    f"total: {convert_bytes(total)}, length: {len(dlist)}",
                ]
            )
        return "\n".join(
            [
                "========================",
                f"total: {convert_bytes(GEntry.total)}, length: {GEntry.count}",
            ]
        )


def dirs_size(cdir: str) -> int:
    total_size = 0
    stack = [cdir]
    while stack:
        tdir = stack.pop()
        try:
            with scandir(tdir) as entries:
                for entry in entries:
                    if entry.is_file():
                        total_size += entry.stat().st_size
                    elif entry.is_dir():
                        stack.append(entry.path)
        except Exception as e:
            print(e)
            return 0
    return total_size


def g_dir_stat(cdir: str, mode=0) -> list:
    if not exists(cdir):
        return f"[error] path is missing: {cdir} "
    content = []
    total = 0
    for item in scandir(cdir):
        if item.is_dir():
            s = dirs_size(item.path)
            total += s
            d = GEntry("[D]", item.name, s)
            content.append(d)
        if item.is_file():
            s = item.stat().st_size
            total += s
            d = GEntry("[F]", item.name, s)
            content.append(d)
    # update total
    GEntry.total = total
    length = 5
    for e in content:
        if mode == 0:
            l = len(convert_gb(e.size).encode("utf-8"))
        else:
            l = len(convert_bytes(e.size).encode("utf-8"))
        length = l if l > length else length
    GEntry.length = length
    GEntry.count = len(content)

    return content


def g_cmd_dir_stat(cdir: str, mode=1) -> list:
    words = "========================\n"
    content = g_dir_stat(cdir, mode=mode)
    words += "\n".join([str(d) for d in content])
    words += "\n" + GEntry.format_total(content)
    print(words)
