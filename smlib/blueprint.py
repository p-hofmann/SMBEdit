__author__ = 'Peter Hofmann'

import os
import sys
import operator

from .common.loggingwrapper import DefaultLogging
from .utils.blockconfig import block_config
from .utils.autoshape import AutoShape
from .utils.periphery import Periphery
from .utils.annotate import Annotate
from .utils.replace import Replace
from .utils.vector import Vector
from .smblueprint.header import Header
from .smblueprint.logic import Logic
from .smblueprint.meta.meta import Meta
from .smblueprint.smd3.smd import Smd
from .smblueprint.smdblock.blockpool import block_pool
from .utils.blueprintentity import BlueprintEntity


class Blueprint(DefaultLogging):
    """

    @type header: Header
    @type logic: Logic
    @type meta: Meta
    @type smd3: Smd
    @type _annotate: Annotate
    @type _entity_name: str

    """

    def __init__(self, entity_name, logfile=None, verbose=False, debug=False):
        """
        Constructor

        @param logfile: file handler or file path to a log file
        @type logfile: file | FileIO | StringIO | str
        @param verbose: Not verbose means that only warnings and errors will be past to stream
        @type verbose: bool
        @param debug: Display debug messages
        @type debug: bool

        @rtype: None
        """
        super(Blueprint, self).__init__(label="Blueprint", logfile=logfile, verbose=verbose, debug=debug)
        self.header = Header(logfile=logfile, verbose=verbose, debug=debug)
        self.logic = Logic(logfile=logfile, verbose=verbose, debug=debug)
        self.meta = Meta(logfile=logfile, verbose=verbose, debug=debug)
        self.smd3 = Smd(logfile=logfile, verbose=verbose, debug=debug)
        self._annotate = None
        self._entity_name = entity_name
        return

    def __del__(self):
        del self.header
        del self.logic
        del self.meta
        del self.smd3

    # #######################################
    # ###  Read
    # #######################################

    def read(self, directory_blueprint):
        """
        Read blueprint from a directory

        @param directory_blueprint: /../StarMade/blueprints/blueprint_name/
        @type directory_blueprint: str
        """
        self.header = Header(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        self.logic = Logic(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        self.meta = Meta(logfile=self._logfile, verbose=self._verbose, debug=self._debug)
        self.smd3 = Smd(logfile=self._logfile, verbose=self._verbose, debug=self._debug)

        self.header.read(directory_blueprint)
        self.logic.read(directory_blueprint)
        self.meta.read(directory_blueprint)
        self.smd3.read(directory_blueprint)

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

    def replace_outdated_docker_modules(self, rail_docked_label_prefix, is_docked_entity):
        rail_docker_id = 663
        if is_docked_entity and self.smd3.search(rail_docker_id) is None:
            self._logger.info("Adding 'Rail docker' to docked entity.")
            block = block_pool(rail_docker_id).get_modified_block(
                block_id=rail_docker_id, axis_rotation=2, rotations=2)
            position_below_core = (16, 15, 16)
            self.smd3.add(position_below_core, block)
            self.header.update(self.smd3)

        if not self.meta.has_old_docked_entities():
            return
        self._logger.info("Replacing outdated docker modules")
        self.meta.update_docked_entities(self.smd3, self._entity_name, rail_docked_label_prefix)
        self.smd3.update()
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
            elif self.header.type == 2:
                self.header.set_class(self._ct_to_station_class[entity_class])
            else:
                entity_class = list(BlueprintEntity.entity_classification[entity_type].keys())[0]
                self.header.set_class(entity_class)

    @staticmethod
    def rotate_position(position, axis=None, number=0):
        """
        Rotate the position in the plane perpendicular to the given axis
 
        @type position: (int, int, int)
        @param axis: rotation axis {x, y, z}
        @type axis: str
        @param number: number of 90 degrees rotation {0, 1, 2, 3}
        @type number: int
        """ 
 
        # rotate the position if needed
 
        number %= 4
 
        axes = dict(x=(1, 2), y=(2, 0), z=(0, 1))

        if (number == 0) or (axis not in axes):
            return position
 
        # tuples are immutable. Convert to a list before processing
        position = list(position)
        if number == 2:
            position[axes[axis][0]] *= -1
            position[axes[axis][1]] *= -1
 
        if number == 1:
            position[axes[axis][0]], position[axes[axis][1]] = position[axes[axis][1]], -position[axes[axis][0]]
        else:
            position[axes[axis][0]], position[axes[axis][1]] = -position[axes[axis][1]], position[axes[axis][0]]
        return position

    def add_blocks(self, block_id, positions,
                   rotations=None, offset=[0, 0, 0],
                   rotation_axis=None, rotation_number=0):
        """
        Add blocks with a specific ID with/at different rotations/positions
        Note: since this function is design to create the most recent
        blueprints, it works only with the Segment-data v3

        @type block_id: int
        @type positions: list[(int, int, int)] | set[(int, int, int)]
        @type rotations: list[int]
        @param offset: if blocks centered around origin (0, 0, 0) then offset (16, 16, 16)
        @type offset: (int, int, int)
        """
        # check if block_id is known
        assert block_id in block_config, "Unknown block id: {}".format(block_id)
        for idx_position, position in enumerate(positions):
            if rotations:
                rotation = rotations[idx_position]
                assert rotation < 32, "Invalid rotation: {}".format(rotation)  # (1 << 5)
                # the rotations correspond to the last 5 bits of the state (int_24)
                block_id += (rotation << 19)
            new_block = block_pool(block_id)
            self.smd3.add_block(new_block,
                                tuple(map(operator.add,
                                          self.rotate_position(position, axis=rotation_axis, number=rotation_number),
                                          offset)),)

        self.logic.update(self.smd3)
        self.header.update(self.smd3)

    def remove_blocks(self, block_ids):
        """
        Removing all blocks of a specific id

        @param block_ids:
        @type block_ids: set[int]
        """
        self.smd3.remove_blocks(block_ids)
        self.logic.update(self.smd3)
        self.header.update(self.smd3)

    def reset_ship_hull_shape(self):
        periphery = Periphery(self.smd3.get_block_list())
        if self._annotate is None:
            self._logger.info("Tracing entity boundary, this can take some time...")
            self._annotate = Annotate(self.smd3.get_block_list(), periphery)
            min_position, max_position = self.smd3.get_min_max_vector()
            # start_position = Vector.subtraction(min_position, (1, 1, 1))
            # self._annotate.flood(start_position, min_position, max_position)
            self._annotate.calc_boundaries(min_position, max_position)
            self._logger.info("Tracing done.")
        marked, border = self._annotate.get_data()
        periphery.set_annotation(marked=marked, border=border)
        replace = Replace(self.smd3.get_block_list())
        replace.reset_hull_shape(border)
        self.header.update(self.smd3)

    def replace_blocks_hull(self, new_hull_type, hull_type=None):
        """
        Replace all blocks of a specific hull type or all hull

        @param new_hull_type:
        @type new_hull_type: int
        @param hull_type:
        @type hull_type: int | None
        """
        replace = Replace(self.smd3.get_block_list())
        replace.replace_hull(new_hull_type, hull_type)
        self.header.update(self.smd3)

    def replace_blocks(self, block_id, replace_id):
        """
        Replace all blocks of a specific id

        @type block_id: int
        @type replace_id: int
        """
        compatible = block_config[block_id].block_style == block_config[replace_id].block_style
        replace = Replace(self.smd3.get_block_list())
        replace.replace_blocks(block_id, replace_id, compatible)
        self.header.update(self.smd3)

    def update(self):
        """
        Remove invalid/outdated blocks and exchange docking modules with rails
        """
        self.smd3.update()
        self.logic.update(self.smd3)
        self.header.update(self.smd3)

    def auto_hull_shape(self, auto_wedge=False, auto_tetra=False, auto_corner=False, auto_hepta=False):
        # if self._debug:
        #     self.smd3.auto_hepta_debug()
        #     # self.smd3.auto_wedge_debug()
        #     return
        periphery = Periphery(self.smd3.get_block_list())
        if self._annotate is None:
            self._logger.info("Tracing entity boundary, this can take some time...")
            self._annotate = Annotate(self.smd3.get_block_list(), periphery)
            min_position, max_position = self.smd3.get_min_max_vector()
            # start_position = Vector.subtraction(min_position, (1, 1, 1))
            # self._annotate.flood(start_position, min_position, max_position)
            self._annotate.calc_boundaries(min_position, max_position)
            self._logger.info("Tracing done.")
        marked, border = self._annotate.get_data()
        periphery.set_annotation(marked=marked, border=border)
        auto_shape = AutoShape(self.smd3.get_block_list(), periphery)
        auto_shape.auto_hull_shape(
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
        distance = Vector.distance(position, (16, 16, 16))
        if distance == 0:
            return
        direction_vector = Vector.get_direction_vector_to_center(position)
        self.move_center_by_vector(direction_vector)

    def move_center_by_vector(self, direction_vector):
        """
        Relocate center/core in a direction

        @param direction_vector: vector
        @type direction_vector: tuple[int]
        """
        assert isinstance(direction_vector, tuple)
        self.smd3.move_center(direction_vector)
        min_vector, max_vector = self.smd3.get_min_max_vector()
        self.logic.move_center(direction_vector, self.header.type)
        self.header.set_box(min_vector, max_vector)
        self.header.update(self.smd3)
        self.meta.move_center_by_vector(direction_vector)

    def mirror_axis(self, axis_index=0, reverse=False):
        """
        Relocate center/core in a direction

        @param axis_index:  0: x left to right
                            1: y top to bottom
                            2: z front to back
        @type axis_index: int
        @param reverse: reverse mirror direction
        @type reverse: bool
        """
        self.smd3.mirror(axis_index=axis_index, reverse=reverse)
        self.logic.mirror(axis_index=axis_index, reverse=reverse)
        min_vector, max_vector = self.smd3.get_min_max_vector()
        self.header.set_box(min_vector, max_vector)
        self.header.update(self.smd3)
        self.logic.update(self.smd3)
        # self.meta.mirror(axis_index=axis_index, reverse=reverse)

    def turn_tilt(self, index_turn_tilt):
        """
        0: # tilt up
        1: # tilt down
        2: # turn right
        3: # turn left
        4: # tilt right
        5: # tilt left

        @param index_turn_tilt:
        @type index_turn_tilt: int
        """
        assert 0 <= index_turn_tilt <= 5
        self.logic.tilt_turn(index_turn_tilt)
        self.smd3.tilt_turn(index_turn_tilt)
        min_vector, max_vector = self.smd3.get_min_max_vector()
        self.header.set_box(min_vector, max_vector)
        self.header.update(self.smd3)
        self.logic.update(self.smd3)

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
