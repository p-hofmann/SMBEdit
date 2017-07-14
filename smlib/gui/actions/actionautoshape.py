__author__ = 'Peter Hofmann'


# from smbeditGUI import SMBEditGUI
from ..frames.rootframe import RootFrame


class ActionAutoshape(RootFrame):
    """
    @type _smbedit: SMBEditGUI
    """
    def __init__(self, root, smbedit):
        """

        @type root: tk.Tk
        @type smbedit: SMBEditGUI
        """
        self._smbedit = smbedit
        RootFrame.__init__(self, root, smbedit)

        self.main_frame.tool.auto_shape.button_reset.configure(command=self.button_press_autoshape_reset)
        self.main_frame.tool.auto_shape.button_wedge.configure(command=self.button_press_autoshape_wedge)
        self.main_frame.tool.auto_shape.button_corner.configure(command=self.button_press_autoshape_corner)
        self.main_frame.tool.auto_shape.button_hepta.configure(command=self.button_press_autoshape_hepta)
        self.main_frame.tool.auto_shape.button_tetra.configure(command=self.button_press_autoshape_tetra)

    def button_press_autoshape_reset(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].reset_ship_hull_shape()

    def button_press_autoshape_wedge(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].auto_hull_shape(auto_wedge=True)

    def button_press_autoshape_corner(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].auto_hull_shape(auto_corner=True)

    def button_press_autoshape_hepta(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].auto_hull_shape(auto_hepta=True)

    def button_press_autoshape_tetra(self):
        self._smbedit.blueprint[self.main_frame.combo_box_entities.current()].auto_hull_shape(auto_tetra=True)
