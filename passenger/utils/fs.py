import os


def mkdirp(target):
    os.makedirs(target, exists_ok=True)


def dirname(target):
    return os.path.dirname(target)
