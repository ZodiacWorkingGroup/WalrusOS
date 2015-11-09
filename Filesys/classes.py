import json


class File:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def rename(self, newname):
        self.name = newname

    def read(self):
        return self.content

    def write(self, newcont):
        self.content = newcont

    def write_append(self, text):
        self.content += text

    def dump(self):
        return json.dumps({'name': self.name,
                           'content': self.content})


class Folder:
    def __init__(self):
        self.files = {}

    def __getitem__(self, item):
        return self.files[item]

    def create_file(self, name):
        self.files[name] = File(name, '')
        return self.files[name]  # Return a reference to the file

    def is_file(self, name):
        return name in self.files

    def dump(self):
        dumpable = {}
        for key in self.files:
            dumpable[key] = self.files[key].dump()

        return json.dumps(dumpable)

    def load(self, string):
        files = json.loads(string)
        for f in files:
            self.files[f] = File(files[f]['name'], files[f]['content'])