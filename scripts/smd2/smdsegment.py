__author__ = 'Peter Hofmann'

import sys
import zlib
import datetime
from bit_and_bytes import BitAndBytes
from blueprintutils import BlueprintUtils
from smdblock import SmdBlock


class SmdSegment(BlueprintUtils, BitAndBytes):

	def __init__(self, segment_size):
		super(SmdSegment, self).__init__()
		self._segment_size = segment_size
		self._blocksize_y = self._segment_size
		self._blocksize_z = self._segment_size * self._segment_size
		self._max_blocks = self._segment_size * self._segment_size * self._segment_size
		self.version = 0
		self.timestamp = 0
		self.position = None
		self.has_valid_data = False
		self.compressed_size = 0
		self.block_index_to_block = {}

	def read(self, input_stream):
		return

	def to_stream(self, output_stream=sys.stdout, extended=False):
		return


class Smd2Segment(SmdSegment):

	def __init__(self):
		super(Smd2Segment, self).__init__(16)

	def read(self, input_stream):
		return
