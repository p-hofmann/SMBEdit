__author__ = 'Peter Hofmann'

import os
from scripts.loggingwrapper import DefaultLogging
from scripts.blueprintutils import BlueprintUtils
from scripts.header import Header
from scripts.logic import Logic
from scripts.meta import Meta
from scripts.smd import Smd


class Blueprint(DefaultLogging, BlueprintUtils):

	_label = "Blueprint"

	def __init__(self, logfile=None, verbose=False, debug=False):
		super(Blueprint, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		self.header = Header()
		self.logic = Logic()
		self.meta = Meta()
		self.smd3 = Smd()
		return

	# #######################################
	# ###  Read
	# #######################################

	def read(self, directory_blueprint):
		self.header = Header()
		self.header.read(directory_blueprint)
		self.logic = Logic()
		self.logic.read(directory_blueprint)
		self.meta = Meta()
		# self.meta.read(directory_blueprint)
		self.smd3 = Smd(
			logfile=self._logfile,
			verbose=self._verbose,
			debug=self._debug)
		self.smd3.read(directory_blueprint)

	# #######################################
	# ###  Write
	# #######################################

	def write(self, directory_blueprint):
		if directory_blueprint.endswith('/') or directory_blueprint.endswith('\\'):
			directory_blueprint = directory_blueprint[:-1]
		# root_dir = os.path.dirname(directory_blueprint)
		blueprint_name = os.path.basename(directory_blueprint)
		directory_blueprint_unique = directory_blueprint
		assert not os.path.exists(directory_blueprint_unique), "Output folder exists, aborting."
		os.mkdir(directory_blueprint_unique)
		# directory_blueprint_unique = tempfile.mkdtemp(prefix=blueprint_name+"_", dir=root_dir)
		# print "Output:", directory_blueprint_unique
		self.header.write(directory_blueprint_unique)
		self.logic.write(directory_blueprint_unique)
		self.meta.write(directory_blueprint_unique)
		self.smd3.write(directory_blueprint_unique, blueprint_name)

	# #######################################
	# ###  Else
	# #######################################

	def _get_direction_vector_to_center(self, position):
		return self.vector_subtraction(position, (16, 16, 16))

	def move_center_by_block_id(self, block_id):
		assert isinstance(block_id, (int, long))
		position = self.smd3.search(block_id)
		assert position is not None, "Block id not found: {}".format(block_id)
		distance = self.vector_distance(position, (16, 16, 16))
		if distance == 0:
			return
		direction_vector = self._get_direction_vector_to_center(position)
		self.move_center_by_vector(direction_vector)

	def set_entity_type(self, entity_type):
		assert isinstance(entity_type, (int, long))
		self.header.set_type(entity_type)
		self.logic.set_type(entity_type)
		self.smd3.set_type(entity_type)

	def update(self):
		entity_type = self.header.type
		# self.header.update()
		self.logic.update()
		self.smd3.update(entity_type)
		self.header.set_quantities(self.smd3.get_block_id_to_quantity())

	def move_center_by_vector(self, direction_vector):
		assert isinstance(direction_vector, tuple)
		min_vector, max_vector = self.smd3.move_center(direction_vector)
		self.logic.move_center(direction_vector, self.header.type)
		self.header.set_box(min_vector, max_vector)

	def to_string(self, summary=True):
		self.header.to_stream(summary=summary)
		self.logic.to_stream(summary=summary)
		# self.meta.to_stream()
		self.smd3.to_stream(summary=summary)
