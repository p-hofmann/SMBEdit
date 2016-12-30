__author__ = 'Peter Hofmann'

import sys
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class Docking(DefaultLogging):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "Meta-DataType3"
		super(Docking, self).__init__(logfile, verbose, debug)
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
		# string_length = self._read_int_unassigned(input_stream)
		# entry["name"] = input_stream.read(string_length).decode('utf-8')
		name = input_stream.read_string()
		data["position"] = input_stream.read_vector_3_int16()
		data["size"] = input_stream.read_vector_3_int32()
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
		self._logger.debug("docked_blueprints num_docked: '{}'".format(num_docked))
		assert 0 <= num_docked < 1000, num_docked  # debug sanity check
		for index in range(0, num_docked):
			name, dock_entry = self._read_dock_entry(input_stream)
			self._logger.debug("docked_blueprints docked: '{}': {}".format(name, dock_entry))
			assert name not in self._docked_entity
			self._docked_entity[name] = dock_entry

	# #######################################
	# ###  Write
	# #######################################

	def write(self, output_stream):
		"""
		write values

		@param output_stream: Output stream
		@type output_stream: ByteStream
		"""
		self._logger.debug("Writing")
		output_stream.write_byte(3)
		output_stream.write_int32_unassigned(len(self._docked_entity))
		for _ in self._docked_entity:
			raise NotImplementedError("Docking write is not implemented, yet.")

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream logic values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("Docked: {}\n".format(len(self._docked_entity)))
		if self._debug:
			for relative_dir in self._docked_entity.keys():
				data = len(self._docked_entity[relative_dir])
				output_stream.write("{}: #{}\n".format(relative_dir, data))
		output_stream.write("\n")
