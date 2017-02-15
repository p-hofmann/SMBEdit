from lib.utils.blocklist import BlockList
from lib.utils.blockconfig import block_config


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
        list = self._block_list
        self._block_list = None
        del list

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


class PeripherySimple(PeripheryBase):
    """

    # @type peripheries: dict[int, dict[int, list[int]] | dict[int, dict[tuple[any], list[int]]]]
    """

    # shapes = ["cube", "wedge", "corner", "tetra", "hepta"]
    # "cube": 0,
    # "Wedge": 1,
    # "Corner": 2,
    # "Tetra": 3,
    # "Hepta": 4,
    peripheries = dict()

    # wedge
    peripheries[1] = {
        # [axis rotation, rotations]
        43: [0, 0],
        46: [0, 1],
        39: [0, 2],
        15: [0, 3],
        57: [1, 0],
        29: [1, 1],
        53: [1, 2],
        60: [1, 3],
        27: [2, 0],
        23: [2, 1],
        58: [2, 2],
        54: [2, 3],
    }

    # corner
    peripheries[2] = {
        # (): [bit_19, bit_22, bit_23, rotations]
        38: {
            (True, True, False): (5, 0),
            (True, False, True): (2, 2),
            (False, True, True): (0, 2),
        },
        7: {
            (False, True, True): (4, 0),
            (True, False, True): (0, 1),
            (True, True, False): (2, 3),
        },
        42: {
            (False, True, True): (0, 3),
            (True, True, False): (5, 3),
            (True, False, True): (3, 3),
        },
        11: {
            (False, True, True): (4, 3),
            (True, True, False): (3, 0),
            (True, False, True): (0, 0),
        },
        52: {
            (False, True, True): (2, 1),
            (True, True, False): (5, 1),
            (True, False, True): (1, 2),
        },
        21: {
            (False, True, True): (4, 1),
            (True, False, True): (2, 0),
            (True, True, False): (1, 1),
        },
        56: {
            (False, True, True): (3, 2),
            (True, False, True): (1, 3),
            (True, True, False): (5, 2),
        },
        25: {
            (False, True, True): (4, 2),
            (True, True, False): (1, 0),
            (True, False, True): (3, 1),
        },
    }

    # tetra
    peripheries[3] = {
        # [axis rotation, rotations]
        11: [0, 0],
        7: [0, 1],
        38: [0, 2],
        42: [0, 3],
        25: [1, 0],
        21: [1, 1],
        52: [1, 2],
        56: [1, 3],
        }

    # hepta
    peripheries[4] = {
        59: {
            (True, False, False, True, False): (0, 3),
            (True, True, False, False, False): (1, 3),
            (False, True, False, False, True): (1, 0),
            (False, False, False, True, True): (0, 0),
        },
        47: {
            (True, False, True, False, False): (0, 3),
            (True, False, False, True, False): (0, 2),
            (False, False, False, True, True): (0, 1),
            (False, False, True, False, True): (0, 0),
        },
        55: {
            (True, True, False, False, False): (1, 2),
            (True, False, False, True, False): (0, 2),
            (False, True, False, False, True): (1, 1),
            (False, False, False, True, True): (0, 1),
        },
        63: {
            (False, True, True, False, False, True): (1, 0),
            (True, True, True, False, False, False): (1, 3),
            (True, False, True, False, True, False): (0, 3),
            (False, False, False, True, True, True): (0, 1),
            (True, True, False, True, False, False): (1, 2),
            (False, True, False, True, False, True): (1, 1),
            (True, False, False, True, True, False): (0, 2),
            (False, False, True, False, True, True): (0, 0),
        },
        61: {
            (True, False, True, False, False): (1, 2),
            (False, False, True, False, True): (1, 1),
            (True, True, False, False, False): (1, 3),
            (False, True, False, False, True): (1, 0),
        },
        62: {
            (False, True, False, True, False): (0, 3),
            (False, False, True, True, False): (0, 2),
            (True, False, True, False, False): (1, 2),
            (True, True, False, False, False): (1, 3),
        },
        31: {
            (False, True, False, True, False): (1, 1),
            (False, False, True, False, True): (0, 0),
            (False, True, True, False, False): (1, 0),
            (False, False, False, True, True): (0, 1),
        },
    }

    # def get_position_periphery_index_9x9(self, position):
    #     """
    #     Every position in a 3x3x3 periphery is represented by a bit.
    #
    #     @type position: (int, int, int)
    #     @rtype: int
    #     """
    #     periphery_index = 0
    #     power = 1
    #     for x in range(position[0]-1, position[0]+2):
    #         for y in range(position[1]-1, position[1]+2):
    #             for z in range(position[2]-1, position[2]+2):
    #                 position_tmp = (x, y, z)
    #                 if position_tmp == position:
    #                     continue
    #                 if self._block_list.has_block_at(position_tmp):
    #                     periphery_index |= power
    #                 power <<= 1
    #     # print power
    #     return periphery_index

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
        periphery_index = self.get_position_block_periphery_index(position, 1)
        if periphery_index not in self.peripheries[shape_id]:
            return None
        periphery_shape = self.get_position_shape_periphery(position, 1)
        if periphery_shape not in self.peripheries[shape_id][periphery_index]:
            return None
        return self.peripheries[shape_id][periphery_index][periphery_shape]


