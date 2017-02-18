# import os
from io import BytesIO
from unittest import TestCase

from unittests.blueprints import blueprint_handler
from lib.smblueprint.meta.meta import Meta
from lib.binarystream import BinaryStream
from lib.utils.vector import Vector
from lib.smblueprint.meta.tag.datatype2.aiconfig import AIConfig
from lib.smblueprint.meta.tag.raildockentitylinks import RailDockedEntityLinks

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: Meta
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprints = blueprint_handler

    def setUp(self):
        # block_config.from_hard_coded()
        self.object = Meta()

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestMeta(DefaultSetup):
    def test_read_file(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)

    def test__write_dummy(self):
        input_stream = BinaryStream(BytesIO())
        self.object._write_dummy(input_stream)

    def test__write_file(self):
        input_stream = BinaryStream(BytesIO())
        self.object._write_file(input_stream, "./")

    def test_move_center_by_vector(self):
        for directory_blueprint in self._blueprints:
            # print(directory_blueprint, self.object._version[3])
            self.object.read(directory_blueprint)
            self.object.move_center_by_vector((2, 5, 6))

    def test_datatype_7(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            # print(directory_blueprint, self.object._version[3])
            # if not self.object._data_type_7.has_data():
            #     continue
            # for key, value in self.object._data_type_7._data.items():
            #     position = Vector.get_pos(key)
            #     # print(position, value)

    def test_datatype_6(self):
        for directory_blueprint in self._blueprints._blueprint_attachments:
            # print("\n\n", directory_blueprint, self.object._version[3])
            self.object.read(directory_blueprint)
            # for index, rail_entry in self.object._data_type_6._data.items():
            #     rail_entry.to_stream()

    def test_datatype_5(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            if not self.object._data_type_5.has_data():
                continue
            # print("\n\n", directory_blueprint, self.object._version[3])
            tag_stream_original = BytesIO()
            tag_stream_return = BytesIO()
            tag_object = AIConfig()
            tag_object.from_tag(self.object._data_type_5._tag_data.get_root_tag())
            self.object._data_type_5._tag_data.get_root_tag().write(BinaryStream(tag_stream_original))
            tag_object.to_tag().write(BinaryStream(tag_stream_return))
            tag_stream_original.seek(0)
            tag_stream_return.seek(0)
            self.assertEqual(tag_stream_original.getvalue(), tag_stream_return.getvalue(), directory_blueprint)

    def test_datatype_4(self):
        for directory_blueprint in self._blueprints:
            # print("\n\n", directory_blueprint)
            self.object.read(directory_blueprint)
            for docker in self.object._data_type_4:
                tag_object = RailDockedEntityLinks()
                tag_object.from_tag(docker.get_root_tag(), self.object._version)
                tag_stream_original = BytesIO()
                tag_stream_return = BytesIO()
                docker.get_root_tag().write(BinaryStream(tag_stream_original))
                # print("\n\n", directory_blueprint, self.object._version[3])
                # docker.get_root_tag().to_stream()
                # tag_object.to_tag(self.object._version[3]).to_stream()
                # tag_object.to_stream()
                tag_object.to_tag(self.object._version).write(BinaryStream(tag_stream_return))
                tag_stream_original.seek(0)
                tag_stream_return.seek(0)
                self.assertEqual(tag_stream_original.getvalue(), tag_stream_return.getvalue(), directory_blueprint)
            for key, value in self.object._data_type_4._entity_wireless_logic_stuff.items():
                unknown_string, unknown_position_index_0, unknown_position_index_1 = value
                for position_index in {unknown_position_index_0, unknown_position_index_1}:
                    position = Vector.get_position(position_index)
                    self.assertEqual(position_index, Vector.get_index(position))
        position = (-16, -10, -3)
        position_index = Vector.get_index(position)
        self.assertTupleEqual(position, Vector.get_position(position_index))
