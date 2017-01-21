__author__ = 'Peter Hofmann'

import os
import sys
from lib.bits_and_bytes import ByteStream
from lib.loggingwrapper import DefaultLogging
from lib.blueprint.blueprintutils import BlueprintUtils


class DockedEntity(object):
    """
    Class for a docked entity

    @type position: tuple[int]
    @type size: tuple[float]
    @type style: int
    @type orientation: int
    """
    def __init__(self):
        self._label = "DockedEntity"
        self.position = (0, 0, 0)
        self.size = (.0, .0, .0)
        self.style = 0
        self.orientation = 0

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """

        @param input_stream:
        @type input_stream: ByteStream

        @return:
        @rtype: int
        """
        assert isinstance(input_stream, ByteStream)
        relative_path = input_stream.read_string()
        self.position = input_stream.read_vector_3_int32()
        self.size = input_stream.read_vector_3_float()
        self.style = input_stream.read_int16_unassigned()
        self.orientation = input_stream.read_byte()
        _, dock_index = relative_path.rsplit('_', 1)
        return int(dock_index)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, output_stream, dock_index, relative_path):
        """

        @param output_stream:
        @type output_stream: ByteStream
        @type dock_index: int
        @type relative_path: str
        """
        assert isinstance(output_stream, ByteStream)
        new_relative_directory = os.path.join(relative_path, "ATTACHED_{}".format(dock_index))
        output_stream.write_string(new_relative_directory)
        output_stream.write_vector_3_int32(self.position)
        output_stream.write_vector_3_float(self.size)
        output_stream.write_int16_unassigned(self.style)
        output_stream.write_byte(self.orientation)

    # #######################################
    # ###  Else
    # #######################################

    def move_position(self, vector_direction):
        self.position = BlueprintUtils.vector_addition(self.position, vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("Position: {}\t".format(self.position))
        output_stream.write("Size: {}\t".format(self.size))
        output_stream.write("Style: {}\t".format(self.style))
        output_stream.write("Orientation: {}\n".format(self.orientation))


class DataType3(DefaultLogging):
    """
    Reading data type 2 meta data

    @type _docked_entity: dict[int, DockedEntity]
    """

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "DataType3"
        super(DataType3, self).__init__(logfile, verbose, debug)
        self._docked_entity = {}
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, input_stream):
        """

        @param input_stream:
        @type input_stream: ByteStream

        @return:
        @rtype: dict
        """
        num_docked = input_stream.read_int32_unassigned()
        assert 0 <= num_docked < 1000, num_docked  # debug sanity check
        for index in range(0, num_docked):
            docked_entry = DockedEntity()
            dock_index = docked_entry.read(input_stream)
            # self._logger.debug("relative path: '{}': {}".format(name, dock_entry))
            assert dock_index not in self._docked_entity
            self._docked_entity[dock_index] = docked_entry

    # #######################################
    # ###  Write
    # #######################################

    def write_dummy(self, output_stream):
        """
        write dummy values

        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        self._logger.debug("Writing")
        output_stream.write_byte(3)
        output_stream.write_int32_unassigned(0)

    def write(self, output_stream, relative_path):
        """
        write values

        @param output_stream: Output stream
        @type output_stream: ByteStream
        """
        self._logger.debug("Writing")
        output_stream.write_byte(3)
        output_stream.write_int32_unassigned(len(self._docked_entity))
        for dock_index in self._docked_entity.keys():
            self._docked_entity[dock_index].write(output_stream, dock_index, relative_path)

    # #######################################
    # ###  Else
    # #######################################

    def popitem(self):
        """

        @rtype: Tuple[Dock_index, DockedEntity]
        """
        return self._docked_entity.popitem()

    def has_data(self):
        """
        True if data about docked entities are available.

        @rtype: bool
        """
        return len(self._docked_entity) != 0

    def move_position(self, vector_direction):
        if self.has_data():
            for dock_index in self._docked_entity.keys():
                self._docked_entity[dock_index].move_position(vector_direction)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("DataType3: {}\n".format(len(self._docked_entity)))
        if self._debug:
            for dock_index in self._docked_entity.keys():
                output_stream.write("{}:\t".format(dock_index))
                self._docked_entity[dock_index].to_stream(output_stream)
        output_stream.write("\n")
