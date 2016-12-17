__author__ = 'Peter Hofmann'

import os
import sys
import zlib
import gzip
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


# #######################################
# ###  META
# #######################################

class Meta(DefaultLogging):

	_file_name = "meta.smbpm"

	_tag_type = {
		1: "Finish",
		2: "SegManager",
		3: "Docking"
	}

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "Meta"
		super(Meta, self).__init__(logfile, verbose, debug)
		self.version = 0
		self.root_tag = None
		self.is_compressed = False
		self.blueprints = {}
		self.tail_data = ""
		return

	# #######################################
	# ###  Read
	# #######################################

	def _read_dock_entry(self, input_stream):
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
		data["orientation"] = input_stream.read_char()
		return name, data

	def _read_docked_blueprints(self, input_stream):
		"""

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: dict
		"""
		data = {}
		num_docked = input_stream.read_int32_unassigned()
		self._logger.debug("docked_blueprints num_docked: '{}'".format(num_docked))
		assert 0 <= num_docked < 1000, num_docked  # debug sanity check
		for index in range(0, num_docked):
			name, dock_entry = self._read_dock_entry(input_stream)
			self._logger.debug("docked_blueprints docked: '{}': {}".format(name, dock_entry))
			assert name not in data
			data[name] = dock_entry
		return data

	def _read_tag(self, input_stream):
		"""
		# 0x0 - End of tag struct marker -- no tag name or data follows this
		# 0xD - Start of new tag struct
		# 0xE - Serialized object (not yet implemented here)
		# Finish = 1,
		# SegManager = 2,
		# Docking = 3

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: dict
		"""
		assert isinstance(input_stream, ByteStream)
		entry = dict()
		entry["type"] = abs(input_stream.read_char())
		if entry["type"] > 0:
			entry["name"] = input_stream.read_string()
		if entry["type"] != 0:
			entry["payload"] = self._read_payload(input_stream, entry["type"])
		return entry

	# TagList
	def _read_payload_list(self, input_stream):
		"""

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: dict
		"""
		assert isinstance(input_stream, ByteStream)
		entry = dict()
		entry["type"] = input_stream.read_char()
		length_list = input_stream.read_int32_unassigned()
		entry["payload"] = {}
		for index in range(0, length_list):
			entry["payload"][index] = self._read_payload(input_stream, entry["type"])
		return entry

	# TagStructure
	def _read_tag_list(self, input_stream):
		"""

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: dict
		"""
		data = {}
		count = 0
		while True:
			tag = self._read_tag(input_stream)
			self._logger.debug("tag_list tag: '{}'".format(tag))
			if tag["type"] == 0:
				break
			data[count] = tag
			count += 1
		return data

	def _read_payload(self, input_stream, data_type):
		"""

		@param input_stream:
		@type input_stream: ByteStream
		@param data_type:
		@type data_type: int

		@return:
		@rtype: any
		"""
		self._logger.debug("payload data_type: '{}'".format(data_type))
		if data_type == 0:
			return None
		elif data_type == 1:  # Byte
			return input_stream.read_char()
		elif data_type == 2:  # Short
			return input_stream.read_int16()
		elif data_type == 3:  # Int
			return input_stream.read_int32()
		elif data_type == 4:  # Long
			return input_stream.read_int64_unassigned()
		elif data_type == 5:  # Float
			return input_stream.read_float()
		elif data_type == 6:  # Double
			return input_stream.read_double()
		elif data_type == 7:  # Byte array
			return input_stream.read_byte_array()
		elif data_type == 8:  # String
			return input_stream.read_string()  # utf?
		elif data_type == 9:  # Float vector
			return input_stream.read_vector_3_float()
		elif data_type == 10:  # int vector
			return input_stream.read_vector_3_int32()
		elif data_type == 11:  # Byte vector
			return input_stream.read_vector_3_byte()
		elif data_type == 12:  # TagList -> Payload List
			return self._read_payload_list(input_stream)
		elif data_type == 13:  # TagStructure -> Tag list
			return self._read_tag_list(input_stream)
		elif data_type == 14:  # Factory registration # factoryId
			return input_stream.read_char()
		elif data_type == 15:  # Float4 vector
			return input_stream.read_vector_4_float()
		elif data_type == 16:  # Float 4x4 matrix
			return input_stream.read_matrix_4_float()
		elif data_type == 17:  # null
			return None
		else:
			raise Exception("Bad payload data type: {}".format(data_type))
			# return None

	def _read_tag_root(self, input_stream, var1, var2):  # aLt.class
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		version = input_stream.read_int16_unassigned()  # version or tag?
		self._logger.debug("tag_root version: '{}'".format(version))

		input_stream.seek(-2, 1)
		if version == 0x1f8b:  # if(var4[0] == 31 && var4[1] == -117)
			self.is_compressed = True
			self._logger.debug("tag_root compressed data: '{}'".format(self.is_compressed))
			input_stream = ByteStream(gzip.GzipFile(fileobj=input_stream))  # new GZIPInputStream(var15, 4096)
		else:
			self._logger.debug("tag_root compressed data: '{}'".format(self.is_compressed))
			if var2:
				self._logger.debug("tag_root var2: '{}'".format("RECORDING SIZE!!!"))
		tag = self._read_tag(input_stream)
		self._logger.debug("tag_root tag: '{}'".format(tag))
		return version, tag

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

	def _read_datatype_4(self, input_stream):
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		vector_float_0 = input_stream.read_vector_3_float()
		vector_float_1 = input_stream.read_vector_3_float()
		self._logger.debug("datatype_4 vector: '{}', '{}'".format(vector_float_0, vector_float_1))
		unknown_number = 0
		if self.version < 4:
			unknown_number = 8
		if self.version >= 2:
			unknown_string = input_stream.read_string()  # utf
			unknown_int = input_stream.read_int32()
			self._logger.debug("datatype_4 string main: '{}', num d4 data:'{}'".format(unknown_string, unknown_int))
			for _ in range(0, unknown_int):
				self._read_unknown_d4_stuff(input_stream, unknown_number)

		unknown_int1 = input_stream.read_int32()
		unknown_counter = 0
		self._logger.debug("datatype_4 number of byte arrays: '{}'".format(unknown_int1))
		while True:
			if unknown_counter >= unknown_int1:
				return
			unknown_string = input_stream.read_string()  # utf
			# new avt(var15, var1.a);
			byte_array = input_stream.read_byte_array()
			# aLt.a(new FastByteArrayInputStream(var7), true, false); root tag?
			self._logger.debug("datatype_4 length of '{}' byte array: '{}'".format(unknown_string, len(byte_array)))
			unknown_counter += 1

	def _read_datatype_5(self, input_stream):
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		byte_array = input_stream.read_byte_array()
		self._logger.debug("datatype_5 length of byte array: '{}'".format(len(byte_array)))
		# aLt.a(new FastByteArrayInputStream(var7), true, false); root tag?
		return len(byte_array)

	def _read_file(self, input_stream):  # avt.class
		"""
		Read data from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		assert isinstance(input_stream, ByteStream)
		self.version = input_stream.read_int32_unassigned()
		while True:
			data_type = input_stream.read_char()
			self._logger.debug("read_file data_type: {}".format(data_type))
			# input_stream.read(38)
			if data_type == 1:  # Finish
				break
			elif data_type == 2:  # SegManager # aLt.class
				self.root_tag = self._read_tag_root(input_stream, False, False)
				break
			elif data_type == 3:  # Docking
				self.blueprints = self._read_docked_blueprints(input_stream)
			elif data_type == 4:  # Unknown stuff
				self._read_datatype_4(input_stream)
			elif data_type == 5:  # Unknown byte array
				byte_array_length = self._read_datatype_5(input_stream)  # aLt.class
				if byte_array_length > 1:
					break
			else:
				self._logger.debug("read_file unknown data type: {}".format(data_type))
				break
		self.tail_data = input_stream.read()  # any data left?
		self._logger.debug("read_file tail_data: {}".format(len(self.tail_data)))

	def read(self, directory_blueprint):
		"""
		Read data from meta file in blueprint directory

		@param directory_blueprint: input directory
		@type directory_blueprint: str
		"""
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'rb') as input_stream:
			self._read_file(ByteStream(input_stream))

	# #######################################
	# ###  Write
	# #######################################

	@staticmethod
	def _write_dummy(output_stream):
		"""
		Write dummy data to a byte stream
		Until I know how a meta file has to look like, this will have to do

		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		output_stream.write_int32_unassigned(0)  # version
		output_stream.write_char(1)  # data byte 'Finish'

	def write(self, directory_blueprint):
		"""
		Write data to the meta file of a blueprint

		@param directory_blueprint: output directory
		@type directory_blueprint: str
		"""
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'wb') as output_stream:
			self._write_dummy(ByteStream(output_stream))

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream logic values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("####\nMETA v{}\n####\n\n".format(self.version))
		if self._debug:
			output_stream.write("CompressedTag: {}\n\n".format(self.is_compressed))
		if self._debug:
			output_stream.write("Blueprints: {}\n\n".format(len(self.blueprints)))
		for name, blueprint in self.blueprints.iteritems():
			output_stream.write("{}: #{}\n".format(name, blueprint["position"]))
			output_stream.write("\n")
		if self._debug:
			output_stream.write("Tail: {} bytes\n".format(len(self.tail_data)))
		output_stream.write("\n")
