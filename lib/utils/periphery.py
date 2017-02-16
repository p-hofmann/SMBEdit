from lib.utils.blocklist import BlockList
from lib.utils.blockconfig import block_config
from lib.utils.peripheryhardcoded import PeripheryHardcoded

__author__ = 'Peter Hofmann'


class PeripheryBase(object):
    """

    @type _block_list: BlockList
    """
    def __init__(self, block_list):
        """

        @type block_list: BlockList
        """
        self._block_list = block_list

    def __del__(self):
        del self._block_list
        self._block_list = None

    _shape_id_wedge = block_config.get_shape_id("wedge")
    _shape_id_tetra = block_config.get_shape_id("tetra")
    _shape_id_corner = block_config.get_shape_id("corner")
    _shape_id_hepta = block_config.get_shape_id("hepta")

    def get_orientation_simple(self, position, shape_wedge=False, shape_tetra=False):
        """

        @type position: (int, int, int)
        @type shape_wedge: bool
        @type shape_tetra: bool

        @return: (shape id, (axis rotation, rotations)) | None
        @rtype: (int (int, int)) | None
        """
        pass

    def get_orientation_complex(self, position, shape_id):
        """

        @type position: (int, int, int)
        @type shape_id: int
        @return: (axis rotation, rotations) | None
        @rtype: (int, int) | None
        """
        pass

    def get_position_block_periphery_index(self, position, periphery_range=1):
        """
        Some positions in a 3x3x3 periphery, represented by a bit each.

        @type position: (int, int, int)
        @rtype: int
        """
        assert 1 <= periphery_range <= 3
        periphery_index = 0
        power = 1
        range_p = [-1, 0, 1]
        for x in range_p:
            for y in range_p:
                for z in range_p:
                    if abs(x) + abs(y) + abs(z) > periphery_range:
                        continue
                    position_tmp = (position[0] + x, position[1] + y, position[2] + z)
                    if position_tmp == position:
                        continue
                    if self._block_list.has_block_at(position_tmp):
                        periphery_index |= power
                    power <<= 1
        return periphery_index


class PeripherySimple(PeripheryBase, PeripheryHardcoded):
    """

    # @type peripheries: dict[int, dict[int, list[int]] | dict[int, dict[tuple[any], list[int]]]]
    """

    def get_position_shape_periphery(self, position, periphery_range):
        """
        Return a 3x3x3 periphery description

        Shapes:
            "cube": 0,
            "Wedge": 1,
            "Corner": 2,
            "Tetra": 3,
            "Hepta": 4,
            "1/4": 5,
            "1/2": 6,
            "3/4": 7,

        @type position: (int, int, int)
        @type periphery_range: int

        @rtype: tuple[int]
        """
        assert 1 <= periphery_range <= 3
        angle_shapes = {block_config.get_shape_id("wedge"), block_config.get_shape_id("tetra")}  # 5, 7,
        shape_periphery = []
        range_p = [-1, 0, 1]
        for x in range_p:
            for y in range_p:
                for z in range_p:
                    if abs(x) + abs(y) + abs(z) > periphery_range:
                        continue
                    position_tmp = (position[0] + x, position[1] + y, position[2] + z)
                    if position_tmp == position:
                        continue
                    if self._block_list.has_block_at(position_tmp):
                        block_tmp = self._block_list[position_tmp]
                        block_id = block_tmp.get_id()
                        is_angled_shape = False
                        if block_config[block_id].shape in angle_shapes:
                            is_angled_shape = True
                        shape_periphery.append(is_angled_shape)
        return tuple(shape_periphery)

    def get_orientation_simple(self, position, shape_wedge=False, shape_tetra=False):
        """

        @type position: (int, int, int)
        @type shape_wedge: bool
        @type shape_tetra: bool

        @return: (shape id, (axis rotation, rotations)) | None
        @rtype: (int (int, int)) | None
        """
        periphery_index = self.get_position_block_periphery_index(position, 1)
        if shape_wedge and periphery_index in self.peripheries_simple[self._shape_id_wedge]:
            # "wedge"
            new_shape_id = self._shape_id_wedge
        elif shape_tetra and periphery_index in self.peripheries_simple[self._shape_id_tetra]:
            # tetra
            new_shape_id = self._shape_id_tetra
        else:
            return None
        return new_shape_id, self.peripheries_simple[new_shape_id][periphery_index]

    def get_orientation_complex(self, position, shape_id):
        """

        @type position: (int, int, int)
        @type shape_id: int
        @return: (axis rotation, rotations) | None
        @rtype: (int, int) | None
        """
        periphery_index = self.get_position_block_periphery_index(position, 1)
        if periphery_index not in self.peripheries_simple[shape_id]:
            return None
        periphery_shape = self.get_position_shape_periphery(position, 1)
        if periphery_shape not in self.peripheries_simple[shape_id][periphery_index]:
            return None
        return self.peripheries_simple[shape_id][periphery_index][periphery_shape]


# ##################
# Periphery using Annotate
# ##################


