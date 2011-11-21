import commands
import os
import time
import re



log_dir =  os.path.dirname(os.path.abspath(__file__))

bash_log = os.path.join(log_dir, "bash_out.log")


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

def rpm_install(package):
    out = bash("sudo yum -y install %s" % package)
    return cmd_output_contains_pattern(out, "Installed:[\s\S]*%s.*" % package)


def rpm_remove(package):
    bash("sudo yum -q -y erase %s" % package)


def rpm_installed(package):
    out = bash("rpmquery %s" % package)
    return not ('not installed' in out[1])


def rpm_available(package):
    out = bash("yum list | grep '^%s\..*'" % package)
    return cmd_successful(out) and cmd_output_nonempty(out)



def check_can_execute_sudo_without_pwd():
    out = bash("sudo -l")    
    return cmd_successful(out) and cmd_output_nonempty(out) and cmd_output_contains_pattern(out, "\(ALL\)(\s)*NOPASSWD:(\s)*ALL")

