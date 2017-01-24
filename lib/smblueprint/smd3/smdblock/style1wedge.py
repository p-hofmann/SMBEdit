from lib.smblueprint.smd3.smdblock.orientation import Orientation, BitAndBytes


__author__ = 'Peter Hofmann'


class Style1Wedge(Orientation):
    """
    Type        Bits                Description
    Type 1      23     22           The axis of rotation.
                                    00 : +Y
                                    01 : -Y
                                    10 : -Z
                                    11 : +Z
                21     20           The amount of clockwise rotation around the axis of rotation, in 90-degree steps

    @type _orientation_to_str: dict[tuple[int], str]
    """
    # https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

    _orientation_to_str = {
        # 19: 0
        # (19,23,22,rot): square sides
        (0, 0, 0, 0): "Bottom, Front",
        (0, 0, 0, 1): "Bottom, Left",
        (0, 0, 0, 2): "Bottom, Back",
        (0, 0, 0, 3): "Bottom, Right",

        (0, 0, 1, 0): "Top, Front",
        (0, 0, 1, 1): "Top, Right",
        (0, 0, 1, 2): "Top, Back",
        (0, 0, 1, 3): "Top, Left",

        (0, 1, 0, 0): "Right, Front",
        (0, 1, 0, 1): "Right, Back",
        (0, 1, 0, 2): "Left, Front",
        (0, 1, 0, 3): "Left, Back",
    }

    def to_string(self):
        """
        @rtype: str
        """
        orientation = self.get_orientation_values()
        return "Square sides: {}".format(self._orientation_to_str[orientation])

    def bit_combine(self, new_int_24bit, bit_23=None, bit_22=None, rotations=None, **kwargs):
        """
        Set orientation bits of an integer

        @type new_int_24bit: int
        @type bit_22: int
        @type bit_23: int
        @type rotations: int

        @rtype: int
        """
        if rotations is None:
            rotations = self._get_rotations()
        if bit_22 is None:
            bit_22 = self._get_bit_22()
        if bit_23 is None:
            bit_23 = self._get_bit_23()
        new_int_24bit <<= 5
        new_int_24bit >>= 5
        new_int_24bit = BitAndBytes.bits_combine(rotations, new_int_24bit, Orientation._bit_rotation_start)
        new_int_24bit = BitAndBytes.bits_combine(bit_22, new_int_24bit, 22)
        new_int_24bit = BitAndBytes.bits_combine(bit_23, new_int_24bit, 23)
        return new_int_24bit

    # #######################################
    # ###  Mirror
    # #######################################

    def mirror_x(self):
        """
        Mirror left - right
        """
        rotations = self._get_rotations()
        bit_23 = self._get_bit_23()
        if bit_23 == 0 and rotations % 2 == 0:
            # no change
            return
        rotations = (rotations + 2) % 4
        self._int_24bit = self.bit_combine(self._int_24bit, rotations=rotations)

    def mirror_y(self):
        """
        Mirror Top - Bottom
        """
        bit_22 = self._get_bit_22()
        bit_23 = self._get_bit_23()
        if bit_23 == 1:
            # no change
            return
        bit_22 = (bit_22 + 1) % 2
        self._int_24bit = self.bit_combine(self._int_24bit, bit_22=bit_22)

    # front - back
    def mirror_z(self):
        """
        Mirror front - back
        """
        rotations = self._get_rotations()
        bit_23 = self._get_bit_23()
        if bit_23 == 0:
            if rotations % 2 == 1:
                # no change
                return
            rotations = (rotations + 2) % 4
        else:
            rotations = (rotations + 1) % 4
        self._int_24bit = self.bit_combine(self._int_24bit, rotations=rotations)
