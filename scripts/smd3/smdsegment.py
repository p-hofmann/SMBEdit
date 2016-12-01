__author__ = 'Peter Hofmann'

import sys
import zlib
import datetime
from scripts.loggingwrapper import DefaultLogging
from scripts.bit_and_bytes import BitAndBytes
from scripts.blueprintutils import BlueprintUtils
from smdblock import SmdBlock


class SmdSegment(DefaultLogging, BlueprintUtils, BitAndBytes):

	def __init__(self, segment_size, logfile=None, verbose=False, debug=False):
		self._label = "SmdSegment"
		super(SmdSegment, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		self._segment_size = segment_size
		self._blocksize_y = self._segment_size
		self._blocksize_z = self._segment_size * self._segment_size
		self._max_blocks = self._segment_size * self._segment_size * self._segment_size
		self.version = 2
		self.timestamp = 0
		self.position = None
		self.has_valid_data = 0
		self.compressed_size = 0
		self.block_index_to_block = {}

	def read(self, input_stream):
		return

	def to_stream(self, output_stream=sys.stdout, summary=False):
		return


class Smd3Segment(SmdSegment):

	def __init__(self, logfile=None, verbose=False, debug=False):
		self._label = "Smd3Segment {}".format(datetime.time)
		super(Smd3Segment, self).__init__(
			32,
			logfile=logfile,
			verbose=verbose,
			debug=debug)

	# #######################################
	# ###  Read
	# #######################################

	def read(self, input_stream):
		"""

		@param input_stream:
		@type input_stream: fileIO
		"""
		# always total size 49152 byte
		self.version = self._read_char(input_stream)  # 1 byte
		self.timestamp = self._read_double(input_stream)  # 8 byte
		# data["timestamp"] = self._read_long_long_unassigned(input_stream)
		self.position = self._read_vector_3i(input_stream)  # 12 byte
		self.has_valid_data = self._read_char(input_stream)  # 1 byte
		self.compressed_size = self._read_int_unassigned(input_stream)  # 4 byte
		if self.has_valid_data != 1:
			# print "invalid data", self.has_valid_data
			self.to_stream()
			assert isinstance(input_stream, file)
			input_stream.seek(49126, 1)
			# input_stream.read(49126)
		else:
			decompressed_data = zlib.decompress(input_stream.read(self.compressed_size))
			self.block_index_to_block = {}
			for block_index in range(0, len(decompressed_data)/3):
				position = block_index * 3
				block = SmdBlock()
				block.set_data_byte_string(decompressed_data[position:position+3])
				if block.get_id() > 0:
					self.block_index_to_block[block_index] = block
			input_stream.seek(49126-self.compressed_size, 1)
			# input_stream.read(49126-compressed_size)
		if self.has_valid_data == 1 and len(self.block_index_to_block) == 0:
			# print "No blocks read"
			self.has_valid_data = 0

	# #######################################
	# ###  Write
	# #######################################

	def write(self, output_stream):
		"""

		@param output_stream:
		@type output_stream: fileIO
		"""
		# always total size 49152 byte
		assert isinstance(output_stream, file)
		self._write_char(self.version, output_stream)  # 1 byte
		self._write_double(self.timestamp, output_stream)  # 8 byte
		# self._write_long_long_unassigned(self.timestamp, output_stream)  # 8 byte
		self._write_vector_3i(self.position, output_stream)  # 12 byte
		self._write_char(self.has_valid_data, output_stream)  # 1 byte

		if self.has_valid_data != 1:
			self.compressed_size = 0
			self._write_int_unassigned(self.compressed_size, output_stream)   # 4 byte
		else:
			byte_string = ""
			set_of_valid_block_index = set(self.block_index_to_block.keys())
			for block_index in range(0, self._blocksize_y * self._blocksize_y * self._blocksize_y):
				if block_index in set_of_valid_block_index:
					byte_string += self.block_index_to_block[block_index].get_data_byte_string()
					continue
				byte_string += "\0" * 3
			compressed_data = zlib.compress(byte_string)
			self.compressed_size = len(compressed_data)
			self._write_int_unassigned(self.compressed_size, output_stream)   # 4 byte
			output_stream.write(compressed_data)
		output_stream.seek(49125-self.compressed_size, 1)
		output_stream.write("\0")

	# #######################################
	# ###  Else
	# #######################################

	def get_number_of_blocks(self):
		"""

		@rtype: int
		"""
		return len(self.block_index_to_block)

	def get_position_by_block_index(self, block_index):
		"""

		@param block_index:
		@ptype block_index: int

		@rtype: tuple[int,int,int]
		"""
		# block size z 1024
		# block size y 32
		z = block_index / self._blocksize_z
		rest = block_index % self._blocksize_z
		y = rest / self._blocksize_y
		x = rest % self._blocksize_y
		return x+self.position[0], y+self.position[1], z+self.position[2]

	def get_block_index_by_position(self, position):
		"""

		@param position:
		@type position: tuple[int,int,int]

		@rtype: int
		"""
		# max_blocks 32768
		# block size z 1024
		# block size y 32
		assert isinstance(position, (list, tuple))
		# return (position[0] + self._blocksize_y*position[1] + self._blocksize_z*position[2]) % self._max_blocks
		return (position[0] % self._blocksize_y) + self._blocksize_y*(position[1] % self._blocksize_y) + self._blocksize_z*(position[2] % self._blocksize_y)

	def update(self, entity_type=0):
		"""

		@param entity_type:
		@type entity_type: int
		"""
		list_of_block_index = self.block_index_to_block.keys()
		for block_index in list_of_block_index:
			block = self.block_index_to_block[block_index]
			if not self._is_valid_block_id(block.get_id(), entity_type):
				self.remove_block(self.get_position_by_block_index(block_index))
				continue
			if block.get_id() not in self._docking_to_rails:
				continue
			updated_block_id = self._docking_to_rails[block.get_id()]
			if updated_block_id is None:
				self.remove_block(self.get_position_by_block_index(block_index))
				continue
			self.block_index_to_block[block_index].set_id(updated_block_id)

	def remove_block(self, block_position):
		"""

		@param block_position:
		@type block_position: tuple[int,int,int]
		"""
		assert isinstance(block_position, tuple)
		block_index = self.get_block_index_by_position(block_position)
		assert block_index in self.block_index_to_block, (block_index, block_position, self.get_position_by_block_index(block_index))
		# print "deleting", self.get_block_name_by_id(self.block_index_to_block[block_index].get_id())
		self.block_index_to_block.pop(block_index)
		if self.get_number_of_blocks() == 0:
			self._logger.debug("Segment {} has no more blocks.".format(self.position))
			self.has_valid_data = 0

	def add(self, block_position, block):
		"""

		@param block_position:
		@type block_position: tuple[int,int,int]
		@param block:
		@type block: SmdBlock
		"""
		assert isinstance(block, SmdBlock)
		if self.position is None:
			self.position = self.get_segment_position_of_position(block_position)
		block_index = self.get_block_index_by_position(block_position)
		self.block_index_to_block[block_index] = block
		self.has_valid_data = 1

	def search(self, block_id):
		"""

		@param block_id:
		@type block_id: int

		@rtype: None | tuple[int,int,int]
		"""
		for block_index, block in self.block_index_to_block.iteritems():
			if block.get_id() == block_id:
				return self.get_position_by_block_index(block_index)
		return None

	def iteritems(self):
		"""

		@rtype: tuple[tuple[int,int,int], SmdBlock]
		"""
		for block_index, block in self.block_index_to_block.iteritems():
			yield self.get_position_by_block_index(block_index), block

	def to_stream(self, output_stream=sys.stdout, summary=True):
		"""

		@param output_stream:
		@type output_stream: fileIO
		@param summary:
		@type summary: bool
		"""
		output_stream.write("Segment: {} '{}' ({})\n".format(
			self.position,
			datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
			# segment_data["timestamp"],
			self.version,
			))
		# output_stream.write("Valid: {}\n".format(self.has_valid_data == 1))
		output_stream.flush()
		if summary:
			return
		for block_index in sorted(self.block_index_to_block.keys()):
			output_stream.write("{}\t".format(self.get_position_by_block_index(block_index)))
			# output_stream.write("{}\t".format(block_index))
			self.block_index_to_block[block_index].to_stream(output_stream)
		output_stream.flush()
