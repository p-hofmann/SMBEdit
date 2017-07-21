import csv
import os

from xml.etree import ElementTree
from ..common.validator import Validator
from .blockconfighardcoded import BlockConfigHardcoded
from .blueprintentity import BlueprintEntity, SHIP


class BlockInfo(object):

    def __init__(self):
        self.id = 0
        self.name = None
        self.icon = None
        self.hit_points = 0
        self.can_activate = False
        self.block_style = 0

        self.texture_id = None
        self.armour = 0
        self.armor_hp_contribution = 0
        self.structure_hp_contribution = 0
        # ExplosionAbsorbtion ??
        self.mass = 0
        self.volume = 0
        self.individual_sides = 0
        self.slab_ids = None

        self.color = None
        self.shape = None
        self.tier = None

        self.deprecated = False
        self.is_station_block = False

    def __str__(self):
        text = ""
        text += "{}\t".format(self.id)
        text += "HP: {}\t".format(self.hit_points)
        text += "style: {}\t".format(self.block_style)
        text += "ca: {}\t".format(self.can_activate)
        text += "color: {}\t".format(self._list_index_to_string(BlockConfig.colors, self.color))
        text += "shape: {}\t".format(self._list_index_to_string(BlockConfig.shapes, self.shape))
        text += "tier: {}\t".format(self._list_index_to_string(BlockConfig.tiers, self.tier))
        text += "{}\t".format(self.name)
        return text

    def __repr__(self):
        return self.name

    def is_hull(self):
        """
        @rtype: bool
        """
        return self.tier is not None

    def is_rail(self):
        """
        @rtype: bool
        """
        return BlockConfigHardcoded.is_rail(self.id)

    def is_docking(self):
        """
        @rtype: bool
        """
        return self.id in BlockConfigHardcoded.docking_to_rails

    def get_rail_equivalent(self):
        """
        @rtype: int | None
        """
        assert self.is_docking(), "Not docking block"
        return BlockConfigHardcoded.docking_to_rails[self.id]

    def is_valid(self, entity_type=0):
        """
        Test if an id is outdated or not valid for a specific entity type

        @param entity_type:
        @type entity_type: int

        @return:
        @rtype: bool
        """
        assert entity_type in BlueprintEntity.entity_types
        if BlockConfigHardcoded.is_deprecated(self.id):
            return False
        if entity_type == SHIP and BlockConfigHardcoded.is_station(self.id):
            return False
        if entity_type != SHIP and self.id == 1:
            return False
        return True

    def get_details(self):
        """
        Return detail ids
        @rtype: (int|None,int|None,int|None)
        """
        return self.tier, self.color, self.shape

    @staticmethod
    def _list_index_to_string(values, list_index):
        if list_index is None:
            return "''"
        return values[list_index]


class SuperBlockConfig(object):
    """
    docstring for BlockConfig

    @type _id_to_block: dict[int, BlockInfo]
    @type _label_to_block: dict[str, BlockInfo]
    """

    def __init__(self):
        self._id_to_block = dict()
        self._label_to_block = dict()

    def __getattr__(self, block_id):
        """
        access to block config from the class

        @rtype: BlockInfo
        """
        return self._id_to_block[block_id]

    def __getitem__(self, int_block_id):
        """
        access to block config from the class

        @rtype: BlockInfo
        """
        try:
            return self._id_to_block[int(int_block_id)]
        except KeyError as e:
            msg = 'Unknown block id: {}. '.format(int_block_id)
            msg += 'Have you pointed "-sm" to latest version of StarMade?'
            raise KeyError(msg)

    def __iter__(self):
        """
        access to block config from the class

        @rtype:
        """
        for block_id in sorted(self._id_to_block):
            yield self._id_to_block[block_id]


