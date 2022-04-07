"""
MCP23017, I2C GPIO expander
connected to a Neokey5x6 (matrix keypad)
"""
from digitalio import DigitalInOut, Pull
from supervisor import ticks_ms

class KeyEvent:
	def __init__(self, key, timestamp, pressed=False, released=False):
		self.key_number = key
		self.timestamp = timestamp
		self.pressed = pressed
		self.released = released

	def __eq__(self, other):
		return (
			self.key_number == other.key_number
			and self.pressed == other.pressed
			and self.released == other.released
		)

	def __hash__(self):
		return (
			self.key_number << 2
			+ int(self.pressed)
			+ int(self.released) * 2
		)

class McpMatrixScanner:
	def __init__(self, mcp, rows, columns, irq=None):
		self.num_cols = len(columns)
		self.columns = columns
		self.rows = rows
		self.mcp = mcp
		self.keys_state = set()
		# note: events are inserted at the start, for ease of pop()
		# (might be optimised with a deque class or something)
		self.queue = []
		# set port A to output (columns)
		mcp.iodira = 0x00
		# set port B to input (rows) all pull ups
		mcp.iodirb = 0xFF
		mcp.gppub = 0xFF
		# set interrupts
		self.irq = None
		if irq:
			self.irq = DigitalInOut(irq)
			self.irq.switch_to_input(Pull.UP)
			mcp.interrupt_enable = 0xFF00
			mcp.default_value = 0xFFFF
			# compare input to default value (1) or previous value (0)
			mcp.interrupt_configuration = 0xFF00
			mcp.io_control = 0x44  # Interrupt as open drain and mirrored
			mcp.clear_ints()

	def _scan_matrix(self):
		"""Scan the matrix and return the list of keys down"""
		pressed = set()
		for scan_column in self.columns:
			# set all outputs to 1 on port A except the scan_column
			self.mcp.gpioa = 0xFF - (1 << scan_column)
			if self.irq is None or not self.irq.value:
				# read the input
				inputs = self.mcp.gpiob
				if inputs:
					# adds (columns,row) if the row is 0 too
					for row in self.rows:
						if (inputs >> row) & 1 == 0:
							pressed.add(scan_column + self.num_cols * row)
		# set back port A to default
		self.mcp.gpioa = 0xFF
		return pressed

	def update_queue(self):
		"""
		Run the scan and create events in the event queue.
		"""
		timing = ticks_ms()
		# scan the matrix, find Neo
		current_state = self._scan_matrix()
		# use set algebra to find released and pressed keys
		released_keys = self.keys_state - current_state
		pressed_keys = current_state - self.keys_state
		# create the events
		queue = []
		for key in released_keys:
			queue.append(KeyEvent(key, timing, released=True))
		for key in pressed_keys:
			queue.append(KeyEvent(key, timing, pressed=True))
		# add in front
		if queue:
			self.queue = queue + self.queue
		# end
		self.keys_state = current_state

	def pop_next_event(self):
		"""
		Return the next event and remove it from the event queue.
		
		Example:
			while event := scanner.pop_next_event():
				print(event.key_number, event.released, event.pressed)
		"""
		if self.queue:
			return self.queue.pop()
		return None

	def key_number_to_row_column(self, key_number: int) -> Tuple[int]:
		"""Convert key number to row, column"""
		row = key_number // self.num_cols
		column = key_number % self.num_cols
		return (row, column)

	def row_column_to_key_number(self, row: int, column: int) -> int:
		"""Convert row, column to key number"""
		return row * self.num_cols + column
