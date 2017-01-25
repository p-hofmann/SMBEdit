__author__ = 'Peter Hofmann'
__version__ = '0.1.2'

import os
import sys
import zipfile
import traceback

from lib.argumenthandler import ArgumentHandler
from lib.utils.blockconfig import block_config
from lib.blueprint import Blueprint


class SMBEdit(ArgumentHandler):
    """
    # #######################################
    # ###  StarMade Blueprint Editor
    # #######################################

    Works with blueprints made by StarMade v0.199.257
    """

    def __init__(self, options, logfile=None, verbose=False, debug=False):
        """
        Constructor of Starmade Blueprint Editor

        @param logfile: file handler or file path to a log file
        @type logfile: file | str
        @param verbose: Not verbose means that only warnings and errors will be past to stream
        @type verbose: bool
        @param debug: Display debug messages
        @type debug: bool

        @rtype: None
        """
        self._label = "SMBEdit"
        super(SMBEdit, self).__init__(
            options=options,
            logfile=logfile,
            verbose=verbose,
            debug=debug)

    def __exit__(self, type, value, traceback):
        super(SMBEdit, self).__exit__(type, value, traceback)

    @staticmethod
    def get_label():
        return "SMBEdit"

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
                output_stream.write(file_path, arcname=relative_path)

    def _move_center_or_core(self, blueprint):
        """
        @type blueprint: Blueprint
        """
        if ',' in self._move_center:  # vector
            direction_vector = [0, 0, 0]
            tmp = self._move_center.split(',')
            assert len(tmp) == 3, "Bad vector: '{}'".format(self._move_center)
            for index, value in enumerate(tmp):
                assert isinstance(value, str)
                # assert value.isdigit(), "Bad vector: '{}'".format(move_center)
                direction_vector[index] = int(value)
            blueprint.move_center_by_vector(tuple(direction_vector))
        else:  # block id
            assert self._move_center.isdigit(), "Bad block id: '{}'".format(self._move_center)
            blueprint.move_center_by_block_id(int(self._move_center))

    def _replace_blocks(self, blueprint):
        """
        @type blueprint: Blueprint
        """
        assert isinstance(self._replace, str)
        assert ':' in self._replace, "Bad replace: '{}'".format(self._replace)
        old_block_id, replace_id = self._replace.split(':')
        assert old_block_id.isdigit(), "Bad old block id: '{}'".format(old_block_id)
        assert replace_id.isdigit(), "Bad replace block id: '{}'".format(replace_id)
        old_block_id = int(old_block_id)
        replace_id = int(replace_id)
        blueprint.replace_blocks(old_block_id, replace_id)

    def _replace_hull_and_armor(self, blueprint):
        """
        @type blueprint: Blueprint
        """
        assert isinstance(self._replace_hull, str), "Bad replace hull: '{}'".format(self._replace_hull)
        assert ':' in self._replace_hull, "Bad hull replace: '{}'".format(self._replace_hull)
        old_hull_type, new_hull_type = self._replace_hull.split(':', 1)
        assert new_hull_type in self._char_to_hull_type, "Bad replace hull type: '{}'".format(new_hull_type)
        new_hull_type = self._char_to_hull_type[new_hull_type]
        if old_hull_type != "":
            assert old_hull_type in self._char_to_hull_type, "Bad hull type: '{}'".format(old_hull_type)
            old_hull_type = self._char_to_hull_type[old_hull_type]
        else:
            old_hull_type = None
        blueprint.replace_hull(new_hull_type, old_hull_type)

    def run(self):
        try:
            if self._directory_starmade is not None:
                block_config.read(self._directory_starmade)
            else:
                block_config.from_hard_coded()
            self.run_commands()

            if self._path_output is not None and self._is_archived:
                # .sment file
                self._logger.info("Exporting blueprint to:\n{}".format(self._path_output))
                self.zip_directory(self._directory_output, self._path_output)
                assert os.path.exists(self._path_output), "Compressing blueprint failed."

        except (KeyboardInterrupt, SystemExit, Exception, ValueError, RuntimeError) as e:
            self._logger.debug("\n{}\n".format(traceback.format_exc()))
            if len(e.args) > 0:
                self._logger.error(e.args[0])
            self._logger.error("Aborted")
        except AssertionError as e:
            if len(e.args) > 0:
                self._logger.error(e.args[0])
            self._logger.error("Aborted")
        else:
            self._logger.info("Finished")

    def run_commands(self, directory_input=None, directory_output=None, blueprint_path=None, entity_name=None):
        is_docked_entity = True
        if directory_input is None:
            is_docked_entity = False
            directory_input = self._directory_input
            directory_output = self._directory_output

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

        if entity_name is not None:
            docked_entity_name_prefix = entity_name
        else:
            entity_name = "ENTITY_SHIP_Main"
            docked_entity_name_prefix = "ENTITY_SHIP_RAIL_DOCK_"

        list_of_folders = os.listdir(directory_input)
        for folder_name in list_of_folders:
            if "ATTACHED_" not in folder_name:
                continue
            _, dock_index = folder_name.rsplit('_', 1)
            directory_src = os.path.join(directory_input, folder_name)
            directory_dst = None
            if directory_output is not None:
                directory_dst = os.path.join(directory_output, folder_name)
            self.run_commands(
                directory_input=directory_src,
                directory_output=directory_dst,
                blueprint_path=blueprint_path,
                entity_name="{}{}".format(docked_entity_name_prefix, dock_index))

        blueprint = Blueprint(
            logfile=self._logfile,
            verbose=self._verbose,
            debug=self._debug,
        )

        blueprint_name = os.path.basename(directory_input)
        self._logger.info("Reading blueprint '{}' ...".format(blueprint_name))
        blueprint.read(directory_input)

        blueprint.replace_outdated_docker_modules(entity_name, docked_entity_name_prefix, is_docked_entity)

        if self._docked_entities or not is_docked_entity:

            if self._remove_blocks is not None:
                self._logger.info("Removing blocks...")
                blueprint.remove_blocks(self._remove_blocks)

            if not is_docked_entity and self._move_center is not None:
                self._logger.info("Moving center/core of blueprint...")
                self._move_center_or_core(blueprint)

            if not is_docked_entity and self._mirror_axis is not None:
                self._logger.info("Mirror at axis...")
                blueprint.mirror_axis(axis_index=self._mirror_axis[0], reverse=self._mirror_axis[1])

            if self._replace is not None:
                self._logger.info("Replacing blocks...")
                self._replace_blocks(blueprint)

            if self._replace_hull is not None:
                self._logger.info("Replacing hull...")
                self._replace_hull_and_armor(blueprint)

            if True in self._auto_hull_shape:
                self._logger.info("Automatically set a shape to hull blocks...")
                blueprint.auto_hull_shape(
                    auto_wedge=self._auto_hull_shape[0],
                    auto_tetra=self._auto_hull_shape[1],
                    auto_corner=self._auto_hull_shape[2],
                    auto_hepta=self._auto_hull_shape[3]
                )

            if self._index_turn_tilt is not None:
                blueprint.turn_tilt(self._index_turn_tilt)

            if not is_docked_entity and (self._entity_type is not None or self._entity_class is not None):
                self._logger.info("Changing entity type/class blueprint...")
                blueprint.set_entity(self._entity_type, self._entity_class)

            if self._link_salvage:
                self._logger.info("Linking salvage computers/modules...")
                blueprint.link_salvage_modules()

            if self._update and self._entity_type is None:
                self._logger.info("Updating blueprint...")
                blueprint.update()

            if self._summary:
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
    options = ArgumentHandler.get_parser_options(label=SMBEdit.get_label(), version=__version__)
    verbose = not options.silent
    debug = options.debug_mode
    logfile = options.logfile
    try:
        with SMBEdit(
            options=options,
            logfile=logfile,
            verbose=verbose,
            debug=debug
                ) as manipulator:
            manipulator.run()
    except (KeyboardInterrupt, SystemExit, Exception, ValueError, RuntimeError) as e:
        if debug:
            sys.stderr.write("\n{}\n".format(traceback.format_exc()))
        if len(e.args) > 0:
            sys.stderr.write("ERROR: ")
            sys.stderr.write(e.args[0])
        sys.stderr.write("\nAborted\n")
    except AssertionError as e:
        if len(e.args) > 0:
            sys.stderr.write(e.args[0])
        sys.stderr.write("\nAborted\n")

if __name__ == "__main__":
    main()
