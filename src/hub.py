"""
Class Hub
"""


import select
import time


class Hub:
    def __init__(self) -> None:
        self.greenlets = []
        self.completed_greeblets = []

        # {fd: Greenlet}
        self.events_waiting = {}
        self.r_events_waiting = {}
        self.w_events_waiting = {}

        # sleep的greenlet
        self.sleep_events_waiting = {}

    def run(self):
        # 找出等待事件已就绪的Greenlet
        # 运行它
        timeout = 5
        timeout = min(self.sleep_events_waiting.values())

        while True:
            if not self.r_events_waiting and not self.w_events_waiting:
                time.sleep(timeout)
            else:
                rlist, wlist, _ = select.select(
                    self.r_events_waiting.keys(), self.w_events_waiting.keys(), [],
                    timeout
                )

                for fd in rlist:
                    greenlet = self.r_events_waiting.get(fd)
                    greenlet.run()
                    self.r_events_waiting.pop(fd)
                    if greenlet.is_completed():
                        self.remove(greenlet)

                for fd in wlist:
                    greenlet = self.w_events_waiting.get(fd)
                    greenlet.run()
                    self.w_events_waiting.pop(fd)
                    if greenlet.is_completed():
                        self.remove(greenlet)

            for greenlet, seconds in self.sleep_events_waiting:
                if seconds == timeout:
                    greenlet.run()
                    if greenlet.is_completed():
                        self.remove(greenlet)

            if len(self.greenlets) == 0:
                break

    def add_read_event(self, greenlet, fd):
        """[summary]

        Args:
            greenlet (Greenlet): [description]
            fds (fd or list of fd): [description]
        """
        self.r_events_waiting[fd] = greenlet
        self.greenlets.append(greenlet)

    def add_write_event(self, greenlet, fd):
        """[summary]

        Args:
            greenlet (Greenlet): [description]
            fds (fd or list of fd): [description]
        """
        self.w_events_waiting[fd] = greenlet
        self.greenlets.append(greenlet)

    def add_sleep_event(self, greenlet, seconds):
        """[summary]

        Args:
            greenlet (Greenlet): [description]
            fds (fd or list of fd): [description]
        """
        self.sleep_events_waiting[greenlet] = seconds
        self.greenlets.append(greenlet)
