__author__ = 'Peter Hofmann'

import struct


class BitAndBytes(object):

	def __init__(self):
		return

	"""
	@ 	native 	native 	native
	= 	native 	standard 	none
	< 	little-endian 	standard 	none
	> 	big-endian 	standard 	none
	! 	network (= big-endian) 	standard 	none
	"""

	@staticmethod
	def parse_bits(bit_array, start, length):
		"""
		Used to parse a portion of a bitfield.
		"""
		tmp = bit_array >> start
		return tmp & (2 ** length - 1)

	@staticmethod
	def combine_bits(bits, bit_array, start):
		"""
		Used to parse a portion of a bitfield.
		"""
		tmp = bits << start
		return tmp | bit_array

	@staticmethod
	def _read_char(input_stream, order='>'):
		return struct.unpack('{}b'.format(order), input_stream.read(1))[0]

	@staticmethod
	def _read_float(input_stream, order='>'):
		return struct.unpack('{}f'.format(order), input_stream.read(4))[0]

	@staticmethod
	def _read_double(input_stream, order='>'):
		return struct.unpack('{}d'.format(order), input_stream.read(8))[0]

	@staticmethod
	def _read_int(input_stream, order='>'):
		return struct.unpack('{}i'.format(order), input_stream.read(4))[0]

	@staticmethod
	def _read_int24_unassigned(input_stream, order='>'):
		bytes = input_stream.read(3)
		return struct.unpack('{}i'.format(order), '\x00' + bytes)[0]

	@staticmethod
	def _read_long_long_unassigned(input_stream, order='>'):
		return struct.unpack('{}Q'.format(order), input_stream.read(8))[0]

	@staticmethod
	def _read_int_unassigned(input_stream, order='>'):
		return struct.unpack('{}I'.format(order), input_stream.read(4))[0]

	@staticmethod
	def _read_short_int(input_stream, order='>'):
		return struct.unpack('{}h'.format(order), input_stream.read(2))[0]

	@staticmethod
	def _read_short_int_unassigned(input_stream, order='>'):
		return struct.unpack('{}H'.format(order), input_stream.read(2))[0]

	def _read_string(self, input_stream, order='>'):
		length = self._read_short_int(input_stream, order)
		print length
		return struct.unpack(str(length) + 's', input_stream.read(length))[0]

	def _read_byte_array(self, input_stream):
		array = []
		length = self._read_int_unassigned(input_stream)
		for index in range(0, length):
			array.append(self._read_char(input_stream))
		return array

	def _read_vector_3si(self, input_stream):
		vector = [
			self._read_short_int(input_stream),
			self._read_short_int(input_stream),
			self._read_short_int(input_stream),
			]
		return vector

	def _read_vector_3i(self, input_stream):
		vector = [
			self._read_int(input_stream),
			self._read_int(input_stream),
			self._read_int(input_stream),
			]
		return vector

	def _read_vector_3f(self, input_stream):
		vector = [
			self._read_float(input_stream),
			self._read_float(input_stream),
			self._read_float(input_stream),
			]
		return vector

	def _read_vector_4f(self, input_stream):
		vector = [
			self._read_float(input_stream),
			self._read_float(input_stream),
			self._read_float(input_stream),
			self._read_float(input_stream),
			]
		return vector

	def _read_vector_3b(self, input_stream):
		vector = [
			self._read_char(input_stream),
			self._read_char(input_stream),
			self._read_char(input_stream),
			]
		return vector

# ###############
# #
# #	write
# #
# ###############

	@staticmethod
	def _write_char(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}b'.format(order), value))

	@staticmethod
	def _write_float(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}f'.format(order), value))

	@staticmethod
	def _write_double(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}d'.format(order), value))

	@staticmethod
	def _write_int(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}i'.format(order), value))

	@staticmethod
	def _write_int24_unassigned(value, output_stream, order='>'):
		byte_string = struct.pack('{}i'.format(order), value)
		output_stream.write(byte_string[1:])

	@staticmethod
	def _write_long_long_unassigned(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}Q'.format(order), value))

	@staticmethod
	def _write_int_unassigned(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}I'.format(order), value))

	@staticmethod
	def _write_short_int(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}h'.format(order), value))

	@staticmethod
	def _write_short_int_unassigned(value, output_stream, order='>'):
		output_stream.write(struct.pack('{}H'.format(order), value))

	def _write_string(self, value, output_stream, order='>'):
		length = len(value)
		self._write_short_int(length, output_stream, order)
		output_stream.write(struct.pack(str(length) + 's', value))

	def _write_byte_array(self, byte_array, output_stream):
		length = len(byte_array)
		self._write_int_unassigned(length, output_stream)
		for byte in byte_array:
			self._write_char(byte, output_stream)

	def _write_vector_3si(self, values, output_stream):
		self._write_short_int(values[0], output_stream),
		self._write_short_int(values[1], output_stream),
		self._write_short_int(values[2], output_stream),

	def _write_vector_3i(self, values, output_stream):
		self._write_int(values[0], output_stream),
		self._write_int(values[1], output_stream),
		self._write_int(values[2], output_stream),

	def _write_vector_3f(self, values, output_stream):
		self._write_float(values[0], output_stream),
		self._write_float(values[1], output_stream),
		self._write_float(values[2], output_stream),

	def _write_vector_4f(self, values, output_stream):
		self._write_float(values[0], output_stream),
		self._write_float(values[1], output_stream),
		self._write_float(values[2], output_stream),
		self._write_float(values[3], output_stream),

	def _write_vector_3b(self, values, output_stream):
		self._write_char(values[0], output_stream),
		self._write_char(values[1], output_stream),
		self._write_char(values[2], output_stream),
