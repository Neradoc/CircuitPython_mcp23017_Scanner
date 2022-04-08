from supervisor import ticks_ms

class Profiler:
	def __init__(self, sample_size=5):
		self.samples = sample_size
		self.times = [0] * sample_size
		self.index_times = 0
		self.t0 = 0
		self.t1 = 0
		self.newline = False

	def start(self):
		self.t0 = ticks_ms()

	def profile(self, newline=False):
		self.t1 = ticks_ms()
		self.times[self.index_times % self.samples] = self.t1 - self.t0
		self.index_times += 1
		average = (
			sum(self.times[:self.index_times+1])
			/ min(self.index_times, self.samples)
		)
		print(f"Average scan time: {average:8.2f}     ", end = "\r")
		if bool(newline): print("")

	def __enter__(self):
		self.t0 = ticks_ms()
		return self

	def __exit__(self, type, value, traceback):
		self.profile(self.newline)
