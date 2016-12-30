__author__ = 'Peter Hofmann'

import sys
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class DataType6(DefaultLogging):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "Meta-DataType6"
		super(DataType6, self).__init__(logfile, verbose, debug)
		self._root_tag = 1
		self._data = {}
		return

	# #######################################
	# ###  Read
	# #######################################

	def read(self, input_stream):
		"""
		Read tag root from byte stream

		# 06 		01 		00 00 00 01 	00  	00 00 0b 00  00 00 0e ff  ff ff 6c 02  97 09 01 64
		# 06 		01		00 00 00 00

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		self._root_tag = input_stream.read_byte()
		if self._root_tag == 0:
			return
		elif self._root_tag == 1:
			unknown_int32 = input_stream.read_int32_unassigned()
			assert unknown_int32 < 2, unknown_int32
			self._data = {}
			for index in range(unknown_int32):
				unknown_byte = input_stream.read_byte()
				# self._data[unknown_byte] = input_stream.read_vector_x_int32(4)
				self._data[unknown_byte] = input_stream.read_vector_4_float()
		else:
			raise NotImplementedError("Unknown tag: {}".format(self._root_tag))

	# #######################################
	# ###  Write
	# #######################################

	def write(self, output_stream):
		"""
		write values

		@param output_stream: Output stream
		@type output_stream: ByteStream
		"""
		# if len(self._data) == 0:
		# 	return
		self._logger.debug("Writing")
		output_stream.write_byte(6)
		output_stream.write_byte(self._root_tag)
		if self._root_tag == 0:
			return
		elif self._root_tag == 1:
			output_stream.write_int32_unassigned(len(self._data))
			for unknown_byte in sorted(self._data.keys()):
				output_stream.write_byte(unknown_byte)
				output_stream.write_vector_4_float(self._data[unknown_byte])

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream logic values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		if self._debug:
			output_stream.write("DataType6: #{}\n".format(self._data))
			output_stream.write("\n")
