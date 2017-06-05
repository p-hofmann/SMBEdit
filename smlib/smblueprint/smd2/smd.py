__author__ = 'Peter Hofmann'

import sys
import os
import math

from ...loggingwrapper import DefaultLogging
from ...utils.blocklist import BlockList
from .smdregion import SmdRegion, StyleBasic


class Smd(DefaultLogging):
    """
    # #######################################
    # ###  smd
    # #######################################

    @type position_to_region: dict[tuple[int], SmdRegion]
    @type : BlockList
    """

    _core_position = 8

    def __init__(self, segments_in_a_line_of_a_region=16, blocks_in_a_line_of_a_segment=16, logfile=None, verbose=False, debug=False):
        """
        Constructor

        @param blocks_in_a_line_of_a_segment: The number of blocks that fit beside each other within a segment
        @type blocks_in_a_line_of_a_segment: int
        @param segments_in_a_line_of_a_region: The number of segments that fit beside each other within a region
        @type segments_in_a_line_of_a_region: int
        """
        super(Smd, self).__init__(
            label="Smd2",
            logfile=logfile,
            verbose=verbose,
            debug=debug)
        self._blocks_in_a_line_in_a_segment = blocks_in_a_line_of_a_segment
        self._segments_in_a_line_of_a_region = segments_in_a_line_of_a_region
        self.position_to_region = {}
        self._block_list = BlockList()
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, directory_blueprint):
        """
        Read smd data from files in the blueprint/data/ directory

        @param directory_blueprint: input directory path
        @type directory_blueprint: str
        """
        directory_data = os.path.join(directory_blueprint, "DATA")
        file_list = sorted(os.listdir(directory_data))
        assert len(file_list) > 0, "No smd files found"
        file_name = file_list[0]
        file_path = os.path.join(directory_data, file_name)
        if os.path.isdir(file_path) and file_name.startswith("ATTACHED_"):
            directory_data = os.path.join(directory_data, file_name)
            file_list = sorted(os.listdir(directory_data))
            assert len(file_list) > 0, "No smd files found"
        smd_region = SmdRegion(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        for file_name in file_list:
            file_path = os.path.join(directory_data, file_name)
            assert file_path.endswith(".smd2"), "Unexpected file extension: {}".format(file_path)
            smd_region.read(file_path, self._block_list)

    # #######################################
    # ###  Get
    # #######################################

    def get_block_list(self):
        """
        @rtype BlockPool:
        """
        return self._block_list

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
        return int(math.floor((value + blocks_in_a_line_in_a_region / 2) / float(blocks_in_a_line_in_a_region)))

    def get_number_of_blocks(self):
        """
        Get total number of blocks

        @return: number of blocks in segment
        @rtype: int
        """
        return len(self._block_list)

    def add(self, block_position, block, replace=True):
        """
        Add a block to the segment based on its global position

        @param block_position: x,y,z position of block
        @type block_position: int,int,int
        @param block:
        @type block: StyleBasic
        """
        assert isinstance(block_position, tuple)
        assert isinstance(block, StyleBasic)
        position_region = self.get_region_position_of_position(block_position)
        if position_region not in self.position_to_region:
            self.position_to_region[position_region] = SmdRegion(
                logfile=self._logfile,
                verbose=self._verbose,
                debug=self._debug)
        self.position_to_region[position_region].add(block_position, block, replace)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream smd values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("####\nSMD\n####\n\n")
        output_stream.write("Total blocks: {}\n\n".format(self.get_number_of_blocks()))
        for position in sorted(list(self.position_to_region.keys()), key=lambda tup: (tup[2], tup[1], tup[0])):
            output_stream.write("SmdRegion: {}\n".format(list(position)))
            self.position_to_region[position].to_stream(output_stream)
            output_stream.write("\n")
