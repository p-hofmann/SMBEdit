__author__ = 'Peter Hofmann'

import sys

from lib.blueprint.meta.tag.tagmanager import TagPayload, TagList
from lib.blueprint.meta.tag.storage import StorageList
from lib.blueprint.meta.tag.aiconfig import AIConfig
from lib.blueprint.meta.tag.shop import Shop
from lib.blueprint.meta.tag.displaylist import DisplayList


class Unknown4(object):
    """
    @type _unknown_long: int
    """

    def __init__(self):
        self._unknown_long = 0

    def from_tag(self, tag_payload):
        """
        -13: {-4: -9223372036854775808, }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
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


class Datatype2TagReader(object):
    """
    Handling datatype2 tag structure
    @type _label: str
    """

    def __init__(self):
        self._label = 'container'

        self._storage = None
        self._unknown_1_tag = None
        self._unknown_2_tag = None
        self._unknown_3_tag = None
        self._shop = None
        self._unknown_5_tag = None
        self._displays = None
        self._unknown_7_tag = None
        self._unknown_8_tag = None
        self._unknown_9_tag = None
        self._ai_config = None
        self._unknown_11_tag = None
        self._unknown_12_tag = None
        self._unknown_13_tag = None
        self._unknown_14_tag = TagPayload()
        return

    def from_tag(self, tag_payload):
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
                -13: {-2: 478, -3: 0, }-13: {-2: 3, -3: 0, }-13: {-2: 937, -3: 0, }-13: {-2: 8, -3: 12, }-13: {-2: 122, -3: 2, }
                -13: {-2: 22, -3: 0, }-13: {-2: 14, -3: 0, }-13: {-2: 15, -3: 0, }-13: {-2: 2, -3: 99, }-13: {-2: 671, -3: 0, }
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


        @type tag_payload: TagPayload
        """
        tag_list = tag_payload.payload
        list_of_tag_paylaods = tag_list.get_list()

        tag_payload = list_of_tag_paylaods[0]
        if tag_payload.id == -13:
            self._storage = StorageList()
            self._storage.from_tag(tag_payload)
        else:
            self._ai_config = tag_payload

        self._unknown_1_tag = list_of_tag_paylaods[1]
        self._unknown_2_tag = list_of_tag_paylaods[2]
        self._unknown_3_tag = list_of_tag_paylaods[3]

        tag_payload = list_of_tag_paylaods[4]
        if tag_payload.id == 13 and "exS" in tag_payload.name:
            self._shop = Shop()
            self._shop.from_tag(tag_payload)
        else:
            self._shop = tag_payload

        self._unknown_5_tag = list_of_tag_paylaods[5]

        tag_payload = list_of_tag_paylaods[6]
        self._displays = DisplayList()
        self._displays.from_tag(tag_payload)

        self._unknown_7_tag = list_of_tag_paylaods[7]
        if len(list_of_tag_paylaods) <= 9:
            return
        self._unknown_8_tag = list_of_tag_paylaods[8]
        self._unknown_9_tag = list_of_tag_paylaods[9]

        tag_payload = list_of_tag_paylaods[10]
        if tag_payload.id == 13 and "AIConfig" in tag_payload.name:
            self._ai_config = AIConfig()
            self._ai_config.from_tag(tag_payload)
        else:
            self._ai_config = tag_payload

        self._unknown_11_tag = list_of_tag_paylaods[11]
        self._unknown_12_tag = list_of_tag_paylaods[12]
        if len(list_of_tag_paylaods) <= 14:
            return
        self._unknown_13_tag = list_of_tag_paylaods[13]
        self._unknown_14_tag = list_of_tag_paylaods[14]

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
        self._unknown_1_tag.to_stream(output_stream)
        output_stream.write("\n")
        self._unknown_2_tag.to_stream(output_stream)
        output_stream.write("\n")
        self._unknown_3_tag.to_stream(output_stream)
        output_stream.write("\n")
        # self._shop.to_stream(output_stream)
        self._unknown_5_tag.to_stream(output_stream)
        output_stream.write("\n")
        # self._displays.to_stream(output_stream)
        self._unknown_7_tag.to_stream(output_stream)
        output_stream.write("\n")
        if self._unknown_8_tag is None:
            return
        self._unknown_8_tag.to_stream(output_stream)
        output_stream.write("\n")
        self._unknown_9_tag.to_stream(output_stream)
        output_stream.write("\n")
        # self._ai_config.to_stream(output_stream)
        self._unknown_11_tag.to_stream(output_stream)
        output_stream.write("\n")
        self._unknown_12_tag.to_stream(output_stream)
        output_stream.write("\n")
        if self._unknown_13_tag is None:
            return
        self._unknown_13_tag.to_stream(output_stream)
        output_stream.write("\n")
        self._unknown_14_tag.to_stream(output_stream)
        output_stream.write("\n")
