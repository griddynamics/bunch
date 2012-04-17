from optparse import OptionValueError
from types import StringTypes
from lettuce_bunch.special import get_current_bunch_dir

def parse_plugin_params(option, opt_str, value, parser):
    def join_multiple(params_tuple):
        return ";".join(map(lambda x: x.rstrip(';'), params_tuple))

    def get_params(params_str):
        return dict( [param.split("=", 1) for param in params_str.split(";") ])

    if not isinstance(value, StringTypes) and option.nargs > 1:
        value = join_multiple(value)

    try:
        params = get_params(value)
    except ValueError:
        raise OptionValueError("plugin params string has invalid format")
    else:
        parser.values.plugin_params = params




class BaseOutputPlugin(object):
    def __init__(self, dst_dir=None, **kwargs):
        self.dst_dir = get_current_bunch_dir() if dst_dir is None else dst_dir

    def transform(self, et, details):
        pass



