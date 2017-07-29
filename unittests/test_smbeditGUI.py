from unittest import TestCase
from smbeditGUI import main

__author__ = 'Peter Hofmann'


class DefaultSetup(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestSMBEdit(DefaultSetup):
    def test_run(self):
        self.skipTest("Can not manage to install tkinter on circleci")
        main(True)
