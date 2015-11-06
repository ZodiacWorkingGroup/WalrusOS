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

    def _dump(self):
        return json.dumps({'name': self.name,
                           'content': self.content})