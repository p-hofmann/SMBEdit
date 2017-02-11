__author__ = 'Peter Hofmann'

import sys
import os

from lib.bits_and_bytes import BinaryStream
from lib.loggingwrapper import DefaultLogging
from lib.smblueprint.meta.tag.tagmanager import TagManager
from lib.smblueprint.meta.tag.raildockentitylinks import RailDockedEntityLinks


class DataType4(DefaultLogging):
    """
    Reading data type 4 meta data

    @type _vector_float_0: tuple[float]
    @type _vector_float_1: tuple[float]
    @type _entity_label: str
    @type _entity_wireless_logic_stuff: dict[int, tuple]
    @type _docked_entities: dict[int,TagManager]
    """

    def __init__(self, meta_version, logfile=None, verbose=False, debug=False):
        """

        @type meta_version: int
        @return:
        """
        self._meta_version = meta_version
        self._label = "DataType4"
        super(DataType4, self).__init__(logfile, verbose, debug)
        self._vector_float_0 = (0, 0, 0)
        self._vector_float_1 = (0, 0, 0)
        self._entity_label = ""
        self._entity_wireless_logic_stuff = {}
        self._docked_entities = {}
        return

    # #######################################
    # ###  Read
    # #######################################

    @staticmethod
    def get_index(position_x, position_y, position_z):
        """

        @param position_x:
        @type position_x: int
        @param position_y:
        @type position_y: int
        @param position_z:
        @type position_z: int

        @return:
        @rtype: int
        """
        return int(position_z << 32) + int(position_y << 16) + int(position_x)

    @staticmethod
    def get_pos(position_index, bit_shift=0):
        """

        @param position_index:
        @type position_index: int

        @return:
        @rtype: int
        """
        if bit_shift == 0:
            return int(position_index & 65535)
        return int(position_index >> bit_shift & 65535)

    def chunk16_to_chunk_32_shift_index(self, position_index, offset):
        """

        @type position_index: int
        @type offset: int

        @return:
        @rtype: int
        """
        return self.get_index(
            self.get_pos(position_index) + offset,
            self.get_pos(position_index, 16) + offset,
            self.get_pos(position_index, 32) + offset)

    def _read_wireless_logic_stuff(self, input_stream, offset):
        """
        Read unknown stuff from byte stream

        @param input_stream: input stream
        @type input_stream: BinaryStream

        @rtype (str, int, int)
        """
        unknown_string = input_stream.read_string()  # utf
        unknown_position_index_0 = input_stream.read_int64()
        unknown_position_index_1 = input_stream.read_int64()
        self._logger.debug("wireless_logic stuff string: '{}'".format(unknown_string))
        # if offset != 0:
        #     # chunk16 to 32
        #     unknown_position_index_0 = self.chunk16_to_chunk_32_shift_index(unknown_position_index_0, offset)
        #     unknown_position_index_1 = self.chunk16_to_chunk_32_shift_index(unknown_position_index_1, offset)
        return unknown_string, unknown_position_index_0, unknown_position_index_1

    def read(self, input_stream, version):
        """
        Read rail docker data?

        @param input_stream: input stream
        @type input_stream: BinaryStream
        """
        self._vector_float_0 = input_stream.read_vector_3_float()
        self._vector_float_1 = input_stream.read_vector_3_float()
        offset = 0
        if version < (0, 0, 0, 4):
            offset = 8
        if version >= (0, 0, 0, 2):
            self._entity_label = input_stream.read_string()  # utf
            number_of_wireless_connections = input_stream.read_int32()
            self._entity_wireless_logic_stuff = {}
            for some_index in range(number_of_wireless_connections):
                self._entity_wireless_logic_stuff[some_index] = self._read_wireless_logic_stuff(input_stream, offset)

        self._docked_entities = {}
        amount_of_docked_entities = input_stream.read_int32()
        for turret_index in range(amount_of_docked_entities):
            relative_path = input_stream.read_string()  # utf
            _, dock_index = relative_path.rsplit('_', 1)
            tag_size = input_stream.read_int32_unassigned()
            if tag_size > 0:
                self._docked_entities[int(dock_index)] = TagManager(
                    logfile=self._logfile, verbose=self._verbose, debug=self._debug)
                self._docked_entities[int(dock_index)].read(input_stream)

    # #######################################
    # ###  Write
    # #######################################

    @staticmethod
    def _write_wireless_logic_stuff(output_stream, stuff):
        """
        Write some stuff to byte stream

        @param output_stream: output_stream
        @type output_stream: BinaryStream
        """
        output_stream.write_string(stuff[0])
        output_stream.write_int64(stuff[1])
        output_stream.write_int64(stuff[2])

    def write(self, output_stream, version, relative_path, compressed=False):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: BinaryStream
        """
        self._logger.debug("Writing")
        output_stream.write_byte(4)

        output_stream.write_vector_3_float(self._vector_float_0)
        output_stream.write_vector_3_float(self._vector_float_1)

        if version >= (0, 0, 0, 2):
            output_stream.write_string(self._entity_label)
            list_size_of_unknown_stuff = len(self._entity_wireless_logic_stuff)
            output_stream.write_int32_unassigned(list_size_of_unknown_stuff)
            if list_size_of_unknown_stuff > 0:
                self._logger.warning("Writing unknown stuff.")
            for index in sorted(self._entity_wireless_logic_stuff.keys()):
                self._write_wireless_logic_stuff(output_stream, self._entity_wireless_logic_stuff[index])

        output_stream.write_int32_unassigned(len(self._docked_entities))
        for dock_index in sorted(self._docked_entities.keys()):
            new_relative_directory = os.path.join(relative_path, "ATTACHED_{}".format(dock_index))
            # self._logger.debug(new_relative_directory)
            output_stream.write_string(new_relative_directory)
            file_position_size = output_stream.tell()
            output_stream.seek(4, whence=1)  # skip size for later
            file_position_tag = output_stream.tell()
            self._docked_entities[dock_index].write(output_stream, compressed)
            file_position_end = output_stream.tell()
            output_stream.seek(file_position_size)
            tag_size = file_position_end-file_position_tag
            output_stream.write_int32_unassigned(tag_size)
            output_stream.seek(file_position_end)

    # #######################################
    # ###  Else
    # #######################################

    def add(self, docked_entity_index, rail_docker_links):
        """

        @type docked_entity_index: int
        @type rail_docker_links: RailDockedEntityLinks
        """
        assert docked_entity_index not in self._docked_entities, "Docked entity already exists: {}".format(
            docked_entity_index)
        tag_manager = TagManager(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        tag_manager.set_root_tag(rail_docker_links.to_tag())
        self._docked_entities[docked_entity_index] = tag_manager

    def move_position(self, vector_direction, main_only=False):
        """
        Move positions of rail docked entities

        @type vector_direction: tuple[int]
        """
        for docker_key in self._docked_entities.keys():
            rail_docker_links = RailDockedEntityLinks(self._meta_version)
            rail_docker_links.from_tag(self._docked_entities[docker_key].get_root_tag())
            rail_docker_links.move_position(vector_direction, main_only)
            self._docked_entities[docker_key].set_root_tag(rail_docker_links.to_tag())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("DataType4: {}\n".format(len(self._docked_entities)))
        output_stream.write("Label: '{}'\t".format(self._entity_label))
        output_stream.write("Vector: '{}', '{}'\n".format(self._vector_float_0, self._vector_float_1))
        list_size_of_unknown_stuff = len(self._entity_wireless_logic_stuff)
        if self._debug and list_size_of_unknown_stuff > 0:
            output_stream.write("Wireless connections: #{}\n".format(len(self._entity_wireless_logic_stuff)))
            for index in self._entity_wireless_logic_stuff:
                name, long0, long1 = self._entity_wireless_logic_stuff[index]
                output_stream.write("{}: {} {}\n".format(name, long0, long1))

        if self._debug:
            for dock_index in sorted(self._docked_entities.keys()):
                output_stream.write("\nDocked entity {}:\n".format(dock_index))
                # self._docked_entities[dock_index].to_stream(output_stream)
                links = RailDockedEntityLinks(self._meta_version)
                links.from_tag(self._docked_entities[dock_index].get_root_tag())
                links.to_stream(output_stream)
        output_stream.write("\n")
