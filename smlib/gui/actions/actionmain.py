__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionMain(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionMain, self).__init__(main_frame=main_frame, smbedit=smbedit)
        ActionMain.set_commands(self)

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.entities_check_box.configure(command=self.entities_check_box_onchange)
        self._main_frame.entities_combo_box.bind('<<ComboboxSelected>>', self.entities_combo_box_onchange)

    def entities_check_box_onchange(self):
        if not self._main_frame.entities_variable_checkbox.get():
            self._main_frame.entities_combo_box['values'] = ['All']
        elif len(self._main_frame.list_of_entity_names) > 0:
            self._main_frame.entities_combo_box['values'] = self._main_frame.list_of_entity_names
        self._main_frame.entities_combo_box.current(0)
        self._main_frame.update_summary(self._smbedit)

    def entities_combo_box_onchange(self, event):
        """

        @type event: tk.Event
        @return:
        """
        self._main_frame.update_summary(self._smbedit)
