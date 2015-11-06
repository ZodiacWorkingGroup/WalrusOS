from tkinter import *
from tkinter.scrolledtext import ScrolledText
import json
from os.path import isfile


class Main(Tk):
    def __init__(self, f, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.f = f
        content = open(f).read()
        self.font = json.loads(content)
        self.curchar = 'a'

        self.mb = Menu()
        self.fm = Menu(tearoff=False)
        self.fm.add_command(label='Save', command=self.save, accelerator='Ctrl+S')

        self.cm = Menu(tearoff=False)
        self.cm.add_command(label='Update', command=self.updatechar)
        self.cm.add_command(label='Open new char', command=self.switchchar)

        self.mb.add_cascade(label='File', menu=self.fm)
        self.mb.add_cascade(label='Character', menu=self.cm)

        self.charlabel = Label(text='a')

        self.st = ScrolledText()

        self.meta = Frame(self)
        self.widthl = Label(self.meta, text='Character Width: ')
        self.widthe = Entry(self.meta)

        self.widthl.grid(row=0, column=0)
        self.widthe.grid(row=0, column=1)

        self.config(menu=self.mb)
        self.charlabel.grid(row=1, column=0)
        self.st.grid(row=2, column=0)
        self.meta.grid(row=3, column=0)

        self.bind('<Control-s>', self.save)

        self.updatest()

    def save(self, event=None):
        print('Saved!')
        self.updatechar()
        open(self.f, 'w').write(json.dumps(self.font))

    def updatechar(self):
        self.font[self.curchar] = [[ln for ln in self.st.get(1.0, END).split('\n') if ln],
                                   {'width: ': float(self.widthe.get())}]

    def switchchar(self):
        self.curchar = input('New char: ')
        self.charlabel.config(text=self.curchar)
        self.updatest()

    def updatest(self):
        self.st.delete(1.0, END)
        for line in self.font[self.curchar][0]:
            self.st.insert(END, line)
            self.st.insert(END, '\n')
        self.widthe.delete(0, END)
        self.widthe.insert(0, self.font[self.curchar][1]['width'])


inp = ''
while not isfile(inp):
    inp = input('Font file: ')

m = Main(inp)

m.mainloop()
