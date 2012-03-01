

class BaseFixtureRunner(object):
    def __init__(self, id):
        self.id = id

    def running(self):
        return False

    def ready(self):
        return False

    def successful(self):
        return None

    def wait(self, Timeout=None):
        pass

    def execute(self):
        pass


class BaseSetupRunner(BaseFixtureRunner):
    pass

    
class BaseTeardownRunner(BaseFixtureRunner):
    pass




