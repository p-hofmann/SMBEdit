__author__ = 'Peter Hofmann'

import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk


class StatusBar(tk.Frame):
    def __init__(self, master):
        """

        @type master: tk.Tk
        """
        tk.Frame.__init__(self, master)
        self._text = tk.StringVar()
        self._label = tk.Label(
            self, relief=tk.SUNKEN, anchor=tk.W,
            textvariable=self._text,
            # font=('arial', 16, 'normal'), bd=1
        )
        self._label.pack(fill=tk.X)
        # self.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self, text):
        """
        @type text: str
        """
        self._text.set(text)
