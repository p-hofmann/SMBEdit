from unittest import TestCase

from smlib.smblueprint.meta.meta import Meta
from unittests.testinput import blueprint_handler
from smlib.smblueprint.meta.tag.datatype2tagreader import Datatype2TagReader

__author__ = 'Peter Hofmann'


# class DefaultSetup(TestCase):
class DefaultSetup(object):
    """
    @type object: Meta
    """

    def __init__(self, methodName='runTest'):
        # super(DefaultSetup, self).__init__(methodName)
        self.object = None
        self._blueprints = blueprint_handler

    def setUp(self):
        self.object = Meta()

    def tearDown(self):
        self.object = None


class TestDatatype2TagReader(DefaultSetup):
    def test_index_1(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            tag_object = Datatype2TagReader()
            if not self.object._data_type_2.has_data():
                continue
            # print(directory_blueprint)
            tag_object.from_tag(self.object._data_type_2._tag_data.get_root_tag())
            # tag_stream_original = BytesIO()
            # tag_stream_return = BytesIO()
            # self.object._data_type_2._tag_data.get_root_tag().to_stream()
            tag_object._unknown_1.to_stream()

    def test_index_4(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            tag_reader = Datatype2TagReader()
            if not self.object._data_type_2.has_data():
                continue
            # print(directory_blueprint)
            tag_reader.from_tag(self.object._data_type_2._tag_data.get_root_tag())
            # tag_stream_original = BytesIO()
            # tag_stream_return = BytesIO()
            self.object._data_type_4._debug = True
            self.object._data_type_4.to_stream()
            # tag_reader._unknown_5_tag.to_stream()

    def test_index_5(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            tag_reader = Datatype2TagReader()
            if not self.object._data_type_2.has_data():
                continue
            # print(directory_blueprint)
            tag_reader.from_tag(self.object._data_type_2._tag_data.get_root_tag())
            # tag_stream_original = BytesIO()
            # tag_stream_return = BytesIO()
            self.object._data_type_2._tag_data.get_root_tag().to_stream()
            # tag_reader._unknown_5_tag.to_stream()

    def test_index_9(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            tag_object = Datatype2TagReader()
            if not self.object._data_type_2.has_data():
                continue
            # print(directory_blueprint)
            tag_object.from_tag(self.object._data_type_2._tag_data.get_root_tag())
            # tag_stream_original = BytesIO()
            # tag_stream_return = BytesIO()
            # docker.get_root_tag().to_stream()
            tag_object._unknown_9_tag.to_stream()

    def test_index_11(self):
        for directory_blueprint in self._blueprints:
            self.object.read(directory_blueprint)
            tag_object = Datatype2TagReader()
            if not self.object._data_type_2.has_data():
                continue
            # print(directory_blueprint)
            tag_object.from_tag(self.object._data_type_2._tag_data.get_root_tag())
            # tag_stream_original = BytesIO()
            # tag_stream_return = BytesIO()
            # docker.get_root_tag().to_stream()
            tag_object._hot_bar.to_stream()
