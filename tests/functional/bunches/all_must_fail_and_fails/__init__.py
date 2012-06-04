from lettuce import step


@step(u'(.*?)Must Fail(.*?)')
def must_fail(step, before, after):
    assert False


@step(u'(.*?)Should Pass(.*?)')
def should_pass(step, before, after):
    assert True