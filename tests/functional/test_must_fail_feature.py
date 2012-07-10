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
from nose.tools import assert_equals, assert_not_equals
from tests.utils import run_bunch_cli


CURRENT_DIR = abspath(dirname(__file__))
BUNCHES = join(CURRENT_DIR, 'bunches')
RESULT_DIR = join(CURRENT_DIR, 'results', 'must_fail')


def must_fail_routine(bunch_name, verification_fcn, bunch_params=None):
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
    bunch_deployment = join(RESULT_DIR, "".join(bunch_name))
    with open(bunch_deployment + "_console.log", 'w') as f:
        f.write(out)
    verification_fcn(code, out, err, bunch_deployment)

def positive_verification(code, out, err, bunch_results):
    assert_equals(code, 0, "Return code nonzero")
    assert_equals(err, "", "stderr is not empty: \n%s" % err)

def negative_verification(code, out, err, bunch_results):
    assert_equals(code, 2, "Return code is not 2")
    assert_equals(err, "", "stderr is not empty: \n%s" % err)

def test_step_must_fail_and_fails():
    must_fail_routine("step_must_fail_and_fails", positive_verification)

def test_step_must_fail_but_passed():
    must_fail_routine("step_must_fail_but_passed", negative_verification)

def test_scenario_must_fail_and_fails():
    must_fail_routine("scenario_must_fail_and_fails", positive_verification)

def test_scenario_must_fail_but_passed():
    must_fail_routine("scenario_must_fail_but_passed", negative_verification)

def test_feature_must_fail_and_fails():
    must_fail_routine("feature_must_fail_and_fails", positive_verification)

def test_feature_must_fail_but_passed():
    must_fail_routine("feature_must_fail_but_passed", negative_verification)

def test_all_must_fail_and_fails():
    must_fail_routine("all_must_fail_and_fails", positive_verification)

def test_all_must_fail_but_passed():
    must_fail_routine("all_must_fail_but_passed", negative_verification)

def test_light_story_mustfail():
    must_fail_routine("light_story_mustfail", positive_verification, '-e clean')

def test_light_setup_mustfail():
    must_fail_routine("light_setup_mustfail", positive_verification, '-e clean')

def test_light_teardown_mustfail():
    must_fail_routine("light_teardown_mustfail", positive_verification, '-e clean')

def test_step_just_fails():
    must_fail_routine("step_just_fails", negative_verification)

