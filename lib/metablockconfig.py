import csv
import logging
from lxml import etree

logger = logging.getLogger(__name__)


class MetaBlockConfig(type):

    def __init__(cls, name, bases, attrs):
        cls._id_to_block = dict()
        cls._label_to_block = dict()

    def __getattr__(cls, block_id):
        """access to block config from the class"""
        return cls._id_to_block[block_id]

    def __getitem__(cls, int_block_id):
        """access to block config from the class"""
        try:
            return cls._id_to_block[str(int_block_id)]
        except Exception as e:
            logger.error(str(e) + 'unknown block id')
            logger.error(
                'Have you loaded the last version of the Starmade configuration files ?')
            exit()

    def __iter__(cls):
        return iter(cls._id_to_block.values())


class BlockConfig(object, metaclass=MetaBlockConfig):

    """docstring for BlockConfig"""

    def __init__(self, blockTypes_path, blockConfig_path):
        with open(blockTypes_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter='=')
            # Skip the header
            next(csvreader, None)
            next(csvreader, None)
            # and read
            for row in csvreader:
                self._id_to_block[row[1]] = dict(label=row[0], block_id=row[1])
                self._label_to_block[row[0]] = self._id_to_block[row[1]]
        tree = etree.parse(blockConfig_path)
        colors = ["dark grey", "black", "white", "purple", "pink", "blue",
                  "teal", "green", "yellow", "orange", "red", "brown", "grey"]
        shapes = ["wedge", "hepta", "tetra", "corner", "cube"]
        tiers = ["crystal", "standard", "advanced", "hull"]
        slabes = ["1/4", "1/2", "3/4"]
        # fill the flags dict with id values
        for blockConfigNode in tree.findall(".//*/Block"):
            label = blockConfigNode.attrib["type"]
            self._label_to_block[label][
                "name"] = blockConfigNode.attrib["name"]
            self._label_to_block[label][
                "icon"] = blockConfigNode.attrib["icon"]
            self._label_to_block[label][
                "texture_id"] = blockConfigNode.attrib["textureId"]
            self._label_to_block[label]["max_HP"] = int(
                blockConfigNode.find("Hitpoints").text)
            self._label_to_block[label]['can_activate'] = blockConfigNode.find(
                'CanActivate').text == "true"
            self._label_to_block[label][
                'door'] = blockConfigNode.find('Door').text

            self._label_to_block[label]['color'] = "grey"
            self._label_to_block[label]['shape'] = "cube"
            self._label_to_block[label]['tier'] = None
            self._label_to_block[label]['slabe'] = 1.

            name_lower_case = self._label_to_block[label]["name"].lower()

            # Check for color name
            colors = ["dark grey", "black", "white", "purple", "pink", "blue",
                      "teal", "green", "yellow", "orange", "red", "brown"]  # , "grey"]
            for color in colors:
                if color in name_lower_case:
                    self._label_to_block[label]['color'] = color
                    break

            # Check for shape name
            shapes = ["wedge", "hepta", "tetra", "corner"]

            for shape in shapes:
                if shape in name_lower_case:
                    self._label_to_block[label]['shape'] = shape
                    break

            # Check for tier armor name
            tiers = ["crystal", "standard", "advanced", "hull"]

            for tier in tiers:
                if tier in name_lower_case:
                    self._label_to_block[label]['tier'] = tier
                    break

            # Check for slabe
            slabes = ["1/4", "1/2", "3/4"]
            for slabe in slabes:
                if slabe in name_lower_case:
                    values = slabe.split("/")
                    self._label_to_block[label]['slabe'] = float(
                        values[0])/float(values[1])
                    break
