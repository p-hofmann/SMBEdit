import argparse
import sys

from functools import partial
from smbedit import main as cli_smbedit

def subcommand(func, description=None):
    """
    Decorator to indicate and register subcommands
    """
    func._is_subcommand = True
    if description is None:
        func._cli_description = func.__doc__ if func.__doc__ else '\n\tNo description'
    else:
        func._cli_description = '\n\t'+description
    return func


class Smb(object):

    def __init__(self, subcommands={}):
        # setup subcommand dict
        self._subcommands = {func: getattr(self, func)
            for func in dir(self)
            if getattr(getattr(self, func), '_is_subcommand', False)}
        self.add_subcommand(subcommands)

        usage_help = ('smb <command> [<args>]\n\n' +
            ' -- Available subcommands -- \n\n' +
            '\n'.join([name + ':' + func._cli_description
            for name, func in self._subcommands.items()]))

        # create the parser
        self.parser = argparse.ArgumentParser(
            description='Create/Edit StarMade Blueprints',
            usage=usage_help)
        self.parser.add_argument('command', help='Subcommand to run')

    @subcommand
    def edit(self):
        """
        Edit an existing blueprint
        """
        # drop the global command name
        sys.argv = sys.argv[1:]
        # launch smbedit
        cli_smbedit()

    @subcommand
    def voxelize(self):
        """
        Create a blueprint from a 3D model (obj/stl)
        """
        parser = argparse.ArgumentParser(
            description=self.voxelize._cli_description)
        # 3d model input path (obj or stl)
        parser.add_argument(
            "path_input",
            type=str,
            help="'*.obj' or '*.stl' file path.")

        parser.add_argument(
            "-o", "--path_output",
            default=None,
            type=str,
            help="Output directory of modified blueprint or '*.sment' file path")
        args = parser.parse_args(sys.argv[2:])

    def unrecognized_command(self, command_name):
        """
        Method used to print a warning and exit if the requested
        command does not exist
        """
        sys.stdout.write('Unrecognized command "%s"\n' % command_name)
        self.parser.print_help()
        exit(1)

    def add_subcommand(self, commands):
        """
        Add subcommand to the 
        """
        self._subcommands.update(commands)

    def run(self):
        # parse the command name
        args = self.parser.parse_args(sys.argv[1:2])

        # use partial to bind command name to unrecognized_command 
        default_subcommand = partial(self.unrecognized_command, args.command)
        # use dispatch pattern to invoke the corresponding subcommand
        self._subcommands.get(args.command, default_subcommand)()

if __name__ == '__main__':
    cli = Smb()
    cli.run()