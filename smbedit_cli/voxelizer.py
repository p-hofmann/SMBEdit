import sys
import argparse
import os

from voxlib.voxelize import voxelize
from smlib.blueprint import Blueprint
from smlib.utils.blockconfig import block_config

def CheckExt(choices):
    """
    File extension checking with argparse
    """
    class Act(argparse.Action):
        def __call__(self,parser,namespace,fname,option_string=None):
            ext = os.path.splitext(fname)[1][1:].lower()
            if ext not in choices:
                option_string = '({})'.format(option_string) if option_string else ''
                parser.error("file doesn't end with one of {}{}".format(choices,option_string))
            else:
                setattr(namespace,self.dest,fname)

    return Act


def main(sys_argv, description='Create a blueprint from a 3D model (obj/stl)'):
    # setup argparse
    parser = argparse.ArgumentParser(
        description=description)
    # 3d model input path (obj or stl)
    parser.add_argument(
        '-i', '--path_input',
        action=CheckExt({'obj','stl'}),
        help="'*.obj' or '*.stl' file path.",
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
        help="Output directory of modified blueprint or '*.sment' file path",
        required=True)
    args = parser.parse_args(sys_argv)

    # load block config 
    block_config.from_hard_coded()

    # create the blueprint

    bp = Blueprint('bp_vox')
    # set the entity to space station
    bp.set_entity(2, 0)

    # populate the bp
    bp.add_blocks(
        args.block_id,
        positions=list(voxelize(args.path_input, resolution=args.resolution)),
        offset=(16, 16, 16)
    )

    # create output dir if not already existing
    if not os.path.exists(args.path_output):
        os.makedirs(args.path_output)

    # write the file
    bp.write(args.path_output)

if __name__ == '__main__':
    main(sys.argv[1:])