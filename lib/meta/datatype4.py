__author__ = 'Peter Hofmann'

import sys
import os
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging
from lib.meta.tagmanager import TagManager


class DataType4(DefaultLogging):
	"""
	Reading data type 4 meta data

	@type _vector_float_0: tuple[float]
	@type _vector_float_1: tuple[float]
	@type _entity_label: str
	@type _entity_unknown_list_of_tuple: dict[list]
	@type _docked_entity: dict[int,TagManager]
	"""

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "DataType4"
		super(DataType4, self).__init__(logfile, verbose, debug)
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
		@type var0: long
		@param var1:
		@type var1: long
		@param var2:
		@type var2: long

		@return:
		@rtype: int
		"""
		return long((var2 & unicode('ffff')) << 32) + long((var1 & unicode('ffff')) << 16) + long(var0 & unicode('ffff'))

	@staticmethod
	def get_pos(var0, shift=0):
		"""

		@param var0:
		@type var0: long

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
		Read unknown stuff from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		unknown_string = input_stream.read_string()  # utf
		unknown_long0 = input_stream.read_int64()
		unknown_long1 = input_stream.read_int64()
		self._logger.debug("unknown_d4_stuff string: '{}'".format(unknown_string))
		# if unknown_number != 0:
		# 	unknown_long0 = self.shift_index(unknown_long0, unknown_number, unknown_number, unknown_number)
		# 	unknown_long1 = self.shift_index(unknown_long1, unknown_number, unknown_number, unknown_number)
		return [unknown_string, unknown_long0, unknown_long1]

	def read(self, input_stream, version):
		"""
		Read rail docker data?

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
			self._entity_unknown_list_of_tuple = {}
			if list_size_of_unknown_stuff > 0:
				self._logger.warning("Reading unknown stuff.")
			for some_index in range(list_size_of_unknown_stuff):
				self._entity_unknown_list_of_tuple[some_index] = self._read_unknown_d4_stuff(input_stream, unknown_number)

		self._docked_entity = {}
		amount_of_docked_entities = input_stream.read_int32()
		for turret_index in range(amount_of_docked_entities):
			relative_path = input_stream.read_string()  # utf
			_, dock_index = relative_path.rsplit('_', 1)
			tag_size = input_stream.read_int32_unassigned()
			if tag_size > 0:
				self._docked_entity[int(dock_index)] = TagManager(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
				self._docked_entity[int(dock_index)].read(input_stream)

	# #######################################
	# ###  Write
	# #######################################

	@staticmethod
	def _write_unknown_d4_stuff(output_stream, stuff, unknown_number):
		"""
		Write some stuff to byte stream

		@param output_stream: output_stream
		@type output_stream: ByteStream
		"""
		# if unknown_number != 0:
		# 	unknown_long0 = self.shift_index(unknown_long0, unknown_number, unknown_number, unknown_number)
		# 	unknown_long1 = self.shift_index(unknown_long1, unknown_number, unknown_number, unknown_number)
		output_stream.write_string(stuff[0])  # utf
		output_stream.write_int64(stuff[1])
		output_stream.write_int64(stuff[2])

	def write(self, output_stream, version, relative_path, compressed=False):
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
			list_size_of_unknown_stuff = len(self._entity_unknown_list_of_tuple)
			output_stream.write_int32_unassigned(list_size_of_unknown_stuff)
			if list_size_of_unknown_stuff > 0:
				self._logger.warning("Writing unknown stuff.")
			for index in sorted(self._entity_unknown_list_of_tuple.keys()):
				self._write_unknown_d4_stuff(output_stream, self._entity_unknown_list_of_tuple[index], unknown_number)

		output_stream.write_int32_unassigned(len(self._docked_entity))
		for dock_index in sorted(self._docked_entity.keys()):
			new_relative_directory = os.path.join(relative_path, "ATTACHED_{}".format(dock_index))
			self._logger.debug(new_relative_directory)
			output_stream.write_string(new_relative_directory)
			tag_size = self._docked_entity[dock_index].get_size(compressed)
			output_stream.write_int32_unassigned(tag_size)
			self._docked_entity[dock_index].write(output_stream, compressed)
			# output_stream.write_byte_array(self._docked_entity[dock_index])

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream logic values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("DataType4: {}\n".format(len(self._docked_entity)))
		output_stream.write("Label: '{}'\t".format(self._entity_label))
		output_stream.write("Vector: '{}', '{}'\n".format(self._vector_float_0, self._vector_float_1))
		list_size_of_unknown_stuff = len(self._entity_unknown_list_of_tuple)
		if self._debug and list_size_of_unknown_stuff > 0:
			output_stream.write("unknown tuple: #{}\n".format(len(self._entity_unknown_list_of_tuple)))

		if self._debug:
			for dock_index in sorted(self._docked_entity.keys()):
				self._docked_entity[dock_index].to_stream(output_stream)
		output_stream.write("\n")
