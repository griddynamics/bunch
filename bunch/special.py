from lettuce import step, world
import pprint

pp = pprint.PrettyPrinter(indent=4)

@step(u'Requires setup:? "(.*)"')
def requires_setup(step, Phrase):
    """
        This step checks whether required setups are passed or not.
        It is not launches these setups by itself, instead they are launched
        by the Bunch before launching lettuce.
    """
    pp.pprint(step)