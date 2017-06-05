__author__ = 'Peter Hofmann'

import sys

from smlib.utils.blockconfig import block_config
from smlib.utils.vector import Vector
from .tagmanager import TagPayload, TagList


class RailBasis(object):

    _rail_orientation_map_old = {
        (0, 0): "Right_forward",
        (1, 0): "Right_up",
        (2, 0): "Right_backwards",
        (3, 0): "Right_down",
        (4, 0): "Left_forward",
        (5, 0): "Left_up",
        (6, 0): "Left_backwards",
        (7, 0): "Left_down",
        (0, 1): "Front_down",
        (1, 1): "Front_left",
        (2, 1): "Front_up",
        (3, 1): "Front_right",
        (4, 1): "Back_down",
        (5, 1): "Back_left",
        (6, 1): "Back_up",
        (7, 1): "Back_right",
        (8, 1): "Bottom_backwards",
        (9, 1): "Bottom_left",
        (10, 1): "Bottom_forward",
        (11, 1): "Bottom_right",
        (12, 1): "Top_backwards",
        (13, 1): "Top_left",
        (14, 1): "Top_forward",
        (15, 1): "Top_right",
    }

    # meta version 5, 0_199_435:
    _rail_orientation_map = {
        (0, 0): "Front_down",
        (1, 0): "Front_left",
        (2, 0): "Front_up",
        (3, 0): "Front_right",
        (4, 0): "Back_down",
        (5, 0): "Back_left",
        (6, 0): "Back_up",
        (7, 0): "Back_right",
        (8, 0): "Bottom_backwards",
        (9, 0): "Bottom_left",
        (10, 0): "Bottom_forward",
        (11, 0): "Bottom_right",
        (12, 0): "Top_backwards",
        (13, 0): "Top_left",
        (14, 0): "Top_forward",
        (15, 0): "Top_right",
        (16, 0): "Right_forward",
        (17, 0): "Right_up",
        (18, 0): "Right_backwards",
        (19, 0): "Right_down",
        (20, 0): "Left_forward",
        (21, 0): "Left_up",
        (22, 0): "Left_backwards",
        (23, 0): "Left_down",
    }


class RailDockedEntity(RailBasis):
    """
    Handling rail docked entity tag structure

    @type _location: tuple[int]
    """

    _side_to_orientation = {
        0: (2, 1),  # "Front_up",
        1: (4, 1),  # "Back_down",
        2: (14, 1),  # "Top_forward"
        3: (8, 1),  # "Bottom_backwards"
        4: (0, 0),  # "Right_forward",
        5: (4, 0),  # "Left_forward",
    }

    _side_to_orientation_v5 = {
        0: (2, 0),  # "Front_up",
        1: (4, 0),  # "Back_down",
        2: (14, 0),  # "Top_forward"
        3: (8, 0),  # "Bottom_backwards"
        4: (16, 0),  # "Right_forward",
        5: (20, 0),  # "Left_forward",
    }

    # 0: "FRONT ",
    # 1: "BACK  ",
    # 2: "TOP   ",
    # 3: "BOTTOM",
    # 4: "RIGHT ",
    # 5: "LEFT  ",

    def __init__(self):
        """

        @return:
        """
        self._unknown_byte_0 = -1
        self._label = ""
        self._location = (0, 0, 0)
        self._block_id = 0
        self._byte_orientation_1 = 0
        self._byte_orientation_2 = 0
        self._hit_points = 100
        return

    def move_position(self, vector_direction):
        """
        Move positions of rail docked entities

        @type vector_direction: tuple[int]
        """
        self._location = Vector.addition(self._location, vector_direction)

    def set_by_block_side(self, label, location, block_id, side, version):
        """

        @param label:
        @type label: str
        @param location:
        @type location: tuple[int]
        @param block_id:
        @type block_id: int
        @param side:
        @type side: int
        """
        byte_orientation_1, byte_orientation_2 = self._side_to_orientation[side]
        if version > 4:
            byte_orientation_1, byte_orientation_2 = self._side_to_orientation_v5[side]

        self.set(label, location, block_id, byte_orientation_1, byte_orientation_2)

    def set(self, label, location, block_id, byte_orientation_1, byte_orientation_2):
        """

        @param label:
        @type label: str
        @param location:
        @type location: tuple[int]
        @param block_id:
        @type block_id: int
        @param byte_orientation_1:
        @type byte_orientation_1: int
        @param byte_orientation_2:
        @type byte_orientation_2: int
        """
        self._label = label
        self._location = location
        self._block_id = block_id
        self._byte_orientation_1 = byte_orientation_1
        self._byte_orientation_2 = byte_orientation_2
        self._hit_points = block_config[block_id].hit_points

    def get_block_id(self):
        """
        @rtype: int
        """
        return self._block_id

    def from_tag(self, tag_payload, version):
        """
        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload), tag_payload
        assert abs(tag_payload.id) == 13, (tag_payload.id, tag_payload.payload)
        assert isinstance(tag_payload.payload, TagList)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        offset = 0
        # if version > 4:
        if list_of_tags[0].id == -1:
            offset = 1
            self._unknown_byte_0 = list_of_tags[0].payload
        # assert list_of_tags[0+offset].id == -8, list_of_tags[0+offset].id
        self._label = list_of_tags[0+offset].payload
        self._location = list_of_tags[1+offset].payload
        self._block_id = list_of_tags[2+offset].payload
        self._byte_orientation_1 = list_of_tags[3+offset].payload
        self._byte_orientation_2 = list_of_tags[4+offset].payload
        self._hit_points = list_of_tags[5+offset].payload

    def to_tag(self, version):
        """
        -1: 0,  # meta version 5
        -8: ENTITY_SHIP_Skallagrim_1483048232229,
        -10: (16, 15, 16),
        -2: 662,
        -1: 10,
        -1: 1,
        -1: 100,

        @rtype: TagPayload
        """
        tag_list = TagList()
        byte_orientation_1 = self._byte_orientation_1
        byte_orientation_2 = self._byte_orientation_2
        if version > 4 and self._unknown_byte_0 != -1:
            tag_list.add(TagPayload(-1, None, self._unknown_byte_0))
        #     if byte_orientation_2 == 0 and byte_orientation_1 < 8:
        #         byte_orientation_1 += 16
        tag_list.add(TagPayload(-8, None, self._label))
        tag_list.add(TagPayload(-10, None, self._location))
        tag_list.add(TagPayload(-2, None, self._block_id))
        tag_list.add(TagPayload(-1, None, byte_orientation_1))
        tag_list.add(TagPayload(-1, None, byte_orientation_2))
        tag_list.add(TagPayload(-1, None, self._hit_points))
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout, version=5):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO[str]
        """
        output_stream.write("{}\t".format(self._location))
        output_stream.write("{}\t".format(self._block_id))
        orientation = (self._byte_orientation_1, self._byte_orientation_2)
        if self._byte_orientation_2 == 1 or version < 5:
            #
            output_stream.write("{}\t".format(self._rail_orientation_map_old[orientation]))
        else:
            output_stream.write("{}\t".format(self._rail_orientation_map[orientation]))
        output_stream.write("{}\n".format(self._label))


