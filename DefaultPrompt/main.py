from WalText2.main import create_text
from tkinter import *
import codecs
import json
from string import digits, ascii_letters


class CommandPrompt(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        for x in range(1):
            Grid.columnconfigure(self, x, weight=1)
            Grid.rowconfigure(self, x, weight=1)

        self.c = Canvas(background='black')
        self.c.grid(row=0, column=0, sticky=N+E+S+W)
        self.text = ['']
        self.texti = 1

        self.bind('<Key>', self.kp)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)

        self.font = json.loads(codecs.open('../WalText2/standard_edit.fnt', 'r', 'utf-8').read())

    def up(self, event):
        self.texti -= 1
        self.text[-1] = self.text[-self.texti]
        self.update_view()

    def down(self, event):
        self.texti += 1
        self.text[-1] = self.text[-self.texti]
        self.update_view()

    def kp(self, event):
        print(repr(event.char))
        if event.char == '\r':
            self.exec(self.text[-1])
            self.text.append('')

        elif event.char == '\x08':
            self.text[-1] = self.text[-1][:-1]

        else:
            self.text[-1] += event.char

        self.update_view()

    def update_view(self):
        self.c.delete(ALL)
        base = 60

        for line in self.text[:-1]:
            create_text(self.c, line, self.font, base, color='#00AA00', scalar=0.75)
            base += 40
        create_text(self.c, self.text[-1], self.font, base, color='#00FF00', scalar=0.75)

    def exec(self, com):
        pass


main = CommandPrompt()
main.wm_state('zoomed')
main.mainloop()