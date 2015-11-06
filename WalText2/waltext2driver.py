import tkinter as tk
from tkinter import N, E, S, W, BOTH, ALL

from WalText2 import main


class C(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.config(background="#AAAAAA", width=800, height=500)
        self.fontfile = input('font file: ')
        self.bind('<Button-1>', self.draw)
        self.draw()

    def draw(self, event=None):
        self.delete(ALL)
        font = open(self.fontfile).read()
        text = open('testtext.txt').readlines()

        baseline = 40
        for ln in text:
            main.create_text(self, ln, main.loadfont(font), baseline)
            baseline += 60


top = tk.Tk()
top.wm_state('zoomed')
c = C(top)

c.grid(sticky=N+E+S+W)

top.mainloop()
