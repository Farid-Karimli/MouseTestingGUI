import time

class Timer(object):
    def __init__(self):
        self.start_time = 0
        self.end = 0
        self.elapsed_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def pause(self):
        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False

    def continue_timer(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
    
    def stop(self):
        if self.is_running:
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False
        total_time = self.elapsed_time
        self.elapsed_time = 0  # Reset the timer
        return total_time
    
    def get_elapsed(self):
        if self.is_running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time