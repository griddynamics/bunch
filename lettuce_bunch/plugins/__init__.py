import os.path, pkgutil
from nose.util import isclass
from lettuce_bunch.plugins.base import BaseOutputPlugin
from collections import OrderedDict
import traceback


PLUGIN_CLASS_NAME = 'OutputPlugin'
MODULE_PREFIX = 'lettuce_bunch.plugins'

def plugins_list():
    def filter_no_plugins(module):
        name =  MODULE_PREFIX + ".%s" % module
        try:
            module = __import__(name, fromlist=[PLUGIN_CLASS_NAME])
            module_attrs = dir(module)
            if 'OutputPlugin' in module_attrs:
                plugin = getattr(module, PLUGIN_CLASS_NAME)
                if isclass(plugin):
                    return True
        except ImportError, e:
            str_reason = traceback.format_exc(e)
            return False

        return False

    pkgpath = os.path.dirname(__file__)
    pkglist = filter(filter_no_plugins,[name for _, name, _ in pkgutil.iter_modules([pkgpath])])

    return pkglist

def load_plugin(name, params):
    params = {} if params is None else params
    if name is not None:
        name =  MODULE_PREFIX + ".%s" % name
        module = __import__(name, fromlist=[PLUGIN_CLASS_NAME])
        plugin_class = getattr(module, PLUGIN_CLASS_NAME)
        return plugin_class(**params)
    return BaseOutputPlugin(**params)

class BunchDetails(object):
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description

class BunchResultItem(object):
    def __init__(self, item):
        self.item = item

    def result(self):
        item_result = self.item.find('result')
        if item_result is not None:
            return item_result.text
        return ''

    def get_type(self):
        if self.item.tag == 'feature':
            return 'features'
        elif self.item.tag == 'scenario':
            return 'scenarios'
        elif self.item.tag == 'step':
            return 'steps'

        return None

    def name(self):
        name_path = 'properties/sentence' if self.item.tag == 'step' else 'properties/name'
        item_name = self.item.find(name_path)
        if item_name is not None:
            return item_name.text
        return ''


class BunchResults(object):
    def __init__(self, et):
        self.et = et.find('.')

    def __get_result_map(self, items):
        map = OrderedDict()
        for item in items:
            item_result = item.find('result')
            name_path = 'properties/sentence' if item.tag == 'step' else 'properties/name'
            item_name = item.find(name_path)
            if item_name is not None and item_name.text != '':
                #map[item_name.text] = item_result.text
                map[item] = (item_name.text, item_result.text)
        return map

    def get_by_type(self, item_type):
        type_map = {'features': self.features,
                    'scenarios' : self.scenarios,
                    'steps' : self.steps}

        rez = type_map[item_type]()
        return rez

    def __self_result_map(self):
        return self.__get_result_map(self.et.findall('.'))

    def __len__(self):
        return len(self.features()) + len(self.scenarios()) + len(self.steps())

    def features(self):
        #return self.__get_result_map(self.et.findall('feature'))
        rez =  self.__get_result_map(self.et.findall('.//feature'))
#        if len(rez) == 0 and self.et.tag == 'feature':
#            rez = self.__get_result_map(self.et.findall('.'))
        return rez

    def scenarios(self):
        #return self.__get_result_map(self.et.findall('feature/scenarios/scenario'))
        rez =  self.__get_result_map(self.et.findall('.//scenario'))
#        if len(rez) == 0 and self.et.tag == 'scenario':
#            rez = self.__get_result_map(self.et.findall('.'))
        return rez

    def steps(self):
        #return self.__get_result_map(self.et.findall('feature/scenarios/scenario/steps/step'))
        rez = self.__get_result_map(self.et.findall('.//step'))
#        if len(rez) == 0 and self.et.tag == 'step':
#            rez = self.__get_result_map(self.et.findall('.'))
        return rez