class BlockConfig(SuperBlockConfig, ):
    """
    docstring for BlockConfig

    @type _hulls_dict: dict[int, dict[int, dict[int, int]]]
    """

    _hulls_dict = None

    def _make_hulls_dict(self):
        self._hulls_dict = {}
        for block_id in self._id_to_block:
            if not self._id_to_block[block_id].is_hull():
                continue
            hull_type = self._id_to_block[block_id].tier
            color = self._id_to_block[block_id].color
            shape_id = self._id_to_block[block_id].shape
            if hull_type not in self._hulls_dict:
                self._hulls_dict[hull_type] = {}
            if color not in self._hulls_dict[hull_type]:
                self._hulls_dict[hull_type][color] = {}
            self._hulls_dict[hull_type][color][shape_id] = block_id

    def get_block_id_by_details(self, hull_type, color, shape_id):
        if self._hulls_dict is None:
            self._make_hulls_dict()
        return self._hulls_dict[hull_type][color][shape_id]

    colors = [
        "dark grey", "black", "white", "purple", "pink", "blue",
        "teal", "green", "yellow", "orange", "red", "brown", "grey"
        ]

    shapes = ["cube", "wedge", "corner", "tetra", "hepta", "1/4", "1/2", "3/4"]

    tiers = ["hull", "standard armor", "advanced armor", "crystal armor", "hazard armor"]

    def get_shape_id(self, name):
        assert name.lower() in self.shapes, "Unknown shape: {}".format(name)
        return self.shapes.index(name.lower())

    def from_hard_coded(self):
        for block_id, name in BlockConfigHardcoded.items():
            self._id_to_block[block_id] = BlockInfo()
            self._id_to_block[block_id].id = block_id
            self._id_to_block[block_id].name = name
            self._id_to_block[block_id].hit_points = 1
            if self._id_to_block[block_id].is_rail() or block_id == 663:
                self._id_to_block[block_id].hit_points = 100
            self._id_to_block[block_id].can_activate = BlockConfigHardcoded.is_activatable_block(block_id)
            self._id_to_block[block_id].deprecated = BlockConfigHardcoded.is_deprecated(block_id)
            try:
                self._id_to_block[block_id].block_style = BlockConfigHardcoded.get_block_style(block_id)
            except LookupError as e:
                # TODO: output a warning
                self._id_to_block[block_id].block_style = 0

            name_lower_case = self._id_to_block[block_id].name.lower()

            # Check for color name
            if "dark grey" in name_lower_case:
                self._id_to_block[block_id].color = self.colors.index("dark grey")
            else:
                for index, color in enumerate(BlockConfig.colors):
                    if color in name_lower_case:
                        self._id_to_block[block_id].color = index
                        break

            # Check for shape name
            self._id_to_block[block_id].shape = 0
            for index, shape in enumerate(BlockConfig.shapes):
                if shape in name_lower_case:
                    self._id_to_block[block_id].shape = index
                    break

            # Check for tier armor name
            for index, tier in enumerate(BlockConfig.tiers):
                if tier in name_lower_case:
                    self._id_to_block[block_id].tier = index
                    self._id_to_block[block_id].hit_points = BlockConfigHardcoded.get_hp_by_hull_type(index)
                    break

    def read(self, directory_starmade):
        """

        @param directory_starmade: StarMade directory
        @type directory_starmade: str
        """
        validator = Validator()
        assert validator.validate_dir(directory_starmade)
        directory_config = os.path.join(directory_starmade, "data", "config")

        file_path_block_types = os.path.join(directory_config, "BlockTypes.properties")
        file_path_block_config = os.path.join(directory_config, "BlockConfig.xml")
        assert validator.validate_file(file_path_block_config)
        assert validator.validate_file(file_path_block_types)
        self._read(file_path_block_types, file_path_block_config)

    def _read(self, file_path_block_types, file_path_block_config):
        """

        @param file_path_block_types:
        @type file_path_block_types: str
        @param file_path_block_config:
        @type file_path_block_config: str
        """
        with open(file_path_block_types, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter='=')
            # Skip the header
            next(csvreader, None)
            next(csvreader, None)
            # and read
            for block_type, block_id in csvreader:
                block_type = block_type.strip()
                block_id = block_id.strip()
                block_id = int(block_id)
                self._id_to_block[block_id] = BlockInfo()
                self._id_to_block[block_id].id = block_id
                # dict(label=row[0], block_id=row[1])
                self._label_to_block[block_type] = self._id_to_block[block_id]

        tree = ElementTree.parse(file_path_block_config)
        # fill the flags dict with id values
        for blockConfigNode in tree.findall(".//*/Block"):
            label = blockConfigNode.attrib["type"]
            if label not in self._label_to_block:
                print("Unknown label: {}".format(label))
                continue
            try:
                self._label_to_block[label].name = blockConfigNode.attrib["name"]
                self._label_to_block[label].icon = blockConfigNode.attrib["icon"]
                self._label_to_block[label].texture_id = blockConfigNode.attrib["textureId"]
                self._label_to_block[label].hit_points = int(blockConfigNode.find("Hitpoints").text)
                self._label_to_block[label].can_activate = blockConfigNode.find('CanActivate').text == "true"
                # self._label_to_block[label]['door'] = blockConfigNode.find('Door').text
                self._label_to_block[label].block_style = int(blockConfigNode.find("BlockStyle").text)

                self._label_to_block[label].armour = float(blockConfigNode.find("Armour").text)
                self._label_to_block[label].armor_hp_contribution = int(blockConfigNode.find("ArmorHPContribution").text)
                self._label_to_block[label].structure_hp_contribution = int(blockConfigNode.find("StructureHPContribution").text)
                # ExplosionAbsorbtion ??
                self._label_to_block[label].mass = float(blockConfigNode.find("Mass").text)
                self._label_to_block[label].volume = float(blockConfigNode.find("Volume").text)
                self._label_to_block[label].individual_sides = int(blockConfigNode.find("IndividualSides").text)
                slab_node = blockConfigNode.find("SlabIds")
                if slab_node is not None:
                    self._label_to_block[label].slab_ids = list(map(int, slab_node.text.split(", ")))
                self._label_to_block[label].deprecated = blockConfigNode.find('Deprecated').text == "true"
            except AttributeError:
                import sys
                sys.stderr.write("WARNING: [BlockConfig] Could not parse: {}\n".format(label))
                continue

            name_lower_case = self._label_to_block[label].name.lower()
            # Check for color name
            if "dark grey" in name_lower_case:
                self._label_to_block[label].color = "dark grey"
            else:
                for index, color in enumerate(BlockConfig.colors):
                    if color in name_lower_case:
                        self._label_to_block[label].color = index
                        break

            # Check for shape name
            self._label_to_block[label].shape = 0
            for index, shape in enumerate(BlockConfig.shapes):
                if shape in name_lower_case:
                    self._label_to_block[label].shape = index
                    break

            # Check for tier armor name
            for index, tier in enumerate(BlockConfig.tiers):
                if tier in name_lower_case:
                    self._label_to_block[label].tier = index
                    break

block_config = BlockConfig()
