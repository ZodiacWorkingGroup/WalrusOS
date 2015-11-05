import tkinter as tk

from WalText2 import main


class C(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        font = '''{
        "a": [["ellipse 12 15 12 15 0", "line 24 30 24 0"],
        {"width":24}]
        }'''
        main.render_text(self, 'aa', main.loadfont(font), 50)


top = tk.Tk()
c = C(top)

c.pack()

top.mainloop()