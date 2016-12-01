__author__ = 'Peter Hofmann'

import os
import sys
from blueprintutils import BlueprintUtils
from bit_and_bytes import BitAndBytes


# #######################################
# ###  HEADER smbph
# #######################################

class Header(BlueprintUtils, BitAndBytes):

	_file_name = "header.smbph"

	def __init__(self):
		super(Header, self).__init__()
		self.version = ""
		self.type = -1
		self.box_min = [0., 0., 0.]
		self.box_max = [0., 0., 0.]
		self.block_id_to_quantity = {}
		# unknown = None
		self.tail_data = None
		return

	# #######################################
	# ###  Read
	# #######################################

	def read(self, directory_blueprint):
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'rb') as input_stream:
			self._read_file(input_stream)

	def _read_file(self, input_stream):
		assert isinstance(input_stream, file)
		self.version = self._read_int_unassigned(input_stream)
		self.type = self._read_int_unassigned(input_stream)
		self.box_min = self._read_vector_3f(input_stream)
		self.box_max = self._read_vector_3f(input_stream)
		num_of_block_types = self._read_int_unassigned(input_stream)
		assert 0 < num_of_block_types < 1000, num_of_block_types

		for index in range(0, num_of_block_types):
			identifier = self._read_short_int_unassigned(input_stream)
			quantity = self._read_int_unassigned(input_stream)
			self.block_id_to_quantity[identifier] = quantity
		self.tail_data = input_stream.read()

	# #######################################
	# ###  Write
	# #######################################

	def write(self, directory_blueprint):
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'wb') as output_stream:
			self._write_file(output_stream)

	def _write_file(self, output_stream):
		assert isinstance(output_stream, file)
		self._write_int_unassigned(self.version, output_stream)
		self._write_int_unassigned(self.type, output_stream)
		self._write_vector_3f(self.box_min, output_stream)
		self._write_vector_3f(self.box_max, output_stream)

		num_of_block_types = len(self.block_id_to_quantity)
		self._write_int_unassigned(num_of_block_types, output_stream)
		for identifier, quantity in self.block_id_to_quantity.iteritems():
			self._write_short_int_unassigned(identifier, output_stream)
			self._write_int_unassigned(quantity, output_stream)
		output_stream.write(self.tail_data)

	# #######################################
	# ###  Else
	# #######################################

	def _get_measure(self, index):
		return self.box_max[index] - self.box_min[index]

	def get_type_name(self):
		return self._entity_types[self.type]

	def get_width(self):
		return self._get_measure(0)

	def get_height(self):
		return self._get_measure(1)

	def get_length(self):
		return self._get_measure(2)

	def add(self, identifier, quantity):
		assert quantity > 0
		if identifier not in self.block_id_to_quantity:
			self.block_id_to_quantity[identifier] = 0
		self.block_id_to_quantity[identifier] += quantity

	def set_type(self, entity_type):
		"""
		0: "Ship",
		"""
		assert isinstance(entity_type, (int, long))
		assert 0 <= entity_type <= 4
		self.type = entity_type

		block_id_core = 1
		if entity_type > 0 and block_id_core in self.block_id_to_quantity:
			self.remove(block_id_core)
		elif block_id_core not in self.block_id_to_quantity:
			self.add(block_id_core, 1)
		self.update()

	def set_quantities(self, block_id_to_quantity):
		"""

		@param block_id_to_quantity:
		@type block_id_to_quantity: dict[int, in]
		"""
		self.block_id_to_quantity = block_id_to_quantity

	def update(self):
		block_id_list = self.block_id_to_quantity.keys()
		for block_id in block_id_list:
			if not self._is_valid_block_id(block_id, self.type):
				self.remove(block_id)
				continue
			if block_id not in self._docking_to_rails:
				continue
			updated_block_id = self._docking_to_rails[block_id]
			if updated_block_id is None:
				self.remove(block_id)
				continue
			quantity = self.block_id_to_quantity.pop(block_id)
			self.block_id_to_quantity[updated_block_id] = quantity

	def remove(self, block_id, quantity=None):
		assert quantity is None or quantity > 0, quantity
		assert block_id in self.block_id_to_quantity, block_id
		assert quantity is None or self.block_id_to_quantity[block_id] >= quantity, (self.block_id_to_quantity[block_id], quantity)
		if quantity is None:
			quantity = self.block_id_to_quantity[block_id]
		self.block_id_to_quantity[block_id] -= quantity
		if self.block_id_to_quantity[block_id] == 0:
			self.block_id_to_quantity.pop(block_id)

	def set_box(self, min_vector, max_vector):
		min_vector = self.vector_subtraction(min_vector, (1, 1, 1))
		max_vector = self.vector_addition(max_vector, (2, 2, 2))
		self.box_min = self.vector_subtraction(min_vector, (16, 16, 16))
		self.box_max = self.vector_subtraction(max_vector, (16, 16, 16))

	def to_stream(self, output_stream=sys.stdout, summary=True):
		output_stream.write("####\nHEADER ({})\n####\n\n".format(self.version))
		output_stream.write("{} (w:{} , h:{}, l:{})\t{}, {}\n\n".format(
			self.get_type_name(),
			self.get_width(),
			self.get_height(),
			self.get_length(),
			self.box_min,
			self.box_max,
			))
		output_stream.write("Blocks: {}\n".format(sum(self.block_id_to_quantity.values())))
		if summary:
			output_stream.flush()
			return
		for identifier, quantity in self.block_id_to_quantity.iteritems():
			output_stream.write("{}: {}\n".format(self.get_block_name_by_id(identifier), quantity))
		output_stream.write("\n")
		# stream.write("{}\n".format(self.unknown))
		output_stream.write("Tail: {} bytes\n".format(len(self.tail_data)))
		output_stream.write("\n")
		output_stream.flush()
