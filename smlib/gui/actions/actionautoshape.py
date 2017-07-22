__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionAutoshape(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionAutoshape, self).__init__(main_frame=main_frame, smbedit=smbedit)
        ActionAutoshape.set_commands(self)

    def set_commands(self):
        """
        Set commands of components
        """
        self._main_frame.tool.auto_shape.button_reset.configure(command=self.button_press_autoshape_reset)
        self._main_frame.tool.auto_shape.button_wedge.configure(command=self.button_press_autoshape_wedge)
        self._main_frame.tool.auto_shape.button_corner.configure(command=self.button_press_autoshape_corner)
        self._main_frame.tool.auto_shape.button_hepta.configure(command=self.button_press_autoshape_hepta)
        self._main_frame.tool.auto_shape.button_tetra.configure(command=self.button_press_autoshape_tetra)

    def button_press_autoshape_reset(self):
        self._main_frame.status_bar.set("Resetting hull block shapes to cubes ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].reset_ship_hull_shape()
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.reset_ship_hull_shape()
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Resetting hull block shapes to cubes ... Done!".format())

    def button_press_autoshape_wedge(self):
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to wedges...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_wedge=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_wedge=True)
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to wedges... Done!".format())

    def button_press_autoshape_corner(self):
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to corners ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_corner=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_corner=True)
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to corners ... Done!".format())

    def button_press_autoshape_hepta(self):
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to heptas ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_hepta=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_hepta=True)
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to heptas ... Done!".format())

    def button_press_autoshape_tetra(self):
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to tetras ...".format())
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_tetra=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_tetra=True)
        self._main_frame.update_summary(self._smbedit)
        self._main_frame.status_bar.set("Setting appropriate hull block shapes to tetras ... Done!".format())
