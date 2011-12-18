
from lettuce import step, world
from nose.tools import assert_equals
from bunch.special import requires_setup

@step(u'Say "(.*)"')
def CheckSaidHelloWorld(step, Phrase):
    assert_equals(Phrase, 'Hello World!')


@step(u'In the beginning was "(.*)"')  
def CheckWord(step, Phrase):
    assert_equals(Phrase, 'the Word')

@step(u'Teardown "(.*)"')
def CheckTeardown(step, Phrase):
    assert_equals(Phrase, 'the World')


@step(u'Requires setup:? "(.*)"')
def requires_setup(step, setup_names):
    """
        This step checks whether required setups are passed or not.
        It is not launches these setups by itself, instead they are launched
        by the Bunch before launching lettuce.
    """
    pass