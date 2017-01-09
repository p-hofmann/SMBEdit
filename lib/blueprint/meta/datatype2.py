__author__ = 'Peter Hofmann'

import sys

from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging
from lib.blueprint.meta.tagmanager import TagManager


class DataType2(DefaultLogging):
    """
    Reading data type 2 meta data

    @type _tag_data: TagManager
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType2"
        super(DataType2, self).__init__(logfile, verbose, debug)
        self._tag_data = TagManager(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read tags from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream
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
        @type output_stream: ByteStream
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

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        if self._debug:
            output_stream.write("DataType2\n")
            self._tag_data.to_stream(output_stream)
            output_stream.write("\n")
