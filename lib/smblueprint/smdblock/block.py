__author__ = 'Peter Hofmann'


from lib.utils.blockconfig import block_config
from lib.smblueprint.smdblock.style.stylebasic import StyleBasic
from lib.smblueprint.smdblock.style.style0 import Style0
from lib.smblueprint.smdblock.style.style1wedge import Style1Wedge
from lib.smblueprint.smdblock.style.style2corner import Style2Corner
from lib.smblueprint.smdblock.style.style3 import Style3
from lib.smblueprint.smdblock.style.style4tetra import Style4Tetra
from lib.smblueprint.smdblock.style.style5hepta import Style5Hepta
from lib.smblueprint.smdblock.style.style6 import Style6


class Block(object):
    """
    """

    _valid_versions = {0, 1, 2, 3}

    def __call__(self, int_24bit, version=None):
        """

        @rtype: int
        """
        if version is None:
            version = max(self._valid_versions)
        return self._get_style(int_24bit, version)

    @staticmethod
    def _get_style(int_24bit, version=3):
        """

        @type int_24bit: int

        @rtype: StyleBasic
        """
        block_style = block_config[StyleBasic(int_24bit, version).get_id()].block_style
        if block_style == 0:
            return Style0(int_24bit, version)
        if block_style == 1:
            return Style1Wedge(int_24bit, version)
        if block_style == 2:
            return Style2Corner(int_24bit, version)
        if block_style == 3:
            return Style3(int_24bit, version)
        if block_style == 4:
            return Style4Tetra(int_24bit, version)
        if block_style == 5:
            return Style5Hepta(int_24bit, version)
        if block_style == 6:
            return Style6(int_24bit, version)
