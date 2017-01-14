__author__ = 'Peter Hofmann'

import sys

from lib.blueprint.meta.tag.tagmanager import TagPayload, TagList
from lib.blueprint.meta.tag.storage import StorageList
from lib.blueprint.meta.tag.aiconfig import AIConfig
from lib.blueprint.meta.tag.shop import Shop
from lib.blueprint.meta.tag.displaylist import DisplayList


class GateList(object):
    """
    Race gate tag

    @type _warp_gates: list[Gate]
    """

    def __init__(self):
        self._warp_gates = []

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -13:
        }
                // no data
        -1: 0

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        if tag_payload.id == -1:
            return
        assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        for tag_payload in list_of_tag_payloads:
            warp_gate = Gate()
            warp_gate.from_tag(tag_payload)
            self._warp_gates.append(warp_gate)

    def to_tag(self):
        """
        -13:
        {
            -13:
        }
                // no data
        -1: 0

        @rtype: TagPayload
        """
        if len(self._warp_gates) == 0:
            return TagPayload(-1, None, 0)
        tag_list = TagList()
        for warp_gate in self._warp_gates:
            tag_list.add(warp_gate.to_tag())
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        if len(self._warp_gates) == 0:
            output_stream.write("No Gates\n")
            return
        output_stream.write("Gates:\n")
        for warp_gate in self._warp_gates:
            warp_gate.to_stream(output_stream)


class Gate(object):
    """
    Race gate tag

    @type _unknown_byte: float
    @type _target_entity: str
    @type _position_source: tuple[int]
    """

    def __init__(self):
        self._unknown_byte = 1
        self._target_entity = "none"
        self._position_source = (0, 0, 0)
        self._position_destination = (0, 0, 0)

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -10: (15, 17, 16),
            -13:
            {
                -1: 1,
                -8: 'none',
                -10: (0, 0, 0),
            }
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        assert list_of_tag_payloads[0].id == -10
        self._position_source = list_of_tag_payloads[0].payload

        tag_payload = list_of_tag_payloads[1]
        assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        assert list_of_tag_payloads[0].id == -1, list_of_tag_payloads[0].id
        assert list_of_tag_payloads[1].id == -8
        assert list_of_tag_payloads[2].id == -10
        self._unknown_byte = list_of_tag_payloads[0].payload
        self._target_entity = list_of_tag_payloads[1].payload
        self._position_destination = list_of_tag_payloads[2].payload

    def to_tag(self):
        """
        -13:
        {
            -10: (15, 17, 16),
            -13:
            {
                -1: 1,
                -8: 'none',
                -10: (0, 0, 0),
            }
        }

        @rtype: TagPayload
        """
        tag_list_destination = TagList()
        tag_list_destination.add(TagPayload(-1, None, self._unknown_byte))
        tag_list_destination.add(TagPayload(-8, None, self._target_entity))
        tag_list_destination.add(TagPayload(-10, None, self._position_destination))

        tag_list = TagList()
        tag_list.add(TagPayload(-10, None, self._position_source))
        tag_list.add(TagPayload(-13, None, tag_list_destination))
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Local: {}\t".format(self._position_source))
        output_stream.write("'{}': {}\n".format(self._target_entity, self._position_destination))


