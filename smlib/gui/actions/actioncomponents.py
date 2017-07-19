__author__ = 'Peter Hofmann'


class ActionComponents(object):
    """
    @type _smbedit: smbeditGUI.SMBEditGUI
    """
    def __init__(self, main_frame, smbedit):
        """

        @type main_frame: smlib.gui.frames.mainframe.MainFrame
        @type smbedit: smbeditGUI.SMBEditGUI
        """
        self._smbedit = smbedit
        self.main_frame = main_frame

        self.main_frame.entities_check_box.configure(command=self.entities_check_box_onchange)
        self.main_frame.entities_combo_box.bind('<<ComboboxSelected>>', self.entities_combo_box_onchange)

    def entities_check_box_onchange(self):
        if not self.main_frame.entities_variable_checkbox.get():
            self.main_frame.entities_combo_box['values'] = ['All']
        elif len(self.main_frame.list_of_entity_names) > 0:
            self.main_frame.entities_combo_box['values'] = self.main_frame.list_of_entity_names
        self.main_frame.entities_combo_box.current(0)
        self.main_frame.update_summary(self._smbedit)

    def entities_combo_box_onchange(self, event):
        """

        @type event: tk.Event
        @return:
        """
        self.main_frame.update_summary(self._smbedit)