# ##################
# Periphery using Annotate
# ##################


class Periphery(PeripheryBase):
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

    peripheries = dict()
    # shapes = ["cube", "wedge", "corner", "tetra", "hepta"]
    # "cube": 0,
    # "Wedge": 1,
    # "Corner": 2,
    # "Tetra": 3,
    # "Hepta": 4,

    # wedge
    peripheries[1] = {
        # [axis rotation, rotations]
        20: [0, 0],
        17: [0, 1],
        24: [0, 2],
        48: [0, 3],
        6: [1, 0],
        34: [1, 1],
        10: [1, 2],
        3: [1, 3],
        36: [2, 0],
        40: [2, 1],
        5: [2, 2],
        9: [2, 3],
        }

    # corner
    peripheries[2] = {
        52: {
            (1, 0, 0, 2, 0, 0): {
                ((0, 0), None, None, (0, 1), None, None): [0, 0],
            },
            (2, 2, 0, 2, 0, 0): {
                ((5, 3), (4, 2), None, (4, 0), None, None): [4, 3],
                ((3, 3), (3, 1), None, (2, 3), None, None): [3, 0],
                ((0, 3), (1, 0), None, (0, 1), None, None): [0, 0],
            },
            (2, 0, 0, 1, 0, 0): {
                ((0, 3), None, None, (0, 3), None, None): [0, 0],
            },
            (2, 0, 0, 2, 0, 0): {
                ((0, 3), None, None, (0, 1), None, None): [0, 0],
            },
            (2, 2, 0, 1, 0, 0): {
                ((0, 3), (1, 0), None, (0, 3), None, None): [0, 0],
                ((5, 3), (4, 2), None, (0, 3), None, None): [4, 3],
            },
            (1, 1, 0, 0, 0, 0): {
                ((0, 0), (2, 0), None, None, None, None): [3, 0],
            },
            (1, 2, 0, 0, 0, 0): {
                ((0, 0), (3, 1), None, None, None, None): [3, 0],
            },
            (0, 2, 0, 1, 0, 0): {
                (None, (4, 2), None, (0, 3), None, None): [4, 3],
            },
            (0, 2, 0, 2, 0, 0): {
                (None, (4, 2), None, (4, 0), None, None): [4, 3],
            },
            (2, 1, 0, 2, 0, 0): {
                ((5, 3), (2, 0), None, (4, 0), None, None): [4, 3],
                ((3, 3), (2, 0), None, (2, 3), None, None): [3, 0],
            },
            (1, 0, 0, 1, 0, 0): {
                ((0, 0), None, None, (0, 3), None, None): [0, 0],
            },
            (2, 2, 0, 0, 0, 0): {
                ((3, 3), (3, 1), None, None, None, None): [3, 0],
            },
            (1, 2, 0, 2, 0, 0): {
                ((0, 0), (3, 1), None, (2, 3), None, None): [3, 0],
            },
            (0, 1, 0, 1, 0, 0): {
                (None, (2, 0), None, (0, 3), None, None): [4, 3],
            },
            (0, 1, 0, 2, 0, 0): {
                (None, (2, 0), None, (4, 0), None, None): [4, 3],
            },
            (2, 1, 0, 0, 0, 0): {
                ((3, 3), (2, 0), None, None, None, None): [3, 0],
            },
        },
        21: {
            (0, 2, 0, 1, 0, 2): {
                (None, (5, 2), None, (0, 1), None, (4, 3)): [5, 3],
                (None, (1, 3), None, (0, 1), None, (0, 0)): [0, 3],
            },
            (0, 1, 0, 0, 0, 2): {
                (None, (2, 2), None, None, None, (3, 0)): [3, 3],
            },
            (0, 1, 0, 1, 0, 0): {
                (None, (2, 2), None, (0, 1), None, None): [5, 3],
            },
            (0, 2, 0, 2, 0, 2): {
                (None, (5, 2), None, (5, 0), None, (4, 3)): [5, 3],
                (None, (3, 2), None, (2, 2), None, (3, 0)): [3, 3],
                (None, (1, 3), None, (0, 2), None, (0, 0)): [0, 3],
            },
            (0, 0, 0, 2, 0, 1): {
                (None, None, None, (0, 2), None, (0, 0)): [0, 3],
            },
            (0, 1, 0, 2, 0, 2): {
                (None, (2, 2), None, (5, 0), None, (4, 3)): [5, 3],
                (None, (2, 2), None, (2, 2), None, (3, 0)): [3, 3],
            },
            (0, 0, 0, 1, 0, 2): {
                (None, None, None, (0, 1), None, (0, 0)): [0, 3],
            },
            (0, 2, 0, 0, 0, 2): {
                (None, (3, 2), None, None, None, (3, 0)): [3, 3],
            },
            (0, 2, 0, 2, 0, 1): {
                (None, (3, 2), None, (2, 2), None, (0, 0)): [3, 3],
            },
            (0, 2, 0, 1, 0, 0): {
                (None, (5, 2), None, (0, 1), None, None): [5, 3],
            },
            (0, 2, 0, 2, 0, 0): {
                (None, (5, 2), None, (5, 0), None, None): [5, 3],
            },
            (0, 2, 0, 0, 0, 1): {
                (None, (3, 2), None, None, None, (0, 0)): [3, 3],
            },
            (0, 1, 0, 0, 0, 1): {
                (None, (2, 2), None, None, None, (0, 0)): [3, 3],
            },
            (0, 1, 0, 2, 0, 0): {
                (None, (2, 2), None, (5, 0), None, None): [5, 3],
            },
            (0, 0, 0, 2, 0, 2): {
                (None, None, None, (0, 2), None, (0, 0)): [0, 3],
            },
            (0, 0, 0, 1, 0, 1): {
                (None, None, None, (0, 1), None, (0, 0)): [0, 3],
            },
        },
        38: {
            (1, 0, 0, 2, 0, 0): {
                ((1, 0), None, None, (1, 1), None, None): [1, 0],
            },
            (1, 0, 0, 0, 1, 0): {
                ((1, 0), None, None, None, (2, 0), None): [3, 1],
            },
            (2, 0, 0, 1, 0, 0): {
                ((1, 3), None, None, (1, 1), None, None): [1, 0],
            },
            (2, 0, 0, 2, 0, 0): {
                ((1, 3), None, None, (1, 1), None, None): [1, 0],
            },
            (1, 0, 0, 0, 2, 0): {
                ((1, 0), None, None, None, (3, 0), None): [3, 1],
            },
            (0, 0, 0, 1, 2, 0): {
                (None, None, None, (1, 1), (4, 3), None): [4, 2],
            },
            (2, 0, 0, 2, 1, 0): {
                ((5, 2), None, None, (4, 1), (2, 0), None): [4, 2],
                ((3, 2), None, None, (2, 0), (2, 0), None): [3, 1],
            },
            (1, 0, 0, 1, 0, 0): {
                ((1, 0), None, None, (1, 1), None, None): [1, 0],
            },
            (0, 0, 0, 1, 1, 0): {
                (None, None, None, (1, 1), (2, 0), None): [4, 2],
            },
            (1, 0, 0, 2, 2, 0): {
                ((1, 0), None, None, (2, 0), (3, 0), None): [3, 1],
            },
            (2, 0, 0, 0, 2, 0): {
                ((3, 2), None, None, None, (3, 0), None): [3, 1],
            },
            (2, 0, 0, 1, 2, 0): {
                ((5, 2), None, None, (1, 1), (4, 3), None): [4, 2],
                ((1, 3), None, None, (1, 1), (0, 0), None): [1, 0],
            },
            (2, 0, 0, 2, 2, 0): {
                ((5, 2), None, None, (4, 1), (4, 3), None): [4, 2],
                ((3, 2), None, None, (2, 0), (3, 0), None): [3, 1],
                ((1, 3), None, None, (1, 1), (0, 0), None): [1, 0],
            },
            (2, 0, 0, 0, 1, 0): {
                ((3, 2), None, None, None, (2, 0), None): [3, 1],
            },
            (0, 0, 0, 2, 1, 0): {
                (None, None, None, (4, 1), (2, 0), None): [4, 2],
            },
            (0, 0, 0, 2, 2, 0): {
                (None, None, None, (4, 1), (4, 3), None): [4, 2],
            },
        },
        7: {
            (0, 0, 0, 2, 1, 2): {
                (None, None, None, (5, 1), (2, 2), (4, 2)): [5, 2],
                (None, None, None, (2, 1), (2, 2), (3, 1)): [3, 2],
            },
            (0, 0, 0, 2, 0, 1): {
                (None, None, None, (1, 2), None, (1, 0)): [1, 3],
            },
            (0, 0, 0, 2, 2, 2): {
                (None, None, None, (5, 1), (5, 3), (4, 2)): [5, 2],
                (None, None, None, (2, 1), (3, 3), (3, 1)): [3, 2],
                (None, None, None, (1, 2), (0, 3), (1, 0)): [1, 3],
            },
            (0, 0, 0, 2, 2, 0): {
                (None, None, None, (5, 1), (5, 3), None): [5, 2],
            },
            (0, 0, 0, 1, 0, 2): {
                (None, None, None, (1, 3), None, (1, 0)): [1, 3],
            },
            (0, 0, 0, 1, 0, 1): {
                (None, None, None, (1, 3), None, (1, 0)): [1, 3],
            },
            (0, 0, 0, 1, 1, 0): {
                (None, None, None, (1, 3), (2, 2), None): [5, 2],
            },
            (0, 0, 0, 0, 1, 1): {
                (None, None, None, None, (2, 2), (1, 0)): [3, 2],
            },
            (0, 0, 0, 0, 1, 2): {
                (None, None, None, None, (2, 2), (3, 1)): [3, 2],
            },
            (0, 0, 0, 2, 1, 0): {
                (None, None, None, (5, 1), (2, 2), None): [5, 2],
            },
            (0, 0, 0, 2, 2, 1): {
                (None, None, None, (2, 1), (3, 3), (1, 0)): [3, 2],
            },
            (0, 0, 0, 1, 2, 2): {
                (None, None, None, (1, 3), (0, 3), (1, 0)): [1, 3],
                (None, None, None, (1, 3), (5, 3), (4, 2)): [5, 2],
            },
            (0, 0, 0, 2, 0, 2): {
                (None, None, None, (1, 2), None, (1, 0)): [1, 3],
            },
            (0, 0, 0, 0, 2, 1): {
                (None, None, None, None, (3, 3), (1, 0)): [3, 2],
            },
            (0, 0, 0, 1, 2, 0): {
                (None, None, None, (1, 3), (5, 3), None): [5, 2],
            },
            (0, 0, 0, 0, 2, 2): {
                (None, None, None, None, (3, 3), (3, 1)): [3, 2],
            },
        },
        56: {
            (2, 2, 1, 0, 0, 0): {
                ((0, 2), (1, 1), (0, 3), None, None, None): [0, 1],
                ((5, 0), (4, 1), (0, 3), None, None, None): [4, 0],
            },
            (1, 0, 1, 0, 0, 0): {
                ((0, 2), None, (0, 3), None, None, None): [0, 1],
            },
            (1, 2, 2, 0, 0, 0): {
                ((0, 2), (2, 0), (3, 0), None, None, None): [2, 3],
            },
            (0, 2, 1, 0, 0, 0): {
                (None, (4, 1), (0, 3), None, None, None): [4, 0],
            },
            (0, 1, 1, 0, 0, 0): {
                (None, (2, 1), (0, 3), None, None, None): [4, 0],
            },
            (2, 2, 2, 0, 0, 0): {
                ((5, 0), (4, 1), (4, 3), None, None, None): [4, 0],
                ((2, 2), (2, 0), (3, 0), None, None, None): [2, 3],
                ((0, 2), (1, 1), (0, 0), None, None, None): [0, 1],
            },
            (0, 2, 2, 0, 0, 0): {
                (None, (4, 1), (4, 3), None, None, None): [4, 0],
            },
            (2, 1, 2, 0, 0, 0): {
                ((2, 2), (2, 1), (3, 0), None, None, None): [2, 3],
                ((5, 0), (2, 1), (4, 3), None, None, None): [4, 0],
            },
            (0, 1, 2, 0, 0, 0): {
                (None, (2, 1), (4, 3), None, None, None): [4, 0],
            },
            (1, 2, 0, 0, 0, 0): {
                ((0, 2), (2, 0), None, None, None, None): [2, 3],
            },
            (2, 2, 0, 0, 0, 0): {
                ((2, 2), (2, 0), None, None, None, None): [2, 3],
            },
            (1, 0, 2, 0, 0, 0): {
                ((0, 2), None, (0, 0), None, None, None): [0, 1],
            },
            (2, 0, 1, 0, 0, 0): {
                ((0, 2), None, (0, 3), None, None, None): [0, 1],
            },
            (1, 1, 0, 0, 0, 0): {
                ((0, 2), (2, 1), None, None, None, None): [2, 3],
            },
            (2, 1, 0, 0, 0, 0): {
                ((2, 2), (2, 1), None, None, None, None): [2, 3],
            },
            (2, 0, 2, 0, 0, 0): {
                ((0, 2), None, (0, 0), None, None, None): [0, 1],
            },
        },
        25: {
            (0, 1, 2, 0, 0, 0): {
                (None, (2, 3), (5, 3), None, None, None): [5, 0],
            },
            (0, 2, 2, 0, 0, 0): {
                (None, (5, 1), (5, 3), None, None, None): [5, 0],
            },
            (0, 2, 2, 0, 0, 1): {
                (None, (2, 1), (3, 3), None, None, (0, 2)): [2, 2],
            },
            (0, 2, 1, 0, 0, 0): {
                (None, (5, 1), (0, 1), None, None, None): [5, 0],
            },
            (0, 1, 1, 0, 0, 0): {
                (None, (2, 3), (0, 1), None, None, None): [5, 0],
            },
            (0, 2, 0, 0, 0, 2): {
                (None, (2, 1), None, None, None, (2, 3)): [2, 2],
            },
            (0, 1, 0, 0, 0, 2): {
                (None, (2, 3), None, None, None, (2, 3)): [2, 2],
            },
            (0, 0, 2, 0, 0, 1): {
                (None, None, (0, 3), None, None, (0, 2)): [0, 2],
            },
            (0, 1, 2, 0, 0, 2): {
                (None, (2, 3), (5, 3), None, None, (4, 0)): [5, 0],
                (None, (2, 3), (3, 3), None, None, (2, 3)): [2, 2],
            },
            (0, 0, 1, 0, 0, 1): {
                (None, None, (0, 1), None, None, (0, 2)): [0, 2],
            },
            (0, 2, 1, 0, 0, 2): {
                (None, (1, 2), (0, 1), None, None, (0, 1)): [0, 2],
                (None, (5, 1), (0, 1), None, None, (4, 0)): [5, 0],
            },
            (0, 2, 0, 0, 0, 1): {
                (None, (2, 1), None, None, None, (0, 2)): [2, 2],
            },
            (0, 1, 0, 0, 0, 1): {
                (None, (2, 3), None, None, None, (0, 2)): [2, 2],
            },
            (0, 2, 2, 0, 0, 2): {
                (None, (5, 1), (5, 3), None, None, (4, 0)): [5, 0],
                (None, (1, 2), (0, 3), None, None, (0, 1)): [0, 2],
                (None, (2, 1), (3, 3), None, None, (2, 3)): [2, 2],
            },
            (0, 0, 1, 0, 0, 2): {
                (None, None, (0, 1), None, None, (0, 1)): [0, 2],
            },
            (0, 0, 2, 0, 0, 2): {
                (None, None, (0, 3), None, None, (0, 1)): [0, 2],
            },
        },
        42: {
            (1, 0, 1, 0, 0, 0): {
                ((1, 2), None, (1, 1), None, None, None): [1, 1],
            },
            (2, 0, 0, 0, 1, 0): {
                ((2, 1), None, None, None, (2, 1), None): [2, 0],
            },
            (2, 0, 0, 0, 2, 0): {
                ((2, 1), None, None, None, (2, 3), None): [2, 0],
            },
            (0, 0, 1, 0, 1, 0): {
                (None, None, (1, 1), None, (2, 1), None): [4, 1],
            },
            (2, 0, 2, 0, 1, 0): {
                ((2, 1), None, (3, 1), None, (2, 1), None): [2, 0],
                ((5, 1), None, (4, 2), None, (2, 1), None): [4, 1],
            },
            (0, 0, 2, 0, 2, 0): {
                (None, None, (4, 2), None, (4, 0), None): [4, 1],
            },
            (2, 0, 1, 0, 2, 0): {
                ((5, 1), None, (1, 1), None, (4, 0), None): [4, 1],
                ((1, 2), None, (1, 1), None, (0, 1), None): [1, 1],
            },
            (1, 0, 2, 0, 2, 0): {
                ((1, 2), None, (3, 1), None, (2, 3), None): [2, 0],
            },
            (2, 0, 2, 0, 2, 0): {
                ((2, 1), None, (3, 1), None, (2, 3), None): [2, 0],
                ((1, 2), None, (1, 0), None, (0, 1), None): [1, 1],
                ((5, 1), None, (4, 2), None, (4, 0), None): [4, 1],
            },
            (1, 0, 2, 0, 0, 0): {
                ((1, 2), None, (1, 0), None, None, None): [1, 1],
            },
            (1, 0, 0, 0, 1, 0): {
                ((1, 2), None, None, None, (2, 1), None): [2, 0],
            },
            (1, 0, 0, 0, 2, 0): {
                ((1, 2), None, None, None, (2, 3), None): [2, 0],
            },
            (2, 0, 1, 0, 0, 0): {
                ((1, 2), None, (1, 1), None, None, None): [1, 1],
            },
            (0, 0, 2, 0, 1, 0): {
                (None, None, (4, 2), None, (2, 1), None): [4, 1],
            },
            (0, 0, 1, 0, 2, 0): {
                (None, None, (1, 1), None, (4, 0), None): [4, 1],
            },
            (2, 0, 2, 0, 0, 0): {
                ((1, 2), None, (1, 0), None, None, None): [1, 1],
            },
        },
        11: {
            (0, 0, 2, 0, 2, 1): {
                (None, None, (3, 2), None, (2, 2), (1, 2)): [2, 1],
            },
            (0, 0, 2, 0, 0, 2): {
                (None, None, (1, 3), None, None, (1, 1)): [1, 2],
            },
            (0, 0, 1, 0, 1, 0): {
                (None, None, (1, 3), None, (2, 3), None): [5, 1],
            },
            (0, 0, 2, 0, 2, 0): {
                (None, None, (5, 2), None, (5, 0), None): [5, 1],
            },
            (0, 0, 1, 0, 2, 0): {
                (None, None, (1, 3), None, (5, 0), None): [5, 1],
            },
            (0, 0, 0, 0, 2, 1): {
                (None, None, None, None, (2, 2), (1, 2)): [2, 1],
            },
            (0, 0, 1, 0, 2, 2): {
                (None, None, (1, 3), None, (5, 0), (4, 1)): [5, 1],
                (None, None, (1, 3), None, (0, 2), (1, 1)): [1, 2],
            },
            (0, 0, 2, 0, 0, 1): {
                (None, None, (1, 3), None, None, (1, 2)): [1, 2],
            },
            (0, 0, 0, 0, 1, 1): {
                (None, None, None, None, (2, 3), (1, 2)): [2, 1],
            },
            (0, 0, 1, 0, 0, 1): {
                (None, None, (1, 3), None, None, (1, 2)): [1, 2],
            },
            (0, 0, 2, 0, 1, 2): {
                (None, None, (3, 2), None, (2, 3), (2, 0)): [2, 1],
                (None, None, (5, 2), None, (2, 3), (4, 1)): [5, 1],
            },
            (0, 0, 0, 0, 1, 2): {
                (None, None, None, None, (2, 3), (2, 0)): [2, 1],
            },
            (0, 0, 2, 0, 2, 2): {
                (None, None, (1, 3), None, (0, 2), (1, 1)): [1, 2],
                (None, None, (5, 2), None, (5, 0), (4, 1)): [5, 1],
                (None, None, (3, 2), None, (2, 2), (2, 0)): [2, 1],
            },
            (0, 0, 2, 0, 1, 0): {
                (None, None, (5, 2), None, (2, 3), None): [5, 1],
            },
            (0, 0, 1, 0, 0, 2): {
                (None, None, (1, 3), None, None, (1, 1)): [1, 2],
            },
            (0, 0, 0, 0, 2, 2): {
                (None, None, None, None, (2, 2), (2, 0)): [2, 1],
            },
        },
    }

    # Tetra
    peripheries[3] = {
        52: [0, 0],
        56: [0, 1],
        25: [0, 2],
        21: [0, 3],
        38: [1, 0],
        42: [1, 1],
        11: [1, 2],
        7: [1, 3],
        }

    # hepta
    peripheries[4] = {
        0: {
            (0, 0, 0, 3, 3, 3): {
                (None, None, None, (0, 1), (0, 1), (0, 1)): [0, 1],
            },
            (3, 3, 0, 3, 0, 0): {
                ((1, 2), (1, 2), None, (1, 2), None, None): [1, 2],
            },
            (3, 0, 0, 3, 3, 0): {
                ((0, 2), None, None, (0, 2), (0, 2), None): [0, 2],
            },
            (0, 3, 0, 3, 0, 3): {
                (None, (1, 1), None, (1, 1), None, (1, 1)): [1, 1],
            },
            (0, 0, 3, 0, 3, 3): {
                (None, None, (0, 0), None, (0, 0), (0, 0)): [0, 0],
            },
            (3, 0, 3, 0, 3, 0): {
                ((0, 3), None, (0, 3), None, (0, 3), None): [0, 3],
            },
            (3, 3, 3, 0, 0, 0): {
                ((1, 3), (1, 3), (1, 3), None, None, None): [1, 3],
            },
            (0, 3, 3, 0, 0, 3): {
                (None, (1, 0), (1, 0), None, None, (1, 0)): [1, 0],
            },
            (3, 3, 0, 3, 0, 0): {
                ((1, 2), (1, 2), None, (1, 2), None, None): [1, 2],
            },
            (0, 0, 0, 3, 3, 3): {
                (None, None, None, (0, 1), (0, 1), (0, 1)): [0, 1],
            },
            (3, 0, 0, 3, 3, 0): {
                ((0, 2), None, None, (0, 2), (0, 2), None): [0, 2],
            },
            (0, 3, 0, 3, 0, 3): {
                (None, (1, 1), None, (1, 1), None, (1, 1)): [1, 1],
            },
            (3, 3, 3, 0, 0, 0): {
                ((1, 3), (1, 3), (1, 3), None, None, None): [1, 3],
            },
            (0, 3, 3, 0, 0, 3): {
                (None, (1, 0), (1, 0), None, None, (1, 0)): [1, 0],
            },
            (0, 0, 3, 0, 3, 3): {
                (None, None, (0, 0), None, (0, 0), (0, 0)): [0, 0],
            },
            (3, 0, 3, 0, 3, 0): {
                ((0, 3), None, (0, 3), None, (0, 3), None): [0, 3],
            },
        },
        1: {
            (0, 0, 0, 3, 3, 0): {
                (None, None, None, (0, 2), (0, 2), None): [0, 2],
            },
            (0, 3, 0, 3, 0, 0): {
                (None, (1, 2), None, (1, 2), None, None): [1, 2],
            },
            (0, 0, 3, 0, 3, 0): {
                (None, None, (0, 3), None, (0, 3), None): [0, 3],
            },
            (0, 3, 3, 0, 0, 0): {
                (None, (1, 3), (1, 3), None, None, None): [1, 3],
            },
            (0, 0, 0, 3, 3, 3): {
                (None, None, None, (0, 1), (0, 1), (0, 1)): [0, 1],
            },
            (0, 3, 3, 0, 0, 3): {
                (None, (1, 0), (1, 0), None, None, (1, 0)): [1, 0],
            },
            (0, 0, 3, 0, 3, 3): {
                (None, None, (0, 0), None, (0, 0), (0, 0)): [0, 0],
            },
            (0, 3, 0, 3, 0, 3): {
                (None, (1, 1), None, (1, 1), None, (1, 1)): [1, 1],
            },
        },
        2: {
            (3, 0, 3, 0, 0, 0): {
                ((1, 3), None, (1, 3), None, None, None): [1, 3],
            },
            (0, 0, 3, 0, 0, 3): {
                (None, None, (1, 0), None, None, (1, 0)): [1, 0],
            },
            (3, 0, 0, 3, 0, 0): {
                ((1, 2), None, None, (1, 2), None, None): [1, 2],
            },
            (0, 0, 0, 3, 0, 3): {
                (None, None, None, (1, 1), None, (1, 1)): [1, 1],
            },
            (0, 0, 0, 3, 3, 3): {
                (None, None, None, (0, 1), (0, 1), (0, 1)): [0, 1],
            },
            (3, 0, 3, 0, 3, 0): {
                ((0, 3), None, (0, 3), None, (0, 3), None): [0, 3],
            },
            (0, 0, 3, 0, 3, 3): {
                (None, None, (0, 0), None, (0, 0), (0, 0)): [0, 0],
            },
            (3, 0, 0, 3, 3, 0): {
                ((0, 2), None, None, (0, 2), (0, 2), None): [0, 2],
            },
        },
        3: {
            (0, 0, 0, 3, 3, 3): {
                (None, None, None, (0, 1), (0, 1), (0, 1)): [0, 1],
            },
        },
        4: {
            (0, 0, 0, 0, 3, 3): {
                (None, None, None, None, (0, 0), (0, 0)): [0, 0],
            },
            (3, 0, 0, 0, 3, 0): {
                ((0, 3), None, None, None, (0, 3), None): [0, 3],
            },
            (3, 3, 0, 0, 0, 0): {
                ((1, 3), (1, 3), None, None, None, None): [1, 3],
            },
            (0, 3, 0, 0, 0, 3): {
                (None, (1, 0), None, None, None, (1, 0)): [1, 0],
            },
            (3, 3, 0, 3, 0, 0): {
                ((1, 2), (1, 2), None, (1, 2), None, None): [1, 2],
            },
            (0, 0, 0, 3, 3, 3): {
                (None, None, None, (0, 1), (0, 1), (0, 1)): [0, 1],
            },
            (3, 0, 0, 3, 3, 0): {
                ((0, 2), None, None, (0, 2), (0, 2), None): [0, 2],
            },
            (0, 3, 0, 3, 0, 3): {
                (None, (1, 1), None, (1, 1), None, (1, 1)): [1, 1],
            },
        },
        5: {
            (0, 0, 0, 3, 3, 3): {
                (None, None, None, (0, 1), (0, 1), (0, 1)): [0, 1],
            },
            (0, 3, 0, 3, 0, 3): {
                (None, (1, 1), None, (1, 1), None, (1, 1)): [1, 1],
            },
        },
        8: {
            (0, 0, 0, 0, 3, 3): {
                (None, None, None, None, (0, 1), (0, 1)): [0, 1],
            },
            (3, 0, 0, 0, 3, 0): {
                ((0, 2), None, None, None, (0, 2), None): [0, 2],
            },
            (3, 3, 0, 0, 0, 0): {
                ((1, 2), (1, 2), None, None, None, None): [1, 2],
            },
            (0, 3, 0, 0, 0, 3): {
                (None, (1, 1), None, None, None, (1, 1)): [1, 1],
            },
            (3, 3, 3, 0, 0, 0): {
                ((1, 3), (1, 3), (1, 3), None, None, None): [1, 3],
            },
            (3, 0, 3, 0, 3, 0): {
                ((0, 3), None, (0, 3), None, (0, 3), None): [0, 3],
            },
            (0, 0, 3, 0, 3, 3): {
                (None, None, (0, 0), None, (0, 0), (0, 0)): [0, 0],
            },
            (0, 3, 3, 0, 0, 3): {
                (None, (1, 0), (1, 0), None, None, (1, 0)): [1, 0],
            },
        },
        9: {
            (0, 3, 3, 0, 0, 3): {
                (None, (1, 0), (1, 0), None, None, (1, 0)): [1, 0],
            },
            (0, 0, 3, 0, 3, 3): {
                (None, None, (0, 0), None, (0, 0), (0, 0)): [0, 0],
            },
        },
        16: {
            (3, 0, 3, 0, 0, 0): {
                ((0, 3), None, (0, 3), None, None, None): [0, 3],
            },
            (0, 0, 3, 0, 0, 3): {
                (None, None, (0, 0), None, None, (0, 0)): [0, 0],
            },
            (3, 0, 0, 3, 0, 0): {
                ((0, 2), None, None, (0, 2), None, None): [0, 2],
            },
            (0, 0, 0, 3, 0, 3): {
                (None, None, None, (0, 1), None, (0, 1)): [0, 1],
            },
            (3, 3, 0, 3, 0, 0): {
                ((1, 2), (1, 2), None, (1, 2), None, None): [1, 2],
            },
            (0, 3, 3, 0, 0, 3): {
                (None, (1, 0), (1, 0), None, None, (1, 0)): [1, 0],
            },
            (3, 3, 3, 0, 0, 0): {
                ((1, 3), (1, 3), (1, 3), None, None, None): [1, 3],
            },
            (0, 3, 0, 3, 0, 3): {
                (None, (1, 1), None, (1, 1), None, (1, 1)): [1, 1],
            },
        },
        32: {
            (0, 0, 0, 3, 3, 0): {
                (None, None, None, (0, 1), (0, 1), None): [0, 1],
            },
            (0, 3, 0, 3, 0, 0): {
                (None, (1, 1), None, (1, 1), None, None): [1, 1],
            },
            (0, 0, 3, 0, 3, 0): {
                (None, None, (0, 0), None, (0, 0), None): [0, 0],
            },
            (0, 3, 3, 0, 0, 0): {
                (None, (1, 0), (1, 0), None, None, None): [1, 0],
            },
            (3, 3, 0, 3, 0, 0): {
                ((1, 2), (1, 2), None, (1, 2), None, None): [1, 2],
            },
            (3, 0, 3, 0, 3, 0): {
                ((0, 3), None, (0, 3), None, (0, 3), None): [0, 3],
            },
            (3, 3, 3, 0, 0, 0): {
                ((1, 3), (1, 3), (1, 3), None, None, None): [1, 3],
            },
            (3, 0, 0, 3, 3, 0): {
                ((0, 2), None, None, (0, 2), (0, 2), None): [0, 2],
            },
        },
        34: {
            (3, 0, 0, 3, 3, 0): {
                ((0, 2), None, None, (0, 2), (0, 2), None): [0, 2],
            },
        },
        36: {
            (3, 3, 0, 3, 0, 0): {
                ((1, 2), (1, 2), None, (1, 2), None, None): [1, 2],
            },
            (3, 0, 0, 3, 3, 0): {
                ((0, 2), None, None, (0, 2), (0, 2), None): [0, 2],
            },
        },
        40: {
            (3, 0, 3, 0, 3, 0): {
                ((0, 3), None, (0, 3), None, (0, 3), None): [0, 3],
            },
            (3, 3, 3, 0, 0, 0): {
                ((1, 3), (1, 3), (1, 3), None, None, None): [1, 3],
            },
        },
    }

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
        periphery = {}
        for position_index in self._border:
            block = self._block_list[position_index]
            if block_config[block.get_id()].shape != shape_id:
                continue
            position = self._block_list.get_position(position_index)
            periphery_index = self.get_position_periphery_index(position, 1)
            periphery_shape, periphery_orientation = self.get_position_shape_periphery(position, 1)
            rotations = block.get_rotations()
            axis_rotation = block.get_axis_rotation()
            if periphery_index not in periphery:
                periphery[periphery_index] = {}
            if periphery_shape not in periphery[periphery_index]:
                periphery[periphery_index][periphery_shape] = {}
            periphery[periphery_index][periphery_shape][periphery_orientation] = [axis_rotation, rotations]
        return periphery

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
