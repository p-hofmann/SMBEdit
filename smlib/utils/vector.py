import struct


class Vector(object):
    """
    Collection of vector calculations
    """

    @staticmethod
    def get_index(position):
        """

        @param position:
        @type position: (int, int, int)

        @return:
        @rtype: int
        """
        tmp = struct.pack("<hhhh", position[0], position[1], position[2], 0)
        return struct.unpack("<q", tmp)[0]

    @staticmethod
    def get_position(position_index):
        """

        @param position_index:
        @type position_index: int

        @return:
        @rtype: (int, int, int)
        """
        # assert isinstance(position_index, int), position_index
        tmp = struct.pack("<q", position_index)
        return tuple(struct.unpack("<hhhh", tmp)[:3])

    @staticmethod
    def shift_position_index(position_index, offset):
        """

        @type position_index: int
        @type offset: (int, int, int)

        @return:
        @rtype: int
        """
        # Vector
        position = Vector.get_position(position_index)
        new_position = Vector.addition(position, offset)
        return Vector.get_index(new_position)

    @staticmethod
    def addition(vector1, vector2):
        """
        Add one vector to another

        @param vector1: (x,y,z)
        @type vector1: int, int, int
        @param vector2: (x,y,z)
        @type vector2: int, int, int

        @return:
        @rtype: int, int, int
        """
        assert len(vector1) == len(vector2)
        result = [0] * len(vector1)
        for index in range(0, len(vector1)):
            result[index] = vector1[index] + vector2[index]
        return tuple(result)

    @staticmethod
    def subtraction(vector1, vector2):
        """
        Subtract vector2 from vector1

        @param vector1: (x,y,z)
        @type vector1: int, int, int
        @param vector2: (x,y,z)
        @type vector2: int, int, int

        @return:
        @rtype: int, int, int
        """
        assert len(vector1) == len(vector2)
        result = [0] * len(vector1)
        for index in range(0, len(vector1)):
            result[index] = vector1[index] - vector2[index]
        return tuple(result)

    @staticmethod
    def multiplication(vector1, vector2):
        """
        multiply entries of vector2 with vector1

        @param vector1: (x,y,z)
        @type vector1: int, int, int
        @param vector2: (x,y,z)
        @type vector2: int, int, int

        @return:
        @rtype: int, int, int
        """
        assert len(vector1) == len(vector2)
        result = [0] * len(vector1)
        for index in range(0, len(vector1)):
            result[index] = vector1[index] * vector2[index]
        return tuple(result)

    @staticmethod
    def distance(vector1, vector2):
        """
        Calculate distance between two vectors

        @param vector1: (x,y,z)
        @type vector1: int, int, int
        @param vector2: (x,y,z)
        @type vector2: int, int, int

        @return: Distance between two vectors
        @rtype: int
        """
        assert len(vector1) == len(vector2)
        distance = 0
        for index in range(0, len(vector1)):
            distance += abs(vector1[index] - vector2[index])
        return distance

    _core_position = (16, 16, 16)

    @staticmethod
    def get_direction_vector_to_center(position):
        """
        Relocate center/core in a direction

        @param position: vector
        @type position: int, int, int

        @rtype: int, int, int
        """
        return Vector.subtraction(position, Vector._core_position)

    # #######################################
    # ###  Turning
    # #######################################

    _turn_indexes = {
        0: (0, 2, 1),  # tilt up
        1: (0, 2, 1),  # tilt down
        2: (2, 1, 0),  # turn right
        3: (2, 1, 0),  # turn left
        4: (1, 0, 2),  # tilt right
        5: (1, 0, 2),  # tilt left
    }

    _turn_multiplicator = {
        0: (1, 1, -1),  # tilt up
        1: (1, -1, 1),  # tilt down
        2: (-1, 1, 1),  # turn right
        3: (1, 1, -1),  # turn left
        4: (-1, 1, 1),  # tilt right
        5: (1, -1, 1),  # tilt left
    }

    @staticmethod
    def tilt_turn_position(position, tilt_index):
        """
        Turn or tilt this entity.

        @param position:
        @type position: tuple
        @param tilt_index: integer representing a specific turn
        @type tilt_index: int

        @return: new minimum and maximum coordinates of the blueprint
        @rtype: tuple[int,int,int], tuple[int,int,int]
        """
        multiplicator = Vector._turn_multiplicator[tilt_index]
        indexes = Vector._turn_indexes[tilt_index]
        new_block_position = Vector.subtraction(position, Vector._core_position)
        new_block_position = (
            multiplicator[0]*new_block_position[indexes[0]],
            multiplicator[1]*new_block_position[indexes[1]],
            multiplicator[2]*new_block_position[indexes[2]])
        new_block_position = Vector.addition(new_block_position, Vector._core_position)
        return new_block_position

    @staticmethod
    def mirror_position(position_block, axis_index, position_mirror=None):
        """

        @param position_block:
        @param axis_index:
        @param position_mirror:
        @return:
        """
        if position_mirror is None:
            position_mirror = Vector._core_position
        vector_factor = [1] * 3
        vector_factor[axis_index] = -1
        position_tmp = Vector.subtraction(position_block, position_mirror)
        position_tmp = Vector.multiplication(position_tmp, vector_factor)
        return Vector.addition(position_tmp, position_mirror)
