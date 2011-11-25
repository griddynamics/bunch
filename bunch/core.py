
import os
import sys
import re
from lettuce import fs
from shutil import copytree, rmtree, move
import yaml
from jinja2 import Template
from lettuce import lettuce_cli, Feature
from xml.dom import minidom
import multiprocessing
import subprocess


class FeaturePersonalizer(object):
    """Class responsible for creating personalized tests
    """
    def __init__(self, working_dir, global_config=None):
        self.working_dir = working_dir
        self.local_config = None
        self.global_config = None
        self.local_config = None

        if os.path.exists(global_config):
            with open(global_config) as global_config_file:
                self.global_config = yaml.load(global_config_file)

        expected_local_config_file = os.path.join(self.working_dir, 'config.yaml')
        if os.path.exists(expected_local_config_file):
            with open(expected_local_config_file) as local_config_file:
                self.local_config = yaml.load(local_config_file)

    def __find_feature_files(self):
        paths = fs.FileSystem.locate(self.working_dir, "*.setup") +\
            fs.FileSystem.locate(self.working_dir, "*.test") +\
            fs.FileSystem.locate(self.working_dir, "*.teardown")
        return paths

    def personalize(self):
        if (not self.global_config is None) or (not self.local_config is None):
            environment = dict()
            if not self.global_config is None: environment.update(self.global_config)
            if not self.local_config is None: environment.update(self.local_config)
            for filename in self.__find_feature_files():
                with open(filename, "r") as f:
                    template = Template(f.read())
        #            print template
                
                with open(filename, "w") as f:
                    f.write(template.render(**environment))
                    print f.name


class Bunch(object):
    def __init__(self, src_dir, dst_dir, global_config=None):
        self.global_config = global_config
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.is_single_test = self.__is_single_test(src_dir)

        if not self.is_single_test:
            self.bunch_dir = src_dir
        else:
            self.bunch_dir = self.__get_test_bunch(src_dir)

        self.deploy_dir = os.path.join(self.dst_dir, self.name())
        self.deploy_backup_dir = self.deploy_dir + '.backup'

    def __get_test_bunch(self, path):
        return os.path.dirname(path)

    def __is_single_test(self, path):
        if os.path.isfile(path) and os.path.basename(path).endswith(".test"):
            return True

        return False

    def name(self):
        return os.path.basename(self.bunch_dir)
    
    def deploy(self):
        # if output folder already exists we should back it up first
        if os.path.exists(self.deploy_dir):
            #delete backup folder if exists
            if os.path.exists(self.deploy_backup_dir):
                rmtree(self.deploy_backup_dir)
            move(self.deploy_dir, self.deploy_backup_dir)
        # copy template to the output folder
        # they will be rewritten after processing
        copytree(self.src_dir, self.deploy_dir)

    def personalize(self):
        FeaturePersonalizer(self.deploy_dir, self.global_config).personalize()

    def deployed_at(self):
        return self.bunch_dir

    def get_test_scenarios(self):
        test_scripts = fs.FileSystem.locate(self.deploy_dir, "*.test")
        setup_scripts = fs.FileSystem.locate(self.deploy_dir, "*.setup")
        teardown_scripts = fs.FileSystem.locate(self.deploy_dir, "*.teardown")
        scenarios = []
        for test in test_scripts:
            test_name, ext = os.path.splitext(os.path.basename(test))
            test_prefix = test_name + "."
            test_setup_scripts = [item for item in setup_scripts if os.path.basename(item).startswith(test_prefix)]
            test_teardown_scripts = [item for item in teardown_scripts if os.path.basename(item).startswith(test_prefix)]
            scenarios.append(BunchTestStory(test, test_setup_scripts, test_teardown_scripts))

        return scenarios

            


