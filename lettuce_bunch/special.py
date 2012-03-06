from lettuce import step, world
import pprint
import os

pp = pprint.PrettyPrinter(indent=4)

BUNCH_PATH_ENV_VAR = "CURRENT_BUNCH_DIR"

@step(u'Require setup:? "(.*)"')
def requires_setup(step, Phrase):
    """
        This step checks whether required setups are passed or not.
        It is not launches these setups by itself, instead they are launched
        by the Bunch before launching lettuce.
    """
    pp.pprint(step)

@step(u'Require external setup:? "(.*)"')
def requires_external_setup(step, Phrase):
    """
        This step checks whether required setups are passed or not.
        It is not launches these setups by itself, instead they are launched
        by the Bunch before launching lettuce.
    """
    pp.pprint(step)

def get_current_bunch_dir():
    return os.getenv(BUNCH_PATH_ENV_VAR)

def set_current_bunch_dir(value):
    os.putenv(BUNCH_PATH_ENV_VAR, value)