__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from ...frames.widgets import Widgets
from ....utils.blockconfig import block_config


class FrameReplace(tk.Frame):
    """
    @type variable_remove: ttk.StringVar
    @type button_remove: ttk.Button

    @type variable_block_original: ttk.StringVar
    @type variable_block_replacement: ttk.StringVar
    @type button_replace_block: ttk.Button

    @type variable_hull_original: ttk.IntVar
    @type variable_hull_replacement: ttk.IntVar
    @type button_replace_hull: ttk.Button
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # , text="Remove/Replace"
        self._gui_remove_block()
        self._gui_replace_block()
        self._gui_replace_hull_and_armor()

    # #################
    # GUI
    # #################

    def _gui_remove_block(self):
        frame_main = tk.Frame(self)
        vcmd = (frame_main.register(Widgets.validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # TOP
        frame_top = tk.Frame(frame_main)
        self.variable_remove = tk.IntVar()

        self.button_remove = tk.Button(
            text="Remove block id",
            bd=2,
            master=frame_top)
        self.button_remove.pack(fill=tk.X, side=tk.LEFT)

        textbox = tk.Entry(
            frame_top, textvariable=self.variable_remove, exportselection=0, validate='key',
            validatecommand=vcmd, width=4)
        textbox.pack(side=tk.LEFT)
        frame_top.pack(side=tk.TOP, anchor=tk.W)
        # TOP END

        # BOTTOM
        frame_bottom = tk.Frame(frame_main)
        label = tk.Label(frame_bottom, relief=tk.RAISED, text='', width=9)
        label.pack(fill=tk.X, expand=tk.TRUE)
        self.variable_remove.trace(
            "w", lambda name, index, mode,
            text_variable=self.variable_remove,
            label_block=label: Widgets.callback_block_id(text_variable, label_block))
        frame_bottom.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X)
        # BOTTOM END

        frame_main.pack(anchor=tk.W, fill=tk.X, padx=2, pady=2)

    def _gui_replace_block(self):
        frame_main = tk.Frame(self)

        vcmd = (frame_main.register(Widgets.validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # TOP
        frame_top = tk.Frame(frame_main)
        self.variable_block_original = tk.IntVar()
        self.variable_block_replacement = tk.IntVar()

        self.button_replace_block = tk.Button(
            text="Replace block id",
            bd=2,
            master=frame_top)
        self.button_replace_block.pack(fill=tk.X, side=tk.LEFT)

        textbox = tk.Entry(
            frame_top, textvariable=self.variable_block_original, exportselection=0, validate='key',
            validatecommand=vcmd, width=4)
        textbox.pack(fill=tk.X, side=tk.LEFT)

        textbox = tk.Entry(
            frame_top, textvariable=self.variable_block_replacement, exportselection=0, validate='key',
            validatecommand=vcmd, width=4)
        textbox.pack(fill=tk.X, side=tk.LEFT)
        frame_top.pack(side=tk.TOP, anchor=tk.W)
        # TOP END

        # BOTTOM
        frame_bottom = tk.Frame(frame_main)

        label_replace_block_original = tk.Label(frame_bottom, relief=tk.RAISED, text='', width=9)
        label_replace_block_original.pack(side=tk.TOP, fill=tk.X, expand=tk.TRUE)
        self.variable_block_original.trace(
            "w", lambda name, index, mode,
            text_variable_0=self.variable_block_original,
            label0=label_replace_block_original: Widgets.callback_block_id(text_variable_0, label0))

        label_replace_block_replacement = tk.Label(frame_bottom, relief=tk.RAISED, text='', width=9)
        label_replace_block_replacement.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.TRUE)
        self.variable_block_replacement.trace(
            "w", lambda name, index, mode,
            text_variable_1=self.variable_block_replacement,
            label1=label_replace_block_replacement: Widgets.callback_block_id(text_variable_1, label1))

        frame_bottom.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X)
        # BOTTOM END

        frame_main.pack(fill=tk.X, padx=2, pady=2)

    def _gui_replace_hull_and_armor(self):
        frame_main = tk.Frame(self)

        # TOP
        frame_top = tk.Frame(frame_main)
        self.variable_hull_original = tk.IntVar()
        self.variable_hull_replacement = tk.IntVar()

        radio_box_0 = tk.LabelFrame(frame_top, relief=tk.RIDGE, text="From")
        radio_box_1 = tk.LabelFrame(frame_top, relief=tk.RIDGE, text="To")

        tiers = ["hull", "std. armor", "adv. armor", "crystal armor", "hazard armor"]
        for index, tier_name in enumerate(tiers[:4]):
            left = tk.Radiobutton(radio_box_0, text=tier_name, variable=self.variable_hull_original, value=index)
            right = tk.Radiobutton(radio_box_1, text=tier_name, variable=self.variable_hull_replacement, value=index)
            left.pack(anchor=tk.W)
            right.pack(anchor=tk.W)
            # left.grid()
            # right.grid()
        left = tk.Radiobutton(radio_box_0, text="All", variable=self.variable_hull_original, value=None)
        left.pack(anchor=tk.W)

        radio_box_0.pack(side=tk.LEFT, fill=tk.Y)
        radio_box_1.pack(side=tk.LEFT, fill=tk.Y)
        frame_top.pack(side=tk.TOP, anchor=tk.W)
        # TOP END

        # BOTTOM
        frame_bottom = tk.Frame(frame_main)

        self.button_replace_hull = tk.Button(
            text="Replace",
            bd=2,
            master=frame_bottom)
        self.button_replace_hull.pack(fill=tk.X, side=tk.LEFT)

        frame_bottom.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X)
        # BOTTOM END

        frame_main.pack(fill=tk.X, padx=2, pady=2)

    def disable(self):
        self.button_remove.config(state=tk.DISABLED)
        self.button_replace_block.config(state=tk.DISABLED)
        self.button_replace_hull.config(state=tk.DISABLED)

    def enable(self):
        self.button_remove.config(state=tk.NORMAL)
        self.button_replace_block.config(state=tk.NORMAL)
        self.button_replace_hull.config(state=tk.NORMAL)
