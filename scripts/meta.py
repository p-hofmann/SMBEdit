__author__ = 'Peter Hofmann'

import os
import sys
import gzip
from bit_and_bytes import BitAndBytes


# #######################################
# ###  META
# #######################################

class Meta(BitAndBytes):

	_file_name = "meta.smbpm"

	_tag_type = {
		1: "Finish",
		2: "SegManager",
		3: "Docking"
	}

	version = ""
	root_tag = None
	is_compressed = False
	blueprints = {}
	tail_data = ""

	def __init__(self):
		super(Meta, self).__init__()
		return

	# #######################################
	# ###  Read
	# #######################################

	def _read_dock_entry(self, input_stream):
		assert isinstance(input_stream, file)
		data = {}
		# string_length = self._read_int_unassigned(input_stream)
		# entry["name"] = input_stream.read(string_length).decode('utf-8')
		name = self._read_string(input_stream)
		print name
		data["position"] = self._read_vector_3si(input_stream)
		print data["position"]
		data["size"] = self._read_vector_3i(input_stream)
		print data["size"]
		data["style"] = self._read_short_int_unassigned(input_stream)
		print data["style"]
		data["orientation"] = self._read_char(input_stream)
		print data["orientation"]
		return name, data

	def _read_docked_blueprints(self, input_stream):
		data = {}
		num_docked = self._read_int_unassigned(input_stream)
		print "Docked", num_docked
		assert 0 <= num_docked < 1000, num_docked
		for index in range(0, num_docked):
			name, dock_entry = self._read_dock_entry(input_stream)
			assert name not in data
			data[name] = dock_entry
		return data

	def _read_tag(self, input_stream):
		"""
		# 0x0 - End of tag struct marker -- no tag name or data follows this
		# 0xD - Start of new tag struct
		# 0xE - Serialized object (not yet implemented here)
		# Finish = 1,
		# SegManager = 2,
		# Docking = 3
		"""
		assert isinstance(input_stream, file)
		entry = dict()
		entry["type"] = self._read_char(input_stream)
		if entry["type"] > 0:
			entry["name"] = self._read_string(input_stream)
		if entry["type"] != 0:
			entry["payload"] = self._read_payload(input_stream, entry["type"])
		return entry

	# TagList
	def _read_payload_list(self, input_stream):
		assert isinstance(input_stream, file)
		entry = dict()
		entry["type"] = self._read_char(input_stream)
		length_list = self._read_int_unassigned(input_stream)
		entry["payload"] = {}
		for index in range(0, length_list):
			entry["payload"][index] = self._read_payload(input_stream, entry["type"])
		return entry

	# TagStructure
	def _read_tag_list(self, input_stream):
		data = {}
		count = 0
		while True:
			tag = self._read_tag(input_stream)
			if tag["type"] == 0:
				break
			data[count] = tag
			count += 1
		return data

	def _read_payload(self, input_stream, data_type):
		if data_type == 0:
			return None
		elif data_type == 1:  # Byte
			return self._read_char(input_stream)
		elif data_type == 2:  # Short
			return self._read_short_int(input_stream)
		elif data_type == 3:  # Int
			return self._read_int(input_stream)
		elif data_type == 4:  # Long
			return self._read_long_long_unassigned(input_stream)
		elif data_type == 5:  # Float
			return self._read_float(input_stream)
		elif data_type == 6:  # Double
			return self._read_double(input_stream)
		elif data_type == 7:  # Byte array
			return self._read_byte_array(input_stream)
		elif data_type == 8:  # String
			return self._read_string(input_stream)
		elif data_type == 9:  # Float vector
			return self._read_vector_3f(input_stream)
		elif data_type == 10:  # int vector
			return self._read_vector_3i(input_stream)
		elif data_type == 11:  # Byte vector
			return self._read_vector_3b(input_stream)
		elif data_type == 12:  # TagList -> Payload List
			return self._read_payload_list(input_stream)
		elif data_type == 13:  # TagStructure -> Tag list
			return self._read_tag_list(input_stream)
		elif data_type == 14:  # Factory registration # factoryId
			return self._read_char(input_stream)
		elif data_type == 15:  # Float4 vector
			return self._read_vector_4f(input_stream)
		else:
			return None

	def _read_tag_root(self, input_stream):
		version = self._read_short_int_unassigned(input_stream)
		print "!!!!!", version
		if version == 0x1f8b:
			input_stream = gzip.GzipFile(fileobj=input_stream)
		tag = self._read_tag(input_stream)
		return version, tag

	def read(self, directory_blueprint):
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'rb') as input_stream:
			self._read_file(input_stream)

	def _read_file(self, input_stream):
		assert isinstance(input_stream, file)
		self.version = self._read_int_unassigned(input_stream)
		while True:
			data_type = self._read_char(input_stream)
			input_stream.read(38)
			# print "XXX", data_type
			if data_type == 1:  # Finish
				break
			elif data_type == 2:  # SegManager
				self.root_tag = self._read_tag_root(input_stream)
				return
			elif data_type == 3:  # Docking
				self.blueprints = self._read_docked_blueprints(input_stream)
				break
		self.tail_data = input_stream.read()

	# #######################################
	# ###  Write
	# #######################################

	def write(self, directory_blueprint):
		file_path = os.path.join(directory_blueprint, self._file_name)
		with open(file_path, 'wb') as output_stream:
			self._write_dummy(output_stream)

	def _write_dummy(self, output_stream):
		self._write_int_unassigned(0, output_stream)
		self._write_char(1, output_stream)

	# #######################################
	# ###  Else
	# #######################################

	def to_stream(self, output_stream=sys.stdout):
		output_stream.write("####\nMETA ({})\n####\n\n".format(self.version))
		output_stream.write("CompressedTag: {}\n\n".format(self.is_compressed))
		output_stream.write("Blueprints: {}\n\n".format(len(self.blueprints)))
		for name, blueprint in self.blueprints.iteritems():
			output_stream.write("{}: #{}\n".format(name, blueprint["position"]))
			output_stream.write("\n")
		output_stream.write("Tail: {} bytes\n".format(len(self.tail_data)))
		output_stream.write("\n")
