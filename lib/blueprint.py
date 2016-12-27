__author__ = 'Peter Hofmann'

import os
import sys
from lib.loggingwrapper import DefaultLogging
from lib.blueprintutils import BlueprintUtils
from lib.header import Header
from lib.logic import Logic
from lib.meta import Meta
from lib.smd3.smd import Smd


class Blueprint(DefaultLogging, BlueprintUtils):

	def __init__(self, logfile=None, verbose=False, debug=False):
		"""
		Constructor

		@param logfile: file handler or file path to a log file
		@type logfile: file | FileIO | StringIO | basestring
		@param verbose: Not verbose means that only warnings and errors will be past to stream
		@type verbose: bool
		@param debug: Display debug messages
		@type debug: bool

		@rtype: None
		"""
		self._label = "Blueprint"
		super(Blueprint, self).__init__(logfile=logfile, verbose=verbose, debug=debug)
		self.header = Header(logfile=logfile, verbose=verbose, debug=debug)
		self.logic = Logic(logfile=logfile, verbose=verbose, debug=debug)
		self.meta = Meta(logfile=logfile, verbose=verbose, debug=debug)
		self.smd3 = Smd(logfile=logfile, verbose=verbose, debug=debug)
		return

	# #######################################
	# ###  Read
	# #######################################

	def read(self, directory_blueprint):
		"""
		Read blueprint from a directory

		@param directory_blueprint: /../StarMade/blueprints/blueprint_name/
		@type directory_blueprint: str
		"""
		self.header = Header(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
		self.logic = Logic(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
		self.meta = Meta(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
		self.smd3 = Smd(logfile=self._logfile, verbose=self._verbose, debug=self._debug)

		self.header.read(directory_blueprint)
		self.logic.read(directory_blueprint)
		# self.meta.read(directory_blueprint)
		self.smd3.read(directory_blueprint)

	# #######################################
	# ###  Write
	# #######################################

	def write(self, directory_blueprint):
		"""
		Save blueprint to a directory

		@param directory_blueprint: /../StarMade/blueprints/blueprint_name/
		@type directory_blueprint: str
		"""
		if directory_blueprint.endswith('/') or directory_blueprint.endswith('\\'):
			directory_blueprint = directory_blueprint[:-1]

		blueprint_name = os.path.basename(directory_blueprint)
		directory_blueprint_unique = directory_blueprint
		assert not os.path.exists(directory_blueprint_unique), "Output directory exists, not writing blueprint to exiting folder to prevent overwriting."
		assert os.path.exists(os.path.dirname(directory_blueprint_unique)), "Parent folder of output dir does not exist, can not write blueprint."
		os.mkdir(directory_blueprint_unique)

		self.header.write(directory_blueprint_unique)
		self.logic.write(directory_blueprint_unique)
		self.meta.write(directory_blueprint_unique)
		self.smd3.write(directory_blueprint_unique, blueprint_name)

	# #######################################
	# ###  Else
	# #######################################

	def set_entity_type(self, entity_type):
		"""
		Change entity type
		0: "Ship",
		2: "Station",

		@param entity_type: ship=0/station=2/etc
		@type entity_type: int
		"""
		assert isinstance(entity_type, (int, long))
		self.smd3.set_type(entity_type)
		self.logic.set_type(entity_type)
		self.header.set_type(entity_type)
		self.update()

	def replace_blocks(self, block_id, replace_id, replace_hp):
		"""
		Replace all blocks of a specific id

		@type block_id: int
		@type replace_id: int
		@type replace_hp: int
		"""
		compatible = self.are_compatible_blocks(block_id, replace_id)
		self.smd3.replace_blocks(block_id, replace_id, replace_hp, compatible)
		self.header.update(self.smd3)

	def update(self):
		"""
		Remove invalid/outdated blocks and exchange docking modules with rails
		"""
		entity_type = self.header.type
		self.smd3.update(entity_type)
		self.logic.update(self.smd3)
		self.header.update(self.smd3)

	def move_center_by_block_id(self, block_id):
		"""
		Relocate center/core to the position of a hopefully unique block

		@param block_id: block id
		@type block_id: int
		"""
		assert isinstance(block_id, (int, long))
		position = self.smd3.search(block_id)
		assert position is not None, "Block id not found: {}".format(block_id)
		distance = self.vector_distance(position, (16, 16, 16))
		if distance == 0:
			return
		direction_vector = self._get_direction_vector_to_center(position)
		self.move_center_by_vector(direction_vector)

	def move_center_by_vector(self, direction_vector):
		"""
		Relocate center/core in a direction

		@param direction_vector: vector
		@type direction_vector: int, int, int
		"""
		assert isinstance(direction_vector, tuple)
		min_vector, max_vector = self.smd3.move_center(direction_vector, self.header.type)
		self.logic.move_center(direction_vector, self.header.type)
		self.header.set_box(min_vector, max_vector)
		self.header.update(self.smd3)

	def turn_tilt(self, index_turn_tilt):
		"""

		@param index_turn_tilt:
		@type index_turn_tilt: int
		"""
		assert 0 <= index_turn_tilt <= 5
		self.logic.tilt_turn(index_turn_tilt)
		min_vector, max_vector = self.smd3.tilt_turn(index_turn_tilt)
		self.header.set_box(min_vector, max_vector)

	def link_salvage_modules(self):
		"""
		Automatically link salvage computers to salvage modules
		"""
		position_salvage_computers = self.smd3.search_all(4)
		assert len(position_salvage_computers) > 0, "No salvage computer found"
		position_salvage_modules = self.smd3.search_all(24)
		assert len(position_salvage_modules) > 0, "No salvage modules found"
		groups = {}
		salvage_computer_count = len(position_salvage_computers)

		if salvage_computer_count == 1:
			self.logic.set_link(position_salvage_computers.pop(), 24, position_salvage_modules)
			return

		for index in range(salvage_computer_count):
			groups[index] = set()
		for position in position_salvage_modules:
			group_index = (position[0] + position[1]) % salvage_computer_count
			groups[group_index].add(position)
		position_salvage_computers = list(position_salvage_computers)
		for group_index in groups.keys():
			self.logic.set_link(position_salvage_computers[group_index], 24, groups[group_index])

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream blueprint values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		self.header.to_stream(output_stream)
		self.logic.to_stream(output_stream)
		self.meta.to_stream(output_stream)
		self.smd3.to_stream(output_stream)
