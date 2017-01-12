__author__ = 'Peter Hofmann'

import sys

from lib.blueprint.meta.tagmanager import TagPayload, TagList, TagPayloadList


class Inventory(object):
    """
    Handling Srotage tag structure

    @type :
    """

    _label = 'stash'

    def __init__(self):

    def set(self):
        """
        @type : str
        """

    def from_tag(self, tag_payload):
        """
        13: 'inv1'
        {
                    -12:
                        3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                    -12:
                        2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                    -13: {
                            -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                     }
         }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

    def to_tag(self):
        """
        13: 'inv1'
        {
                    -12:
                        3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                    -12:
                        2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                    -13: {
                            -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                     }
         }

        @rtype: TagPayload
        """
        return TagPayload(13, self._label, TagList())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """


class Storage(object):
    """
    Handling Srotage tag structure

    @type :
    """

    _label = 'stash'

    def __init__(self):

    def set(self):
        """
        @type : str
        """

    def from_tag(self, tag_payload):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash' {
                -13: {
                     -2: 0,
                    -13: {  // pull stuff
                        -13: {-2: 331, -3: 99999, }
                        -13: {-2: 476, -3: 99999, }
                        -13: {-2: 978, -3: 99999, }
                        -13: {-2: 121, -3: 99999, }
                        -13: {-2: 423, -3: 99999, }
                        .....
                    }
                     -8: ''
                }
                13: 'inv1' {
                            -12:
                                3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                            -12:
                                2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                            -13: {
                                    -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                             }
                 }
            }
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == -13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

    def to_tag(self):
        """
        -13:
        {
            -3: 3,
            -10: (7, 221, 33), // position
            13: 'stash' {
                -13: {
                     -2: 0,
                    -13: {  // pull stuff
                        -13: {-2: 331, -3: 99999, }
                        -13: {-2: 476, -3: 99999, }
                        -13: {-2: 978, -3: 99999, }
                        -13: {-2: 121, -3: 99999, }
                        -13: {-2: 423, -3: 99999, }
                        .....
                    }
                     -8: ''
                }
                13: 'inv1' {
                            -12:
                                3: [0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19]
                            -12:
                                2: [4	545	54	334	46	414	416	6	38	24	30	48	335	333	415	417	16	32	978	544	] ,
                            -13: {
                                    -3: 25, -3: 69455, -3: 1, -3: 50, -3: 9, -3: 54, -3: 50, -3: 105, -3: 105, -3: 21450
                             }
                 }
            }
        }
        @rtype: TagPayload
        """
        return TagPayload(13, self._label, TagList())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
