__author__ = 'Peter Hofmann'

import sys

from lib.bits_and_bytes import BitAndBytes
# from lib.blueprint.blueprintutils import BlueprintUtils


# DefaultLogging
class BlockOrientation(object):
	"""
	Type    	Bits    	Description

	Type1   	23 	22 	21 	The block facing
	"""
	# https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

	_bit_block_id_start = 0
	_bit_block_id_length = 12
	_bit_is_active_start = 12
	_bit_is_active_length = 1
	_bit_hit_points_start = 13
	_bit_hit_points_length = 8

	def __init__(self, logfile=None, verbose=False, debug=False):
		"""
		Constructor

		# Block styles:
		# 0: slabs/doors/weapons/station/logic/lighting/medical/factions/systems/effects/tools:
		# 1: Wedge
		# 2: Corner
		# 3: Rod/Paint/Capsules/Hardener/Plants/Shards
		# 4: Tetra
		# 5: Hepta
		# 6: Rail/Pickup/White Light Bar/Pipe/Decorative Console/Shipyard Module/Core Anchor/Mushroom/
		"""
		self._label = "BlockOrientation"
		# super(BlockOrientation, self).__init__(logfile=logfile, verbose=verbose, debug=debug)
		self._verbose = verbose
		self._debug = debug
		super(BlockOrientation, self).__init__()
		self._int_24bit = 0

	# #######################################
	# get
	# #######################################

	def get_int_24bit(self):
		"""
		Return integer representing block

		@rtype: int
		"""
		return self._int_24bit

	def get_id(self):
		"""
		Returns the block id

		@rtype: int
		"""
		return BitAndBytes.bits_parse(self._int_24bit, self._bit_block_id_start, self._bit_block_id_length)

	def get_style(self):
		"""
		Returns the block style

		@rtype: int | None
		"""
		# block_id = self.get_id()
		# if block_id == 0:
		# 	return None
		# return BlueprintUtils.get_block_style(block_id)
		return 0

	def _get_bit_19(self):
		return BitAndBytes.bits_parse(self._int_24bit, 19, 1)

	def _get_bit_22(self):
		return BitAndBytes.bits_parse(self._int_24bit, 22, 1)

	def _get_bit_23(self):
		return BitAndBytes.bits_parse(self._int_24bit, 23, 1)

	def _get_block_side_id(self):
		return BitAndBytes.bits_parse(self._int_24bit, 20, 3)

	def _get_clockwise_rotations(self):
		return BitAndBytes.bits_parse(self._int_24bit, 20, 2)

	# #######################################
	# set
	# #######################################

	def set_int_24bit(self, int_24bit):
		"""
		Set integer representing block

		@param int_24bit:
		@type int_24bit: int
		"""
		self._int_24bit = int_24bit

	def _bits_combine_orientation(self, new_int_24bit, style=None, block_side_id=None, bit_19=None, bit_22=None, bit_23=None, rotations=None):
		"""
		Set orientation bits of an integer

		@type new_int_24bit: int

		@rtype: int
		"""
		if style is None:
			style = self.get_style()
		if style == 0:
			if block_side_id is None:
				block_side_id = self._get_block_side_id()
			return BitAndBytes.bits_combine(block_side_id, new_int_24bit, 20)
		if style != 0:
			if bit_19 is None:
				bit_19 = self._get_bit_19()
			new_int_24bit = BitAndBytes.bits_combine(bit_19, new_int_24bit, 19)

		if rotations is None:
			rotations = self._get_clockwise_rotations()
		if bit_22 is None:
			bit_22 = self._get_bit_22()
		if bit_23 is None:
			bit_23 = self._get_bit_23()
		new_int_24bit = BitAndBytes.bits_combine(rotations, new_int_24bit, 20)
		new_int_24bit = BitAndBytes.bits_combine(bit_22, new_int_24bit, 22)
		new_int_24bit = BitAndBytes.bits_combine(bit_23, new_int_24bit, 23)
		return new_int_24bit

	# #######################################
	# ###  Turning - Experimental
	# #######################################

	#   -Y  	    Z   	   Z
	# -X   X	 -Y   Y 	-X   X
	#    Y  	   -Z   	  -Z

	_direction_turn_90_yz = {
		(1, 0): (0, -1),
		(0, -1): (-1, 0),
		(-1, 0): (1, 0),
	}
	# 		(0, 1): (-1, 0),

	_direction_turn_270_yz = {
		(1, 0): (-1, 0),
		(-1, 0): (0, -1),
		(0, -1): (1, 0),
	}

	_direction_turn_90_xyz = {
		(1, 0): (0, -1),
		(0, -1): (-1, 0),
		(-1, 0): (0, 1),
		(0, 1): (1, 0),
	}

	_direction_turn_270_xyz = {
		(1, 0): (0, 1),
		(0, 1): (-1, 0),
		(-1, 0): (0, -1),
		(0, -1): (1, 0),
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

	def _orientation_to_stream(self, output_stream=sys.stdout):
		"""

		@param output_stream:
		@type output_stream: FileIO
		"""
		output_stream.write(self._orientation_to_string())

	def _orientation_to_string(self):
		"""
		Return orientation data as string

		@rtype: str
		"""
		if self._debug:
			return self._bit_orientation_to_string()

		if self.get_style == 0:
			return "Side: {}".format(self._block_side_id_to_str[self._get_block_side_id()])

		side = self._get_side_from_direction()
		return_string = ""
		return_string += "Side: {}".format(self._block_side_id_to_str[side])
		return_string += " {}* ".format(self._get_clockwise_rotations() * 90)
		return return_string

	def _bit_orientation_to_string(self):
		return_string = ""
		# return_string += "{}\t".format(self._orientation)
		return_string += "({},{},{}) ".format(self._get_bit_19(), self._get_bit_23(), self._get_bit_22())
		rotation = "{}*".format(self._get_clockwise_rotations() * 90)
		return_string += rotation.rjust(4) + "\t"
		return_string += "F {}".format(self._get_block_side_id())
		return return_string

	def _get_side_from_direction(self):
		"""

		@rtype: int
		"""
		orientation = (self._get_bit_19(), self._get_bit_23(), self._get_bit_22())
		if self.get_style == 1:  # wedge
			orientation = (0, self._get_bit_23(), self._get_bit_22())
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

	# def turn_upside_down(self):
	# 	if self._type == 1:
	# 		self._turn_facing_180()
	# 		return
	# 	self._turn_direction_180()
	#
	# def turn_180(self):
	# 	if self._type == 1:
	# 		self._turn_facing_180()
	# 		return
	# 	self._turn_direction_180()

	def turn_90_x(self):
		if self.get_style() == 1:
			self._turn_facing_90_x()
			return
		self._turn_direction_270_x()

	def turn_270_x(self):
		if self.get_style() == 1:
			self._turn_facing_270_x()
			return
		self._turn_direction_90_x()

	def turn_90_y(self):
		if self.get_style() == 1:
			self._turn_facing_90_y()
			return
		self._turn_direction_90_y()

	def turn_270_y(self):
		if self.get_style() == 1:
			self._turn_facing_270_y()
			return
		self._turn_direction_270_y()

	def turn_90_z(self):
		if self.get_style() == 1:
			self._turn_facing_90_z()
			return
		self._turn_direction_90_z()

	def turn_270_z(self):
		if self.get_style() == 1:
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
		if self.get_style() == 2:
			direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
			self._bit_23, self._bit_22 = self._direction_to_orientation[(-1*direction[0], -1*direction[1])]

		if self.get_style() == 3:
			direction = self._orientation_to_direction[(self._bit_19, self._bit_23, self._bit_22)]
			self._bit_19, self._bit_23, self._bit_22 = self._direction_to_orientation[(-1*direction[0], -1*direction[1], -1*direction[2])]

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
		if self.get_style() == 2:
			if self._orientation == 0:
				direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
				self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_270_yz[direction[0], direction[1]]]
				return
			direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
			self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_90_yz[direction[0], direction[1]]]

		if self.get_style() == 3:
			direction = self._orientation_to_direction[(self._bit_19, self._bit_23, self._bit_22)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			direction_turn = self._direction_turn_270_xyz[direction[1], direction[2]]
			new_bits = self._direction_to_orientation[direction[0], direction_turn[0], direction_turn[1]]
			# print (self._bit_19, self._bit_23, self._bit_22), new_bits, "\t", direction, direction_turn
			self._bit_19, self._bit_23, self._bit_22 = new_bits
		self._clockwise_rotations = (self._clockwise_rotations + 1) % 4

	def _turn_direction_270_x(self):
		if self.get_style() == 2:
			if self._orientation == 8:
				direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
				self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_90_yz[direction[0], direction[1]]]
				return
			direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
			self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_270_yz[direction[0], direction[1]]]

		if self.get_style() == 3:
			direction = self._orientation_to_direction[(self._bit_19, self._bit_23, self._bit_22)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			direction_turn = self._direction_turn_90_xyz[direction[1], direction[2]]
			new_bits = self._direction_to_orientation[direction[0], direction_turn[0], direction_turn[1]]
			# print (self._bit_19, self._bit_23, self._bit_22), new_bits, "\t", direction, direction_turn
			self._bit_19, self._bit_23, self._bit_22 = new_bits
		self._clockwise_rotations = (self._clockwise_rotations + 3) % 4

	# ###  Turning Y Axis

	def _turn_direction_90_y(self):
		if self.get_style() == 2:
			direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_90_z[direction[0], direction[1]]]

		if self.get_style() == 3:
			direction = self._orientation_to_direction[(self._bit_19, self._bit_23, self._bit_22)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			direction_turn = self._direction_turn_90_z[direction[0], direction[2]]
			self._bit_19, self._bit_23, self._bit_22 = self._direction_to_orientation[direction_turn[0], direction[1], direction_turn[1]]

	def _turn_direction_270_y(self):
		if self.get_style() == 2:
			direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
			if direction[0] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_270_z[direction[0], direction[1]]]

		if self.get_style() == 3:
			direction = self._orientation_to_direction[(self._bit_19, self._bit_23, self._bit_22)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			direction_turn = self._direction_turn_270_z[direction[0], direction[2]]
			self._bit_19, self._bit_23, self._bit_22 = self._direction_to_orientation[direction_turn[0], direction[1], direction_turn[1]]

	# ###  Turning Z Axis

	def _turn_direction_90_z(self):
		if self.get_style() == 2:
			direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_90_z[direction[0], direction[1]]]

		if self.get_style() == 3:
			direction = self._orientation_to_direction[(self._bit_19, self._bit_23, self._bit_22)]
			if direction[2] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 1) % 4
				return
			direction_turn = self._direction_turn_90_xy[direction[0], direction[1]]
			self._bit_19, self._bit_23, self._bit_22 = self._direction_to_orientation[direction_turn[0], direction_turn[1], direction[2]]

	def _turn_direction_270_z(self):
		if self.get_style() == 2:
			direction = self._orientation_to_direction[(self._bit_23, self._bit_22)]
			if direction[1] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			self._bit_23, self._bit_22 = self._direction_to_orientation[self._direction_turn_270_z[direction[0], direction[1]]]

		if self.get_style() == 3:
			direction = self._orientation_to_direction[(self._bit_19, self._bit_23, self._bit_22)]
			if direction[2] != 0:
				self._clockwise_rotations = (self._clockwise_rotations + 3) % 4
				return
			direction_turn = self._direction_turn_270_xy[direction[0], direction[1]]
			self._bit_19, self._bit_23, self._bit_22 = self._direction_to_orientation[direction_turn[0], direction_turn[1], direction[2]]
