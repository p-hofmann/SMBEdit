from lib.smblueprint.smdblock.style.stylebasic import StyleBasic


__author__ = 'Peter Hofmann'


class Style1Wedge(StyleBasic):
    """
    Type        Bits                Description
    Type 1      23     22           The axis of rotation.
                                    00 : +Y
                                    01 : -Y
                                    10 : -Z
                21     20           The amount of clockwise rotation around the axis of rotation, in 90-degree steps

    @type _orientation_to_str: dict[tuple[int], str]
    """
    # https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

    _orientation_to_str = {
        # (axis_rotation,rot): square sides
        (0, 0): "Bottom, Front",
        (0, 1): "Bottom, Left",
        (0, 2): "Bottom, Back",
        (0, 3): "Bottom, Right",

        (1, 0): "Top, Front",
        (1, 1): "Top, Right",
        (1, 2): "Top, Back",
        (1, 3): "Top, Left",

        (2, 0): "Right, Front",
        (2, 1): "Right, Back",
        (2, 2): "Left, Front",
        (2, 3): "Left, Back",
    }

    def to_string(self):
        """
        @rtype: str
        """
        rotations = self.get_rotations()
        axis_rotation = self.get_axis_rotation()
        return "Square sides: {}".format(self._orientation_to_str[(axis_rotation, rotations)])

    # #######################################
    # ###  Mirror
    # #######################################

    def _mirror_x(self):
        """
        Mirror left - right
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        if axis_rotation < 2 and rotations % 2 == 0:
            # no change
            return self._int_24
        rotations = (rotations + 2) % 4
        return self.modify_orientation(self._int_24, rotations=rotations)

    def _mirror_y(self):
        """
        Mirror Top - Bottom
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        if axis_rotation == 2:
            # no change
            return self._int_24
        axis_rotation = (axis_rotation + 1) % 2
        if rotations % 2 == 1:
            rotations = (rotations + 2) % 4
        return self.modify_orientation(self._int_24, axis_rotation=axis_rotation, rotations=rotations)

    # front - back
    def _mirror_z(self):
        """
        Mirror front - back
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        if axis_rotation < 2:
            if rotations % 2 == 1:
                # no change
                return self._int_24
            rotations = (rotations + 2) % 4
        else:
            if rotations % 2 == 0:
                rotations += 1
            else:
                rotations -= 1
        return self.modify_orientation(self._int_24, rotations=rotations)
