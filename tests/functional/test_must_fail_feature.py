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

