import commands
import os
import re
import socket
import yaml
import shutil

with open('config.yaml') as config_file:
    global_config = yaml.load(config_file)


__docformat__ = 'restructuredtext en'
def rpm_install(name):
    """ Not implemented yet
    """
    #    Common.bash("yum -q clean all")
    #    Common.bash("yum -q -y install %s" % package)
    pass


def rpm_check(name, installed=True):
#    out = Common.bash("rpmquery %s" % package)
#
#    if (installed=='1') and ('not installed' in out):
#        Common.fail("Package %s must be installed. Error: %s" % (package,out))
#
#    elif (installed=='0') and 'already installed' in out:
#        Common.fail("Package %s must NOT  be installed. Error: %s" % (package,out))
    pass



def fix_nova_conf(conf_file, flags_to_fix):
    """
    :param conf_file: path ot a nova.conf file
    :param flags_to_fix: a dict where keys are the flag names and values are
        actual flag values e.g. flags_to_fix = {'--verbose': 'true'}
    """

    conf_lines=_parse_config(conf_file)
    for flag in conf_lines:
        if flag in flags_to_fix:
            #Searching for flag. If found - change value and mark it changed. We suupose flags has no dupes
            #if bool(debug): print "Changing Flag:%s from %s to %s" %
            # (flag,conf_lines[flag],flags_to_fix[flag])
            conf_lines[flag]=flags_to_fix[flag]
            del flags_to_fix[flag]

    # If we have flags that weren't already been in the nova.conf we must add
    # them  to the config
    if len(flags_to_fix):
        for flag in flags_to_fix:
            conf_lines[flag]=flags_to_fix[flag]

    with open(conf_file+'.new', 'w') as new_conf:
        for param in conf_lines:
           new_conf.write(param+'='+conf_lines[param]+'\n')

    shutil.move(conf_file, conf_file+".back")
    shutil.move(conf_file+'.new', conf_file)

def _parse_config(filename):
    COMMENT_CHAR = '#'
    OPTION_CHAR =  '='

    options = {}
    with open(filename) as f:
        for line in f:
            if COMMENT_CHAR in line:
                line, comment = line.split(COMMENT_CHAR, 1)

            if OPTION_CHAR in line:
                option, value = line.split(OPTION_CHAR, 1)
                option = option.strip()
                value = value.strip()
                options[option] = value

    return options

def start_service(service_name):
    return _service(service_name, 'start')

def _service(service_name, action):
    cmd = 'service %s %s'
    return bash(cmd % (service_name, action))


def bash(cmd, errcode='0'):
    if 'runtime' not in os.listdir('./'):
        if commands.getstatusoutput('mkdir -p runtime')[0]:
            fail('Failed to create ./runtime dir!')

    #if bool(debug):
    print "\nBash: "+cmd
    retcode = commands.getstatusoutput(cmd)
    if retcode[0] != '0'  :
        print "OUT:\n "+retcode[1]+"\n"

    if retcode[0]<0:
        fail("\n\n\nCommand '%s' failed with code %s.\n Error: %s\n" %
               (cmd, retcode[0],retcode[1]))
    elif retcode[0]>0:
        #if bool(debug):
        print ("\n\n\nNon fatal: \n Command '%s' failed with code %s.\n Error: %s\n" % (cmd, retcode[0],retcode[1]))

#    log=open(logfile, 'a')
#    log.write('\n'+time.ctime()+': Command: %s \n' % cmd )
#    log.write(time.ctime()+': Output (%s): %s \n' % (retcode[0],retcode[1]) )
#    log.close()

    return retcode[1]



def fail(msg):
#    log=open(logfile, 'a')
#    log.write('\n'+time.ctime()+': ERROR: %s \n' % msg )
#    log.close()
    raise Exception("Got exception: %s" % msg)


def mysql_create_database(database, sql_file):
    bash("mysqladmin -uroot create {0}".format(database))
#    bash("cat {0} | mysql -uroot mysql ".format(sql_file))
    host = socket.gethostname()
#    bash('''echo "GRANT ALL PRIVILEGES ON %s.* TO %s@'%s' IDENTIFIED BY
# '%s';" | mysql -uroot -pnova mysql''' % (database, user, host, password))
#    Common.bash(echo "GRANT ALL PRIVILEGES ON '%s'.* TO '%s' IDENTIFIED BY '%s';" | mysql -uroot -pnova mysql % (database, 'root', 'nova'))
#    Common.bash(echo "GRANT ALL PRIVILEGES ON '%s'.* TO '%s'@'any' IDENTIFIED BY '%s';" | mysql -uroot -pnova mysql % (database, user, password))
    sql = '''CREATE USER '{username}' IDENTIFIED BY '{password}';
    CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';
    GRANT ALL PRIVILEGES ON {dbname}.* TO '{username}' IDENTIFIED BY '{password}';
    GRANT ALL PRIVILEGES ON {dbname}.* TO '{username}'@'localhost' IDENTIFIED BY '{password}';
    GRANT ALL PRIVILEGES ON {dbname}.* TO '{username}'@'127.0.0.1' IDENTIFIED BY '{password}';
    '''.format(**{'username':global_config['db']['user'],
                'password':global_config['db']['user'],
                'dbname': database})
    print(sql)
    bash(sql)


def mysql_check_database( database='nova'):
    p = bash("echo 'show databases;' | mysql -uroot --raw")
    if database not in p:
        fail("Database %s not exist" % (database,))


def mysql_check_miss_database( database='nova'):
    p = bash("echo 'show databases;' | mysql -uroot --raw")
    if database in p:
        fail("Database %s exist" % (database,))


def sync_db():
    bash('nova-manage db sync')


def check_service(service_name, is_running=True):
    out=_service(service_name,'status')

    if 'running' in out and is_running:
        pass
    elif 'running' in out and not is_running:
        fail("Service %s refused to stop." % service_name)
    elif 'stoped' in out and is_running:
        fail("Service %s refused to start." % service_name)
    elif 'unrecognized' in out:
        fail("Service %s is not exist." % service_name)
    else:
        fail("Service %s failed.: %s" % (service_name,out))

    out == bash('ps ax -o pid,comm |grep nova')
    if 'defunc' in out:
        bash('killall '+service_name)


def create_admin_user(user):
    out=bash("nova-manage user list")
    m=re.match(user, out)
    if m:
        pass
        #fail("Try to crate user %s, but it exist!" % user)
    else:
        out=bash('nova-manage user admin %s' % user)
    return out


def check_user(user, exist=True):
    out=bash("nova-manage user list")
    found = re.search(user, out)
    if found and not exist:
        fail("Deleted by script user %s  exist, but it must not." % user)
    elif not found and exist:
        fail("Created by script user %s does not exist, but it must." % user)