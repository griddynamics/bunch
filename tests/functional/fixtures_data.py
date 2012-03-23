from os.path import dirname, abspath, join
CURRENT_DIR = abspath(dirname(__file__))
DATA_DIR = join(CURRENT_DIR, 'data')

def load_data_from_file(file):
    with open(join(DATA_DIR,file), 'rU') as f:
        return f.read()

SIMPLE_DEPS_CONSOLE_OUTPUT_PATTERN = load_data_from_file('simple_deps_console.pattern')
BASIC_REQS_CONSOLE_OUTPUT_PATTERN = load_data_from_file('osc_requires_basic_console.pattern')
BASICP_REQS_CONSOLE_OUTPUT_PATTERN = load_data_from_file('osc_requires_basic_proper_console.pattern')
LIGHT_REQS_CONSOLE_OUTPUT_PATTERN =   load_data_from_file('light_console.pattern')
