__author__ = 'Peter Hofmann'

import sys
from lib.blueprint.meta.tag.tagmanager import TagPayload, TagList


class PositionFloat(object):
    """
    Handling docking tag structure

    @type _entries: list[tuple]
    """

    def __init__(self):
        self._label = ''
        self._entries = []

    def __len__(self):
        return len(self._entries)

    def from_tag(self, tag_payload_root):
        """
        13: ''
        {
            -13:
            {
                -10: (16, 18, 16),
                -5: 0.0,
            }
        }

        @type tag_payload_root: TagPayload
        """
        assert isinstance(tag_payload_root, TagPayload)
        assert tag_payload_root.id == 13, (tag_payload_root.id, tag_payload_root.name)
        self._label = tag_payload_root.name
        tag_list = tag_payload_root.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        for tag_payload in list_of_tag_payloads:
            assert isinstance(tag_payload, TagPayload)
            assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
            tag_list = tag_payload.payload
            assert isinstance(tag_list, TagList)
            list_of_tag_payloads_entry = tag_list.get_list()
            assert list_of_tag_payloads_entry[0].id == -10
            assert list_of_tag_payloads_entry[1].id == -5
            position = list_of_tag_payloads_entry[0].payload
            unknown_float = list_of_tag_payloads_entry[1].payload
            self._entries.append((position, unknown_float))

    def to_tag(self):
        """
        13: 'J'
        {
            -13:
            {
                -10: (16, 18, 16),
                -5: 0.0,
            }
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        for position, unknown_byte in self._entries:
            tag_list_docker = TagList()
            tag_list_docker.add(TagPayload(-10, None, position))
            tag_list_docker.add(TagPayload(-5, None, unknown_byte))
            tag_list.add(TagPayload(-13, None, tag_list_docker))
        return TagPayload(13, self._label, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for position, unknown_byte in self._entries:
            output_stream.write("{}: {}\n".format(
                position, unknown_byte))
        output_stream.write("\n")


class JumpDrives(PositionFloat):
    """
    Handling docking tag structure
    """


class Scanner(PositionFloat):
    """
    Handling docking tag structure
    """


class PositionByte(object):
    """
    Handling docking tag structure

    @type _entries: list[tuple]
    """

    def __init__(self):
        self._label = ''
        self._entries = []

    def __len__(self):
        return len(self._entries)

    def from_tag(self, tag_payload_root):
        """
        13: ''
        {
            -13:
            {
                -10: (23, -22, 55),
                -1: 0,
            }
        }

        @type tag_payload_root: TagPayload
        """
        assert isinstance(tag_payload_root, TagPayload)
        assert tag_payload_root.id == 13, (tag_payload_root.id, tag_payload_root.name)
        self._label = tag_payload_root.name
        tag_list = tag_payload_root.payload
        assert isinstance(tag_list, TagList)
        list_of_tag_payloads = tag_list.get_list()
        for tag_payload in list_of_tag_payloads:
            assert isinstance(tag_payload, TagPayload)
            assert tag_payload.id == -13, (tag_payload.id, tag_payload.name)
            tag_list = tag_payload.payload
            assert isinstance(tag_list, TagList)
            list_of_tag_payloads_entry = tag_list.get_list()
            assert list_of_tag_payloads_entry[0].id == -10
            assert list_of_tag_payloads_entry[1].id == -1
            position = list_of_tag_payloads_entry[0].payload
            unknown_byte = list_of_tag_payloads_entry[1].payload
            self._entries.append((position, unknown_byte))

    def to_tag(self):
        """
        13: ''
        {
            -13: {-10: (23, -22, 55), -1: 0, }
            -13: {-10: (16, 45, -88), -1: 0, }
        }

        @rtype: TagPayload
        """
        tag_list = TagList()
        for position, unknown_byte in self._entries:
            tag_list_docker = TagList()
            tag_list_docker.add(TagPayload(-10, None, position))
            tag_list_docker.add(TagPayload(-1, None, unknown_byte))
            tag_list.add(TagPayload(-13, None, tag_list_docker))
        return TagPayload(13, self._label, tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        for position, unknown_byte in self._entries:
            output_stream.write("{}: {}\n".format(
                position, unknown_byte))
        output_stream.write("\n")


class DockedEntities(PositionByte):
    """
    Handling docking tag structure
    """


class JumpInhibitor(PositionByte):
    """
    Handling docking tag structure
    """


class Datatype2TagReader(object):
    """
    Handling datatype2 tag structure
    """

    def __init__(self):
        self._wireless_logic = None
        self._transporters = None
        self._docker_turrets = None
        self._docker_ships = None
        self._jump_drives = None
        self._jump_inhibitors = None
        self._scanner = None
        self._shipyards = None
        return

    def from_tag(self, tag_payload_root):
        """
        -13:
        {
            13: 'ACD'   // wireless logic
            13: 'TR'    // transporter
            13: 'A'     // Old Turred Docker
            13: 'A'     // probably old normal docker
            13: 'J'     // Jump Drive
            13: 'JP'    // Jump Inhibitor
            13: 'SC'    // Scanner
            13: 'SYRD'  // Shipyard
        }

        @type tag_payload_root: TagPayload
        """
        assert isinstance(tag_payload_root, TagPayload), tag_payload_root
        tag_list = tag_payload_root.payload
        list_of_tag_payload = tag_list.get_list()
        for tag_payload in list_of_tag_payload:
            assert tag_payload.id == 13
            if tag_payload.name == "ACD":
                self._wireless_logic = None
            if tag_payload.name == "TR":
                self._transporters = None
            if tag_payload.name == "A" and self._docker_turrets is None:
                self._docker_turrets = DockedEntities()
                self._docker_turrets.from_tag(tag_payload)
            if tag_payload.name == "A":
                self._docker_ships = DockedEntities()
                self._docker_ships.from_tag(tag_payload)
            if tag_payload.name == "J":
                self._jump_drives = JumpDrives()
                self._jump_drives.from_tag(tag_payload)
            if tag_payload.name == "JP":
                self._jump_inhibitors = JumpInhibitor()
                self._jump_inhibitors.from_tag(tag_payload)
            if tag_payload.name == "SC":
                self._scanner = Scanner()
                self._scanner.from_tag(tag_payload)
            if tag_payload.name == "SYRD":
                self._shipyards = None

    def to_tag(self):
        """
        -13:
        {
            13: 'ACD' {}
            13: 'TR' {}
            13: 'A' {}
            13: 'A' {}
            13: 'J' {}
            13: 'JP' {}
            13: 'SC' {}
        }

        @rtype: TagPayload
        """
        return TagPayload(-13, None, TagList())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """

        output_stream.write("\n")
