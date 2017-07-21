__author__ = 'Peter Hofmann'

import sys

from ...utils.smbinarystream import SMBinaryStream
from ...common.loggingwrapper import DefaultLogging
from .tag.tagmanager import TagManager
from .tag.datatype2tagreader import Datatype2TagReader


class DataType2(DefaultLogging):
    """
    Reading data type 2 meta data

    @type _is_station: bool
    @type _tag_data: TagManager
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._is_station = False
        super(DataType2, self).__init__(label="DataType2", logfile=logfile, verbose=verbose, debug=debug)
        self._tag_data = TagManager(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read tags from byte stream

        @param input_stream: input stream
        @type input_stream: SMBinaryStream
        """
        self._tag_data = TagManager(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        self._tag_data.read(input_stream)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream, compressed=False):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: SMBinaryStream
        """
        if not self.has_data():
            return
        self._logger.debug("Writing")
        output_stream.write_byte(2)
        self._tag_data.write(output_stream, compressed)

    # #######################################
    # ###  Else
    # #######################################

    def has_data(self):
        return self._tag_data.has_data()

    def move_position(self, vector_direction):
        if self.has_data():
            self._tag_data.move_position(vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        if self._debug and self._tag_data.has_data():
            output_stream.write("DataType2\n")
            reader = Datatype2TagReader()
            reader.from_tag(self._tag_data.get_root_tag())
            reader.to_stream()
            # self._tag_data.to_stream(output_stream)
            output_stream.write("\n")
