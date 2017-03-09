import time
import datetime


class allsparkStopwatch(object):
    def __init__(self, **kwargs):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def duration(self):
        time_taken = self.end_time - self.start_time
        time_diff = datetime.timedelta(seconds=time_taken)
        return time_diff

    def split(self):
        temp_end_time = time.time()
        time_taken = temp_end_time - self.start_time
        return datetime.timedelta(seconds=time_taken)
