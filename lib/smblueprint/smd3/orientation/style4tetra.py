from lib.smblueprint.smd3.orientation.orientation import Orientation


__author__ = 'Peter Hofmann'


class Style4Tetra(Orientation):
    """
    Type            Bits                    Description
    Type 4          19     23     22        The axis of rotation.
                                            000 : +Y
                                            001 : -Y
                    21     20               An amount of rotation around the axis of rotation,
                                            in 90-degree step

    @type _orientation_to_tuple_str: dict[tuple[int], tuple[str]]
    @type _tuple_str_to_orientation: dict[tuple[str], tuple[int]]
    """
    # https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

    _orientation_to_tuple_str = {
        # 19: 0
        # 23: 0
        # (22,rot): slope sides
        (0, 0): ("Bottom", "Front", "Right"),
        (0, 1): ("Bottom", "Back", "Right"),
        (0, 2): ("Bottom", "Back", "Left"),
        (0, 3): ("Bottom", "Front", "Left"),

        (1, 0): ("Top", "Front", "Right"),
        (1, 1): ("Top", "Back", "Right"),
        (1, 2): ("Top", "Back", "Left"),
        (1, 3): ("Top", "Front", "Left")
    }

    _tuple_str_to_orientation = {
        # (22,rot): slope sides
        ("Bottom", "Front", "Right"): (0, 0),
        ("Bottom", "Back", "Right"): (0, 1),
        ("Bottom", "Back", "Left"): (0, 2),
        ("Bottom", "Front", "Left"): (0, 3),

        ("Top", "Front", "Right"): (1, 0),
        ("Top", "Back", "Right"): (1, 1),
        ("Top", "Back", "Left"): (1, 2),
        ("Top", "Front", "Left"): (1, 3)
    }

    def to_string(self):
        """
        @rtype: str
        """
        orientation = self.get_orientation()
        tuple_str = self._orientation_to_tuple_str[orientation]
        slopes = ", ".join(tuple_str)
        return "Sloped sides: {}".format(slopes)

    # #######################################
    # ###  Mirror
    # #######################################

    def mirror_x(self):
        """
        Mirror Left - Right
        """
        rotations = self._get_rotations()
        bit_22 = self._get_bit_22()
        tuple_str = self._orientation_to_tuple_str[(bit_22, rotations)]
        replacements = {"Left": "Right", "Right": "Left"}
        tuple_str = self._replace_string(tuple_str, replacements)
        bit_22, rotations = self._tuple_str_to_orientation[tuple_str]
        self._int_24bit = self._bits_combine_orientation(
            self._int_24bit, bit_22=bit_22, rotations=rotations)

    def mirror_y(self):
        """
        Mirror Top - Bottom
        """
        rotations = self._get_rotations()
        bit_22 = self._get_bit_22()
        bit_22 = (bit_22 + 1) % 2
        self._int_24bit = self._bits_combine_orientation(
            self._int_24bit, bit_22=bit_22, rotations=rotations)

    # front - back
    def mirror_z(self):
        """
        Mirror Front - Back
        """
        rotations = self._get_rotations()
        bit_22 = self._get_bit_22()
        tuple_str = self._orientation_to_tuple_str[(bit_22, rotations)]
        replacements = {"Front": "Back", "Back": "Front"}
        tuple_str = self._replace_string(tuple_str, replacements)
        bit_22, rotations = self._tuple_str_to_orientation[tuple_str]
        self._int_24bit = self._bits_combine_orientation(
            self._int_24bit, bit_22=bit_22, rotations=rotations)