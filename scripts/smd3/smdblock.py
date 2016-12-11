__author__ = 'Peter Hofmann'

import sys
import struct
from scripts.bit_and_bytes import BitAndBytes, ByteStream
from scripts.blueprintutils import BlueprintUtils
from blockorientation import BlockOrientation

class SmdBlock(BitAndBytes, BlueprintUtils):

	# https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data
	_block_type_bit_positions = {
		1: (0, 11, 20, 21),  # logic block
		2: (0, 11, 20, 20),  # normal block
		3: (0, 11, 19, 19),  # corner block
	}

	# _block_type_bit_positions = {
	# 	1: (0, 10, 18, 19),  # logic block
	# 	2: (0, 10, 18, 19),  # logic block
	# 	3: (0, 10, 18, 19),  # logic block
	# }

	def __init__(self):
		self._label = "SmdBlock"
		super(SmdBlock, self).__init__()
		self._type = 0
		self._id = 0
		self._hitpoints = 0
		self._active = 0
		self._orientation = BlockOrientation(self._type)
		self._byte_string = ""

	def get_id(self):
		"""
		Returns the block id

		@rtype: int
		"""
		return self._id

	def get_hitpoints(self):
		"""
		Returns the hit points of the block

		@rtype: int
		"""
		return self._hitpoints

	def is_active(self):
		"""
		Returns the 'active' status.

		@rtype: int
		"""
		return self._active == 1

	def get_orientation(self):
		"""
		Returns the orientation of the block as integer.

		@rtype: BlockOrientation
		"""
		# Todo: find out what integer is what direction.
		return self._orientation

	def set_id(self, value):
		"""
		Change block id of block

		@param value:
		@type value: int
		"""
		self._id = value
		self._refresh_block_type()
		self._refresh_data_byte_string()

	def set_hitpoints(self, value):
		"""
		Change hit points of block

		@param value:
		@type value: int
		"""
		self._hitpoints = value
		self._refresh_data_byte_string()

	def set_active(self, value):
		"""
		Change 'active' status of of block

		@param value:
		@type value: bool
		"""
		if value:
			self._active = 1
		else:
			self._active = 0
		self._refresh_data_byte_string()

	def set_orientation(self, value):
		"""
		Change orientation of block

		@param value:
		@type value: BlockOrientation
		"""
		self._orientation = value
		self._refresh_data_byte_string()

	def set_data_byte_string(self, byte_string):
		"""
		Change the byte string representing the block and parse it for easy access.
		The byte string is kept to speed up writing files.

		@param byte_string:
		@type byte_string: str
		"""
		self._byte_string = byte_string
		self._parse_byte_string()

	def get_data_byte_string(self):
		"""
		Returns the byte string representing a block.

		@rtype: str
		"""
		return self._byte_string

	def _parse_byte_string(self):
		"""
		The byte string is turned into an integer so bit operations can pick out each value.
		An integer is 4 byte (32 bit) but a block is only 3 byte long. THis is why '\x00' is added.
		'\x00' is added first because of big endian.
		"""
		# bit_array = self._read_int24_unassigned(input_stream)
		bit_array = struct.unpack('>i', '\x00' + self._byte_string)[0]
		# bit_array = ByteStream.unpack('\x00' + self._byte_string, 'i')
		self._id = self.bits_parse(bit_array, 0, 11)
		self._refresh_block_type()
		self._hitpoints = self.bits_parse(bit_array, self._block_type_bit_positions[self._type][1], self._block_type_bit_positions[self._type][2]-self._block_type_bit_positions[self._type][1])
		if self._type == 0:  # For blocks with an activation status
			self._active = self.bits_parse(bit_array, self._block_type_bit_positions[self._type][2], self._block_type_bit_positions[self._type][3]-self._block_type_bit_positions[self._type][2])  # For blocks with an activation status
		self._orientation = BlockOrientation(self._type)
		self._orientation.set_bit_array(bit_array)
		# = self.bits_parse(bit_array, self._block_type_bit_positions[self._type][3], 24-self._block_type_bit_positions[self._type][3])

	def _refresh_data_byte_string(self):
		"""
		In the rare case a block value is changed, they are turned into a byte string.
		'[1:]' since only the last three bytes of an integer are used for block information.
		"""
		bit_array = 0
		bit_array = self.bits_combine(self._id, bit_array, 0)
		bit_array = self.bits_combine(self._hitpoints, bit_array, self._block_type_bit_positions[self._type][1])
		if self._type == 0:  # For blocks with an activation status
			bit_array = self.bits_combine(self._active, bit_array, self._block_type_bit_positions[self._type][2])
		# bit_array = self.bits_combine(self._orientation, bit_array, self._block_type_bit_positions[self._type][3])
		bit_array = self._orientation.get_bit_array(bit_array)
		self._byte_string = struct.pack('>i', bit_array)[1:]

	def _refresh_block_type(self):
		if self._is_activatable_block(self._id):
			self._type = 1
			return
		if self._is_corner_block(self._id):
			self._type = 3
			return
		self._type = 2

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream block values

		@param output_stream:
		@type output_stream: fileIO
		"""
		output_stream.write("({})\t".format(self._type))
		output_stream.write("HP: {}\t".format(self._hitpoints))
		output_stream.write("Active: {}\t".format(self._active))
		output_stream.write("Or.: {}\t".format(self._orientation.to_string()))
		output_stream.write("{}\n".format(self.get_block_name_by_id(self._id)))
	#
	#Element.class
	#
    # private static void createOrientationMapping() {
    #     (orientationMapping = new byte[24])[4] = 0;
    #     orientationMapping[5] = 1;
    #     orientationMapping[2] = 2;
    #     orientationMapping[3] = 3;
    #     orientationMapping[0] = 4;
    #     orientationMapping[1] = 5;
    #     orientationMapping[6] = 6;
    #     orientationMapping[7] = 7;
    #     orientationMapping[12] = 8;
    #     orientationMapping[13] = 9;
    #     orientationMapping[10] = 10;
    #     orientationMapping[11] = 11;
    #     orientationMapping[8] = 12;
    #     orientationMapping[9] = 13;
    #     orientationMapping[14] = 14;
    #     orientationMapping[15] = 15;
    #     orientationMapping[20] = 16;
    #     orientationMapping[21] = 17;
    #     orientationMapping[18] = 18;
    #     orientationMapping[19] = 19;
    #     orientationMapping[16] = 20;
    #     orientationMapping[17] = 21;
    #     orientationMapping[22] = 22;
    #     orientationMapping[23] = 23;
    #     (orientationBackMapping = new byte[24])[0] = 4;
    #     orientationBackMapping[1] = 5;
    #     orientationBackMapping[2] = 2;
    #     orientationBackMapping[3] = 3;
    #     orientationBackMapping[4] = 0;
    #     orientationBackMapping[5] = 1;
    #     orientationBackMapping[6] = 6;
    #     orientationBackMapping[7] = 7;
    #     orientationBackMapping[8] = 12;
    #     orientationBackMapping[9] = 13;
    #     orientationBackMapping[10] = 10;
    #     orientationBackMapping[11] = 11;
    #     orientationBackMapping[12] = 8;
    #     orientationBackMapping[13] = 9;
    #     orientationBackMapping[14] = 14;
    #     orientationBackMapping[15] = 15;
    #     orientationBackMapping[16] = 20;
    #     orientationBackMapping[17] = 21;
    #     orientationBackMapping[18] = 18;
    #     orientationBackMapping[19] = 19;
    #     orientationBackMapping[20] = 16;
    #     orientationBackMapping[21] = 17;
    #     orientationBackMapping[22] = 22;
    #     orientationBackMapping[23] = 23;
    # }
	#
    # public static int getOpposite(int var0) {
    #     switch(var0) {
    #     case 0:
    #         return 1;
    #     case 1:
    #         return 0;
    #     case 2:
    #         return 3;
    #     case 3:
    #         return 2;
    #     case 4:
    #         return 5;
    #     case 5:
    #         return 4;
    #     default:
    #         throw new RuntimeException("SIDE NOT FOUND: " + var0);
    #     }
    # }
	#
    # public static int getClockWiseZ(int var0) {
    #     switch(var0) {
    #     case 0:
    #         return 0;
    #     case 1:
    #         return 1;
    #     case 2:
    #         return 4;
    #     case 3:
    #         return 5;
    #     case 4:
    #         return 3;
    #     case 5:
    #         return 2;
    #     default:
    #         throw new RuntimeException("SIDE NOT FOUND: " + var0);
    #     }
    # }
	#
    # public static int getCounterClockWiseZ(int var0) {
    #     switch(var0) {
    #     case 0:
    #         return 0;
    #     case 1:
    #         return 1;
    #     case 2:
    #         return 5;
    #     case 3:
    #         return 4;
    #     case 4:
    #         return 2;
    #     case 5:
    #         return 3;
    #     default:
    #         throw new RuntimeException("SIDE NOT FOUND: " + var0);
    #     }
    # }
	#
    # public static int getClockWiseX(int var0) {
    #     switch(var0) {
    #     case 0:
    #         return 3;
    #     case 1:
    #         return 2;
    #     case 2:
    #         return 0;
    #     case 3:
    #         return 1;
    #     case 4:
    #         return 4;
    #     case 5:
    #         return 5;
    #     default:
    #         throw new RuntimeException("SIDE NOT FOUND: " + var0);
    #     }
    # }
	#
    # public static int getCounterClockWiseX(int var0) {
    #     switch(var0) {
    #     case 0:
    #         return 2;
    #     case 1:
    #         return 3;
    #     case 2:
    #         return 1;
    #     case 3:
    #         return 0;
    #     case 4:
    #         return 0;
    #     case 5:
    #         return 5;
    #     default:
    #         throw new RuntimeException("SIDE NOT FOUND: " + var0);
    #     }
    # }
	#
    # public static int getCounterClockWiseY(int var0) {
    #     switch(var0) {
    #     case 0:
    #         return 4;
    #     case 1:
    #         return 5;
    #     case 2:
    #         return 2;
    #     case 3:
    #         return 3;
    #     case 4:
    #         return 1;
    #     case 5:
    #         return 0;
    #     default:
    #         throw new RuntimeException("SIDE NOT FOUND: " + var0);
    #     }
    # }
	#
    # public static int getClockWiseY(int var0) {
    #     switch(var0) {
    #     case 0:
    #         return 5;
    #     case 1:
    #         return 4;
    #     case 2:
    #         return 2;
    #     case 3:
    #         return 3;
    #     case 4:
    #         return 0;
    #     case 5:
    #         return 1;
    #     default:
    #         throw new RuntimeException("SIDE NOT FOUND: " + var0);
    #     }
    # }
