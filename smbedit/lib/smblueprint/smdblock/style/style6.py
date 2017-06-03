from lib.smblueprint.smdblock.style.style2corner import Style2Corner


__author__ = 'Peter Hofmann'


class Style6(Style2Corner):
    """
    Type            Bits                    Description
    Type 6          19     23     22        The axis of rotation.
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

    # shipyard and rails
    _orientation_to_tuple_str = {
        # (axis,rotation): icon faces, icon pointing towards
        (0, 0): ("Front", "Bottom"),
        (0, 1): ("Front", "Left"),
        (0, 2): ("Front", "Top"),
        (0, 3): ("Front", "Right"),

        (1, 0): ("Back", "Bottom"),
        (1, 1): ("Back", "Left"),
        (1, 2): ("Back", "Top"),
        (1, 3): ("Back", "Right"),

        (2, 0): ("Bottom", "Back"),
        (2, 1): ("Bottom", "Left"),
        (2, 2): ("Bottom", "Front"),
        (2, 3): ("Bottom", "Right"),

        (3, 0): ("Top", "Back"),
        (3, 1): ("Top", "Left"),
        (3, 2): ("Top", "Front"),
        (3, 3): ("Top", "Right"),

        (4, 0): ("Right", "Front"),
        (4, 1): ("Right", "Top"),
        (4, 2): ("Right", "Back"),
        (4, 3): ("Right", "Bottom"),

        (5, 0): ("Left", "Front"),
        (5, 1): ("Left", "Top"),
        (5, 2): ("Left", "Back"),
        (5, 3): ("Left", "Bottom")
    }

    _tuple_str_to_orientation = {
        # square side, wedge sides: (axis,rotation)
        ("Front", "Bottom"): (0, 0),
        ("Front", "Left"): (0, 1),
        ("Front", "Top"): (0, 2),
        ("Front", "Right"): (0, 3),

        ("Back", "Bottom"): (1, 0),
        ("Back", "Left"): (1, 1),
        ("Back", "Top"): (1, 2),
        ("Back", "Right"): (1, 3),

        ("Bottom", "Back"): (2, 0),
        ("Bottom", "Left"): (2, 1),
        ("Bottom", "Front"): (2, 2),
        ("Bottom", "Right"): (2, 3),

        ("Top", "Back"): (3, 0),
        ("Top", "Left"): (3, 1),
        ("Top", "Front"): (3, 2),
        ("Top", "Right"): (3, 3),

        ("Right", "Front"): (4, 0),
        ("Right", "Top"): (4, 1),
        ("Right", "Back"): (4, 2),
        ("Right", "Bottom"): (4, 3),

        ("Left", "Front"): (5, 0),
        ("Left", "Top"): (5, 1),
        ("Left", "Back"): (5, 2),
        ("Left", "Bottom"): (5, 3)
    }

    def to_string(self):
        """
        @rtype: str
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        tuple_str = ", ".join(self._orientation_to_tuple_str[(axis_rotation, rotations)])
        return "Faces: {}, pointing: {}".format(tuple_str[0], tuple_str[1])
