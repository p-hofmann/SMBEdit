from .actiondefault import ActionDefault
from ...utils.blockconfig import block_config


class ActionReplace(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionReplace, self).__init__(main_frame=main_frame, smbedit=smbedit)

    def button_press_remove(self):
        text = self.combobox_remove_blocks.currentText()
        index = self.combobox_remove_blocks.findText(text)
        if index == -1:
            self._main_frame.status_bar.showMessage("Unknown block: '{}'".format(text))
            return
        block_id = int(self.combobox_remove_blocks.itemData(index))

        if block_id not in block_config:
            self._main_frame.status_bar.showMessage("Unknown id: '{}'".format(block_id))
            return

        self._main_frame.status_bar.showMessage("Removing blocks ...".format())
        if self._main_frame.entities_check_box.isChecked():
            entity_index = self._main_frame.entities_combo_box.currentIndex()
            self._smbedit.blueprint[entity_index].remove_blocks({block_id})
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.remove_blocks({block_id})

        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Removing blocks ... Done!".format())

    def button_press_replace_block(self):
        text = self.combobox_replace_original.currentText()
        index = self.combobox_replace_original.findText(text)
        if index == -1:
            self._main_frame.status_bar.showMessage("Unknown block: '{}'".format(text))
            return
        block_id_old = int(self.combobox_replace_original.itemData(index))

        text = self.combobox_replace_replacement.currentText()
        index = self.combobox_replace_replacement.findText(text)
        if index == -1:
            self._main_frame.status_bar.showMessage("Unknown block: '{}'".format(text))
            return
        block_id_new = int(self.combobox_replace_replacement.itemData(index))

        if block_id_old not in block_config:
            self._main_frame.status_bar.showMessage("Unknown id: '{}'".format(block_id_old))
            return

        if block_id_new not in block_config:
            self._main_frame.status_bar.showMessage("Unknown id: '{}'".format(block_id_new))
            return

        self._main_frame.status_bar.showMessage("Replacing blocks ...".format())
        if self._main_frame.entities_check_box.isChecked():
            entity_index = self._main_frame.entities_combo_box.currentIndex()
            self._smbedit.blueprint[entity_index].replace_blocks(block_id_old, block_id_new)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.replace_blocks(block_id_old, block_id_new)

        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Replacing blocks ... Done!".format())

    def button_press_replace_hull(self):
        block_tier_old = self._main_frame.tool.tool_replace.combobox_replace_hull_original.currentIndex()
        block_tier_new = self._main_frame.tool.tool_replace.combobox_replace_hull_replacement.currentIndex()

        if not block_tier_old and block_tier_old != 0:
            self._main_frame.status_bar.showMessage("Enter a tier first.".format())
            return
        if not block_tier_new and block_tier_new != 0:
            self._main_frame.status_bar.showMessage("Enter a tier first.".format())
            return

        if block_tier_old == 5:
            # replace every tier of hull blocks
            block_tier_old = None

        self._main_frame.status_bar.showMessage("Replacing hull blocks ...".format())
        if self._main_frame.entities_check_box.isChecked():
            entity_index = self._main_frame.entities_combo_box.currentIndex()
            self._smbedit.blueprint[entity_index].replace_blocks_hull(block_tier_new, block_tier_old)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.replace_blocks_hull(block_tier_new, block_tier_old)

        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Replacing hull blocks ... Done!".format())
