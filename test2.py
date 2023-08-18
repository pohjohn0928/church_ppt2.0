import os


def get_file_by_pattern(root_dir, pattern):
    fs = []
    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            _, ending = os.path.splitext(name)
            if ending == f".{pattern}":
                # fs.append(os.path.join(root, name))
                fs.append(name)
    return fs
