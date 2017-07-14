__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from smlib.gui import Widgets
from lib.utils.blockconfig import block_config


class FrameReplace(tk.LabelFrame):
    """
    @type variable_remove: ttk.StringVar
    @type button_remove: ttk.Button

    @type variable_block_original: ttk.StringVar
    @type variable_block_replacement: ttk.StringVar
    @type button_replace_block: ttk.Button

    @type ariable_hull_original: ttk.IntVar
    @type variable_hull_replacement: ttk.IntVar
    @type button_replace_hull: ttk.Button
    """

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text="Replace")
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
        self.variable_remove = tk.StringVar()

        self.button_remove = tk.Button(
            text="Remove block id",
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

        frame_main.pack(anchor=tk.W, fill=tk.X, padx=5, pady=5)

    def _gui_replace_block(self):
        frame_main = tk.Frame(self)

        vcmd = (frame_main.register(Widgets.validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # TOP
        frame_top = tk.Frame(frame_main)
        self.variable_block_original = tk.StringVar()
        self.variable_block_replacement = tk.StringVar()

        self.button_replace_block = tk.Button(
            text="Replace block id",
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

        frame_main.pack(fill=tk.X, padx=5, pady=5)

    def _gui_replace_hull_and_armor(self):
        frame_main = tk.Frame(self)

        # TOP
        frame_top = tk.Frame(frame_main)
        self.ariable_hull_original = tk.IntVar()
        self.variable_hull_replacement = tk.IntVar()

        radio_box_0 = tk.LabelFrame(frame_top, relief=tk.RIDGE, text="From")
        radio_box_1 = tk.LabelFrame(frame_top, relief=tk.RIDGE, text="To")

        for index, tier_name in enumerate(block_config.tiers[:4]):
            left = tk.Radiobutton(radio_box_0, text=tier_name, variable=self.ariable_hull_original, value=index)
            right = tk.Radiobutton(radio_box_1, text=tier_name, variable=self.variable_hull_replacement, value=index)
            left.pack(anchor=tk.W)
            right.pack(anchor=tk.W)
            # left.grid()
            # right.grid()
        left = tk.Radiobutton(radio_box_0, text="All", variable=self.ariable_hull_original, value=None)
        left.pack(anchor=tk.W)

        radio_box_0.pack(side=tk.LEFT, fill=tk.Y)
        radio_box_1.pack(side=tk.LEFT, fill=tk.Y)
        frame_top.pack(side=tk.TOP, anchor=tk.W)
        # TOP END

        # BOTTOM
        frame_bottom = tk.Frame(frame_main)

        self.button_replace_hull = tk.Button(
            text="Replace",
            master=frame_bottom)
        self.button_replace_hull.pack(fill=tk.X, side=tk.LEFT)

        frame_bottom.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X)
        # BOTTOM END

        frame_main.pack(fill=tk.X, padx=5, pady=5)
