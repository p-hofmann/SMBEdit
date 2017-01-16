__author__ = 'Peter Hofmann'

import sys

from lib.blueprint.meta.tag.tagmanager import TagPayload, TagList, TagPayloadList


class ItemGroup(object):
    """
    Handling ItemGroup tag structure

    @type _label: str
    @type _items: dict{int, int}
    """

    def __init__(self):
        self._label = ''
        self._items = dict()

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -8: 'advancedgreenarmor',
            -13:
            {
                -2: 268,
                -3: 30,
            }
            -13:
            {
                -2: 316,
                -3: 8,
            }
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        item_tag_list = tag_payload.payload
        assert isinstance(item_tag_list, TagList)
        list_of_tags = item_tag_list.get_list()

        for tag_item in list_of_tags:
            if abs(tag_item.id) == 8:
                self._label = tag_item.payload
                continue
            assert isinstance(tag_item, TagPayload)
            assert abs(tag_item.id) == 13
            tag_item_list = tag_item.payload
            assert isinstance(tag_item_list, TagList)
            list_of_itrm_tags = tag_item_list.get_list()
            assert abs(list_of_itrm_tags[0].id) == 2
            assert abs(list_of_itrm_tags[1].id) == 3
            self._items[list_of_itrm_tags[0].payload] = list_of_itrm_tags[1].payload

    def to_tag(self):
        """
        -13:
        {
            -8: 'advancedgreenarmor',
            -13:
            {
                -2: 268,
                -3: 30,
            }
            -13:
            {
                -2: 316,
                -3: 8,
            }
        }

        @rtype: TagPayload
        """
        tag_list_storage = TagList()
        tag_list_storage.add(TagPayload(-8, None, self._label))
        for block_id in self._items.keys():
            tag_list_item = TagList()
            tag_list_item.add(TagPayload(-2, None, block_id))
            tag_list_item.add(TagPayload(-3, None, self._items[block_id]))
            tag_list_storage.add(TagPayload(-13, None, tag_list_item))
        return TagPayload(-13, None, tag_list_storage)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._label))
        for block_id in self._items.keys():
            output_stream.write("{}: {}, ".format(block_id, self._items[block_id]))
        output_stream.write("\n")


class ItemLogbook(object):
    """
    @type _log_entry: str
    """

    def __init__(self):
        self._log_entry = "Personal Logbook"

    def from_tag(self, tag_payload):
        """
        -8: 'Personal Logbook'

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 8
        self._log_entry = tag_payload.payload

    def to_tag(self):
        """
        -8: 'Personal Logbook'

        @rtype: TagPayload
        """
        return TagPayload(-8, None, self._log_entry)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Log: '{}'\n".format(self._log_entry))


class ItemHelmet(object):
    """
    @type _unknown_byte: int
    """

    def __init__(self):
        self._unknown_byte = 0

    def from_tag(self, tag_payload):
        """
        -1: 0,

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 1
        self._unknown_byte = tag_payload.payload

    def to_tag(self):
        """
        -1: 0,

        @rtype: TagPayload
        """
        return TagPayload(-1, None, self._unknown_byte)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\n".format(self._unknown_byte))


class ItemTransporterMarker(object):
    """
    @type _mark_0: str
    @type _mark_1: str
    @type _unknown_long: int
    @type _unknown_float: float
    """

    def __init__(self):
        self._mark_0 = "unmarked"
        self._mark_1 = "unmarked"
        self._unknown_long = 0
        self._unknown_float = .0

    def from_tag(self, tag_payload):
        """
    -13: "Transporter Marker"
    {
        -8: 'unmarked',
        -8: 'unmarked',
        -4: -9223372036854775808,
        -5: 1.39999997616,
    }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -8
        assert list_of_tags[1].id == -8
        assert list_of_tags[2].id == -4
        assert list_of_tags[3].id == -5
        self._mark_0 = list_of_tags[0].payload
        self._mark_1 = list_of_tags[1].payload
        self._unknown_long = list_of_tags[2].payload
        self._unknown_float = list_of_tags[3].payload

    def to_tag(self):
        """
    -13: "Transporter Marker"
    {
        -8: 'unmarked',
        -8: 'unmarked',
        -4: -9223372036854775808,
        -5: 1.39999997616,
    }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-8, None, self._mark_0))
        taglist_item.add(TagPayload(-8, None, self._mark_1))
        taglist_item.add(TagPayload(-4, None, self._unknown_long))
        taglist_item.add(TagPayload(-5, None, self._unknown_float))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("'{}'\t".format(self._mark_0))
        output_stream.write("'{}'\t".format(self._mark_1))
        output_stream.write("{}\t".format(self._unknown_long))
        output_stream.write("{}\n".format(self._unknown_float))


