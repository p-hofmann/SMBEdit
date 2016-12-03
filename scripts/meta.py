__author__ = 'Peter Hofmann'

import os
import sys
import zlib
import struct
import gzip
from bit_and_bytes import ByteStream


# #######################################
# ###  META
# #######################################

class Meta(object):

	_file_name = "meta.smbpm"

	_tag_type = {
		1: "Finish",
		2: "SegManager",
		3: "Docking"
	}

	def __init__(self):
		super(Meta, self).__init__()
		self.version = ""
		self.root_tag = None
		self.is_compressed = False
		self.blueprints = {}
		self.tail_data = ""
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
		print name
		data["position"] = input_stream.read_vector_3_int16()
		print data["position"]
		data["size"] = input_stream.read_vector_3_int32()
		print data["size"]
		data["style"] = input_stream.read_int16_unassigned()
		print data["style"]
		data["orientation"] = input_stream.read_char()
		print data["orientation"]
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
		print "Docked", num_docked
		assert 0 <= num_docked < 1000, num_docked  # debug sanity check
		for index in range(0, num_docked):
			name, dock_entry = self._read_dock_entry(input_stream)
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
		entry["type"] = input_stream.read_char()
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
			return input_stream.read_string()
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
		else:
			return None

	def _read_tag_root(self, input_stream):
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		version = input_stream.read_int16_unassigned()
		if version == 0x1f8b:
			self.is_compressed = True
			print "compressed file"
		input_stream = gzip.GzipFile(fileobj=input_stream)
		tag = self._read_tag(input_stream)
		return version, tag

	def _read_file(self, input_stream):
		"""
		Read data from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		assert isinstance(input_stream, ByteStream)
		self.version = input_stream.read_int32_unassigned()
		while True:
			data_type = input_stream.read_char()
			print "data_type", data_type  # debug
			# input_stream.read(38)
			if data_type == 1:  # Finish
				break
			elif data_type == 2:  # SegManager
				self.root_tag = self._read_tag_root(input_stream)
			elif data_type == 4:  # Unknown stuff
				pass
			elif data_type == 3:  # Docking
				self.blueprints = self._read_docked_blueprints(input_stream)
			else:
				print "unknown data type {}".format(data_type)
				break
		self.tail_data = input_stream.read()  # any data left?

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

	def to_stream(self, output_stream=sys.stdout, summary=True):
		"""
		Stream logic values

		@param output_stream: Output stream
		@type output_stream: fileIO
		@param summary: If true the output is reduced
		@type summary: bool
		"""
		output_stream.write("####\nMETA ({})\n####\n\n".format(self.version))
		output_stream.write("CompressedTag: {}\n\n".format(self.is_compressed))
		output_stream.write("Blueprints: {}\n\n".format(len(self.blueprints)))
		for name, blueprint in self.blueprints.iteritems():
			output_stream.write("{}: #{}\n".format(name, blueprint["position"]))
			output_stream.write("\n")
		output_stream.write("Tail: {} bytes\n".format(len(self.tail_data)))
		output_stream.write("\n")
