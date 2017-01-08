import os
from .definitions import BLOCKTYPES_PATH, BLOCKCONFIG_PATH
from .lib.metablockconfig import BlockConfig

# Create the block config during the first call of the package
BlockConfig(BLOCKTYPES_PATH, BLOCKCONFIG_PATH)