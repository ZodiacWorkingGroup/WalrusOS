import tkinter as tk
from tkinter import N, E, S, W, BOTH, ALL

from WalText2 import main

from string import ascii_lowercase, ascii_uppercase, digits, punctuation


class C(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.config(background="#AAAAAA", width=800, height=500)
        self.fontfile = input('font file: ')
        print(ascii_lowercase)
        print(ascii_uppercase)
        print(digits)
        print(punctuation)
        self.bind('<Button-1>', self.draw)
        self.draw()

    def draw(self, event=None):
        self.delete(ALL)
        font = open(self.fontfile).read()
        main.render_text(self, ascii_lowercase, main.loadfont(font), 40)
        main.render_text(self, ascii_uppercase, main.loadfont(font), 100)
        main.render_text(self, digits, main.loadfont(font), 160)
        main.render_text(self, punctuation, main.loadfont(font), 220)


top = tk.Tk()
top.wm_state('zoomed')
c = C(top)

c.grid(sticky=N+E+S+W)

top.mainloop()
