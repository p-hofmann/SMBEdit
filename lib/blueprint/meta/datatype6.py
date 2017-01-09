__author__ = 'Peter Hofmann'

import sys
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging


class DataType6(DefaultLogging):
    """
    Reading data type 6 meta data

    @type _data: dict[int,dict[str, any]]
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType6"
        super(DataType6, self).__init__(logfile, verbose, debug)
        self._has_data = 1
        self._data = {}
        return

    # #######################################
    # ###  Read
    # #######################################

    def _read_entry(self, input_stream):
        """
        Read entry from byte stream (17 byte)

        @param input_stream: input stream
        @type input_stream: ByteStream
        """
        entry = {
            "Pos": input_stream.read_vector_3_int32(),
            "block_id": input_stream.read_int16(),
            "byte1": input_stream.read_byte(),
            "bool": input_stream.read_bool(),
            "byte2": input_stream.read_byte()
            }
        return entry

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
                self._data[index] = self._read_entry(input_stream)

    # #######################################
    # ###  Write
    # #######################################

    def _write_entry(self, output_stream, entry):
        """
        Read entry from byte stream (17 byte)

        @param output_stream: input stream
        @type output_stream: ByteStream
        """
        output_stream.write_vector_3_int32(entry["Pos"]),
        output_stream.write_int16(entry["block_id"]),
        output_stream.write_byte(entry["byte1"]),
        output_stream.write_bool(entry["bool"]),
        output_stream.write_byte(entry["byte2"])
        return entry

    def write(self, output_stream):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        # if len(self._data) == 0:
        #     return
        self._logger.debug("Writing")
        output_stream.write_byte(6)
        output_stream.write_byte(self._has_data)
        if self._has_data == 0:
            return
        elif self._has_data == 1:
            output_stream.write_int32_unassigned(len(self._data))
            for some_index in sorted(self._data.keys()):
                self._write_entry(output_stream, self._data[some_index])

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
            output_stream.write("DataType6: #{}\n".format(len(self._data)))
            for index in self._data.keys():
                entry = self._data[index]
                output_stream.write("{}\t{}\t{}\t{}\t{}\n".format(
                    entry["Pos"], entry["block_id"], entry["byte1"], entry["bool"], entry["byte1"]))
            output_stream.write("\n")
