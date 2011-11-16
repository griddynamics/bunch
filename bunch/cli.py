#!/usr/bin/env python


import sys
import os
from optparse import OptionParser
from bunch.core import SerialBunchRunner, Bunch


def usage():
    print sys.argv
    print """\
%prog -- executes bunches of lettuce .feature files
usage: %prog [options] [bunch_dir]... result_dir

    bunch_dir - one or more bunches/tests to execute
    result_dir - destination directory for pesonalized feature files and test results

    options:
    -c|--config[=config.yaml] - Reads global config file before bunch execution
    -b|--bunch-concurrency=serial|full|limited

"""



def main():

    def derive_base_dir(path):
        if os.path.isabs(path):
            return path
        return os.path.abspath(path)


    parser = OptionParser()
    parser.add_option("-c", "--config", action="store", type="string",
                      dest="config", default='config.yaml', metavar="FILE",
                      help="YAML config file")
    parser.add_option("-b", "--bunch-concurency",  action="store", type="string",
                      dest="concurrency", default='serial',
                      help="This option indicates test execution parallelism", metavar="FILE")
    (options, args) = parser.parse_args()

    if len(args) <= 1:  usage(); sys.exit(2)
    output_dir_arg = args[-1]
    bunch_dir_args = args[:-1]


    config_file_name = derive_base_dir(options.config)
    concurrency = options.concurrency
    output_dir = derive_base_dir(output_dir_arg)
    bunch_dirs = map(derive_base_dir, bunch_dir_args)

    # Options are parsed let's personalize test scenarios
    bunch_list = []
    for item in bunch_dirs:
        bunch = Bunch(item, output_dir, config_file_name)
        bunch.deploy()
        bunch.personalize()
        bunch_list.append(bunch)



    def filter_args_for_lettuce(arg):
        if arg in parser._long_opt  or arg in parser._short_opt:
            return False

        for opt in parser._long_opt:
            if str(arg).startswith(opt):
                return False

        for opt in parser._short_opt:
            if str(arg).startswith(opt):
                return False

        if arg in [options.config, options.concurrency]:
            return False

        if arg in bunch_dir_args:
            return False

        if arg == output_dir_arg:
                return False

        if arg == "--with-xunit" or str(arg).startswith("--xunit-file"):
            return False

        return True


    args = filter(filter_args_for_lettuce, sys.argv)
    SerialBunchRunner(bunch_list, args).run()



if __name__ == '__main__':
    main()


  