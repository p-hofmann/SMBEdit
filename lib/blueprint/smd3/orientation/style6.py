from lib.blueprint.smd3.orientation.style2corner import Style2Corner


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
        # (19,23,22,rot): icon faces, icon pointing towards
        (0, 0, 0, 0): ("Front", "Bottom"),
        (0, 0, 0, 1): ("Front", "Left"),
        (0, 0, 0, 2): ("Front", "Top"),
        (0, 0, 0, 3): ("Front", "Right"),

        (0, 0, 1, 0): ("Back", "Bottom"),
        (0, 0, 1, 1): ("Back", "Left"),
        (0, 0, 1, 2): ("Back", "Top"),
        (0, 0, 1, 3): ("Back", "Right"),

        (0, 1, 0, 0): ("Bottom", "Back"),
        (0, 1, 0, 1): ("Bottom", "Left"),
        (0, 1, 0, 2): ("Bottom", "Front"),
        (0, 1, 0, 3): ("Bottom", "Right"),

        (0, 1, 1, 0): ("Top", "Back"),
        (0, 1, 1, 1): ("Top", "Left"),
        (0, 1, 1, 2): ("Top", "Front"),
        (0, 1, 1, 3): ("Top", "Right"),

        (1, 0, 0, 0): ("Right", "Front"),
        (1, 0, 0, 1): ("Right", "Top"),
        (1, 0, 0, 2): ("Right", "Back"),
        (1, 0, 0, 3): ("Right", "Bottom"),

        (1, 0, 1, 0): ("Left", "Front"),
        (1, 0, 1, 1): ("Left", "Top"),
        (1, 0, 1, 2): ("Left", "Back"),
        (1, 0, 1, 3): ("Left", "Bottom")
    }

    _tuple_str_to_orientation = {
        # square side, wedge sides: (19,23,22,rot)
        ("Front", "Bottom"): (0, 0, 0, 0),
        ("Front", "Left"): (0, 0, 0, 1),
        ("Front", "Top"): (0, 0, 0, 2),
        ("Front", "Right"): (0, 0, 0, 3),

        ("Back", "Bottom"): (0, 0, 1, 0),
        ("Back", "Left"): (0, 0, 1, 1),
        ("Back", "Top"): (0, 0, 1, 2),
        ("Back", "Right"): (0, 0, 1, 3),

        ("Bottom", "Back"): (0, 1, 0, 0),
        ("Bottom", "Left"): (0, 1, 0, 1),
        ("Bottom", "Front"): (0, 1, 0, 2),
        ("Bottom", "Right"): (0, 1, 0, 3),

        ("Top", "Back"): (0, 1, 1, 0),
        ("Top", "Left"): (0, 1, 1, 1),
        ("Top", "Front"): (0, 1, 1, 2),
        ("Top", "Right"): (0, 1, 1, 3),

        ("Right", "Front"): (1, 0, 0, 0),
        ("Right", "Top"): (1, 0, 0, 1),
        ("Right", "Back"): (1, 0, 0, 2),
        ("Right", "Bottom"): (1, 0, 0, 3),

        ("Left", "Front"): (1, 0, 1, 0),
        ("Left", "Top"): (1, 0, 1, 1),
        ("Left", "Back"): (1, 0, 1, 2),
        ("Left", "Bottom"): (1, 0, 1, 3)
    }

    def to_string(self):
        """
        @rtype: str
        """
        orientation = self.get_orientation()
        tuple_str = self._orientation_to_tuple_str[orientation]
        return "Faces: {}, pointing: {}".format(tuple_str[0], tuple_str[1])
