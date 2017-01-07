__author__ = 'Peter Hofmann'

import sys
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class DataType3(DefaultLogging):
	"""
	Reading data type 2 meta data

	@type _docked_entity: dict[str, dict[str, int]]
	"""

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "DataType3"
		super(DataType3, self).__init__(logfile, verbose, debug)
		self._docked_entity = {}
		return

	# #######################################
	# ###  Read
	# #######################################

	@staticmethod
	def _read_dock_entry(input_stream):
		"""

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: str, dict
		"""
		assert isinstance(input_stream, ByteStream)
		data = {}
		name = input_stream.read_string()
		data["position"] = input_stream.read_vector_3_int32()
		data["size"] = input_stream.read_vector_3_float()
		data["style"] = input_stream.read_int16_unassigned()
		data["orientation"] = input_stream.read_byte()
		return name, data

	def read(self, input_stream):
		"""

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: dict
		"""
		num_docked = input_stream.read_int32_unassigned()
		assert 0 <= num_docked < 1000, num_docked  # debug sanity check
		for index in range(0, num_docked):
			name, dock_entry = self._read_dock_entry(input_stream)
			# self._logger.debug("relative path: '{}': {}".format(name, dock_entry))
			assert name not in self._docked_entity
			self._docked_entity[name] = dock_entry

	# #######################################
	# ###  Write
	# #######################################

	@staticmethod
	def _write_dock_entry(output_stream, name, data):
		"""

		@param output_stream:
		@type output_stream: ByteStream

		@return:
		@rtype: str, dict
		"""
		assert isinstance(output_stream, ByteStream)
		output_stream.write_string(name)
		output_stream.write_vector_3_int32(data["position"])
		output_stream.write_vector_3_float(data["size"])
		output_stream.write_int16_unassigned(data["style"])
		output_stream.write_byte(data["orientation"])

	def write(self, output_stream):
		"""
		write values

		@param output_stream: Output stream
		@type output_stream: ByteStream
		"""
		self._logger.debug("Writing")
		output_stream.write_byte(3)
		output_stream.write_int32_unassigned(len(self._docked_entity))
		for name in self._docked_entity.keys():
			self._write_dock_entry(output_stream, name, self._docked_entity[name])

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("DataType3: {}\n".format(len(self._docked_entity)))
		if self._debug:
			for name in self._docked_entity.keys():
				data = self._docked_entity[name]
				output_stream.write("{}:\t".format(name))
				output_stream.write("Position: {}\tSize: {}\t Style {}\t Orientation: {}\n".format(
					data["position"], data["size"], data["style"], data["orientation"]))
		output_stream.write("\n")
