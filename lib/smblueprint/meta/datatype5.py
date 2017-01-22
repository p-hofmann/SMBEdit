__author__ = 'Peter Hofmann'

import sys

from lib.bits_and_bytes import BinaryStream
from lib.loggingwrapper import DefaultLogging
from lib.smblueprint.meta.tag.tagmanager import TagManager
from lib.smblueprint.meta.tag.aiconfig import AIConfig


class DataType5(DefaultLogging):

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType5"
        super(DataType5, self).__init__(logfile, verbose, debug)
        self._tag_data = TagManager(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read tag root from byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        tag_size = input_stream.read_int32_unassigned()
        if tag_size > 0:
            self._tag_data = TagManager(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
            self._tag_data.read(input_stream)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream, compressed=False):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: BinaryStream
        """
        # if not self.has_data():
        #     return
        self._logger.debug("Writing")
        output_stream.write_byte(5)
        file_position_size = output_stream.tell()
        output_stream.seek(4, whence=1)  # skip size for later
        file_position_tag = output_stream.tell()
        self._tag_data.write(output_stream, compressed)
        file_position_end = output_stream.tell()
        output_stream.seek(file_position_size)
        tag_size = file_position_end-file_position_tag
        output_stream.write_int32_unassigned(tag_size)
        output_stream.seek(file_position_end)

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
        if self._debug:
            output_stream.write("DataType5\n")
            if self._tag_data.has_data():
                # self._tag_data.to_stream(output_stream)
                ai_config = AIConfig()
                ai_config.from_tag(self._tag_data.get_root_tag())
                ai_config.to_stream()
                output_stream.write("\n")
