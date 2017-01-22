__author__ = 'Peter Hofmann'

import sys

from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging
from lib.utils.vector import Vector


class RailEntry(object):
    """
    Data type 6 rail meta data

    @type _position: tuple[int]
    """

    def __init__(self):
        self._position = None
        self._block_id = 0
        self._unknown_byte_0 = 0
        self._active = False
        self._unknown_byte_1 = 0
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read entry from byte stream (17 byte)

        @param input_stream: input stream
        @type input_stream: ByteStream
        """
        self._position = input_stream.read_vector_3_int32()
        self._block_id = input_stream.read_int16()
        self._unknown_byte_0 = input_stream.read_byte()
        self._active = input_stream.read_bool()
        self._unknown_byte_1 = input_stream.read_byte()

    def write(self, output_stream):
        """
        Read entry from byte stream (17 byte)

        @param output_stream: input stream
        @type output_stream: ByteStream
        """
        output_stream.write_vector_3_int32(self._position),
        output_stream.write_int16(self._block_id),
        output_stream.write_byte(self._unknown_byte_0),
        output_stream.write_bool(self._active),
        output_stream.write_byte(self._unknown_byte_1)

    def move_position(self, vector_direction):
        self._position = Vector.vector_addition(self._position, vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t{}\t{}\t{}\t{}\n".format(
            self._position,
            self._block_id,
            self._unknown_byte_0,
            self._active,
            self._unknown_byte_1))


class DataType6(DefaultLogging):
    """
    Reading data type 6 meta data

    @type _data: dict[int,RailEntry]
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType6"
        super(DataType6, self).__init__(logfile, verbose, debug)
        self._has_data = 0
        self._data = {}
        return

    def read(self, input_stream):
        """
        Read from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream
        """
        self._has_data = input_stream.read_byte()
        if self._has_data == 0:
            return
        elif self._has_data > 0:
            number_of_entries = input_stream.read_int32_unassigned()
            self._data = {}
            for index in range(number_of_entries):
                # self._data[unknown_byte] = input_stream.read_vector_x_int32(4)
                self._data[index] = RailEntry()
                self._data[index].read(input_stream)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        if len(self._data) == 0:
            return
        self._logger.debug("Writing")
        output_stream.write_byte(6)
        output_stream.write_byte(self._has_data)
        if self._has_data == 0:
            return
        elif self._has_data == 1:
            output_stream.write_int32_unassigned(len(self._data))
            for some_index in sorted(self._data.keys()):
                self._data[some_index].write(output_stream)

    # #######################################
    # ###  Else
    # #######################################

    def move_position(self, vector_direction):
        for index in self._data.keys():
            self._data[index].move_position(vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        if self._debug:
            output_stream.write("DataType6: #{}\n".format(len(self._data)))
            for index in self._data.keys():
                self._data[index].to_stream(output_stream)
            output_stream.write("\n")
