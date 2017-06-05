__author__ = 'Peter Hofmann'

import sys
import os
import math

from ...loggingwrapper import DefaultLogging
from ...utils.blockconfig import block_config
from ...utils.blocklist import BlockList
from ...utils.vector import Vector
from ...utils.blueprintentity import BlueprintEntity
from ..smdblock.blockpool import block_pool, StyleBasic
from ..smd2.smd import Smd as Smd2
from .smdregion import SmdRegion



class Smd(DefaultLogging):
    """
    # #######################################
    # ###  smd
    # #######################################

    @type position_to_region: dict[tuple[int], SmdRegion]
    @type _block_list: BlockList
    """

    def __init__(self, segments_in_a_line_of_a_region=16, blocks_in_a_line_of_a_segment=32, logfile=None, verbose=False, debug=False):
        """
        Constructor

        @param blocks_in_a_line_of_a_segment: The number of blocks that fit beside each other within a segment
        @type blocks_in_a_line_of_a_segment: int
        @param segments_in_a_line_of_a_region: The number of segments that fit beside each other within a region
        @type segments_in_a_line_of_a_region: int
        """
        super(Smd, self).__init__(
            label="Smd3",
            logfile=logfile,
            verbose=verbose,
            debug=debug)
        self._position_core = (16, 16, 16)
        self._blocks_in_a_line_in_a_segment = blocks_in_a_line_of_a_segment
        self._segments_in_a_line_of_a_region = segments_in_a_line_of_a_region
        self._file_name_prefix = ""
        self.position_to_region = {}
        self._block_list = BlockList()
        return

    def __del__(self):
        list = self._block_list
        self._block_list = None
        del list

    # #######################################
    # ###  Read
    # #######################################

    def read(self, directory_blueprint):
        """
        Read smd data from files in the blueprint/data/ directory

        @param directory_blueprint: input directory path
        @type directory_blueprint: str
        """
        self._block_list = BlockList()
        directory_data = os.path.join(directory_blueprint, "DATA")
        file_list = sorted(os.listdir(directory_data))
        assert len(file_list) > 0, "No smd files found"
        file_name = file_list[0]
        file_path = os.path.join(directory_data, file_name)
        if os.path.isdir(file_path) and file_name.startswith("ATTACHED_"):
            directory_data = os.path.join(directory_data, file_name)
            file_list = sorted(os.listdir(directory_data))
            assert len(file_list) > 0, "No smd files found"
            file_name = file_list[0]
        if file_name.endswith(".smd3"):
            smd_region = SmdRegion(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
            for file_name in file_list:
                file_path = os.path.join(directory_data, file_name)
                self._file_name_prefix, x, y, z = os.path.splitext(file_name)[0].rsplit('.', 3)
                smd_region.read(file_path, self._block_list)
        elif file_name.endswith(".smd2"):
            self._logger.debug("'smd2' file format found.")
            msg = "'smd2'->'smd3' conversion can results in blocks with low hit points if '-sm' argument is not used."
            self._logger.debug(msg)
            smd2 = Smd2(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
            smd2.read(directory_blueprint)
            offset = (8, 8, 8)
            self._block_list = smd2.get_block_list()
            self._block_list.move_positions(offset)
        else:
            raise RuntimeError("Unknown smd format: '{}'".format(directory_data))

    # #######################################
    # ###  Write
    # #######################################

    def write(self, directory_blueprint, blueprint_name):
        """
        Write smd data to files in the blueprint/data/ directory

        @param directory_blueprint: output directory path
        @type directory_blueprint: str
        @param blueprint_name: name of blueprint
        @type blueprint_name: str
        """
        # move blocks from pool into smd data structure
        for position_block, block in self._block_list.pop_positions():
            self.add(position_block, block)
        directory_data = os.path.join(directory_blueprint, "DATA")
        if not os.path.exists(directory_data):
            os.mkdir(directory_data)
        # print self.position_to_region.keys()
        for position, region in self.position_to_region.items():
            assert isinstance(region, SmdRegion)
            file_name = blueprint_name + "." + ".".join(map(str, position)) + ".smd3"
            file_path = os.path.join(directory_data, file_name)
            region.write(file_path)

    # #######################################
    # ###  Get
    # #######################################

    def get_block_list(self):
        """
        @rtype BlockPool:
        """
        return self._block_list

    def get_block_at_position(self, position):
        """
        Get a block at a specific position

        @param position:
        @param position: (int, int, int)

        @return:
        @rtype: Block
        """

        return self._block_list[position]

    # ###  Index and positions

    def get_region_position_of_position(self, position):
        """
        Return the position of a region a position belongs to.

        @param position: Any global position like that of a block
        @type position: int, int, int

        @return:
        @rtype: int, int, int
        """
        return (
            self._get_region_position_of(position[0]),
            self._get_region_position_of(position[1]),
            self._get_region_position_of(position[2]))

    def _get_region_position_of(self, value):
        """
        Return the region coordinate

        @param value: any x or y or z coordinate
        @param value: int

        @return: segment x or y or z coordinate
        @rtype: int
        """
        blocks_in_a_line_in_a_region = self._blocks_in_a_line_in_a_segment * self._segments_in_a_line_of_a_region
        return int(math.floor((value + int(blocks_in_a_line_in_a_region / 2)) / float(blocks_in_a_line_in_a_region)))

    # #######################################
    # ###  moving blocks
    # #######################################

    def move_center(self, direction_vector):
        """
        Move center (core) in a specific direction

        @attention: The core/center never moves, but all other blocks do.

        @param direction_vector: (x,y,z)
        @type direction_vector: (int,int,int)
        @rtype: None
        """
        # test if core exists
        block_core = None
        if self._block_list.has_core():
            block_core = self._block_list.pop(self._position_core)

        new_direction_vector = Vector.multiplication((-1, -1, -1), direction_vector)
        self._block_list.move_positions(new_direction_vector)

        # return core if it existed
        if block_core is not None:
            self._block_list[self._position_core] = block_core

    def mirror(self, axis_index, reverse=False):
        """
        Mirror at center (core), top to bottom, left to right, front to back

        @param axis_index:  0: x left to right
                            1: y top to bottom
                            2: z front to back
        @type axis_index: int
        @type reverse: bool
        """
        vector_factor = [1] * 3
        vector_factor[axis_index] = -1
        for position_block, block in self._block_list.pop_positions():
            if position_block[axis_index] == self._position_core[axis_index]:
                self._block_list[position_block] = block
                continue
            if reverse:
                mirror = position_block[axis_index] < self._position_core[axis_index]
            else:
                mirror = position_block[axis_index] > self._position_core[axis_index]
            if not mirror:
                continue
            position_tmp = Vector.subtraction(position_block, self._position_core)
            position_tmp = Vector.multiplication(position_tmp, vector_factor)
            new_block_position = Vector.addition(position_tmp, self._position_core)
            new_block = block.get_mirror(axis_index)
            self._block_list[position_block] = block
            self._block_list[new_block_position] = new_block

    # #######################################
    # ###  Turning
    # #######################################

    def tilt_turn(self, tilt_index):
        """
        Turn or tilt this entity.

        @param tilt_index: integer representing a specific turn
        @type tilt_index: int
        """
        for position_block, block in self._block_list.pop_positions():
            new_block_position = position_block
            if block.get_id() != 1:  # core
                new_block_position = Vector.tilt_turn_position(position_block, tilt_index)
                # block.tilt_turn(tilt_index)  # todo: needs fixing
            self._block_list[new_block_position] = block

    # #######################################
    # ###  Else
    # #######################################

    def remove_blocks(self, block_ids):
        """
        Removing all blocks of a specific id

        @param block_ids:
        @type block_ids: set[int]
        """
        self._block_list.remove_blocks(block_ids)

    def get_number_of_blocks(self):
        """
        Get total number of blocks

        @return: number of blocks in segment
        @rtype: int
        """
        return len(self._block_list)

    def update(self):
        """
        Remove invalid/outdated blocks and exchange docking modules with rails
        """
        entity_type = 2
        if self._block_list.has_core():
            entity_type = 0

        invalid_ids = set()
        for position, block in self._block_list.items():
            if not block_config[block.get_id()].is_valid(entity_type):
                invalid_ids.add(block.get_id())
                continue
            if not block_config[block.get_id()].is_docking():
                continue
            updated_block_id = block_config[block.get_id()].get_rail_equivalent()
            if updated_block_id is None:
                invalid_ids.add(block.get_id())
                continue
            new_block = block.to_style6(block_id=updated_block_id)
            self._block_list[position] = new_block
        self._block_list.remove_blocks(invalid_ids)

    def add(self, block_position, block, replace=True):
        """
        Add a block to the segment based on its global position

        @param block_position: x,y,z position of block
        @type block_position: int,int,int
        @param block:
        @type block: StyleBasic
        """
        assert isinstance(block_position, tuple)
        assert isinstance(block, StyleBasic), block
        position_region = self.get_region_position_of_position(block_position)
        if position_region not in self.position_to_region:
            self.position_to_region[position_region] = SmdRegion(
                logfile=self._logfile,
                verbose=self._verbose,
                debug=self._debug)
        self.position_to_region[position_region].add(block_position, block, replace)

    def search(self, block_id):
        """
        Search and return the global position of the first occurrence of a block
        If no block is found, return None

        @param block_id: Block id as found in utils class
        @type block_id: int

        @return: None or (x,y,z)
        @rtype: None | int,int,int
        """
        return self._block_list.search(block_id)

    def search_all(self, block_id):
        """
        Search and return the global position of block positions

        @param block_id: Block id as found in utils class
        @type block_id: int

        @return: None or (x,y,z)
        @rtype: set[(int, int, int)]
        """
        return self._block_list.search_positions(set(block_id))

    def has_block_at(self, position):
        """
        Returns true if a block exists at a position

        @param position: (x,y,z)
        @type position: int,int,int

        @return:
        @rtype: bool
        """
        return self._block_list.has_block_at(position)

    def get_block_id_to_quantity(self):
        """
        Return the quantity of each block type

        @return: dictionary of block id to the quantity of that block type
        @rtype: dict[int, int]
        """
        block_id_to_quantity = {}
        for position, block in self._block_list.items():
            if block.get_id() not in block_id_to_quantity:
                block_id_to_quantity[block.get_id()] = 0
            block_id_to_quantity[block.get_id()] += 1
        return block_id_to_quantity

    def set_type(self, entity_type):
        """
        Change entity type of blueprint
        0: "Ship",
        2: "Station",

        @param entity_type:
        @type entity_type: int
        """
        assert isinstance(entity_type, int)
        assert entity_type in BlueprintEntity.entity_types

        if entity_type == 0:  # Ship
            core_block = block_pool(1).get_modified_block(block_id=1, active=False)
            self._block_list[self._position_core] = core_block
        else:  # not a ship
            if self._block_list.has_core(self._position_core):
                self._block_list.pop(self._position_core)
        self.update()  # remove blocks invalid for ships and other cleanup

    def get_min_max_vector(self):
        """
        Get the minimum and maximum coordinates of the blueprint

        @return: Minimum(x,y,z), Maximum(x,y,z)
        @rtype: tuple[int,int,int], tuple[int,int,int]
        """
        min_vector = [16, 16, 16]
        max_vector = [16, 16, 16]
        for position_block, block in self._block_list.items():
            for index, value in enumerate(position_block):
                if value < min_vector[index]:
                    min_vector[index] = value
                if value > max_vector[index]:
                    max_vector[index] = value
        return tuple(min_vector), tuple(max_vector)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream smd values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("####\nSMD\n####\n\n")
        output_stream.write("Total blocks: {}\n\n".format(self.get_number_of_blocks()))
        if self._debug:
            for position_block, block in sorted(self._block_list.items()):
                output_stream.write("{}\t{}\t".format(position_block, block.get_int_24()))
                block.to_stream(output_stream)
            output_stream.write("\n")
