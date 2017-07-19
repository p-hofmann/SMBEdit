__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk


class FrameMirror(tk.LabelFrame):
    """
    @type variable_radiobox_axis: tk.IntVar
    @type variable_checkbox_reversed: tk.BooleanVar
    @type button_mirror: tk.Button
    """

    def __init__(self, master):
        """
        """
        tk.LabelFrame.__init__(self, master, text="Mirror")
        self._gui_mirror()

    def _gui_mirror(self):
        """
        0: x left to right
        1: y top to bottom
        2: z front to back
        """
        frame_main = tk.Frame(self)

        # TOP
        frame_top = tk.Frame(frame_main)
        self.variable_radiobox_axis = tk.IntVar()
        self.variable_checkbox_reversed = tk.BooleanVar()

        radio_box_0 = tk.LabelFrame(frame_top, relief=tk.RIDGE, text="")

        radio_box_option = tk.Radiobutton(
            radio_box_0, text="Left -> Right", variable=self.variable_radiobox_axis, value=0)
        radio_box_option.pack(anchor=tk.W)
        radio_box_option = tk.Radiobutton(
            radio_box_0, text="Top -> Bottom", variable=self.variable_radiobox_axis, value=1)
        radio_box_option.pack(anchor=tk.W)
        radio_box_option = tk.Radiobutton(
            radio_box_0, text="Front -> Back", variable=self.variable_radiobox_axis, value=2)
        radio_box_option.pack(anchor=tk.W)

        radio_box_0.pack(side=tk.LEFT, fill=tk.Y)
        frame_top.pack(side=tk.TOP, anchor=tk.W)
        # TOP END

        # BOTTOM
        frame_bottom = tk.Frame(frame_main)

        check_button = tk.Checkbutton(
            frame_bottom, text="Reverse", variable=self.variable_checkbox_reversed,
            onvalue=True, offvalue=False)
        check_button.pack(fill=tk.X, side=tk.RIGHT)

        self.button_mirror = tk.Button(
            text="Mirror",
            bd=2,
            master=frame_bottom)
        self.button_mirror.pack(fill=tk.X, side=tk.RIGHT)

        frame_bottom.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X)
        # BOTTOM END

        frame_main.pack(fill=tk.X, padx=5, pady=5)
