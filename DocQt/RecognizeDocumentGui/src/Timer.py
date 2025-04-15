import time

class Timer:

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.end_time = time.time()
        return self.stop_timer - self.start_timer