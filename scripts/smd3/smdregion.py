__author__ = 'Peter Hofmann'

import sys
from scripts.loggingwrapper import DefaultLogging
from scripts.bit_and_bytes import BitAndBytes
from scripts.blueprintutils import BlueprintUtils
from smdblock import SmdBlock
from smdsegment import Smd3Segment


class SmdRegion(DefaultLogging, BlueprintUtils, BitAndBytes):

	# #######################################
	# ###  SmdRegion
	# #######################################

	def __init__(self, segments_in_a_line=16, logfile=None, verbose=False, debug=False):
		"""
		Constructor

		@param segments_in_a_line: The number of segments that fit beside each other within a region
		@type segments_in_a_line: int
		"""
		self._label = "SmdRegion"
		super(SmdRegion, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		self._segments_in_a_line = segments_in_a_line  # 16
		self._segments_in_an_area = self._segments_in_a_line * self._segments_in_a_line  # 256
		self._segments_in_a_cube = self._segments_in_an_area * self._segments_in_a_line  # 4096
		self.version = 33554432
		self.position_to_segment = {}
		# self.tail_data = ""

	# #######################################
	# ###  Read
	# #######################################

	def _read_segment_index(self, input_stream):
		"""
		Read a segment index from a byte stream
		The identifier is used to tell where in the file a segment is found.
		An identifier = 1 points to the first segment in the file and so on.
		segment position in file 	= (region header size) + (identifier - 1) * (segment data size)
									= (4+4096*4) + (identifier-1) * 49152

		The size is the actual size of the segment data, header (26 bytes) + size of compressed block data

		@param input_stream:
		@type input_stream: file

		@rtype: tuple[int, int]
		"""
		identifier = self._read_short_int_unassigned(input_stream)
		size = self._read_short_int_unassigned(input_stream)
		return identifier, size

	def _read_region_header(self, input_stream):
		"""
		Read region header to a byte stream
		The index of a segment is the linear representation of the location of a segment within a region.

		@param input_stream: input stream
		@type input_stream: fileIO

		@rtype: int
		"""
		self.version = self._read_int_unassigned(input_stream)
		# for _ in range(0, 16*16*16):
		number_of_segments = 0
		for index in range(0, self._segments_in_a_cube):
			identifier, size = self._read_segment_index(input_stream)
			# assert identifier == 0, index
			if identifier > 0:
				number_of_segments += 1
		return number_of_segments

	def _read_file(self, input_stream):
		"""
		Read region data from a byte stream

		@param input_stream: input stream
		@type input_stream: fileIO
		"""
		number_of_segments = self._read_region_header(input_stream)
		for _ in xrange(number_of_segments):
			segment = Smd3Segment(
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug)
			segment.read(input_stream)
			if segment.has_valid_data == 0:
				continue
			self.position_to_segment[tuple(segment.position)] = segment
		# self.tail_data = input_stream.read()

	def read(self, file_path):
		"""
		Read region data from a file

		@param file_path: region file path
		@type file_path: str
		"""
		# print file_path
		self._logger.debug("Reading file '{}'".format(file_path))
		with open(file_path, 'rb') as input_stream:
			self._read_file(input_stream)

	# #######################################
	# ###  Write
	# #######################################

	def _write_segment_index(self, identifier, size, output_stream):
		"""
		Write a segment index to a byte stream
		The identifier is used to tell where in the file a segment is found.
		An identifier = 1 points to the first segment in the file and so on.
		segment position in file 	= (region header size) + (identifier - 1) * (segment data size)
									= 16388 + (identifier-1) * 49152

		The size is the actual size of the segment data, header (26 bytes) + size of compressed block data

		@param identifier: segment position indicator within file
		@type identifier: int
		@param size: actual size of segment data
		@type size: int
		@param output_stream: output stream
		@type output_stream: fileIO
		"""
		self._write_short_int_unassigned(identifier, output_stream)
		self._write_short_int_unassigned(size, output_stream)

	def _write_region_header(self, output_stream):
		"""
		Write region header to a byte stream
		The index of a segment is the linear representation of the location of a segment within a region.

		@param output_stream: output stream
		@type output_stream: fileIO
		"""
		# Version
		self._write_int_unassigned(self.version, output_stream)

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
		@type output_stream: fileIO
		"""
		output_stream.seek(4+self._segments_in_a_cube*4)  # skip header: version(4byte) + 4096 segment index (4 byte)
		for position in sorted(self.position_to_segment.keys(), key=lambda tup: (tup[2], tup[1], tup[0])):
			segment = self.position_to_segment[position]
			assert isinstance(segment, Smd3Segment)
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
			self._write_file(output_stream)

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
			assert isinstance(segment, Smd3Segment)
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
				if self.position_to_segment[position_segment].has_valid_data == 1:
					self._logger.debug("'remove' NOT Removing empty segment {} WTF?.".format(position_segment))
					continue
				self._logger.debug("'remove' Removing empty segment {}.".format(position_segment))
				self.position_to_segment.pop(position_segment)

	def remove_block(self, block_position):
		"""
		Remove Block at specific position.

		@param block_position: x,z,y position of a block
		@type block_position: tuple[int,int,int]
		"""
		assert isinstance(block_position, tuple), block_position
		position_segment = self.get_segment_position_of_position(block_position)
		assert position_segment in self.position_to_segment, block_position
		self.position_to_segment[position_segment].remove_block(block_position)

	def add(self, block_position, block):
		"""
		Add a block to the segment based on its global position

		@param block_position: x,y,z position of block
		@type block_position: tuple[int,int,int]
		@param block: A block! :)
		@type block: SmdBlock
		"""
		assert isinstance(block, SmdBlock)
		position_segment = self.get_segment_position_of_position(block_position)
		if position_segment not in self.position_to_segment:
			self.position_to_segment[position_segment] = Smd3Segment(
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug)
			self.position_to_segment[position_segment].position = position_segment
		self.position_to_segment[position_segment].add(block_position, block)

	def search(self, block_id):
		"""
		Search and return the global position of the first occurance of a block
		If no block is found, return None

		@param block_id: Block id as found in utils class
		@type block_id: int

		@return: None or (x,y,z)
		@rtype: None | tuple[int,int,int]
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
		@rtype: generator(tuple[tuple[int,int,int], SmdBlock])
		"""
		for position_segment, segment in self.position_to_segment.iteritems():
			assert isinstance(segment, Smd3Segment)
			for position_block, block in segment.iteritems():
				yield position_block, block

	def to_stream(self, output_stream=sys.stdout, summary=True):
		"""
		Stream segment values

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
