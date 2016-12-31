__author__ = 'Peter Hofmann'

import sys
from lib.bits_and_bytes import BitAndBytes
from lib.blueprintutils import BlueprintUtils
from lib.smd3.blockorientation import BlockOrientation


class SmdBlock(BlockOrientation):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "SmdBlock"
		super(SmdBlock, self).__init__(logfile=logfile, verbose=verbose, debug=debug)

	# Get

	def get_hit_points(self):
		"""
		Returns the hit points of the block

		@rtype: int
		"""
		if self.get_id() == 0:
			return None
		return BitAndBytes.bits_parse(self._int_24bit, 11, 8)

	def is_active(self):
		"""
		Returns the 'active' status.

		@rtype: bool
		"""
		style = self.get_style
		if style != 0 or style is None:
			return False
		return self._get_active_value() == 0

	def _get_active_value(self):
		"""
		Returns the 'active' bit value.

		@rtype: bool
		"""
		return BitAndBytes.bits_parse(self._int_24bit, 19, 1)

	# Set

	def update(self, block_id=None, hit_points=None, active=None):
		"""
		In the rare case a block value is changed, they are turned into a byte string.

		@type block_id: int | None
		@type hit_points: int | None
		@type active: bool | None
		"""
		if block_id is None:
			block_id = self.get_id()
		elif block_id == 0:
			self._int_24bit = 0
			return

		if hit_points is None:
			hit_points = self.get_hit_points()

		if active is None:
			active = self._get_active_value()
		elif active:
			active = 0
		elif not active:
			active = 1

		style = BlueprintUtils.get_block_style(block_id)
		int_24bit = 0
		int_24bit = BitAndBytes.bits_combine(block_id, int_24bit, 0)
		int_24bit = BitAndBytes.bits_combine(hit_points, int_24bit, 11)
		if style == 1:  # For blocks with an activation status
			int_24bit = BitAndBytes.bits_combine(active, int_24bit, 19)
		self._int_24bit = self._bits_combine_orientation(int_24bit)
		# '[1:]' since only the last three bytes of an integer are used for block information.
		# self._byte_string = struct.pack('>i', int_24bit)[1:]

	def set_id(self, block_id):
		"""
		Change block id of block

		@param block_id:
		@type block_id: int
		"""
		self.update(block_id=block_id)

	def set_hit_points(self, hit_points):
		"""
		Change hit points of block

		@param hit_points:
		@type hit_points: int
		"""
		self.update(hit_points=hit_points)

	def set_active(self, active):
		"""
		Change 'active' status of of block

		@param active:
		@type active: bool
		"""
		assert self.get_style() == 0, "Block id {} has no 'active' status".format(self.get_id())
		self.update(active=active)

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
		output_stream.write("({})\t".format(self.get_style()))
		output_stream.write("HP: {}\t".format(self.get_hit_points()))
		output_stream.write("Active: {}\t".format(self.is_active()))
		output_stream.write("Or.: {}\t".format(self._orientation_to_string()))
		output_stream.write("{}\n".format(BlueprintUtils.get_block_name_by_id(self.get_id())))
