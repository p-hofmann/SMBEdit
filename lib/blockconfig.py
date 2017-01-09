import csv
import logging
from lxml import etree

logger = logging.getLogger(__name__)


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
        self.slab = None
        self.tier = None

        self.deprecated = False

    def __str__(self):
        text = ""
        text += "{}\t".format(self.id)
        text += "HP: {}\t".format(self.hit_points)
        text += "style: {}\t".format(self.block_style)
        text += "ca: {}\t".format(self.can_activate)
        text += "color: {}\t".format(self._list_index_to_string(BlockConfig.colors, self.color))
        text += "shape: {}\t".format(self._list_index_to_string(BlockConfig.shapes, self.shape))
        text += "tier: {}\t".format(self._list_index_to_string(BlockConfig.tiers, self.tier))
        text += "slab: {}\t".format(self._list_index_to_string(BlockConfig.slabs, self.slab))
        text += "{}\t".format(self.name)
        return text

    def __repr__(self):
        return self.name

    @staticmethod
    def _list_index_to_string(values, list_index):
        if list_index is None:
            return "''"
        return values[list_index]


class MetaBlockConfig(object):
    """
    docstring for BlockConfig

    @type _id_to_block: dict[int, BlockInfo]
    @type _label_to_block: dict[str, BlockInfo]
    """

    def __init__(self):
        self._id_to_block = dict()
        self._label_to_block = dict()

    def __getattr__(self, block_id):
        """access to block config from the class"""
        return self._id_to_block[block_id]

    def __getitem__(self, int_block_id):
        """access to block config from the class"""
        try:
            return self._id_to_block[int(int_block_id)]
        except Exception as e:
            logger.error(str(e) + 'unknown block id')
            logger.error(
                'Have you loaded the last version of the Starmade configuration files ?')
            exit()

    def __iter__(self):
        for block_id in sorted(self._id_to_block.keys()):
            yield self._id_to_block[block_id]


class BlockConfig(MetaBlockConfig):
    """
    docstring for BlockConfig
    """

    colors = [
        "dark grey", "black", "white", "purple", "pink", "blue",
        "teal", "green", "yellow", "orange", "red", "brown", "grey"
        ]

    shapes = ["cube", "wedge", "corner", "tetra", "hepta"]

    tiers = ["hull", "standard armor", "advanced armor", "crystal armor", "hazard armor"]

    slabs = ["1/4", "1/2", "3/4"]

    def read(self, file_path_block_types, file_path_block_config):
        """

        @param file_path_block_types:
        @type file_path_block_types: str
        @param file_path_block_config:
        @type file_path_block_config: str
        @return:
        """
        with open(file_path_block_types, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter='=')
            # Skip the header
            next(csvreader, None)
            next(csvreader, None)
            # and read
            for row in csvreader:
                type, blockid = row
                blockid = int(blockid)
                self._id_to_block[blockid] = BlockInfo()
                self._id_to_block[blockid].id = blockid
                # dict(label=row[0], block_id=row[1])
                self._label_to_block[type] = self._id_to_block[blockid]

        tree = etree.parse(file_path_block_config)
        # fill the flags dict with id values
        for blockConfigNode in tree.findall(".//*/Block"):
            label = blockConfigNode.attrib["type"]
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
                self._label_to_block[label].slab_ids = map(int, slab_node.text.split(", "))
            self._label_to_block[label].deprecated = blockConfigNode.find('Deprecated').text == "true"

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

            # Check for slabe
            for index, slab in enumerate(BlockConfig.slabs):
                if slab in name_lower_case:
                    self._label_to_block[label].slab = index
                    break
