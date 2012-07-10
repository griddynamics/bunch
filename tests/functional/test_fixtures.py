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


from os.path import dirname, abspath, join
from nose.tools import assert_equals, assert_raises
from tests.asserts import assert_matches, assert_feature_matches
from tests.utils import run_bunch_cli
from fixtures_data import SIMPLE_DEPS_CONSOLE_OUTPUT_PATTERN, BASIC_REQS_CONSOLE_OUTPUT_PATTERN, BASICP_REQS_CONSOLE_OUTPUT_PATTERN, LIGHT_REQS_CONSOLE_OUTPUT_PATTERN


CURRENT_DIR = abspath(dirname(__file__))
BUNCHES = join(CURRENT_DIR, 'bunches')
RESULT_DIR = join(CURRENT_DIR, 'results', 'fixtures')

def fixtures_routine(bunch_name, pattern, bunch_params=None):
    if not isinstance(bunch_name, basestring):
        bunch_dir = " ".join(map(lambda b: join(BUNCHES, b),bunch_name))
    else:
        bunch_dir = join(BUNCHES, bunch_name)
    bunch_params = "" if bunch_params is None else bunch_params
    cmdline = "bunch {bunch_params} {bunch} {result}".format(
        bunch=bunch_dir,
        result=RESULT_DIR,
        bunch_params=bunch_params)

    code, out, err = run_bunch_cli(cmdline)
    assert_equals(code, 0, "Return code nonzero")
    assert_equals(err, "", "stderr is not empty: \n%s" % err)
    with open(join(RESULT_DIR, "".join(bunch_name)+"_console.log"), 'w') as f:
        f.write(out)
    assert_feature_matches(out, pattern)


def test_simple_deps():
    fixtures_routine('simple_deps', SIMPLE_DEPS_CONSOLE_OUTPUT_PATTERN)

def test_osc_basic_deps():
    fixtures_routine('osc_requires_basic', BASIC_REQS_CONSOLE_OUTPUT_PATTERN, '-e clean')

def test_osc_basic_proper_deps():
    fixtures_routine('osc_requires_basic_proper', BASICP_REQS_CONSOLE_OUTPUT_PATTERN, '-e clean')

def test_osc_light():
    fixtures_routine(['basic', 'keystone', 'light'], LIGHT_REQS_CONSOLE_OUTPUT_PATTERN, '-e clean')

