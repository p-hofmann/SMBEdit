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


class BlockHandler(object):
    """
    """

    _valid_versions = {0, 1, 2, 3}

    def __init__(self):
        self._basic = StyleBasic(0, 0)
        self._styles = [
            Style0(0, 0),
            Style1Wedge(0, 0),
            Style2Corner(0, 0),
            Style3(0, 0),
            Style4Tetra(0, 0),
            Style5Hepta(0, 0),
            Style6(0, 0)]

    def __call__(self, int_24bit, version=None):
        """
        @type int_24bit: int
        @type version: int

        @rtype: StyleBasic
        """
        assert isinstance(int_24bit, int)
        if version is None:
            version = max(self._valid_versions)
        return self._get_style(int_24bit, version)

    @staticmethod
    def get_max_version():
        return max(BlockHandler._valid_versions)

    def _get_style(self, int_24bit, version=3):
        """

        @type int_24bit: int

        @rtype: StyleBasic
        """
        self._basic(int_24bit, version)
        if self._basic.get_id() == 0:
            return self._basic
        block_style = block_config[self._basic.get_id()].block_style
        self._styles[block_style](int_24bit, version)
        return self._styles[block_style]

block_handler = BlockHandler()
