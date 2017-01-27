import sys
from lib.utils.blocklist import BlockList, BlockSmd3
from lib.utils.blockconfig import block_config


__author__ = 'Peter Hofmann'


class AutoShape(object):
    """
    Collection of auto shape stuff

    @type _block_pool: BlockList
    """

    def __init__(self, block_pool):
        """

        @type block_pool: BlockList
        """
        self._block_pool = block_pool

    def get_position_periphery_index_9x9(self, position):
        """
        Every position in a 3x3x3 periphery is represented by a bit.

        @type position: tuple[int]
        @rtype: int
        """
        periphery_index = 0
        power = 1
        for x in range(position[0]-1, position[0]+2):
            for y in range(position[1]-1, position[1]+2):
                for z in range(position[2]-1, position[2]+2):
                    position_tmp = (x, y, z)
                    if position_tmp == position:
                        continue
                    if self._block_pool.has_block_at(position_tmp):
                        periphery_index |= power
                    power <<= 1
        # print power
        return periphery_index

    def get_position_periphery_index(self, position, periphery_range):
        """
        Some positions in a 3x3x3 periphery, represented by a bit each.

        @type position: tuple[int]
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
                    if self._block_pool.has_block_at(position_tmp):
                        periphery_index |= power
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

        @type position: tuple[int]
        @type periphery_range: int

        @rtype: tple[int]
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
                    if self._block_pool.has_block_at(position_tmp):
                        block_tmp = self._block_pool[position_tmp]
                        block_id = block_tmp.get_id()
                        is_angled_shape = False
                        if block_config[block_id].shape in angle_shapes:
                            is_angled_shape = True
                        shape_periphery.append(is_angled_shape)
        return tuple(shape_periphery)

    def auto_hull_shape_independent(self, auto_wedge, auto_tetra):
        """
        Replace hull blocks with shaped hull blocks with shapes,
        that can be determined without knowing the shapes of blocks around it

        @type auto_wedge: bool
        @type auto_tetra: bool
        """
        for position, block in self._block_pool.items():
            block_id = block.get_id()
            if not block_config[block_id].is_hull():
                continue

            periphery_index = self.get_position_periphery_index(position, 1)
            shape_id_wedge = block_config.get_shape_id("wedge")
            shape_id_tetra = block_config.get_shape_id("tetra")
            if auto_wedge and periphery_index in AutoShape.peripheries[shape_id_wedge]:
                # "wedge"
                new_shape_id = shape_id_wedge
            elif auto_tetra and periphery_index in AutoShape.peripheries[shape_id_tetra]:
                # tetra
                new_shape_id = shape_id_tetra
            else:
                continue

            bit_19, bit_22, bit_23, rotations = AutoShape.peripheries[new_shape_id][periphery_index]
            block_hull_tier, color_id, shape_id = block_config[block_id].get_details()
            new_block_id = block_config.get_block_id_by_details(block_hull_tier, color_id, new_shape_id)
            new_block = BlockSmd3(block.get_int_24bit()).get_modification(
                block_id=new_block_id, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)
            self._block_pool(position, new_block.get_int_24bit())

    def auto_hull_shape_dependent(self, block_shape_id):
        """
        Replace hull blocks with shaped hull blocks with shapes,
        that can only be determined by the shapes of blocks around it

        @type block_shape_id: int
        """
        for position, block in self._block_pool.items():
            block_id = block.get_id()
            if not block_config[block_id].is_hull():
                continue

            periphery_index = self.get_position_periphery_index(position, 1)
            if periphery_index not in AutoShape.peripheries[block_shape_id]:
                continue
            periphery_shape = self.get_position_shape_periphery(position, 1)
            if periphery_shape not in AutoShape.peripheries[block_shape_id][periphery_index]:
                continue
            bit_19, bit_22, bit_23, rotations = AutoShape.peripheries[block_shape_id][periphery_index][periphery_shape]
            block_hull_type, color, shape_id = block_config[block_id].get_details()
            new_block_id = block_config.get_block_id_by_details(block_hull_type, color, block_shape_id)
            new_block = BlockSmd3(block.get_int_24bit()).get_modification(
                block_id=new_block_id, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)
            self._block_pool(position, new_block.get_int_24bit())

    def auto_hull_shape(self, auto_wedge, auto_tetra, auto_corner, auto_hepta=None):
        """
        Automatically set shapes to blocks on edges and corners.

        @type auto_wedge: bool
        @type auto_tetra: bool
        @type auto_corner: bool
        @type auto_hepta: bool
        """
        self.auto_hull_shape_independent(auto_wedge, auto_tetra)
        shape_id_corner = block_config.get_shape_id("corner")
        shape_id_hepta = block_config.get_shape_id("hepta")
        if auto_corner:
            self.auto_hull_shape_dependent(shape_id_corner)
        if auto_hepta:
            self.auto_hull_shape_dependent(shape_id_hepta)

    def auto_wedge_debug(self):
        """
        Replace hull blocks on edges with wedges.
        """
        peripheries = {}
        for position, block in self._block_pool.items():
            if not block_config[block.get_id()].is_hull():
                continue
            # wedge 599
            # corner 600
            # hepta 601
            # tetra 602
            if block.get_id() != 602:
                continue
            periphery_index = self.get_position_periphery_index(position, 1)
            if periphery_index == 0:
                continue
            # hull_type, color, shape_id = BlueprintUtils._get_hull_details(block.get_id())
            bit_19, bit_23, bit_22, rotations = block.get_orientation().get_orientation_values()
            if periphery_index in peripheries:
                tmp = (bit_19, bit_22, bit_23, rotations)
                if peripheries[periphery_index] != tmp:
                    sys.stderr.write("{}: {}\n".format(
                        periphery_index, tmp))
                continue
            sys.stdout.write("\t\t{}: [{}, {}, {}, {}],\n".format(
                periphery_index, bit_19, bit_22, bit_23, rotations))
            # sys.stdout.write("\t\t{}: [{}, {}],  # {}\n".format(periphery_index, shape_id, block.get_int_24bit(), position))

            # int_24 = block.get_int_24bit()
            # block.update(block_id=599, bit_19=bit_19, bit_22=bit_22, bit_23=bit_23, rotations=rotations)
            # assert int_24 == block.get_int_24bit()
            peripheries[periphery_index] = (bit_19, bit_22, bit_23, rotations)

    def auto_hepta_debug(self):
        """
        Replace hull blocks on edges with wedges.
        """
        peripheries = {}
        bad_orientations = 0
        for position, block in self._block_pool.items():
            if not block_config[block.get_id()].is_hull():
                continue
            # wedge 599
            # corner 600
            # hepta 601
            # tetra 602
            if block.get_id() != 601:
                continue
            periphery_index = self.get_position_periphery_index(position, 1)
            periphery_shape = self.get_position_shape_periphery(position, 1)
            if periphery_index not in peripheries:
                peripheries[periphery_index] = {}

            bit_19, bit_23, bit_22, rotations = block.get_orientation().get_orientation_values()
            orientation = (bit_19, bit_22, bit_23, rotations)

            if all(periphery_shape):
                continue
            if periphery_shape in peripheries[periphery_index] and peripheries[periphery_index][periphery_shape] != orientation:
                bad_orientations += 1
                continue
            peripheries[periphery_index][periphery_shape] = orientation

        print("bad_orientations", bad_orientations)
        for periphery_index in peripheries:
            print("\t\t{}:".format(periphery_index), '{')
            for periphery_shape in peripheries[periphery_index]:
                print("\t\t\t{}: {},".format(periphery_shape, peripheries[periphery_index][periphery_shape]))
            print("\t\t},")

    peripheries = dict()
    # shapes = ["cube", "wedge", "corner", "tetra", "hepta"]
    # "cube": 0,
    # "Wedge": 1,
    # "Corner": 2,
    # "Tetra": 3,
    # "Hepta": 4,

    # wedge
    peripheries[1] = {
        # [bit_19, bit_22, bit_23, rotations]
        15: [0, 0, 0, 3],
        54: [0, 0, 1, 3],
        43: [0, 0, 0, 0],
        27: [0, 0, 1, 0],
        58: [0, 0, 1, 2],
        29: [0, 1, 0, 1],
        39: [0, 0, 0, 2],
        23: [0, 0, 1, 1],
        53: [0, 1, 0, 2],
        57: [0, 1, 0, 0],
        60: [0, 1, 0, 3],
        46: [0, 0, 0, 1],
    }

    # corner
    peripheries[2] = {
        # (): [bit_19, bit_22, bit_23, rotations]
        38: {
            (True, True, False): (1, 1, 0, 0),
            (True, False, True): (0, 0, 1, 2),
            (False, True, True): (0, 0, 0, 2),
        },
        7: {
            (False, True, True): (1, 0, 0, 0),
            (True, False, True): (0, 0, 0, 1),
            (True, True, False): (0, 0, 1, 3),
        },
        42: {
            (False, True, True): (0, 0, 0, 3),
            (True, True, False): (1, 1, 0, 3),
            (True, False, True): (0, 1, 1, 3),
        },
        11: {
            (False, True, True): (1, 0, 0, 3),
            (True, True, False): (0, 1, 1, 0),
            (True, False, True): (0, 0, 0, 0),
        },
        52: {
            (False, True, True): (0, 0, 1, 1),
            (True, True, False): (1, 1, 0, 1),
            (True, False, True): (0, 1, 0, 2),
        },
        21: {
            (False, True, True): (1, 0, 0, 1),
            (True, False, True): (0, 0, 1, 0),
            (True, True, False): (0, 1, 0, 1),
        },
        56: {
            (False, True, True): (0, 1, 1, 2),
            (True, False, True): (0, 1, 0, 3),
            (True, True, False): (1, 1, 0, 2),
        },
        25: {
            (False, True, True): (1, 0, 0, 2),
            (True, True, False): (0, 1, 0, 0),
            (True, False, True): (0, 1, 1, 1),
        },
}

    # tetra
    peripheries[3] = {
        # [bit_19, bit_22, bit_23, rotations]
        56: [0, 1, 0, 3],
        38: [0, 0, 0, 2],
        21: [0, 1, 0, 1],
        25: [0, 1, 0, 0],
        11: [0, 0, 0, 0],
        42: [0, 0, 0, 3],
        7: [0, 0, 0, 1],
        52: [0, 1, 0, 2],
        }

    # hepta
    peripheries[4] = {
        59: {
            (True, False, False, True, False): (0, 0, 0, 3),
            (True, True, False, False, False): (0, 1, 0, 3),
            (False, True, False, False, True): (0, 1, 0, 0),
            (False, False, False, True, True): (0, 0, 0, 0),
        },
        47: {
            (True, False, True, False, False): (0, 0, 0, 3),
            (True, False, False, True, False): (0, 0, 0, 2),
            (False, False, False, True, True): (0, 0, 0, 1),
            (False, False, True, False, True): (0, 0, 0, 0),
        },
        55: {
            (True, True, False, False, False): (0, 1, 0, 2),
            (True, False, False, True, False): (0, 0, 0, 2),
            (False, True, False, False, True): (0, 1, 0, 1),
            (False, False, False, True, True): (0, 0, 0, 1),
        },
        63: {
            (False, True, True, False, False, True): (0, 1, 0, 0),
            (True, True, True, False, False, False): (0, 1, 0, 3),
            (True, False, True, False, True, False): (0, 0, 0, 3),
            (False, False, False, True, True, True): (0, 0, 0, 1),
            (True, True, False, True, False, False): (0, 1, 0, 2),
            (False, True, False, True, False, True): (0, 1, 0, 1),
            (True, False, False, True, True, False): (0, 0, 0, 2),
            (False, False, True, False, True, True): (0, 0, 0, 0),
        },
        61: {
            (True, False, True, False, False): (0, 1, 0, 2),
            (False, False, True, False, True): (0, 1, 0, 1),
            (True, True, False, False, False): (0, 1, 0, 3),
            (False, True, False, False, True): (0, 1, 0, 0),
        },
        62: {
            (False, True, False, True, False): (0, 0, 0, 3),
            (False, False, True, True, False): (0, 0, 0, 2),
            (True, False, True, False, False): (0, 1, 0, 2),
            (True, True, False, False, False): (0, 1, 0, 3),
        },
        31: {
            (False, True, False, True, False): (0, 1, 0, 1),
            (False, False, True, False, True): (0, 0, 0, 0),
            (False, True, True, False, False): (0, 1, 0, 0),
            (False, False, False, True, True): (0, 0, 0, 1),
        },
    }
