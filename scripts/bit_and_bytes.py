__author__ = 'Peter Hofmann'

import struct


class ByteStream(object):
	"""
	Class idea based on:
	http://stackoverflow.com/questions/442188/readint-readbyte-readstring-etc-in-python/4338551#4338551

	Notes:
	@ 	native 	native 	native
	= 	native 	standard 	none
	< 	little-endian 	standard 	none
	> 	big-endian 	standard 	none
	! 	network (= big-endian) 	standard 	none

	x 	pad byte        	no value
	c 	char            	string of length 1 	1
	b 	signed char     	integer 	1 	(3)
	B 	unsigned char     	integer 	1 	(3)
	? 	_Bool           	bool    	1 	(1)
	h 	short           	integer 	2 	(3)
	H 	unsigned short  	integer 	2 	(3)
	i 	int             	integer 	4 	(3)
	I 	unsigned int     	integer 	4 	(3)
	l 	long            	integer 	4 	(3)
	L 	unsigned long     	integer 	4 	(3)
	q 	long long       	integer 	8 	(2), (3)
	Q 	unsigned long long 	integer 	8 	(2), (3)
	f 	float           	float   	4 	(4)
	d 	double          	float   	8 	(4)
	s 	char[]          	string
	p 	char[]          	string
	P 	void *          	integer 	  	(5), (3)
	"""

	def __init__(self, bytestream, byte_order=">"):
		"""

		@param bytestream:
		@type bytestream: FileIO
		@param byte_order:
		@type byte_order: str
		"""
		self._bytestream = bytestream
		self._byte_order = byte_order
		return

	def __exit__(self, type, value, traceback):
		self._bytestream = None
		return

	def __enter__(self):
		return self

	# #######################################
	# ###  Packing and unpacking
	# #######################################

	def pack(self, value, data_type):
		"""
		Pack value to byte string

		@param value: value to be packed
		@type value: any
		@param data_type: datatype
		@type data_type: str

		@return: byte string
		@rtype: str
		"""
		return struct.pack("{order}{type}".format(
			order=self._byte_order,
			type=data_type), value)

	def _pack(self, value, data_type, padded=False):
		byte_string = self.pack(value, data_type)
		if not padded:
			self._bytestream.write(byte_string)
		if self._byte_order == '>' or self._byte_order == '!':
			self._bytestream.write(byte_string[1:])
		self._bytestream.write(byte_string[:-1])  # todo: check if this is right

	def unpack(self, byte_string, data_type):
		"""
		Pack value to byte string

		@param byte_string: value to be packed
		@type byte_string: str
		@param data_type: datatype
		@type data_type: str

		@return: depends on data_type
		@rtype: any
		"""
		return struct.unpack("{order}{type}".format(
			order=self._byte_order,
			type=data_type), byte_string)[0]

	def _unpack(self, length, data_type, padding=""):
		if self._byte_order == '>' or self._byte_order == '!':
			return self.unpack(padding + self._bytestream.read(length), data_type)
		return self.unpack(self._bytestream.read(length) + padding, data_type)

	# #######################################
	# ###  Reading bytes
	# #######################################

	def read(self):
		return self._bytestream.read()

	def read_bool(self):
		return self._unpack(1, '?')

	def read_char(self):
		return self._unpack(1, 'b')

	def read_int16(self):
		return self._unpack(2, 'h')

	def read_int16_unassigned(self):
		return self._unpack(2, 'H')

	def read_int24(self):
		return self._unpack(3, 'i', '\x00')

	def read_int24_unassigned(self):
		return self._unpack(3, 'I', '\x00')

	def read_int32(self):
		return self._unpack(4, 'i')

	def read_int32_unassigned(self):
		return self._unpack(4, 'I')

	def read_float(self):
		return self._unpack(4, 'f')

	def read_double(self):
		return self._unpack(8, 'd')

	def read_int64(self):
		return self._unpack(8, 'q')

	def read_int64_unassigned(self):
		return self._unpack(8, 'Q')

	def read_string(self):
		length = self.read_int16_unassigned()
		# return struct.unpack(str(length) + 's', self._bytestream.read(length))[0]
		return self._unpack(length, str(length) + 's')

	def read_byte_array(self):
		array = []
		length = self.read_int32_unassigned()
		for index in range(0, length):
			array.append(self.read_char())
		return array

	def read_vector_3_int16(self):
		vector = [
			self.read_int16(),
			self.read_int16(),
			self.read_int16(),
			]
		return tuple(vector)

	def read_vector_3_int32(self):
		vector = [
			self.read_int32(),
			self.read_int32(),
			self.read_int32(),
			]
		return tuple(vector)

	def read_vector_3_float(self):
		vector = [
			self.read_float(),
			self.read_float(),
			self.read_float(),
			]
		return tuple(vector)

	def read_vector_4_float(self):
		vector = [
			self.read_float(),
			self.read_float(),
			self.read_float(),
			self.read_float(),
			]
		return tuple(vector)

	def read_vector_3_byte(self):
		vector = [
			self.read_char(),
			self.read_char(),
			self.read_char(),
			]
		return tuple(vector)

	# #######################################
	# ###  Writing bytes
	# #######################################

	def write(self, value):
		self._bytestream.write(value)

	def write_bool(self, value):
		self._pack(value, '?')

	def write_char(self, value):
		self._pack(value, 'b')

	def write_int16(self, value):
		self._pack(value, 'h')

	def write_int16_unassigned(self, value):
		self._pack(value, 'H')

	def write_int24(self, value):
		self._pack(value, 'i', padded=True)

	def write_int24_unassigned(self, value):
		self._pack(value, 'I', padded=True)

	def write_int32(self, value):
		self._pack(value, 'i')

	def write_int32_unassigned(self, value):
		self._pack(value, 'I')

	def write_int64(self, value):
		self._pack(value, 'q')

	def write_int64_unassigned(self, value):
		self._pack(value, 'Q')

	def write_float(self, value):
		self._pack(value, 'f')

	def write_double(self, value):
		self._pack(value, 'd')

	def write_string(self, value):
		length = len(value)
		self.write_int16_unassigned(length)
		self._pack(value, str(length) + 's')

	def write_byte_array(self, byte_array):
		length = len(byte_array)
		self.write_int32_unassigned(length)
		for byte in byte_array:
			self.write_char(byte)

	def write_vector_3_int16(self, values):
		self.write_int16(values[0]),
		self.write_int16(values[1]),
		self.write_int16(values[2]),

	def write_vector_3_int32(self, values):
		self.write_int32(values[0]),
		self.write_int32(values[1]),
		self.write_int32(values[2]),

	def write_vector_3_float(self, values):
		self.write_float(values[0]),
		self.write_float(values[1]),
		self.write_float(values[2]),

	def write_vector_4_float(self, values):
		self.write_float(values[0]),
		self.write_float(values[1]),
		self.write_float(values[2]),
		self.write_float(values[3]),

	def write_vector_3b(self, values):
		self.write_char(values[0]),
		self.write_char(values[1]),
		self.write_char(values[2]),


class BitAndBytes(object):

	def __init__(self):
		return

	@staticmethod
	def bits_parse(bit_array, start, length):
		"""
		Parse a portion of a bitfield.
		"""
		tmp = bit_array >> start
		return tmp & (2 ** length - 1)

	@staticmethod
	def bits_combine(bits, bit_array, start):
		"""
		Combine a values into a bit_array.

		@param bits: bits to add into bit_array
		@type bits: int
		@param bit_array: bit array in which bits are set
		@type bit_array: int
		"""
		tmp = bits << start  # move bits to the start position
		return tmp | bit_array
