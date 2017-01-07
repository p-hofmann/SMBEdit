__author__ = 'Peter Hofmann'

import sys
from lib.blueprintutils import BlueprintUtils
from lib.meta.tagmanager import TagPayload, TagList


class RailDockedEntity(object):
	"""
	Handling rail docked entity tag structure

	@type _location: tuple[int]
	"""

	def __init__(self):
		self._label = ""
		self._location = (0, 0, 0)
		self._block_id = 0
		self._unknown_byte_10_14 = 0
		self._unknown_byte_0 = 1
		self._unknown_byte_1 = 100
		return

	def set(self, label, location, block_id, unknown_byte):
		"""

		@param label:
		@type label: str
		@param location:
		@type location: tuple[int]
		@param block_id:
		@type block_id: int
		@param unknown_byte:
		@type unknown_byte: int
		"""
		self._label = label
		self._location = location
		self._block_id = block_id
		self._unknown_byte_10_14 = unknown_byte

	def get_block_id(self):
		"""
		@rtype: int
		"""
		return self._block_id

	def from_tag(self, entity_tag):
		"""
		@type entity_tag: TagList
		"""
		tag_list = entity_tag.get_list()
		self._label = tag_list[0].payload
		self._location = tag_list[1].payload
		self._block_id = tag_list[2].payload
		self._unknown_byte_10_14 = tag_list[3].payload
		self._unknown_byte_0 = tag_list[4].payload
		self._unknown_byte_1 = tag_list[5].payload

	def to_tag(self):
		"""
		-8: ENTITY_SHIP_Skallagrim_1483048232229,
		-10: (16, 15, 16),
		-2: 662,
		-1: 10,  // sometimes 14
		-1: 1,
		-1: 100,

		@rtype: TagList
		"""
		tag_list = TagList()
		tag_list.add(TagPayload(-8, None, self._label))
		tag_list.add(TagPayload(-10, None, self._location))
		tag_list.add(TagPayload(-2, None, self._block_id))
		tag_list.add(TagPayload(-1, None, self._unknown_byte_10_14))
		# seemingly static unknown stuff
		tag_list.add(TagPayload(-1, None, self._unknown_byte_0))
		tag_list.add(TagPayload(-1, None, self._unknown_byte_1))
		return tag_list

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream values

		@param output_stream: Output stream
		@type output_stream: fileIO[str]
		"""
		output_stream.write("{}\t".format(self._location))
		output_stream.write("{}\t".format(self._block_id))
		output_stream.write("{}\n".format(self._label))


class RailDockedEntityLink(object):
	"""
	Handling rail docked entity tag structure

	@type _entity_main: RailDockedEntity
	@type _entity_docked: RailDockedEntity
	@type _docked_entity_location: tuple[int]
	@type _unknown_matrix_0: list[list[int]]
	@type _unknown_matrix_1: list[list[int]]
	@type _unknown_matrix_2: list[list[int]]
	"""

	def __init__(self):
		self._entity_main = None
		self._entity_docked = None
		self._docked_entity_location = (0, 0, 0)
		self._unknown_matrix_0 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
		self._unknown_matrix_1 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
		self._unknown_matrix_2 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
		self._unknown_byte_0 = 0
		self._unknown_byte_1 = 0
		self._unknown_byte_2 = 0
		return

	def set(self, docked_entity_location, entity_main, entity_docked):
		"""

		@type entity_main: RailDockedEntity
		@type entity_docked: RailDockedEntity
		@type docked_entity_location: tuple[int]
		"""
		assert BlueprintUtils.is_rail(entity_main.get_block_id()), "Expected Rail id but got {}.".format(
			entity_docked.get_block_id())
		assert entity_docked.get_block_id() == 663, "Expected Rail Docker id but got {}.".format(
			entity_docked.get_block_id())
		self._entity_main = entity_main
		self._entity_docked = entity_docked
		self._docked_entity_location = docked_entity_location

	def from_tag(self, entity_link_tag):
		"""
		@type entity_link_tag: TagList
		"""
		tag_list = entity_link_tag.get_list()
		self._entity_main = RailDockedEntity()
		self._entity_main.from_tag(tag_list[0])
		self._entity_docked = RailDockedEntity()
		self._entity_docked.from_tag(tag_list[1])
		self._unknown_matrix_0 = tag_list[2].payload
		self._unknown_matrix_1 = tag_list[3].payload
		self._docked_entity_location = tag_list[4]
		self._unknown_matrix_2 = tag_list[5].payload
		self._unknown_byte_0 = tag_list[6].payload
		self._unknown_byte_1 = tag_list[7].payload
		self._unknown_byte_2 = tag_list[8].payload

	def to_tag(self):
		"""
		# entity_entry
		-13:  {}		// "Rail Basic" 	Main entity
		# entity_entry
		-13:  {}		// "Rail Docker"	Docked entity
		-16: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
		-16: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
		-10: (16, 14, 16),
		-16: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]],
		-1: 0,
		-1: 0,
		-1: 0,

		@rtype: TagList
		"""
		link_tag = TagList()
		link_tag.add(self._entity_main.to_tag())
		link_tag.add(self._entity_docked.to_tag())
		link_tag.add(TagPayload(-16, None, self._unknown_matrix_0))
		link_tag.add(TagPayload(-16, None, self._unknown_matrix_1))
		link_tag.add(TagPayload(-10, None, self._docked_entity_location))
		link_tag.add(TagPayload(-16, None, self._unknown_matrix_2))
		link_tag.add(TagPayload(-1, None, self._unknown_byte_0))
		link_tag.add(TagPayload(-1, None, self._unknown_byte_1))
		link_tag.add(TagPayload(-1, None, self._unknown_byte_2))
		return link_tag

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream values

		@param output_stream: Output stream
		@type output_stream: fileIO[str]
		"""
		output_stream.write("Location: {}\n".format(self._docked_entity_location))
		output_stream.write("Main:\t")
		output_stream.write(self._entity_main.to_stream(output_stream))
		output_stream.write("Docked:\t")
		output_stream.write(self._entity_main.to_stream(output_stream))


class RailDockedEntityLinks(object):
	"""
	Handling rail docked entity tag structure

	@type _list_links: list[RailDockedEntityLink]
	"""

	def __init__(self):
		self._list_links = []
		return

	def set(self, links):
		"""
		@type links: list[RailDockedEntityLink]
		"""
		self._list_links = links

	def from_tag(self, entity_link_tag):
		"""
		@type entity_link_tag: TagList
		"""
		tag_list = entity_link_tag.get_list()
		number_of_links = tag_list[0].payload
		for tag_index in range(number_of_links):
			tag_list_link = tag_list[tag_index+1]
			assert isinstance(tag_list_link, TagList)
			link = RailDockedEntityLink()
			link.from_tag(tag_list_link)
			self._list_links.append(link)

	def to_tag(self):
		"""
		-13: {
				-1: 1,
				-13:  { #RailDockedEntityLink }
				-13:  {}
			}

		@rtype: TagList
		"""
		link_tag_list = TagList()
		link_tag_list.add(TagPayload(-1, None, len(self._list_links)))
		for link in self._list_links:
			link_tag_list.add(link.to_tag())
		link_tag_list.add(TagList())  # why is here a empty tag list? No clue!
		return link_tag_list

	def to_stream(self, output_stream=sys.stdout):
		"""
		Stream values

		@param output_stream: Output stream
		@type output_stream: fileIO[str]
		"""
		for link in self._list_links:
			link.to_stream(output_stream)
			output_stream.write("\n")
