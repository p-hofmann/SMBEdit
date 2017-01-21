from lib.blueprint.smd3.orientation.orientation import Orientation


__author__ = 'Peter Hofmann'


class Style2Corner(Orientation):
    """
    Type            Bits                    Description
    Type 2          19     23     22        The axis of rotation.
                                            000 : +Y
                                            001 : -Y
                                            010 : -Z
                                            011 : +Z
                                            100 : -X
                                            101 : +X
                    21     20               An amount of rotation around the axis of rotation,
                                            in 90-degree step

    @type _orientation_to_tuple_str: dict[tuple[int], tuple[str]]
    @type _tuple_str_to_orientation: dict[tuple[str], tuple[int]]
    """
    # https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

    _orientation_to_tuple_str = {
        # (19,23,22,rot): square side, wedge sides
        (0, 0, 0, 0): ("Bottom", "Front", "Right"),
        (0, 0, 0, 1): ("Bottom", "Back", "Right"),
        (0, 0, 0, 2): ("Bottom", "Back", "Left"),
        (0, 0, 0, 3): ("Bottom", "Front", "Left"),

        (0, 0, 1, 0): ("Top", "Front", "Right"),
        (0, 0, 1, 1): ("Top", "Back", "Right"),
        (0, 0, 1, 2): ("Top", "Back", "Left"),
        (0, 0, 1, 3): ("Top", "Front", "Left"),

        (0, 1, 0, 0): ("Back", "Top", "Right"),
        (0, 1, 0, 1): ("Back", "Top", "Left"),
        (0, 1, 0, 2): ("Back", "Bottom", "Left"),
        (0, 1, 0, 3): ("Back", "Bottom", "Right"),

        (0, 1, 1, 0): ("Front", "Bottom", "Right"),
        (0, 1, 1, 1): ("Front", "Top", "Right"),
        (0, 1, 1, 2): ("Front", "Top", "Left"),
        (0, 1, 1, 3): ("Front", "Bottom", "Left"),

        (1, 0, 0, 0): ("Right", "Back", "Bottom"),
        (1, 0, 0, 1): ("Right", "Back", "Top"),
        (1, 0, 0, 2): ("Right", "Front", "Top"),
        (1, 0, 0, 3): ("Right", "Front", "Bottom"),

        (1, 0, 1, 0): ("Left", "Back", "Bottom"),
        (1, 0, 1, 1): ("Left", "Back", "Top"),
        (1, 0, 1, 2): ("Left", "Front", "Top"),
        (1, 0, 1, 3): ("Left", "Front", "Bottom")
    }

    _tuple_str_to_orientation = {
        # square side, wedge sides: (19,23,22,rot)
        ("Bottom", "Front", "Right"): (0, 0, 0, 0),
        ("Bottom", "Back", "Right"): (0, 0, 0, 1),
        ("Bottom", "Back", "Left"): (0, 0, 0, 2),
        ("Bottom", "Front", "Left"): (0, 0, 0, 3),

        ("Top", "Front", "Right"): (0, 0, 1, 0),
        ("Top", "Back", "Right"): (0, 0, 1, 1),
        ("Top", "Back", "Left"): (0, 0, 1, 2),
        ("Top", "Front", "Left"): (0, 0, 1, 3),

        ("Back", "Top", "Right"): (0, 1, 0, 0),
        ("Back", "Top", "Left"): (0, 1, 0, 1),
        ("Back", "Bottom", "Left"): (0, 1, 0, 2),
        ("Back", "Bottom", "Right"): (0, 1, 0, 3),

        ("Front", "Bottom", "Right"): (0, 1, 1, 0),
        ("Front", "Top", "Right"): (0, 1, 1, 1),
        ("Front", "Top", "Left"): (0, 1, 1, 2),
        ("Front", "Bottom", "Left"): (0, 1, 1, 3),

        ("Right", "Back", "Bottom"): (1, 0, 0, 0),
        ("Right", "Back", "Top"): (1, 0, 0, 1),
        ("Right", "Front", "Top"): (1, 0, 0, 2),
        ("Right", "Front", "Bottom"): (1, 0, 0, 3),

        ("Left", "Back", "Bottom"): (1, 0, 1, 0),
        ("Left", "Back", "Top"): (1, 0, 1, 1),
        ("Left", "Front", "Top"): (1, 0, 1, 2),
        ("Left", "Front", "Bottom"): (1, 0, 1, 3)
    }

    def to_string(self):
        """
        @rtype: str
        """
        orientation = self.get_orientation()
        tuple_str = self._orientation_to_tuple_str[orientation]
        square = tuple_str[0]
        slopes = ", ".join(tuple_str[1:])
        return "Square sides: {}, sloped sides: {}".format(square, slopes)

    # #######################################
    # ###  Mirror
    # #######################################

    def mirror_x(self):
        """
        Mirror Left - Right
        """
        bit_19, bit_23, bit_22, rotations = self.get_orientation()
        tuple_str = self._orientation_to_tuple_str[(bit_19, bit_23, bit_22, rotations)]
        replacements = {"Left": "Right", "Right": "Left"}
        tuple_str = self._replace_string(tuple_str, replacements)
        bit_19, bit_23, bit_22, rotations = self._tuple_str_to_orientation[tuple_str]
        self._int_24bit = self._bits_combine_orientation(
            self._int_24bit, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)

    def mirror_y(self):
        """
        Mirror Top - Bottom
        """
        bit_19, bit_23, bit_22, rotations = self.get_orientation()
        tuple_str = self._orientation_to_tuple_str[(bit_19, bit_23, bit_22, rotations)]
        replacements = {"Top": "Bottom", "Bottom": "Top"}
        tuple_str = self._replace_string(tuple_str, replacements)
        bit_19, bit_23, bit_22, rotations = self._tuple_str_to_orientation[tuple_str]
        self._int_24bit = self._bits_combine_orientation(
            self._int_24bit, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)

    # front - back
    def mirror_z(self):
        """
        Mirror Front - Back
        """
        bit_19, bit_23, bit_22, rotations = self.get_orientation()
        tuple_str = self._orientation_to_tuple_str[(bit_19, bit_23, bit_22, rotations)]
        replacements = {"Front": "Back", "Back": "Front"}
        tuple_str = self._replace_string(tuple_str, replacements)
        bit_19, bit_23, bit_22, rotations = self._tuple_str_to_orientation[tuple_str]
        self._int_24bit = self._bits_combine_orientation(
            self._int_24bit, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)
