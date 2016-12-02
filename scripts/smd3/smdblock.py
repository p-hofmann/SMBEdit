__author__ = 'Peter Hofmann'

import sys
import struct
from scripts.bit_and_bytes import BitAndBytes
from scripts.blueprintutils import BlueprintUtils


class SmdBlock(BitAndBytes, BlueprintUtils):

	# https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data
	_block_type = {
		1: (0, 11, 20, 21),
		2: (0, 11, 20, 20),  # no active bit
		3: (0, 11, 19, 19),  # no active bit
	}

	def __init__(self):
		self._label = "SmdBlock"
		# todo: take _block_type into account
		super(SmdBlock, self).__init__()
		self._id = 0
		self._hitpoints = 0
		self._active = 0
		self._orientation = 0
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

		@rtype: int
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
		@type value: int
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
		self._id = self.parse_bits(bit_array, 0, 11)
		self._hitpoints = self.parse_bits(bit_array, 11, 9)
		self._active = self.parse_bits(bit_array, 20, 1)  # For blocks with an activation status
		self._orientation = self.parse_bits(bit_array, 21, 3)

	def _refresh_data_byte_string(self):
		"""
		In the rare case a block value is changed, they are turned into a byte string.
		'[1:]' since only the last three bytes of an integer are used for block information.
		"""
		bit_array = 0
		bit_array = self.combine_bits(self._id, bit_array, 0)
		bit_array = self.combine_bits(self._hitpoints, bit_array, 11)
		bit_array = self.combine_bits(self._active, bit_array, 20)  # For blocks with an activation status
		bit_array = self.combine_bits(self._orientation, bit_array, 21)
		self._byte_string = struct.pack('>i', bit_array)[1:]

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream block values

		@param output_stream:
		@type output_stream: fileIO
		"""
		output_stream.write("HP: {}\t".format(self._hitpoints))
		output_stream.write("Active: {}\t".format(self._active))
		output_stream.write("Or.: {}\t".format(self._orientation))
		output_stream.write("{}\n".format(self.get_block_name_by_id(self._id)))
