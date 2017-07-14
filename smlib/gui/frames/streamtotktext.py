__author__ = 'Peter Hofmann'

import sys
if sys.version_info < (3,):
    import Tkinter as tk
else:
    import tkinter as tk


class StreamToTkText(object):
    """
    @type _text_area: tk.Text
    """

    def __init__(self, tk_text):
        self._text_area = tk_text
        self._pointer = 0

    def write(self, text, index0=None):
        if index0 is None:
            index0 = tk.END
        self._text_area.config(state=tk.NORMAL)
        self._text_area.insert(index0, text)
        self._text_area.config(state=tk.DISABLED)
        self._text_area.update_idletasks()

    def read(self):
        return self._text_area.get(1.0, tk.END)

    def delete(self, index1=None, index2=None):
        if index1 is None:
            index1 = "1.0"
        if index2 is None:
            index2 = tk.END
        self._text_area.config(state=tk.NORMAL)
        self._text_area.delete(index1, index2)
        self._text_area.config(state=tk.DISABLED)
