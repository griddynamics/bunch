from lettuce import step, world
from nose.tools import assert_equals, assert_true, assert_false
import utils
import os

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
utils.init(dir_path)
config_file = os.path.join(dir_path, "config.yaml")
config = utils.load_yaml_config(config_file)

def dump(obj):
  for attr in dir(obj):
    print "obj.%s = %s" % (attr, getattr(obj, attr))

mysql_admin = config['db']['admin']
mysql_admin_pwd = config['db']['admin_pwd']

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


@step(u'every RPM package is installed:')
def check_rpm_installed(step):
    for data in step.hashes:
        assert_true(utils.rpm_installed(data['PackageName']))

@step(u'I remove RPM package\(s\):')
def remove_rpm(step):
    utils.rpm_clean_all_cached_data()
    for data in step.hashes:
        assert_true(utils.rpm_remove(data['PackageName']))

@step(u'every RPM package is not installed:')
def check_rpm_not_installed(step):
    for data in step.hashes:
        assert_false(utils.rpm_installed(data['PackageName']))

@step(u'I create MySQL database "(.*)"')
def create_mysql_db(step, db_name):
    assert_true(utils.mysql_create_db(db_name, mysql_admin, mysql_admin_pwd))

@step(u'I grant all privileges on database "(.*)" to user "(.*)" identified by password "(.*)" at hosts:')
def setup_mysql_access_for_hosts(step, db_name, db_user, db_pwd):
    for data in step.hashes:
        assert_true(utils.grant_db_access_for_hosts(data['Hostname'],db_name, db_user, db_pwd, mysql_admin, mysql_admin_pwd))

@step(u'I grant all privileges on database "(.*)" to user "(.*)" identified by password "(.*)" locally')
def setup_mysql_access_local(step, db_name, db_user, db_pwd):
    assert_true(utils.grant_db_access_local(db_name, db_user, db_pwd, mysql_admin, mysql_admin_pwd))
    assert_true(utils.grant_db_access_local(db_name, mysql_admin, mysql_admin_pwd, mysql_admin, mysql_admin_pwd))

@step(u'every service is running:')
def every_service_is_running(step):
    for data in step.hashes:
        assert_true(utils.check_service_is_running(data['ServiceName']))

@step(u'I start services:')
def start_services(step):
    for data in step.hashes:
        assert_true(utils.start_service(data['ServiceName']))


@step(u'MySQL database "(.*)" exists')
def mysql_db_exists(step, db_name):
    print db_name
    assert_true(utils.check_mysql_db_exists(db_name, mysql_admin, mysql_admin_pwd))


@step(u'user "(.*)" has all privileges on database "(.*)"')
def mysql_user_has_all_privileges(step, user, db_name):
    assert_true(utils.check_mysql_user_has_all_privileges_on_db(user, db_name, mysql_admin, mysql_admin_pwd))

@step(u'I perform Nova DB sync')
def perform_nova_db_sync(step):
    assert_true(utils.perform_nova_db_sync())


@step(u'I stop services:')
def stop_services(step):
    for data in step.hashes:
        assert_true(utils.stop_service(data['ServiceName']))

@step(u'every service is stopped:')
def every_service_is_stopped(step):
    for data in step.hashes:
        assert_true(utils.check_service_is_stopped(data['ServiceName']))

@step(u'I clean state files:')
def clean_state_files(step):
    for data in step.hashes:
        assert_true(utils.remove_files_recursively_forced(data['PathWildCard']))

@step(u'no files exist:')
def no_files_exist(step):
    for data in step.hashes:
        assert_true(utils.check_no_files_exists(data['PathWildCard']))