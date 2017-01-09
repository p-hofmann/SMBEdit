from __future__ import unicode_literals
from builtins import range
from builtins import object
__author__ = 'Peter Hofmann'

import sys
# import gzip
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging
from lib.blueprint.blueprintutils import BlueprintUtils


class TagUtil(object):

    # #######################################
    # ###  Read
    # #######################################

    @staticmethod
    def _read_payload(payload_type, input_stream):
        """

        @param payload_type:
        @type payload_type: int
        @param input_stream:
        @type input_stream: ByteStream

        @return:
        @rtype: any
        """
        # self._logger.debug("payload payload_type: '{}'".format(payload_type))
        if payload_type == 0:
            return None
        elif payload_type == 1:  # Byte
            return input_stream.read_byte()
        elif payload_type == 2:  # Short
            return input_stream.read_int16()
        elif payload_type == 3:  # Int
            return input_stream.read_int32()
        elif payload_type == 4:  # Long
            return input_stream.read_int64()
        elif payload_type == 5:  # Float
            return input_stream.read_float()
        elif payload_type == 6:  # Double
            return input_stream.read_double()
        elif payload_type == 7:  # Byte array
            return input_stream.read_byte_array()
        elif payload_type == 8:  # String
            return input_stream.read_string()  # utf?
        elif payload_type == 9:  # Float vector
            return input_stream.read_vector_3_float()
        elif payload_type == 10:  # int vector
            if BlueprintUtils.offset is not None:
                return BlueprintUtils.vector_addition(input_stream.read_vector_3_int32(), BlueprintUtils.offset)
            return input_stream.read_vector_3_int32()
        elif payload_type == 11:  # Byte vector
            return input_stream.read_vector_3_byte()
        elif payload_type == 12:  # TagList -> Payload List
            tag_payload_list = TagPayloadList()
            tag_payload_list.read(input_stream)
            return tag_payload_list
        elif payload_type == 13:  # TagStructure -> Tag list
            tag_list = TagList()
            tag_list.read(input_stream)
            return tag_list
        elif payload_type == 14:  # Factory registration # factoryId
            return input_stream.read_byte()
        elif payload_type == 15:  # Float4 vector
            return input_stream.read_vector_4_float()
        elif payload_type == 16:  # Float 4x4 matrix
            return input_stream.read_matrix_4_float()
        elif payload_type == 17:  # null
            return None
        else:
            # return None
            raise Exception("Unknown payload data type: {}".format(payload_type))

    # #######################################
    # ###  Write
    # #######################################

    @staticmethod
    def _write_payload(payload, payload_type, output_stream=sys.stdout):
        """
        Write payload

        @param payload:
        @type payload: any
        @param payload_type:
        @type payload_type: int
        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        if isinstance(payload, (TagList, TagPayloadList)):
            payload.write(output_stream)  # 12 / 13
            return
        if payload_type == 1:  # Byte
            output_stream.write_byte(payload)
        elif payload_type == 2:  # Short
            output_stream.write_int16(payload)
        elif payload_type == 3:  # Int
            output_stream.write_int32(payload)
        elif payload_type == 4:  # Long
            output_stream.write_int64(payload)
        elif payload_type == 5:  # Float
            output_stream.write_float(payload)
        elif payload_type == 6:  # Double
            output_stream.write_double(payload)
        elif payload_type == 7:  # Byte array
            output_stream.write_byte_array(payload)
        elif payload_type == 8:  # String
            output_stream.write_string(payload)  # utf?
        elif payload_type == 9:  # Float vector
            output_stream.write_vector_3_float(payload)
        elif payload_type == 10:  # int vector
            output_stream.write_vector_3_int32(payload)
        elif payload_type == 11:  # Byte vector
            output_stream.write_vector_3_byte(payload)
        # elif payload_type == 12:  # TagList -> Payload List
        #     payload.write(output_stream)
        # elif payload_type == 13:  # TagStructure -> Tag list
        #     payload.write(output_stream)
        elif payload_type == 14:  # Factory registration # factoryId
            output_stream.write_byte(payload)
        elif payload_type == 15:  # Float4 vector
            output_stream.write_vector_4_float(payload)
        elif payload_type == 16:  # Float 4x4 matrix
            output_stream.write_matrix_4_float(payload)
        else:
            raise Exception("Unknown payload data type: {}".format(payload_type))

    @staticmethod
    def _payload_to_stream(payload, output_stream=sys.stdout):
        if isinstance(payload, (TagPayload, TagList, TagPayloadList)):
            payload.to_stream(output_stream)
        else:
            output_stream.write("{}, ".format(payload))


class TagList(object):
    """

    @type tag_list: list[TagPayload|TagList|TagPayloadList]
    """

    def __init__(self):
        self.tag_list = []

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read a list of tags

        @param input_stream:
        @type input_stream: ByteStream

        @return:
        @rtype: TagList
        """
        self.tag_list = []
        while True:
            tag = TagPayload()
            tag.read(input_stream)
            # self._logger.debug("tag_list tag: '{}'".format(tag))
            if tag.id == 0:
                break
            self.tag_list.append(tag)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        for tag in self.tag_list:
            tag.write(output_stream)
        # write 0 tag to mark end of list
        output_stream.write_byte(0)

    def to_stream(self, output_stream=sys.stdout):
        output_stream.write(" {")
        for tag in self.tag_list:
            tag.to_stream(output_stream)
        output_stream.write("} ")

    # #######################################
    # ###  Get
    # #######################################

    def get_list(self):
        """
        @rtype: list[TagPayload]
        """
        return self.tag_list

    # #######################################
    # ###  Set
    # #######################################

    def add(self, tag):
        """
        @type tag: TagPayload
        """
        assert isinstance(tag, (TagPayload, TagList, TagPayloadList))
        self.tag_list.append(tag)


