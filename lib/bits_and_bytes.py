__author__ = 'Peter Hofmann'

import struct


class ByteStream(object):

    """
    Class idea based on:
    http://stackoverflow.com/questions/442188/readint-readbyte-readstring-etc-in-python/4338551#4338551

    Notes:
    @ 	native 	native 	native
    = 	native 	standard 	none
    < 	little-endian 	standard 	none
    > 	big-endian 	standard 	none
    ! 	network (= big-endian) 	standard 	none

    x 	pad byte        	no value
    c 	char            	string of length 1 	1
    b 	signed char     	integer 	1 	(3)
    B 	unsigned char     	integer 	1 	(3)
    ? 	_Bool           	bool    	1 	(1)
    h 	short           	integer 	2 	(3)
    H 	unsigned short  	integer 	2 	(3)
    i 	int             	integer 	4 	(3)
    I 	unsigned int     	integer 	4 	(3)
    l 	long            	integer 	4 	(3)
    L 	unsigned long     	integer 	4 	(3)
    q 	long long       	integer 	8 	(2), (3)
    Q 	unsigned long long 	integer 	8 	(2), (3)
    f 	float           	float   	4 	(4)
    d 	double          	float   	8 	(4)
    s 	char[]          	string
    p 	char[]          	string
    P 	void *          	integer 	  	(5), (3)

    @type _bytestream: file
    """

    def __init__(self, bytestream, byte_order=">"):
        """

        @param bytestream:
        @type bytestream: FileIO
        @param byte_order:
        @type byte_order: str
        """
        # assert isinstance(bytestream, file)
        self._bytestream = bytestream
        self._byte_order = byte_order
        return

    def __exit__(self, type, value, traceback):
        self._bytestream = None
        return

    def __enter__(self):
        return self

    # #######################################
    # ###  Packing and unpacking
    # #######################################

    @staticmethod
    def pack_int24(int_24bit):
        """
        @type int_24bit: int
        @rtype: str
        """
        return struct.pack('>i', int_24bit)[1:]

    @staticmethod
    def unpack_int24(byte_string):
        """
        @type byte_string: str
        @rtype: int
        """
        return struct.unpack(">i", '\x00' + byte_string)[0]

    def pack(self, value, data_type):
        """
        Pack value to byte string

        @param value: value to be packed
        @type value: any
        @param data_type: datatype
        @type data_type: str

        @return: byte string
        @rtype: str
        """
        return struct.pack("{order}{type}".format(
            order=self._byte_order,
            type=data_type), value)

    def _pack(self, value, data_type, padded=False):
        byte_string = self.pack(value, data_type)
        if not padded:
            self._bytestream.write(byte_string)
            return
        if self._byte_order == '>' or self._byte_order == '!':
            self._bytestream.write(byte_string[1:])
            return
        self._bytestream.write(byte_string[:-1])

    def unpack(self, byte_string, data_type):
        """
        Pack value to byte string

        @param byte_string: value to be packed
        @type byte_string: str
        @param data_type: datatype
        @type data_type: str

        @return: depends on data_type
        @rtype: any
        """
        return struct.unpack("{order}{type}".format(
            order=self._byte_order,
            type=data_type), byte_string)[0]

    def _unpack(self, length, data_type, padding=""):
        if self._byte_order == '>' or self._byte_order == '!':
            return self.unpack(padding + self._bytestream.read(length), data_type)
        return self.unpack(self._bytestream.read(length) + padding, data_type)

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
        return self._unpack(1, '?')

    def read_byte(self):
        return self._unpack(1, 'b')

    def read_byte_unassigned(self):
        return self._unpack(1, 'B')

    def read_int16(self):
        """
        @rtype: int
        """
        return self._unpack(2, 'h')

    def read_int16_unassigned(self):
        """
        @rtype: int
        """
        return self._unpack(2, 'H')

    def read_int24(self):
        """
        @rtype: int
        """
        return self._unpack(3, 'i', '\x00')

    def read_int24_unassigned(self):
        """
        @rtype: int
        """
        return self._unpack(3, 'I', '\x00')

    def read_int32(self):
        """
        @rtype: int
        """
        return self._unpack(4, 'i')

    def read_int32_unassigned(self):
        """
        @rtype: int
        """
        return self._unpack(4, 'I')

    def read_float(self):
        """
        @rtype: float
        """
        return self._unpack(4, 'f')

    def read_double(self):
        """
        @rtype: float
        """
        return self._unpack(8, 'd')

    def read_int64(self):
        """
        @rtype: int
        """
        return self._unpack(8, 'q')

    def read_int64_unassigned(self):
        """
        @rtype: int
        """
        return self._unpack(8, 'Q')

    def read_string(self):
        """
        @rtype: str
        """
        length = self.read_int16_unassigned()
        return self._unpack(length, str(length) + 's')

    def read_byte_array(self):
        """
        @rtype: list[int]
        """
        array = []
        length = self.read_int32_unassigned()
        assert 0 <= length < 1000000000
        if length == 0:
            return []
        for index in range(0, length):
            array.append(self.read_byte())
        return array

    def read_vector_3_int16(self):
        """
        @rtype: tuple[int]
        """
        vector = [
            self.read_int16(),
            self.read_int16(),
            self.read_int16(),
        ]
        return tuple(vector)

    def read_vector_3_int32(self):
        """
        @rtype: tuple[int]
        """
        vector = [
            self.read_int32(),
            self.read_int32(),
            self.read_int32(),
        ]
        return tuple(vector)

    def read_vector_3_float(self):
        """
        @rtype: tuple[float]
        """
        vector = [
            self.read_float(),
            self.read_float(),
            self.read_float(),
        ]
        return tuple(vector)

    def read_vector_4_float(self):
        """
        @rtype: tuple[float]
        """
        vector = [
            self.read_float(),
            self.read_float(),
            self.read_float(),
            self.read_float(),
        ]
        return tuple(vector)

    def read_vector_3_byte(self):
        """
        @rtype: tuple[int]
        """
        vector = [
            self.read_byte(),
            self.read_byte(),
            self.read_byte(),
        ]
        return tuple(vector)

    def read_vector_4_byte(self):
        """
        @rtype: tuple[int]
        """
        vector = [
            self.read_byte(),
            self.read_byte(),
            self.read_byte(),
            self.read_byte(),
        ]
        return tuple(vector)

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

    def read_vector_x_int32(self, amount):
        """
        @rtype: tuple[int]
        """
        vector = []
        for _ in range(amount):
            vector.append(self.read_int32())
        return tuple(vector)

    def read_matrix_4_float(self):
        """
        @rtype: list[list[float]]
        """
        matrix = []
        for _ in range(0, 4):
            matrix.append(
                [
                    self.read_float(),
                    self.read_float(),
                    self.read_float(),
                    self.read_float(),
                ])
        return matrix

    # #######################################
    # ###  Writing bytes
    # #######################################

    def write(self, value):
        """
        @type value: str
        """
        self._bytestream.write(value)

    def write_bool(self, value):
        """
        @type value: bool
        """
        self._pack(value, '?')

    def write_byte(self, value):
        """
        @type value: int
        """
        self._pack(value, 'b')

    def write_int16(self, value):
        """
        @type value: int
        """
        self._pack(value, 'h')

    def write_int16_unassigned(self, value):
        """
        @type value: int
        """
        self._pack(value, 'H')

    def write_int24(self, value):
        """
        @type value: int
        """
        self._pack(value, 'i', padded=True)

    def write_int24_unassigned(self, value):
        """
        @type value: int
        """
        self._pack(value, 'I', padded=True)

    def write_int32(self, value):
        """
        @type value: int
        """
        self._pack(value, 'i')

    def write_int32_unassigned(self, value):
        """
        @type value: int
        """
        self._pack(value, 'I')

    def write_int64(self, value):
        """
        @type value: int
        """
        self._pack(value, 'q')

    def write_int64_unassigned(self, value):
        """
        @type value: int
        """
        self._pack(value, 'Q')

    def write_float(self, value):
        """
        @type value: float
        """
        self._pack(value, 'f')

    def write_double(self, value):
        """
        @type value: float
        """
        self._pack(value, 'd')

    def write_string(self, value):
        """
        @type value: str
        """
        length = len(value)
        self.write_int16_unassigned(length)
        self._pack(value, str(length) + 's')

    def write_byte_array(self, values):
        """
        @type values: list[int]
        """
        length = len(values)
        self.write_int32_unassigned(length)
        for byte in values:
            self.write_byte(byte)

    def write_vector_3_byte(self, values):
        """
        @type values: tuple[int]
        """
        self.write_byte(values[0])
        self.write_byte(values[1])
        self.write_byte(values[2])

    def write_vector_4_byte(self, values):
        """
        @type values: tuple[int]
        """
        self.write_byte(values[0])
        self.write_byte(values[1])
        self.write_byte(values[2])
        self.write_byte(values[3])

    def write_vector_3_int16(self, values):
        """
        @type values: tuple[int]
        """
        self.write_int16(values[0])
        self.write_int16(values[1])
        self.write_int16(values[2])

    def write_vector_3_int32(self, values):
        """
        @type values: tuple[int]
        """
        self.write_int32(values[0])
        self.write_int32(values[1])
        self.write_int32(values[2])

    def write_vector_3_float(self, values):
        """
        @type values: tuple[float]
        """
        self.write_float(values[0])
        self.write_float(values[1])
        self.write_float(values[2])

    def write_vector_4_float(self, values):
        """
        @type values: tuple[float]
        """
        self.write_float(values[0])
        self.write_float(values[1])
        self.write_float(values[2])
        self.write_float(values[3])

    def write_vector_3b(self, values):
        """
        @type values: tuple[int]
        """
        self.write_byte(values[0])
        self.write_byte(values[1])
        self.write_byte(values[2])

    def write_vector_x_int32(self, values):
        """
        @type values: tuple[int]
        """
        for value in values:
            self.write_int32(value)

    def write_vector_x_byte(self, values):
        """
        @type values: tuple[int]
        """
        for value in values:
            self.write_byte(value)

    def write_matrix_4_float(self, matrix):
        """
        @type matrix: list[list[float]]
        """
        for index_x in range(0, 4):
            for index_y in range(0, 4):
                self.write_float(matrix[index_x][index_y])

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


class BitAndBytes(object):

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
