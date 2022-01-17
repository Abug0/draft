"""
class Greenlet
"""


class Greenlet:
    def __init__(self, func=None) -> None:
        self.func = func
        self.has_completed = False
        self.ret = None

    def run(self):
        if self.func:
            self.ret = self.func()

        self.has_completed = True

    def get(self):
        pass

    def is_completed(self):
        return self.has_completed
