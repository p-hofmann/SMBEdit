__author__ = 'Peter Hofmann'

import sys
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class DataType5(DefaultLogging):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "Meta-DataType5"
		super(DataType5, self).__init__(logfile, verbose, debug)
		self._tail_data = ""
		return

	# #######################################
	# ###  Read
	# #######################################

	def read(self, input_stream):
		"""
		Read tag root from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		# byte_array = input_stream.read_byte_array()
		# if not self._debug:
		self._tail_data = input_stream.read()
		return 1
		length = input_stream.read_int32_unassigned()
		self._logger.debug("datatype_5 length of byte array: '{}'".format(length))
		unknown_int = input_stream.read_vector_x_byte(3)
		unknown_string = input_stream.read_string()
		self._logger.debug("datatype_5 string: '{}', '{}'".format(unknown_int, unknown_string))
		unknown_int = input_stream.read_vector_x_byte(4)
		unknown_string = input_stream.read_string()
		self._logger.debug("datatype_5 string: '{}', '{}'".format(unknown_int, unknown_string))
		unknown_int = input_stream.read_vector_x_byte(5)
		unknown_string = input_stream.read_string()
		self._logger.debug("datatype_5 string: '{}', '{}'".format(unknown_int, unknown_string))
		unknown_int = input_stream.read_vector_x_byte(5)
		unknown_string = input_stream.read_string()
		self._logger.debug("datatype_5 string: '{}', '{}'".format(unknown_int, unknown_string))
		unknown_int = input_stream.read_vector_x_byte(6)
		unknown_string = input_stream.read_string()
		self._logger.debug("datatype_5 string: '{}', '{}'".format(unknown_int, unknown_string))
		unknown_int = input_stream.read_vector_x_byte(3)
		unknown_string = input_stream.read_string()
		self._logger.debug("datatype_5 string: '{}', '{}'".format(unknown_int, unknown_string))

		# aLt.a(new FastByteArrayInputStream(var7), true, false); root tag?
		return length

	# #######################################
	# ###  Write
	# #######################################

	def write(self, output_stream):
		"""
		write values

		@param output_stream: Output stream
		@type output_stream: ByteStream
		"""
		if len(self._tail_data) == 0:
			return
		self._logger.debug("Writing")
		output_stream.write_byte(5)
		output_stream.write(self._tail_data)

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
			output_stream.write("DataType5: #{}\n".format(len(self._tail_data)))
			output_stream.write("\n")
