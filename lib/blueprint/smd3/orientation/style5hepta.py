from lib.blueprint.smd3.orientation.style4tetra import Style4Tetra


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
        orientation = self.get_orientation()
        tuple_str = self._orientation_to_tuple_str[orientation]
        squares = ", ".join(tuple_str)
        return "Square sides: {}".format(squares)
