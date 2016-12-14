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

	#   -Y  	   -Z   	  -Z
	# -X   X	 -Y   Y 	-X   X
	#    Y  	    Z   	   Z

	_direction_turn_90 = {
		(-1, 0): (0, -1),
		(0, -1): (1, 0),
		(1, 0): (0, 1),
		(0, 1): (-1, 0),
	}

	_direction_turn_270 = {
		(0, -1): (-1, 0),
		(-1, 0): (0, 1),
		(0, 1): (1, 0),
		(1, 0): (0, -1),
	}

	_orientation_to_direction = {
		(1, 0, 0): (-1, 0, 0),  # -X
		(1, 0, 1): (1, 0, 0),  # +X
		(0, 0, 0): (0, 1, 0),  # +Y
		(0, 0, 1): (0, -1, 0),  # -Y
		(0, 1, 0): (0, 0, -1),  # -Z
		(0, 1, 1): (0, 0, 1),  # +Z
		(0, 0): (1, 0),  # +Y
		(0, 1): (-1, 0),  # -Y
		(1, 0): (0, -1),  # -Z
		(1, 1): (0, 1),  # +Z
		# (1, 1, 0): (0, 0, -1),  # -Z odd hull blocks
		# (1, 1, 1): (0, 0, 1),  # +Z odd hull blocks
	}

	_direction_to_orientation = {
		(-1, 0, 0): (1, 0, 0),  # -X
		(1, 0, 0): (1, 0, 1),  # +X
		(0, 1, 0): (0, 0, 0),  # +Y
		(0, -1, 0): (0, 0, 1),  # -Y
		(0, 0, -1): (0, 1, 0),  # -Z
		(0, 0, 1): (0, 1, 1),  # +Z
		(1, 0): (0, 0),  # +Y
		(-1, 0): (0, 1),  # -Y
		(0, -1): (1, 0),  # -Z
		(0, 1): (1, 1),  # +Z
	}

	_block_side_id_to_str = {
		0: "FRONT ",
		1: "BACK  ",
		2: "TOP   ",
		3: "BOTTOM",
		4: "RIGHT ",
		5: "LEFT  ",
	}

	# https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

	def __init__(self, block_type):
		self._label = "BlockOrientation"
		super(BlockOrientation, self).__init__()
		self._type = block_type
		self._bit_array = 0
		self._block_side_id = 0
		self._x = 0
		self._y = 0
		self._z = 0
		self._clockwise_rotations = 0

	def set_bit_array(self, bit_array):
		self._bit_array = bit_array
		self._parse_bit_array()

	def get_bit_array(self, bit_array):
		if self._type == 1:
			return self.bits_combine(self._x, bit_array, 20)
		if self._type != 1:
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
		self._block_side_id = 0
		self._x = 0
		self._y = 0
		self._z = 0
		self._clockwise_rotations = 0
		if self._type == 1:
			self._block_side_id = self.bits_parse(self._bit_array, 20, 4)
			return
		if self._type != 1:
			self._x = self.bits_parse(self._bit_array, 19, 1)
		self._clockwise_rotations = self.bits_parse(self._bit_array, 20, 2)
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
		# return str(self.bits_parse(self._bit_array, 19, 4))
		if self._type == 1:
			return "Facing: {}".format(self._block_side_id_to_str[self._block_side_id])
		side = self._get_side_from_direction()
		return_string = ""
		return_string += "Facing: {}".format(self._block_side_id_to_str[side])
		return_string += " {}* ".format(self._clockwise_rotations * 90)
		# if self._type != 1:
		# 	return_string += "X: {}, ".format(self._x)
		# return_string += "Y {}, ".format(self._y)
		# return_string += "Z: {}".format(self._z)
		return return_string

	# #######################################
	# ###  Turning - Experimental
	# #######################################

	def _get_side_from_direction(self):
		"""

		@rtype: int
		"""
		orientation = (self._x, self._y, self._z)
		if self._type == 2:
			orientation = (0, self._y, self._z)
		assert orientation in self._orientation_to_direction
		direction = self._orientation_to_direction[orientation]
		assert abs(direction[0]) + abs(direction[1]) + abs(direction[2]) == 1, "Bad direction: {}".format(direction)
		if direction[0] == 1:
			return 4
		if direction[0] == -1:
			return 5
		if direction[1] == 1:
			return 2
		if direction[1] == -1:
			return 3
		if direction[2] == 1:
			return 0
		if direction[2] == -1:
			return 1
		raise Exception("Bad direction: {}".format(direction))

	def turn_upside_down(self):
		if self._type == 1:
			self._turn_facing_180()
			return
		self._turn_direction_180()

	def turn_180(self):
		if self._type == 1:
			self._turn_facing_180()
			return
		self._turn_direction_180()

	def turn_90_x(self):
		if self._type == 1:
			self._turn_facing_90_x()
			return
		self._turn_direction_90_x()

	def turn_270_x(self):
		if self._type == 1:
			self._turn_facing_270_x()
			return
		self._turn_direction_270_x()

	def turn_90_y(self):
		if self._type == 1:
			self._turn_facing_90_y()
			return
		self._turn_direction_90_y()

	def turn_270_y(self):
		if self._type == 1:
			self._turn_facing_270_y()
			return
		self._turn_direction_270_y()

	def turn_90_z(self):
		if self._type == 1:
			self._turn_facing_90_z()
			return
		self._turn_direction_90_z()

	def turn_270_z(self):
		if self._type == 1:
			self._turn_facing_270_z()
			return
		self._turn_direction_270_z()

	# #######################################
	# ###  Turning type 1
	# #######################################

	def _turn_facing_180(self):
		self._block_side_id = {
			0: 1,
			1: 0,
			2: 3,
			3: 2,
			4: 5,
			5: 4,
		}[self._block_side_id]

	def _turn_facing_90_x(self):
		self._block_side_id = {
			0: 3,
			1: 2,
			2: 0,
			3: 1,
			4: 4,
			5: 5,
		}[self._block_side_id]

	def _turn_facing_270_x(self):
		self._block_side_id = {
			0: 2,
			1: 3,
			2: 1,
			3: 0,
			4: 4,
			5: 5,
		}[self._block_side_id]

	def _turn_facing_90_y(self):
		self._block_side_id = {
			0: 5,
			1: 4,
			2: 2,
			3: 3,
			4: 0,
			5: 1,
		}[self._block_side_id]

	def _turn_facing_270_y(self):
		self._block_side_id = {
			0: 4,
			1: 5,
			2: 2,
			3: 3,
			4: 1,
			5: 0,
		}[self._block_side_id]

	def _turn_facing_90_z(self):
		self._block_side_id = {
			0: 0,
			1: 1,
			2: 4,
			3: 5,
			4: 3,
			5: 2,
		}[self._block_side_id]

	def _turn_facing_270_z(self):
		self._block_side_id = {
			0: 0,
			1: 1,
			2: 5,
			3: 4,
			4: 2,
			5: 3,
		}[self._block_side_id]

	# #######################################
	# ###  Turning type 2 + 3
	# #######################################

	def _turn_direction_upside_down(self):
		if self._type == 2:
			direction = self._orientation_to_direction[(self._y, self._z)]
			self._y, self._z = self._direction_to_orientation[(-1*direction[0], -1*direction[1])]

		if self._type == 3:
			direction = self._orientation_to_direction[(self._x, self._y, self._z)]
			self._x, self._y, self._z = self._direction_to_orientation[(-1*direction[0], -1*direction[1], -1*direction[2])]

		# self._clockwise_rotations = (self._clockwise_rotations + 2) % 4

	# def _turn_direction_180(self, upside_down=False):
	# 	if self._type == 2:
	# 		direction = self._orientation_to_direction[(self._y, self._z)]
	# 		self._y, self._z = self._direction_to_orientation[(-1*direction[0], -1*direction[1])]
	#
	# 	if self._type == 3:
	# 		direction = self._orientation_to_direction[(self._x, self._y, self._z)]
	# 		self._x, self._y, self._z = self._direction_to_orientation[(-1*direction[0], -1*direction[1], -1*direction[2])]
	#
	# 	self._clockwise_rotations = (self._clockwise_rotations + 2) % 4

	# ###  Turning X Axis

	def _turn_direction_90_x(self):
		if self._type == 2:
			direction = self._orientation_to_direction[(self._y, self._z)]
			self._y, self._z = self._direction_to_orientation[self._direction_turn_90[direction[0], direction[1]]]

		if self._type == 3:
			direction = self._orientation_to_direction[(self._x, self._y, self._z)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			direction_turn = self._direction_turn_90[direction[1], direction[2]]
			self._x, self._y, self._z = self._direction_to_orientation[direction[0], direction_turn[0], direction_turn[1]]
		self._clockwise_rotations = (self._clockwise_rotations + 2) % 4

	def _turn_direction_270_x(self):
		if self._type == 2:
			direction = self._orientation_to_direction[(self._y, self._z)]
			self._y, self._z = self._direction_to_orientation[self._direction_turn_270[direction[0], direction[1]]]

		if self._type == 3:
			direction = self._orientation_to_direction[(self._x, self._y, self._z)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			direction_turn = self._direction_turn_270[direction[1], direction[2]]
			self._x, self._y, self._z = self._direction_to_orientation[direction[0], direction_turn[0], direction_turn[1]]
		self._clockwise_rotations = (self._clockwise_rotations + 2) % 4

	# ###  Turning Y Axis

	def _turn_direction_90_y(self):
		if self._type == 2:
			direction = self._orientation_to_direction[(self._y, self._z)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			self._y, self._z = self._direction_to_orientation[self._direction_turn_90[direction[0], direction[1]]]

		if self._type == 3:
			direction = self._orientation_to_direction[(self._x, self._y, self._z)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			direction_turn = self._direction_turn_90[direction[0], direction[2]]
			self._x, self._y, self._z = self._direction_to_orientation[direction_turn[0], direction[1], direction_turn[1]]

	def _turn_direction_270_y(self):
		if self._type == 2:
			direction = self._orientation_to_direction[(self._y, self._z)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			self._y, self._z = self._direction_to_orientation[self._direction_turn_270[direction[0], direction[1]]]

		if self._type == 3:
			direction = self._orientation_to_direction[(self._x, self._y, self._z)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			direction_turn = self._direction_turn_270[direction[0], direction[2]]
			self._x, self._y, self._z = self._direction_to_orientation[direction_turn[0], direction[1], direction_turn[1]]

	# ###  Turning Z Axis

	def _turn_direction_90_z(self):
		if self._type == 2:
			direction = self._orientation_to_direction[(self._y, self._z)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			self._y, self._z = self._direction_to_orientation[self._direction_turn_90[direction[0], direction[1]]]

		if self._type == 3:
			direction = self._orientation_to_direction[(self._x, self._y, self._z)]
			if direction[2] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			direction_turn = self._direction_turn_90[direction[0], direction[1]]
			self._x, self._y, self._z = self._direction_to_orientation[direction_turn[0], direction_turn[1], direction[2]]

	def _turn_direction_270_z(self):
		if self._type == 2:
			direction = self._orientation_to_direction[(self._y, self._z)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			self._y, self._z = self._direction_to_orientation[self._direction_turn_270[direction[0], direction[1]]]

		if self._type == 3:
			direction = self._orientation_to_direction[(self._x, self._y, self._z)]
			if direction[2] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			direction_turn = self._direction_turn_270[direction[0], direction[1]]
			self._x, self._y, self._z = self._direction_to_orientation[direction_turn[0], direction_turn[1], direction[2]]
