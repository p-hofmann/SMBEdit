__author__ = 'Peter Hofmann'

import sys

from smlib.utils.blockconfig import block_config
from smlib.smblueprint.smdblock.blockbits import BlockBits
# from smlib.smblueprint.smdblock.blockhandler import block_pool


class StyleBasic(BlockBits):

    def __call__(self, int_24, version=None):
        """
        @type int_24: int
        @type version: int

        @rtype: StyleBasic
        """
        self._int_24 = int_24
        self._version = version

    def __repr__(self):
        return "{}".format(block_config[self.get_id()].name)

    # #######################################
    # ###  Mirror
    # #######################################

    def get_mirror(self, axis_index):
        """
        Mirror orientation
        @type axis_index: int

        @rtype: StyleBasic
        """
        from smlib.smblueprint.smdblock.blockpool import block_pool
        if axis_index == 0:
            return block_pool(self._mirror_x())
        if axis_index == 1:
            return block_pool(self._mirror_y())
        if axis_index == 2:
            return block_pool(self._mirror_z())
        raise RuntimeError("Unknown Axis index: {}".format(axis_index))

    def _mirror_x(self):
        """
        Mirror orientation

        @rtype: int
        """
        pass

    def _mirror_y(self):
        """
        Mirror orientation

        @rtype: int
        """
        pass

    # front - back
    def _mirror_z(self):
        """
        Mirror orientation

        @rtype: int
        """
        pass

    # #######################################
    # ###  Stream
    # #######################################

    def to_string(self):
        pass

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream block values

        @param output_stream:
        @type output_stream: fileIO
        """
        block_id = self.get_id()
        output_stream.write("{} ({})\t".format(block_id, block_config[block_id].block_style))
        output_stream.write("HP: {}\t".format(self.get_hit_points()))
        output_stream.write("Active: {}\t".format(self.is_active()))
        output_stream.write("Or.: {}\t".format(self.to_string()))
        output_stream.write("{}\n".format(block_config[block_id].name))

    # #######################################
    # ###  Convert
    # #######################################

    def to_style6(self, block_id):
        """
        Return a side to type 6 orientation conversion, focusing on forward and up

        @type block_id: int

        @rtype: StyleBasic
        """
        pass

    def convert(self, version):
        """
        @type version: int
        @rtype: None
        """
        block_id = self.get_id()
        active = self._get_active_bit()
        rotations = self.get_rotations()
        axis_rotation = self.get_axis_rotation()
        block_side_id = self.get_block_side_id()
        self._version = version
        self._int_24 = self.get_modified_int_24bit(
            block_id=block_id, active=active,
            block_side_id=block_side_id, axis_rotation=axis_rotation, rotations=rotations)

    @staticmethod
    def _replace_string(tuple_str, replacements):
        """
        @type tuple_str: tuple[str]
        @type replacements: dict[str, str]
        """
        tmp_list = list(tuple_str)
        for index, word in enumerate(tuple_str):
            if word in replacements:
                tmp_list[index] = replacements[word]
                return tuple(tmp_list)
        return tuple(tmp_list)
