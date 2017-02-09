__author__ = 'Peter Hofmann'


from lib.bits_and_bytes import BitAndBytes
from lib.utils.blockconfig import block_config


class BlockBits(object):
    """
    Type        Bits                    Description

    Type0/3     23      22      21      The block facing

    Type 1      23      22              The axis of rotation.
                21      20              An amount rotation around the axis of rotation, in 90-degree steps

    Type 4/5    19      23     22       The axis of rotation.
                21      20              An amount rotation around the axis of rotation, in 90-degree steps

    Type 2/6    19      23     22       The axis of rotation.
                21      20              An amount rotation around the axis of rotation, in 90-degree steps
    """

    def __init__(self, int_24bit, version):
        self._int_24bit = int_24bit
        self._version = version

    def get_id(self):
        """
        Returns the block id

        @rtype: int
        """
        return BitAndBytes.bits_parse(self._int_24bit, 0, 11)

    def get_hit_points(self):
        """
        Returns the hit points of the block

        @rtype: int
        """
        if self._version < 2:
            return BitAndBytes.bits_parse(self._int_24bit, 11, 9)
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24bit, 11, 8)
        # version 3
        return BitAndBytes.bits_parse(self._int_24bit, 11, 7)

    def is_active(self):
        """
        Returns the 'active' status.

        @rtype: bool
        """
        block_id = self.get_id()
        if not block_config[block_id].can_activate:
            return False
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24bit, 19, 1) == 0
        # version 3
        return BitAndBytes.bits_parse(self._int_24bit, 18, 1) == 0

    def get_axis_rotations(self):
        if self._version < 3:
            block_id = self.get_id()
            bit_22_23 = BitAndBytes.bits_parse(self._int_24bit, 22, 2)
            if block_config[block_id].block_style in {2, 6}:
                return bit_22_23 | (BitAndBytes.bits_parse(self._int_24bit, 19, 1) << 2)
            return bit_22_23
        # version 3
        return BitAndBytes.bits_parse(self._int_24bit, 21, 3)

    def get_rotations(self):
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24bit, 20, 2)
        # version 3
        return BitAndBytes.bits_parse(self._int_24bit, 19, 2)

    def get_block_side_id(self):
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24bit, 20, 3)
        # version 3
        return BitAndBytes.bits_parse(self._int_24bit, 19, 3)

    # #######################################
    # ###  Edit integer Bits
    # #######################################

    def modify_block(self, block_id=None, hit_points=None, active=None, **kwargs):
        """
        In the rare case a block value is changed, they are turned into a byte string.

        @type block_id: int | None
        @type hit_points: int | None
        @type active: bool | None

        @rtype: Block
        """
        if block_id is None:
            block_id = self.get_id()
        elif block_id == 0:
            self._int_24bit = 0
            return
        elif hit_points is None:
            hit_points = block_config[block_id].hit_points

        if hit_points is None:
            hit_points = self.get_hit_points()

        active_bit = 0
        if active:
            active_bit = 0
        elif not active:
            active_bit = 1
        else:
            if block_config[block_id].can_activate and not self.is_active():
                active_bit = 1

        int_24bit = 0
        int_24bit = BitAndBytes.bits_combine(block_id, int_24bit, 0)
        int_24bit = BitAndBytes.bits_combine(hit_points, int_24bit, 11)
        if block_config[block_id].can_activate:  # For blocks with an activation status
            if self._version < 3:
                int_24bit = BitAndBytes.bits_combine(active_bit, int_24bit, 19)
            else:
                # version 3
                int_24bit = BitAndBytes.bits_combine(active_bit, int_24bit, 18)
        return int_24bit

    def modify_orientation(self, new_int_24bit, **kwargs):
        pass

    def get_modified_int_24bit(self, **kwargs):
        """
        In the rare case a block value is changed, they are turned into a byte string.

        @rtype: int
        """
        int_24bit = self.modify_block(**kwargs)
        self.modify_orientation(int_24bit, **kwargs)

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
        # (axis_rotation, rotations) (19, 23, 22, rotations)
        0: (0, 2),  # (0, 0, 0, 2),  # FRONT up
        1: (1, 0),  # (0, 0, 1, 0),  # BACK down/up?
        2: (3, 2),  # (0, 1, 1, 2),  # TOP forward
        3: (2, 2),  # (0, 1, 0, 2),  # BOTTOM forward
        4: (4, 0),  # (1, 0, 0, 0),  # RIGHT forward
        5: (5, 0),  # (1, 0, 1, 0),  # LEFT forward
    }

    @staticmethod
    def side_id_to_axis_rotation(side_id):
        """
        Return style 6 bits representing side id

        @rtype: tuple[int]
        """
        return BlockBits._block_side_id_to_type_6[side_id]
