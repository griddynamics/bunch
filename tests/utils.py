# -*- coding: utf-8 -*-
# <Bunch - BDD test tool for Lettuce scenarios>
# Copyright (c) 2012 Grid Dynamics Consulting Services, Inc, All Rights Reserved
# http://www.griddynamics.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import sys
import os
import shlex
from lettuce_bunch.cli import main
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




