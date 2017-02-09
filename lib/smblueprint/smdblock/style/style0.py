from lib.bits_and_bytes import BitAndBytes
from lib.smblueprint.smdblock.style.stylebasic import StyleBasic
from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.style.style6 import Style6


__author__ = 'Peter Hofmann'


class Style0(StyleBasic):
    """
    Type        Bits                Description
    Type0       23     22     21    The block facing
                              19    0: active
                              19    1: not active

    @type _orientation_to_str: dict[int, str]
    """
    # https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

    _orientation_to_str = {
        # 19: 1
        0: "FRONT ",
        1: "BACK  ",
        2: "TOP   ",
        3: "BOTTOM",
        4: "RIGHT ",
        5: "LEFT  ",
    }

    def to_string(self):
        """
        @rtype: str
        """
        side_id = self.get_block_side_id()
        return "Facing: {}".format(self._orientation_to_str[side_id])

    def modify_orientation(self, new_int_24bit, block_side_id=None, **kwargs):
        """
        Set orientation bits of an integer

        @type new_int_24bit: int
        @type block_side_id: int

        @rtype: int
        """
        if block_side_id is None:
            block_side_id = self.get_block_side_id()
        new_int_24bit &= 0b000001111111111111111111
        if self._version < 3:
            return BitAndBytes.bits_combine(block_side_id, new_int_24bit, 20)
        return BitAndBytes.bits_combine(block_side_id, new_int_24bit, 19)

    def to_style6(self, block_id):
        """
        Return a side to type 6 orientation conversion, focusing on forward and up

        @type block_id: int

        @rtype: StyleBasic
        """
        assert block_config[block_id].block_style == 6
        side_id = self.get_block_side_id()
        assert side_id in self._block_side_id_to_type_6, "Bad side id: {}".format(side_id)
        axis_rotation, rotations = self._block_side_id_to_type_6[side_id]
        return Style6(block_id, self._version).get_modified_int_24bit(
            block_id=block_id, active=False,
            axis_rotation=axis_rotation, rotations=rotations)

    # #######################################
    # ###  Mirror
    # #######################################

    def _mirror_x(self):
        """
        Mirror left - right
        """
        side_id = self.get_block_side_id()
        if side_id not in [4, 5]:
            return
        side_id = Style0._turn_y_90(side_id)
        side_id = Style0._turn_y_90(side_id)
        int_24 = self._int_24bit
        self._int_24bit = self.modify_orientation(int_24, block_side_id=side_id)

    def _mirror_y(self):
        """
        Mirror top - down
        """
        side_id = self.get_block_side_id()
        if side_id not in [2, 3]:
            return
        side_id = Style0._turn_z_90(side_id)
        side_id = Style0._turn_z_90(side_id)
        int_24 = self._int_24bit
        self._int_24bit = self.modify_orientation(int_24, block_side_id=side_id)

    # front - back
    def _mirror_z(self):
        """
        Mirror front - back
        """
        side_id = self.get_block_side_id()
        if side_id not in [0, 1]:
            return
        side_id = Style0._turn_x_90(side_id)
        side_id = Style0._turn_x_90(side_id)
        int_24 = self._int_24bit
        self._int_24bit = self.modify_orientation(int_24, block_side_id=side_id)

    # #######################################
    # ###  Turning type 0
    # #######################################

    @staticmethod
    def _turn_x_90(side_id):
        """
        @type side_id: int
        @return: int
        """
        return {
            0: 3,
            1: 2,
            2: 0,
            3: 1,
            4: 4,
            5: 5,
        }[side_id]

    @staticmethod
    def _turn_x_270(side_id):
        """
        @type side_id: int
        @return: int
        """
        return {
            0: 2,
            1: 3,
            2: 1,
            3: 0,
            4: 4,
            5: 5,
        }[side_id]

    @staticmethod
    def _turn_y_90(side_id):
        """
        @type side_id: int
        @return: int
        """
        return {
            0: 4,
            1: 5,
            2: 2,
            3: 3,
            4: 1,
            5: 0,
        }[side_id]

    @staticmethod
    def _turn_y_270(side_id):
        """
        @type side_id: int
        @return: int
        """
        return {
            0: 5,
            1: 4,
            2: 2,
            3: 3,
            4: 0,
            5: 1,
        }[side_id]

    @staticmethod
    def _turn_z_90(side_id):
        """
        @type side_id: int
        @return: int
        """
        return {
            0: 0,
            1: 1,
            2: 4,
            3: 5,
            4: 3,
            5: 2,
        }[side_id]

    @staticmethod
    def _turn_z_270(side_id):
        """
        @type side_id: int
        @return: int
        """
        return {
            0: 0,
            1: 1,
            2: 5,
            3: 4,
            4: 2,
            5: 3,
        }[side_id]
