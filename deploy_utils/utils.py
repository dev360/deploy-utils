import os, re, shutil, sys


def system(cmd, verbose=False):
    """
    Like os.system, except quiter
    """
    fout, process, ferror = os.popen3(cmd)
    result = process.read()
    if verbose:
        sys.stdout.write(result)
    process.close()
    return result


