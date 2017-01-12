__author__ = 'Peter Hofmann'

import sys

from lib.blueprint.meta.tagmanager import TagPayload, TagList, TagPayloadList


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
        for block_id in self._items.keys():
            output_stream.write("{} - {}: {}".format(self._label, block_id, self._items[block_id]))


class Inventory(object):
    """
    Handling Srotage tag structure

    @type _inventory_slot: list[int]
    @type _item_ids: list[int]
    @type _item_amount: list[int]
    """

    _label = 'inv1'

    _item_group_id = -32768

    def __init__(self):
        self._inventory_slot = None

    def set(self):
        """
        @type : str
        """

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
        assert abs(tag_payload.id) == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

    def to_tag(self):
        """
        13: 'inv1'
        {
                    -12:
                        3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                    -12:
                        2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                    -13: {
                            -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                     }
         }

        @rtype: TagPayload
        """
        return TagPayload(13, self._label, TagList())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """


class Storage(object):
    """
    Handling Srotage tag structure

    @type :
    """

    _label = 'stash'

    def __init__(self):

    def set(self):
        """
        @type : str
        """

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash' {
                -13: {
                     -2: 0,
                    -13: {  // pull stuff
                        -13: {-2: 331, -3: 99999, }
                        -13: {-2: 476, -3: 99999, }
                        -13: {-2: 978, -3: 99999, }
                        -13: {-2: 121, -3: 99999, }
                        -13: {-2: 423, -3: 99999, }
                        .....
                    }
                     -8: ''
                }
                13: 'inv1' {
                            -12:
                                3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                            -12:
                                2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                            -13: {
                                    -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                             }
                 }
            }
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

    def to_tag(self):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash' {
                -13: {
                     -2: 0,
                    -13: {  // pull stuff
                        -13: {-2: 331, -3: 99999, }
                        -13: {-2: 476, -3: 99999, }
                        -13: {-2: 978, -3: 99999, }
                        -13: {-2: 121, -3: 99999, }
                        -13: {-2: 423, -3: 99999, }
                        .....
                    }
                     -8: ''
                }
                13: 'inv1' {
                            -12:
                                3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                            -12:
                                2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                            -13: {
                                    -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                             }
                 }
            }
        }
        @rtype: TagPayload
        """
        return TagPayload(13, self._label, TagList())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
