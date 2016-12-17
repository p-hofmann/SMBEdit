__author__ = 'Peter Hofmann'

import os
import argparse
import traceback
from scripts.loggingwrapper import DefaultLogging
from blueprint import Blueprint


class SMBlueprintManipulator(DefaultLogging):

	def __init__(self, logfile=None, verbose=False, debug=False):
		"""
		Constructor

		@param logfile: file handler or file path to a log file
		@type logfile: file | FileIO | StringIO | basestring
		@param verbose: Not verbose means that only warnings and errors will be past to stream
		@type verbose: bool
		@param debug: Display debug messages
		@type debug: bool

		@rtype: None
		"""
		self._label = "SMBlueprintManipulator"
		super(SMBlueprintManipulator, self).__init__(
			logfile=logfile,
			verbose=verbose,
			debug=debug)
		return

	# #######################################
	# ###  Read
	# #######################################

	@staticmethod
	def get_parser_options(args=None, version="Prototype"):
		"""
		Parsing of passed arguments.

		@param args: Passed arguemnts

		@return: any
		"""
		parser = argparse.ArgumentParser(
			usage="python %(prog)s directory_blueprint",
			version="BlueprintManipulator {}".format(version),
			description="""
	#######################################
	#    SMBlueprintManipulator             #
	#    Version: {}#
	#######################################

	Manipulation of Starmade blueprints""".format(version.ljust(24)),
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
			"-t", "--turn",
			default=None,
			type=int,
			choices=[0, 1, 2, 3, 4, 5],
			help='''turn the ship/station:
		0: "tilt up",
		1: "tilt down",
		2: "turn right",
		3: "turn left",
		4: "tilt right",
		5: "tilt left"
	''')

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
			"-o", "--directory_output",
			default=None,
			type=str,
			help="Directory of modified blueprint. Will be used as prefix for unique directory name.")

		group_input = parser.add_argument_group('required')
		group_input.add_argument(
			"directory_blueprint",
			type=str,
			help="directory of a blue print")

		if args is None:
			return parser.parse_args()
		else:
			return parser.parse_args(args)

	def run(self, options):
		try:
			directory_blueprint = options.directory_blueprint
			directory_output = options.directory_output
			index_turn_tilt = options.turn
			move_center = options.move_center
			update = options.update
			entity_type = options.entity_type
			summary = options.summary

			assert os.path.exists(directory_blueprint), "Blueprint folder does not exists, aborting."
			assert directory_output is None or not os.path.exists(directory_output), "Output folder exists, aborting."

			blueprint = Blueprint(
				logfile=self._logfile,
				verbose=self._verbose,
				debug=self._debug,
			)

			self._logger.info("Reading blueprint...")
			blueprint.read(directory_blueprint)

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

			if index_turn_tilt is not None:
				blueprint.turn_tilt(index_turn_tilt)

			if entity_type is not None:
				self._logger.info("Changing entity type and updating blueprint...")
				blueprint.set_entity_type(entity_type)

			if update and entity_type is None:
				self._logger.info("Updating blueprint...")
				blueprint.update()

			if summary:
				self._logger.info("Summary of blueprint to stdout")
				blueprint.to_stream()

			if directory_output is not None:
				self._logger.info("Saving blueprint to:\n{}".format(directory_output))
				# Todo: validate parent dir
				blueprint.write(directory_output)

		except (KeyboardInterrupt, SystemExit, Exception, ValueError, RuntimeError) as e:
			self._logger.debug("\n{}\n".format(traceback.format_exc()))
			if len(e.args) > 0:
				self._logger.error(e.args[0])
			self._logger.info("Aborted")
		except AssertionError:
			self._logger.info("Aborted")
		else:
			self._logger.info("Finished")


def main():
	options = SMBlueprintManipulator.get_parser_options()
	verbose = options.verbose
	debug = options.debug_mode
	logfile = options.logfile
	manipulator = SMBlueprintManipulator(
		logfile=logfile,
		verbose=verbose,
		debug=debug)
	manipulator.run(options)

if __name__ == "__main__":
	main()
