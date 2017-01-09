from __future__ import division
from __future__ import unicode_literals
from builtins import range
from past.utils import old_div
__author__ = 'Peter Hofmann'

import sys
import zlib
import datetime

from lib.loggingwrapper import DefaultLogging
from lib.bits_and_bytes import ByteStream
from lib.blueprint.blueprintutils import BlueprintUtils
from lib.blueprint.smd2.smdblock import SmdBlock


class SmdSegment(DefaultLogging, BlueprintUtils):
    """
    Each segment represents an area the size of 32 x 32 x 32 (smd3) and contains 32768 blocks
    A Segment position is the lowest coordinate of a segment area.
    The Position coordinates are always a multiple of 32, like (32, 0, 128)
    Example: The core, or center of a blueprint is (16,16,16) and the position of its segment is (0,0,0)

    @type block_index_to_block: dict[int, SmdBlock]
    """

    def __init__(self, version, blocks_in_a_line=16, logfile=None, verbose=False, debug=False):
        self._label = "SmdSegment {}".format(datetime.time)
        super(SmdSegment, self).__init__(
            logfile=logfile,
            verbose=verbose,
            debug=debug)
        self._blocks_in_a_line = blocks_in_a_line
        self._blocks_in_an_area = self._blocks_in_a_line * self._blocks_in_a_line
        self._blocks_in_a_cube = self._blocks_in_an_area * self._blocks_in_a_line
        self._region_version = version
        self._version = 0
        self._timestamp = 0
        self._position = None
        self._has_valid_data = False
        self._compressed_size = 0
        self.block_index_to_block = {}
        self._header_size = 26
        if self._region_version == 0:
            self._header_size = 25
        self._data_size = 5120-self._header_size

    # #######################################
    # ###  Read
    # #######################################

    def _read_header(self, input_stream):
        """
        Read segment header data from a byte stream.
        Size: 25/26 byte

        @param input_stream: input byte stream
        @type input_stream: ByteStream
        """
        if self._region_version != 0:
            self._version = input_stream.read_byte()  # 1 byte
        self._timestamp = input_stream.read_int64_unassigned()  # 8 byte
        self._position = input_stream.read_vector_3_int32()  # 12 byte
        self._has_valid_data = input_stream.read_bool()  # 1 byte
        self._compressed_size = input_stream.read_int32_unassigned()  # 4 byte

    def _read_block_data(self, input_stream):
        """
        Read segment block data from a byte stream.
        Size: 49126 byte

        @param input_stream: input byte stream
        @type input_stream: ByteStream
        """
        decompressed_data = zlib.decompress(input_stream.read(self._compressed_size))
        self.block_index_to_block = {}
        for block_index in range(0, old_div(len(decompressed_data),3)):
            position = block_index * 3
            block = SmdBlock(debug=self._debug)
            int_24bit = ByteStream.unpack_int24(decompressed_data[position:position+3])
            block.set_int_24bit(int_24bit)
            if block.get_id() > 0:
                self.block_index_to_block[block_index] = block
        input_stream.seek(self._data_size-self._compressed_size, 1)  # skip unused bytes

    def read(self, input_stream):
        """
        Read segment data from a byte stream.
        Always total size 49152 byte

        @param input_stream: input byte stream
        @type input_stream: ByteStream
        """
        assert isinstance(input_stream, ByteStream)
        self._read_header(input_stream)
        if not self._has_valid_data:
            input_stream.seek(self._data_size, 1)  # skip presumably empty bytes
        else:
            self._read_block_data(input_stream)
        if self._has_valid_data and len(self.block_index_to_block) == 0:
            self._has_valid_data = False

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
        if not self._has_valid_data:
            self._compressed_size = 0
            output_stream.write_int32_unassigned(self._compressed_size)   # 4 byte
        else:
            byte_string = ""
            set_of_valid_block_index = set(self.block_index_to_block.keys())
            for block_index in range(0, self._blocks_in_a_cube):
                if block_index in set_of_valid_block_index:
                    block_int_24 = self.block_index_to_block[block_index].get_int_24bit()
                    byte_string += ByteStream.pack_int24(block_int_24)
                    continue
                byte_string += "\0" * 3
            compressed_data = zlib.compress(byte_string)
            self._compressed_size = len(compressed_data)
            output_stream.write_int32_unassigned(self._compressed_size)   # 4 byte
            output_stream.write(compressed_data)

        output_stream.seek((self._data_size-1)-self._compressed_size, 1)
        output_stream.write("\0")  # this should fill the skipped positions with \0

    def _write_header(self, output_stream):
        """
        Write segment header data to a byte stream.
        Size: 26 byte - 4 byte

        @attention: compressed_size, 4 bytes, will be written later when the size is known

        @param output_stream: input byte stream
        @type output_stream: ByteStream
        """
        output_stream.write_byte(self._version)  # 1 byte
        output_stream.write_int64_unassigned(self._timestamp)  # 8 byte
        output_stream.write_vector_3_int32(self._position)  # 12 byte
        output_stream.write_bool(self._has_valid_data)  # 1 byte

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
        @rtype: tuple[int]
        """
        # block size z 1024
        # block size y 32
        z = old_div(block_index, self._blocks_in_an_area)
        rest = block_index % self._blocks_in_an_area
        y = old_div(rest, self._blocks_in_a_line)
        x = rest % self._blocks_in_a_line
        return x+self._position[0], y+self._position[1], z+self._position[2]

    def get_block_index_by_block_position(self, position):
        """
        Get block index of position in this segment

        @param position: x,y,z position of block
        @type position: tuple[int]

        @return: index of block of this segment 0:32767
        @rtype: int
        """
        assert isinstance(position, (list, tuple))
        return \
            (position[0] % self._blocks_in_a_line) + \
            (position[1] % self._blocks_in_a_line) * self._blocks_in_a_line + \
            (position[2] % self._blocks_in_a_line) * self._blocks_in_an_area

    # #######################################
    # ###  Get
    # #######################################

    def get_block_at_position(self, position):
        """
        Get a block at a specific position

        @param position:
        @param position: tuple[int]

        @return:
        @rtype: SmdBlock
        """
        block_index = self.get_block_index_by_block_position(position)
        assert block_index in self.block_index_to_block
        return self.block_index_to_block[block_index]

    def get_number_of_blocks(self):
        """
        Get number of blocks of this segment

        @return: number of blocks in segment
        @rtype: int
        """
        return len(self.block_index_to_block)

    def has_block_at_position(self, position):
        """
        Returns true if a block exists at a position

        @param position: (x,y,z)
        @type position: tuple[int]

        @return:
        @rtype: bool
        """
        block_index = self.get_block_index_by_block_position(position)
        return block_index in self.block_index_to_block

    # #######################################
    # ###  Set
    # #######################################

    def set_position(self, segment_position):
        """
        Set position of segment

        @param segment_position: x,y,z position of segment
        @type segment_position: tuple[int]
        """
        self._position = segment_position

    # #######################################
    # ###  Get
    # #######################################

    def replace_blocks(self, block_id, replace_id, replace_hp, compatible=False):
        """
        Replace all blocks of a specific id
        """
        for block_index in list(self.block_index_to_block.keys()):
            if self.block_index_to_block[block_index].get_id() == block_id:
                if compatible:
                    self.block_index_to_block[block_index].set_id(replace_id)
                    self.block_index_to_block[block_index].set_hit_points(replace_hp)
                else:
                    new_block = SmdBlock(debug=self._debug)
                    new_block.set_id(block_id)
                    new_block.set_hit_points(replace_hp)
                    self.block_index_to_block[block_index] = new_block

    _replace_cache_positive = {}
    _replace_cache_negative = set()

    def replace_hull(self, new_hull_type, hull_type=None):
        """
        Replace all blocks of a specific hull type or all hull

        @param new_hull_type:
        @type new_hull_type: int
        @param hull_type:
        @type hull_type: int | None
        """
        for block_index in list(self.block_index_to_block.keys()):
            block_id = self.block_index_to_block[block_index].get_id()
            if not self.is_hull(block_id or block_id in self._replace_cache_negative):
                continue
            if block_id not in self._replace_cache_positive:
                block_hull_type, color, shape_id = self._get_hull_details(block_id)
                if hull_type is not None and hull_type != block_hull_type:  # not replaced
                    self._replace_cache_negative.add(block_id)
                    continue
                new_block_id = self.get_hull_id_by_details(new_hull_type, color, shape_id)
                self._replace_cache_positive[block_id] = new_block_id
            self.block_index_to_block[block_index].set_id(self._replace_cache_positive[block_id])
            self.block_index_to_block[block_index].set_hit_points(self.get_hp_by_hull_type(new_hull_type))

    def update(self, entity_type=0):
        """
        Remove invalid/outdated blocks and exchange docking modules with rails

        @param entity_type: ship=0/station=2/etc
        @type entity_type: int
        """
        assert entity_type in self._entity_types
        list_of_block_index = list(self.block_index_to_block.keys())
        for block_index in list_of_block_index:
            block = self.block_index_to_block[block_index]
            if not self.is_valid_block_id(block.get_id(), entity_type):
                self.remove_block(self.get_block_position_by_block_index(block_index))
                continue
            if block.get_id() not in self.docking_to_rails:
                continue
            updated_block_id = self.docking_to_rails[block.get_id()]
            if updated_block_id is None:
                self.remove_block(self.get_block_position_by_block_index(block_index))
                continue
            self.block_index_to_block[block_index].set_id(updated_block_id)

    def remove_blocks(self, block_id):
        """
        Removing all blocks of a specific id

        @param block_id:
        @type block_id: int
        """
        for block_index in list(self.block_index_to_block.keys()):
            if self.block_index_to_block[block_index].get_id() != block_id:
                continue
            self.block_index_to_block.pop(block_index)
        if self.get_number_of_blocks() == 0:
            self._logger.debug("Segment {} has no more blocks.".format(self._position))
            self._has_valid_data = False

    def remove_block(self, block_position):
        """
        Remove Block at specific position.

        @param block_position: x,z,y position of a block
        @type block_position: tuple[int]
        """
        assert isinstance(block_position, tuple)
        block_index = self.get_block_index_by_block_position(block_position)
        assert block_index in self.block_index_to_block, (
            block_index, block_position, self.get_block_position_by_block_index(block_index))
        # print "deleting", self.get_block_name_by_id(self.block_index_to_block[block_index].get_id())
        self.block_index_to_block.pop(block_index)
        if self.get_number_of_blocks() == 0:
            self._logger.debug("Segment {} has no more blocks.".format(self._position))
            self._has_valid_data = False

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
        self._has_valid_data = True

    def search(self, block_id):
        """
        Search and return the global position of the first occurance of a block
        If no block is found, return None

        @param block_id: Block id as found in utils class
        @type block_id: int

        @return: None or (x,y,z)
        @rtype: None | tuple[int]
        """
        for block_index, block in list(self.block_index_to_block.items()):
            if block.get_id() == block_id:
                return self.get_block_position_by_block_index(block_index)
        return None

    def search_all(self, block_id):
        """
        Search and return the global position of block positions

        @param block_id: Block id as found in utils class
        @type block_id: int

        @return: None or (x,y,z)
        @rtype: set[tuple[int]]
        """
        positions = set()
        for block_index, block in list(self.block_index_to_block.items()):
            if block.get_id() == block_id:
                positions.add(self.get_block_position_by_block_index(block_index))
        return positions

    def iteritems(self):
        """
        Iterate over each block and its global position, not the position within the segment

        @return: (x,y,z), block
        @rtype: tuple[int], SmdBlock
        """
        for block_index, block in list(self.block_index_to_block.items()):
            yield self.get_block_position_by_block_index(block_index), block

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream segment values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("Segment: {} '{}' ({})\n".format(
            self._position,
            datetime.datetime.fromtimestamp(old_div(self._timestamp,1000.0)).strftime('%Y-%m-%d %H:%M:%S'),
            self._version,
            ))
        output_stream.flush()
        if self._debug:
            for block_index in sorted(self.block_index_to_block.keys()):
                output_stream.write("{}\t".format(self.get_block_position_by_block_index(block_index)))
                # output_stream.write("{}\t".format(block_index))
                self.block_index_to_block[block_index].to_stream(output_stream)
        output_stream.flush()
