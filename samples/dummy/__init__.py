
from lettuce import step, world
from nose.tools import assert_equals

@step(u'Say "(.*)"')
def CheckSaidHelloWorld(step, Phrase):
    assert_equals(Phrase, 'Hello World!')


@step(u'In the beginning was "(.*)"')  
def CheckWord(step, Phrase):
    assert_equals(Phrase, 'the Word')

@step(u'Teardown "(.*)"')
def CheckTeardown(step, Phrase):
    assert_equals(Phrase, 'the World')
