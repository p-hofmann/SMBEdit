from unittest import TestCase
from io import BytesIO

from smlib.utils.smbinarystream import SMBinaryStream
from smlib.smblueprint.logic import Logic
from smlib.smblueprint.smd3.smd import Smd
from smlib.utils.blockconfig import block_config
from unittests.testinput import blueprint_handler

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Logic
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None

    def setUp(self):
        block_config.from_hard_coded()
        self.object = Logic()
        self._blueprints = blueprint_handler

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestLogic(DefaultSetup):
    def test_read_file(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)

    def test_bad_version(self):
        input_stream = SMBinaryStream(BytesIO())
        input_stream.write_int32_unassigned(1)
        input_stream.seek(0)
        self.assertRaises(AssertionError, self.object._read_file, input_stream)

    def test_bad_controller_version(self):
        input_stream = SMBinaryStream(BytesIO())
        input_stream.write_int32_unassigned(0)
        input_stream.write_int32(-1024)
        input_stream.seek(0)
        self.assertRaises(NotImplementedError, self.object._read_file, input_stream)

    def test_smd2_logic(self):
        input_stream = SMBinaryStream(BytesIO())
        input_stream.write_int32_unassigned(0)
        input_stream.write_int32(0)
        input_stream.seek(0)
        self.object._read_file(input_stream)
        expected_tuple = (8, 8, 8)
        self.assertTupleEqual(expected_tuple, self.object._offset)

        input_stream = SMBinaryStream(BytesIO())
        input_stream.write_int32_unassigned(0)
        input_stream.write_int32(-1026)
        input_stream.write_int32_unassigned(0)
        input_stream.seek(0)
        self.object._read_file(input_stream)
        self.assertIsNone(self.object._offset)

    def test_set_of_positions(self):
        expected_set_of_positions = set()
        expected_set_of_positions.add((1, 2, 3))
        expected_set_of_positions.add((1, 2, 5))

        input_stream = SMBinaryStream(BytesIO())
        self.object._write_list_of_positions(expected_set_of_positions, input_stream)

        input_stream.seek(0)
        set_of_positions = self.object._read_set_of_positions(input_stream)
        self.assertSetEqual(expected_set_of_positions, set_of_positions)

    def test_dict_of_groups(self):
        expected_set_of_positions = set()
        expected_set_of_positions.add((1, 2, 3))
        expected_set_of_positions.add((1, 2, 5))
        expected_dict = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        input_stream = SMBinaryStream(BytesIO())
        self.object._write_list_of_groups(expected_dict, input_stream)
        input_stream.seek(0)
        read_dict = self.object._read_dict_of_groups(input_stream)
        self.assertDictEqual(expected_dict, read_dict)

    def test__write_list_of_controllers(self):
        expected_set_of_positions = set()
        expected_set_of_positions.add((1, 2, 3))
        expected_set_of_positions.add((1, 2, 5))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (0, 0, 0): expected_group,
            (1, 0, 0): expected_group,
        }
        input_stream = SMBinaryStream(BytesIO())
        self.object._controller_position_to_block_id_to_block_positions = expected_controller
        self.object._write_list_of_controllers(input_stream)
        input_stream.seek(0)
        read_dict = self.object._read_list_of_controllers(input_stream)
        self.assertDictEqual(expected_controller, read_dict)

    def test_set_link(self):
        expected_set_of_positions = set()
        expected_set_of_positions.add((1, 2, 3))
        expected_set_of_positions.add((1, 2, 5))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (0, 0, 0): expected_group,
            (1, 0, 0): expected_group,
        }
        for position_controller, group in expected_controller.items():
            for block_id, set_of_positions in group.items():
                self.object.set_link(position_controller, block_id, set_of_positions)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

    def test_move_center(self):
        directory_vector = (1, 1, 1)

        initial_set_of_positions = set()
        initial_set_of_positions.add((16, 16, 16))
        initial_set_of_positions.add((17, 17, 17))
        initial_group = {
            1: initial_set_of_positions,
            100: initial_set_of_positions,
        }
        initial_controller = {
            (16, 16, 16): initial_group,
            (17, 17, 17): initial_group,
        }

        # station
        expected_set_of_positions = set()
        expected_set_of_positions.add((15, 15, 15))
        expected_set_of_positions.add((16, 16, 16))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (15, 15, 15): expected_group,
            (16, 16, 16): expected_group,
        }
        self.object._controller_position_to_block_id_to_block_positions = initial_controller
        self.object.move_center(directory_vector, 2)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

        # ship
        expected_set_of_positions = set()
        expected_set_of_positions.add((15, 15, 15))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (16, 16, 16): expected_group,
        }
        self.object._controller_position_to_block_id_to_block_positions = initial_controller
        self.object.move_center(directory_vector, 0)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

    def test__update_groups(self):
        initial_set_of_positions0 = set()
        initial_set_of_positions0.add((16, 16, 16))
        initial_set_of_positions0.add((17, 17, 17))
        initial_set_of_positions1 = set()
        initial_set_of_positions1.add((16, 16, 16))
        initial_set_of_positions1.add((17, 17, 17))
        initial_set_of_positions2 = set()
        initial_set_of_positions2.add((16, 16, 16))
        initial_set_of_positions2.add((17, 17, 17))
        initial_set_of_positions3 = set()
        initial_set_of_positions3.add((16, 16, 16))
        initial_set_of_positions3.add((17, 17, 17))
        initial_group0 = {
            1: initial_set_of_positions0,
            100: initial_set_of_positions1,
        }
        initial_group1 = {
            1: initial_set_of_positions2,
            100: initial_set_of_positions3,
        }
        initial_controller = {
            (16, 16, 16): initial_group0,
            (17, 17, 17): initial_group1,
        }

        self.object._controller_position_to_block_id_to_block_positions = initial_controller

        expected_set_of_positions = set()
        expected_set_of_positions.add((16, 16, 16))
        expected_set_of_positions.add((17, 17, 17))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (16, 16, 16): expected_group,
            (17, 17, 17): dict(),
        }
        controller_position = (17, 17, 17)
        block_ids = [1, 100]
        smd = Smd()
        for block_id in block_ids:
            self.object._update_groups(controller_position, block_id, smd)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

    def test_update(self):
        initial_set_of_positions0 = set()
        initial_set_of_positions0.add((16, 16, 16))
        initial_set_of_positions0.add((17, 17, 17))
        initial_set_of_positions1 = set()
        initial_set_of_positions1.add((16, 16, 16))
        initial_set_of_positions1.add((17, 17, 17))
        initial_set_of_positions2 = set()
        initial_set_of_positions2.add((16, 16, 16))
        initial_set_of_positions2.add((17, 17, 17))
        initial_set_of_positions3 = set()
        initial_set_of_positions3.add((16, 16, 16))
        initial_set_of_positions3.add((17, 17, 17))
        initial_group0 = {
            1: initial_set_of_positions0,
            100: initial_set_of_positions1,
        }
        initial_group1 = {
            1: initial_set_of_positions2,
            100: initial_set_of_positions3,
        }
        initial_controller = {
            (16, 16, 16): initial_group0,
            (17, 17, 17): initial_group1,
        }
        self.object._controller_position_to_block_id_to_block_positions = initial_controller

        expected_controller = dict()
        smd = Smd()
        self.object.update(smd)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

    def test_update_link(self):
        initial_set_of_positions0 = set()
        initial_set_of_positions0.add((16, 16, 16))
        initial_set_of_positions0.add((17, 17, 17))
        initial_set_of_positions1 = set()
        initial_set_of_positions1.add((16, 16, 16))
        initial_set_of_positions1.add((17, 17, 17))
        initial_set_of_positions2 = set()
        initial_set_of_positions2.add((16, 16, 16))
        initial_set_of_positions2.add((17, 17, 17))
        initial_set_of_positions3 = set()
        initial_set_of_positions3.add((16, 16, 16))
        initial_set_of_positions3.add((17, 17, 17))
        initial_group0 = {
            1: initial_set_of_positions0,
            100: initial_set_of_positions1,
        }
        initial_group1 = {
            1: initial_set_of_positions2,
            100: initial_set_of_positions3,
        }
        initial_controller = {
            (16, 16, 16): initial_group0,
            (17, 17, 17): initial_group1,
        }
        self.object._controller_position_to_block_id_to_block_positions = initial_controller

        expected_set_of_positions = set()
        expected_set_of_positions.add((16, 16, 16))
        expected_set_of_positions.add((18, 18, 18))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (16, 16, 16): expected_group,
            (18, 18, 18): expected_group,
        }

        old_position = (17, 17, 17)
        new_position = (18, 18, 18)
        self.object.update_link(old_position, new_position)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

    def test_remove_all(self):
        initial_set_of_positions0 = set()
        initial_set_of_positions0.add((16, 16, 16))
        initial_set_of_positions0.add((17, 17, 17))
        initial_set_of_positions1 = set()
        initial_set_of_positions1.add((16, 16, 16))
        initial_set_of_positions1.add((17, 17, 17))
        initial_set_of_positions2 = set()
        initial_set_of_positions2.add((16, 16, 16))
        initial_set_of_positions2.add((17, 17, 17))
        initial_set_of_positions3 = set()
        initial_set_of_positions3.add((16, 16, 16))
        initial_set_of_positions3.add((17, 17, 17))
        initial_group0 = {
            1: initial_set_of_positions0,
            100: initial_set_of_positions1,
        }
        initial_group1 = {
            1: initial_set_of_positions2,
            100: initial_set_of_positions3,
        }
        initial_controller = {
            (16, 16, 16): initial_group0,
            (17, 17, 17): initial_group1,
        }
        self.object._controller_position_to_block_id_to_block_positions = initial_controller
        expected_controller = dict()
        self.object.remove_all()
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

    def test_set_type(self):
        self.assertRaises(AssertionError, self.object.set_type, 6)
        initial_set_of_positions0 = set()
        initial_set_of_positions0.add((16, 16, 16))
        initial_set_of_positions0.add((17, 17, 17))
        initial_set_of_positions1 = set()
        initial_set_of_positions1.add((16, 16, 16))
        initial_set_of_positions1.add((17, 17, 17))
        initial_set_of_positions2 = set()
        initial_set_of_positions2.add((16, 16, 16))
        initial_set_of_positions2.add((17, 17, 17))
        initial_set_of_positions3 = set()
        initial_set_of_positions3.add((16, 16, 16))
        initial_set_of_positions3.add((17, 17, 17))
        initial_group0 = {
            1: initial_set_of_positions0,
            100: initial_set_of_positions1,
        }
        initial_group1 = {
            1: initial_set_of_positions2,
            100: initial_set_of_positions3,
        }
        initial_controller = {
            (16, 16, 16): initial_group0,
            (17, 17, 17): initial_group1,
        }

        # X to Ship
        expected_set_of_positions = set()
        expected_set_of_positions.add((16, 16, 16))
        expected_set_of_positions.add((17, 17, 17))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (16, 16, 16): expected_group,
            (17, 17, 17): expected_group,
        }
        self.object._controller_position_to_block_id_to_block_positions = initial_controller
        self.object.set_type(0)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)

        # Ship to Station
        expected_set_of_positions = set()
        expected_set_of_positions.add((17, 17, 17))
        expected_group = {
            1: expected_set_of_positions,
            100: expected_set_of_positions,
        }
        expected_controller = {
            (17, 17, 17): expected_group,
        }
        self.object.set_type(2)
        self.assertDictEqual(expected_controller, self.object._controller_position_to_block_id_to_block_positions)
