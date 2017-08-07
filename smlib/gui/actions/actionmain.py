from PyQt5.QtWidgets import QWidget


class ActionMain(QWidget):
    """
    Dealing with component interactions

    @type _smbedit: smbeditGUI.SMBEditGUI
    """

    def __init__(self, smbedit):
        super().__init__()
        self._smbedit = smbedit
        self.entities_check_box = None
        self.entities_combo_box = None
        self.list_of_entity_names = []

    def entities_check_box_onchange(self, checked):
        if not checked:
            self.entities_combo_box.clear()
            self.entities_combo_box.addItem('All')
        elif len(self.list_of_entity_names) > 0:
            self.entities_combo_box.clear()
            for entity_name in self.list_of_entity_names:
                self.entities_combo_box.addItem(entity_name)
        self.update_summary()

    def entities_combo_box_onchange(self, *__args):
        """

        @type event: tk.Event
        @return:
        """
        self.update_summary()

    def update_summary(self):
        pass
