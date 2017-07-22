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
            bd=2,
            master=self)
        self.button_reset.pack(fill=tk.X, padx=4, pady=1)

        some_frame = tk.Frame(self)
        self.button_wedge = tk.Button(
            text="Wedge",
            bd=2,
            master=some_frame)
        self.button_wedge.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X, padx=2, pady=1)

        self.button_tetra = tk.Button(
            text="Tetra",
            bd=2,
            master=some_frame)
        self.button_tetra.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X, padx=2, pady=1)
        some_frame.pack(fill=tk.X, pady=5, padx=3)

        some_frame = tk.Frame(self)
        self.button_corner = tk.Button(
            text="Corner",
            bd=2,
            master=some_frame)
        self.button_corner.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X, padx=2, pady=1)

        self.button_hepta = tk.Button(
            text="Hepta",
            bd=2,
            master=some_frame)
        self.button_hepta.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.X, padx=2, pady=1)
        some_frame.pack(fill=tk.X, pady=5, padx=3)

    def disable(self):
        self.button_reset.config(state=tk.DISABLED)
        self.button_wedge.config(state=tk.DISABLED)
        self.button_tetra.config(state=tk.DISABLED)
        self.button_corner.config(state=tk.DISABLED)
        self.button_hepta.config(state=tk.DISABLED)

    def enable(self):
        self.button_reset.config(state=tk.NORMAL)
        self.button_wedge.config(state=tk.NORMAL)
        self.button_tetra.config(state=tk.NORMAL)
        self.button_corner.config(state=tk.NORMAL)
        self.button_hepta.config(state=tk.NORMAL)
