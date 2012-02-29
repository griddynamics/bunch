import os
import sys
import re
from lettuce import fs
from shutil import copytree, rmtree, move
import yaml
from jinja2 import Template
from lettuce import Feature
from xml.dom import minidom
import subprocess
import pprint
from bunch import dependencies
from bunch.exceptions import CyclicDependencySpecification


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
        return sorted(paths)

    def personalize(self):
        if (not self.global_config is None) or (not self.local_config is None):
            environment = dict()
            if not self.global_config is None: environment.update(self.global_config)
            if not self.local_config is None: environment.update(self.local_config)


            for filename in self.__find_feature_files():
                with open(filename, "r") as f:
                    template = Template(f.read())
                
                with open(filename, "w") as f:
                    f.write(template.render(**environment))



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

    def get_stories(self):
        test_scripts = sorted(fs.FileSystem.locate(self.deploy_dir, "*.test"))
        setup_scripts = sorted(fs.FileSystem.locate(self.deploy_dir, "*.setup"))
        teardown_scripts = sorted(fs.FileSystem.locate(self.deploy_dir, "*.teardown"))
        stories = []
        for test in test_scripts:
            test_name, ext = os.path.splitext(os.path.basename(test))
            test_prefix = test_name + "."
            test_setup_scripts = [item for item in setup_scripts if os.path.basename(item).startswith(test_prefix)]
            test_teardown_scripts = [item for item in teardown_scripts if os.path.basename(item).startswith(test_prefix)]
            stories.append(BunchTestStory(test, test_setup_scripts, test_teardown_scripts))

        return stories

            


class BunchTestStory(object):
    setup_scenario = u'Setup prerequisites'
    re_setup = re.compile(r'Require setup:? "(.*)"')
    re_external_setup = re.compile(r'Require external setup:? "(.*)"')


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
            return setup_names.split()

    def __find_external_setup_definitions(self, sentence):
        external_setup_names = self.re_external_setup.findall(sentence)[0]
        if external_setup_names:
            return external_setup_names.split()

    def __get_setup_requirements(self):
        feature = Feature.from_file(self.test)
        for scenario in feature.scenarios:
            if scenario.name == self.setup_scenario:
                for step in scenario.steps:
                    setup_names = self.__find_setup_definitions(step.original_sentence)
                    return setup_names
        return []

    def get_test_triplet(self, env_name=None):
        setup_names = [os.path.splitext(os.path.basename(item))[0] for item in self.setup]
        teardown_names = [os.path.splitext(os.path.basename(item))[0] for item in self.teardown]

        def name_with_env(name, env):
            return name+"."+env

        def select_existing(name_list, name, env):
            if env is not None and name_with_env(name, env) in name_list:
                return name_with_env(name, env)

            return name if name in name_list else None

        setup_name = select_existing(setup_names, self.name, env_name)
        teardown_name = select_existing(teardown_names, self.name, env_name)
        setup = self.setup[setup_names.index(setup_name)] if setup_name is not None else None
        teardown = self.teardown[teardown_names.index(teardown_name)] if teardown_name is not None else None
        return self.test, setup, teardown


    def __get_dependencies(self, name_list, basedir, suffix, env_name=None):
        def fixture_env_select(name):
            item = os.path.join(basedir, name)
            if env_name is not None and os.path.exists(item+'.'+env_name+suffix):
                return item+'.'+env_name+suffix

            if os.path.exists(item+suffix):
                return item+suffix

            return None

        return map(fixture_env_select, name_list)

    def __get_dependency_groups(self, type_suffix, env_name=None):
        def split_list(lst, pivot):
            remainder = lst
            result = []
            while pivot in remainder:
                idx = remainder.index(pivot)
                result.append(remainder[:idx])
                remainder = remainder[idx+1:]
            result.append(remainder)
            return result

        fixture_reqs = self.__get_setup_requirements()
        req_groups = filter(None, split_list(fixture_reqs, '!'))
        dep_groups = [filter(None, self.__get_dependencies(group, os.path.dirname(self.test),type_suffix, env_name))
                    for group in req_groups]
        #filter out places of missing fixtures
        dep_groups = filter(None, dep_groups)

        return dep_groups

    def get_setup_dependency_groups(self, env_name=None):
        return self.__get_dependency_groups(".setup", env_name)

    def get_teardown_dependency_groups(self, env_name=None):
        return list(reversed(self.__get_dependency_groups(".teardown", env_name)))

    def get_test_setup_dependencies(self, env_name=None):
        return self.__get_dependencies(filter(lambda x: '!' not in x, self.__get_setup_requirements()),
                                    os.path.dirname(self.test),
                                    ".setup", env_name)

    def get_test_teardown_dependencies(self, env_name=None):
        return self.__get_dependencies(filter(lambda x: '!' not in x, self.__get_setup_requirements()),
                                    os.path.dirname(self.test),
                                    ".teardown", env_name)


    def get_fixtures(self, env_name=None):
        test, setup, teardown  = self.get_test_triplet(env_name)
        setup_dependencies = self.get_test_setup_dependencies(env_name)
        teardown_dependencies = self.get_test_teardown_dependencies(env_name)
        pairs = map(lambda a,b: (a,b), setup_dependencies, teardown_dependencies)

        #Now we should detect if setup is specified explicitly in setup_dependencies
        if setup not in setup_dependencies:
            pairs.append((setup, teardown))

        return pairs

