__author__ = 'Peter Hofmann'

import os
import sys
from lib.loggingwrapper import DefaultLogging
from lib.blueprintutils import BlueprintUtils
from lib.bits_and_bytes import ByteStream
from lib.smd3.smd import Smd


# #######################################
# ###  HEADER smbph
# #######################################


class Statistics(object):

	_valid_versions = {0, 1}

	def __init__(self):
		super(Statistics, self).__init__()
		self.has_statistics = False
		self.version = 1
		self.offensive0 = 0.
		self.defensive = 0.
		self.power = 0.
		self.mobility = 0.
		self.danger = 0.
		self.survivability = 0.
		self.offensive1 = 0.
		self.support = 0
		self.mining = 0

	def read_statistics(self, input_stream):
		"""
		Read statistic data from a byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		self.has_statistics = input_stream.read_bool()
		if not self.has_statistics:
			return
		self.version = input_stream.read_int16_unassigned()
		assert self.version in self._valid_versions, "Unsupported Statistic v{}".format(self.version)
		self.offensive0 = input_stream.read_double()
		self.defensive = input_stream.read_double()
		self.power = input_stream.read_double()
		self.mobility = input_stream.read_double()
		self.danger = input_stream.read_double()
		self.survivability = input_stream.read_double()
		self.offensive1 = input_stream.read_double()
		self.support = input_stream.read_double()
		if self.version > 0:
			self.mining = input_stream.read_double()

	def write_statistics(self, output_stream):
		"""
		Write statistic data to a byte stream

		@param output_stream: input stream
		@type output_stream: ByteStream
		"""
		output_stream.write_bool(self.has_statistics)
		if not self.has_statistics:
			return
		output_stream.write_int16_unassigned(self.version)
		output_stream.write_double(self.offensive0)
		output_stream.write_double(self.defensive)
		output_stream.write_double(self.power)
		output_stream.write_double(self.mobility)
		output_stream.write_double(self.danger)
		output_stream.write_double(self.survivability)
		output_stream.write_double(self.offensive1)
		output_stream.write_double(self.support)
		if self.version > 0:
			output_stream.write_double(self.mining)

	def to_stream(self, output_stream=sys.stdout):
		"""
		Write statistic values to a stream

		@param output_stream: input stream
		@type output_stream: fileIO
		"""
		if not self.has_statistics:
			return
		output_stream.write("Statistics:\nVersion: {}\n".format(self.version))
		output_stream.write("Offensive0: {}\n".format(self.offensive0))
		output_stream.write("Offensive1: {}\n".format(self.offensive1))
		output_stream.write("Defensive: {}\n".format(self.defensive))
		output_stream.write("Power: {}\n".format(self.power))
		output_stream.write("Mobility: {}\n".format(self.mobility))
		output_stream.write("Danger: {}\n".format(self.danger))
		output_stream.write("Survivability: {}\n".format(self.survivability))
		output_stream.write("Support: {}\n".format(self.support))
		if self.version > 0:
			output_stream.write("Mining: {}\n".format(self.mining))
		output_stream.write("\n")


class Header(DefaultLogging, BlueprintUtils):

	_file_name = "header.smbph"

	_valid_versions = {2, 3}

	def __init__(self, logfile=None, verbose=False, debug=False):
		super(Header, self).__init__(logfile, verbose, debug)
		self.version = 2
		self.type = 2
		self.box_min = [0., 0., 0.]
		self.box_max = [0., 0., 0.]
		self.block_id_to_quantity = {}
		self.statistics = Statistics()
		return

	# #######################################
	# ###  Read
	# #######################################

	def _read_block_quantities(self, input_stream):
		"""
		Read block quantities from a byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		assert isinstance(input_stream, ByteStream)
		num_of_block_types = input_stream.read_int32_unassigned()
		for index in range(0, num_of_block_types):
			block_identifier = input_stream.read_int16_unassigned()
			quantity = input_stream.read_int32_unassigned()
			self.block_id_to_quantity[block_identifier] = quantity

	def _read_header(self, input_stream):
		"""
		Read header data from a byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		assert isinstance(input_stream, ByteStream)
		self.version = input_stream.read_int32_unassigned()
		assert self.version in self._valid_versions, "Unsupported HEADER v{}".format(self.version)
		self.type = input_stream.read_int32_unassigned()
		if self.version > 2:
			self.classification = input_stream.read_int32_unassigned()
		self.box_min = input_stream.read_vector_3_float()
		self.box_max = input_stream.read_vector_3_float()

	def _read_file(self, input_stream):
		"""
		Read blueprint header data from a byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		assert isinstance(input_stream, ByteStream)
		self._read_header(input_stream)
		self._read_block_quantities(input_stream)
		self.statistics.read_statistics(input_stream)

	def read(self, directory_blueprint):
		"""
		Read header data from the header file of a blueprint

		@param directory_blueprint: input directory
		@type directory_blueprint: str
		"""
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'rb') as input_stream:
			self._read_file(ByteStream(input_stream))

	# #######################################
	# ###  Write
	# #######################################

	def _write_block_quantities(self, output_stream):
		"""
		Write block quantities to a byte stream

		@param output_stream: input stream
		@type output_stream: ByteStream
		"""
		assert isinstance(output_stream, ByteStream)
		num_of_block_types = len(self.block_id_to_quantity)
		output_stream.write_int32_unassigned(num_of_block_types)
		for identifier, quantity in self.block_id_to_quantity.iteritems():
			output_stream.write_int16_unassigned(identifier)
			output_stream.write_int32_unassigned(quantity)

	def _write_header(self, output_stream):
		"""
		Write header data to a byte stream

		@param output_stream: input stream
		@type output_stream: ByteStream
		"""
		assert isinstance(output_stream, ByteStream)
		output_stream.write_int32_unassigned(self.version)
		output_stream.write_int32_unassigned(self.type)
		if self.version > 2:
			output_stream.write_int32_unassigned(self.classification)
		output_stream.write_vector_3_float(self.box_min)
		output_stream.write_vector_3_float(self.box_max)

	def _write_file(self, output_stream):
		"""
		Write header data to a byte stream

		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		assert isinstance(output_stream, ByteStream)
		self._write_header(output_stream)
		self._write_block_quantities(output_stream)
		self.statistics.write_statistics(output_stream)

	def write(self, directory_blueprint):
		"""
		Write header data to the header file of a blueprint

		@param directory_blueprint: output directory
		@type directory_blueprint: str
		"""
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'wb') as output_stream:
			self._write_file(ByteStream(output_stream))

	# #######################################
	# ###  Else
	# #######################################

	def iteritems(self):
		for block_id in self.block_id_to_quantity.keys():
			yield block_id, self.block_id_to_quantity[block_id]

	def _get_measure(self, index):
		"""
		@param index:
		@type index: int

		@rtype: int
		"""
		return self.box_max[index] - self.box_min[index]

	def get_type_name(self):
		"""
		@return: Type of blueprint
		@rtype: str
		"""
		return self._entity_types[self.type]

	def get_classification_name(self):
		"""
		@return: classification of blueprint
		@rtype: str
		"""
		return self._entity_classification[self.classification]

	def get_width(self):
		"""
		@return: Width of bluprint
		@rtype: int
		"""
		return self._get_measure(0)

	def get_height(self):
		"""
		@return: Height of bluprint
		@rtype: int
		"""
		return self._get_measure(1)

	def get_length(self):
		"""
		@return: Length of bluprint
		@rtype: int
		"""
		return self._get_measure(2)

	def add(self, block_id, quantity):
		"""
		Add some blocks of a specific id

		@param block_id: block id
		@type block_id: int
		@param quantity: quantity
		@type quantity: int
		"""
		assert quantity > 0
		if block_id not in self.block_id_to_quantity:
			self.block_id_to_quantity[block_id] = 0
		self.block_id_to_quantity[block_id] += quantity

	def set_type(self, entity_type):
		"""
		Change entity type of header
		0: "Ship",
		2: "Station",

		@param entity_type:
		@type entity_type: int
		"""
		assert isinstance(entity_type, (int, long))
		assert 0 <= entity_type <= 4
		self.type = entity_type

		block_id_core = 1
		if entity_type > 0:
			if block_id_core in self.block_id_to_quantity:
				self.remove(block_id_core)
			self.statistics.has_statistics = False  # statistics only for ships
		elif block_id_core not in self.block_id_to_quantity:
			self.add(block_id_core, 1)

	def set_quantities(self, block_id_to_quantity):
		"""

		@param block_id_to_quantity:
		@type block_id_to_quantity: dict[int, in]
		"""
		self.block_id_to_quantity = block_id_to_quantity

	def update(self, smd=None):
		"""
		Remove invalid/outdated blocks and exchange docking modules with rails

		@param smd: Smd values
		@type smd: Smd
		"""
		if smd is not None:
			# update directly from smd data
			assert isinstance(smd, Smd)
			self.set_quantities(smd.get_block_id_to_quantity())
			min_vector, max_vector = smd.get_min_max_vector()
			self.set_box(min_vector=min_vector, max_vector=max_vector)
		else:
			# update manually and hope it reflects the smd data
			block_id_list = self.block_id_to_quantity.keys()
			for block_id in block_id_list:
				if not self.is_valid_block_id(block_id, self.type):
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
		"""
		remove blocks of a specific quantity

		@param block_id: block id
		@type block_id: int
		@param quantity: quantity of blocks
		@type quantity: int
		@return:
		"""
		assert quantity is None or quantity > 0, quantity
		assert block_id in self.block_id_to_quantity, block_id
		assert quantity is None or self.block_id_to_quantity[block_id] >= quantity, (self.block_id_to_quantity[block_id], quantity)
		if quantity is None:
			quantity = self.block_id_to_quantity[block_id]
		self.block_id_to_quantity[block_id] -= quantity
		if self.block_id_to_quantity[block_id] == 0:
			self.block_id_to_quantity.pop(block_id)

	def set_box(self, min_vector, max_vector):
		"""
		Set render box around blueprint

		@param min_vector: (x,y,z)
		@type min_vector: int, int, int
		@param max_vector:  (x,y,z)
		@type max_vector:  int, int, int
		"""
		min_vector = self.vector_subtraction(min_vector, (1, 1, 1))
		max_vector = self.vector_addition(max_vector, (2, 2, 2))
		self.box_min = self.vector_subtraction(min_vector, (16, 16, 16))
		self.box_max = self.vector_subtraction(max_vector, (16, 16, 16))

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream header values

		@param output_stream: Output stream
		@type output_stream: fileIO
		"""
		output_stream.write("####\nHEADER v{}\n####\n\n".format(self.version))
		output_stream.write("Type: {} (w:{} , h:{}, l:{})\n".format(
			self.get_type_name(),
			self.get_width(),
			self.get_height(),
			self.get_length()
			))
		if self.version > 2:
			output_stream.write("Classification: {}\n".format(self.get_classification_name()))

		if self._verbose or self._debug:
			output_stream.write("Box min: {}, Box max: {}\n".format(
				self.box_min,
				self.box_max,
				))
		output_stream.write("Blocks: {}\n".format(sum(self.block_id_to_quantity.values())))
		output_stream.write("\n")

		if self._verbose or self._debug:
			for identifier, quantity in self.block_id_to_quantity.iteritems():
				output_stream.write("{}: {}\n".format(self.get_block_name_by_id(identifier), quantity))
			output_stream.write("\n")
			self.statistics.to_stream(output_stream)
		output_stream.flush()
