__author__ = 'Peter Hofmann'


from unittest import TestLoader, TestSuite, TextTestRunner, TextTestResult
from unittests.test_block import TestBlock
from unittests.test_header import TestHeader
from unittests.test_logic import TestLogic
from unittests.test_meta import TestMeta
from unittests.test_smd import TestSmd
from unittests.test_statistics import TestStatistics
import sys


if __name__ == '__main__':
	tests = list()
	tests.append(TestLoader().loadTestsFromTestCase(TestBlock))
	tests.append(TestLoader().loadTestsFromTestCase(TestHeader))
	tests.append(TestLoader().loadTestsFromTestCase(TestLogic))
	tests.append(TestLoader().loadTestsFromTestCase(TestMeta))
	tests.append(TestLoader().loadTestsFromTestCase(TestSmd))
	tests.append(TestLoader().loadTestsFromTestCase(TestStatistics))
	test_suite = TestSuite(tests)
	# TextTestRunner(verbosity=2, buffer=True).run(test_suite)
	test_runner = TextTestRunner(verbosity=2, resultclass=TextTestResult).run(test_suite)
	assert isinstance(test_runner, TextTestResult)
	sys.exit(not test_runner.wasSuccessful())
