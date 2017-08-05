from PyQt5.QtWidgets import QComboBox
from ...utils.blockconfig import block_config


class Widgets(object):
    @staticmethod
    def validate_float(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed in ['', '-', '.']:
            return True
        if text in '0123456789.-':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def validate_int(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed in ['', '-']:
            return True
        if text in '0123456789-':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def callback_block_id(text_variable, label):
        try:
            label['text'] = block_config[text_variable.get()].name
        except (KeyError, ValueError):
            label['text'] = ""

    @staticmethod
    def callback_tier(tier, label):
        try:
            label['text'] = block_config.tiers[tier]
        except (KeyError, ValueError):
            label['text'] = ""

    @staticmethod
    def insert_items(combo_box):
        """

        @type combo_box: QComboBox
        """
        for block_id in block_config:
            combo_box.addItem(block_config[block_id].name, block_id)
            combo_box.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