class ItemMarkerBeam(object):
    """
    @type _marked_entity_0: str
    @type _marked_entity_1: str
    @type _unknown_long: int
    """

    def __init__(self):
        self._marked_entity_0 = "unmarked"
        self._marked_entity_1 = "unmarked"
        self._unknown_long = 0

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -8: 'unmarked',
            -8: 'unmarked',
            -4: -9223372036854775808,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -8
        assert list_of_tags[1].id == -8
        assert list_of_tags[2].id == -4
        self._marked_entity_0 = list_of_tags[0].payload
        self._marked_entity_1 = list_of_tags[1].payload
        self._unknown_long = list_of_tags[2].payload

    def to_tag(self):
        """
        -13:
        {
            -8: 'unmarked',
            -8: 'unmarked',
            -4: -9223372036854775808,
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-8, None, self._marked_entity_0))
        taglist_item.add(TagPayload(-8, None, self._marked_entity_1))
        taglist_item.add(TagPayload(-4, None, self._unknown_long))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("'{}'\t".format(self._marked_entity_0))
        output_stream.write("'{}'\t".format(self._marked_entity_1))
        output_stream.write("{}\n".format(self._unknown_long))


class ItemGrapple(object):
    """
    @type _unknown_float_0: float
    @type _unknown_vector_float_x4: tuple[float]
    @type _unknown_float_1: float
    """

    def __init__(self):
        self._unknown_float_0 = 0
        self._unknown_vector_float_x4 = 0
        self._unknown_float_1 = 0

    def from_tag(self, tag_payload):
        """
        -13: "Grapple"
        {
            -5: 50.0,
            -15: (1.0, 1.0, 0.7940500974655151, 1.0),
            -5: 150.0,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -5
        assert list_of_tags[1].id == -15
        assert list_of_tags[2].id == -5
        self._unknown_float_0 = list_of_tags[0].payload
        self._unknown_vector_float_x4 = list_of_tags[1].payload
        self._unknown_float_1 = list_of_tags[2].payload

    def to_tag(self):
        """
        -13: "Grapple"
        {
            -5: 50.0,
            -15: (1.0, 1.0, 0.7940500974655151, 1.0),
            -5: 150.0,
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-5, None, self._unknown_float_0))
        taglist_item.add(TagPayload(-15, None, self._unknown_vector_float_x4))
        taglist_item.add(TagPayload(-5, None, self._unknown_float_1))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_float_0))
        output_stream.write("{}\t".format(self._unknown_vector_float_x4))
        output_stream.write("{}\n".format(self._unknown_float_1))


class ItemSniperRifle(object):
    """
    @type _unknown_int32_0: int
    @type _unknown_float_0: float
    @type _unknown_float_1: float
    @type _unknown_vector_float_x4: tuple[float]
    @type _unknown_float_2: float
    """

    def __init__(self):
        self._unknown_int32_0 = 0
        self._unknown_float_0 = 0
        self._unknown_float_1 = 0
        self._unknown_vector_float_x4 = 0
        self._unknown_float_2 = 0

    def from_tag(self, tag_payload):
        """
        -13: "Sniper Rifle"
        {
            -3: 100,
            -5: 70.0,
            -5: 5.0,
            -15: (0.11056612432003021, 0.6573101282119751, 0.5764869451522827, 1.0),
            -5: 400.0,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -3
        assert list_of_tags[1].id == -5
        assert list_of_tags[2].id == -5
        assert list_of_tags[3].id == -15
        assert list_of_tags[4].id == -5
        self._unknown_int32_0 = list_of_tags[0].payload
        self._unknown_float_0 = list_of_tags[1].payload
        self._unknown_float_1 = list_of_tags[2].payload
        self._unknown_vector_float_x4 = list_of_tags[3].payload
        self._unknown_float_2 = list_of_tags[4].payload

    def to_tag(self):
        """
        -13: "Sniper Rifle"
        {
            -3: 100,
            -5: 70.0,
            -5: 5.0,
            -15: (0.11056612432003021, 0.6573101282119751, 0.5764869451522827, 1.0),
            -5: 400.0,
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-3, None, self._unknown_int32_0))
        taglist_item.add(TagPayload(-5, None, self._unknown_float_0))
        taglist_item.add(TagPayload(-5, None, self._unknown_float_1))
        taglist_item.add(TagPayload(-15, None, self._unknown_vector_float_x4))
        taglist_item.add(TagPayload(-5, None, self._unknown_float_2))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_int32_0))
        output_stream.write("{}\t".format(self._unknown_float_0))
        output_stream.write("{}\t".format(self._unknown_float_1))
        output_stream.write("{}\t".format(self._unknown_vector_float_x4))
        output_stream.write("{}\n".format(self._unknown_float_2))


class ItemRocketLauncher(object):
    """
    @type _unknown_int32_0: int
    @type _unknown_float_0: float
    @type _unknown_int32_1: int
    @type _unknown_vector_float_x4: tuple[float]
    @type _unknown_float_1: float
    @type _unknown_float_2: float
    """

    def __init__(self):
        self._unknown_int32_0 = 0
        self._unknown_float_0 = 0
        self._unknown_int32_1 = 0
        self._unknown_vector_float_x4 = 0
        self._unknown_float_1 = 0
        self._unknown_float_2 = 0

    def from_tag(self, tag_payload):
        """
        -13: "Rocket Launcher"
        {
            -3: 200,
            -5: 30.0,
            -3: 13000,
            -15: (1.0, 0.8890293836593628, 0.48737263679504395, 1.0),
            -5: 7.5,
            -5: 300.0,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -3
        assert list_of_tags[1].id == -5
        assert list_of_tags[2].id == -3
        assert list_of_tags[3].id == -15
        assert list_of_tags[4].id == -5
        assert list_of_tags[5].id == -5
        self._unknown_int32_0 = list_of_tags[0].payload
        self._unknown_float_0 = list_of_tags[1].payload
        self._unknown_int32_1 = list_of_tags[2].payload
        self._unknown_vector_float_x4 = list_of_tags[3].payload
        self._unknown_float_1 = list_of_tags[4].payload
        self._unknown_float_2 = list_of_tags[5].payload

    def to_tag(self):
        """
        -13: "Rocket Launcher"
        {
            -3: 200,
            -5: 30.0,
            -3: 13000,
            -15: (1.0, 0.8890293836593628, 0.48737263679504395, 1.0),
            -5: 7.5,
            -5: 300.0,
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-3, None, self._unknown_int32_0))
        taglist_item.add(TagPayload(-5, None, self._unknown_float_0))
        taglist_item.add(TagPayload(-3, None, self._unknown_int32_1))
        taglist_item.add(TagPayload(-15, None, self._unknown_vector_float_x4))
        taglist_item.add(TagPayload(-5, None, self._unknown_float_1))
        taglist_item.add(TagPayload(-5, None, self._unknown_float_2))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_int32_0))
        output_stream.write("{}\t".format(self._unknown_float_0))
        output_stream.write("{}\t".format(self._unknown_int32_1))
        output_stream.write("{}\t".format(self._unknown_vector_float_x4))
        output_stream.write("{}\t".format(self._unknown_float_1))
        output_stream.write("{}\n".format(self._unknown_float_2))


class ItemHandHeld(object):
    """
    @type _unknown_int32_0: int
    @type _unknown_float: float
    @type _unknown_int32_1: int
    @type _unknown_vector_float_x4: tuple[float]
    """

    def __init__(self):
        self._unknown_int32_0 = 0
        self._unknown_float = 0
        self._unknown_int32_1 = 0
        self._unknown_vector_float_x4 = 0

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -3: 10,
            -5: 80.0,
            -3: 150,
            -15: (1.0, 0.9553626179695129, 1.0, 1.0),
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -3
        assert list_of_tags[1].id == -5
        assert list_of_tags[2].id == -3
        assert list_of_tags[3].id == -15
        self._unknown_int32_0 = list_of_tags[0].payload
        self._unknown_float = list_of_tags[1].payload
        self._unknown_int32_1 = list_of_tags[2].payload
        self._unknown_vector_float_x4 = list_of_tags[3].payload

    def to_tag(self):
        """
        -13:
        {
            -3: 10,
            -5: 80.0,
            -3: 150,
            -15: (1.0, 0.9553626179695129, 1.0, 1.0),
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-3, None, self._unknown_int32_0))
        taglist_item.add(TagPayload(-5, None, self._unknown_float))
        taglist_item.add(TagPayload(-3, None, self._unknown_int32_1))
        taglist_item.add(TagPayload(-15, None, self._unknown_vector_float_x4))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_int32_0))
        output_stream.write("{}\t".format(self._unknown_float))
        output_stream.write("{}\t".format(self._unknown_int32_1))
        output_stream.write("{}\n".format(self._unknown_vector_float_x4))


