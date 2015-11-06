from tkinter import *
from tkinter.scrolledtext import ScrolledText
import json
from os.path import isfile

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support (for ? character)


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
        self.cm.add_command(label='Next char', command=self.next)
        self.cm.add_command(label='Previous char', command=self.prev)

        self.mb.add_cascade(label='File', menu=self.fm)
        self.mb.add_cascade(label='Character', menu=self.cm)

        self.charlabel = Label(text='a', font=('Times', 20, 'roman'))
        self.charinput = Entry(font=('Times', 20, 'roman'))

        self.st = ScrolledText()

        self.meta = Frame(self)
        self.widthl = Label(self.meta, text='Width: ')
        self.widthe = Entry(self.meta)

        self.topl = Label(self.meta, text='Top: ')
        self.tope = Entry(self.meta)

        self.widthl.grid(row=0, column=0)
        self.widthe.grid(row=0, column=1)
        self.topl.grid(row=0, column=2)
        self.tope.grid(row=0, column=3)

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
                                   {'width': int(self.widthe.get()),
                                    'top': int(self.tope.get())
                                    }]

    def switchchar(self):
        self.charlabel.destroy()
        self.charinput.grid(row=1, column=0)
        self.charinput.insert(0, self.curchar)
        self.charinput.bind('<Return>', self.switchcharfinish)

    def switchcharfinish(self, event=None):
        self.curchar = self.charinput.get()
        self.charinput.destroy()
        self.charlabel = Label(text=self.curchar, font=('Times', 20, 'roman'))
        self.charlabel.grid(row=1, column=0)
        self.charinput = Entry(font=('Times', 20, 'roman'))
        self.updatest()

    def next(self, event=None):
        self.curchar = chr(ord(self.curchar)+1)
        self.updatecl()
        self.updatest()

    def prev(self, event=None):
        self.curchar = chr(ord(self.curchar)-1)
        self.updatecl()
        self.updatest()

    def updatecl(self):
        self.charlabel.destroy()
        self.charlabel = Label(text=self.curchar, font=('Times', 20, 'roman'))
        self.charlabel.grid(row=1, column=0)

    def updatest(self):
        self.st.delete(1.0, END)
        if self.curchar in self.font:
            for line in self.font[self.curchar][0]:
                self.st.insert(END, line)
                self.st.insert(END, '\n')

            self.widthe.delete(0, END)
            try:
                self.widthe.insert(0, self.font[self.curchar][1]['width'])
            except:
                self.widthe.insert(0, '0')

            self.tope.delete(0, END)
            try:
                self.tope.insert(0, self.font[self.curchar][1]['top'])
            except:
                self.tope.insert(0, '0')
        else:
            self.widthe.delete(0, END)
            self.widthe.insert(0, '0')

            self.tope.delete(0, END)
            self.tope.insert(0, '0')


inp = ''
while not isfile(inp):
    inp = input('Font file: ')

m = Main(inp)

m.mainloop()
