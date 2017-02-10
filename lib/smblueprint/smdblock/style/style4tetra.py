from lib.smblueprint.smdblock.style.stylebasic import StyleBasic


__author__ = 'Peter Hofmann'


class Style4Tetra(StyleBasic):
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
        # (axis_rotation,rot): slope sides
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
        # (axis_rotation,rot): slope sides
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
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        tuple_str = ", ".join(self._orientation_to_tuple_str[(axis_rotation, rotations)])
        slopes = ", ".join(tuple_str)
        return "Sloped sides: {}".format(slopes)

    # #######################################
    # ###  Mirror
    # #######################################

    def _mirror_x(self):
        """
        Mirror Left - Right
        """
        rotations = self.get_rotations()
        axis_rotation = self.get_axis_rotation()
        tuple_str = self._orientation_to_tuple_str[(axis_rotation, rotations)]
        replacements = {"Left": "Right", "Right": "Left"}
        tuple_str = self._replace_string(tuple_str, replacements)
        axis_rotation, rotations = self._tuple_str_to_orientation[tuple_str]
        return self.modify_orientation(
            self._int_24bit, axis_rotation=axis_rotation, rotations=rotations)

    def _mirror_y(self):
        """
        Mirror Top - Bottom
        """
        rotations = self.get_rotations()
        axis_rotation = self.get_axis_rotation()
        axis_rotation = (axis_rotation + 1) % 2
        return self.modify_orientation(
            self._int_24bit, axis_rotation=axis_rotation, rotations=rotations)

    # front - back
    def _mirror_z(self):
        """
        Mirror Front - Back
        """
        rotations = self.get_rotations()
        axis_rotation = self.get_axis_rotation()
        tuple_str = self._orientation_to_tuple_str[(axis_rotation, rotations)]
        replacements = {"Front": "Back", "Back": "Front"}
        tuple_str = self._replace_string(tuple_str, replacements)
        bit_22, rotations = self._tuple_str_to_orientation[tuple_str]
        return self.modify_orientation(
            self._int_24bit, axis_rotation=axis_rotation, rotations=rotations)
