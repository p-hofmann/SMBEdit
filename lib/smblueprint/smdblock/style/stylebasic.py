__author__ = 'Peter Hofmann'

import sys

from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.blockbits import BlockBits


class StyleBasic(BlockBits):

    def __repr__(self):
        return "{}".format(block_config[self.get_id()].name)

    # #######################################
    # ###  Mirror
    # #######################################

    def get_mirror(self, axis_index):
        """
        Mirror orientation
        @type axis_index: int

        @rtype: int
        """
        if axis_index == 0:
            return self._mirror_x()
        if axis_index == 1:
            return self._mirror_y()
        if axis_index == 2:
            return self._mirror_z()

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

        @rtype: int
        """
        pass

    def convert(self, version):
        """
        @type version: int
        @rtype: StyleBasic
        """
        block_id = self.get_id()
        active = self._get_active_bit()
        rotations = self.get_rotations()
        axis_rotation = self.get_axis_rotation()
        block_side_id = self.get_block_side_id()
        return StyleBasic(self._int_24bit, version=version).get_modified_int_24bit(
            block_id=block_id, active=active,
            block_side_id=block_side_id, axis_rotation=axis_rotation, rotations=rotations)

    def to_v2(self):
        """
        @rtype: StyleBasic
        """
        return self.convert(2)

    def to_v3(self):
        """
        @rtype: StyleBasic
        """
        return self.convert(3)
