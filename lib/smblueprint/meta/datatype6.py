__author__ = 'Peter Hofmann'

import sys

from lib.binarystream import BinaryStream
from lib.loggingwrapper import DefaultLogging
from lib.utils.vector import Vector
from lib.smblueprint.meta.tag.raildockentitylinks import RailBasis


class RailDockerEntry(RailBasis):
    """
    Data type 6 rail meta data

    @type _position: tuple[int]
    """

    def __init__(self):
        self._position = None
        self._block_id = 0
        self._orientation = 0
        self._orientation_bit_3 = 0
        self._hit_points = 0
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read entry from byte stream (17 byte)

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        self._position = input_stream.read_vector_3_int32()
        self._block_id = input_stream.read_int16()
        self._orientation = input_stream.read_byte()
        self._orientation_bit_3 = input_stream.read_byte()
        self._hit_points = input_stream.read_byte()

    def write(self, output_stream):
        """
        Read entry from byte stream (17 byte)

        @param output_stream: input stream
        @type output_stream: BinaryStream
        """
        output_stream.write_vector_3_int32(self._position),
        output_stream.write_int16(self._block_id),
        output_stream.write_byte(self._orientation),
        output_stream.write_byte(self._orientation_bit_3),
        output_stream.write_byte(self._hit_points)

    def move_position(self, vector_direction):
        self._position = Vector.addition(self._position, vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\tId: {}\tOr.: {}\tHp: {}\n".format(
            self._position,
            self._block_id,
            self._rail_orientation_map[(self._orientation, self._orientation_bit_3)],
            self._hit_points))


class DataType6(DefaultLogging):
    """
    Reading data type 6 meta data

    @type _data: dict[int,RailDockerEntry]
    @type _has_data: bool
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType6"
        super(DataType6, self).__init__(logfile, verbose, debug)
        self._has_data = False
        self._data = {}
        return

    def read(self, input_stream):
        """
        Read from byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        self._has_data = input_stream.read_bool()
        if not self._has_data:
            return
        number_of_entries = input_stream.read_int32_unassigned()
        self._data = {}
        for index in range(number_of_entries):
            # self._data[unknown_byte] = input_stream.read_vector_x_int32(4)
            self._data[index] = RailDockerEntry()
            self._data[index].read(input_stream)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: BinaryStream
        """
        # if len(self._data) == 0:
        #     return
        self._logger.debug("Writing")
        output_stream.write_byte(6)
        output_stream.write_bool(self._has_data)
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
