from lib.smblueprint.smdblock.style.style0 import Style0


__author__ = 'Peter Hofmann'


class Style3(Style0):
    """
    Type        Bits                Description
    Type3       23     22     21    The block facing
                              19    0 always

    @type _orientation_to_str: dict[int, str]
    """
    # https://starmadepedia.net/wiki/Blueprint_File_Formats#Block_Data

    _orientation_to_str = {
        # 19: 0
        0: "BACK  ",
        1: "FRONT ",
        2: "BOTTOM",
        3: "TOP   ",
        4: "LEFT  ",
        5: "RIGHT ",
    }
