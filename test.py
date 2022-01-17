import time

from src.hub import Hub
from src.greenlet import Greenlet


hub = Hub()


def sleep(seconds=1):
    hub.add_sleep_event(self, seconds)


def func1():
    print("func1---time: %s", time.time())
    sleep(3)


def func2():
    print("func2---time: %s", time.time())
    sleep(3)


g1 = Greenlet(func1)
g2 = Greenlet(func2)

hub.run()
