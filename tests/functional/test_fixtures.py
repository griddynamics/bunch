from os.path import dirname, abspath, join
from nose.tools import assert_equals, assert_raises
from tests.asserts import assert_matches, assert_feature_matches
from tests.utils import run_bunch_cli
from fixtures_data import SIMPLE_DEPS_CONSOLE_OUTPUT_PATTERN, BASIC_REQS_CONSOLE_OUTPUT_PATTERN, BASICP_REQS_CONSOLE_OUTPUT_PATTERN


CURRENT_DIR = abspath(dirname(__file__))
BUNCHES = join(CURRENT_DIR, 'bunches')
RESULT_DIR = join(CURRENT_DIR, 'results', 'fixtures')

def fixtures_routine(bunch_name, pattern, bunch_params=None):
    bunch_dir = join(BUNCHES, bunch_name)
    bunch_params = "" if bunch_params is None else bunch_params
    cmdline = "bunch {bunch_params} {bunch} {result}".format(
        bunch=bunch_dir,
        result=RESULT_DIR,
        bunch_params=bunch_params)

    code, out, err = run_bunch_cli(cmdline)
    assert_equals(code, 0, "Return code nonzero")
    assert_equals(err, "", "stderr is not empty: \n%s" % err)
    with open(join(RESULT_DIR, bunch_name+"_console.log"), 'w') as f:
        f.write(out)
    assert_feature_matches(out, pattern)


def test_simple_deps():
    fixtures_routine('simple_deps', SIMPLE_DEPS_CONSOLE_OUTPUT_PATTERN)

def test_osc_basic_deps():
    fixtures_routine('osc_requires_basic', BASIC_REQS_CONSOLE_OUTPUT_PATTERN, '-e clean')

def test_osc_basic_proper_deps():
    fixtures_routine('osc_requires_basic_proper', BASICP_REQS_CONSOLE_OUTPUT_PATTERN, '-e clean')
