__author__ = 'Peter Hofmann'

import sys

from ..tagmanager import TagPayload, TagList


class AIConfig(object):
    """
    Handling AIConfig1 tag structure

    @type _target: str
    @type _ai_type: str
    @type _active: bool
    """

    _label = 'AIConfig1'

    TARGET = 0
    AI_TYPE = 1
    ACTIVE = 2

    _config_id_map = {
        TARGET: "Target",
        AI_TYPE: "AI_Type",
        ACTIVE: "Active"
    }

    _ai_types = {"Ship", "Turret", "Fleet"}

    _targets = {"Any", "Missiles", "Selected Target", "Astronauts"}

    def __init__(self):
        self._target = "Any"
        self._ai_type = "Ship"
        self._active = False

    def set(self, ai_type, active, target):
        """
        @type ai_type: str
        @type active: bool
        @type target: str
        """
        assert target in self._targets
        assert ai_type in self._ai_types
        self._target = target
        self._ai_type = ai_type
        self._active = active

    def from_tag(self, tag_payload):
        """
        13: 'AIConfig1'
        {
            -13:
            {
                -1: 1,
                -8: Ship,
            }
            -13:
            {
                -1: 2,
                -8: false,
            }
            -13:
            {
                -1: 0,
                -8: Any,
            }
        }

        @type tag_payload: TagPayload
        """
        assert isinstance(tag_payload, TagPayload)
        assert abs(tag_payload.id) == 13
        tag_list = tag_payload.payload
        assert isinstance(tag_list, TagList)
        list_of_tags = tag_list.get_list()

        for tag_entry in list_of_tags:
            assert isinstance(tag_entry, TagPayload)
            assert abs(tag_entry.id) == 13
            entry_tag_list = tag_entry.payload
            assert isinstance(entry_tag_list, TagList)
            entry_list_of_tags = entry_tag_list.get_list()
            assert abs(entry_list_of_tags[0].id) == 1
            assert abs(entry_list_of_tags[1].id) == 8
            config_id = entry_list_of_tags[0].payload
            config_value = entry_list_of_tags[1].payload
            assert config_id in self._config_id_map

            if config_id == AIConfig.TARGET:
                assert config_value in AIConfig._targets
                self._target = config_value
            elif config_id == AIConfig.AI_TYPE:
                assert config_value in AIConfig._ai_types
                self._ai_type = config_value
            elif config_id == AIConfig.ACTIVE:
                assert config_value in {"false", "true"}
                self._active = config_value == "true"

    def to_tag(self):
        """
        13: 'AIConfig1'
        {
            -13:
            {
                -1: 1,
                -8: Ship,
            }
            -13:
            {
                -1: 2,
                -8: false,
            }
            -13:
            {
                -1: 0,
                -8: Any,
            }
        }

        @rtype: TagPayload
        """
        ai_type_tag_list = TagList()
        ai_type_tag_list.add(TagPayload(-1, None, 1))
        ai_type_tag_list.add(TagPayload(-8, None, self._ai_type))
        ai_type_tag = TagPayload(-13, None, ai_type_tag_list)

        active_tag_list = TagList()
        active_tag_list.add(TagPayload(-1, None, 2))
        active_tag_list.add(TagPayload(-8, None, str(self._active).lower()))
        active_tag = TagPayload(-13, None, active_tag_list)

        target_tag_list = TagList()
        target_tag_list.add(TagPayload(-1, None, 0))
        target_tag_list.add(TagPayload(-8, None, self._target))
        target_tag = TagPayload(-13, None, target_tag_list)

        ai_config_tag_list = TagList()
        ai_config_tag_list.add(ai_type_tag)
        ai_config_tag_list.add(active_tag)
        ai_config_tag_list.add(target_tag)

        return TagPayload(13, self._label, ai_config_tag_list)

    def to_stream(self, output_stream=sys.stdout):
        """
        Stream values

        @param output_stream: Output stream
        @type output_stream: file
        """
        # self.to_tag().to_stream()
        output_stream.write("AI_Type: '{}'\t".format(self._ai_type))
        output_stream.write("Active: {}\t".format(self._active))
        output_stream.write("Target: '{}'\n".format(self._target))
