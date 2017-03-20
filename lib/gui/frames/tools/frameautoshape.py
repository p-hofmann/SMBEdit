__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk


class FrameAutoShape(tk.LabelFrame):
    """
    @type button_reset: tk.Button
    @type button_wedge: tk.Button
    @type button_tetra: tk.Button
    @type button_corner: tk.Button
    @type button_hepta: tk.Button
    """

    def __init__(self, master):
        """
        """
        tk.LabelFrame.__init__(self, master, text="Auto Shape")

        self.button_reset = tk.Button(
            text="Cube",
            master=self)
        self.button_reset.pack(fill=tk.X)

        self.button_wedge = tk.Button(
            text="Wedge",
            master=self)
        self.button_wedge.pack(fill=tk.X)

        self.button_tetra = tk.Button(
            text="Tetra",
            master=self)
        self.button_tetra.pack(fill=tk.X)

        self.button_corner = tk.Button(
            text="Corner",
            master=self)
        self.button_corner.pack(fill=tk.X)

        self.button_hepta = tk.Button(
            text="Hepta",
            master=self)
        self.button_hepta.pack(fill=tk.X)
