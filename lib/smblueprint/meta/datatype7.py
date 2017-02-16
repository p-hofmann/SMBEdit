__author__ = 'Peter Hofmann'

import sys
from lib.binarystream import BinaryStream
from lib.loggingwrapper import DefaultLogging
from lib.utils.vector import Vector


class DataType7(DefaultLogging):
    """
    Reading data type 7 meta data
    # location of anything with storage and its volume

    @type _data: dict[int,float]
    """
    def __init__(self, logfile=None, verbose=False, debug=False):
        super(DataType7, self).__init__(label="DataType7", logfile=logfile, verbose=verbose, debug=debug)
        self._has_data = False
        self._data = {}
        return

    def has_data(self):
        return self._has_data

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read from byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        self._has_data = input_stream.read_bool()
        if self._has_data:
            number_of_entries = input_stream.read_int32_unassigned()
            self._data = {}
            for _ in range(number_of_entries):
                key = input_stream.read_int64()
                value = input_stream.read_double()
                self._data[key] = value

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: BinaryStream
        """
        self._logger.debug("Writing")
        output_stream.write_byte(7)
        output_stream.write_bool(self._has_data)
        if not self._has_data:
            return
        output_stream.write_int32_unassigned(len(self._data))
        for key in sorted(self._data.keys()):
            output_stream.write_int64(key)
            output_stream.write_double(self._data[key])

    # #######################################
    # ###  Else
    # #######################################

    def move_position(self, vector_direction):
        """
        Move positions of rail docked entities

        @type vector_direction: tuple[int]
        """
        old_data = self._data
        self._data = {}
        for position_index, volume in old_data.items():
            position_index = Vector.shift_position_index(position_index, vector_direction)
            self._data[position_index] = volume
        del old_data

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        if self._debug:
            output_stream.write("DataType7: #{}\n".format(len(self._data)))
