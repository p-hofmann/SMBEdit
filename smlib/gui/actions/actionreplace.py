__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault
from ...utils.blockconfig import block_config


class ActionReplace(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionReplace, self).__init__(main_frame=main_frame, smbedit=smbedit)
        ActionReplace.set_commands(self)

    def set_commands(self):
        """
        Set commands of components
        """
        # print("ActionReplace")
        self._main_frame.tool.tool_replace.button_remove.configure(command=self.button_press_remove)
        self._main_frame.tool.tool_replace.button_replace_block.configure(command=self.button_press_replace_block)
        self._main_frame.tool.tool_replace.button_replace_hull.configure(command=self.button_press_replace_hull)

    def button_press_remove(self):
        block_id_entry = self._main_frame.tool.tool_replace.variable_remove.get()
        if block_id_entry not in block_config:
            self._main_frame.status_bar.set("Unknown id: '{}'".format(block_id_entry))
            return

        self._main_frame.status_bar.set("Removing blocks ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            entity_index = self._main_frame.entities_combo_box.current()
            self._smbedit.blueprint[entity_index].remove_blocks({block_id_entry})
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.remove_blocks({block_id_entry})

        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Removing blocks ... Done!".format())

    def button_press_replace_block(self):
        block_id_old = self._main_frame.tool.tool_replace.variable_block_original.get()
        block_id_new = self._main_frame.tool.tool_replace.variable_block_replacement.get()

        if block_id_old not in block_config:
            self._main_frame.status_bar.set("Unknown id: '{}'".format(block_id_old))
            return

        if block_id_new not in block_config:
            self._main_frame.status_bar.set("Unknown id: '{}'".format(block_id_new))
            return

        self._main_frame.status_bar.set("Replacing blocks ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            entity_index = self._main_frame.entities_combo_box.current()
            self._smbedit.blueprint[entity_index].replace_blocks(block_id_old, block_id_new)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.replace_blocks(block_id_old, block_id_new)

        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Replacing blocks ... Done!".format())

    def button_press_replace_hull(self):
        block_tier_old = self._main_frame.tool.tool_replace.variable_hull_original.get()
        block_tier_new = self._main_frame.tool.tool_replace.variable_hull_replacement.get()

        if not block_tier_old and block_tier_old != 0:
            self._main_frame.status_bar.set("Enter a tier first.".format())
            return
        if not block_tier_new and block_tier_new != 0:
            self._main_frame.status_bar.set("Enter a tier first.".format())
            return

        self._main_frame.status_bar.set("Replacing hull blocks ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            entity_index = self._main_frame.entities_combo_box.current()
            self._smbedit.blueprint[entity_index].replace_blocks_hull(block_tier_new, block_tier_old)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.replace_blocks_hull(block_tier_new, block_tier_old)

        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Replacing hull blocks ... Done!".format())
