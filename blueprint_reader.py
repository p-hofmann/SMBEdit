__author__ = 'Peter Hofmann'

import sys
import os
import argparse
from blueprint import Blueprint


def _get_parser_options(args=None, version="Prototype"):
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
#    BlueprintManipulator             #
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
		help="display summary of blueprint")

	group_input.add_argument(
		"-u", "--update",
		action='store_true',
		default=False,
		help="Remove outdated blocks and replace old docking blocks")

	group_input.add_argument(
		"-t", "--entity_type",
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

	# ##########
	# i/o
	# ##########

	group_input = parser.add_argument_group('required')
	group_input.add_argument(
		"directory_blueprint",
		type=str,
		help="directory of a blue print")

	if args is None:
		return parser.parse_args()
	else:
		return parser.parse_args(args)


def main():
	options = _get_parser_options()
	verbose = options.verbose
	debug = options.debug_mode
	logfile = options.logfile
	directory_blueprint = options.directory_blueprint
	directory_output = options.directory_output
	move_center = options.move_center
	update = options.update
	entity_type = options.entity_type
	summary = options.summary

	assert directory_output is None or not os.path.exists(directory_output), "Output folder exists, aborting."

	blueprint = Blueprint(
		logfile=logfile,
		verbose=verbose,
		debug=debug,
	)

	blueprint.read(directory_blueprint)

	if move_center is not None:
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

	if entity_type is not None:
		blueprint.set_entity_type(entity_type)

	if update:
		blueprint.update()

	if summary:
		blueprint.to_string(not verbose)

	if directory_output is not None:
		# Todo: validate parent dir
		blueprint.write(directory_output)

main()
