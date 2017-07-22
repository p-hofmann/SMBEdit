__author__ = 'Peter Hofmann'


import sys
if sys.version_info < (3,):
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk
from ...frames.widgets import Widgets


class FrameMoveCenter(tk.LabelFrame):
    """
    @type button_block_id: ttk.Button
    @type button_vector: ttk.Button
    @type variable_block_id: ttk.StringVar
    @type variable_x: ttk.StringVar
    @type variable_y: ttk.StringVar
    @type variable_z: ttk.StringVar
    """

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text="Move Center")
        self._gui_move_center_by_block_id()
        self._gui_move_center_by_vector()

    # #################
    # GUI
    # #################

    def _gui_move_center_by_block_id(self):
        frame_main = tk.Frame(self)
        vcmd = (frame_main.register(Widgets.validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # TOP
        frame_top = tk.Frame(frame_main)
        self.variable_block_id = tk.StringVar()

        self.button_block_id = tk.Button(
            text="To block id",
            bd=2,
            master=frame_top)
        self.button_block_id.pack(fill=tk.X, side=tk.LEFT)

        textbox = tk.Entry(
            frame_top, textvariable=self.variable_block_id, exportselection=0, validate='key', validatecommand=vcmd, width=4)
        textbox.pack(side=tk.LEFT)
        frame_top.pack(side=tk.TOP, anchor=tk.W)
        # TOP END

        # BOTTOM
        frame_bottom = tk.Frame(frame_main)
        label = tk.Label(frame_main, relief=tk.RAISED, text='', width=9)
        # label.propagate(tk.FALSE)
        label.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.TRUE)
        self.variable_block_id.trace(
            "w", lambda name, index, mode, text_variable=self.variable_block_id: Widgets.callback_block_id(
                text_variable, label))
        frame_bottom.pack(side=tk.BOTTOM)
        # BOTTOM END

        frame_main.pack(anchor=tk.W, fill=tk.X, padx=2, pady=2)

    def _gui_move_center_by_vector(self):
        new_frame = tk.Frame(self)

        vcmd = (new_frame.register(Widgets.validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.variable_x = tk.StringVar()
        self.variable_x.set('0')
        self.variable_y = tk.StringVar()
        self.variable_y.set('0')
        self.variable_z = tk.StringVar()
        self.variable_z.set('0')

        self.button_vector = tk.Button(
            text=" By vector ",
            bd=2,
            master=new_frame)
        self.button_vector.pack(fill=tk.X, side=tk.LEFT)

        textbox = tk.Entry(
            new_frame, textvariable=self.variable_x, exportselection=0, validate='key',
            validatecommand=vcmd, width=4)
        textbox.pack(fill=tk.X, side=tk.LEFT)
        textbox = tk.Entry(
            new_frame, textvariable=self.variable_y, exportselection=0, validate='key',
            validatecommand=vcmd, width=4)
        textbox.pack(fill=tk.X, side=tk.LEFT)
        textbox = tk.Entry(
            new_frame, textvariable=self.variable_z, exportselection=0, validate='key',
            validatecommand=vcmd, width=4)
        textbox.pack(fill=tk.X, side=tk.LEFT)

        new_frame.pack(fill=tk.X, padx=2, pady=2)

    def disable(self):
        self.button_block_id.config(state=tk.DISABLED)
        self.button_vector.config(state=tk.DISABLED)

    def enable(self):
        self.button_block_id.config(state=tk.NORMAL)
        self.button_vector.config(state=tk.NORMAL)
