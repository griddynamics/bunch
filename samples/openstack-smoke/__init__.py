from lettuce import step, world
from nose.tools import assert_equals, assert_true
import utils



@step(u'current user can execute sudo without password')
def check_current_user_sudo_nopwd(step):
    assert_true(utils.check_can_execute_sudo_without_pwd())


@step(u'every RPM package available:')
def check_rpm_available(step):
    for data in step.hashes:
        assert_true(utils.rpm_available(data['PackageName']))


@step(u'I install RPM package\(s\):')
def install_rpm(step):
    utils.rpm_clean_all_cached_data()
    for data in step.hashes:
        assert_true(utils.rpm_install(data['PackageName']))


@step(u'every RPM package installed:')
def check_rpm_installed(step):
    for data in step.hashes:
        assert_true(utils.rpm_installed(data['PackageName']))