class ItemTorch(object):
    """
    @type _unknown_vector_float_x4: tuple[float]
    @type _unknown_byte: int
    """

    def __init__(self):
        self._unknown_vector_float_x4 = 0
        self._unknown_byte = 0

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -15: (1.0, 1.0, 1.0, 1.0),
            -1: 0,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -15
        assert list_of_tags[1].id == -1
        self._unknown_vector_float_x4 = list_of_tags[0].payload
        self._unknown_byte = list_of_tags[1].payload

    def to_tag(self):
        """
        -13:
        {
            -15: (1.0, 1.0, 1.0, 1.0),
            -1: 0,
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-15, None, self._unknown_vector_float_x4))
        taglist_item.add(TagPayload(-1, None, self._unknown_byte))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_vector_float_x4))
        output_stream.write("{}\n".format(self._unknown_byte))


class ItemBuildProhibiter(object):
    """
    @type _unknown_float: tuple[float]
    @type _unknown_byte: int
    """

    def __init__(self):
        self._unknown_float = 0
        self._unknown_byte = 0

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -5: 32.0,
            -1: 0,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -5
        assert list_of_tags[1].id == -1
        self._unknown_float = list_of_tags[0].payload
        self._unknown_byte = list_of_tags[1].payload

    def to_tag(self):
        """
        -13:
        {
            -5: 32.0,
            -1: 0,
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-5, None, self._unknown_float))
        taglist_item.add(TagPayload(-1, None, self._unknown_byte))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_float))
        output_stream.write("{}\n".format(self._unknown_byte))


