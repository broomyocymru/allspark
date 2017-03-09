from Tkinter import Tk


class Clipboard(object):
    @staticmethod
    def copy(content):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(content)
        r.destroy()
