from lettuce import step, world
import utils

@step(u'Install "(.*)"')
def install_group1(step, group1):
    utils.rpm_install(group1)

@step(u'Check if "(.*)" is not installed')
def check_if_group1_is_not_installed(step, name):
    utils.rpm_check(name, installed=False)

@step(u'Check if "(.*)" is installed')
def check_if_group1_is_installed(step, name):
    utils.rpm_check(name)

@step(u'Change flags in "([^"]*)":')
def change_flags_in_group1(step, file_name):
    values={}
    for data in step.hashes:
        values[data['Flag']]=data['Value']
    utils.fix_nova_conf(conf_file=file_name, flags_to_fix=values)


@step(u'Start services:')
def start_services(step):
    for data in step.hashes:
        utils.start_service(data['ServiceName'])

@step(u'Create database "([^"]*)" with data "([^"]*)"')
def create_database_group1_with_data_group2(step, name, script):
    utils.mysql_create_database(database=name, sql_file=script)


@step(u'Check database "([^"]*)" exists')
def check_database_group1(step, dbname):
    utils.mysql_check_database(dbname)


@step(u'Check database "([^"]*)" not exists')
def check_database_group1(step, dbname):
    utils.mysql_check_miss_database(dbname)

@step(u'Sync database')
def sync_database(step):
    utils.sync_db()


@step(u'Check services running:')
def check_openstack_services_running(step):
    for data in step.hashes:
        servicename = data['ServiceName']
        utils.check_service(servicename)

@step(u'Check services NOT running:')
def check_openstack_services_not_running(step):
    for data in step.hashes:
        servicename = data['ServiceName']
        utils.check_service(servicename, is_running=False)


@step(u'Create admin user "(.*)"')
def create_admin_user_group1(step, name):
    utils.create_admin_user(name)

@step(u'Check user "(.*)" exist')
def check_user_group1_exist(step, group1):
    utils.check_user(group1)

@step(u'Check user "(.*)" does not exist')
def check_user_group1_not_exist(step, group1):
    utils.check_user(group1, False)