class Periphery(PeripheryBase, PeripheryHardcoded):
    """
    Collection of auto shape stuff

    @type _marked: set[str]
    @type _border: set[str]
    """

    def __init__(self, block_list):
        """

        @type block_list: BlockList
        """
        super(Periphery, self).__init__(block_list)
        self._marked = set()
        self._border = set()

    def set_annotation(self, marked, border):
        """

        @type marked: set[str]
        @type border: set[str]
        """
        self._marked = marked
        self._border = border

    def get_position_periphery_index(self, position, periphery_range=1):
        """
        Some positions in a 3x3x3 periphery, represented by a bit each.

        @type position: (int, int, int)
        @rtype: int
        """
        assert 1 <= periphery_range <= 3
        periphery_index = 0
        power = 1
        range_p = [-1, 0, 1]
        for x in range_p:
            for y in range_p:
                for z in range_p:
                    if abs(x) + abs(y) + abs(z) > periphery_range:
                        continue
                    position_tmp = (position[0] + x, position[1] + y, position[2] + z)
                    if position_tmp == position:
                        continue
                    if self._block_list.get_index(position_tmp) in self._marked:
                        periphery_index |= power
                    # if not marked and self._block_list.get_index(position_tmp) not in self._marked:
                    #     periphery_index |= power
                    power <<= 1
        return periphery_index

    def get_position_shape_periphery(self, position, periphery_range):
        """
        Return a 3x3x3 periphery description

        Shapes:
            "cube": 0,
            "Wedge": 1,
            "Corner": 2,
            "Tetra": 3,
            "Hepta": 4,
            "1/4": 5,
            "1/2": 6,
            "3/4": 7,

        @type position: (int, int, int)
        @type periphery_range: int

        @rtype: tuple[int], tuple[tuple[int] | None]
        """
        assert 1 <= periphery_range <= 3
        angle_shapes = {self._shape_id_wedge, self._shape_id_corner, self._shape_id_tetra, self._shape_id_hepta}
        periphery_orientation = []
        periphery_shape = []
        range_p = [-1, 0, 1]
        for x in range_p:
            for y in range_p:
                for z in range_p:
                    if abs(x) + abs(y) + abs(z) > periphery_range:
                        continue
                    position_tmp = (position[0] + x, position[1] + y, position[2] + z)
                    if position_tmp == position:
                        continue
                    if not self._block_list.has_block_at(position_tmp):
                        shape_orientation = 0
                        orientation = None
                    else:
                        block_tmp = self._block_list[position_tmp]
                        block_id = block_tmp.get_id()
                        shape_orientation = 0
                        orientation = None
                        if block_config[block_id].shape in angle_shapes:
                            shape_orientation = block_config[block_id].shape
                            orientation = block_tmp.get_axis_rotation(), block_tmp.get_rotations()
                    periphery_shape.append(shape_orientation)
                    periphery_orientation.append(orientation)
        return tuple(periphery_shape), tuple(periphery_orientation)

    def get_periphery_simple(self, shape_id):
        """
        Shapes:
            "Wedge": 1,
            "Tetra": 3,
        """
        periphery = {}
        for position_index in self._border:
            block = self._block_list[position_index]
            if block_config[block.get_id()].shape != shape_id:
                continue
            position = self._block_list.get_position(position_index)
            periphery_index = self.get_position_periphery_index(position, 1)
            rotations = block.get_rotations()
            axis_rotation = block.get_axis_rotation()
            periphery[periphery_index] = [axis_rotation, rotations]
        return periphery

    def get_periphery_complex(self, shape_id):
        """
        Called in test

        Shapes:
            "Corner": 2,
            "Hepta": 4,
        """
        for position_index in self._border:
            block = self._block_list[position_index]
            if block_config[block.get_id()].shape != shape_id:
                continue
            position = self._block_list.get_position(position_index)
            periphery_index = self.get_position_periphery_index(position, 1)
            periphery_shape, periphery_orientation = self.get_position_shape_periphery(position, 1)
            rotations = block.get_rotations()
            axis_rotation = block.get_axis_rotation()
            yield periphery_index, periphery_shape, periphery_orientation, (axis_rotation, rotations)

    def get_orientation_simple(self, position, shape_wedge=False, shape_tetra=False):
        """

        @type position: (int, int, int)
        @type shape_wedge: bool
        @type shape_tetra: bool

        @return: (shape id, (axis rotation, rotations)) | None
        @rtype: (int (int, int)) | None
        """
        periphery_index = self.get_position_periphery_index(position, 1)
        if shape_wedge and periphery_index in self.peripheries[self._shape_id_wedge]:
            # "wedge"
            new_shape_id = self._shape_id_wedge
        elif shape_tetra and periphery_index in self.peripheries[self._shape_id_tetra]:
            # tetra
            new_shape_id = self._shape_id_tetra
        else:
            return None
        return new_shape_id, self.peripheries[new_shape_id][periphery_index]

    def get_orientation_complex(self, position, shape_id):
        """

        @type position: (int, int, int)
        @type shape_id: int
        @return: (axis rotation, rotations) | None
        @rtype: (int, int) | None
        """
        periphery_index = self.get_position_periphery_index(position, 1)
        if periphery_index not in self.peripheries[shape_id]:
            return None
        periphery_shape, periphery_orientation = self.get_position_shape_periphery(position, 1)
        if periphery_shape not in self.peripheries[shape_id][periphery_index]:
            return None
        if periphery_orientation not in self.peripheries[shape_id][periphery_index][periphery_shape]:
            return None
        return self.peripheries[shape_id][periphery_index][periphery_shape][periphery_orientation]
