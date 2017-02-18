__author__ = 'Peter Hofmann'


import sys
from lib.utils.vector import Vector
from lib.smblueprint.meta.tag.tagmanager import TagPayload, TagList


class Hotbar(object):
    """

    @type _index11_position: HotbarItems
    """

    def __init__(self):
        self._unknown_byte = 0
        self._index11_position = HotbarItems()

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -1: 0,
            -13: {}
        }

        @type tag_payload: TagPayload
        """
        assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        assert list_of_tag_payloads[0].id == -1
        self._unknown_byte = list_of_tag_payloads[0].payload
        self._index11_position.from_tag(list_of_tag_payloads[1])

    def to_tag(self):
        """
        -13:
        {
            -1: 0,
            -13: {}
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        tag_list.add(TagPayload(-1, None, self._unknown_byte))
        tag_list.add(self._index11_position.to_tag())
        return TagPayload(-13, None, tag_list)

    def move_positions(self, vector_direction):
        """
        Move positions of rail docked entities

        @type vector_direction: (int, int, int)
        """
        self._index11_position.move_positions(vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        # output_stream.write("Unknown long values:\n")
        self._index11_position.to_stream(output_stream)


class HotbarItems(object):
    """


    @type _positions: dict[tuple]
    """

    def __init__(self):
        self._positions = {}

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -13: {-1: 9, -4: 68720525328, }
            -13: {-1: 5, -4: 68720525329, }
            -13: {-1: 6, -4: 64425558033, }
            -13: {-1: 3, -4: 68720525327, }
            -13: {-1: 4, -4: 64425558031, }
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        for tag_payload in list_of_tag_payloads:
            assert isinstance(tag_payload, TagPayload)
            assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
            tag_list = tag_payload.payload
            assert isinstance(tag_list, TagList)
            list_of_tag_payloads_long = tag_list.get_list()
            assert list_of_tag_payloads_long[0].id == -1
            assert list_of_tag_payloads_long[1].id == -4
            hot_bar_index = list_of_tag_payloads_long[0].payload
            long_value = list_of_tag_payloads_long[1].payload
            self._positions[hot_bar_index] = long_value

    def to_tag(self):
        """
        -13:
        {
            -13: {-1: 9, -4: 68720525328, }
            -13: {-1: 5, -4: 68720525329, }
            -13: {-1: 6, -4: 64425558033, }
            -13: {-1: 3, -4: 68720525327, }
            -13: {-1: 4, -4: 64425558031, }
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        for byte_value, long_value in self._positions.items():
            tag_list_longs = TagList()
            tag_list_longs.add(TagPayload(-1, None, byte_value))
            tag_list_longs.add(TagPayload(-4, None, long_value))
            tag_list.add(TagPayload(-13, None, tag_list_longs))
        return TagPayload(-13, None, tag_list)

    def move_positions(self, vector_direction):
        """
        Move positions of rail docked entities

        @type vector_direction: (int, int, int)
        """
        old_dict = self._positions
        self._positions = {}
        for byte_value, long_value in old_dict.items():
            self._positions[byte_value] = (byte_value, Vector.shift_position_index(long_value, vector_direction))

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for byte_value, long_value in self._positions.items():
            output_stream.write("{}: ".format(Vector.get_position(long_value)))
            output_stream.write("{}\n".format(byte_value))
            # output_stream.write("{}: {}\n".format(byte_value, long_value))
