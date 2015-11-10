from WalText2 import main as wt2
from DefaultPrompt import execr
from Filesys import classes as fs
from tkinter import *
import codecs
import json


def flatten(l):
    r = []
    for sl in l:
        if type(sl) == list:
            r.extend(flatten(sl))
        else:
            r.append(sl)
    return r


class CommandPrompt(Tk):
    def __init__(self, filesys, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        for x in range(1):
            Grid.columnconfigure(self, x, weight=1)
            Grid.rowconfigure(self, x, weight=1)

        self.filesys = filesys

        self.cf = Frame(self, width=300, height=300)
        self.cf.grid(row=0, column=0, sticky=N+E+S+W)

        self.update()

        self.c = Canvas(self.cf, background='black', width=300,height=300, scrollregion=self.cf.bbox(ALL))
        self.text = ['']
        self.texti = 1

        self.scroller = Scrollbar(self.cf, orient=VERTICAL)

        self.scroller.pack(side=RIGHT, fill=Y)

        self.scroller.config(command=self.c.yview)
        self.c.config(width=300, height=300)
        self.c.config(yscrollcommand=self.scroller.set)

        self.c.pack(side=LEFT, expand=True, fill=BOTH)

        self.bind('<Key>', self.kp)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)

        self.font = json.loads(codecs.open('WalText2/standard_edit.fnt', 'r', 'utf-8').read())

        self.executer = execr.Executer()

        self.base = 60
        self.lines = [[[]]]  # The list to hold the created graphics

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
        if event.char in ['\r', '\n']:
            # This block is a mess. I'm so sorry.
            output = self.exec(self.text[-1])
            if output:
                self.text.append(output)
                self.lines.append([[]])
                self.base += 60
            self.update_view()
            self.text.append('')
            self.base += 60
            self.lines.append([[]])
            self.update_view()

        elif event.char == '\x08':
            self.text[-1] = self.text[-1][:-1]
            self.update_view()

        else:
            self.text[-1] += event.char
            self.update_view()

    def update_view(self, value=1):
        for ln in range(value+1)[1:]:
            for x in flatten(self.lines[-ln][-1]):
                self.c.delete(x)

            self.lines[-1][-1] = wt2.create_text(self.c, self.text[-1], self.font, self.base, color='#00FF00', scalar=0.75)

    def exec(self, com):
        return self.executer.runline(com, self.filesys)


if __name__ == '__main__':
    filesys = fs.Folder()
    filesys.load(open('DefaultPrompt/DefaultSys.fsys').read())
    main = CommandPrompt(filesys)
    main.wm_state('zoomed')
    main.mainloop()
