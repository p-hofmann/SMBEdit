__author__ = 'Peter Hofmann'

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

    def read_vector_3_int16(self, byte_order=None):
        """
        @rtype: (int, int, int)
        """
        return self._unpack(6, 'hhh', byte_order)

    def read_vector_3_int32(self, byte_order=None):
        """
        @rtype: (int, int, int)
        """
        return self._unpack(12, 'iii', byte_order)

    def read_vector_3_float(self, byte_order=None):
        """
        @rtype: (float, float, float)
        """
        return self._unpack(12, 'fff', byte_order)

    def read_vector_4_float(self, byte_order=None):
        """
        @rtype: (float, float, float, float)
        """
        return self._unpack(16, 'ffff', byte_order)

    def read_vector_3_byte(self):
        """
        @rtype: (int, int, int)
        """
        return self._unpack(3, 'bbb')

    def read_vector_4_byte(self):
        """
        @rtype: (int, int, int, int)
        """
        return self._unpack(4, 'bbbb')

    def read_vector_x_byte(self, amount):
        """
        @rtype: tuple[int]
        """
        vector = []
        for _ in range(amount):
            vector.append(self.read_byte())
        return tuple(vector)

    def read_vector_x_byte_unassigned(self, amount):
        """
        @rtype: tuple[int]
        """
        vector = []
        for _ in range(amount):
            vector.append(self.read_byte_unassigned())
        return tuple(vector)

    def read_vector_x_int32(self, amount, byte_order=None):
        """
        @rtype: tuple[int]
        """
        vector = []
        for _ in range(amount):
            vector.append(self.read_int32(byte_order))
        return tuple(vector)

    def read_matrix_4_float(self, byte_order=None):
        """
        @rtype: list[list[float]]
        """
        matrix = []
        for _ in range(0, 4):
            matrix.append(list(self.read_vector_4_float(byte_order)))
        return matrix

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

    def write_vector_3_byte(self, values):
        """
        @type values: (int, int, int)
        """
        self.write_byte(values[0])
        self.write_byte(values[1])
        self.write_byte(values[2])

    def write_vector_4_byte(self, values):
        """
        @type values: (int, int, int, int)
        """
        self.write_byte(values[0])
        self.write_byte(values[1])
        self.write_byte(values[2])
        self.write_byte(values[3])

    def write_vector_3_int16(self, values, byte_order=None):
        """
        @type values: (int, int, int)
        """
        self.write_int16(values[0], byte_order)
        self.write_int16(values[1], byte_order)
        self.write_int16(values[2], byte_order)

    def write_vector_3_int32(self, values, byte_order=None):
        """
        @type values: (int, int, int)
        """
        self.write_int32(values[0], byte_order)
        self.write_int32(values[1], byte_order)
        self.write_int32(values[2], byte_order)

    def write_vector_3_float(self, values, byte_order=None):
        """
        @type values: (float, float, float)
        """
        self.write_float(values[0], byte_order)
        self.write_float(values[1], byte_order)
        self.write_float(values[2], byte_order)

    def write_vector_4_float(self, values, byte_order=None):
        """
        @type values: (float, float, float, float)
        """
        self.write_float(values[0], byte_order)
        self.write_float(values[1], byte_order)
        self.write_float(values[2], byte_order)
        self.write_float(values[3], byte_order)

    def write_vector_x_int32(self, values, byte_order=None):
        """
        @type values: tuple[int]
        """
        for value in values:
            self.write_int32(value, byte_order)

    def write_vector_x_byte(self, values):
        """
        @type values: tuple[int]
        """
        for value in values:
            self.write_byte(value)

    def write_matrix_4_float(self, matrix, byte_order=None):
        """
        @type matrix: list[list[float]]
        """
        for index_x in range(0, 4):
            for index_y in range(0, 4):
                self.write_float(matrix[index_x][index_y], byte_order)

    # #######################################
    # ugly methods
    # #######################################

    @staticmethod
    def pack_int24(int_24bit, byte_order='>'):
        """
        @type int_24bit: int
        @rtype: str | bytes
        """
        return BinaryStream.pack('i', byte_order, int_24bit)[1:]

    @staticmethod
    def pack_int24b(int_24bit, byte_order='>'):
        """
        @type int_24bit: int
        @rtype: str | bytes
        """
        data = (
            BinaryStream.bits_parse(int_24bit, 0, 8),
            BinaryStream.bits_parse(int_24bit, 8, 8),
            BinaryStream.bits_parse(int_24bit, 16, 8),
        )
        return BinaryStream.pack('BBB', byte_order, data[0], data[1], data[2])

    @staticmethod
    def unpack_int24(byte_string):
        """
        @type byte_string: str | bytes
        @rtype: int
        """
        return struct.unpack(">i", b'\x00' + byte_string)[0]

    @staticmethod
    def unpack_int24b(byte_string):
        """
        @type byte_string: str | bytes
        @rtype: int
        """
        data = struct.unpack(">BBB", byte_string)
        return data[0] | data[1] << 8 | data[2] << 16

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
