__author__ = 'Peter Hofmann'


class AutoShape(object):
    """
    Collection of auto shape stuff
    """

    peripheries = dict()
    # "cube": 0,
    # "1/4": 1,
    # "1/2": 2,
    # "3/4": 3,
    # "Wedge": 4,
    # "Corner": 5,
    # "Tetra": 6,
    # "Hepta": 7,

    # wedge
    peripheries[4] = {
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
    peripheries[5] = {
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
    peripheries[6] = {
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
    peripheries[7] = {
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