class BunchTestStory(object):
    setup_scenario = u'Prepare setup'
    #re_setup = re.compile(r'.*Requires setup(:[\s\S]*"""[\s\S]*""")|(".*")')
    re_setup = re.compile(r'Requires setup:? "(.*)"')
    re_external_setup = re.compile(r'Requires external setup:? "(.*)"')
    #re_external_setup = re.compile(r'Requires external setup "(.*)"')

    def __init__(self, test, setup=None, teardown=None):
        self.test = test
        self.setup = [] if setup is None else setup
        self.teardown = [] if teardown is None else teardown
        self.name = self.__get_name()

    def __get_name(self):
        test_name, ext = os.path.splitext(os.path.basename(self.test))
        return test_name

    def __find_setup_definitions(self, sentence):
        setup_names = self.re_setup.findall(sentence)[0]
        if setup_names:
            return setup_names

    def __find_external_setup_definitions(self, sentence):
        external_setup_names = self.re_external_setup.findall(sentence)[0]
        if external_setup_names:
            return external_setup_names

    def __get_setup_requirements(self):
        feature = Feature.from_file(self.test)
        for scenario in feature.scenarios:
            if scenario.name == self.setup_scenario:
                for step in scenario.steps:
                    setup_names = self.__find_setup_definitions(step.original_sentence)
                    return setup_names


    def get_test_triplet(self, env_name=None):
        fixture_name = self.name if env_name is None else self.name + "." + env_name
        setup_names = [os.path.splitext(os.path.basename(item))[0] for item in self.setup]
        teardown_names = [os.path.splitext(os.path.basename(item))[0] for item in self.teardown]
        setup = self.setup[setup_names.index(fixture_name)] if fixture_name in setup_names else None
        teardown = self.teardown[teardown_names.index(fixture_name)] if fixture_name in teardown_names else None
        return self.test, setup, teardown

    def __get_depencies(self, name_list, basedir, postfix):
        if name_list and len(name_list):
            name2path = lambda n: os.path.join(basedir, n+postfix)
            return map(name2path, name_list)

    def get_test_setup_dependencies(self):
        #returns a list of tuples: ('bunch', "script")
        return self.__get_depencies(self.__get_setup_requirements(),
                                    os.path.dirname(self.test),
                                    ".setup")

    def get_test_teardown_dependencies(self):
        reqs = self.__get_setup_requirements()
        if reqs and len(reqs):
            name2path = lambda n: os.path.join(os.path.dirname(self.test), n+".teardown")
            #reverse
            return map(name2path, reqs)

    def get_story_files(self, env_name=None):
        """ Return file names list of the story files.
            First elements of this list are setup files required by test,
            then goes test file itself, and then teardown files in reverse order
        """
        test, setup, teardown  = self.get_test_triplet(env_name)
        test_depencies = self.get_test_setup_dependencies()
        teardown_depencies = self.get_test_teardown_dependencies()

        story_files = [setup]
        if test_depencies:
            story_files.extend(test_depencies)
        story_files.append(test)
        if teardown_depencies:
            story_files.extend(reversed(teardown_depencies))
        story_files.append(teardown)

        return story_files






class SerialBunchRunner(object):
    def __init__(self, bunch_list, args, env_name=None):
        self.args = args
        self.bunch_list = bunch_list
        self.env_name=env_name

    def __save_path_for_test(self, test):
        return os.path.splitext(test)[0] + ".result.xml"

    def run(self):
        for bunch in self.bunch_list:
            scenarios = bunch.get_test_scenarios()
            for scenario in scenarios:
                #test, setup, teardown  = scenario.get_test_triplet(self.env_name)
                #TODO: если присутсвует в писке
                story_files = scenario.get_story_files(self.env_name)
                results = XmlResultCollector()
                for item in story_files:
                    if item:
                        if item == scenario.test and (not results.all_successful()):
                            break
                        runner = LettuceRunner(item, self.args)
                        runner.run()
                        results.pickup(runner.xml_result())
                        runner.clean()
                        #TODO add fixture result handling
                results.dump(self.__save_path_for_test(scenario.test))



class XmlResultCollector(object):
    re_success = re.compile(r'<testsuite.*failed="0"')
    
    def __init__(self):
        self.results = []


    def pickup(self, filename):
        with open(filename, 'r') as result_file:
                self.results.append(result_file.read())


    def __junit_test_passed(self, result):
        search_result = XmlResultCollector.re_success.search(result)
        return (not search_result is None) and len(search_result.group()) > 0

    def __successful(self, result_index):
        return self.__junit_test_passed(self.results[result_index])

    def all_successful(self):
        for result in self.results:
            if not self.__junit_test_passed(result):
                return False

        return True

    def dump(self, filename):
        with open(filename, 'w') as result_file:
            result_file.write(self.__merge_results().encode('utf-8'))

    def __merge_results(self):
        total_steps = 0
        failed_steps = 0
        rez_doc = minidom.Document()
        all_testcases = []

        for text in self.results:
            doc = minidom.parseString(text)
            ts = doc.getElementsByTagName("testsuite")
            for item in ts:
                if item.hasAttribute("failed"):
                    failed_steps += int(item.getAttribute("failed"))
                if item.hasAttribute("tests"):
                    total_steps += int(item.getAttribute("tests"))
                all_testcases.extend(item.getElementsByTagName("testcase"))

        root = rez_doc.createElement("testsuite")
        root.setAttribute("tests", str(total_steps))
        root.setAttribute("failed", str(failed_steps))

        for tc in all_testcases:
            root.appendChild(tc)

        rez_doc.appendChild(root)
        return rez_doc.toxml()



class LettuceRunner(object):
    def __init__(self, script, args):
        self.args = args
        self.script = script

    def __xml_report_file(self):
        return os.path.join(os.path.dirname(self.script), "result.xml")

    def run(self):
        new_args = []
        new_args.extend(self.args)
        new_args.append("--with-xunit")
        new_args.append("--xunit-file=" + self.__xml_report_file())
        new_args.append(self.script)
        sys.argv = new_args
        #lettuce_cli.main()
        #Due to bug in Lettuce: we need to call it via console script
        lettuce_cmd_line = ["lettuce"]
        lettuce_cmd_line.extend(sys.argv[1:])
        subprocess.call(lettuce_cmd_line)

    def xml_result(self):
        return self.__xml_report_file()

    def clean(self):
        os.remove(self.xml_result())