__author__ = 'Peter Hofmann'

import sys
import os
import math
from lib.loggingwrapper import DefaultLogging
from lib.blueprintutils import BlueprintUtils
from lib.smd3.smdregion import SmdRegion
from lib.smd3.smdblock import SmdBlock


class Smd(DefaultLogging, BlueprintUtils):
	"""
	# #######################################
	# ###  smd
	# #######################################

	@type position_to_region: dict[tuple[int], SmdRegion]
	"""

	def __init__(
		self, segments_in_a_line_of_a_region=16, blocks_in_a_line_of_a_segment=32, logfile=None, verbose=False, debug=False):
		"""
		Constructor

		@param blocks_in_a_line_of_a_segment: The number of blocks that fit beside each other within a segment
		@type blocks_in_a_line_of_a_segment: int
		@param segments_in_a_line_of_a_region: The number of segments that fit beside each other within a region
		@type segments_in_a_line_of_a_region: int
		"""
		self._label = "Smd3"
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
		Read smd data from files in the blueprint/data/ directory

		@param directory_blueprint: input directory path
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
		Write smd data to files in the blueprint/data/ directory

		@param directory_blueprint: output directory path
		@type directory_blueprint: str
		@param blueprint_name: name of blueprint
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
	# ###  Get
	# #######################################

	def get_block_at_position(self, position):
		"""
		Get a block at a specific position

		@param position:
		@param position: tuple[int]

		@return:
		@rtype: SmdBlock
		"""
		region_position = self.get_region_position_of_position(position)
		assert region_position in self.position_to_region
		return self.position_to_region[region_position].get_block_at_position(position)

	# ###  Index and positions

	def get_region_position_of_position(self, position):
		"""
		Return the position of a region a position belongs to.

		@param position: Any global position like that of a block
		@type position: int, int, int

		@return:
		@rtype: int, int, int
		"""
		return (
			self._get_region_position_of(position[0]),
			self._get_region_position_of(position[1]),
			self._get_region_position_of(position[2]))

	def _get_region_position_of(self, value):
		"""
		Return the region coordinate

		@param value: any x or y or z coordinate
		@param value: int

		@return: segment x or y or z coordinate
		@rtype: int
		"""
		blocks_in_a_line_in_a_region = self._blocks_in_a_line_in_a_segment * self._segments_in_a_line_of_a_region
		return int(math.floor((value+blocks_in_a_line_in_a_region/2) / float(blocks_in_a_line_in_a_region)))

	# #######################################
	# ###  moving blocks
	# #######################################

	def move_center(self, direction_vector, entity_type):
		"""
		Move center (core) in a specific direction

		@param direction_vector: (x,y,z)
		@type direction_vector: int,int,int

		@return: new minimum and maximum coordinates of the blueprint
		@rtype: tuple[int,int,int], tuple[int,int,int]
		"""
		new_smd = Smd(
			segments_in_a_line_of_a_region=self._segments_in_a_line_of_a_region,
			blocks_in_a_line_of_a_segment=self._blocks_in_a_line_in_a_segment,
			logfile=self._logfile,
			verbose=self._verbose,
			debug=self._debug)
		min_vector = [16, 16, 16]
		max_vector = [16, 16, 16]
		for position_block, block in self.iteritems():
			assert isinstance(block, SmdBlock)
			new_block_position = self.vector_subtraction(position_block, direction_vector)
			if entity_type == 0 and new_block_position == (16, 16, 16):
				continue
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

	# #######################################
	# ###  Turning
	# #######################################

	def tilt_turn(self, tilt_index):
		"""
		Turn or tilt this entity.

		@param tilt_index: integer representing a specific turn
		@type tilt_index: int

		@return: new minimum and maximum coordinates of the blueprint
		@rtype: tuple[int,int,int], tuple[int,int,int]
		"""
		new_smd = Smd(
			segments_in_a_line_of_a_region=self._segments_in_a_line_of_a_region,
			blocks_in_a_line_of_a_segment=self._blocks_in_a_line_in_a_segment,
			logfile=self._logfile,
			verbose=self._verbose,
			debug=self._debug)
		min_vector = [16, 16, 16]
		max_vector = [16, 16, 16]
		for position_block, block in self.iteritems():
			assert isinstance(block, SmdBlock)
			new_block_position = position_block
			if block.get_id() != 1:  # core
				new_block_position = self._tilt_turn_position(position_block, tilt_index)
				# block.tilt_turn(tilt_index)  # todo: needs fixing
			new_smd.add(new_block_position, block)

			for index, value in enumerate(new_block_position):
				if value < min_vector[index]:
					min_vector[index] = value
				if value > max_vector[index]:
					max_vector[index] = value
		del self.position_to_region
		self.position_to_region = new_smd.position_to_region
		return tuple(min_vector), tuple(max_vector)

	# #######################################
	# ###  Else
	# #######################################

	def get_number_of_blocks(self):
		"""
		Get number of blocks of this region

		@return: number of blocks in segment
		@rtype: int
		"""
		number_of_blocks = 0
		for position, region in self.position_to_region.iteritems():
			assert isinstance(region, SmdRegion)
			number_of_blocks += region.get_number_of_blocks()
		return number_of_blocks

	def replace_hull(self, new_hull_type, hull_type=None):
		"""
		Replace all blocks of a specific hull type or all hull

		@param new_hull_type:
		@type new_hull_type: int
		@param hull_type:
		@type hull_type: int | None
		"""
		for region_position in self.position_to_region.keys():
			self.position_to_region[region_position].replace_hull(new_hull_type, hull_type)

	def replace_blocks(self, block_id, replace_id, replace_hp, compatible=False):
		"""
		Replace all blocks of a specific id
		"""
		for region_position in self.position_to_region.keys():
			self.position_to_region[region_position].replace_blocks(block_id, replace_id, replace_hp, compatible)

	def update(self, entity_type=0):
		"""
		Remove invalid/outdated blocks and exchange docking modules with rails

		@param entity_type: ship=0/station=2/etc
		@type entity_type: int
		"""
		for position_region in self.position_to_region.keys():
			region = self.position_to_region[position_region]
			assert isinstance(region, SmdRegion)
			region.update(entity_type)
		self._remove_empty_regions()

	def _remove_empty_regions(self):
		"""
		Search for and remove regions with no blocks
		"""
		list_of_position_region = self.position_to_region.keys()
		for position_region in list_of_position_region:
			if self.position_to_region[position_region].get_number_of_blocks() == 0:
				self._logger.debug("'remove' Removing empty region {}.".format(position_region))
				self.position_to_region.pop(position_region)

	def remove_block(self, block_position):
		"""
		Remove Block at specific position.

		@param block_position: x,z,y position of a block
		@type block_position: int,int,int
		"""
		assert isinstance(block_position, tuple), block_position
		position_region = self.get_region_position_of_position(block_position)
		assert position_region in self.position_to_region, block_position
		self.position_to_region[position_region].remove_block(block_position)

	def add(self, block_position, block):
		"""
		Add a block to the segment based on its global position

		@param block_position: x,y,z position of block
		@type block_position: int,int,int
		@param block: A block! :)
		@type block: SmdBlock
		"""
		assert isinstance(block_position, tuple)
		position_region = self.get_region_position_of_position(block_position)
		if position_region not in self.position_to_region:
			self.position_to_region[position_region] = SmdRegion(
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug)
		self.position_to_region[position_region].add(block_position, block)

	def search(self, block_id):
		"""
		Search and return the global position of the first occurrence of a block
		If no block is found, return None

		@param block_id: Block id as found in utils class
		@type block_id: int

		@return: None or (x,y,z)
		@rtype: None | int,int,int
		"""
		for position, region in self.position_to_region.iteritems():
			block_position = region.search(block_id)
			if block_position is not None:
				return block_position
		return None

	def search_all(self, block_id):
		"""
		Search and return the global position of block positions

		@param block_id: Block id as found in utils class
		@type block_id: int

		@return: None or (x,y,z)
		@rtype: set[tuple[int]]
		"""
		positions = set()
		for position, region in self.position_to_region.iteritems():
			positions = positions.union(region.search_all(block_id))
		return positions

	def has_block_at_position(self, position):
		"""
		Returns true if a block exists at a position

		@param position: (x,y,z)
		@type position: int,int,int

		@return:
		@rtype: bool
		"""
		region_position = self.get_region_position_of_position(position)
		if region_position not in self.position_to_region:
			return False
		return self.position_to_region[region_position].has_block_at_position(position)

	def get_block_id_to_quantity(self):
		"""
		Return the quantity of each block type

		@return: dictionary of block id to the quantity of that block type
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
		Iterate over each block and its global position, not the position within the segment

		@return: (x,y,z), block
		@rtype: tuple[int,int,int], SmdBlock
		"""
		for position_region, region in self.position_to_region.iteritems():
			assert isinstance(region, SmdRegion), type(region)
			for position_block, block in region.iteritems():
				assert isinstance(block, SmdBlock), type(block)
				yield position_block, block

	def get_min_max_vector(self):
		"""
		Get the minimum and maximum coordinates of the blueprint

		@return: Minimum(x,y,z), Maximum(x,y,z)
		@rtype: tuple[int,int,int], tuple[int,int,int]
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
		Change entity type of blueprint
		0: "Ship",
		2: "Station",

		@param entity_type:
		@type entity_type: int
		"""
		assert isinstance(entity_type, (int, long))
		assert 0 <= entity_type <= 4

		position_core = (16, 16, 16)
		if entity_type == 0:  # Ship
			core_block = SmdBlock()
			core_block.set_id(1)
			core_block.set_hit_points(250)
			self.add(position_core, core_block)
		else:  # not a ship
			try:
				self.remove_block(position_core)
			except AssertionError as exception_object:
				self._logger.debug("'set_type' exception: {}".format(exception_object.message))
		self.update(entity_type)  # remove blocks invalid for ships and other cleanup

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream smd values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("####\nSMD\n####\n\n")
		output_stream.write("Total blocks: {}\n\n".format(self.get_number_of_blocks()))
		for position in sorted(self.position_to_region.keys(), key=lambda tup: (tup[2], tup[1], tup[0])):
			output_stream.write("SmdRegion: {}\n".format(list(position)))
			self.position_to_region[position].to_stream(output_stream)
			output_stream.write("\n")

	# auto wedge

	def get_position_periphery_index_9x9(self, position):
		"""
		Every position in a 3x3x3 periphery is represented by a bit.

		@type position: tuple[int]
		@rtype: int
		"""
		periphery_index = long(0)
		power = long(1)
		for x in range(position[0]-1, position[0]+2):
			for y in range(position[1]-1, position[1]+2):
				for z in range(position[2]-1, position[2]+2):
					position_tmp = (x, y, z)
					if position_tmp == position:
						continue
					if self.has_block_at_position(position_tmp):
						periphery_index |= power
					power <<= 1
		# print power
		return periphery_index

	def get_position_periphery_index(self, position, periphery_range):
		"""
		Some positions in a 3x3x3 periphery, represented by a bit each.

		@type position: tuple[int]
		@rtype: int
		"""
		assert 1 <= periphery_range <= 3
		periphery_index = long(0)
		power = long(1)
		range_p = [-1, 0, 1]
		for x in range_p:
			for y in range_p:
				for z in range_p:
					if abs(x) + abs(y) + abs(z) > periphery_range:
						continue
					position_tmp = (position[0] + x, position[1] + y, position[2] + z)
					if position_tmp == position:
						continue
					if self.has_block_at_position(position_tmp):
						periphery_index |= power
					power <<= 1
		return periphery_index

	def get_position_shape_periphery(self, position, periphery_range):
		"""
		Return a 3x3x3 periphery description

		Shapes:
			"": 0,
			"1/4": 1,
			"1/2": 2,
			"3/4": 3,
			"Wedge": 4,
			"Corner": 5,
			"Tetra": 6,
			"Hepta": 7,

		@type position: tuple[int]
		@type periphery_range: int

		@rtype: tple[int]
		"""
		assert 1 <= periphery_range <= 3
		angle_shapes = {4, 6}  # 5, 7,
		shape_periphery = []
		range_p = [-1, 0, 1]
		for x in range_p:
			for y in range_p:
				for z in range_p:
					if abs(x) + abs(y) + abs(z) > periphery_range:
						continue
					position_tmp = (position[0] + x, position[1] + y, position[2] + z)
					if position_tmp == position:
						continue
					if self.has_block_at_position(position_tmp):
						block_tmp = self.get_block_at_position(position_tmp)
						block_id = block_tmp.get_id()
						is_angled_shape = False
						if BlueprintUtils.is_hull(block_id):
							block_hull_type, color, shape_id = self._get_hull_details(block_id)
							if shape_id in angle_shapes:
								is_angled_shape = True
						elif "wedge" in BlueprintUtils.get_block_name_by_id(block_id).lower():
							is_angled_shape = True
						shape_periphery.append(is_angled_shape)
		return tuple(shape_periphery)

	def auto_hull_shape_independent(self, auto_wedge, auto_tetra):
		"""
		Replace hull blocks with shaped hull blocks with shapes,
		that can be determined without knowing the shapes of blocks around it

		@type auto_wedge: bool
		@type auto_tetra: bool
		"""
		for position, block in self.iteritems():
			block_id = block.get_id()
			if not BlueprintUtils.is_hull(block_id):
				continue

			periphery_index = self.get_position_periphery_index(position, 1)
			if auto_wedge and periphery_index in BlueprintUtils.peripheries[4]:
				# "wedge"
				new_shape_id = 4
			elif auto_tetra and periphery_index in BlueprintUtils.peripheries[6]:
				# tetra
				new_shape_id = 6
			else:
				continue

			bit_19, bit_22, bit_23, rotations = BlueprintUtils.peripheries[new_shape_id][periphery_index]
			block_hull_type, color, shape_id = self._get_hull_details(block_id)
			new_block_id = self.get_hull_id_by_details(block_hull_type, color, new_shape_id)
			block.update(block_id=new_block_id, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)

	def auto_hull_shape_dependent(self, block_shape_id):
		"""
		Replace hull blocks with shaped hull blocks with shapes,
		that can only be determined by the shapes of blocks around it

		@type block_shape_id: int
		"""
		for position, block in self.iteritems():
			block_id = block.get_id()
			if not BlueprintUtils.is_hull(block_id):
				continue

			periphery_index = self.get_position_periphery_index(position, 1)
			if periphery_index not in BlueprintUtils.peripheries[block_shape_id]:
				continue
			periphery_shape = self.get_position_shape_periphery(position, 1)
			if periphery_shape not in BlueprintUtils.peripheries[block_shape_id][periphery_index]:
				continue
			bit_19, bit_22, bit_23, rotations = BlueprintUtils.peripheries[block_shape_id][periphery_index][periphery_shape]
			block_hull_type, color, shape_id = self._get_hull_details(block_id)
			new_block_id = self.get_hull_id_by_details(block_hull_type, color, block_shape_id)
			block.update(block_id=new_block_id, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)

	def auto_hull_shape(self, auto_wedge, auto_tetra, auto_corner, auto_hepta=None):
		"""
		Automatically set shapes to blocks on edges and corners.
		"": 0,
		"1/4": 1,
		"1/2": 2,
		"3/4": 3,
		"Wedge": 4,
		"Corner": 5,
		"Tetra": 6,
		"Hepta": 7,

		@type auto_wedge: bool
		@type auto_tetra: bool
		@type auto_corner: bool
		@type auto_hepta: bool
		"""
		self.auto_hull_shape_independent(auto_wedge, auto_tetra)
		if auto_corner:
			self.auto_hull_shape_dependent(5)
		if auto_hepta:
			self.auto_hull_shape_dependent(7)

	def auto_wedge_debug(self):
		"""
		Replace hull blocks on edges with wedges.
		"""
		peripheries = {}
		for position, block in self.iteritems():
			if not BlueprintUtils.is_hull(block.get_id()):
				continue
			# wedge 599
			# corner 600
			# hepta 601
			# tetra 602
			if block.get_id() != 602:
				continue
			periphery_index = self.get_position_periphery_index(position, 1)
			if periphery_index == 0:
				continue
			# hull_type, color, shape_id = BlueprintUtils._get_hull_details(block.get_id())
			bit_19 = block._get_bit_19()
			bit_22 = block._get_bit_22()
			bit_23 = block._get_bit_23()
			rotations = block._get_clockwise_rotations()
			if periphery_index in peripheries:
				tmp = (bit_19, bit_22, bit_23, rotations)
				if peripheries[periphery_index] != tmp:
					sys.stderr.write("{}: {}\n".format(
						periphery_index, tmp))
				continue
			sys.stdout.write("\t\t{}: [{}, {}, {}, {}],\n".format(
				periphery_index, bit_19, bit_22, bit_23, rotations))
			# sys.stdout.write("\t\t{}: [{}, {}],  # {}\n".format(periphery_index, shape_id, block.get_int_24bit(), position))

			# int_24 = block.get_int_24bit()
			# block.update(block_id=599, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)
			# assert int_24 == block.get_int_24bit()
			peripheries[periphery_index] = (bit_19, bit_22, bit_23, rotations)

	def auto_hepta_debug(self):
		"""
		Replace hull blocks on edges with wedges.
		"""
		peripheries = {}
		bad_orientations = 0
		for position, block in self.iteritems():
			if not BlueprintUtils.is_hull(block.get_id()):
				continue
			# wedge 599
			# corner 600
			# hepta 601
			# tetra 602
			if block.get_id() != 601:
				continue
			periphery_index = self.get_position_periphery_index(position, 1)
			periphery_shape = self.get_position_shape_periphery(position, 1)
			if periphery_index not in peripheries:
				peripheries[periphery_index] = {}

			bit_19 = block._get_bit_19()
			bit_22 = block._get_bit_22()
			bit_23 = block._get_bit_23()
			rotations = block._get_clockwise_rotations()
			orientation = (bit_19, bit_22, bit_23, rotations)

			if all(periphery_shape):
				continue
			if periphery_shape in peripheries[periphery_index] and peripheries[periphery_index][periphery_shape] != orientation:
				bad_orientations += 1
				continue
			peripheries[periphery_index][periphery_shape] = orientation

		print "bad_orientations", bad_orientations
		for periphery_index in peripheries.keys():
			print "\t\t{}:".format(periphery_index), '{'
			for periphery_shape in peripheries[periphery_index].keys():
				print "\t\t\t{}: {},".format(periphery_shape, peripheries[periphery_index][periphery_shape])
			print "\t\t},"
