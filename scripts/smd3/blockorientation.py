__author__ = 'Peter Hofmann'

import sys
from scripts.bit_and_bytes import BitAndBytes
from scripts.blueprintutils import BlueprintUtils


class BlockOrientation(BitAndBytes, BlueprintUtils):
	"""
	Type    	Bits    	Description

	Type1   	23 	22 	21 	The block facing

	Type 2  	23 	22 		The axis of rotation.
							00 : +Y
							01 : -Y
							10 : -Z
							11 : +Z
				21 	20 		The amount of clockwise rotation around the axis of rotation, in 90-degree steps

	Type 3 		19 	23 	22 	The axis of rotation.
							000 : +Y
							001 : -Y
							010 : -Z
							011 : +Z
							100 : -X
							101 : +X
				21 	20 		The amount of clockwise rotation around the axis of rotation, in 90-degree step
	"""

	# https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

	def __init__(self, block_type):
		self._label = "BlockOrientation"
		super(BlockOrientation, self).__init__()
		self._type = block_type
		self._bit_array = 0
		self._block_facing = 0
		self._x = 0
		self._y = 0
		self._z = 0
		self._clockwise_rotations = 0

	def set_bit_array(self, bit_array):
		self._bit_array = bit_array
		self._parse_bit_array()

	def get_bit_array(self, bit_array):
		if self._type == 1:
			return self.bits_combine(self._x, bit_array, 21)
		if self._type == 3:
			bit_array = self.bits_combine(self._x, bit_array, 19)
		bit_array = self.bits_combine(self._clockwise_rotations, bit_array, 20)
		bit_array = self.bits_combine(self._y, bit_array, 22)
		bit_array = self.bits_combine(self._z, bit_array, 23)
		return bit_array

	def _parse_bit_array(self):
		"""
		The byte string is turned into an integer so bit operations can pick out each value.
		An integer is 4 byte (32 bit) but a block is only 3 byte long. THis is why '\x00' is added.
		'\x00' is added first because of big endian.
		"""
		self._block_facing = 0
		self._x = 0
		self._y = 0
		self._z = 0
		self._clockwise_rotations = 0
		if self._type == 1:
			self._block_facing = self.bits_parse(self._bit_array, 21, 3)
			return
		self._clockwise_rotations = self.bits_parse(self._bit_array, 20, 2)
		if self._type == 3:
			self._x = self.bits_parse(self._bit_array, 19, 1)
		self._y = self.bits_parse(self._bit_array, 22, 1)
		self._z = self.bits_parse(self._bit_array, 23, 1)

	def to_stream(self, output_stream=sys.stdout):
		"""

		@param output_stream:
		@type output_stream: FileIO
		"""
		output_stream.write(self.to_string())

	def to_string(self):
		"""
		@rtype: str
		"""
		if self._type == 1:
			return "Block facing: {}".format(self._block_facing)
		return_string = "Clockwise rotations: {} ".format(self._clockwise_rotations)
		if self._type == 3:
			return_string += "X: {}, ".format(self._x)
		return_string += "Y {}, ".format(self._y)
		return_string += "Z: {}".format(self._z)
		return return_string
