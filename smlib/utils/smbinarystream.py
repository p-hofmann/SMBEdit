__author__ = 'Peter Hofmann'

import struct

from ..common.binarystream import BinaryStream


class SMBinaryStream(BinaryStream):
    """
    Modified BinaryStream dealing with StarMade specific binary data
    """

    # #######################################
    # ###  Reading bytes
    # #######################################

    def read_int24(self, by_byte=False):
        """
        @rtype: int
        """
        if by_byte:
            return self.unpack_int24b(self.read(3))
        return self.unpack_int24(self.read(3))

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
    # Methods for byte conversion of sm-block data
    # #######################################

    @staticmethod
    def pack_int24(int_24bit, byte_order='>'):
        """
        @type int_24bit: int
        @rtype: str | bytes
        """
        return SMBinaryStream.pack('i', byte_order, int_24bit)[1:]

    @staticmethod
    def pack_int24b(int_24bit, byte_order='>'):
        """
        @type int_24bit: int
        @rtype: str | bytes
        """
        data = (
            SMBinaryStream.bits_parse(int_24bit, 0, 8),
            SMBinaryStream.bits_parse(int_24bit, 8, 8),
            SMBinaryStream.bits_parse(int_24bit, 16, 8),
        )
        return SMBinaryStream.pack('BBB', byte_order, data[0], data[1], data[2])

    @staticmethod
    def unpack_int24(byte_string):
        """
        Read values as integer

        @type byte_string: str | bytes
        @rtype: int
        """
        return struct.unpack(">i", b'\x00' + byte_string)[0]

    @staticmethod
    def unpack_int24b(byte_string):
        """
        Read values one bytes at a time

        @type byte_string: str | bytes
        @rtype: int
        """
        data = struct.unpack(">BBB", byte_string)
        return data[0] | data[1] << 8 | data[2] << 16
