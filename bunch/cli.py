#!/usr/bin/env python

import codecs
import getopt
import yaml
import pprint
import sys
import os
from optparse import OptionParser
from lettuce import fs, lettuce_cli
import bunch
from shutil import copytree, rmtree, move
from jinja2 import Template


# TODO: load configs files located with templates folder
# TODO: do not delete output folder, back it up or merge it

#default values
base_dir         = os.path.join(os.path.dirname(os.curdir))
config_file_name = os.path.join(base_dir, 'config.yaml')
templates_dir    = os.path.join(base_dir, 'tests')
output_dir       = os.path.join(base_dir, 'personalized')
output_backup_dir= os.path.join(base_dir, 'personalized.backup')

class FeaturePersonalizer(object):
    """Class responsible for creating personalized tests
    """
    def __init__(self, base_dir, global_config, templates_dir=templates_dir,
                 output_dir=output_dir):
        self.global_config = global_config
        self.base_dir = os.path.abspath(base_dir)
        self.templates_dir = templates_dir
        self.output_dir    =  output_dir
        self.output_backup_dir=output_dir+'.backup'

        print "Reading global config: \n", global_config

        # if output folder already exists we should back it up first
        if os.path.exists(self.output_dir):
            #delete backup folder if exists
            if os.path.exists(self.output_backup_dir):
                rmtree(self.output_backup_dir)
            move(self.output_dir, self.output_backup_dir)
        # copy template to the output folder
        # they will be rewritten after processing
        copytree(self.templates_dir, self.output_dir)

    def find_feature_files(self):
        paths = fs.FileSystem.locate(self.output_dir, "*.feature")
        return paths

    def personalize(self):
        for filename in self.find_feature_files():
            with open(filename) as f:
                template = Template(f.read())
    #            print template
            with open(filename, "w") as f:
                f.write(template.render(**self.global_config))
                print f.name


def usage():
    print """\
personalizer.py -- personalizes lettuce .feature files
usage: personalizer.py [output_dir] [--config config.yaml] [--templates template_dir]
"""

pp = pprint.PrettyPrinter(indent=4)

def main():
    parser = OptionParser()
    parser.add_option("-c", "--config", action="store", type="string",
                      dest="config", default='config.yaml', metavar="FILE",
                      help="YAML config file")
    parser.add_option("-t", "--templates",  action="store", type="string",
                      dest="templates_dir", default='tests',
                      help="don't print status messages to stdout", metavar="FILE")
    (options, args) = parser.parse_args()

    config_file_name = os.path.join(base_dir, options.config)
    templates_dir = os.path.join(base_dir, options.templates_dir)


    if len(args) > 0:
        output_dir = os.path.join(base_dir, args[0])

    error = False
    if not os.path.exists(config_file_name):
        print "Config file {0} does not exists".format\
            (config_file_name)
        error = True

    if not os.path.exists(templates_dir):
        print "Template directory {0} does not exists".format\
            (templates_dir)
        error = True

    if error: usage(); sys.exit(2)

    with open(config_file_name) as config_file:
        global_config = yaml.load(config_file)

    print "Using config: ", config_file_name
    print "Using templates dir: ", templates_dir
    print "Write personalized to: ", output_dir

    personalizer = FeaturePersonalizer(base_dir, global_config,
                                       templates_dir=templates_dir,
                                       output_dir=output_dir)
    personalizer.personalize()

    def filter_args_for_lettuce(arg):
        if arg in parser._long_opt  or arg in parser._short_opt:
            return False

        for opt in parser._long_opt:
            if str(arg).startswith(opt):
                return False

        for opt in parser._short_opt:
            if str(arg).startswith(opt):
                return False

        if arg in [options.config, options.templates_dir]:
            return False

        return True

    sys.argv = filter(filter_args_for_lettuce, sys.argv)
    lettuce_cli.main()


if __name__ == '__main__':
    main()


  