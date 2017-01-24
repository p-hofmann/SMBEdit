__author__ = 'Peter Hofmann'

import sys

from lib.bits_and_bytes import BitAndBytes


class Orientation(object):
    """
    Type        Bits                    Description

    Type0/3     23      22      21      The block facing

    Type 1      23      22              The axis of rotation.
                                        00 : +Y
                                        01 : -Y
                                        10 : -Z
                                        11 : +Z
                21      20              An amount rotation around the axis of rotation, in 90-degree steps

    Type 4/5    19      23     22       The axis of rotation.
                                            000 : +Y
                                            001 : -Y
                21      20              An amount rotation around the axis of rotation, in 90-degree steps

    Type 2/6    19      23     22       The axis of rotation.
                                        000 : +Y
                                        001 : -Y
                                        010 : -Z
                                        011 : +Z
                                        100 : -X
                                        101 : +X
                21      20              An amount rotation around the axis of rotation, in 90-degree steps
    """

    _bit_rotation_start = 20
    _bit_rotation_length = 2

    _bit_block_side_start = 20
    _bit_block_side_length = 3

    def __init__(self, int_24bit):
        """
        Constructor

        # Block styles:
        # 0: slabs/doors/weapons/station/logic/lighting/medical/factions/systems/effects/tools:
        # 1: Wedge
        # 2: Corner
        # 3: Rod/Paint/Capsules/Hardener/Plants/Shards
        # 4: Tetra
        # 5: Hepta
        # 6: Rail/Pickup/White Light Bar/Pipe/Decorative Console/Shipyard Module/Core Anchor/Mushroom/

        @type int_24bit: int
        """
        self._label = "Orientation"
        # super(BlockOrientation, self).__init__(logfile=logfile, verbose=verbose, debug=debug)
        self._int_24bit = int_24bit

    # #######################################
    # get
    # #######################################

    def get_orientation(self):
        """
        @rtype: tuple[int]
        """
        return self._get_bit_19(), self._get_bit_23(), self._get_bit_22(), self._get_rotations()

    def _get_bit_19(self):
        return BitAndBytes.bits_parse(self._int_24bit, 19, 1)

    def _get_bit_22(self):
        return BitAndBytes.bits_parse(self._int_24bit, 22, 1)

    def _get_bit_23(self):
        return BitAndBytes.bits_parse(self._int_24bit, 23, 1)

    def _get_rotations(self):
        return BitAndBytes.bits_parse(self._int_24bit, Orientation._bit_rotation_start, Orientation._bit_rotation_length)

    def get_block_side_id(self):
        return BitAndBytes.bits_parse(self._int_24bit, Orientation._bit_block_side_start, Orientation._bit_block_side_length)

    # #######################################
    # ###  Turning - Experimental
    # #######################################

    #   -Y          Z          Z
    # -X   X     -Y   Y     -X   X
    #    Y         -Z         -Z

    @staticmethod
    def _replace_string(tuple_str, replacements):
        """
        @type tuple_str: tuple[str]
        @type replacements: dict[str, str]
        """
        tmp_list = list(tuple_str)
        for index, word in enumerate(tuple_str):
            if word in replacements:
                tmp_list[index] = replacements[word]
                return tuple(tmp_list)
        return tuple(tmp_list)

    _block_side_id_to_type_6 = {
        # (19, 23, 22, rotations)
        0: (0, 0, 0, 2),  # FRONT up
        1: (0, 0, 1, 0),  # BACK down/up?
        2: (0, 1, 1, 2),  # TOP forward
        3: (0, 1, 0, 2),  # BOTTOM forward
        4: (1, 0, 0, 0),  # RIGHT forward
        5: (1, 0, 1, 0),  # LEFT forward
    }

    def _orientation_to_stream(self, output_stream=sys.stdout):
        """

        @param output_stream:
        @type output_stream: file
        """
        output_stream.write(self._bit_orientation_to_string())

    def _bit_orientation_to_string(self):
        """
        Return orientation data as string

        @rtype: str
        """
        return_string = ""
        # return_string += "{}\t".format(self._orientation)
        return_string += "({},{},{}) ".format(self._get_bit_19(), self._get_bit_23(), self._get_bit_22())
        rotation = "{}*".format(self._get_rotations() * 90)
        return_string += rotation.rjust(4) + "\t"
        return_string += "F {}".format(self.get_block_side_id())
        return return_string
