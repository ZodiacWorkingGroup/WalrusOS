import json
from tkinter import *
import classes
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText


class Editor(Tk):
    def __init__(self, fname, *args, **kwargs):  # This is a tangled mess. I am sorry.
        Tk.__init__(self, *args, **kwargs)
        for x in range(1):
            Grid.columnconfigure(self, x, weight=1)
            Grid.rowconfigure(self, x, weight=1)

        self.fname = fname
        self.opened = None
        self.tree = ttk.Treeview(self)
        self.ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.ysb.set)
        self.tree.heading('#0', text='Path', anchor='w')
        self.data = classes.Folder()
        self.data.load(open(self.fname).read())

        self.iidmap = {}

        self.root_node = self.tree.insert('', 'end', text='/', open=True)

        self.updatetree()

        self.st = ScrolledText()

        self.st.grid(row=1, column=1, sticky=N+E+S+W)

        self.meta = Frame()
        self.namel = Label(self.meta)
        self.namee = Entry(self.meta)

        self.namel.grid(row=0, column=0)
        self.namee.grid(row=0, column=1)

        self.tree.grid(rowspan=2, row=0, column=0, sticky=N+S+E+W)

        self.meta.grid(row=2, column=1)

        self.bind('<Control-s>', self.save)

        self.mb = Menu()
        self.fm = Menu()
        self.fm.add_command(label='Save', accelerator='Ctrl+S', command=self.save)
        self.mb.add_cascade(menu=self.fm, label='Savefile')
        self.dm = Menu()
        self.dm.add_command(label='New file', command=self.newfile)
        self.mb.add_cascade(menu=self.dm, label='Files')
        self.config(menu=self.mb)

    def loadf(self, event=None):
        self.st.delete(1.0, END)
        self.namee.delete(0, END)

        if self.data[self.opened]:
            self.st.insert(1.0, self.data[self.opened].content)
            self.namee.insert(1, self.data[self.opened].name)

    def updatetree(self):
        self.tree.delete(self.root_node)
        self.root_node = self.tree.insert('', 'end', text='/', open=True)
        for f in self.data:
            item = self.tree.insert(self.root_node, 'end', text=f, open=False)
            self.iidmap[item] = f

        self.tree.bind('<Double-1>', self.openitem)

    def openitem(self, event=None):
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.opened = self.iidmap[item]
            self.loadf()

    def save(self, event=None):
        self.update_fs()
        open(self.fname, 'w').write(json.dumps(self.data.dump()))

    def update_fs(self, event=None):
        self.data[self.opened].write(self.st.get(1.0, END))
        self.data[self.opened].rename(self.namee.get())

    def newfile(self, event=None):
        name = input('Filename: ')
        self.opened = name
        self.data.create_file(name)
        self.updatetree()


main = Editor(input('Filename: '))
main.mainloop()
