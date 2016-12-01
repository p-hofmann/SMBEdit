__author__ = 'Peter Hofmann'

import os
import sys
from bit_and_bytes import BitAndBytes
from blueprintutils import BlueprintUtils


# #######################################
# ###  LOGIC
# #######################################

class Logic(BitAndBytes, BlueprintUtils):

	_file_name = "logic.smbpl"

	def __init__(self):
		super(Logic, self).__init__()
		self.version = ""
		self.unknown_int = None
		self.controller_position_to_groups_to_positions = {}
		# tail_data = None
		return

	# #######################################
	# ###  Read
	# #######################################

	def _read_list_of_positions(self, input_stream, amount):
		assert 0 < amount < 500000, amount
		data = {}
		for entry_index in range(0, amount):
			data[entry_index] = self._read_vector_3si(input_stream)
		return data

	def _read_list_of_groups(self, input_stream, amount):
		assert 0 < amount < 500000, amount
		block_id_to_positions = {}
		for entry_index in range(0, amount):
			block_id = self._read_short_int_unassigned(input_stream)
			number_of_positions = self._read_int_unassigned(input_stream)
			block_id_to_positions[block_id] = self._read_list_of_positions(input_stream, number_of_positions)
		return block_id_to_positions

	def _read_list_of_controllers(self, input_stream, amount):
		assert 0 <= amount < 1000, amount
		data = {}
		for entry_index in range(0, amount):
			position = self._read_vector_3si(input_stream)
			num_group = self._read_int_unassigned(input_stream)
			# print num_group
			data[tuple(position)] = self._read_list_of_groups(input_stream, num_group)
		return data

	def _read_file(self, input_stream):
		self.version = self._read_int_unassigned(input_stream)
		self.unknown_int = self._read_int_unassigned(input_stream)
		num_controllers = self._read_int_unassigned(input_stream)
		# print num_controllers
		# num_controllers = 10
		self.controller_position_to_groups_to_positions = self._read_list_of_controllers(input_stream, num_controllers)
		# self.tail_data = input_stream.read()

	def read(self, directory_blueprint):
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'rb') as input_stream:
			self._read_file(input_stream)

	# #######################################
	# ###  Write
	# #######################################

	def write(self, directory_blueprint):
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'wb') as output_stream:
			self._write_file(output_stream)

	def _write_file(self, output_stream):
		self._write_int_unassigned(self.version, output_stream)
		self._write_int_unassigned(self.unknown_int, output_stream)

		num_controllers = len(self.controller_position_to_groups_to_positions)
		self._write_int_unassigned(num_controllers, output_stream)
		self._write_list_of_controllers(output_stream)
		# output_stream.write(self.tail_data)

	def _write_list_of_controllers(self, output_stream):
		for controller_position, groups in self.controller_position_to_groups_to_positions.iteritems():
			self._write_vector_3si(controller_position, output_stream)
			self._write_int_unassigned(len(groups), output_stream)
			# print num_group
			self._write_list_of_groups(groups, output_stream)

	def _write_list_of_groups(self, groups, output_stream):
		for block_id, positions in groups.iteritems():
			self._write_short_int_unassigned(block_id, output_stream)
			self._write_int_unassigned(len(positions), output_stream)
			self._write_list_of_positions(positions, output_stream)

	def _write_list_of_positions(self, positions, output_stream):
		for _, position in positions.iteritems():
			self._write_vector_3si(position, output_stream)

	# #######################################
	# ###  Else
	# #######################################

	def update(self):
		for controller_position in self.controller_position_to_groups_to_positions.keys():
			groups = self.controller_position_to_groups_to_positions[controller_position]
			for block_id in groups.keys():
				if self._is_valid_block_id(block_id):
					continue
				self.controller_position_to_groups_to_positions[controller_position].pop(block_id)
			if len(self.controller_position_to_groups_to_positions[controller_position]) == 0:
				self.controller_position_to_groups_to_positions.pop(controller_position)

	def move_center(self, position_direction, entity_type=0):
		new_dict = {}
		for controller_position, groups in self.controller_position_to_groups_to_positions.iteritems():
			new_controller_position = self.vector_subtraction(controller_position, position_direction)
			if entity_type == 0 and new_controller_position == (16, 16, 16):  # replaced block
				continue
			if entity_type == 0 and controller_position == (16, 16, 16):  # core
				new_controller_position = controller_position
			if new_controller_position not in new_dict:
				new_dict[new_controller_position] = {}
			for block_id, positions in groups.iteritems():
				if block_id not in new_dict[new_controller_position]:
					new_dict[new_controller_position][block_id] = {}
				for block_index, block_position in positions.iteritems():
					new_block_position = self.vector_subtraction(block_position, position_direction)
					if entity_type == 0 and new_block_position == (16, 16, 16):  # replaced block
						continue
					new_dict[new_controller_position][block_id][block_index] = new_block_position
				if len(new_dict[new_controller_position][block_id]) == 0:
					new_dict[new_controller_position].pop(block_id)
			if len(new_dict[new_controller_position]) == 0:
				new_dict.pop(new_controller_position)
		del self.controller_position_to_groups_to_positions
		self.controller_position_to_groups_to_positions = new_dict

	def to_stream(self, output_stream=sys.stdout, summary=True):
		output_stream.write("####\nLOGIC ({})\n####\n\n".format(self.version))
		# stream.write("UNKNOWN: {}\n\n".format(self.unknown_int))
		output_stream.write("Controllers: {}\n\n".format(len(self.controller_position_to_groups_to_positions)))
		if summary:
			output_stream.flush()
			return
		for controller_position, groups in self.controller_position_to_groups_to_positions.iteritems():
			output_stream.write("{}: #{}\n".format(controller_position, len(groups.keys())))
			for block_id, positions in groups.iteritems():
				if len(positions) < 5:
					output_stream.write("\t{}: {}\n".format(block_id, positions.values()))
				else:
					output_stream.write("\t{}: #{}\n".format(block_id, len(positions)))
			output_stream.write("\n")
		# stream.write("Tail: {} bytes\n".format(len(self.tail_data)))
		output_stream.write("\n")
		output_stream.flush()

	def set_type(self, entity_type):
		"""
		0: "Ship",
		"""
		assert isinstance(entity_type, (int, long))
		assert 0 <= entity_type <= 4

		position_core = (16, 16, 16)
		if entity_type == 0:
			return
		if position_core in self.controller_position_to_groups_to_positions:
			self.controller_position_to_groups_to_positions.pop(position_core)
