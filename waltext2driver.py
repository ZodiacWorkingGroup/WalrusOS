import tkinter as tk

from WalText2 import main


class C(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        font = '''{
        "a": [["circle 15 15 15", "line 30 30 30 0"],
        {"width":30}]
        }'''
        main.render_text(self, 'aa', main.loadfont(font), 50)


top = tk.Tk()
c = C(top)

c.pack()

top.mainloop()