__author__ = 'Peter Hofmann'


from lib.bits_and_bytes import BitAndBytes
from lib.utils.blockconfig import block_config
# from lib.smblueprint.smdblock.blockpool import block_pool


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

    def __init__(self, int_24, version):
        self._int_24 = int_24
        self._version = version

    def get_int_24(self):
        """
        Returns the block integer

        @rtype: int
        """
        return self._int_24

    def get_id(self):
        """
        Returns the block id

        @rtype: int
        """
        return BitAndBytes.bits_parse(self._int_24, 0, 11)

    def get_hit_points(self):
        """
        Returns the hit points of the block

        @rtype: int
        """
        if self._version < 2:
            return BitAndBytes.bits_parse(self._int_24, 11, 9)
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24, 11, 8)
        # version 3
        return BitAndBytes.bits_parse(self._int_24, 11, 7)

    def is_active(self):
        """
        Returns the 'active' status.

        @rtype: bool
        """
        block_id = self.get_id()
        if not block_config[block_id].can_activate:
            return False
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24, 19, 1) == 0
        # version 3
        return BitAndBytes.bits_parse(self._int_24, 18, 1) == 0

    def get_axis_rotation(self):
        if self._version < 3:
            block_id = self.get_id()
            bit_22_23 = BitAndBytes.bits_parse(self._int_24, 22, 2)
            if block_config[block_id].block_style in {2, 6}:
                return bit_22_23 | (BitAndBytes.bits_parse(self._int_24, 19, 1) << 2)
            return bit_22_23
        # version 3
        return BitAndBytes.bits_parse(self._int_24, 21, 3)

    def get_rotations(self):
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24, 20, 2)
        # version 3
        return BitAndBytes.bits_parse(self._int_24, 19, 2)

    def get_block_side_id(self):
        if self._version < 3:
            return BitAndBytes.bits_parse(self._int_24, 20, 3)
        # version 3
        return BitAndBytes.bits_parse(self._int_24, 19, 3)

    # #######################################
    # ###  Edit integer Bits
    # #######################################

    def _get_active_bit(self, active=None, block_id=None):
        """
        In the rare case a block value is changed, they are turned into a byte string.

        @type active: bool | None

        @rtype: Block
        """
        if block_id is None:
            block_id = self.get_id()
        if active:
            return 0
        elif active is False:
            return 1
        else:
            if block_config[block_id].can_activate and not self.is_active():
                return 1
        return 0

    def modify_block(self, block_id=None, hit_points=None, active=None):
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
            self._int_24 = 0
            return
        elif hit_points is None:
            hit_points = block_config[block_id].hit_points

        if hit_points is None:
            hit_points = self.get_hit_points()

        active_bit = self._get_active_bit(active=active, block_id=block_id)

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

    def modify_orientation(self, new_int_24bit, rotations=None, axis_rotation=None, **kwargs):
        """
        Set orientation bits of an integer

        @type new_int_24bit: int
        @type axis_rotation: int
        @type rotations: int

        @rtype: int
        """
        if axis_rotation is None:
            axis_rotation = self.get_axis_rotation()
        if rotations is None:
            rotations = self.get_rotations()
        if self._version < 3:
            new_int_24bit &= 0b000000111111111111111111
            if axis_rotation > 3:
                axis_rotation -= 4
                new_int_24bit = BitAndBytes.bits_combine(1, new_int_24bit, 19)
            new_int_24bit = BitAndBytes.bits_combine(rotations, new_int_24bit, 20)
            new_int_24bit = BitAndBytes.bits_combine(axis_rotation, new_int_24bit, 22)
        else:
            new_int_24bit &= 0b000001111111111111111111
            new_int_24bit = BitAndBytes.bits_combine(rotations, new_int_24bit, 19)
            new_int_24bit = BitAndBytes.bits_combine(axis_rotation, new_int_24bit, 21)
        return new_int_24bit

    def get_modified_int_24bit(self, block_id=None, hit_points=None, active=None,
                               block_side_id=None, rotations=None, axis_rotation=None):
        """
        In the rare case a block value is changed, they are turned into a byte string.

        @rtype: int
        """
        int_24bit = self.modify_block(block_id=block_id, hit_points=hit_points, active=active)
        return self.modify_orientation(
            int_24bit, block_side_id=block_side_id, rotations=rotations, axis_rotation=axis_rotation)

    def get_modified_block(self, block_id=None, hit_points=None, active=None,
                               block_side_id=None, rotations=None, axis_rotation=None):
        """
        In the rare case a block value is changed, they are turned into a byte string.

        @rtype: lib.smblueprint.smdblock.style.stylebasic.StyleBasic
        """
        from lib.smblueprint.smdblock.blockpool import block_pool
        return block_pool(self.get_modified_int_24bit(
            block_id=block_id, hit_points=hit_points, active=active,
            block_side_id=block_side_id, rotations=rotations, axis_rotation=axis_rotation))
