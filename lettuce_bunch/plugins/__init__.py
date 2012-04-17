import os.path, pkgutil
from nose.util import isclass
from lettuce_bunch.plugins.base import BaseOutputPlugin

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
        except ImportError:
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