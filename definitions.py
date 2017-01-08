import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

# Specify the path of starmade config files. 'starmade_config' can be a sym 
# link to the starmade folder where config files are stored.

# Be sure to regularly update these files

STARMADE_CONFIG_PATH = os.path.join(ROOT_DIR, 'starmade_config')

BLOCKTYPES_PATH = os.path.join(STARMADE_CONFIG_PATH, 'BlockTypes.properties')
BLOCKCONFIG_PATH = os.path.join(STARMADE_CONFIG_PATH, 'BlockConfig.xml')