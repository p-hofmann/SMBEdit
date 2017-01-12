from __future__ import unicode_literals
from builtins import range
__author__ = 'Peter Hofmann'

import os
import sys

from lib.loggingwrapper import DefaultLogging
from lib.blueprint.blueprintutils import BlueprintUtils
from lib.blueprint.header import Header
from lib.blueprint.logic import Logic
from lib.blueprint.meta.meta import Meta
from lib.blueprint.smd3.smd import Smd
from lib.blueprint.smd3.smdblock import SmdBlock


class Blueprint(DefaultLogging, BlueprintUtils):

    def __init__(self, logfile=None, verbose=False, debug=False):
        """
        Constructor

        @param logfile: file handler or file path to a log file
        @type logfile: file | FileIO | StringIO | basestring
        @param verbose: Not verbose means that only warnings and errors will be past to stream
        @type verbose: bool
        @param debug: Display debug messages
        @type debug: bool

        @rtype: None
        """
        self._label = "Blueprint"
        super(Blueprint, self).__init__(logfile=logfile, verbose=verbose, debug=debug)
        self.header = Header(logfile=logfile, verbose=verbose, debug=debug)
        self.logic = Logic(logfile=logfile, verbose=verbose, debug=debug)
        self.meta = Meta(logfile=logfile, verbose=verbose, debug=debug)
        self.smd3 = Smd(logfile=logfile, verbose=verbose, debug=debug)
        return

    # #######################################
    # ###  Read
    # #######################################

    def read(self, directory_blueprint):
        """
        Read blueprint from a directory

        @attention: smd data needs to be read before meta and logic. An offset will be set if smd2.

        @param directory_blueprint: /../StarMade/blueprints/blueprint_name/
        @type directory_blueprint: str
        """
        self.smd3 = Smd(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        self.header = Header(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        self.logic = Logic(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        self.meta = Meta(logfile=self._logfile, verbose=self._verbose, debug=self._debug)

        self.header.read(directory_blueprint)
        self.smd3.read(directory_blueprint)
        self.logic.read(directory_blueprint)
        self.meta.read(directory_blueprint)

    # #######################################
    # ###  Write
    # #######################################

    def write(self, directory_blueprint, relative_path=None):
        """
        Save blueprint to a directory

        @param directory_blueprint: /../StarMade/blueprints/blueprint_name
        @type directory_blueprint: str
        """
        assert os.path.exists(directory_blueprint), "Output directory failed to be created."
        blueprint_name = os.path.basename(directory_blueprint)

        self.header.write(directory_blueprint)
        self.logic.write(directory_blueprint)
        self.meta.write(directory_blueprint, relative_path=relative_path)
        self.smd3.write(directory_blueprint, blueprint_name)

    # #######################################
    # ###  Else
    # #######################################

    def replace_outdated_docker_modules(self, entity_name, rail_docked_label_prefix, is_docked_entity):
        rail_docker_id = 663
        if is_docked_entity and self.smd3.search(rail_docker_id) is None:
            self._logger.info("Adding 'Rail docker' to docked entity.")
            block = SmdBlock(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
            block.update(
                rail_docker_id, hit_points=100, active=False, bit_19=0, bit_22=0, bit_23=1, rotations=2)
            position_below_core = (16, 15, 16)
            self.smd3.add(position_below_core, block)
            self.header.update(self.smd3)

        if not self.meta.has_old_docked_entities():
            return
        self._logger.info("Replacing outdated docker modules")
        self.meta.update_docked_entities(self.smd3, entity_name, rail_docked_label_prefix)
        self.smd3.update(self.header.type)
        self.header.update(self.smd3)

    _ct_to_station_class = {
        0: 9,  # General
        1: 13,  # Mining
        2: 15,  # Support/Trade
        3: 17,  # Cargo/Shopping
        4: 11,  # Attack/Outpost
        5: 12,  # Defence
        6: 10,  # Carrier/Shipyard
        7: 16,  # Scout/Warp Gate
        8: 14,  # Scavenger/Factory
    }

    def set_entity(self, entity_type, entity_class):
        """
        Change entity type
        0: "Ship",
        2: "Station",

        @param entity_type: ship=0/station=2/etc
        @type entity_type: int
        """
        assert entity_type is None or isinstance(entity_type, int)
        assert entity_class is None or isinstance(entity_class, int)
        if entity_type is not None:
            self.smd3.set_type(entity_type)
            self.logic.set_type(entity_type)
            self.header.set_type(entity_type)
            self.update()
            if entity_class is None:
                entity_class = 0
        if entity_class is not None:
            if self.header.type == 0:
                self.header.set_class(entity_class)
            else:
                self.header.set_class(self._ct_to_station_class[entity_class])

    def remove_blocks(self, block_ids):
        """
        Removing all blocks of a specific id

        @param block_ids:
        @type block_ids: set[int]
        """
        self.smd3.remove_blocks(block_ids)
        self.logic.update(self.smd3)
        self.header.update(self.smd3)

    def replace_hull(self, new_hull_type, hull_type=None):
        """
        Replace all blocks of a specific hull type or all hull

        @param new_hull_type:
        @type new_hull_type: int
        @param hull_type:
        @type hull_type: int | None
        """
        self.smd3.replace_hull(new_hull_type, hull_type)
        self.header.update(self.smd3)

    def replace_blocks(self, block_id, replace_id, replace_hp):
        """
        Replace all blocks of a specific id

        @type block_id: int
        @type replace_id: int
        @type replace_hp: int
        """
        compatible = self.are_compatible_blocks(block_id, replace_id)
        self.smd3.replace_blocks(block_id, replace_id, replace_hp, compatible)
        self.header.update(self.smd3)

    def update(self):
        """
        Remove invalid/outdated blocks and exchange docking modules with rails
        """
        entity_type = self.header.type
        self.smd3.update(entity_type)
        self.logic.update(self.smd3)
        self.header.update(self.smd3)

    def auto_hull_shape(self, auto_wedge, auto_tetra, auto_corner, auto_hepta):
        # if self._debug:
        #     self.smd3.auto_hepta_debug()
        #     # self.smd3.auto_wedge_debug()
        #     return
        self.smd3.auto_hull_shape(
            auto_wedge=auto_wedge, auto_tetra=auto_tetra, auto_corner=auto_corner, auto_hepta=auto_hepta)
        self.header.update(self.smd3)

    def move_center_by_block_id(self, block_id):
        """
        Relocate center/core to the position of a hopefully unique block

        @param block_id: block id
        @type block_id: int
        """
        assert isinstance(block_id, int)
        position = self.smd3.search(block_id)
        assert position is not None, "Block id not found: {}".format(block_id)
        distance = self.vector_distance(position, (16, 16, 16))
        if distance == 0:
            return
        direction_vector = self._get_direction_vector_to_center(position)
        self.move_center_by_vector(direction_vector)

    def move_center_by_vector(self, direction_vector):
        """
        Relocate center/core in a direction

        @param direction_vector: vector
        @type direction_vector: int, int, int
        """
        assert isinstance(direction_vector, tuple)
        min_vector, max_vector = self.smd3.move_center(direction_vector, self.header.type)
        self.logic.move_center(direction_vector, self.header.type)
        self.header.set_box(min_vector, max_vector)
        self.header.update(self.smd3)
        self.meta.move_center_by_vector(direction_vector)

    def turn_tilt(self, index_turn_tilt):
        """

        @param index_turn_tilt:
        @type index_turn_tilt: int
        """
        assert 0 <= index_turn_tilt <= 5
        self.logic.tilt_turn(index_turn_tilt)
        min_vector, max_vector = self.smd3.tilt_turn(index_turn_tilt)
        self.header.set_box(min_vector, max_vector)

    def link_salvage_modules(self):
        """
        Automatically link salvage computers to salvage modules
        """
        position_salvage_computers = self.smd3.search_all(4)
        assert len(position_salvage_computers) > 0, "No salvage computer found"
        position_salvage_modules = self.smd3.search_all(24)
        assert len(position_salvage_modules) > 0, "No salvage modules found"
        groups = {}
        salvage_computer_count = len(position_salvage_computers)

        if salvage_computer_count == 1:
            self.logic.set_link(position_salvage_computers.pop(), 24, position_salvage_modules)
            return

        for index in range(salvage_computer_count):
            groups[index] = set()
        for position in position_salvage_modules:
            group_index = (position[0] + position[1]) % salvage_computer_count
            groups[group_index].add(position)
        position_salvage_computers = list(position_salvage_computers)
        for group_index in groups:
            self.logic.set_link(position_salvage_computers[group_index], 24, groups[group_index])

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream blueprint values

        @param output_stream: Output stream
        @type output_stream: fileIO
        """
        self.header.to_stream(output_stream)
        self.logic.to_stream(output_stream)
        self.meta.to_stream(output_stream)
        self.smd3.to_stream(output_stream)
