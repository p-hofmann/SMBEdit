from unittest import TestCase
from io import BytesIO
from lib.smblueprint.meta.meta import Meta
from lib.bits_and_bytes import BinaryStream
from unittests.blueprints import blueprint_handler
from lib.smblueprint.meta.tag.aiconfig import AIConfig
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
            self.object.read(directory_blueprint)
            self.object.move_center_by_vector((2, 5, 6))

    def test_datatype_5(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            if not self.object._data_type_5.has_data():
                continue
            tag_stream_original = BytesIO()
            tag_stream_return = BytesIO()
            tag_object = AIConfig()
            tag_object.from_tag(self.object._data_type_5._tag_data.get_root_tag())
            self.object._data_type_5._tag_data.get_root_tag().write(BinaryStream(tag_stream_original))
            tag_object.to_tag().write(BinaryStream(tag_stream_return))
            tag_stream_original.seek(0)
            tag_stream_return.seek(0)
            self.assertEqual(tag_stream_original.getvalue(), tag_stream_return.getvalue())

    def test_datatype_4(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            for docker in self.object._data_type_4:
                tag_object = RailDockedEntityLinks()
                tag_object.from_tag(docker.get_root_tag(), self.object._version[3])
                tag_stream_original = BytesIO()
                tag_stream_return = BytesIO()
                docker.get_root_tag().write(BinaryStream(tag_stream_original))
                # docker.get_root_tag().to_stream()
                tag_object.to_tag(self.object._version[3]).write(BinaryStream(tag_stream_return))
                tag_stream_original.seek(0)
                tag_stream_return.seek(0)
                if self.object._version[3] < max(self.object._valid_versions)[3]:
                    self.assertEqual(tag_stream_original.getvalue(), tag_stream_return.getvalue())
                else:
                    self.assertNotEqual(tag_stream_original.getvalue(), tag_stream_return.getvalue())
