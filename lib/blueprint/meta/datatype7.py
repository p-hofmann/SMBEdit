__author__ = 'Peter Hofmann'

import sys
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class DataType7(DefaultLogging):
    """
    Reading data type 7 meta data

    @type _data: dict[int,float]
    """
    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType7"
        super(DataType7, self).__init__(logfile, verbose, debug)
        self._has_data = 0
        self._data = {}
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream
        """
        self._has_data = input_stream.read_byte()
        if self._has_data > 0:
            number_of_entries = input_stream.read_int32_unassigned()
            assert number_of_entries < 10000, number_of_entries
            self._data = {}
            for _ in range(number_of_entries):
                key = input_stream.read_int64()
                value = input_stream.read_double()
                self._data[key] = value
        else:
            raise NotImplementedError("Unknown tag: {}".format(self._has_data))

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
        output_stream.write_byte(7)
        output_stream.write_byte(self._has_data)
        if not self._has_data > 0:
            return
        output_stream.write_int32_unassigned(len(self._data))
        for key in sorted(self._data.keys()):
            output_stream.write_int64(key)
            output_stream.write_double(self._data[key])

    # #######################################
    # ###  Else
    # #######################################

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        if self._debug:
            output_stream.write("DataType7: #{}\n".format(len(self._data)))