class BlockList(object):
    """
    Handling BlockList tag structure

    @type _blocks: dict{int, int}
    """

    def __init__(self):
        self._blocks = dict()

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -13: {-2: 14, -3: 0, }
            -13: {-2: 113, -3: 0, }
            -13: {-2: 122, -3: 1121, }
            -13: {-2: 478, -3: 2854, }
            -13: {-2: 3, -3: 8500, }
            -13: {-2: 2, -3: 1695, }
            -13: {-2: 331, -3: 0, }
        }

        @type tag_payload: TagPayload
        """
        self._blocks = dict()
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == -13
        item_tag_list = tag_payload.payload
        assert isinstance(item_tag_list, TagList)
        list_of_tags = item_tag_list.get_list()

        for tag_payload in list_of_tags:
            assert isinstance(tag_payload, TagPayload)
            assert tag_payload.id == -13
            tag_list_block = tag_payload.payload
            assert isinstance(tag_list_block, TagList)
            list_of_tag_payloads = tag_list_block.get_list()
            assert list_of_tag_payloads[0].id == -2
            assert list_of_tag_payloads[1].id == -3
            self._blocks[list_of_tag_payloads[0].payload] = list_of_tag_payloads[1].payload

    def to_tag(self):
        """
        -13:
        {
            -13: {-2: 14, -3: 0, }
            -13: {-2: 113, -3: 0, }
            -13: {-2: 122, -3: 1121, }
            -13: {-2: 478, -3: 2854, }
            -13: {-2: 3, -3: 8500, }
            -13: {-2: 2, -3: 1695, }
            -13: {-2: 331, -3: 0, }
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        for block_id in self._blocks.keys():
            tag_list_block = TagList()
            tag_list_block.add(TagPayload(-2, None, block_id))
            tag_list_block.add(TagPayload(-3, None, self._blocks[block_id]))
            tag_list.add(TagPayload(-13, None, tag_list_block))
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("BlockList:\t")
        for block_id in self._blocks.keys():
            output_stream.write("{}: {}, ".format(block_id, self._blocks[block_id]))
        output_stream.write("\n")


class Unknown4Ship(object):
    """
    @type _unknown_long: int
    """

    def __init__(self):
        self._unknown_long = 0

    def from_tag(self, tag_payload):
        """
        -13: {-4: -9223372036854775808, }

        // old tag
        1: 'ex' 0

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        if tag_payload.id == 1:
            assert tag_payload.name == "ex", tag_payload.name
            # old tag
            return
        assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -4
        assert len(list_of_tags) == 1
        self._unknown_long = list_of_tags[0].payload

    def to_tag(self):
        """
        -13: {-4: -9223372036854775808, }

        @rtype: TagPayload
        """
        tag_list = TagList()
        tag_list.add(TagPayload(-4, None, self._unknown_long))
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\n".format(self._unknown_long))


class Unknown1(object):
    """
    @type _unknown_int: int
    """

    def __init__(self):
        self._label = "shipMan0"
        self._unknown_int = 0

    def from_tag(self, tag_payload):
        """
        3: 'shipMan0' 0,

        // old station
        13: 'shipMan0'
        {
            13: 'wepContr' {}
            13: 'wepContr' {}
        }
        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        if tag_payload.id == 13:
            # old tag, probably??
            return
        assert tag_payload.id == 3, (tag_payload.id, tag_payload.name)
        self._label = tag_payload.name
        self._unknown_int = tag_payload.payload

    def to_tag(self):
        """
        3: 'shipMan0' 0,

        @rtype: TagPayload
        """
        return TagPayload(3, self._label, self._unknown_int)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}: {}\n".format(self._label, self._unknown_int))


class Power(object):
    """
    Charged power, not maximum

    @type _power: float
    @type _power_auxiliary: float
    """

    def __init__(self):
        self._power = .0
        self._power_auxiliary = .0

    def from_tag(self, tag_payload):
        """
        -13: {-6: 50000.0, -6: 0.0, }

        // old tag:
        6: 'pw' 50000.0,

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        if tag_payload.id == 6:
            assert tag_payload.name == "pw", (tag_payload.id, tag_payload.name)
            # old tag
            self._power = tag_payload.payload
            return
        assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -6
        assert list_of_tags[1].id == -6
        self._power = list_of_tags[0].payload
        self._power_auxiliary = list_of_tags[1].payload

    def to_tag(self):
        """
        -13: {-6: 50000.0, -6: 0.0, }

        @rtype: TagPayload
        """
        tag_list = TagList()
        tag_list.add(TagPayload(-6, None, self._power))
        tag_list.add(TagPayload(-6, None, self._power_auxiliary))
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Power: {}\n".format(self._power))
        output_stream.write("Power Auxiliary: {}\n".format(self._power_auxiliary))


class Shield(object):
    """
    @type _shield: float
    """

    def __init__(self):
        self._label = "sh"
        self._shield = .0

    def from_tag(self, tag_payload):
        """
        6: 'sh' 1000.0,

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == 6, (tag_payload.id, tag_payload.name)
        self._label = tag_payload.name
        self._shield = tag_payload.payload

    def to_tag(self):
        """
        6: 'sh' 1000.0,

        @rtype: TagPayload
        """
        return TagPayload(6, self._label, self._shield)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Shield: {}\n".format(self._shield))


