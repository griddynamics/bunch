from lettuce import step

@step(u'(.*)')
def story_fail(step, statement):
    assert not (step.sentence.find("I start VM instance") >= 0)


