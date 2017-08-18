import sys
import argparse
import os

from voxlib.voxelize import Voxelizer
from smlib.blueprint import Blueprint
from smlib.utils.blockconfig import block_config


def CheckExt(choices):
    """
    File extension checking with argparse
    """
    class Act(argparse.Action):

        def __call__(self, parser, namespace, fname, option_string=None):
            ext = os.path.splitext(fname)[1][1:].lower()
            if ext not in choices:
                option_string = '({})'.format(
                    option_string) if option_string else ''
                parser.error("file doesn't end with one of {}{}".format(
                    choices, option_string))
            else:
                setattr(namespace, self.dest, fname)

    return Act


def main(sys_argv, description='Create a blueprint from a 3D model (obj/stl)'):
    # setup argparse
    parser = argparse.ArgumentParser(
        description=description)
    # 3d model input path (obj or stl)
    parser.add_argument(
        '-i', '--path_input',
        action=CheckExt({'obj', 'stl'}),
        help="'*.obj' or '*.stl' file path",
        required=True)

    parser.add_argument('-r', '--resolution',
                        type=int,
                        help='Voxelization resolution',
                        required=True)

    parser.add_argument(
        '-b', '--block_id',
        type=int,
        help='Block used to voxelize the model [default: 598 (Grey Hull)]',
        default=598)

    parser.add_argument(
        '-o', '--path_output',
        default=None,
        type=str,
        help="Output directory of the blueprint",
        required=True)

    parser.add_argument(
        '-a', '--rotation_axis',
        default=None,
        type=str,
        choices=['x', 'y', 'z'],
        help="The model is rotated in the plane perpendicular to the given axis",
        required=False)

    parser.add_argument(
        '-n', '--rotation_number',
        default=0,
        type=int,
        choices=[0, 1, 2, 3],
        help="Number of times the model is rotated by 90 degrees clockwise",
        required=False)

    parser.add_argument(
        "-et", "--entity_type",
        default=0,
        type=int,
        choices=[0, 1, 2, 3, 4],
        help='''Change entity type to:
        0: Ship
        1: Shop
        2: Space Station
        3: Asteroid
        4: Planet
    ''')

    args = parser.parse_args(sys_argv)

    # load block config
    block_config.from_hard_coded()

    # create the blueprint

    # for the moment, the name of the blueprint is not important since it is
    # the name of the output folder that is used to name the ship
    bp = Blueprint('bp_vox')
    # set the entity type
    bp.set_entity(args.entity_type, 0)

    # populate the bp
    bp.add_blocks(
        args.block_id,
        positions=list(Voxelizer.voxelize(args.path_input, resolution=args.resolution)),
        offset=(16, 16, 16),
        rotation_axis=args.rotation_axis,
        rotation_number=args.rotation_number
    )

    # if it's a ship, add a ship core
    if args.entity_type == 0:
        bp.add_blocks(
            1,
            positions=[(16, 16, 16)]
        )

    # create output dir if not already existing
    if not os.path.exists(args.path_output):
        os.makedirs(args.path_output)

    # write the file
    # note: trailing path separators produce empty bp names
    bp.write(args.path_output.rstrip('\\/'))

if __name__ == '__main__':
    main(sys.argv[1:])
