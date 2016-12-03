__author__ = 'Peter Hofmann'

import os
import sys
from bit_and_bytes import ByteStream
from blueprintutils import BlueprintUtils


# #######################################
# ###  LOGIC
# #######################################

class Logic(BlueprintUtils):

	_file_name = "logic.smbpl"

	def __init__(self):
		super(Logic, self).__init__()
		self.version = ""
		self.unknown_int = None
		self.controller_position_to_block_id_to_block_positions = {}
		# tail_data = None
		return

	# #######################################
	# ###  Read
	# #######################################

	@staticmethod
	def _read_set_of_positions(input_stream):
		"""
		Read position data from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream

		@return: set of positions
		@rtype: set[int, int, int]
		"""
		data = set()
		number_of_positions = input_stream.read_int32_unassigned()
		for _ in range(0, number_of_positions):
			data.add(input_stream.read_vector_3_int16())
		return data

	def _read_dict_of_groups(self, input_stream):
		"""
		Read controller group data from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream

		@return: dict of block id to set of positions
		@rtype: dict[int, set[int, int, int]]
		"""
		block_id_to_positions = {}
		number_of_groups = input_stream.read_int32_unassigned()
		for entry_index in range(0, number_of_groups):
			block_id = input_stream.read_int16_unassigned()
			block_id_to_positions[block_id] = self._read_set_of_positions(input_stream)
		return block_id_to_positions

	def _read_list_of_controllers(self, input_stream):
		"""
		Read controller data from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream

		@return: set of positions
		@rtype: dict[tuple, dict[int, set[int, int, int]]]
		"""
		controller_position_to_groups = {}
		number_of_controllers = input_stream.read_int32_unassigned()
		for entry_index in range(0, number_of_controllers):
			position = input_stream.read_vector_3_int16()
			controller_position_to_groups[position] = self._read_dict_of_groups(input_stream)
		return controller_position_to_groups

	def _read_file(self, input_stream):
		"""
		Read data from byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		self.version = input_stream.read_int32_unassigned()
		self.unknown_int = input_stream.read_int32_unassigned()
		self.controller_position_to_block_id_to_block_positions = self._read_list_of_controllers(input_stream)

	def read(self, directory_blueprint):
		"""
		Read data from logic file in blueprint directory

		@param directory_blueprint: input directory
		@type directory_blueprint: str
		"""
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'rb') as input_stream:
			self._read_file(ByteStream(input_stream))

	# #######################################
	# ###  Write
	# #######################################

	@staticmethod
	def _write_list_of_positions(positions, output_stream):
		"""
		Write position data to a byte stream

		@param positions: dict of block id to list of positions
		@type positions: set[int,int,int]
		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		output_stream.write_int32_unassigned(len(positions))
		for position in positions:
			output_stream.write_vector_3_int16(position)

	def _write_list_of_groups(self, groups, output_stream):
		"""
		Write data to a byte stream

		@param groups: dict of block id to list of positions
		@type groups: dict[int, set[int,int,int]]
		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		output_stream.write_int32_unassigned(len(groups))
		for block_id, positions in groups.iteritems():
			output_stream.write_int16_unassigned(block_id)
			self._write_list_of_positions(positions, output_stream)

	def _write_list_of_controllers(self, output_stream):
		"""
		Write controller data to a byte stream

		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		num_controllers = len(self.controller_position_to_block_id_to_block_positions)
		output_stream.write_int32_unassigned(num_controllers)
		for controller_position, groups in self.controller_position_to_block_id_to_block_positions.iteritems():
			output_stream.write_vector_3_int16(controller_position)
			self._write_list_of_groups(groups, output_stream)

	def _write_file(self, output_stream):
		"""
		Write data to a byte stream

		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		output_stream.write_int32_unassigned(self.version)
		output_stream.write_int32_unassigned(self.unknown_int)
		self._write_list_of_controllers(output_stream)

	def write(self, directory_blueprint):
		"""
		Write data to the logic file of a blueprint

		@param directory_blueprint: output directory
		@type directory_blueprint: str
		"""
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'wb') as output_stream:
			self._write_file(ByteStream(output_stream))

	# #######################################
	# ###  Else
	# #######################################

	def update(self):
		"""
		Delete links with invalid controller
		"""
		# todo: check if linked positions are valid, like storage to factory after changing to ship
		for controller_position in self.controller_position_to_block_id_to_block_positions.keys():
			groups = self.controller_position_to_block_id_to_block_positions[controller_position]
			for block_id in groups.keys():
				if self._is_valid_block_id(block_id):
					continue
				self.controller_position_to_block_id_to_block_positions[controller_position].pop(block_id)
			if len(self.controller_position_to_block_id_to_block_positions[controller_position]) == 0:
				self.controller_position_to_block_id_to_block_positions.pop(controller_position)

	def move_center(self, direction_vector, entity_type=0):
		"""
		Move center (core) in a specific direction and correct all links

		@param direction_vector: (x,y,z)
		@type direction_vector: int,int,int
		"""
		new_dict = {}
		for controller_position, groups in self.controller_position_to_block_id_to_block_positions.iteritems():
			new_controller_position = self.vector_subtraction(controller_position, direction_vector)
			if entity_type == 0 and new_controller_position == (16, 16, 16):  # replaced block
				continue
			if entity_type == 0 and controller_position == (16, 16, 16):  # core
				new_controller_position = controller_position
			if new_controller_position not in new_dict:
				new_dict[new_controller_position] = {}
			for block_id, positions in groups.iteritems():
				if block_id not in new_dict[new_controller_position]:
					new_dict[new_controller_position][block_id] = set()
				for block_position in positions:
					new_block_position = self.vector_subtraction(block_position, direction_vector)
					if entity_type == 0 and new_block_position == (16, 16, 16):  # replaced block
						continue
					new_dict[new_controller_position][block_id].add(new_block_position)
				if len(new_dict[new_controller_position][block_id]) == 0:
					new_dict[new_controller_position].pop(block_id)
			if len(new_dict[new_controller_position]) == 0:
				new_dict.pop(new_controller_position)
		del self.controller_position_to_block_id_to_block_positions
		self.controller_position_to_block_id_to_block_positions = new_dict

	def set_type(self, entity_type):
		"""
		Change entity type
		0: "Ship",
		2: "Station",

		@param entity_type:
		@type entity_type: int
		"""
		assert isinstance(entity_type, (int, long))
		assert 0 <= entity_type <= 4

		position_core = (16, 16, 16)
		if entity_type == 0:
			return
		if position_core in self.controller_position_to_block_id_to_block_positions:
			self.controller_position_to_block_id_to_block_positions.pop(position_core)

	def to_stream(self, output_stream=sys.stdout, summary=True):
		"""
		Stream logic values

		@param output_stream: Output stream
		@type output_stream: fileIO
		@param summary: If true the output is reduced
		@type summary: bool
		"""
		output_stream.write("####\nLOGIC ({})\n####\n\n".format(self.version))
		# stream.write("UNKNOWN: {}\n\n".format(self.unknown_int))
		output_stream.write("Controllers: {}\n".format(len(self.controller_position_to_block_id_to_block_positions)))
		output_stream.write("\n")
		if summary:
			output_stream.flush()
			return
		for controller_position, groups in self.controller_position_to_block_id_to_block_positions.iteritems():
			output_stream.write("{}: #{}\n".format(controller_position, len(groups.keys())))
			for block_id, positions in groups.iteritems():
				if len(positions) < 5:
					output_stream.write("\t{}: {}\n".format(block_id, positions))
				else:
					output_stream.write("\t{}: #{}\n".format(block_id, len(positions)))
			output_stream.write("\n")
		output_stream.write("\n")
		output_stream.flush()
