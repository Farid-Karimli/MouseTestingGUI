import time

class Timer(object):
    def __init__(self):
        self.start_time = 0
        self.end = 0

    def start(self):
        self.start_time = time.time()

    def checkpoint(self):
        self.end = time.time()
        duration = self.end - self.start_time
        self.start_time = self.end
        return duration