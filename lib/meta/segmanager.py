__author__ = 'Peter Hofmann'

import sys
import gzip
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class SegManager(DefaultLogging):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "Meta-DataType2"
		super(SegManager, self).__init__(logfile, verbose, debug)
		self.is_compressed = False
		self.root_tag = None
		self.version = 0
		return

	# #######################################
	# ###  Read
	# #######################################

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
		entry["type"] = abs(input_stream.read_byte())
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
		entry["type"] = input_stream.read_byte()
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
			return input_stream.read_byte()
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
			return input_stream.read_byte()
		elif data_type == 15:  # Float4 vector
			return input_stream.read_vector_4_float()
		elif data_type == 16:  # Float 4x4 matrix
			return input_stream.read_matrix_4_float()
		elif data_type == 17:  # null
			return None
		else:
			raise Exception("Bad payload data type: {}".format(data_type))
			# return None

	def read(self, input_stream, var1, var2):  # aLt.class
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		self.version = input_stream.read_int16_unassigned()  # version or tag?
		self._logger.debug("tag_root version: '{}'".format(self.version))

		input_stream.seek(-2, 1)
		if self.version == 0x1f8b:  # if(var4[0] == 31 && var4[1] == -117)
			self.is_compressed = True
			self._logger.debug("tag_root compressed data: '{}'".format(self.is_compressed))
			input_stream = ByteStream(gzip.GzipFile(fileobj=input_stream))  # new GZIPInputStream(var15, 4096)
		else:
			self._logger.debug("tag_root compressed data: '{}'".format(self.is_compressed))
			if var2:
				self._logger.debug("tag_root var2: '{}'".format("RECORDING SIZE!!!"))
		self.root_tag = self._read_tag(input_stream)
		self._logger.debug("tag_root tag: '{}'".format(self.root_tag))

	# #######################################
	# ###  Write
	# #######################################

	def write(self, output_stream):
		"""
		write values

		@param output_stream: Output stream
		@type output_stream: ByteStream
		"""
		if self.root_tag is None:
			return
		raise NotImplementedError("segmanager write is not implemented, yet.")
		# output_stream.write_byte(2)

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("{} v{}\n".format(self._label, self.version))
		if self._debug:
			output_stream.write("CompressedTag: {}\n\n".format(self.is_compressed))
		output_stream.write("\n")
