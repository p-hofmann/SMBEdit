__author__ = 'Peter Hofmann'


from .actiondefault import ActionDefault


class ActionAutoshape(ActionDefault):
    """
    Dealing with component interactions
    """

    def __init__(self, main_frame, smbedit):
        super(ActionAutoshape, self).__init__(main_frame=main_frame, smbedit=smbedit)

    def button_press_autoshape_reset(self, clicked):
        self._main_frame.status_bar.showMessage("Resetting hull block shapes to cubes ...".format())
        if self._main_frame.entities_check_box.isChecked():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.currentIndex()].reset_ship_hull_shape()
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.reset_ship_hull_shape()
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Resetting hull block shapes to cubes ... Done!".format())

    def button_press_autoshape_wedge(self, clicked):
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to wedges...".format())
        if self._main_frame.entities_check_box.isChecked():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.currentIndex()].auto_hull_shape(auto_wedge=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_wedge=True)
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to wedges... Done!".format())

    def button_press_autoshape_corner(self, clicked):
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to corners ...".format())
        if self._main_frame.entities_check_box.isChecked():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.currentIndex()].auto_hull_shape(auto_corner=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_corner=True)
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to corners ... Done!".format())

    def button_press_autoshape_hepta(self, clicked):
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to heptas ...".format())
        if self._main_frame.entities_check_box.isChecked():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.currentIndex()].auto_hull_shape(auto_hepta=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_hepta=True)
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to heptas ... Done!".format())

    def button_press_autoshape_tetra(self, clicked):
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to tetras ...".format())
        if self._main_frame.entities_check_box.isChecked():
            self._smbedit.blueprint[self._main_frame.entities_combo_box.currentIndex()].auto_hull_shape(auto_tetra=True)
        else:
            for blueprint in self._smbedit.blueprint:
                blueprint.auto_hull_shape(auto_tetra=True)
        self._main_frame.update_summary()
        self._main_frame.status_bar.showMessage("Setting appropriate hull block shapes to tetras ... Done!".format())
