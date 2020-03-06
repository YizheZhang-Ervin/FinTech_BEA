import sys


def daemon():
    import os
    try:
        pid = os.fork()
        if pid > 0:
            return pid
    except OSError as error:
        return -1
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            return pid
    except OSError as error:
        return -1
    sys.stdout.flush()
    sys.stderr.flush()
    si = open("/dev/null", "r")
    so = open("/dev/null", "ab")
    se = open("/dev/null", "ab", 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdin.fileno())
    os.dup2(se.fileno(), sys.stdin.fileno())
    return 0
