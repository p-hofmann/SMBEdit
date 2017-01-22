import sys

from lib.smblueprint.meta.tag.tagmanager import TagPayload, TagList
from lib.smblueprint.meta.tag.storage import Stash


class ShopSetting(object):
    """
    Handling shop config tag structure

    @type _unknown_byte_0: int
    @type _unknown_double: float
    @type _unknown_long_0: int
    @type _unknown_byte_array: int
    @type _unknown_long_1: int
    @type _unknown_long_2: int
    @type _owners: list[str]
    @type _unknown_byte_1: int
    @type _unknown_byte_2: int
    @type _unknown_long_3: int
    """

    def __init__(self):
        self._unknown_byte_0 = 3
        self._unknown_double = .0
        self._unknown_long_0 = 0
        self._unknown_byte_array = 0
        self._unknown_long_1 = 0
        self._unknown_long_2 = 0
        self._owners = []
        self._unknown_byte_1 = 0
        self._unknown_byte_2 = 0
        self._unknown_long_3 = 0

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -1: 0,
            -6: 1.0,
            -4: 0,
            -7: [0, 0, 40, -68, 0, 0, 9, 54, 120, -100, 85, -102, 85, -72, -106, 69, 16, -57, 119, 118, 69, -38,
                 -94, -128, 40, -118, 23, -118, -119, 45, 6, -118, 98, 43, -118, 9, -40, -123, 93, -108, -124, 5,
                 ......],
            -4: 15,
            -4: 0,
            -13: {-8: 'owner', }
            -1: 0,
            -1: 1,
            -4: 2,
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[0].id == -1
        assert list_of_tags[1].id == -6
        assert list_of_tags[2].id == -4
        assert list_of_tags[3].id == -7
        assert list_of_tags[4].id == -4
        assert list_of_tags[5].id == -4
        assert list_of_tags[6].id == -13
        assert list_of_tags[7].id == -1
        assert list_of_tags[8].id == -1
        assert list_of_tags[9].id == -4

        self._unknown_byte_0 = list_of_tags[0].payload
        self._unknown_double = list_of_tags[1].payload
        self._unknown_long_0 = list_of_tags[2].payload
        self._unknown_byte_array = list_of_tags[3].payload
        self._unknown_long_1 = list_of_tags[4].payload
        self._unknown_long_2 = list_of_tags[5].payload
        self._unknown_byte_1 = list_of_tags[7].payload
        self._unknown_byte_2 = list_of_tags[8].payload
        self._unknown_long_3 = list_of_tags[9].payload

        tag_payload = list_of_tags[6]
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        for tag_payload in list_of_tags:
            assert tag_payload.id == -8
            self._owners.append(tag_payload.payload)

    def to_tag(self):
        """
        -13:
        {
            -1: 0,
            -6: 1.0,
            -4: 0,
            -7: [0, 0, 40, -68, 0, 0, 9, 54, 120, -100, 85, -102, 85, -72, -106, 69, 16, -57, 119, 118, 69, -38,
                 -94, -128, 40, -118, 23, -118, -119, 45, 6, -118, 98, 43, -118, 9, -40, -123, 93, -108, -124, 5,
                 ......],
            -4: 15,
            -4: 0,
            -13: {-8: 'owner', }
            -1: 0,
            -1: 1,
            -4: 2,
        }

        @rtype: TagPayload
        """
        tag_list_owners = TagList()
        for owner in self._owners:
            tag_list_owners.add(TagPayload(-8, None, owner))

        tag_list_setting = TagList()
        tag_list_setting.add(TagPayload(-1, None, self._unknown_byte_0))
        tag_list_setting.add(TagPayload(-6, None, self._unknown_double))
        tag_list_setting.add(TagPayload(-4, None, self._unknown_long_0))
        tag_list_setting.add(TagPayload(-7, None, self._unknown_byte_array))
        tag_list_setting.add(TagPayload(-4, None, self._unknown_long_1))
        tag_list_setting.add(TagPayload(-4, None, self._unknown_long_2))
        tag_list_setting.add(TagPayload(-13, None, tag_list_owners))
        tag_list_setting.add(TagPayload(-1, None, self._unknown_byte_1))
        tag_list_setting.add(TagPayload(-1, None, self._unknown_byte_2))
        tag_list_setting.add(TagPayload(-4, None, self._unknown_long_3))
        return TagPayload(-13, None, tag_list_setting)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for owner in self._owners:
            output_stream.write("{}\t".format(owner))
        output_stream.write("\n")
        output_stream.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            self._unknown_byte_0,
            self._unknown_double,
            self._unknown_long_0,
            # self._unknown_byte_array,
            self._unknown_long_1,
            self._unknown_long_2,
            self._unknown_byte_1,
            self._unknown_byte_2,
            self._unknown_long_3,
        ))


class Shop(object):
    """
    Handling shop tag structure

    @type _stash: Stash
    @type _setting: ShopSetting
    """

    def __init__(self):
        self._label = "exS"
        self._stash = None
        self._setting = None

    def from_tag(self, tag_payload):
        """
        13: 'exS'  // shop
        {
             13: 'stash'
            -13:  // setting
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert tag_payload.id == 13
        self._label = tag_payload.name
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        assert list_of_tags[0].id == 13
        assert list_of_tags[1].id == -13
        self._stash = Stash()
        self._stash.from_tag(list_of_tags[0])
        self._setting = ShopSetting()
        self._setting.from_tag(list_of_tags[1])

    def to_tag(self):
        """
        13: 'exS'  // shop
        {
             13: 'stash'
            -13:  // setting
        }

        @rtype: TagPayload
        """
        tag_list_shop = TagList()
        tag_list_shop.add(self._stash.to_tag())
        tag_list_shop.add(self._setting.to_tag())
        return TagPayload(13, self._label, tag_list_shop)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Shop\n")
        if self._setting is not None:
            self._setting.to_stream()
            output_stream.write("\n")
        if self._stash is not None:
            self._stash.to_stream()
