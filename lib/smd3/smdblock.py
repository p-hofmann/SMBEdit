__author__ = 'Peter Hofmann'

import sys
import struct
from lib.bits_and_bytes import BitAndBytes
from lib.blueprintutils import BlueprintUtils
from lib.smd3.blockorientation import BlockOrientation


class SmdBlock(BlockOrientation, BitAndBytes, BlueprintUtils):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "SmdBlock"
		super(SmdBlock, self).__init__(logfile=logfile, verbose=verbose, debug=debug)
		self._style = 0
		self._id = 0
		self._hit_points = 0
		self._active = 0
		self._byte_string = ""

	def get_id(self):
		"""
		Returns the block id

		@rtype: int
		"""
		return self._id

	def get_hit_points(self):
		"""
		Returns the hit points of the block

		@rtype: int
		"""
		return self._hit_points

	def is_active(self):
		"""
		Returns the 'active' status.

		@rtype: int
		"""
		if self._style != 0:
			return False
		return self._active == 0

	def set_id(self, block_id):
		"""
		Change block id of block

		@param block_id:
		@type block_id: int
		"""
		self._id = block_id
		self._style = self.get_block_style(self._id)
		self._refresh_data_byte_string()

	def set_hit_points(self, value):
		"""
		Change hit points of block

		@param value:
		@type value: int
		"""
		self._hit_points = value
		self._refresh_data_byte_string()

	def set_active(self, value):
		"""
		Change 'active' status of of block

		@param value:
		@type value: bool
		"""
		assert self._style == 0, "Block id {} has no 'active' status".format(self._id)
		if value:
			self._active = 0
		else:
			self._active = 1
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
		if self._id == 0:
			return
		self._style = self.get_block_style(self._id)
		self._hit_points = self.bits_parse(int_24bit, 11, 8)
		if self._style == 0:  # For blocks with an activation status
			self._active = self.bits_parse(int_24bit, 19, 1)
		self._set_int_24bit(int_24bit)

	def _refresh_data_byte_string(self):
		"""
		In the rare case a block value is changed, they are turned into a byte string.
		"""
		int_24bit = 0
		int_24bit = self.bits_combine(self._id, int_24bit, 0)
		int_24bit = self.bits_combine(self._hit_points, int_24bit, 11)
		if self._style == 1:  # For blocks with an activation status
			int_24bit = self.bits_combine(self._active, int_24bit, 19)
		int_24bit = self._get_int_24bit(int_24bit)
		# '[1:]' since only the last three bytes of an integer are used for block information.
		self._byte_string = struct.pack('>i', int_24bit)[1:]
		self._parse_byte_string()

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
		self.turn_270_x()

	def tilt_down(self):
		self.turn_90_x()

	def turn_right(self):
		self.turn_90_y()

	def turn_left(self):
		self.turn_270_y()

	def tilt_right(self):
		self.turn_90_z()

	def tilt_left(self):
		self.turn_270_z()

	# #######################################
	# ###  Stream
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream block values

		@param output_stream:
		@type output_stream: fileIO
		"""
		output_stream.write("({})\t".format(self._style))
		output_stream.write("HP: {}\t".format(self._hit_points))
		output_stream.write("Active: {}\t".format(self.is_active()))
		output_stream.write("Or.: {}\t".format(self._orientation_to_string()))
		output_stream.write("{}\n".format(self.get_block_name_by_id(self._id)))
