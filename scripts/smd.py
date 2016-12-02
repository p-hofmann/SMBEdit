__author__ = 'Peter Hofmann'

import sys
import os
import math
from scripts.loggingwrapper import DefaultLogging
from blueprintutils import BlueprintUtils
from smd3.smdregion import SmdRegion
from smd3.smdblock import SmdBlock


class Smd(DefaultLogging, BlueprintUtils):

	# #######################################
	# ###  smd
	# #######################################

	def __init__(
		self, segments_in_a_line_of_a_region=16, blocks_in_a_line_of_a_segment=32, logfile=None, verbose=False, debug=False):
		self._label = "Smd"
		super(Smd, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		self._blocks_in_a_line_in_a_segment = blocks_in_a_line_of_a_segment
		self._segments_in_a_line_of_a_region = segments_in_a_line_of_a_region
		self._file_name_prefix = ""
		self.position_to_region = {}
		return

	# #######################################
	# ###  Read
	# #######################################

	def read(self, directory_blueprint):
		"""

		@param directory_blueprint:
		@type directory_blueprint: str
		"""
		directory_data = os.path.join(directory_blueprint, "DATA")
		file_list = sorted(os.listdir(directory_data))
		for file_name in file_list:
			file_path = os.path.join(directory_data, file_name)
			self._file_name_prefix, x, y, z = os.path.splitext(file_name)[0].rsplit('.', 3)
			position = (int(x), int(y), int(z))
			self.position_to_region[position] = SmdRegion(
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug)
			self.position_to_region[position].read(file_path)

	# #######################################
	# ###  Write
	# #######################################

	def write(self, directory_blueprint, blueprint_name):
		"""

		@param directory_blueprint:
		@type directory_blueprint: str
		@param blueprint_name:
		@type blueprint_name: str
		"""
		directory_data = os.path.join(directory_blueprint, "DATA")
		if not os.path.exists(directory_data):
			os.mkdir(directory_data)
		# print self.position_to_region.keys()
		for position, region in self.position_to_region.iteritems():
			assert isinstance(region, SmdRegion)
			file_name = blueprint_name + "." + ".".join(map(str, position)) + ".smd3"
			file_path = os.path.join(directory_data, file_name)
			region.write(file_path)

	# #######################################
	# ###  Index and positions
	# #######################################

	def get_region_position_of_position(self, position):
		"""
		Return the position of a segment a position belongs to.

		@param position: Any global position like that of a block
		@type position: int, int, int

		@return:
		@rtype: int, int, int
		"""
		return self._get_region_position_of(position[0]), self._get_region_position_of(position[1]), self._get_region_position_of(position[2])

	def _get_region_position_of(self, value):
		"""
		Return the segment coordinate

		@param value: any x or y or z coordinate
		@param value: int

		@return: segment x or y or z coordinate
		@rtype: int
		"""
		blocks_in_a_line_in_a_region = self._blocks_in_a_line_in_a_segment * self._segments_in_a_line_of_a_region
		return int(math.floor((value+blocks_in_a_line_in_a_region/2) / float(blocks_in_a_line_in_a_region)))

	# #######################################
	# ###  Else
	# #######################################

	def get_number_of_blocks(self):
		"""

		@rtype: int
		"""
		number_of_blocks = 0
		for position, region in self.position_to_region.iteritems():
			assert isinstance(region, SmdRegion)
			number_of_blocks += region.get_number_of_blocks()
		return number_of_blocks

	def update(self, entity_type=0):
		"""

		@param entity_type:
		@type entity_type: int
		"""
		for position_region in self.position_to_region.keys():
			region = self.position_to_region[position_region]
			assert isinstance(region, SmdRegion)
			region.update(entity_type)
		self._remove_empty_regions()

	def _remove_empty_regions(self):
		list_of_position_region = self.position_to_region.keys()
		for position_region in list_of_position_region:
			if self.position_to_region[position_region].get_number_of_blocks() == 0:
				self._logger.debug("'remove' Removing empty region {}.".format(position_region))
				self.position_to_region.pop(position_region)

	def remove_block(self, block_position):
		"""

		@param block_position:
		@type block_position: tuple(int,int,int)
		"""
		assert isinstance(block_position, tuple), block_position
		position_region = self.get_region_position_of_position(block_position)
		assert position_region in self.position_to_region, block_position
		self.position_to_region[position_region].remove_block(block_position)

	def add(self, block_position, block_data):
		"""

		@param block_position:
		@type block_position: tuple(int,int,int)
		@param block_data:
		@type block_data: SmdBlock
		"""
		assert isinstance(block_position, tuple)
		position_region = self.get_region_position_of_position(block_position)
		if position_region not in self.position_to_region:
			self.position_to_region[position_region] = SmdRegion(
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug)
		self.position_to_region[position_region].add(block_position, block_data)

	def search(self, block_id):
		"""

		@param block_id:
		@type block_id: int
		"""
		for position, region in self.position_to_region.iteritems():
			block_position = region.search(block_id)
			if block_position is not None:
				return block_position
		return None

	def get_block_id_to_quantity(self):
		"""

		@rtype: dict[int, int]
		"""
		block_id_to_quantity = {}
		for position, block in self.iteritems():
			if block.get_id() not in block_id_to_quantity:
				block_id_to_quantity[block.get_id()] = 0
			block_id_to_quantity[block.get_id()] += 1
		return block_id_to_quantity

	def iteritems(self):
		"""

		@rtype: tuple(tuple[int,int,int], SmdBlock)
		"""
		for position_region, region in self.position_to_region.iteritems():
			assert isinstance(region, SmdRegion), type(region)
			for position_block, block in region.iteritems():
				assert isinstance(block, SmdBlock), type(block)
				yield position_block, block

	def move_center(self, direction_vector):
		"""

		@param direction_vector:
		@type direction_vector: tuple[int,int,int]

		@rtype: tuple[tuple[int,int,int],tuple[int,int,int]]
		"""
		new_smd = Smd()
		min_vector = [16, 16, 16]
		max_vector = [16, 16, 16]
		for position_block, block in self.iteritems():
			assert isinstance(block, SmdBlock)
			new_block_position = self.vector_subtraction(position_block, direction_vector)
			if block.get_id() == 1:  # core
				new_block_position = position_block
			new_smd.add(new_block_position, block)

			for index, value in enumerate(new_block_position):
				if value < min_vector[index]:
					min_vector[index] = value
				if value > max_vector[index]:
					max_vector[index] = value
		del self.position_to_region
		self.position_to_region = new_smd.position_to_region
		return tuple(min_vector), tuple(max_vector)

	def get_min_max_vector(self):
		"""

		@rtype: tuple[tuple[int,int,int],tuple[int,int,int]]
		"""
		min_vector = [16, 16, 16]
		max_vector = [16, 16, 16]
		for position_block, block in self.iteritems():
			assert isinstance(block, SmdBlock)
			for index, value in enumerate(position_block):
				if value < min_vector[index]:
					min_vector[index] = value
				if value > max_vector[index]:
					max_vector[index] = value
		return tuple(min_vector), tuple(max_vector)

	def set_type(self, entity_type):
		"""
		0: "Ship",

		@param entity_type:
		@type entity_type: int
		"""
		assert isinstance(entity_type, (int, long))
		assert 0 <= entity_type <= 4

		position_core = (16, 16, 16)
		if entity_type == 0:  # Ship
			core_block = SmdBlock()
			core_block.set_id(1)
			core_block.set_hitpoints(250)
			core_block.set_active(False)
			core_block.set_orientation(0)
			self.add(position_core, core_block)
		else:  # not a ship
			try:
				self.remove_block(position_core)
			except AssertionError as exception_object:
				self._logger.debug("'set_type' exception: {}".format(exception_object.message))
		self.update(entity_type)  # remove blocks invalid for ships and other cleanup

	def to_stream(self, output_stream=sys.stdout, summary=True):
		"""

		@param output_stream:
		@type output_stream: fileIO
		@param summary:
		@type summary: bool
		"""
		output_stream.write("####\nSMD\n####\n\n")
		output_stream.write("Blocks: {}\n".format(self.get_number_of_blocks()))
		for position in sorted(self.position_to_region.keys(), key=lambda tup: (tup[2], tup[1], tup[0])):
			output_stream.write("SmdRegion: {}\n".format(list(position)))
			self.position_to_region[position].to_stream(output_stream, summary)
			output_stream.write("\n")