class RailDockedEntityLink(object):
    """
    Handling rail docked entity tag structure

    @type _entity_main: RailDockedEntity
    @type _entity_docked: RailDockedEntity
    @type _docked_entity_location: tuple[int]
    @type _unknown_matrix_0: list[list[int]]
    @type _unknown_matrix_1: list[list[int]]
    @type _unknown_matrix_2: list[list[int]]
    """

    def __init__(self):
        """

        @return:
        """
        self._entity_main = None
        self._entity_docked = None
        self._docked_entity_location = (0, 0, 0)
        self._unknown_matrix_0 = [
            [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self._unknown_matrix_1 = [
            [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self._unknown_matrix_2 = [
            [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self._unknown_byte_0 = 0
        self._unknown_byte_1 = 0
        self._unknown_byte_2 = 0
        return

    def move_position(self, vector_direction, main_only=False):
        """
        Move positions of rail docked entities

        @type vector_direction: tuple[int]
        """
        self._docked_entity_location = Vector.addition(self._docked_entity_location, vector_direction)
        self._entity_main.move_position(vector_direction)
        if not main_only:
            self._entity_docked.move_position(vector_direction)

    def set(self, docked_entity_location, entity_main, entity_docked):
        """

        @type entity_main: RailDockedEntity
        @type entity_docked: RailDockedEntity
        @type docked_entity_location: tuple[int]
        """
        assert block_config[entity_main.get_block_id()].is_rail(), "Expected Rail id but got {}.".format(
            entity_docked.get_block_id())
        assert entity_docked.get_block_id() == 663, "Expected Rail Docker id but got {}.".format(
            entity_docked.get_block_id())
        self._entity_main = entity_main
        self._entity_docked = entity_docked
        self._docked_entity_location = docked_entity_location

    def from_tag(self, tag_payload, version):
        """
        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        assert isinstance(tag_payload.payload, TagList)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        self._entity_main = RailDockedEntity()
        self._entity_main.from_tag(list_of_tags[0], version)
        self._entity_docked = RailDockedEntity()
        self._entity_docked.from_tag(list_of_tags[1], version)
        self._unknown_matrix_0 = list_of_tags[2].payload
        self._unknown_matrix_1 = list_of_tags[3].payload
        self._docked_entity_location = list_of_tags[4].payload
        self._unknown_matrix_2 = list_of_tags[5].payload
        self._unknown_byte_0 = list_of_tags[6].payload
        self._unknown_byte_1 = list_of_tags[7].payload
        self._unknown_byte_2 = list_of_tags[8].payload

    def to_tag(self, version):
        """
        # entity_entry
        -13:  {}        // "Rail Basic"     Main entity
        # entity_entry
        -13:  {}        // "Rail Docker"    Docked entity
        -16: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
        -16: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
        -10: (16, 14, 16),
        -16: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
        -1: 0,
        -1: 0,  // 1: 664, 669
        -1: 0,  // 1: 662, sometimes

        @rtype: TagPayload
        """
        link_tag = TagList()
        link_tag.add(self._entity_main.to_tag(version))
        link_tag.add(self._entity_docked.to_tag(version))
        link_tag.add(TagPayload(-16, None, self._unknown_matrix_0))
        link_tag.add(TagPayload(-16, None, self._unknown_matrix_1))
        link_tag.add(TagPayload(-10, None, self._docked_entity_location))
        link_tag.add(TagPayload(-16, None, self._unknown_matrix_2))
        link_tag.add(TagPayload(-1, None, self._unknown_byte_0))
        link_tag.add(TagPayload(-1, None, self._unknown_byte_1))
        link_tag.add(TagPayload(-1, None, self._unknown_byte_2))
        return TagPayload(-13, None, link_tag)

    def to_stream(self, output_stream=sys.stdout, version=5):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        output_stream.write("Location: {}\n".format(self._docked_entity_location))
        output_stream.write("Main:\t")
        self._entity_main.to_stream(output_stream, version)
        output_stream.write("Docked:\t")
        self._entity_docked.to_stream(output_stream, version)
        # output_stream.write("{}\n".format(self._unknown_matrix_0))
        # output_stream.write("{}\n".format(self._unknown_matrix_1))
        # output_stream.write("{}\n".format(self._unknown_matrix_2))
        output_stream.write("{}\n\n".format((self._unknown_byte_0, self._unknown_byte_1, self._unknown_byte_2)))


class NameList(object):
    """
    """
    def __init__(self):
        """

        """
        self._list_names = []
        return

    def from_tag(self, tag_payload):
        """
        -13:  { -8: 'ENTITY_SHIP_Skallagrim_1482413226243_SY_TEST-rl104' }

        @type tag_payload: TagPayload
        """
        self._list_names = []
        assert isinstance(tag_payload, TagPayload), tag_payload
        assert tag_payload.id == -13, tag_payload.id
        assert isinstance(tag_payload.payload, TagList)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        for tag_payload in list_of_tags:
            assert tag_payload.id == -8, (tag_payload.id, tag_payload.payload.get_list())
            self._list_names.append(tag_payload.payload)

    def to_tag(self):
        """
        -13:  { -8: 'ENTITY_SHIP_Skallagrim_1482413226243_SY_TEST-rl104' }

        @rtype: TagPayload
        """
        tag_list = TagList()
        for name in self._list_names:
            tag_list.add(TagPayload(-8, None, name))
        return TagPayload(-13, None, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO[str]
        """
        for name in self._list_names:
            output_stream.write("{}\n".format(name))


class RailDockedEntityLinks(object):
    """
    Handling rail docked entity tag structure

    @type _list_links: list[RailDockedEntityLink]
    """

    def __init__(self):
        """

        """
        self._list_links = []
        self._names = NameList()
        return

    def move_position(self, vector_direction, main_only=False):
        """
        Move positions of rail docked entities

        @type vector_direction: tuple[int]
        """
        for docker_link in self._list_links:
            docker_link.move_position(vector_direction, main_only=main_only)

    def set(self, links):
        """
        @type links: list[RailDockedEntityLink]
        """
        self._list_links = links

    def from_tag(self, tag_payload, version):
        """
        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload), tag_payload
        assert abs(tag_payload.id) == 13
        assert isinstance(tag_payload.payload, TagList)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()
        number_of_links = list_of_tags[0].payload
        assert number_of_links > 0, number_of_links

        tag_payload = list_of_tags[1]
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        assert isinstance(tag_payload.payload, TagList)
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList), tag_list.to_stream(sys.stderr)
        list_of_link_tags = tag_list.get_list()
        for tag_index in range(number_of_links):
            # tag_list_link = tag_list[tag_index+1].payload
            # assert isinstance(tag_list_link, TagList)
            link = RailDockedEntityLink()
            link.from_tag(list_of_link_tags[tag_index], version)
            self._list_links.append(link)
        if len(list_of_tags) > 1+number_of_links:
            self._names.from_tag(list_of_tags[-1])

    def to_tag(self, version):
        """
        -13: {
                -1: 1,
                -13:  { #RailDockedEntityLink }
                -13:  { -8: 'ENTITY_SHIP_Skallagrim_1482413226243_SY_TEST-rl104' }
            }

        @rtype: TagPayload
        """
        links_tag_list = TagList()
        links_tag_list.add(TagPayload(-1, None, len(self._list_links)))

        tag_list = TagList()
        for link in self._list_links:
            tag_list.add(link.to_tag(version))

        links_tag_list.add(TagPayload(-13, None, tag_list))
        links_tag_list.add(self._names.to_tag())  # why is here a empty tag list? No clue!
        return TagPayload(-13, None, links_tag_list)

    def to_stream(self, output_stream=sys.stdout, version=5):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO[str]
        """
        for link in self._list_links:
            link.to_stream(output_stream, version)
            # output_stream.write("\n")
        self._names.to_stream(output_stream)
