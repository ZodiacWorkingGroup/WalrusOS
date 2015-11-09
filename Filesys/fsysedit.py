import json
from tkinter import *
from tkinter.scrolledtext import ScrolledText


class Editor(Tk):
    def __init__(self, fname, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        for x in range(1):
            Grid.columnconfigure(self, x, weight=1)
            Grid.rowconfigure(self, x, weight=1)

        self.fname = fname
        self.data = json.loads(open(self.fname).read())

        self.filee = Entry()
        self.filee.grid(row=0, column=0)

        self.filee.bind('<Return>', self.loadf)

        self.st = ScrolledText()

        self.st.grid(row=1, column=0, sticky=N+E+S+W)

        self.meta = Frame()
        self.namel = Label(self.meta)
        self.namee = Entry(self.meta)

        self.namel.grid(row=0, column=0)
        self.namee.grid(row=0, column=1)

        self.meta.grid(row=2, column=0)

        self.bind('<Control-s>', self.save)

    def loadf(self, event=None):
        self.st.delete(1.0, END)
        self.namee.delete(0, END)

        if self.data.get(self.filee.get()):
            self.st.insert(1.0, self.data[self.filee.get()]['content'])
            self.namee.insert(0, self.data[self.filee.get()]['name'])

    def save(self, event=None):
        self.update()
        open(self.fname, 'w').write(json.dumps(self.data))

    def update(self, event=None):
        self.data[self.filee.get()] = {'name': self.namee.get(), 'content': self.st.get(1.0, END)}


main = Editor(input('Filename: '))
main.mainloop()