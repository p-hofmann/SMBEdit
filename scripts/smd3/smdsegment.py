__author__ = 'Peter Hofmann'

import sys
import zlib
import datetime
from scripts.loggingwrapper import DefaultLogging
from scripts.bit_and_bytes import ByteStream
from scripts.blueprintutils import BlueprintUtils
from scripts.smd3.smdblock import SmdBlock


class SmdSegment(DefaultLogging, BlueprintUtils):
	"""
	Each segment represents an area the size of 32 x 32 x 32 (smd3) and contains 32768 blocks
	A Segment position is the lowest coordinate of a segment area.
	The Position coordinates are always a multiple of 32, like (32, 0, 128)
	Example: The core, or center of a blueprint is (16,16,16) and the position of its segment is (0,0,0)
	"""

	def __init__(self, blocks_in_a_line=32, logfile=None, verbose=False, debug=False):
		self._label = "SmdSegment {}".format(datetime.time)
		super(SmdSegment, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		self._blocks_in_a_line = blocks_in_a_line
		self._blocks_in_an_area = self._blocks_in_a_line * self._blocks_in_a_line
		self._blocks_in_a_cube = self._blocks_in_an_area * self._blocks_in_a_line
		self.version = 2
		self.timestamp = 0
		self.position = None
		self.has_valid_data = False
		self.compressed_size = 0
		self.block_index_to_block = {}

	# #######################################
	# ###  Read
	# #######################################

	def _read_header(self, input_stream):
		"""
		Read segment header data from a byte stream.
		Size: 26 byte

		@param input_stream: input byte stream
		@type input_stream: ByteStream
		"""
		self.version = input_stream.read_char()  # 1 byte
		self.timestamp = input_stream.read_int64_unassigned()
		self.position = input_stream.read_vector_3_int32()  # 12 byte
		self.has_valid_data = input_stream.read_bool()  # 1 byte
		self.compressed_size = input_stream.read_int32_unassigned()  # 4 byte

	def _read_block_data(self, input_stream):
		"""
		Read segment block data from a byte stream.
		Size: 49126 byte

		@param input_stream: input byte stream
		@type input_stream: ByteStream
		"""
		decompressed_data = zlib.decompress(input_stream.read(self.compressed_size))
		self.block_index_to_block = {}
		for block_index in range(0, len(decompressed_data)/3):
			position = block_index * 3
			block = SmdBlock()
			block.set_data_byte_string(decompressed_data[position:position+3])
			if block.get_id() > 0:
				self.block_index_to_block[block_index] = block
		input_stream.seek(49126-self.compressed_size, 1)  # skip unused bytes

	def read(self, input_stream):
		"""
		Read segment data from a byte stream.
		Always total size 49152 byte

		@param input_stream: input byte stream
		@type input_stream: ByteStream
		"""
		assert isinstance(input_stream, ByteStream)
		self._read_header(input_stream)
		if not self.has_valid_data:
			input_stream.seek(49126, 1)  # skip presumably empty bytes
		else:
			self._read_block_data(input_stream)
		if self.has_valid_data and len(self.block_index_to_block) == 0:
			self.has_valid_data = False

	# #######################################
	# ###  Write
	# #######################################

	def _write_block_data(self, output_stream):
		"""
		Write segment block data to a byte stream.
		Size: 49126 byte + 4 byte because of compressed_size

		@param output_stream: input byte stream
		@type output_stream: ByteStream
		"""
		if not self.has_valid_data:
			self.compressed_size = 0
			output_stream.write_int32_unassigned(self.compressed_size)   # 4 byte
		else:
			byte_string = ""
			set_of_valid_block_index = set(self.block_index_to_block.keys())
			for block_index in range(0, self._blocks_in_a_cube):
				if block_index in set_of_valid_block_index:
					byte_string += self.block_index_to_block[block_index].get_data_byte_string()
					continue
				byte_string += "\0" * 3
			compressed_data = zlib.compress(byte_string)
			self.compressed_size = len(compressed_data)
			output_stream.write_int32_unassigned(self.compressed_size)   # 4 byte
			output_stream.write(compressed_data)

		output_stream.seek(49125-self.compressed_size, 1)
		output_stream.write("\0")  # this should fill the skipped positions with \0

	def _write_header(self, output_stream):
		"""
		Write segment header data to a byte stream.
		Size: 26 byte - 4 byte

		@attention: compressed_size, 4 bytes, will be written later when the size is known

		@param output_stream: input byte stream
		@type output_stream: ByteStream
		"""
		output_stream.write_char(self.version)  # 1 byte
		output_stream.write_int64_unassigned(self.timestamp)  # 8 byte
		output_stream.write_vector_3_int32(self.position)  # 12 byte
		output_stream.write_bool(self.has_valid_data)  # 1 byte

	def write(self, output_stream):
		"""
		Write segment as binary data to any kind of stream.
		Always total size 49152 byte

		@param output_stream: Output byte stream
		@type output_stream: ByteStream
		"""
		assert isinstance(output_stream, ByteStream)
		self._write_header(output_stream)
		self._write_block_data(output_stream)

	# #######################################
	# ###  Index and positions
	# #######################################

	def get_block_position_by_block_index(self, block_index):
		"""
		Get global position based on local index

		@param block_index:
		@ptype block_index: int

		@return: (x,y,z), a global position
		@rtype: int, int, int
		"""
		# block size z 1024
		# block size y 32
		z = block_index / self._blocks_in_an_area
		rest = block_index % self._blocks_in_an_area
		y = rest / self._blocks_in_a_line
		x = rest % self._blocks_in_a_line
		return x+self.position[0], y+self.position[1], z+self.position[2]

	def get_block_index_by_block_position(self, position):
		"""
		Get block index of position in this segment

		@param position: x,y,z position of block
		@type position: int, int, int

		@return: index of block of this segment 0:32767
		@rtype: int
		"""
		assert isinstance(position, (list, tuple))
		return \
			(position[0] % self._blocks_in_a_line) + \
			(position[1] % self._blocks_in_a_line) * self._blocks_in_a_line + \
			(position[2] % self._blocks_in_a_line) * self._blocks_in_an_area

	# #######################################
	# ###  Else
	# #######################################

	def set_position(self, segment_position):
		"""
		Set position of segment

		@param segment_position: x,y,z position of segment
		@type segment_position: int, int, int
		"""
		self.position = segment_position

	def get_number_of_blocks(self):
		"""
		Get number of blocks of this segment

		@return: number of blocks in segment
		@rtype: int
		"""
		return len(self.block_index_to_block)

	def update(self, entity_type=0):
		"""
		Remove invalid/outdated blocks and exchange docking modules with rails

		@param entity_type: ship=0/station=2/etc
		@type entity_type: int
		"""
		assert entity_type in self._entity_types
		list_of_block_index = self.block_index_to_block.keys()
		for block_index in list_of_block_index:
			block = self.block_index_to_block[block_index]
			if not self._is_valid_block_id(block.get_id(), entity_type):
				self.remove_block(self.get_block_position_by_block_index(block_index))
				continue
			if block.get_id() not in self._docking_to_rails:
				continue
			updated_block_id = self._docking_to_rails[block.get_id()]
			if updated_block_id is None:
				self.remove_block(self.get_block_position_by_block_index(block_index))
				continue
			self.block_index_to_block[block_index].set_id(updated_block_id)

	def remove_block(self, block_position):
		"""
		Remove Block at specific position.

		@param block_position: x,z,y position of a block
		@type block_position: int,int,int
		"""
		assert isinstance(block_position, tuple)
		block_index = self.get_block_index_by_block_position(block_position)
		assert block_index in self.block_index_to_block, (block_index, block_position, self.get_block_position_by_block_index(block_index))
		# print "deleting", self.get_block_name_by_id(self.block_index_to_block[block_index].get_id())
		self.block_index_to_block.pop(block_index)
		if self.get_number_of_blocks() == 0:
			self._logger.debug("Segment {} has no more blocks.".format(self.position))
			self.has_valid_data = False

	def add(self, block_position, block):
		"""
		Add a block to the segment based on its global position

		@param block_position: x,y,z position of block
		@type block_position: int,int,int
		@param block: A block! :)
		@type block: SmdBlock
		"""
		assert isinstance(block, SmdBlock)
		block_index = self.get_block_index_by_block_position(block_position)
		self.block_index_to_block[block_index] = block
		self.has_valid_data = True

	def search(self, block_id):
		"""
		Search and return the global position of the first occurance of a block
		If no block is found, return None

		@param block_id: Block id as found in utils class
		@type block_id: int

		@return: None or (x,y,z)
		@rtype: None | int,int,int
		"""
		for block_index, block in self.block_index_to_block.iteritems():
			if block.get_id() == block_id:
				return self.get_block_position_by_block_index(block_index)
		return None

	def has_block_at_position(self, position):
		"""
		Returns true if a block exists at a position

		@param position: (x,y,z)
		@type position: int,int,int

		@return:
		@rtype: bool
		"""
		block_index = self.get_block_index_by_block_position(position)
		return block_index in self.block_index_to_block

	def iteritems(self):
		"""
		Iterate over each block and its global position, not the position within the segment

		@return: (x,y,z), block
		@rtype: tuple[int,int,int], SmdBlock
		"""
		for block_index, block in self.block_index_to_block.iteritems():
			yield self.get_block_position_by_block_index(block_index), block

	def to_stream(self, output_stream=sys.stdout, summary=True):
		"""
		Stream segment values

		@param output_stream: Output stream
		@type output_stream: fileIO
		@param summary: If true the output is reduced
		@type summary: bool
		"""
		output_stream.write("Segment: {} '{}' ({})\n".format(
			self.position,
			datetime.datetime.fromtimestamp(self.timestamp/1000.0).strftime('%Y-%m-%d %H:%M:%S'),
			self.version,
			))
		output_stream.flush()
		if summary:
			return
		for block_index in sorted(self.block_index_to_block.keys()):
			output_stream.write("{}\t".format(self.get_block_position_by_block_index(block_index)))
			# output_stream.write("{}\t".format(block_index))
			self.block_index_to_block[block_index].to_stream(output_stream)
		output_stream.flush()
