import pyvisa
from device_controller.prologix_connection import PrologixConnection
from enum import Enum

class ConnectionType(Enum):
	GPIB_connection = 1
	prologix_connection = 2

class GPIBDeviceConnection:
	def __init__(self, port):
		self.port = port
		try : 
			self.device_id = int(port.split('::')[1])
		except :
			raise Exception("Invalid Device Identifier. Try GPIB0::<number>::INSTR")

		try :
			self.connection = pyvisa.ResourceManager().open_resource(self.port)
			self.connection_type = ConnectionType.GPIB_connection
		except pyvisa.VisaIOError:
			self.connection = PrologixConnection(self.device_id)
			self.connection_type = ConnectionType.prologix_connection

	def open(self):
		self.connection.open()
	def close(self):
		self.connection.close()
	def __enter__(self):
		self.connection.__enter__()
		return self
	def __exit__(self, *args):
		self.connection.__exit__(*args)
	def query(self, command):
		return self.connection.query(command)
	def write(self, command):
		return self.connection.write(command)
	def read(self):
		return self.connection.read()

	def read_raw(self, *args):
		if self.connection_type == ConnectionType.GPIB_connection:
			return self.connection.read_raw(*args)
		elif self.connection_type == ConnectionType.prologix_connection:
			return self.read()
	def write_raw(self, *args):
		if self.connection_type == ConnectionType.GPIB_connection:
			return self.connection.write_raw(*args)
		elif self.connection_type == ConnectionType.prologix_connection:
			return self.write(*args)
	





