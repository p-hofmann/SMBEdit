__author__ = 'Peter Hofmann'
__version__ = '0.0.6'

import os
import shutil
import zipfile
import tempfile
import argparse
import traceback

from lib.validator import Validator
from lib.blueprint import Blueprint


class SMBEdit(Validator):
	"""
	# #######################################
	# ###  StarMade Blueprint Editor
	# #######################################

	Works with StarMade v0.199.257


	@type _tmp_dir: str
	"""

	def __init__(self, is_archived=False, temp_directory=None, logfile=None, verbose=False, debug=False):
		"""
		Constructor of Starmade Blueprint Editor

		@param logfile: file handler or file path to a log file
		@type logfile: file | FileIO | StringIO | basestring
		@param verbose: Not verbose means that only warnings and errors will be past to stream
		@type verbose: bool
		@param debug: Display debug messages
		@type debug: bool

		@rtype: None
		"""
		self._label = "SMBEdit"
		super(SMBEdit, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		assert temp_directory is None or self.validate_dir(temp_directory)
		assert isinstance(is_archived, bool)
		self._is_archived = is_archived
		if not is_archived:
			self._tmp_dir = None
			return
		if temp_directory is None:
			self._tmp_dir = tempfile.mkdtemp(prefix="{}_".format(self._label))
		else:
			self._tmp_dir = tempfile.mkdtemp(prefix="{}_".format(self._label), dir=temp_directory)
		return

	def __exit__(self, type, value, traceback):
		super(SMBEdit, self).__exit__(type, value, traceback)
		if self.validate_dir(self._tmp_dir, silent=True):
			shutil.rmtree(self._tmp_dir)

	# #######################################
	# ###  Read command line arguments
	# #######################################

	_char_to_hull_type = {
		'h': 0,
		's': 1,
		'a': 2,
		'c': 3,
		'z': 4,
	}

	@staticmethod
	def get_parser_options(args=None, version="Prototype"):
		"""
		Parsing of passed arguments.

		@param args: Arguments like sys.argv

		@rtype: any
		"""
		parser = argparse.ArgumentParser(
			usage="python %(prog)s directory_blueprint",
			version="{label} {version}".format(label=SMBEdit._label, version=version),
			description="""
	#######################################
	#    {label}#
	#    Version: {version}#
	#######################################

	A StarMade blueprints editor""".format(
				label=SMBEdit._label.ljust(33),
				version=version.ljust(24)
			),
			formatter_class=argparse.RawTextHelpFormatter)

		parser.add_argument(
			"-verbose", "--verbose",
			action='store_true',
			default=False,
			help="display more information")
		parser.add_argument(
			"-debug", "--debug_mode",
			action='store_true',
			default=False,
			help="show exceptions")
		parser.add_argument(
			"-log", "--logfile",
			default=None,
			type=str,
			help="output will also be written to this log file")
		parser.add_argument(
			"-tmp", "--tmp_dir",
			default=None,
			type=str,
			help="Directory for temporary data in case of 'sment' files.")

		group_input = parser.add_argument_group('optional arguments')
		group_input.add_argument(
			"-s", "--summary",
			action='store_true',
			default=False,
			help="Display summary of blueprint")

		group_input.add_argument(
			"-u", "--update",
			action='store_true',
			default=False,
			help="Remove outdated blocks and replace old docking blocks")

		group_input.add_argument(
			"-aw", "--auto_wedge",
			action='store_true',
			default=False,
			help="Automatically replace hull blocks with wedges on edges.")

		group_input.add_argument(
			"-at", "--auto_tetra",
			action='store_true',
			default=False,
			help="Automatically replace hull blocks with tetras on corners.")

		group_input.add_argument(
			"-ls", "--link_salvage",
			action='store_true',
			default=False,
			help="Link salvage computers to salvage modules")

	# 	group_input.add_argument(
	# 		"-t", "--turn",
	# 		default=None,
	# 		type=int,
	# 		choices=[0, 1, 2, 3, 4, 5],
	# 		help='''turn the ship/station:
	# 	0: "tilt up",
	# 	1: "tilt down",
	# 	2: "turn right",
	# 	3: "turn left",
	# 	4: "tilt right",
	# 	5: "tilt left"
	# ''')

		group_input.add_argument(
			"-et", "--entity_type",
			default=None,
			type=int,
			choices=[0, 1, 2, 3, 4],
			help='''change entity type to:
		0: "Ship",
		1: "Shop",
		2: "Space Station",
		3: "Asteroid",
		4: "Planet",
	''')

		group_input.add_argument(
			"-m", "--move_center",
			default=None,
			type=str,
			help="Either a block id or a directional vector like '0,0,1', for moving center (Core) one block forward.")

		group_input.add_argument(
			"-r", "--replace",
			default=None,
			type=str,
			help="old_id,new_id:hit_points")

		group_input.add_argument(
			"-rh", "--replace_hull",
			default=None,
			type=str,
			help='''{h,s,a,c,z}:{h,s,a,c,z}
			h: Hull
			s: Standard armor
			a: Advanced Armor
			c: Crystal Armor
			z: Hazard Armor''')

		group_input.add_argument(
			"-o", "--path_output",
			default=None,
			type=str,
			help="Output directory of modified blueprint or '*.sment' file path")

		group_input = parser.add_argument_group('required')
		group_input.add_argument(
			"path_input",
			type=str,
			help="Directory of a blue print or sment file path")

		if args is None:
			return parser.parse_args()
		else:
			return parser.parse_args(args)

	@staticmethod
	def _clean_dir_path(directory):
		return directory.rstrip('/').rstrip('\\')

	@staticmethod
	def zip_directory(src_dir, dst):
		assert os.path.isdir(src_dir)
		with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as write_handler:
			SMBEdit.zip_stream(src_dir, write_handler)

	@staticmethod
	def zip_stream(src_dir, output_stream):
		"""

		@param src_dir:
		@type src_dir: str
		@param output_stream:
		@type output_stream: zipfile.ZipFile
		@return:
		"""
		root_path = os.path.dirname(src_dir)
		assert os.path.isdir(src_dir)
		for root, directories, files in os.walk(src_dir):
			for file_name in files:
				file_path = os.path.join(root, file_name)
				relative_path = os.path.relpath(file_path, root_path)
				print relative_path,
				output_stream.write(file_path, arcname=relative_path)

	def run(self, options):
		try:

			path_input = options.path_input
			path_output = options.path_output
			link_salvage = options.link_salvage
			index_turn_tilt = None  # options.turn
			replace_hull = options.replace_hull
			replace = options.replace
			move_center = options.move_center
			update = options.update
			auto_hull_shape = (options.auto_wedge, options.auto_tetra)
			entity_type = options.entity_type
			summary = options.summary

			assert path_output is None or self.validate_dir(path_output, only_parent=True)
			directory_output = None
			if self._is_archived:
				# .sment file
				assert self.validate_file(path_input)
				directory_input = tempfile.mkdtemp(dir=self._tmp_dir)
				with zipfile.ZipFile(path_input, "r") as read_handler:
					read_handler.extractall(directory_input)
				list_of_dir = os.listdir(directory_input)
				assert len(list_of_dir) == 1, "Invalid sment file"
				blueprint_name = list_of_dir[0]
				directory_input = os.path.join(directory_input, blueprint_name)

				if path_output is not None:
					assert path_output.endswith(".sment"), "Expected '*.sment' file ending."
					assert not self.validate_file(path_output, silent=True), "Output file exists. Overwriting files is not allowed, aborting."
					directory_output = os.path.join(tempfile.mkdtemp(dir=self._tmp_dir), blueprint_name)
			else:
				directory_input = path_input
				directory_input = self._clean_dir_path(directory_input)
				if path_output is not None:
					directory_output = self._clean_dir_path(path_output)

			self.run_commands(
				directory_input, directory_output,
				link_salvage, index_turn_tilt, replace_hull, replace, move_center, update, auto_hull_shape, entity_type, summary)

			if path_output is not None and self._is_archived:
				# .sment file
				self._logger.info("Exporting blueprint to:\n{}".format(path_output))
				self.zip_directory(directory_output, path_output)
				assert os.path.exists(path_output), [path_output, directory_output]

		except (KeyboardInterrupt, SystemExit, Exception, ValueError, RuntimeError) as e:
			self._logger.debug("\n{}\n".format(traceback.format_exc()))
			if len(e.args) > 0:
				self._logger.error(e.args[0])
			self._logger.info("Aborted")
		except AssertionError as e:
			if len(e.args) > 0:
				self._logger.error(e.args[0])
			self._logger.info("Aborted")
		else:
			self._logger.info("Finished")

	def run_commands(
		self, directory_input, directory_output,
		link_salvage, index_turn_tilt, replace_hull, replace, move_center, update, auto_hull_shape, entity_type, summary, blueprint_path=None):
		file_names = ["header.smbph", "logic.smbpl", "meta.smbpm"]
		assert self.validate_dir(directory_input, file_names=file_names), "Blueprint directory is invalid, aborting."
		if directory_output is not None:
			assert self.validate_dir(directory_output, only_parent=True, key="-o"), "Output Blueprint directory is invalid, aborting."
			if os.path.exists(directory_output):
				if len(os.listdir(directory_output)) > 0:
					raise Exception("Blueprint found in output directory, aborting to prevent overwriting.")
			else:
				os.mkdir(directory_output)

		if blueprint_path is None:
			blueprint_path = directory_output

		if index_turn_tilt is not None:  # if entity is turned, docked entities are removed
			list_of_folders = os.listdir(directory_input)
			for folder_name in list_of_folders:
				if "ATTACHED_" not in folder_name:
					continue
				directory_src = os.path.join(directory_input, folder_name)
				directory_dst = None
				if directory_output is not None:
					directory_dst = os.path.join(directory_output, folder_name)
				self.run_commands(
					directory_src, directory_dst,
					link_salvage, None, replace_hull, replace, None, update, auto_hull_shape, None, summary,
					blueprint_path=blueprint_path)

		blueprint = Blueprint(
			logfile=self._logfile,
			verbose=self._verbose,
			debug=self._debug,
		)

		blueprint_name = os.path.basename(directory_input)
		self._logger.info("Reading blueprint '{}' ...".format(blueprint_name))
		blueprint.read(directory_input)

		if move_center is not None:
			self._logger.info("Moving center/core of blueprint...")
			if ',' in move_center:  # vector
				direction_vector = [0, 0, 0]
				tmp = move_center.split(',')
				assert len(tmp) == 3, "Bad vector: '{}'".format(move_center)
				for index, value in enumerate(tmp):
					assert isinstance(value, basestring)
					# assert value.isdigit(), "Bad vector: '{}'".format(move_center)
					direction_vector[index] = int(value)
				blueprint.move_center_by_vector(tuple(direction_vector))
			else:  # block id
				assert move_center.isdigit(), "Bad block id: '{}'".format(move_center)
				blueprint.move_center_by_block_id(int(move_center))

		if replace is not None:
			self._logger.info("Replacing blocks...")
			assert isinstance(replace, str)
			assert ',' in replace, "Bad replace: '{}'".format(replace)
			old_block_id, suffix = replace.split(',')
			assert old_block_id.isdigit(), "Bad old block id: '{}'".format(old_block_id)
			old_block_id = int(old_block_id)

			assert ':' in suffix, "Bad replace: '{}'".format(replace)
			replace_id, replace_hp = suffix.split(':')
			assert replace_id.isdigit(), "Bad replace block id: '{}'".format(replace_id)
			assert replace_hp.isdigit(), "Bad replace block hp: '{}'".format(replace_hp)
			replace_id = int(replace_id)
			replace_hp = int(replace_hp)
			blueprint.replace_blocks(old_block_id, replace_id, replace_hp)

		if replace_hull is not None:
			self._logger.info("Replacing hull...")
			assert isinstance(replace_hull, str), "Bad replace hull: '{}'".format(replace_hull)
			assert ':' in replace_hull, "Bad hull replace: '{}'".format(replace_hull)
			old_hull_type, new_hull_type = replace_hull.split(':', 1)
			assert new_hull_type in self._char_to_hull_type, "Bad replace hull type: '{}'".format(new_hull_type)
			new_hull_type = self._char_to_hull_type[new_hull_type]
			if old_hull_type != "":
				assert old_hull_type in self._char_to_hull_type, "Bad hull type: '{}'".format(old_hull_type)
				old_hull_type = self._char_to_hull_type[old_hull_type]
			else:
				old_hull_type = None
			blueprint.replace_hull(new_hull_type, old_hull_type)

		if True in auto_hull_shape:
			self._logger.info("Automatically picking hull shape...")
			blueprint.auto_hull_shape(auto_hull_shape)

		if index_turn_tilt is not None:
			blueprint.turn_tilt(index_turn_tilt)

		if entity_type is not None:
			self._logger.info("Changing entity type and updating blueprint...")
			blueprint.set_entity_type(entity_type)

		if link_salvage:
			self._logger.info("Linking salvage computers/modules...")
			blueprint.link_salvage_modules()

		if update and entity_type is None:
			self._logger.info("Updating blueprint...")
			blueprint.update()

		if summary:
			self._logger.info("Summary of blueprint to stdout")
			blueprint.to_stream()

		if directory_output is not None:
			self._logger.info("Saving blueprint to:\n{}".format(directory_output))
			if blueprint_path is None:
				blueprint.write(directory_output)
				return
			relative_path = os.path.relpath(directory_output, os.path.dirname(blueprint_path))
			blueprint.write(directory_output, relative_path=relative_path)


def main():
	options = SMBEdit.get_parser_options(version=__version__)
	verbose = options.verbose
	debug = options.debug_mode
	logfile = options.logfile
	tmp_dir = options.tmp_dir
	path_input = options.path_input
	is_archived = False
	if path_input.endswith(".sment"):
		is_archived = True
	with SMBEdit(
		is_archived=is_archived,
		temp_directory=tmp_dir,
		logfile=logfile,
		verbose=verbose,
		debug=debug) as manipulator:
		manipulator.run(options)

if __name__ == "__main__":
	main()
