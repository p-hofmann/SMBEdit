from lib.smblueprint.smd3.smdblock.orientation import Orientation, BitAndBytes


__author__ = 'Peter Hofmann'


class Style0(Orientation):
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

    def bit_combine(self, new_int_24bit, block_side_id=None, **kwargs):
        """
        Set orientation bits of an integer

        @type new_int_24bit: int
        @type block_side_id: int

        @rtype: int
        """
        if block_side_id is None:
            block_side_id = self.get_block_side_id()
        new_int_24bit &= 0b000011111111111111111111
        return BitAndBytes.bits_combine(block_side_id, new_int_24bit, Orientation._bit_block_side_start)

    def to_style6_bits(self):
        """
        Return style 6 bits representing side id

        @rtype: tuple[int]
        """
        side_id = self.get_block_side_id()
        assert side_id in self._block_side_id_to_type_6, "Bad side id: {}".format(side_id)
        return self._block_side_id_to_type_6[side_id]

    # #######################################
    # ###  Mirror
    # #######################################

    def mirror_x(self):
        """
        Mirror left - right
        """
        side_id = self.get_block_side_id()
        side_id = Style0._turn_y_90(side_id)
        side_id = Style0._turn_y_90(side_id)
        int_24 = self._int_24bit
        self._int_24bit = self.bit_combine(int_24, block_side_id=side_id)

    def mirror_y(self):
        """
        Mirror top - down
        """
        side_id = self.get_block_side_id()
        side_id = Style0._turn_z_90(side_id)
        side_id = Style0._turn_z_90(side_id)
        int_24 = self._int_24bit
        self._int_24bit = self.bit_combine(int_24, block_side_id=side_id)

    # front - back
    def mirror_z(self):
        """
        Mirror front - back
        """
        side_id = self.get_block_side_id()
        side_id = Style0._turn_x_90(side_id)
        side_id = Style0._turn_x_90(side_id)
        int_24 = self._int_24bit
        self._int_24bit = self.bit_combine(int_24, block_side_id=side_id)

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
