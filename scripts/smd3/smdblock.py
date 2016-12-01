__author__ = 'Peter Hofmann'

import sys
import struct
from scripts.bit_and_bytes import BitAndBytes
from scripts.blueprintutils import BlueprintUtils


class SmdBlock(BitAndBytes, BlueprintUtils):

	_label = "SmdBlock"

	def __init__(self):
		super(SmdBlock, self).__init__()
		self._id = 0
		self._hitpoints = 0
		self._active = 0
		self._orientation = 0
		self._byte_string = ""

	def get_id(self):
		return self._id

	def get_hitpoints(self):
		return self._hitpoints

	def is_active(self):
		return self._active == 1

	def get_orientation(self):
		return self._orientation

	def set_id(self, value):
		"""

		@param value:
		@type value: int
		"""
		self._id = value
		self._refresh_data_byte_string()

	def set_hitpoints(self, value):
		"""

		@param value:
		@type value: int
		"""
		self._hitpoints = value
		self._refresh_data_byte_string()

	def set_active(self, value):
		"""

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

		@param value:
		@type value: int
		"""
		self._orientation = value
		self._refresh_data_byte_string()

	def set_data_byte_string(self, byte_string):
		"""

		@param byte_string:
		@type byte_string: str
		"""
		self._byte_string = byte_string
		self._parse_byte_string()

	def get_data_byte_string(self):
		"""

		@rtype: str
		"""
		return self._byte_string

	def _parse_byte_string(self):
		# bit_array = self._read_int24_unassigned(input_stream)
		bit_array = struct.unpack('>i', '\x00' + self._byte_string)[0]
		self._id = self.parse_bits(bit_array, 0, 11)
		self._hitpoints = self.parse_bits(bit_array, 11, 9)
		self._active = self.parse_bits(bit_array, 20, 1)
		self._orientation = self.parse_bits(bit_array, 21, 3)

	def _refresh_data_byte_string(self):
		bit_array = 0
		bit_array = self.combine_bits(self._id, bit_array, 0)
		bit_array = self.combine_bits(self._hitpoints, bit_array, 11)
		bit_array = self.combine_bits(self._active, bit_array, 20)
		bit_array = self.combine_bits(self._orientation, bit_array, 21)
		self._byte_string = struct.pack('>i', bit_array)[1:]

	def to_stream(self, output_stream=sys.stdout):
		"""

		@param output_stream:
		@type output_stream: fileIO
		"""
		output_stream.write("HP: {}\t".format(self._hitpoints))
		output_stream.write("Active: {}\t".format(self._active))
		output_stream.write("Or.: {}\t".format(self._orientation))
		output_stream.write("{}\n".format(self.get_block_name_by_id(self._id)))
