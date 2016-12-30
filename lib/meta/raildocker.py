__author__ = 'Peter Hofmann'

import sys
import os
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class RailDocker(DefaultLogging):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "Meta-DataType4"
		super(RailDocker, self).__init__(logfile, verbose, debug)
		self._vector_float_0 = (0, 0, 0)
		self._vector_float_1 = (0, 0, 0)
		self._entity_label = ""
		self._entity_unknown_list_of_tuple = {}
		self._docked_entity = {}
		return

	# #######################################
	# ###  Read
	# #######################################

	@staticmethod
	def get_index(var0, var1, var2):
		"""

		@param var0:
		@param var0: long
		@param var1:
		@param var1: long
		@param var2:
		@param var2: long

		@return:
		@rtype: int
		"""
		return long((var2 & unicode('ffff')) << 32) + long((var1 & unicode('ffff')) << 16) + long(var0 & unicode('ffff'))

	@staticmethod
	def get_pos(var0, shift=0):
		"""

		@param var0:
		@param var0: long
		@return:
		@rtype: int
		"""
		if shift == 0:
			return int(var0 & 65535L)
		return int(var0 >> shift & 65535L)

	def shift_index(self, var0, var2, var3, var4):
		"""

		@param var0:
		@param var2:
		@param var3:
		@param var4:

		@return:
		@rtype: long
		"""
		return self.get_index(self.get_pos(var0) + var2, self.get_pos(var0, 16) + var3, self.get_pos(var0, 32) + var4)

	def _read_unknown_d4_stuff(self, input_stream, unknown_number):
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		unknown_string = input_stream.read_string()  # utf
		self._logger.debug("unknown_d4_stuff string: '{}'".format(unknown_string))
		unknown_long0 = input_stream.read_int64()
		unknown_long1 = input_stream.read_int64()
		if unknown_number != 0:
			unknown_long0 = self.shift_index(unknown_long0, unknown_number, unknown_number, unknown_number)
			unknown_long1 = self.shift_index(unknown_long1, unknown_number, unknown_number, unknown_number)
		return unknown_long0, unknown_long1

	def read(self, input_stream, version):
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		self._vector_float_0 = input_stream.read_vector_3_float()
		self._vector_float_1 = input_stream.read_vector_3_float()
		unknown_number = 0
		if version < (0, 0, 0, 4):
			unknown_number = 8
		if version >= (0, 0, 0, 2):
			self._entity_label = input_stream.read_string()  # utf
			list_size_of_unknown_stuff = input_stream.read_int32()
			assert list_size_of_unknown_stuff < 10000
			assert list_size_of_unknown_stuff == 0, "Unknown data there that I do not know how to save"
			self._entity_unknown_list_of_tuple = {}
			for some_index in range(0, list_size_of_unknown_stuff):
				self._entity_unknown_list_of_tuple[some_index] = self._read_unknown_d4_stuff(input_stream, unknown_number)

		self._docked_entity = {}
		amount_of_docked_entities = input_stream.read_int32()
		for turret_index in range(amount_of_docked_entities):
			relative_path = input_stream.read_string()  # utf
			_, dock_index = relative_path.rsplit('_', 1)
			# new avt(var15, var1.a);
			byte_array = input_stream.read_byte_array()
			# aLt.a(new FastByteArrayInputStream(var7), true, false); root tag?
			self._docked_entity[int(dock_index)] = byte_array
			self._logger.debug("Length of '{}' byte array: '{}'".format(relative_path, len(byte_array)))

	# #######################################
	# ###  Write
	# #######################################

	def write(self, output_stream, version, relative_path):
		"""
		write values

		@param output_stream: Output stream
		@type output_stream: ByteStream
		"""
		self._logger.debug("Writing")
		output_stream.write_byte(4)

		output_stream.write_vector_3_float(self._vector_float_0)
		output_stream.write_vector_3_float(self._vector_float_1)

		unknown_number = 0
		if version < (0, 0, 0, 4):
			unknown_number = 8
		if version >= (0, 0, 0, 2):
			output_stream.write_string(self._entity_label)
			output_stream.write_int32_unassigned(len(self._entity_unknown_list_of_tuple))
			for _ in sorted(self._entity_unknown_list_of_tuple.keys()):
				unknown_number = unknown_number
				raise NotImplementedError("Docking write is not fully implemented, yet.")

		output_stream.write_int32_unassigned(len(self._docked_entity))
		for dock_index in sorted(self._docked_entity.keys()):
			new_relative_directory = os.path.join(relative_path, "ATTACHED_{}".format(dock_index))
			self._logger.debug(new_relative_directory)
			output_stream.write_string(new_relative_directory)
			output_stream.write_byte_array(self._docked_entity[dock_index])

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream logic values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("Label: '{}'\t".format(self._entity_label))
		output_stream.write("Vector: '{}', '{}'\n".format(self._vector_float_0, self._vector_float_1))
		if self._debug:
			output_stream.write("unknown tuple: {}\n".format(len(self._entity_unknown_list_of_tuple)))

		output_stream.write("RailDocker: {}\n".format(len(self._docked_entity)))
		if self._debug:
			for dock_index in sorted(self._docked_entity.keys()):
				data_size = len(self._docked_entity[dock_index])
				output_stream.write("{}: #{}\n".format(dock_index, data_size))
		output_stream.write("\n")
