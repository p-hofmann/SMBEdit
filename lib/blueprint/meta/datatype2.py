__author__ = 'Peter Hofmann'

import sys

from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging
from lib.blueprint.meta.tagmanager import TagManager
from lib.blueprint.meta.storage import StorageList
from lib.blueprint.meta.aiconfig import AIConfig
from lib.blueprint.meta.shop import Shop
from lib.blueprint.meta.displaylist import DisplayList


class DataType2(DefaultLogging):
    """
    Reading data type 2 meta data

    @type _is_station: bool
    @type _tag_data: TagManager
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType2"
        self._is_station = False
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
            root_tag = self._tag_data.get_root_tag()
            tag_list = root_tag.payload
            list_of_tag_paylaods = tag_list.get_list()

            tag_payload = list_of_tag_paylaods[0]
            sorage_list = StorageList()
            sorage_list.from_tag(tag_payload)
            sorage_list.to_stream(output_stream)
            sorage_test = StorageList()
            sorage_test.from_tag(sorage_list.to_tag())

            tag_payload = list_of_tag_paylaods[4]
            if tag_payload.id == 13 and "exS" in tag_payload.name:
                shop = Shop()
                shop.from_tag(tag_payload)
                shop.to_stream(output_stream)

            tag_payload = list_of_tag_paylaods[6]
            display_list = DisplayList()
            display_list.from_tag(tag_payload)
            display_list.to_stream(output_stream)

            tag_payload = list_of_tag_paylaods[6]
            if tag_payload.id == 13 and "AIConfig" in tag_payload.name:
                ai_config = AIConfig()
                ai_config.from_tag(tag_payload)
                ai_config.to_stream(output_stream)

            # self._tag_data.to_stream(output_stream)
            output_stream.write("\n")
