__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionAutoshape(ActionDefault):
    """
    Dealing with component interactions
    """

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
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].reset_ship_hull_shape()
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.reset_ship_hull_shape()

    def button_press_autoshape_wedge(self):
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_wedge=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_wedge=True)

    def button_press_autoshape_corner(self):
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_corner=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_corner=True)

    def button_press_autoshape_hepta(self):
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_hepta=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_hepta=True)

    def button_press_autoshape_tetra(self):
        if self._main_frame.entities_variable_checkbox.get():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.current()].auto_hull_shape(auto_tetra=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_tetra=True)
