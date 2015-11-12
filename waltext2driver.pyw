import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import N, E, S, W, BOTH, ALL

import WalText2.main as main

import codecs
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support (for ? character)


class C(tk.Canvas):
    def __init__(self, w, h, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.config(background="#AAAAAA", width=w, height=h)
        self.fontfile = askopenfilename(title='Select a font file')
        self.testfile = askopenfilename(title='Select a test file')
        self.bind('<Button-1>', self.draw)
        self.draw()

    def draw(self, event=None):
        self.delete(ALL)
        font = open(self.fontfile).read()
        text = [line.strip() for line in codecs.open(self.testfile, 'r', 'utf-8').readlines()]

        baseline = 40
        for ln in text:
            main.create_text(self, ln, main.loadfont(font), baseline)
            baseline += 60


top = tk.Tk()
top.wm_state('zoomed')
top.update()
c = C(top.winfo_width(), top.winfo_height(), top)

c.grid(sticky=N+E+S+W)

top.mainloop()