class SerialBunchRunner(object):
    def __init__(self, bunch_list, args, env_name=None):
        self.args = args
        self.bunch_list = bunch_list
        self.env_name=env_name

    def __save_path_for_test(self, test):
        return os.path.splitext(test)[0] + ".result.xml"

    def __run_lettuce(self, runner, collector):
        success = runner.run()
        collector.pickup(runner.xml_result())
        runner.clean()
        return success

    def __print_story_scripts_to_run(self, fixture_pairs, test):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(fixture_pairs)
        pp.pprint(test)

    def __print_cyclic_dependencies_error(self, cycle_details, name):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint("bunch {name} execution skipped due to cyclic dependencies found:".format(name=name))
        pp.pprint(cycle_details)

    def __get_fixture_deps(self, stories):
        return [story.get_setup_dependency_groups(self.env_name) for story in stories], \
               [ story.get_teardown_dependency_groups(self.env_name) for story in stories]

    def __run_fixtures(self, groups, results_name, stop_on_failure=True):
        results = XmlResultCollector()
        for group in groups:
            for script in group:
                if not results.all_successful() and stop_on_failure:
                    break
                self.__run_lettuce(LettuceRunner(script, self.args), results)
        results.dump(results_name)
        return results.all_successful()

    def __deps_contain(self, deps, fixture):
        for group in deps:
            if fixture in group:
                return True
        return False

    def __exec_default_fixture(self, fixture, result, deps):
        if not self.__deps_contain(deps, fixture):
            return self.__run_lettuce(LettuceRunner(fixture, self.args), result) and result.all_successful()
        return True

    def __run_story(self, story, setup_seq, teardown_seq):
        result = XmlResultCollector()
        test, setup, teardown = story.get_test_triplet(self.env_name)
        if setup:
            self.__exec_default_fixture(setup, result, setup_seq)
        if result.all_successful():
            self.__run_lettuce(LettuceRunner(test, self.args), result)
        if teardown:
            self.__exec_default_fixture(teardown, result, teardown_seq)
        result.dump(self.__save_path_for_test(story.test))
        return result.all_successful()

    def __run_stories(self, stories, setup_seq, teardown_seq):
        none_failed = True
        for story in stories:
            none_failed = none_failed and self.__run_story(story, setup_seq, teardown_seq)
        return none_failed


    def run(self):
        """
        Execute set of test bunches sequentially
        """
        none_failed = True
        for bunch in self.bunch_list:
            stories = bunch.get_stories()
            setup_deps, teardown_deps = self.__get_fixture_deps(stories)
            try:
                setup_seq = dependencies.combine_fixture_deps(setup_deps)
                teardown_seq = dependencies.combine_fixture_deps(teardown_deps)
            except CyclicDependencySpecification as cycle_error:
                self.__print_cyclic_dependencies_error(cycle_error, bunch.name())
                continue
            #Now perform all setup

            if self.__run_fixtures(setup_seq, self.__save_path_for_test(os.path.join(bunch.deploy_dir,"setup"))):
                #setup passed, execute tests
                none_failed = none_failed and self.__run_stories(stories, setup_seq, teardown_seq)
            else:
                none_failed = False

            #Now execute teardown disregarding setup results and ignoring script failures
            self.__run_fixtures(teardown_seq,
                self.__save_path_for_test(os.path.join(bunch.deploy_dir,"teardown")), False)
        return none_failed



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

    def __exec_cmd(self, args):
        #return subprocess.call(args)
        process = subprocess.Popen(args,stdout = sys.stdout, stderr = sys.stderr)
        output,error = process.communicate()
        return process.poll()



    def run(self):
        new_args = []
        new_args.extend(self.args)
        new_args.append("--verbosity=3")
        new_args.append("--with-xunit")
        new_args.append("--xunit-file=" + self.__xml_report_file())
        new_args.append(self.script)
        sys.argv = new_args
        #lettuce_cli.main()
        #Due to bug in Lettuce: we need to call it via console script
        lettuce_cmd_line = ["lettuce"]
        lettuce_cmd_line.extend(sys.argv[1:])

        retcode = self.__exec_cmd(lettuce_cmd_line)
        return retcode == 0
        






    def xml_result(self):
        return self.__xml_report_file()

    def clean(self):
        os.remove(self.xml_result())