class ItemBlockStorage(object):
    """
    @type _unknown_byte_array: list[int]
    """

    def __init__(self):
        self._unknown_byte_array = 0

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -7: [0, 0, 0, 0]
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        assert list_of_tags[0].id == -7
        self._unknown_byte_array = list_of_tags[0].payload

    def to_tag(self):
        """
        -13:
        {
            -7: [0, 0, 0, 0]
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-7, None, self._unknown_byte_array))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\n".format(self._unknown_byte_array))


class ItemDesign(object):
    """
    @type _label_entity: str
    @type _label_design: str
    """

    def __init__(self):
        self._label_entity = ''
        self._label_design = ''

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -8: 'ENTITY_SHIP_Mining_Drone_1',
            -8: 'Heavy_Mining_Drone_AM',
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[0].id == -8
        assert list_of_tags[1].id == -8
        self._label_entity = list_of_tags[0].payload
        self._label_design = list_of_tags[1].payload

    def to_tag(self):
        """
        -13:
        {
            -8: 'ENTITY_SHIP_Mining_Drone_1',
            -8: 'Heavy_Mining_Drone_AM',
        }

        @rtype: TagPayload
        """
        tag_list_item = TagList()
        tag_list_item.add(TagPayload(-8, None, self._label_entity))
        tag_list_item.add(TagPayload(-8, None, self._label_design))
        return TagPayload(-13, None, tag_list_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._label_entity))
        output_stream.write("{}\n".format(self._label_design))


class ItemBlueprint(object):
    """
    @type _unknown_byte_array_0: list[int]
    @type _unknown_byte_array_1: list[int]
    @type _label: str
    """

    def __init__(self):
        self._unknown_int32 = 0
        self._item_id = -9
        self._unknown_byte_array_0 = []
        self._unknown_byte_array_1 = []
        self._label = ''
        self._unknown_int16 = -1

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -7: [0, 0, 0, 83, 0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 15, 48, 0, 3, 0, 0, 5, 21, 0, 4, 0, 0, 0, 1, 0, 6, 0, 0]
            -7: [0, 0, 0, 0],
            -8: 'Some Ship',
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[0].id == -7
        assert list_of_tags[1].id == -7
        assert list_of_tags[2].id == -8
        self._unknown_byte_array_0 = list_of_tags[0].payload
        self._unknown_byte_array_1 = list_of_tags[1].payload
        self._label = list_of_tags[2].payload

    def to_tag(self):
        """
        -13:
        {
            -7: [0, 0, 0, 83, 0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 15, 48, 0, 3, 0, 0, 5, 21, 0, 4, 0, 0, 0, 1, 0, 6]
            -7: [0, 0, 0, 0],
            -8: 'Some_Ship',
        }

        @rtype: TagPayload
        """
        taglist_item = TagList()
        taglist_item.add(TagPayload(-7, None, self._unknown_byte_array_0))
        taglist_item.add(TagPayload(-7, None, self._unknown_byte_array_1))
        taglist_item.add(TagPayload(-8, None, self._label))
        return TagPayload(-13, None, taglist_item)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_int32))
        output_stream.write("{}\t".format(self._unknown_int16))
        output_stream.write("{}\t".format(self._label))


class ItemSpecial(object):
    """
    @type _unknown_int32: int
    @type _item_id: int
    @type _item: ItemBlueprint|ItemDesign
    @type _item_type: int
    """

    _item_ids = {
        -9: "Blueprint",
        # ?? -10: "Recipe",
        -11: "Logbook",
        -12: "Helmet",
        -13: "Build Prohibiter",
        -14: "Torch",
        -15: "Design",
        -16: "Block Storage",
        -32: "Weapon",
    }

    _item_types = {
        1: "Laser",
        2: "Healing Beam",
        3: "Power Supply Beam",
        4: "Marker Beam",
        5: "Rocket Launcher",
        6: "Sniper Rifle",
        7: "Grapple",
        9: "Transporter Marker"
    }

    def __init__(self):
        self._unknown_int32 = 0
        self._item_id = 0
        self._item = None
        self._item_type = -1

    def from_tag(self, tag_payload):
        """
        -13:
        {
             -3: 158460,
             -2: -32,
            -13: // item
            -2: 1,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[0].id == -3
        assert list_of_tags[1].id == -2
        assert list_of_tags[3].id == -2
        self._unknown_int32 = list_of_tags[0].payload
        self._item_id = list_of_tags[1].payload
        assert self._item_id in ItemSpecial._item_ids, "Unkown item id: {}".format(self._item_id)
        self._item_type = list_of_tags[3].payload

        tag_payload = list_of_tags[2]
        if self._item_id == -9:
            self._item = ItemBlueprint()
            self._item.from_tag(tag_payload)
        elif self._item_id == -11:
            self._item = ItemLogbook()
            self._item.from_tag(tag_payload)
        elif self._item_id == -12:
            self._item = ItemHelmet()
            self._item.from_tag(tag_payload)
        elif self._item_id == -13:
            self._item = ItemBuildProhibiter()
            self._item.from_tag(tag_payload)
        elif self._item_id == -14:
            self._item = ItemTorch()
            self._item.from_tag(tag_payload)
        elif self._item_id == -15:
            self._item = ItemDesign()
            self._item.from_tag(tag_payload)
        elif self._item_id == -16:
            self._item = ItemBlockStorage()
            self._item.from_tag(tag_payload)
        elif self._item_id == -32:
            if self._item_type not in self._item_types:
                raise NotImplementedError("Unknown item type: {}".format(self._item_type))
            if 0 < self._item_type < 4:
                self._item = ItemHandHeld()
            elif self._item_type == 4:
                self._item = ItemMarkerBeam()
            elif self._item_type == 5:
                self._item = ItemRocketLauncher()
            elif self._item_type == 6:
                self._item = ItemSniperRifle()
            elif self._item_type == 7:
                self._item = ItemGrapple()
            elif self._item_type == 9:
                self._item = ItemTransporterMarker()
            else:
                raise NotImplementedError("Unknown item type: {}".format(self._item_type))
            self._item.from_tag(tag_payload)
        else:
            raise NotImplementedError("Unknown item id: {}".format(self._item_id))

    def to_tag(self):
        """
        -13:
        {
             -3: 158460,
             -2: -32,
            -13: // item
            -2: 1,
        }

        @rtype: TagPayload
        """
        tag_list_design = TagList()
        tag_list_design.add(TagPayload(-3, None, self._unknown_int32))
        tag_list_design.add(TagPayload(-2, None, self._item_id))
        tag_list_design.add(self._item.to_tag())
        tag_list_design.add(TagPayload(-2, None, self._item_type))
        return TagPayload(-13, None, tag_list_design)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_int32))
        if self._item_type in self._item_types:
            output_stream.write("{}\t".format(self._item_types[self._item_type]))
        else:
            output_stream.write("{}\t".format(self._item_ids[self._item_id]))
        self._item.to_stream()


