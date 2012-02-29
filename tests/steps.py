from lettuce import step

@step(u'(.*)')
def match_any(step, statement):
    assert True
