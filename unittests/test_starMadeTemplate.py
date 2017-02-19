from unittest import TestCase
from lib.smtpl import StarMadeTemplate
from unittests.testinput import template_handler
from lib.utils.blockconfig import block_config

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):
    """
    @type object: StarMadeTemplate
    """

    def __init__(self, methodName='runTest'):
        super(DefaultSetup, self).__init__(methodName)
        self.object = None
        # self._blueprints = blueprint_handler

    def setUp(self):
        self.object = StarMadeTemplate()
        block_config.from_hard_coded()
        # block_config.from_hard_coded()

    def tearDown(self):
        self.object = None
        # if os.path.exists(self.directory_output):
        #     os.rmdir(self.directory_output)


class TestStarMadeTemplate(DefaultSetup):
    def test_read(self):
        for template in sorted(template_handler):
            print('\n\n', template)
            self.object.read(template)
            # self.object.to_stream()
