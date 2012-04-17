from lettuce import step
import random

def flip(p):
    return True if random.random() < p else False

@step(u'(.*)')
def fail_random(step, statement):
    assert flip(0.5)
