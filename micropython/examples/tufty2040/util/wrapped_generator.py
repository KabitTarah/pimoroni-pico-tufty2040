import time


class WrappedGenerator:
    def __init__(self, iterable):
        self.iterable = iterable
        self.generator = iter(iterable)
        
    def next(self):
        try:
            val = next(self.generator)
        except:
            self.generator = iter(self.iterable)
            val = next(self.generator)
        return val


class WrappedGeneratorTimer(WrappedGenerator):
    def __init__(self, iterable, duration_seconds):
        super().__init__(iterable)
        self.duration = duration_seconds
        self.last_time = time.time()
        self.current = None
        
    def next(self):
        now = time.time()
        val = self.current
        if (now - self.last_time > self.duration) or val is None:
            self.last_time = now
            val = super().next()
            self.current = val
        return val

