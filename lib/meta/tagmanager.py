__author__ = 'Peter Hofmann'

import sys
# import gzip
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class TagUtil(object):

	@staticmethod
	def _data_to_stream(data, output_stream=sys.stdout):
		if isinstance(data, (TagPayload, TagList, TagPayloadList)):
			data.to_stream(output_stream)
		else:
			output_stream.write("{}, ".format(data))


class TagList(object):
	"""

	@type tag_list: list[TagPayload]
	"""

	def __init__(self, tag_list):
		self.tag_list = tag_list

	def to_stream(self, output_stream=sys.stdout):
		output_stream.write(" {")
		for tag in self.tag_list:
			tag.to_stream(output_stream)
		output_stream.write("} ")


class TagPayloadList(TagUtil):
	"""

	@type id: int
	@type payload_list: list[any]
	"""

	def __init__(self, identifier, payload_list):
		self.id = identifier
		self.payload_list = payload_list

	def to_stream(self, output_stream=sys.stdout):
		output_stream.write("{}: [".format(self.id))
		for payload in self.payload_list:
			self._data_to_stream(payload, output_stream)
			output_stream.write("\t")
		output_stream.write("] ".format(self.id))


class TagPayload(TagUtil):
	"""

	@type id: int
	@type name: str | None
	@type payload: any
	"""

	def __init__(self, identifier, name, payload):
		self.id = identifier
		self.name = name
		self.payload = payload

	def to_stream(self, output_stream=sys.stdout):
		output_stream.write("{}: ".format(self.id))
		self._data_to_stream(self.payload, output_stream)
		# output_stream.write("\n")


class TagManager(DefaultLogging):
	"""
	Reading tag structures

	@type _is_compressed: bool
	@type _root_tag: TagPayload
	@type _version: tuple[int]
	@type _tail_data: str
	"""

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "TagManager"
		super(TagManager, self).__init__(logfile, verbose, debug)
		self._is_compressed = False
		self._root_tag = None
		self._version = (0, 0)
		self._tail_data = ""
		return

	# #######################################
	# ###  Read
	# #######################################

	def _read_tag_payload(self, input_stream):
		"""

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: TagPayload
		"""
		assert isinstance(input_stream, ByteStream)
		identifier = input_stream.read_byte()
		name = None
		payload = None
		if identifier != 0:
			if identifier > 0:
				name = input_stream.read_string()
			payload = self._read_payload(input_stream, abs(identifier))
		return TagPayload(identifier, name, payload)

	def _read_tag_payload_list(self, input_stream):
		"""
		Read list of data from the same tag type

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: TagPayloadList
		"""
		assert isinstance(input_stream, ByteStream)
		identifier = input_stream.read_byte()
		length_list = input_stream.read_int32_unassigned()
		payload_list = []
		for index in range(0, length_list):
			payload_list.append(self._read_payload(input_stream, abs(identifier)))
		return TagPayloadList(identifier, payload_list)

	def _read_tag_list(self, input_stream):
		"""
		Read a list of tags

		@param input_stream:
		@type input_stream: ByteStream

		@return:
		@rtype: TagList
		"""
		data = []
		while True:
			tag = self._read_tag_payload(input_stream)
			# self._logger.debug("tag_list tag: '{}'".format(tag))
			if tag.id == 0:
				break
			data.append(tag)
		return TagList(data)

	def _read_payload(self, input_stream, data_type):
		"""

		@param input_stream:
		@type input_stream: ByteStream
		@param data_type:
		@type data_type: int

		@return:
		@rtype: any
		"""
		# self._logger.debug("payload data_type: '{}'".format(data_type))
		if data_type == 0:
			return None
		elif data_type == 1:  # Byte
			return input_stream.read_byte()
		elif data_type == 2:  # Short
			return input_stream.read_int16()
		elif data_type == 3:  # Int
			return input_stream.read_int32()
		elif data_type == 4:  # Long
			return input_stream.read_int64()
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
			return self._read_tag_payload_list(input_stream)
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

	def read(self, input_stream):  # aLt.class
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		self._version = input_stream.read_vector_x_byte(2)  # version or tag?

		# if self.version == 0x1f8b:
		if self._version[0] == 31 and self._version[1] == -117:
			input_stream.seek(-2, 1)
			self._is_compressed = True
			raise NotImplementedError("not fully implemented, yet.")
			# input_stream = ByteStream(gzip.GzipFile(fileobj=input_stream))  # new GZIPInputStream(var15, 4096)
		# else:
		self._root_tag = self._read_tag_payload(input_stream)
		# self._tail_data = input_stream.read()

	# #######################################
	# ###  Write
	# #######################################

	def write(self, output_stream, compressed=False):
		"""
		write values

		@param output_stream: Output stream
		@type output_stream: ByteStream
		"""
		if self._root_tag is None:
			return
		raise NotImplementedError("segmanager write is not implemented, yet.")
		# output_stream.write_byte(2)

	# #######################################
	# ###  Else
	# #######################################

	def get_size(self, compressed=False):
		if not self.has_data():
			return 0
		raise NotImplementedError("not fully implemented, yet.")

	def has_data(self):
		return self._root_tag is not None

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		if not self.has_data:
			return
		output_stream.write("{} v{} gzip: {}\n".format(self._label, self._version, self._is_compressed))
		if self._debug:
			if len(self._tail_data) > 0:
				output_stream.write("Tail data: {}\n".format(len(self._tail_data)))
			self._root_tag.to_stream()
		output_stream.write("\n")
