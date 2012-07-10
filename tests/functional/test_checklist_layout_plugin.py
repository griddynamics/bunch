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
from nose.tools import assert_equals, assert_not_equals, assert_true, assert_false
from tests.utils import run_bunch_cli
import yaml


CURRENT_DIR = abspath(dirname(__file__))
BUNCHES = join(CURRENT_DIR, 'bunches')
RESULT_DIR = join(CURRENT_DIR, 'results', 'checklist_layout')
HTML_OUTPUT_DIR = join(RESULT_DIR, 'report')
PLUGIN_PARAMS = '--output-plugin="checklist_layout" --plugin-params="dst_dir={dst}"'.format(dst=HTML_OUTPUT_DIR)
RESULT_DUMP = join(HTML_OUTPUT_DIR, 'last_result_dump.yaml')

def load_last_result_data():
    with open(RESULT_DUMP, 'r') as f:
        return yaml.load(f)


def checklist_plugin_routine(bunch_name, verification_fcn, bunch_params=None):
    if not isinstance(bunch_name, basestring):
        bunch_dir = " ".join(map(lambda b: join(BUNCHES, b),bunch_name))
    else:
        bunch_dir = join(BUNCHES, bunch_name)
    bunch_params = "" if bunch_params is None else bunch_params
    cmdline = "bunch {bunch_params} {bunch} {result}".format(
        bunch=bunch_dir,
        result=RESULT_DIR,
        bunch_params="{xtra} {plugin}".format(xtra=bunch_params, plugin=PLUGIN_PARAMS))

    code, out, err = run_bunch_cli(cmdline)
    bunch_deployment = join(RESULT_DIR, "".join(bunch_name))
    with open(bunch_deployment + "_console.log", 'w') as f:
        f.write(out)
    verification_fcn(code, out, err, bunch_deployment, load_last_result_data())

def dummy_verification(code, out, err, bunch_results, plugin_output_dump):
    assert_true(True)

def test_all_must_fail_and_fails():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            0, "Some failed")
        assert_equals(code, 0, "Non zero return code")

    checklist_plugin_routine("all_must_fail_and_fails", verify)


def test_all_must_fail_but_passed():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            1, "Num failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            1, "Num failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            1, "Num failed")
        assert_equals(code, 2, "Return code")
    checklist_plugin_routine("all_must_fail_but_passed", verify)

def test_step_must_fail_and_fails():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            0, "Some failed")
        assert_equals(code, 0, "Non zero return code")
    checklist_plugin_routine("step_must_fail_and_fails", verify)

def test_step_must_fail_but_passed():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            1, "Num failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            1, "Num failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            1, "Num failed")
        assert_equals(code, 2, "Return code")
    checklist_plugin_routine("step_must_fail_but_passed", verify)

def test_scenario_must_fail_and_fails():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            0, "Some failed")
        assert_equals(code, 0, "Non zero return code")
    checklist_plugin_routine("scenario_must_fail_and_fails", verify)

def test_scenario_must_fail_but_passed():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            1, "Num failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Num failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            1, "Num failed")
        assert_equals(code, 2, "Return code")
    checklist_plugin_routine("scenario_must_fail_but_passed", verify)

"""
def test_random_fail():
    checklist_plugin_routine("light_failed", dummy_verification)

def test_basic_no_mf():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            0, "Some failed")
        assert_equals(code, 0, "Non zero return code")

    checklist_plugin_routine("basic", verify)

def test_light_story_must_fail():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            0, "Some failed")
        assert_equals(code, 0, "Non zero return code")
    checklist_plugin_routine("light_story_mustfail", verify)

def test_light_story_must_fail():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            0, "Some failed")
        assert_equals(code, 0, "Non zero return code")
    checklist_plugin_routine("light_setup_mustfail", verify)

def test_light_story_must_fail():
    def verify(code, out, err, bunch_results, results):
        assert_equals(
            results['summary']['total']['features']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['steps']['failed'],
            0, "Some failed")
        assert_equals(
            results['summary']['total']['scenarios']['failed'],
            0, "Some failed")
        assert_equals(code, 0, "Non zero return code")
    checklist_plugin_routine("light_teardown_mustfail", verify)
"""