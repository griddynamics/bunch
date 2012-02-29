import sys
import os
import shlex
from bunch.cli import main
import tempfile
import re

def cmdline2argv(cmdline):
    return shlex.split(cmdline, posix=(os.name != 'nt'))

def dump_fo(fo):
    fo.seek(0)
    return fo.read()


def run_cli(func, cmdline=''):
    saveargv, sys.argv = sys.argv, cmdline2argv(cmdline)
    with tempfile.TemporaryFile() as tmp_out:
        with tempfile.TemporaryFile() as tmp_err:
            savestdout, sys.stdout = sys.stdout, tmp_out
            savestderr, sys.stderr = sys.stderr, tmp_err
            try:
                func()
            except SystemExit as e:
                retcode = e.code
            else:
                retcode = 0
            finally:
                stdout, stderr = dump_fo(sys.stdout), dump_fo(sys.stderr)
                #return saved values
                sys.argv, sys.stdout, sys.stderr = saveargv, savestdout, savestderr

    return retcode, stdout, stderr


def run_bunch_cli(cmdline):
    return run_cli(main, cmdline)


def regex_exact_match(regex, text):
    match = re.compile(regex).match(text)
    return match is not None