class TagPayloadList(TagUtil):
    """

    @type id: int
    @type payload_list: list[any]
    """

    def __init__(self):
        self.id = 0
        self.payload_list = []

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """
        Read list of data from the same tag type

        @param input_stream:
        @type input_stream: ByteStream

        @return:
        @rtype: TagPayloadList
        """
        assert isinstance(input_stream, ByteStream)
        self.id = input_stream.read_byte()
        length_list = input_stream.read_int32_unassigned()
        self.payload_list = []
        for index in range(0, length_list):
            self.payload_list.append(self._read_payload(abs(self.id), input_stream))

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        output_stream.write_byte(self.id)
        output_stream.write_int32_unassigned(len(self.payload_list))
        for payload in self.payload_list:
            self._write_payload(payload, abs(self.id), output_stream)

    def to_stream(self, output_stream=sys.stdout):
        output_stream.write("{}: [".format(self.id))
        for payload in self.payload_list:
            self._payload_to_stream(payload, output_stream)
            output_stream.write("\t")
        output_stream.write("] ".format(self.id))


class TagPayload(TagUtil):
    """

    @type id: int
    @type name: str | None
    @type payload: any
    """

    def __init__(self, payload_id=0, name=None, payload=None):
        self.id = payload_id
        if payload_id > 0:
            assert name is not None
        self.name = name
        self.payload = payload

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """

        @param input_stream:
        @type input_stream: ByteStream

        @return:
        @rtype: TagPayload
        """
        assert isinstance(input_stream, ByteStream)
        self.id = input_stream.read_byte()
        if self.id != 0:
            if self.id > 0:
                self.name = input_stream.read_string()
            self.payload = self._read_payload(abs(self.id), input_stream)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        output_stream.write_byte(self.id)
        if self.id == 0:
            return
        if self.id > 0:
            output_stream.write_string(self.name)
        self._write_payload(self.payload, abs(self.id), output_stream)

    def to_stream(self, output_stream=sys.stdout):
        if self.id > 0:
            output_stream.write("{}: '{}' ".format(self.id, self.name))
        else:
            output_stream.write("{}: ".format(self.id))
        self._payload_to_stream(self.payload, output_stream)
        # output_stream.write("\n")


class TagManager(DefaultLogging):
    """
    Reading tag structures

    @type _is_compressed: bool
    @type _root_tag: TagPayload
    @type _version: tuple[int]
    @type _tail_data: str
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "TagManager"
        super(TagManager, self).__init__(logfile, verbose, debug)
        self._is_compressed = False
        self._root_tag = None
        self._version = (0, 0)
        self._tail_data = ""
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):  # aLt.class
        """
        Read tag root from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream
        """
        self._version = input_stream.read_vector_x_byte(2)

        # if self.version == 0x1f8b:
        if self._version[0] == 31 and self._version[1] == -117:
            input_stream.seek(-2, 1)
            self._is_compressed = True
            raise NotImplementedError("not fully implemented, yet.")
            # input_stream = ByteStream(gzip.GzipFile(fileobj=input_stream))  # new GZIPInputStream(var15, 4096)
        # else:
        self._root_tag = TagPayload()
        self._root_tag.read(input_stream)

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
        output_stream.write_vector_x_byte(self._version)
        if compressed:
            raise NotImplementedError("TagManager gzip is not implemented, yet.")
        self._root_tag.write(output_stream)

    # #######################################
    # ###  Get
    # #######################################

    def get_root_tag(self):
        """
        Return Root TagPayload

        @rtype: TagPayload
        """
        return self._root_tag

    def has_data(self):
        return self._root_tag is not None

    # #######################################
    # ###  Set
    # #######################################

    def set_root_tag(self, tag_payload):
        """
        Set root

        @type tag_payload: TagPayload
        """
        self._root_tag = tag_payload

    # #######################################
    # ###  Else
    # #######################################

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        if not self.has_data:
            return
        output_stream.write("{} v{} gzip: {}\n".format(self._label, self._version, self._is_compressed))
        if self._debug:
            if len(self._tail_data) > 0:
                output_stream.write("Tail data: {}\n".format(len(self._tail_data)))
            self._root_tag.to_stream()
        output_stream.write("\n")
