from lib.smblueprint.smdblock.style.stylebasic import StyleBasic


__author__ = 'Peter Hofmann'


class Style2Corner(StyleBasic):
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
        # (axis,rotation): square side, wedge sides
        (0, 0): ("Bottom", "Front", "Right"),
        (0, 1): ("Bottom", "Back", "Right"),
        (0, 2): ("Bottom", "Back", "Left"),
        (0, 3): ("Bottom", "Front", "Left"),

        (1, 0): ("Top", "Front", "Right"),
        (1, 1): ("Top", "Back", "Right"),
        (1, 2): ("Top", "Back", "Left"),
        (1, 3): ("Top", "Front", "Left"),

        (2, 0): ("Back", "Top", "Right"),
        (2, 1): ("Back", "Top", "Left"),
        (2, 2): ("Back", "Bottom", "Left"),
        (2, 3): ("Back", "Bottom", "Right"),

        (3, 0): ("Front", "Bottom", "Right"),
        (3, 1): ("Front", "Top", "Right"),
        (3, 2): ("Front", "Top", "Left"),
        (3, 3): ("Front", "Bottom", "Left"),

        (4, 0): ("Right", "Back", "Bottom"),
        (4, 1): ("Right", "Back", "Top"),
        (4, 2): ("Right", "Front", "Top"),
        (4, 3): ("Right", "Front", "Bottom"),

        (5, 0): ("Left", "Back", "Bottom"),
        (5, 1): ("Left", "Back", "Top"),
        (5, 2): ("Left", "Front", "Top"),
        (5, 3): ("Left", "Front", "Bottom")
    }

    _tuple_str_to_orientation = {
        # square side, wedge sides: (axis,rotation)
        ("Bottom", "Front", "Right"): (0, 0),
        ("Bottom", "Back", "Right"): (0, 1),
        ("Bottom", "Back", "Left"): (0, 2),
        ("Bottom", "Front", "Left"): (0, 3),

        ("Top", "Front", "Right"): (1, 0),
        ("Top", "Back", "Right"): (1, 1),
        ("Top", "Back", "Left"): (1, 2),
        ("Top", "Front", "Left"): (1, 3),

        ("Back", "Top", "Right"): (2, 0),
        ("Back", "Top", "Left"): (2, 1),
        ("Back", "Bottom", "Left"): (2, 2),
        ("Back", "Bottom", "Right"): (2, 3),

        ("Front", "Bottom", "Right"): (3, 0),
        ("Front", "Top", "Right"): (3, 1),
        ("Front", "Top", "Left"): (3, 2),
        ("Front", "Bottom", "Left"): (3, 3),

        ("Right", "Back", "Bottom"): (4, 0),
        ("Right", "Back", "Top"): (4, 1),
        ("Right", "Front", "Top"): (4, 2),
        ("Right", "Front", "Bottom"): (4, 3),

        ("Left", "Back", "Bottom"): (5, 0),
        ("Left", "Back", "Top"): (5, 1),
        ("Left", "Front", "Top"): (5, 2),
        ("Left", "Front", "Bottom"): (5, 3)
    }

    def to_string(self):
        """
        @rtype: str
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        tuple_str = self._orientation_to_tuple_str[(axis_rotation, rotations)]
        square = tuple_str[0]
        slopes = ", ".join(tuple_str[1:])
        return "Square sides: {}, sloped sides: {}".format(square, slopes)

    # #######################################
    # ###  Mirror
    # #######################################

    def _mirror_x(self):
        """
        Mirror Left - Right
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        tuple_str = self._orientation_to_tuple_str[(axis_rotation, rotations)]
        replacements = {"Left": "Right", "Right": "Left"}
        tuple_str = self._replace_string(tuple_str, replacements)
        axis_rotation, rotations = self._tuple_str_to_orientation[tuple_str]
        return self.modify_orientation(
            self._int_24, rotations=rotations, axis_rotation=axis_rotation)

    def _mirror_y(self):
        """
        Mirror Top - Bottom
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        tuple_str = self._orientation_to_tuple_str[(axis_rotation, rotations)]
        replacements = {"Top": "Bottom", "Bottom": "Top"}
        tuple_str = self._replace_string(tuple_str, replacements)
        axis_rotation, rotations = self._tuple_str_to_orientation[tuple_str]
        return self.modify_orientation(
            self._int_24, rotations=rotations, axis_rotation=axis_rotation)

    # front - back
    def _mirror_z(self):
        """
        Mirror Front - Back
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        tuple_str = self._orientation_to_tuple_str[(axis_rotation, rotations)]
        replacements = {"Front": "Back", "Back": "Front"}
        tuple_str = self._replace_string(tuple_str, replacements)
        axis_rotation, rotations = self._tuple_str_to_orientation[tuple_str]
        return self.modify_orientation(
            self._int_24, rotations=rotations, axis_rotation=axis_rotation)
