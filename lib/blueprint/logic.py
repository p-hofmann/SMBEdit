__author__ = 'Peter Hofmann'

import os
import sys

from lib.loggingwrapper import DefaultLogging
from lib.bits_and_bytes import ByteStream
from lib.blueprint.blueprintutils import BlueprintUtils


# #######################################
# ###  LOGIC
# #######################################

class Logic(DefaultLogging, BlueprintUtils):

    _file_name = "logic.smbpl"
    _valid_versions = {0}

    def __init__(self, logfile=None, verbose=False, debug=False):
        self._label = "Logic"
        super(Logic, self).__init__(logfile, verbose, debug)
        self.version = 0
        self._offset = None
        self._controller_version = -1026
        self._controller_position_to_block_id_to_block_positions = {}
        # tail_data = None
        return

    # #######################################
    # ###  Read
    # #######################################

    def _read_set_of_positions(self, input_stream):
        """
        Read position data from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream

        @return: set of positions
        @rtype: set[int, int, int]
        """
        data = set()
        number_of_positions = input_stream.read_int32_unassigned()
        for _ in range(0, number_of_positions):
            position = input_stream.read_vector_3_int16()
            if self._offset is not None:
                # smd2 to smd3 conversion
                position = BlueprintUtils.vector_addition(position, self._offset)
            data.add(position)
        return data

    def _read_dict_of_groups(self, input_stream):
        """
        Read controller group data from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream

        @return: dict of block id to set of positions
        @rtype: dict[int, set[int, int, int]]
        """
        block_id_to_positions = {}
        number_of_groups = input_stream.read_int32_unassigned()
        for entry_index in range(0, number_of_groups):
            block_id = input_stream.read_int16_unassigned()
            block_id_to_positions[block_id] = self._read_set_of_positions(input_stream)
        return block_id_to_positions

    def _read_list_of_controllers(self, input_stream):
        """
        Read controller data from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream

        @return: set of positions
        @rtype: dict[tuple, dict[int, set[int, int, int]]]
        """
        controller_position_to_groups = {}
        number_of_controllers = input_stream.read_int32_unassigned()
        for entry_index in range(0, number_of_controllers):
            position = input_stream.read_vector_3_int16()
            if self._offset is not None:
                # smd2 to smd3 conversion
                position = BlueprintUtils.vector_addition(position, self._offset)
            controller_position_to_groups[position] = self._read_dict_of_groups(input_stream)
        return controller_position_to_groups

    def _read_file(self, input_stream):
        """
        Read data from byte stream

        @param input_stream: input stream
        @type input_stream: ByteStream
        """
        self._offset = None
        self.version = input_stream.read_int32_unassigned()
        assert self.version in self._valid_versions, "Unsupported version '{}' of '{}'.".format(self.version, self._file_name)
        # assert self.version == 0, self.version
        self._controller_version = input_stream.read_int32()
        if self._controller_version >= 0:
            # is number_of_controllers, no controller_version indicates chunk 16
            self._offset = (8, 8, 8)
            input_stream.seek(-4, whence=1)
        if -1024 <= self._controller_version < 0:
            self._offset = (8, 8, 8)
            raise NotImplementedError("Unsupported logic.smbpl with controller version: v{}".format(-self._controller_version))
        self._controller_position_to_block_id_to_block_positions = self._read_list_of_controllers(input_stream)

    def read(self, directory_blueprint):
        """
        Read data from logic file in blueprint directory

        @param directory_blueprint: input directory
        @type directory_blueprint: str
        """
        file_path = os.path.join(directory_blueprint, self._file_name)
        with open(file_path, 'rb') as input_stream:
            self._read_file(ByteStream(input_stream))

    # #######################################
    # ###  Write
    # #######################################

    @staticmethod
    def _write_list_of_positions(positions, output_stream):
        """
        Write position data to a byte stream

        @param positions: dict of block id to list of positions
        @type positions: set[int,int,int]
        @param output_stream: output stream
        @type output_stream: ByteStream
        """
        output_stream.write_int32_unassigned(len(positions))
        for position in positions:
            output_stream.write_vector_3_int16(position)

    def _write_list_of_groups(self, groups, output_stream):
        """
        Write data to a byte stream

        @param groups: dict of block id to list of positions
        @type groups: dict[int, set[int,int,int]]
        @param output_stream: output stream
        @type output_stream: ByteStream
        """
        output_stream.write_int32_unassigned(len(groups))
        for block_id, positions in groups.iteritems():
            output_stream.write_int16_unassigned(block_id)
            self._write_list_of_positions(positions, output_stream)

    def _write_list_of_controllers(self, output_stream):
        """
        Write controller data to a byte stream

        @param output_stream: output stream
        @type output_stream: ByteStream
        """
        num_controllers = len(self._controller_position_to_block_id_to_block_positions)
        output_stream.write_int32_unassigned(num_controllers)
        for controller_position, groups in self._controller_position_to_block_id_to_block_positions.iteritems():
            output_stream.write_vector_3_int16(controller_position)
            self._write_list_of_groups(groups, output_stream)

    def _write_file(self, output_stream):
        """
        Write data to a byte stream

        @param output_stream: output stream
        @type output_stream: ByteStream
        """
        output_stream.write_int32_unassigned(self.version)
        if self._controller_version < 0:
            output_stream.write_int32(self._controller_version)
        self._write_list_of_controllers(output_stream)

    def write(self, directory_blueprint):
        """
        Write data to the logic file of a blueprint

        @param directory_blueprint: output directory
        @type directory_blueprint: str
        """
        self.version = max(self._valid_versions)
        self._controller_version = -1026
        file_path = os.path.join(directory_blueprint, self._file_name)
        with open(file_path, 'wb') as output_stream:
            self._write_file(ByteStream(output_stream))

    # #######################################
    # ###  Turning
    # #######################################

    def tilt_turn(self, index_turn_tilt):
        """
        Turn or tilt this entity.

        @param index_turn_tilt: integer representing a specific turn
        @type index_turn_tilt: int

        """
        new_data = {}
        for controller_position, groups in self._controller_position_to_block_id_to_block_positions.iteritems():
            new_controller_position = self._tilt_turn_position(controller_position, index_turn_tilt)
            new_data[new_controller_position] = {}
            for block_id, positions in groups.iteritems():
                new_data[new_controller_position][block_id] = set()
                for position in positions:
                    new_position = self._tilt_turn_position(position, index_turn_tilt)
                    new_data[new_controller_position][block_id].add(new_position)
        self._controller_position_to_block_id_to_block_positions = new_data

    # #######################################
    # ###  Else
    # #######################################

    def set_link(self, controller_position, group_id, positions):
        """
        Set a link from a controller to a group

        @attention: existing links from this controller to this group id will be replaced

        @param controller_position:
        @type controller_position: tuple[int]
        @param group_id:
        @type group_id: int
        @param positions:
        @type positions: set[tuple[int]]
        """
        assert isinstance(controller_position, tuple)
        assert isinstance(group_id, int)
        assert isinstance(positions, set)
        assert len(positions) > 0
        if controller_position not in self._controller_position_to_block_id_to_block_positions:
            self._controller_position_to_block_id_to_block_positions[controller_position] = {}
        self._controller_position_to_block_id_to_block_positions[controller_position][group_id] = positions

    def move_center(self, direction_vector, entity_type=0):
        """
        Move center (core) in a specific direction and correct all links

        @param direction_vector: (x,y,z)
        @type direction_vector: int,int,int
        """
        new_dict = {}
        for controller_position, groups in self._controller_position_to_block_id_to_block_positions.iteritems():
            new_controller_position = self.vector_subtraction(controller_position, direction_vector)
            if entity_type == 0 and new_controller_position == (16, 16, 16):  # replaced block
                continue
            if entity_type == 0 and controller_position == (16, 16, 16):  # core
                new_controller_position = controller_position
            if new_controller_position not in new_dict:
                new_dict[new_controller_position] = {}
            for block_id, positions in groups.iteritems():
                if block_id not in new_dict[new_controller_position]:
                    new_dict[new_controller_position][block_id] = set()
                for block_position in positions:
                    new_block_position = self.vector_subtraction(block_position, direction_vector)
                    if entity_type == 0 and new_block_position == (16, 16, 16):  # replaced block
                        continue
                    new_dict[new_controller_position][block_id].add(new_block_position)
                if len(new_dict[new_controller_position][block_id]) == 0:
                    new_dict[new_controller_position].pop(block_id)
            if len(new_dict[new_controller_position]) == 0:
                new_dict.pop(new_controller_position)
        del self._controller_position_to_block_id_to_block_positions
        self._controller_position_to_block_id_to_block_positions = new_dict

    def _update_groups(self, controller_position, block_id, smd):
        """
        Delete links to removed blocks

        @param controller_position:
        @type controller_position: int,int,int
        @param block_id:
        @type block_id: int
        @param smd:
        @type smd: Smd
        """
        # todo: check if block at position is activatable if it exists
        positions = list(self._controller_position_to_block_id_to_block_positions[controller_position][block_id])
        for position in positions:
            if not smd.has_block_at_position(position):
                self._controller_position_to_block_id_to_block_positions[controller_position][block_id].remove(position)
        if len(self._controller_position_to_block_id_to_block_positions[controller_position][block_id]) == 0:
            self._controller_position_to_block_id_to_block_positions[controller_position].pop(block_id)

    def update(self, smd):
        """
        Delete links with invalid controller
        """
        for controller_position in self._controller_position_to_block_id_to_block_positions.keys():
            groups = self._controller_position_to_block_id_to_block_positions[controller_position]
            for block_id in groups.keys():
                if self.is_valid_block_id(block_id):
                    self._update_groups(controller_position, block_id, smd)
                    continue
                self._controller_position_to_block_id_to_block_positions[controller_position].pop(block_id)
            if len(self._controller_position_to_block_id_to_block_positions[controller_position]) == 0:
                self._controller_position_to_block_id_to_block_positions.pop(controller_position)

    def update_link(self, old_position, new_position):
        """
        Update the link from or to a block that moved position

        @param old_position:
        @type old_position: int,int,int
        @param new_position:
        @type new_position: int,int,int
        """
        assert isinstance(old_position, tuple)
        assert isinstance(new_position, tuple)
        if self._debug:
            self._logger.debug("update_link: {} -> {}".format(old_position, new_position))
        if old_position in self._controller_position_to_block_id_to_block_positions:
            groups = self._controller_position_to_block_id_to_block_positions.pop(old_position)
            self._controller_position_to_block_id_to_block_positions[new_position] = groups
        for controller_position, groups in self._controller_position_to_block_id_to_block_positions.iteritems():
            for block_id, positions in groups.iteritems():
                if old_position in positions:
                    self._controller_position_to_block_id_to_block_positions[controller_position][block_id].remove(old_position)
                    self._controller_position_to_block_id_to_block_positions[controller_position][block_id].add(new_position)

    def set_type(self, entity_type):
        """
        Change entity type
        0: "Ship",
        2: "Station",

        @param entity_type:
        @type entity_type: int
        """
        assert isinstance(entity_type, (int, long))
        assert 0 <= entity_type <= 4

        position_core = (16, 16, 16)
        if entity_type == 0:
            return
        if position_core in self._controller_position_to_block_id_to_block_positions:
            self._controller_position_to_block_id_to_block_positions.pop(position_core)

    def remove_all(self):
        """
        Remove all links from controllers

        """
        self._controller_position_to_block_id_to_block_positions = {}

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream logic values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        output_stream.write("####\nLOGIC v{}\n####\n\n".format(self.version))
        # stream.write("UNKNOWN: {}\n\n".format(self.unknown_int))
        output_stream.write("Controllers: {}\n".format(len(self._controller_position_to_block_id_to_block_positions)))
        output_stream.write("\n")
        if self._debug or self._verbose:
            for controller_position, groups in self._controller_position_to_block_id_to_block_positions.iteritems():
                output_stream.write("{}: #{}\n".format(controller_position, len(groups.keys())))
                if not self._debug:
                    continue
                for block_id, positions in groups.iteritems():
                    if len(positions) < 5:
                        output_stream.write("\t{}: {}\n".format(block_id, positions))
                    else:
                        output_stream.write("\t{}: #{}\n".format(block_id, len(positions)))
                output_stream.write("\n")
            output_stream.write("\n")
        output_stream.flush()
