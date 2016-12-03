__author__ = 'Peter Hofmann'

import sys
import math
from scripts.loggingwrapper import DefaultLogging
from scripts.bit_and_bytes import ByteStream
from scripts.blueprintutils import BlueprintUtils
from smdblock import SmdBlock
from smdsegment import SmdSegment


class SmdRegion(DefaultLogging, BlueprintUtils):

	# #######################################
	# ###  SmdRegion
	# #######################################

	def __init__(self, segments_in_a_line=16, blocks_in_a_line=32, logfile=None, verbose=False, debug=False):
		"""
		Constructor

		@param blocks_in_a_line: The number of blocks that fit beside each other within a segment
		@type blocks_in_a_line: int
		@param segments_in_a_line: The number of segments that fit beside each other within a region
		@type segments_in_a_line: int
		"""
		self._label = "SmdRegion"
		super(SmdRegion, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		self._blocks_in_a_line_in_a_segment = blocks_in_a_line
		self._segments_in_a_line = segments_in_a_line  # 16
		self._segments_in_an_area = self._segments_in_a_line * self._segments_in_a_line  # 256
		self._segments_in_a_cube = self._segments_in_an_area * self._segments_in_a_line  # 4096
		self.version = 33554432
		self.position_to_segment = {}
		# self.tail_data = ""

	# #######################################
	# ###  Read
	# #######################################

	@staticmethod
	def _read_segment_index(input_stream):
		"""
		Read a segment index from a byte stream
		The identifier is used to tell where in the file a segment is found.
		An identifier = 1 points to the first segment in the file and so on.
		segment position in file 	= (region header size) + (identifier - 1) * (segment data size)
									= (4+4096*4) + (identifier-1) * 49152

		The size is the actual size of the segment data, header (26 bytes) + size of compressed block data

		@param input_stream: input stream
		@type input_stream: ByteStream

		@rtype: int, int
		"""
		identifier = input_stream.read_int16_unassigned()
		size = input_stream.read_int16_unassigned()
		return identifier, size

	def _read_region_header(self, input_stream):
		"""
		Read region header to a byte stream
		The index of a segment is the linear representation of the location of a segment within a region.

		@param input_stream: input stream
		@type input_stream: ByteStream

		@rtype: int
		"""
		self.version = input_stream.read_int32_unassigned()
		number_of_segments = 0
		for index in range(0, self._segments_in_a_cube):
			identifier, size = self._read_segment_index(input_stream)
			if identifier > 0:
				number_of_segments += 1
		return number_of_segments

	def _read_file(self, input_stream):
		"""
		Read region data from a byte stream

		@param input_stream: input stream
		@type input_stream: ByteStream
		"""
		number_of_segments = self._read_region_header(input_stream)
		for _ in xrange(number_of_segments):
			segment = SmdSegment(
				blocks_in_a_line=self._blocks_in_a_line_in_a_segment,
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug)
			segment.read(input_stream)
			if not segment.has_valid_data:
				continue
			self.position_to_segment[segment.position] = segment

	def read(self, file_path):
		"""
		Read region data from a file

		@param file_path: region file path
		@type file_path: str
		"""
		# print file_path
		self._logger.debug("Reading file '{}'".format(file_path))
		with open(file_path, 'rb') as input_stream:
			self._read_file(ByteStream(input_stream))

	# #######################################
	# ###  Write
	# #######################################

	@staticmethod
	def _write_segment_index(identifier, size, output_stream):
		"""
		Write a segment index to a byte stream
		The identifier is used to tell where in the file a segment is found.
		An identifier = 1 points to the first segment in the file and so on.
		segment position in file 	= (region header size) + (identifier - 1) * (segment data size)
									= 16388 + (identifier-1) * 49152

		The size is the actual size of the segment data, header (26 bytes) + size of compressed block data

		@param identifier: segment position indicator within file
		@type identifier: int
		@param size: actual size of segment data: segment_header_size + compressed_size
		@type size: int
		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		output_stream.write_int16_unassigned(identifier)
		output_stream.write_int16_unassigned(size)

	def _write_region_header(self, output_stream):
		"""
		Write region header to a byte stream
		The index of a segment is the linear representation of the location of a segment within a region.

		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		# Version
		output_stream.write_int32_unassigned(self.version)

		# segment index
		segment_header_size = 26
		# for _ in range(0, 16*16*16):
		segment_index_to_size = dict()
		for position, segment in self.position_to_segment.iteritems():
			segment_index = self.get_segment_index_by_position(position)
			segment_index_to_size[segment_index] = self.position_to_segment[position].compressed_size + segment_header_size

		seg_id = 0
		for segment_index in range(0, self._segments_in_a_cube):
			if segment_index not in segment_index_to_size:
				self._write_segment_index(0, 0, output_stream)
				continue
			seg_id += 1
			self._write_segment_index(seg_id, segment_index_to_size[segment_index], output_stream)

	def _write_file(self, output_stream):
		"""
		Write region data to a byte stream

		@param output_stream: output stream
		@type output_stream: ByteStream
		"""
		output_stream.seek(4+self._segments_in_a_cube*4)  # skip header: version(4byte) + 4096 segment index (4 byte)
		for position in sorted(self.position_to_segment.keys(), key=lambda tup: (tup[2], tup[1], tup[0])):
			segment = self.position_to_segment[position]
			assert isinstance(segment, SmdSegment)
			segment.write(output_stream)
		output_stream.seek(0)  # jump back for header
		self._write_region_header(output_stream)

	def write(self, file_path):
		"""
		Write region data to a file

		@param file_path: region file path
		@type file_path: str
		"""
		# print file_path
		with open(file_path, 'wb') as output_stream:
			self._write_file(ByteStream(output_stream))

	# #######################################
	# ###  Index and positions
	# #######################################

	def get_segment_position_of_position(self, position):
		"""
		Return the position of a segment a position belongs to.

		@param position: Any global position like that of a block
		@type position: int, int, int

		@return:
		@rtype: int, int, int
		"""
		return self._get_segment_position_of(position[0]), self._get_segment_position_of(position[1]), self._get_segment_position_of(position[2])

	def _get_segment_position_of(self, value):
		"""
		Return the segment coordinate

		@param value: any x or y or z coordinate
		@param value: int

		@return: segment x or y or z coordinate
		@rtype: int
		"""
		return int(math.floor(value / float(self._blocks_in_a_line_in_a_segment)) * self._blocks_in_a_line_in_a_segment)

	def get_segment_index_by_position(self, segment_position):
		"""
		Get segment index of position in this segment
		Unlike segments, a region has an offset (so the core is roughly in the center of a region)
		The offset is half width of a region in number of blocks.

		@param segment_position: x,y,z
		@type segment_position: int, int, int

		@rtype: int
		"""
		assert isinstance(segment_position, (list, tuple))
		# max_blocks 32768
		offset = self._blocks_in_a_line_in_a_segment * self._segments_in_a_line / 2
		tmp = [0, 0, 0]
		bialias = float(self._blocks_in_a_line_in_a_segment)
		tmp[0] = int(math.floor((segment_position[0]+offset) / bialias))
		tmp[1] = int(math.floor((segment_position[1]+offset) / bialias))
		tmp[2] = int(math.floor((segment_position[2]+offset) / bialias))
		return \
			(tmp[0] % self._segments_in_a_line) + \
			(tmp[1] % self._segments_in_a_line) * self._segments_in_a_line + \
			(tmp[2] % self._segments_in_a_line) * self._segments_in_an_area

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
		for position, segment in self.position_to_segment.iteritems():
			assert isinstance(segment, SmdSegment)
			number_of_blocks += segment.get_number_of_blocks()
		return number_of_blocks

	def update(self, entity_type=0):
		"""
		Remove invalid/outdated blocks and exchange docking modules with rails

		@param entity_type: ship=0/station=2/etc
		@type entity_type: int
		"""
		list_of_position_segment = self.position_to_segment.keys()
		for position_segment in list_of_position_segment:
			self.position_to_segment[position_segment].update(entity_type)
		self._remove_empty_segments()

	def _remove_empty_segments(self):
		"""
		Search for and remove segments with no blocks
		"""
		list_of_positions = self.position_to_segment.keys()
		for position_segment in list_of_positions:
			if self.position_to_segment[position_segment].get_number_of_blocks() == 0:
				self._logger.debug("'remove' Removing empty segment {}.".format(position_segment))
				self.position_to_segment.pop(position_segment)

	def remove_block(self, block_position):
		"""
		Remove Block at specific position.

		@param block_position: x,z,y position of a block
		@type block_position: int,int,int
		"""
		assert isinstance(block_position, tuple), block_position
		position_segment = self.get_segment_position_of_position(block_position)
		assert position_segment in self.position_to_segment, block_position
		self.position_to_segment[position_segment].remove_block(block_position)

	def add(self, block_position, block):
		"""
		Add a block to the segment based on its global position

		@param block_position: x,y,z position of block
		@type block_position: int, int, int
		@param block: A block! :)
		@type block: SmdBlock
		"""
		assert isinstance(block, SmdBlock)
		position_segment = self.get_segment_position_of_position(block_position)
		if position_segment not in self.position_to_segment:
			self.position_to_segment[position_segment] = SmdSegment(
				blocks_in_a_line=self._blocks_in_a_line_in_a_segment,
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug)
			self.position_to_segment[position_segment].set_position(position_segment)
		self.position_to_segment[position_segment].add(block_position, block)

	def search(self, block_id):
		"""
		Search and return the global position of the first occurrence of a block
		If no block is found, return None

		@param block_id: Block id as found in utils class
		@type block_id: int

		@return: None or (x,y,z)
		@rtype: None | int,int,int
		"""
		for position, segment in self.position_to_segment.iteritems():
			block_position = segment.search(block_id)
			if block_position is not None:
				return block_position
		return None

	def iteritems(self):
		"""
		Iterate over each block and its global position, not the position within the segment

		@return: (x,y,z), block
		@rtype: tuple[int,int,int], SmdBlock
		"""
		for position_segment, segment in self.position_to_segment.iteritems():
			assert isinstance(segment, SmdSegment)
			for position_block, block in segment.iteritems():
				yield position_block, block

	def to_stream(self, output_stream=sys.stdout, summary=True):
		"""
		Stream region values

		@param output_stream: Output stream
		@type output_stream: fileIO
		@param summary: If true the output is reduced
		@type summary: bool
		"""
		output_stream.write("Version: {}\n".format(self.version))
		# output_stream.write("Segments: {}\n{}\n".format(len(self._segment_to_size), sorted(self._segment_to_size.keys())))
		output_stream.write("Segments: {}\n".format(len(self.position_to_segment)))
		# output_stream.write("Tail: {} bytes\n\n".format(len(self.tail_data)))
		if self._debug:
			for position in sorted(self.position_to_segment.keys(), key=lambda tup: (tup[2], tup[1], tup[0])):
				self.position_to_segment[position].to_stream(output_stream, summary)
		output_stream.write("\n")
		output_stream.flush()
