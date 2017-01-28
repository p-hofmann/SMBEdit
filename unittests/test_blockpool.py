__author__ = 'Peter Hofmann'

import sys
import struct
from lib.utils.blockconfig import block_config
from lib.utils.blocklist import BlockList, Block
# from simplemetablock import Block

# block_config.from_hard_coded()
# pool = BlockList()
# pool((1, -2, 3), BlockSmd3(1))
# pool((11, -12, 13), BlockSmd3(88))
# pool((111, -112, 113), BlockSmd3(600))
#
# for position, block in pool.items():
#     print(position, block)
#
# position = (99, -32000, 99)
# pindex = pool.get_index(position)
# print(pindex)
# print(sys.getsizeof(pindex), sys.getsizeof(position))
