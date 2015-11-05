import tkinter as tk
from WalText2 import main


class C(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        main.draw_arc(self, 100, 100, 40, 80, 0, 270, 10)
        main.draw_ellipse(self, 100, 100, 40, 80, 20)
        main.draw_circle(self, 100, 100, 40)


top = tk.Tk()
c = C(top)

c.pack()

top.mainloop()