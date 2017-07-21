__author__ = 'Peter Hofmann'
__version__ = "0.0.2"

import struct
import sys

if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes


class BinaryStream(object):
    """
    Class idea based on:
    http://stackoverflow.com/questions/442188/readint-readbyte-readstring-etc-in-python/4338551#4338551

    Notes:
    @     native                native      native
    =     native                standard    none
    <     little-endian         standard    none
    >     big-endian            standard    none
    !     network (= big-endian)standard     none

    x     pad byte              no value
    c     char                  character   1     1
    b     signed char           integer     1     (3)
    B     unsigned char         integer     1     (3)
    ?     _Bool                 bool        1     (1)
    h     short                 integer     2     (3)
    H     unsigned short        integer     2     (3)
    i     int                   integer     4     (3)
    I     unsigned int          integer     4     (3)
    l     long                  integer     4     (3)
    L     unsigned long         integer     4     (3)
    q     long long             integer     8     (2), (3)
    Q     unsigned long long    integer     8     (2), (3)
    f     float                 float       4     (4)
    d     double                float       8     (4)
    s     char[]                string
    p     char[]                string
    P     void *                integer           (5), (3)

    @type _bytestream:
    """

    def __init__(self, bytestream, byte_order=">"):
        """

        @param bytestream: file like object
        @type bytestream: any
        @param byte_order: '<' little-endian, '>' big-endian
        @type byte_order: str
        """
        assert BinaryStream.is_stream(bytestream)
        self._bytestream = bytestream
        self._byte_order = byte_order
        return

    def __exit__(self, type, value, traceback):
        self._bytestream = None
        return

    def __del__(self):
        self._bytestream = None
        return

    def __enter__(self):
        return self

    # #######################################
    # ###  Packing and unpacking
    # #######################################

    @staticmethod
    def pack(data_type, byte_order='>', *values):
        """
        Pack value to byte string

        @param data_type: data type format
        @type data_type: str
        @param values: value to be packed
        @type values: any
        @param byte_order: '<' little-endian, '>' big-endian
        @type byte_order: str

        @return: byte string
        @rtype: str | bytes
        """
        return struct.pack("{order}{type}".format(order=byte_order, type=data_type), *values)

    @staticmethod
    def unpack(data_type, byte_string, byte_order='>'):
        """
        Pack value to byte string

        @param data_type: data type
        @type data_type: str
        @param byte_string: binary data to be unpacked
        @type byte_string: str | bytes
        @param byte_order: '<' little-endian, '>' big-endian
        @type byte_order: str

        @return: depends on data_type
        @rtype: tuple
        """
        return struct.unpack("{order}{type}".format(order=byte_order, type=data_type), byte_string)

    def _pack(self, data_type, byte_order=None, *values):
        """
        Pack value to byte string

        @param data_type: data type
        @type data_type: str
        @param byte_string: binary data to be unpacked
        @type byte_string: str | bytes
        @param byte_order: '<' little-endian, '>' big-endian
        @type byte_order: str | None

        @rtype: None
        """
        if byte_order is None:
            byte_order = self._byte_order
        byte_string = self.pack(data_type, byte_order, *values)
        self._bytestream.write(byte_string)

    def _unpack(self, length, data_type, byte_order=None):
        """
        Pack value to byte string

        @param length: amount of bytes
        @type length: int
        @param data_type: data type
        @type data_type: str
        @param byte_order: '<' little-endian, '>' big-endian
        @type byte_order: str

        @return: depends on data_type
        @rtype: tuple
        """
        if byte_order is None:
            byte_order = self._byte_order
        return self.unpack(data_type, self._bytestream.read(length), byte_order)

    # #######################################
    # ###  Reading bytes
    # #######################################

    def read(self, size=None):
        if size is None:
            return self._bytestream.read()
        return self._bytestream.read(size)

    def read_bool(self):
        """
        @rtype: bool
        """
        return self._unpack(1, '?')[0]

    def read_byte(self):
        return self._unpack(1, 'b')[0]

    def read_byte_unassigned(self):
        return self._unpack(1, 'B')[0]

    def read_int16(self, byte_order=None):
        """
        @rtype: int
        """
        return self._unpack(2, 'h', byte_order)[0]

    def read_int16_unassigned(self, byte_order=None):
        """
        @rtype: int
        """
        return self._unpack(2, 'H', byte_order)[0]

    def read_int32(self, byte_order=None):
        """
        @rtype: int
        """
        return self._unpack(4, 'i', byte_order)[0]

    def read_int32_unassigned(self, byte_order=None):
        """
        @rtype: int
        """
        return self._unpack(4, 'I', byte_order)[0]

    def read_float(self, byte_order=None):
        """
        @rtype: float
        """
        return self._unpack(4, 'f', byte_order)[0]

    def read_double(self, byte_order=None):
        """
        @rtype: float
        """
        return self._unpack(8, 'd', byte_order)[0]

    def read_int64(self, byte_order=None):
        """
        @rtype: int
        """
        return self._unpack(8, 'q', byte_order)[0]

    def read_int64_unassigned(self, byte_order=None):
        """
        @rtype: int
        """
        return self._unpack(8, 'Q', byte_order)[0]

    def read_string(self, byte_order=None):
        """
        @rtype: str
        """
        length = self.read_int16_unassigned(byte_order)
        string = self._unpack(length, '%is' % length, byte_order)[0]
        return string.decode('utf8')

    def read_byte_array(self, byte_order=None):
        """
        @rtype: list[int]
        """
        length = self.read_int32_unassigned(byte_order)
        assert 0 <= length < 1000000000
        return list(self._unpack(length, 'b' * length))

    # #######################################
    # ###  Writing bytes
    # #######################################

    def write(self, value):
        """
        @type value: : str | bytes
        """
        self._bytestream.write(value)

    def write_bool(self, value):
        """
        @type value: bool
        """
        self._pack('?', None, value)

    def write_byte(self, value):
        """
        @type value: int
        """
        self._pack('b', None, value)

    def write_int16(self, value, byte_order=None):
        """
        @type value: int
        """
        self._pack('h', byte_order, value)

    def write_int16_unassigned(self, value, byte_order=None):
        """
        @type value: int
        """
        self._pack('H', byte_order, value)

    def write_int32(self, value, byte_order=None):
        """
        @type value: int
        """
        self._pack('i', byte_order, value)

    def write_int32_unassigned(self, value, byte_order=None):
        """
        @type value: int
        """
        self._pack('I', byte_order, value)

    def write_int64(self, value, byte_order=None):
        """
        @type value: int
        """
        self._pack('q', byte_order, value)

    def write_int64_unassigned(self, value, byte_order=None):
        """
        @type value: int
        """
        self._pack('Q', byte_order, value)

    def write_float(self, value, byte_order=None):
        """
        @type value: float
        """
        self._pack('f', byte_order, value)

    def write_double(self, value, byte_order=None):
        """
        @type value: float
        """
        self._pack('d', byte_order, value)

    def write_string(self, value, byte_order=None):
        """
        @type value: str
        """
        length = len(value)
        self.write_int16_unassigned(length, byte_order)
        if isinstance(value, text_type):
            self._pack('%is' % length, byte_order, value.encode('utf-8'))
        else:
            self._pack('%is' % length, byte_order, value)

    def write_byte_array(self, values, byte_order=None):
        """
        @type values: list[int]
        """
        length = len(values)
        self.write_int32_unassigned(length, byte_order)
        for byte in values:
            self.write_byte(byte)

    # #######################################
    # ###  Navigate bytes
    # #######################################

    def seek(self, offset, whence=None):
        if whence is None:
            return self._bytestream.seek(offset)
        else:
            return self._bytestream.seek(offset, whence)

    def tell(self):
        return self._bytestream.tell()

    def is_eof(self):
        """
        Test if end of file is reached.
        """
        if not self._bytestream.read(1):
            return True
        self._bytestream.seek(-1, 1)
        return False

    @staticmethod
    def is_stream(stream):
        """
        Test for streams

        @param stream: Any kind of stream type
        @type stream: file | io.FileIO | StringIO.StringIO

        @return: True if stream
        @rtype: bool
        """
        attributes = {"read", "write", "seek", "tell"}
        for attribute in attributes:
            if not hasattr(stream, attribute):
                return False
        return True

    @staticmethod
    def bits_parse(some_integer, start, length):
        """
        Parse a section of bits from an integer.

        @param some_integer: value to be parsed
        @type some_integer: int
        @param start: starting bit
        @type start: int
        @param length: Number of bits belonging to a value
        @type length: int

        @rtype: int
        """
        tmp = some_integer >> start
        return tmp & (2 ** length - 1)

    @staticmethod
    def bits_combine(bits, bit_array, start):
        """
        Combine a values into a bit_array.

        @param bits: bits to add into bit_array
        @type bits: int
        @param bit_array: bit array in which bits are set
        @type bit_array: int
        """
        tmp = bits << start  # move bits to the start position
        return tmp | bit_array