class ItemPulls(object):
    """
    Handling item pull tag structure

    @type _item_pulls: dict[int, int]
    """

    def __init__(self):
        self._unknown_number = 0
        self._item_pulls = {}
        self._storage_name = ''

    def from_tag(self, tag_payload):
        """
        -13:
        {
             -2: 0,
            -13:
            {  // pull stuff
                -13: {-2: 331, -3: 99999, }
                -13: {-2: 476, -3: 99999, }
                -13: {-2: 978, -3: 99999, }
                -13: {-2: 121, -3: 99999, }
                -13: {-2: 423, -3: 99999, }
                .....
            }
             -8: ''
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[2].id == -8
        self._storage_name = list_of_tags[2].payload

        tag_payload = list_of_tags[1]
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        for pull_tag in list_of_tags:
            assert isinstance(pull_tag, TagPayload)
            assert abs(pull_tag.id) == 13
            pull_tag_list = pull_tag.payload
            assert isinstance(pull_tag_list, TagList)
            pull_list_of_tags = pull_tag_list.get_list()

            assert pull_list_of_tags[0].id == -2
            assert pull_list_of_tags[1].id == -3
            self._item_pulls[pull_list_of_tags[0].payload] = pull_list_of_tags[1].payload

    def to_tag(self):
        """
        -13:
        {
             -2: 0,
            -13:
            {  // pull stuff
                -13: {-2: 331, -3: 99999, }
                -13: {-2: 476, -3: 99999, }
                -13: {-2: 978, -3: 99999, }
                -13: {-2: 121, -3: 99999, }
                -13: {-2: 423, -3: 99999, }
                .....
            }
             -8: ''
        }

        @rtype: TagPayload
        """
        item_pulls_list = TagList()
        item_pulls_list.add(TagPayload(-2, None, self._unknown_number))

        item_pulls_item_list = TagList()
        for item_id in self._item_pulls:
            item_pull_list = TagList()
            item_pull_list.add(TagPayload(-2, None, item_id))
            item_pull_list.add(TagPayload(-3, None, self._item_pulls[item_id]))
            item_pulls_item_list.add(TagPayload(-13, None, item_pull_list))
        item_pulls_list.add(TagPayload(-13, None, item_pulls_item_list))

        item_pulls_list.add(TagPayload(-8, None, self._storage_name))
        return TagPayload(-13, None, item_pulls_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for item_id in sorted(self._item_pulls.keys()):
            output_stream.write("'{}' {}\t{}\t{}\n".format(
                self._storage_name,
                self._unknown_number,
                item_id,
                self._item_pulls[item_id]))


class Inventory(object):
    """
    Handling storage inventory tag structure

    @type _inventory_slots: dict[tuple[int], int|ItemGroup|ItemDesign|ItemBlueprint]
    """

    _label = 'inv1'

    _item_id_group = -32768

    def __init__(self):
        self._inventory_slots = {}

    def from_tag(self, tag_payload):
        """
        13: 'inv1'
        {
                    -12:
                        3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                    -12:
                        2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                    -13: {
                            -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                            -13:
                            {
                                -8: 'advancedgreenarmor',
                                -13:
                                {
                                    -2: 268,
                                    -3: 30,
                                }
                                -13:
                                {
                                    -2: 316,
                                    -3: 8,
                                }
                            }
                     }
         }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == 13
        self._label = tag_payload.name
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[0].id == -12
        assert list_of_tags[1].id == -12
        assert list_of_tags[2].id == -13

        tag_payload_list_item_slots = list_of_tags[0].payload
        tag_payload_list_item_id = list_of_tags[1].payload
        tag_payload_list_item_amounts = list_of_tags[2].payload
        assert isinstance(tag_payload_list_item_slots, TagPayloadList)
        assert isinstance(tag_payload_list_item_id, TagPayloadList)
        assert isinstance(tag_payload_list_item_amounts, TagList)
        number_of_items = len(tag_payload_list_item_slots)
        if number_of_items == 0:
            return
        list_item_slots = tag_payload_list_item_slots.get_list()
        list_item_id = tag_payload_list_item_id.get_list()
        list_item_amounts = tag_payload_list_item_amounts.get_list()
        for index in range(number_of_items):
            slot_id = list_item_slots[index]
            item_id = list_item_id[index]
            amount_tag = list_item_amounts[index]
            if item_id > 0:
                assert amount_tag.id == -3
                amount = amount_tag.payload
                self._inventory_slots[(slot_id, item_id)] = amount
            elif item_id == self._item_id_group:
                amount = ItemGroup()
                amount.from_tag(amount_tag)
                self._inventory_slots[(slot_id, item_id)] = amount
            else:
                try:
                    amount = ItemSpecial()
                    amount.from_tag(amount_tag)
                    self._inventory_slots[(slot_id, item_id)] = amount
                except (NotImplementedError, AssertionError) as e:
                    if len(e.args) > 0:
                        sys.stderr.write("WARNING: [Storage] " + e.args[0] + "\n")
                    continue

    def to_tag(self):
        """
        13: 'inv1'
        {
            -12:
                3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
            -12:
                2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	-15	-9] ,
            -13: {
                    -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
             }
         }

        @rtype: TagPayload
        """
        list_item_slots = TagPayloadList()
        list_item_id = TagPayloadList()
        list_item_amounts = TagList()
        for slot_id, item_id in self._inventory_slots.keys():
            list_item_slots.add(slot_id, 3)
            list_item_id.add(item_id, 2)
            if item_id > 0:
                list_item_amounts.add(TagPayload(-3, None, self._inventory_slots[(slot_id, item_id)]))
            else:
                list_item_amounts.add(self._inventory_slots[(slot_id, item_id)].to_tag())
        tag_list_inventory = TagList()
        tag_list_inventory.add(TagPayload(-12, None, list_item_slots))
        tag_list_inventory.add(TagPayload(-12, None, list_item_id))
        tag_list_inventory.add(TagPayload(-13, None, list_item_amounts))
        return TagPayload(13, self._label, tag_list_inventory)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for item_slot, item_id in sorted(self._inventory_slots.keys()):
            output_stream.write("[{}]\t".format(item_slot))
            if item_id < 0:
                self._inventory_slots[item_slot, item_id].to_stream(output_stream)
                continue
            output_stream.write("{}: {}\n".format(item_id, self._inventory_slots[item_slot, item_id]))


