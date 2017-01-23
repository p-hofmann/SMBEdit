__author__ = 'Peter Hofmann'


class Vector(object):
    """
    Collection of vector calculations
    """

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
