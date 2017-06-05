__author__ = 'Peter Hofmann'


import sys

from smbedit.lib.utils.vector import Vector
from ..tagmanager import TagPayload, TagList


class LogicTriggerPositions(object):
    """

    @type _positions: list[int]
    """

    def __init__(self):
        self._positions = []

    def from_tag(self, tag_payload):
        """
        -13: {-4: 281479272661011, -4: 1475274596470, }
        @type tag_payload: TagPayload
        """
        self._positions = []
        assert tag_payload.id == -13, tag_payload.id
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        if len(list_of_tag_payloads) == 0:
            return
        for tag_payload_position in list_of_tag_payloads:
            assert tag_payload_position.id == -4, tag_payload_position.id
            self._positions.append(tag_payload_position.payload)

    def to_tag(self):
        """
             //     10101001011110101011011110111010101101011
             //     10100011111110101000000010001110110110111
            -13: {-4: 281479272661011, -4: 1475274596470, }

        @rtype: TagPayload
        """
        link = TagList()
        for position in self._positions:
            link.add(TagPayload(-4, None, position))
        return TagPayload(-13, None, link)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for position in self._positions:
            output_stream.write("{}\n".format(Vector.get_position(position)))


class LogicTriggerTimeStamp(object):
    """

    @type _position_0: int
    @type _timestamp: int
    """

    def __init__(self):
        self._position_0 = 0
        self._timestamp = 0

    def from_tag(self, tag_payload):
        """
        -13: {-4: 281479272661011, -4: 1475274596470, }
        @type tag_payload: TagPayload
        """
        assert tag_payload.id == -13, tag_payload.id
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        assert list_of_tag_payloads[0].id == -4, list_of_tag_payloads[0].id
        assert list_of_tag_payloads[1].id == -4, list_of_tag_payloads[1].id
        self._position_0 = list_of_tag_payloads[0].payload
        self._timestamp = list_of_tag_payloads[1].payload

    def to_tag(self):
        """
             //     10101001011110101011011110111010101101011
             //     10100011111110101000000010001110110110111
            -13: {-4: 281479272661011, -4: 1475274596470, }

        @rtype: TagPayload
        """
        link = TagList()
        link.add(TagPayload(-4, None, self._position_0))
        link.add(TagPayload(-4, None, self._timestamp))
        return TagPayload(-13, None, link)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        import datetime
        output_stream.write("{} - {}\n".format(
            Vector.get_position(self._position_0),
            # self._position_1
            datetime.datetime.fromtimestamp(self._timestamp/1000.0).strftime('%Y-%m-%d %H:%M:%S')
            # Vector.get_position(self._position_1)
        ))


class LogicTriggerTimeStamps(object):
    """

    @type _links: list[LogicTriggerTimeStamp]
    """

    def __init__(self, label="Unknown5"):
        self._links = []
        self._label = label

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -13: {-4: 281479272661011, -4: 1475274596470, }
        }
        @type tag_payload: TagPayload
        """
        assert tag_payload.id == -13, tag_payload.id
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        for tag_payload_link in list_of_tag_payloads:
            link = LogicTriggerTimeStamp()
            link.from_tag(tag_payload_link)
            self._links.append(link)

    def to_tag(self):
        """
        -13:
        {
             //     10101001011110101011011110111010101101011
                    10100011111110101000000010001110110110111
            -13: {-4: 281479272661011, -4: 1475274596470, }
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        for link in self._links:
            tag_list.add(link.to_tag())
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}:\n".format(self._label))
        for link in self._links:
            link.to_stream(output_stream)


class LogicTrigger(object):
    """

    @type _unknown_list_0: LogicTriggerPositions
    @type _unknown_list_1: LogicTriggerTimeStamps
    @type _unknown_list_2: LogicTriggerTimeStamps
    """

    def __init__(self):
        self._label = 'a'
        self._unknown_list_0 = LogicTriggerPositions()
        self._unknown_list_1 = LogicTriggerTimeStamps()
        self._unknown_list_2 = LogicTriggerTimeStamps()

    def from_tag(self, tag_payload):
        """
        13: 'a'
        {
            -13: {}
            -13: {} // Buttons
            -13: {}
        }

        @type tag_payload: TagPayload
        """
        self._unknown_list_0 = LogicTriggerPositions()
        self._unknown_list_1 = LogicTriggerTimeStamps("U5_1")
        self._unknown_list_2 = LogicTriggerTimeStamps("U5_2")
        assert tag_payload.id == 13, (tag_payload.id, tag_payload.name)
        assert tag_payload.name == self._label, tag_payload.name
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        assert list_of_tag_payloads[0].id == -13
        assert list_of_tag_payloads[1].id == -13
        assert list_of_tag_payloads[2].id == -13
        self._unknown_list_0.from_tag(list_of_tag_payloads[0])
        self._unknown_list_1.from_tag(list_of_tag_payloads[1])
        self._unknown_list_2.from_tag(list_of_tag_payloads[2])

    def to_tag(self):
        """
        13: 'a'
        {
            -13: {} -13: {} -13: {}
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        tag_list.add(self._unknown_list_0.to_tag())
        tag_list.add(self._unknown_list_1.to_tag())
        tag_list.add(self._unknown_list_2.to_tag())
        return TagPayload(13, self._label, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Unknown5:\n")
        self._unknown_list_0.to_stream(output_stream)
        self._unknown_list_1.to_stream(output_stream)
        self._unknown_list_2.to_stream(output_stream)