class Datatype2TagReader(object):
    """
    Handling datatype2 tag structure
    @type _label: str
    """

    def __init__(self):
        self._label = 'container'

        self._storage = StorageList()
        self._unknown_1 = Unknown1()
        self._power = Power()
        self._shield = Shield()
        self._shop = None
        self._unknown_5_tag = None
        self._displays = DisplayList()
        self._block_list = BlockList()
        self._warp_gates = GateList()
        self._unknown_9_tag = None
        self._ai_config = AIConfig()
        self._unknown_11_tag = None
        self._race_gate = GateList()
        self._unknown_13_tag = None
        self._unknown_14_tag = TagPayload()
        return

    def from_tag(self, tag_payload_root):
        """
        13: 'container'
        {
        0    -13: {}
        1    3: 'shipMan0' 0,
        2    -13: {-6: 50000.0, -6: 0.0, }
        3    6: 'sh' 1000.0,
        4    -13: {-4: -9223372036854775808, }  // not shop
        5    13: 'a' {-13: {}-13: {}-13: {}}
        6    -13: {}
        7    -13:
            {
                -13: {-2: 478, -3: 0, }-13: {-2: 3, -3: 0, }-13: {-2: 937, -3: 0, }-13: {-2: 8, -3: 12, }
                -13: {-2: 122, -3: 2, }
                -13: {-2: 22, -3: 0, }-13: {-2: 14, -3: 0, }-13: {-2: 15, -3: 0, }-13: {-2: 2, -3: 99, }
                -13: {-2: 671, -3: 0, }
                -13: {-2: 331, -3: 0, } -13: {-2: 978, -3: 0, }
            }
        8    -1: 0,
        9    -13:
            {
                13: 'ACD' {}
                13: 'TR' {}
                13: 'A' {}
                13: 'A' {}
                13: 'J' {}
                13: 'JP' {}
                13: 'SC' {}
            }
        10   13: 'AIConfig1' { -13: {-1: 1, -8: 'Turret', } -13: {-1: 2, -8: 'true', } -13: {-1: 0, -8: 'Any', }}
        11  -13:
            {
                -1: 0,
                -13:
                {
                    -13: {-1: 9, -4: 68720525328, }
                    -13: {-1: 5, -4: 68720525329, }
                    -13: {-1: 6, -4: 64425558033, }
                    -13: {-1: 3, -4: 68720525327, }
                    -13: {-1: 4, -4: 64425558031, }
                }
            }
        12  -1: 0,
        13  -13: {}
        14  -13: {}
        }


        @type tag_payload_root: TagPayload
        """
        assert isinstance(tag_payload_root, TagPayload), tag_payload_root
        tag_list = tag_payload_root.payload
        list_of_tag_payload = tag_list.get_list()
        for list_index, tag_payload in enumerate(list_of_tag_payload):
            if list_index == 0:
                self._storage.from_tag(tag_payload)
            elif list_index == 1:
                self._unknown_1.from_tag(tag_payload)
            elif list_index == 2:
                self._power.from_tag(tag_payload)
            elif list_index == 3:
                self._shield.from_tag(tag_payload)
            elif list_index == 4:
                if tag_payload.id == 13:
                    self._shop = Shop()
                    self._shop.from_tag(tag_payload)
                else:
                    self._shop = Unknown4Ship()

            elif list_index == 5:
                self._unknown_5_tag = tag_payload

            elif list_index == 6:
                self._displays.from_tag(tag_payload)

            elif list_index == 7:
                self._block_list.from_tag(tag_payload)
            elif list_index == 8:
                # self._warp_gates = tag_payload
                self._warp_gates.from_tag(tag_payload)

            elif list_index == 9:
                self._unknown_9_tag = tag_payload

            elif list_index == 10:
                self._ai_config.from_tag(tag_payload)

            elif list_index == 11:
                self._unknown_11_tag = tag_payload
            elif list_index == 12:
                self._race_gate.from_tag(tag_payload)

            elif list_index == 13:
                self._unknown_13_tag = tag_payload
            elif list_index == 14:
                self._unknown_14_tag = tag_payload

    def to_tag(self):
        """
        @rtype: TagPayload
        """
        return TagPayload(13, self._label, TagList())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        # self._storage.to_stream(output_stream)
        # self._unknown_1.to_stream(output_stream)
        # output_stream.write("\n")
        # self._power.to_stream(output_stream)
        # output_stream.write("\n")
        # self._shield.to_stream(output_stream)
        # output_stream.write("\n")
        # self._shop.to_stream(output_stream)
        if self._unknown_5_tag is None:
            return
        self._unknown_5_tag.to_stream(output_stream)
        output_stream.write("\n")
        # self._displays.to_stream(output_stream)
        # self._block_list.to_stream(output_stream)
        # output_stream.write("\n")
        if self._warp_gates is None:
            return
        # self._warp_gates.to_stream(output_stream)
        # output_stream.write("\n")
        if self._unknown_9_tag is None:
            return
        self._unknown_9_tag.to_stream(output_stream)
        output_stream.write("\n")
        # self._ai_config.to_stream(output_stream)
        if self._unknown_11_tag is None:
            return
        self._unknown_11_tag.to_stream(output_stream)
        output_stream.write("\n")
        if self._race_gate is None:
            return
        self._race_gate.to_stream(output_stream)
        output_stream.write("\n")
        if self._unknown_13_tag is None:
            return
        self._unknown_13_tag.to_stream(output_stream)
        output_stream.write("\n")
        if self._unknown_14_tag is None:
            return
        self._unknown_14_tag.to_stream(output_stream)
        output_stream.write("\n")