class Stash(object):
    """
    Handling Stash tag structure

    @type _label: str
    @type _item_pulls: ItemPulls
    @type _inventory: Inventory
    """

    def __init__(self):
        self._label = 'stash'
        self._item_pulls = None
        self._inventory = None

    def from_tag(self, tag_payload):
        """
        13: 'stash'
        {
            -13: // pull stuff
            13: // inventory stuff
        }

        @type tag_payload: TagPayload
        """

        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == 13
        assert tag_payload.name == 'stash', tag_payload.name
        self._label = tag_payload.name
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        self._item_pulls = ItemPulls()
        self._item_pulls.from_tag(list_of_tags[0])
        self._inventory = Inventory()
        self._inventory.from_tag(list_of_tags[1])

    def to_tag(self):
        """
        13: 'stash'
        {
            -13:  // pull stuff
             13: 'inv1'    // inventory stuff
        }
        @rtype: TagPayload
        """
        tag_list_stash = TagList()
        tag_list_stash.add(self._item_pulls.to_tag())
        tag_list_stash.add(self._inventory.to_tag())
        return TagPayload(13, self._label, tag_list_stash)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\n".format(self._label))
        if self._inventory is not None:
            self._item_pulls.to_stream()
            self._inventory.to_stream()
            output_stream.write("\n")


