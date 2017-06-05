import sys

from smlib.utils.vector import Vector
from ..tagmanager import TagPayload, TagList


class Display(object):
    """
    Handling displays tag structure

    @type _position: int
    @type _text: str
    """

    def __init__(self):
        self._position = None
        self._text = None

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -4: 141748600835,
            -8: ''
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[0].id == -4
        assert list_of_tags[1].id == -8
        self._position = list_of_tags[0].payload
        self._text = list_of_tags[1].payload

    def to_tag(self):
        """
        -13:
        {
            -4: 141748600835,
            -8: ''
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        tag_list.add(TagPayload(-4, None, self._position))
        tag_list.add(TagPayload(-8, None, self._text))
        return TagPayload(-13, None, tag_list)

    def move_position(self, vector_direction):
        """
        Move positions of rail docked entities

        @type vector_direction: (int, int, int)
        """
        self._position = Vector.shift_position_index(self._position, vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(Vector.get_position(self._position)))
        output_stream.write("{}\n".format(self._text.strip('\n')))


class DisplayList(object):
    """
    Handling displays tag structure

    @type _displays: list[Display]
    """

    def __init__(self):
        self._displays = []

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -13:    // Display
        }

        @type tag_payload: TagPayload
        """
        self._displays = []
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        for tag_payload in list_of_tags:
            display = Display()
            display.from_tag(tag_payload)
            self._displays.append(display)

    def to_tag(self):
        """
        -13:
        {
            -13:    // Display
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        for display in self._displays:
            tag_list.add(display.to_tag())
        return TagPayload(-13, None, tag_list)

    def move_positions(self, vector_direction):
        """
        Move positions of rail docked entities

        @type vector_direction: (int, int, int)
        """
        for display in self._displays:
            display.move_position(vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Displays: #{}\n".format(len(self._displays)))
        for display in self._displays:
            display.to_stream(output_stream)
