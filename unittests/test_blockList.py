from unittest import TestCase
from lib.utils.vector import Vector
from lib.utils.blocklist import BlockList


__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: BlockList
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        # self._blueprint = blueprint_handler
        self.object = None

    def setUp(self):
        self.object = BlockList()

    def tearDown(self):
        self.object = None


class TestBlockList(DefaultSetup):
    def test_get_index_get_position(self):
        position_range = range(-32768, 32767)
        for x in position_range:
            for y in [0]:
                for z in [0]:
                    expected_position = (x, y, z)
                    result = Vector.get_position(Vector.get_index(expected_position))
                    self.assertTupleEqual(expected_position, result)

    # TODO: more tests