class Storage(object):
    """
    Handling Storage tag structure

    @type _unknown_number: int
    @type _position: tuple[int]
    @type _stash: Stash
    """

    def __init__(self):
        self._unknown_number = 3
        self._position = None
        self._stash = None

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash'
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert abs(list_of_tags[0].id) == 3
        self._unknown_number = list_of_tags[0].payload
        assert abs(list_of_tags[1].id) == 10
        self._position = list_of_tags[1].payload
        assert list_of_tags[2].id == 13

        self._stash = Stash()
        self._stash.from_tag(list_of_tags[2])

    def to_tag(self):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash'
        }
        @rtype: TagPayload
        """
        tag_list_inventory = TagList()
        tag_list_inventory.add(TagPayload(-3, None, self._unknown_number))
        tag_list_inventory.add(TagPayload(-10, None, self._position))
        tag_list_inventory.add(self._stash.to_tag())
        return TagPayload(-13, None, tag_list_inventory)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._position))
        output_stream.write("{}\t".format(self._unknown_number))
        if self._stash is not None:
            self._stash.to_stream()
            output_stream.write("\n")


class StorageList(object):
    """
    Handling Storage list tag structure

    @type _list_of_storage: list[Storage]
    """

    def __init__(self):
        self._list_of_storage = []

    def __len__(self):
        return len(self._list_of_storage)

    def from_tag(self, tag_payload):
        """
        -13:
        {
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13, (tag_payload.id, tag_payload.name)
        if tag_payload.id == 13:
            assert tag_payload.name == "controllerStructure", tag_payload.name
            # old tag, not supported
            return
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        for tag_payload in list_of_tags:
            storage = Storage()
            storage.from_tag(tag_payload)
            self._list_of_storage.append(storage)

    def to_tag(self):
        """
        -13:
        {
        }
        @rtype: TagPayload
        """
        tag_list_storage_list = TagList()
        for storage in self._list_of_storage:
            tag_list_storage_list.add(storage.to_tag())
        return TagPayload(-13, None, tag_list_storage_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for storage in self._list_of_storage:
            storage.to_stream(output_stream)
