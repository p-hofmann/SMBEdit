__author__ = 'Peter Hofmann'

import sys

from lib.blueprint.meta.tagmanager import TagPayload, TagList


class Datatype2TagReader(object):
    """
    Handling datatype2 tag structure
    """

    _label = 'container'

    def __init__(self):
        return

    def set(self, ai_type, active, target):
        """
        @type ai_type: str
        @type active: bool
        @type target: str
        """

    def from_tag(self, tag_payload):
        """
        13: 'container'
        {
            -13:  {}
            3: 'shipMan0' 0,
            -13: { -6: 3063.5747052, -6: 0.0 }
            6: 'sh' 0.0,
            -13: { -4: -9223372036854775808 }
            13: 'a' { -13:  {} -13:  {} -13:  {} }
            -13:  {}
            -13:
            {
                -13: { -2: 478, -3: 0 } "Shield-Recharger"
                -13: { -2:   3, -3: 0 } "Shield Capacitor"
                -13: { -2: 937, -3: 0 } "Pickup Point"
                -13: { -2:   8, -3: 0 } "Thruster Module"
                -13: { -2: 122, -3: 0 } "Plex Door"
                -13: { -2:  22, -3: 0 } "Cloaker"
                -13: { -2:  14, -3: 0 } "Warhead"
                -13: { -2:  15, -3: 0 } "RadarJammer"
                -13: { -2:   2, -3: 0 } "Power Reactor Module"
                -13: { -2: 671, -3: 0 } "Rail Mass Enhancer"
                -13: { -2: 331, -3: 0 } "Power Capacitor"
                -13: { -2: 978, -3: 0 } "Power Auxiliary"
            }
            -1: 0,
            -13:
            {
                13: 'ACD'  {}
                13: 'TR'  {}
                13: 'A'  {}
                13: 'A'  {}
                13: 'J'  {}
                13: 'JP'  {}
                13: 'SC'  {}
            }
             13: 'AIConfig1'  {-13:  {-1: 1, -8: Ship, } -13:  {-1: 2, -8: false, } -13:  {-1: 0, -8: Any, } }
            -13:
            {
                -1: 0,
                -13:
                {
                    -13: { -1: 9, -4: 68720525328 }
                }
            }
            -1: 0,
            -13:  {}
            -13:  {}
        }

        @type tag_payload: TagPayload
        """

    def to_tag(self):
        """
        @rtype: TagPayload
        """
        return TagPayload(13, self._label, TagList())

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
