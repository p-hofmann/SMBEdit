from lib.smblueprint.smdblock.style.style4tetra import Style4Tetra


__author__ = 'Peter Hofmann'


class Style5Hepta(Style4Tetra):
    """
    Type            Bits                    Description
    Type 5          19     23     22        The axis of rotation.
                                            000 : +Y
                                            001 : -Y
                    21     20               An amount of rotation around the axis of rotation,
                                            in 90-degree step

    """
    # https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

    def to_string(self):
        """
        @rtype: str
        """
        axis_rotation = self.get_axis_rotation()
        rotations = self.get_rotations()
        tuple_str = ", ".join(self._orientation_to_tuple_str[(axis_rotation, rotations)])
        squares = ", ".join(tuple_str)
        return "Square sides: {}".format(squares)
