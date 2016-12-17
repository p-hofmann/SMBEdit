__author__ = 'Peter Hofmann'

import sys
import struct
from scripts.bit_and_bytes import BitAndBytes
from scripts.blueprintutils import BlueprintUtils
from scripts.smd3.blockorientation import BlockOrientation


class SmdBlock(BitAndBytes, BlueprintUtils):

	# https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

	# ZR.classs	-	logic blocks only?
	# public final short a() { return (short)ByteUtil.a(ByteUtil.a(this.a, 0), 0, 11); }
	# public final int a() { return (short)ByteUtil.a(ByteUtil.a(this.a, 0), 11, 19); }
	# public final void a(int var1) { ByteUtil.a(this.a, var1, 11, 19); }
	# public final boolean a() { return ByteUtil.a(ByteUtil.a(this.a, 0), 19, 20) == 0; }
	# public final void a(boolean var1) { ByteUtil.a(this.a, var1?0:1, 19, 20); }
	# public final byte b() { return (byte)ByteUtil.a(ByteUtil.a(this.a, 0), 20, 24); }

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
		if self._type != 1:
			return False
		return self._active == 0

	def get_orientation(self):
		"""
		Returns the orientation of the block as integer.

		@rtype: BlockOrientation
		"""
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
			self._active = 0
		else:
			self._active = 1
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
		int_24bit = struct.unpack('>i', '\x00' + self._byte_string)[0]
		# bit_array = ByteStream.unpack('\x00' + self._byte_string, 'i')
		self._id = self.bits_parse(int_24bit, 0, 11)
		self._refresh_block_type()
		self._hitpoints = self.bits_parse(int_24bit, 11, 8)
		if self._type == 1:  # For blocks with an activation status
			self._active = self.bits_parse(int_24bit, 19, 1)
		self._orientation = BlockOrientation(self._type)
		self._orientation.set_int_24bit(int_24bit)

	def _refresh_data_byte_string(self):
		"""
		In the rare case a block value is changed, they are turned into a byte string.
		"""
		int_24bit = 0
		int_24bit = self.bits_combine(self._id, int_24bit, 0)
		int_24bit = self.bits_combine(self._hitpoints, int_24bit, 11)
		if self._type == 1:  # For blocks with an activation status
			int_24bit = self.bits_combine(self._active, int_24bit, 19)
		int_24bit = self._orientation.get_int_24bit(int_24bit)
		# '[1:]' since only the last three bytes of an integer are used for block information.
		self._byte_string = struct.pack('>i', int_24bit)[1:]

	def _refresh_block_type(self):
		"""
		When the block id changes, its type might be different too and must be found out
		"""
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
		output_stream.write("Active: {}\t".format(self.is_active()))
		output_stream.write("Or.: {}\t".format(self._orientation.to_string()))
		output_stream.write("{}\n".format(self.get_block_name_by_id(self._id)))

	# #######################################
	# ###  Turning
	# #######################################

	def tilt_turn(self, index):
		"""
		Turn the block.

		@attention: This does not work right, yet.

		@param index: index representing a specific turn
		@type index: int
		"""
		if index == 0:
			self.tilt_up()
		elif index == 1:
			self.tilt_down()
		elif index == 2:
			self.turn_right()
		elif index == 3:
			self.turn_left()
		elif index == 4:
			self.tilt_right()
		elif index == 5:
			self.tilt_left()
		self._refresh_data_byte_string()

	def tilt_up(self):
		self._orientation.turn_90_x()

	def tilt_down(self):
		self._orientation.turn_270_x()

	def turn_right(self):
		self._orientation.turn_90_y()

	def turn_left(self):
		self._orientation.turn_270_y()

	def tilt_right(self):
		self._orientation.turn_90_z()

	def tilt_left(self):
		self._orientation.turn_270_z()
