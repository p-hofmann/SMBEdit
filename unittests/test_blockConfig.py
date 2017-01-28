from unittest import TestCase
from lib.utils.blockconfig import BlockConfig

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: BlockConfig
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self._starmade_dir = "/home/hofmann/Downloads/starmade-launcher-linux-x64/StarMade"

    def setUp(self):
        self.object = BlockConfig()
        return

    def tearDown(self):
        self.object = None
        return

class TestBlockConfig(DefaultSetup):
    def test_from_hardcoded(self):
        self.object.from_hard_coded()

    def test_from_starmade_config(self):
        self.object.read(self._starmade_dir)

    def test_ids_hard_vs_dynamic(self):
        self.object.from_hard_coded()
        block_config = BlockConfig()
        block_config.read(self._starmade_dir)

        unknown_id = set()
        for block in block_config:
            if block.name is None:
                continue
            try:
                block_hard_code = self.object[block.id]
            except:
                unknown_id.add(block.id)

        for block_id in unknown_id:
            print("{} {} {}".format(block_id, block_config[block_id].block_style, block_config[block_id].name))
        self.assertSetEqual(unknown_id, set())

    def test_block_style_hard_vs_dynamic(self):
        self.object.from_hard_coded()
        block_config = BlockConfig()
        block_config.read(self._starmade_dir)

        unknown_id = set()
        unknown_bad_block_style = set()
        for block in block_config:
            try:
                block_hard_code = self.object[block.id]
                if block.block_style != block_hard_code.block_style:
                    unknown_bad_block_style.add(block.id)
            except:
                unknown_id.add(block.id)
        for block_id in unknown_bad_block_style:
            print("{} {}:{} {}".format(block_id, block_config[block_id].block_style, self.object[block_id].block_style, block_config[block_id].name))
        self.assertSetEqual(unknown_bad_block_style, set())

    def test_activatable_hard_vs_dynamic(self):
        self.object.from_hard_coded()
        block_config = BlockConfig()
        block_config.read(self._starmade_dir)

        activatable_id = set()
        ids_with_bad_attribute = set()
        for block in block_config:
            if block.can_activate:
                activatable_id.add(block.id)
            if block.deprecated:
                continue
            try:
                block_hard_code = self.object[block.id]
                if block.can_activate != block_hard_code.can_activate:
                    ids_with_bad_attribute.add(block.id)
            except:
                pass
        # print(", ".join(map(str, activatable_id)))
        for block_id in ids_with_bad_attribute:
            print("{}\t{}:{}\t{}".format(block_id, block_config[block_id].can_activate, self.object[block_id].can_activate, block_config[block_id].name))
        self.assertSetEqual(ids_with_bad_attribute, set())
