__author__ = 'Peter Hofmann'

import sys
import math

from lib.loggingwrapper import DefaultLogging
from lib.binarystream import BinaryStream
from lib.smblueprint.smd3.smdsegment import SmdSegment, StyleBasic


class SmdRegion(DefaultLogging):
    """
    # #######################################
    # ###  SmdRegion
    # #######################################

    @type position_to_segment: dict[tuple[int], SmdSegment]
    """

    _valid_versions = {
        (2, 0, 0, 0),
        (3, 0, 0, 0),
        }

    def __init__(self, segments_in_a_line=16, blocks_in_a_line=32, logfile=None, verbose=False, debug=False):
        """
        Constructor

        @param blocks_in_a_line: The number of blocks that fit beside each other within a segment
        @type blocks_in_a_line: int
        @param segments_in_a_line: The number of segments that fit beside each other within a region
        @type segments_in_a_line: int
        """
        super(SmdRegion, self).__init__(label="SmdRegion", logfile=logfile, verbose=verbose, debug=debug)
        self._blocks_in_a_line_in_a_segment = blocks_in_a_line
        self._segments_in_a_line = segments_in_a_line  # 16
        self._segments_in_an_area = self._segments_in_a_line * self._segments_in_a_line  # 256
        self._segments_in_a_cube = self._segments_in_an_area * self._segments_in_a_line  # 4096
        self.version = (3, 0, 0, 0)
        self.position_to_segment = {}
        # self.tail_data = ""

    # #######################################
    # ###  Read
    # #######################################

    @staticmethod
    def _is_eof(input_stream):
        """
        Read region header to a byte stream
        The index of a segment is the linear representation of the location of a segment within a region.

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        if not input_stream.read(1):
            return True
        input_stream.seek(-1, whence=1)
        return False

    @staticmethod
    def _read_segment_index(input_stream):
        """
        Read a segment index from a byte stream
        The identifier is used to tell where in the file a segment is found.
        An identifier = 1 points to the first segment in the file and so on.
        segment position in file     = (region header size) + (identifier - 1) * (segment data size)
                                    = (4+4096*4) + (identifier-1) * 49152

        The size is the actual size of the segment data, header (26 bytes) + size of compressed block data

        @param input_stream: input stream
        @type input_stream: BinaryStream

        @rtype: list[int]
        """
        identifier = input_stream.read_int16_unassigned()
        size = input_stream.read_int16_unassigned()
        return identifier, size

    def _read_region_header(self, input_stream):
        """
        Read region header to a byte stream
        The index of a segment is the linear representation of the location of a segment within a region.

        @param input_stream: input stream
        @type input_stream: BinaryStream

        @rtype: dict[int, int]
        """
        self.version = input_stream.read_vector_4_byte()
        assert self.version in self._valid_versions, "Unsupported smd version: {}".format(self.version)
        segment_id_to_size = {}
        for index in range(0, self._segments_in_a_cube):
            identifier, size = self._read_segment_index(input_stream)
            if identifier > 0:
                segment_id_to_size[identifier] = size
        return segment_id_to_size

    def _read_file(self, block_list, input_stream):
        """
        Read region data from a byte stream

        @type block_list: BlockList
        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        segment_id_to_size = self._read_region_header(input_stream)
        segment_id = 0  # ids start with 1
        segment = SmdSegment(
            blocks_in_a_line=self._blocks_in_a_line_in_a_segment,
            logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        while not self._is_eof(input_stream):
            segment_id += 1
            if segment_id not in segment_id_to_size or segment_id_to_size[segment_id] == 0:
                # skip ghost segment
                input_stream.seek(49152, 1)
                continue
            segment.read(block_list, input_stream)

    def read(self, file_path, block_list):
        """
        Read region data from a file

        @param file_path: region file path
        @type file_path: str
        @type block_list: BlockList
        """
        # print file_path
        self._logger.info("Reading file '{}'".format(file_path))
        with open(file_path, 'rb') as input_stream:
            self._read_file(block_list, BinaryStream(input_stream))

    # #######################################
    # ###  Write
    # #######################################

    @staticmethod
    def _write_segment_index(identifier, size, output_stream):
        """
        Write a segment index to a byte stream
        The identifier is used to tell where in the file a segment is found.
        An identifier = 1 points to the first segment in the file and so on.
        segment position in file     = (region header size) + (identifier - 1) * (segment data size)
                                    = 16388 + (identifier-1) * 49152

        The size is the actual size of the segment data, header (26 bytes) + size of compressed block data

        @param identifier: segment position indicator within file
        @type identifier: int
        @param size: actual size of segment data: segment_header_size + compressed_size
        @type size: int
        @param output_stream: output stream
        @type output_stream: BinaryStream
        """
        output_stream.write_int16_unassigned(identifier)
        output_stream.write_int16_unassigned(size)

    def _write_region_header(self, output_stream):
        """
        Write region header to a byte stream
        The index of a segment is the linear representation of the location of a segment within a region.

        @param output_stream: output stream
        @type output_stream: BinaryStream
        """
        # Version
        output_stream.write_vector_4_byte(self.version)
        # output_stream.write_int32_unassigned(self.version)

        # segment index
        segment_header_size = 26
        # for _ in range(0, 16*16*16):
        segment_index_to_size = dict()
        for position, segment in self.position_to_segment.items():
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
        @type output_stream: BinaryStream
        """
        output_stream.seek(4+self._segments_in_a_cube*4)  # skip header: version(4byte) + 4096 segment index (4 byte)
        for position in sorted(list(self.position_to_segment.keys()), key=lambda tup: (tup[2], tup[1], tup[0])):
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
        self.version = max(self._valid_versions)
        with open(file_path, 'wb') as output_stream:
            self._write_file(BinaryStream(output_stream))

    # #######################################
    # ###  Get
    # #######################################

    # ###  Index and positions

    def get_segment_position_of_position(self, position):
        """
        Return the position of a segment a position belongs to.

        @param position: Any global position like that of a block
        @type position: tuple[int]

        @return:
        @rtype: tuple[int]
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
        @type segment_position: tuple[int]

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
    # ###  Set
    # #######################################

    def add(self, block_position, block, replace=True):
        """
        Add a block to the segment based on its global position

        @param block_position: x,y,z position of block
        @type block_position: tuple[int]
        @param block:
        @type block: StyleBasic
        """
        position_segment = self.get_segment_position_of_position(block_position)
        if position_segment not in self.position_to_segment:
            self.position_to_segment[position_segment] = SmdSegment(
                blocks_in_a_line=self._blocks_in_a_line_in_a_segment,
                logfile=self._logfile,
                verbose=self._verbose,
                debug=self._debug)
            self.position_to_segment[position_segment].set_position(position_segment)
        self.position_to_segment[position_segment].add(block_position, block, replace)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream region values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("Version: {}\n".format(self.version))
        output_stream.write("Segments: {}\n".format(len(self.position_to_segment)))
        if self._debug or self._verbose:
            for position in sorted(list(self.position_to_segment.keys()), key=lambda tup: (tup[2], tup[1], tup[0])):
                self.position_to_segment[position].to_stream(output_stream)
        output_stream.write("\n")
        output_stream.flush()
