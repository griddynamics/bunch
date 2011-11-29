import commands
import os
import time
import re
import yaml
import glob




def init(dir_path):
    global env_dir_path, bash_log
    env_dir_path = dir_path
    bash_log = os.path.join(env_dir_path, "bash.log")


def load_yaml_config(filename):
    with open(filename, 'r') as config_file:
        config = yaml.load(config_file)
        return config


def log(logfile, message):
    with open(logfile, 'a') as file:
        file.write('%s: %s\n' % (time.ctime(), message))

def cmd_successful(retcode):
    return retcode[0] == 0

def cmd_output_nonempty(retcode):
    return len(retcode) > 1 and len(retcode[1]) > 0

def cmd_output_contains_pattern(retcode, pattern):
    regex2match = re.compile(pattern)
    search_result = regex2match.search(retcode[1])
    return (not search_result is None) and len(search_result.group()) > 0


def bash(cmd):
    log(bash_log, "[CMD] " + cmd)
    retcode = commands.getstatusoutput(cmd)
    log(bash_log, "[OUT] " + str(retcode))
    return retcode

def rpm_clean_all_cached_data():
    bash("sudo yum -q clean all")

def remove_files_recursively_forced(wildcard):
    out = bash("sudo rm -rf %s" % wildcard)
    return cmd_successful(out)

def check_no_files_exists(wildcard):
    out = bash("sudo ls -1 %s | wc -l" % wildcard)
    return cmd_successful(out) and cmd_output_contains_pattern(out, "(\s)*0(\s)*")

    


def rpm_install(package):
    out = bash("sudo yum -y install '%s'" % package)
    return cmd_successful(out) and cmd_output_contains_pattern(out, "(Installed:[\s\S]*%s.*)|(Package.*%s.* already installed)" % (package, package))


def rpm_remove(package):
    out = bash("sudo yum -y erase '%s'" % package)
    return cmd_output_contains_pattern(out, "(No Match for argument)|(Removed:[\s\S]*%s.*)|(Package.*%s.*not installed)" % (package, package))


def rpm_installed(package):
    out = bash("rpmquery %s" % package)
    return not ('not installed' in out[1])


def rpm_available(package):
    out = bash("yum list | grep '^%s\..*'" % package)
    return cmd_successful(out) and cmd_output_nonempty(out)



def check_can_execute_sudo_without_pwd():
    out = bash("sudo -l")    
    return cmd_successful(out) and cmd_output_nonempty(out) \
        and cmd_output_contains_pattern(out, "\(ALL\)(\s)*NOPASSWD:(\s)*ALL")



def mysql_create_db(db_name, admin_name="root", admin_pwd="root"):
    bash("mysqladmin -u%s -p%s -f drop %s" % (admin_name, admin_pwd, db_name))
    out = bash("mysqladmin -u%s -p%s create %s" % (admin_name, admin_pwd, db_name))
    return cmd_successful(out)

def exec_mysql_command(sql_command, admin_name="root", admin_pwd="root"):
    out = bash('echo "%s" | mysql -u%s -p%s mysql' % (sql_command, admin_name, admin_pwd))
    return out

def grant_db_access_for_hosts(hostname,db_name, db_user, db_pwd, admin_name="root", admin_pwd="root"):
    sql_command =  "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'%s' IDENTIFIED BY '%s';" % (db_name, db_user, hostname, db_pwd)
    return cmd_successful(exec_mysql_command(sql_command, admin_name, admin_pwd))

def grant_db_access_local(db_name, db_user, db_pwd, admin_name="root", admin_pwd="root"):
    sql_command =  "GRANT ALL PRIVILEGES ON %s.* TO %s IDENTIFIED BY '%s';" % (db_name, db_user, db_pwd)
    return cmd_successful(exec_mysql_command(sql_command, admin_name, admin_pwd))

def check_mysql_db_exists(db_name, admin_name="root", admin_pwd="root"):
    sql_command = "show databases;"
    out = exec_mysql_command(sql_command, admin_name, admin_pwd)
    return cmd_successful(out) and cmd_output_contains_pattern(out, "%s" % db_name)

def check_mysql_user_has_all_privileges_on_db(username, db_name, admin_name="root", admin_pwd="root"):
    sql_command = "show grants for '%s'@'localhost';" %username
    out = exec_mysql_command(sql_command, admin_name, admin_pwd)
    return cmd_successful(out) \
        and cmd_output_contains_pattern(out, "GRANT ALL PRIVILEGES ON .*%s.* TO .*%s.*" % (db_name, username))

def start_service(service):
    out = bash("sudo service %s start" % service)
    return cmd_successful(out)


def stop_service(service):
    out = bash("sudo service %s stop" % service)
    return cmd_successful(out)


def check_service_is_running(service):
    out = bash("sudo service %s status" % service)
    return cmd_successful(out) \
        and cmd_output_contains_pattern(out, "(?i)running") \
        and (not cmd_output_contains_pattern(out, "(?i)stopped|unrecognized|dead"))

def check_service_is_stopped(service):
    out = bash("sudo service %s status" % service)
    unusual_service_patterns = {'rabbitmq-server': 'no_nodes_running'}

    if service in unusual_service_patterns:
        return cmd_output_contains_pattern(out, unusual_service_patterns[service])

    return (not cmd_output_contains_pattern(out, "(?i)running")) \
        and cmd_output_contains_pattern(out, "(?i)stopped|unrecognized|dead")


def perform_nova_db_sync():
    out = bash("sudo nova-manage db sync")
    return cmd_successful(out)