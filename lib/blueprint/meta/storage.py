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
        output_stream.write("{}\t".format(self._label))
        for block_id in self._items.keys():
            output_stream.write("{}: {}, ".format(block_id, self._items[block_id]))
        output_stream.write("\n")


class ItemSpecial(object):
    """
    @type _unknown_int32: int
    @type _item_id: int
    @type _item: ItemBlueprint|ItemDesign
    @type _unknown_int16: int
    """

    _item_id_blueprint = -9
    _item_id_design = -15
    _item_id_hand_held = -32
    _item_id_helmet = -12

    _valid_items = {
        _item_id_blueprint,
        _item_id_design,
        _item_id_hand_held,
        _item_id_helmet,
    }

    def __init__(self):
        self._unknown_int32 = 0
        self._item_id = 0
        self._item = None
        self._unknown_int16 = -1

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
        assert self._item_id in ItemSpecial._valid_items, "Unkown item: {}".format(self._item_id)
        self._unknown_int16 = list_of_tags[3].payload

        tag_payload = list_of_tags[2]
        if self._item_id == self._item_id_blueprint:
            self._item = ItemBlueprint()
            self._item.from_tag(tag_payload)
        elif self._item_id == self._item_id_design:
            self._item = ItemDesign()
            self._item.from_tag(tag_payload)
        elif self._item_id == self._item_id_helmet:
            self._item = ItemHelmet()
            self._item.from_tag(tag_payload)
        elif self._item_id == self._item_id_hand_held:
            self._item = ItemHandHeld()
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
        tag_list_design.add(TagPayload(-2, None, self._unknown_int16))
        return TagPayload(-13, None, tag_list_design)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._unknown_int32))
        output_stream.write("{}\t".format(self._unknown_int16))
        self._item.to_stream()


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
            output_stream.write("'{}' {}\t{}\t{}\n".format(self._storage_name, self._unknown_number, item_id, self._item_pulls[item_id]))


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
                amount = ItemSpecial()
                amount.from_tag(amount_tag)
                self._inventory_slots[(slot_id, item_id)] = amount

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


class Storage(object):
    """
    Handling Srotage tag structure

    @type _unknown_number: int
    @type _position: tuple[int]
    @type _item_pulls: ItemPulls
    @type _inventory: Inventory
    """

    def __init__(self):
        self._label = 'stash'
        self._unknown_number = 3
        self._position = None
        self._item_pulls = None
        self._inventory = None

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash'
            {
                -13: // pull stuff
                13: // inventory stuff
            }
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
        self._label = list_of_tags[2].name

        tag_payload = list_of_tags[2]
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        self._item_pulls = ItemPulls()
        self._item_pulls.from_tag(list_of_tags[0])
        self._inventory = Inventory()
        self._inventory.from_tag(list_of_tags[1])

    def to_tag(self):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash'
            {
                -13:  // pull stuff
                 13: 'inv1'    // inventory stuff
            }
        }
        @rtype: TagPayload
        """
        tag_list_stash = TagList()
        tag_list_stash.add(self._item_pulls.to_tag())
        tag_list_stash.add(self._inventory.to_tag())

        tag_list_inventory = TagList()
        tag_list_inventory.add(TagPayload(-3, None, self._unknown_number))
        tag_list_inventory.add(TagPayload(-10, None, self._position))
        tag_list_inventory.add(TagPayload(13, self._label, tag_list_stash))
        return TagPayload(-13, None, tag_list_inventory)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("{}\t".format(self._position))
        output_stream.write("{}\t".format(self._label))
        output_stream.write("{}\n".format(self._unknown_number))
        if self._inventory is not None:
            self._item_pulls.to_stream()
            self._inventory.to_stream()
            output_stream.write("\n")


class StorageList(object):
    """
    Handling Srotage tag structure

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
        assert tag_payload.id == -13
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
