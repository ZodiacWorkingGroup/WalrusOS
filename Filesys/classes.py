import json
import networkx as nx
from networkx.readwrite import json_graph


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
        return {'name': self.name,
                'content': self.content}


class Folder:
    def __init__(self):
        self.files = {}

    def __getitem__(self, item):
        return self.files[item]

    def __iter__(self):
        for key in self.files.keys():
            yield key

    def create_file(self, name):
        self.files[name] = File(name, '')
        return self.files[name]  # Return a reference to the file

    def is_file(self, name):
        return name in self.files

    def dump(self):
        dumpable = {}
        for key in self.files:
            dumpable[key] = self.files[key].dump()

        return dumpable

    def load(self, string):
        files = json.loads(string)
        for f in files:
            self.files[f] = File(files[f]['name'], files[f]['content'])


class FileSys:
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.G.add_node('!', data=Folder())

    def resolve_file(self, path):
        if path[0] in self.G.nodes():
            last = path[0]
        else:
            return None

        for x in path[1:]:
            edges = self.G.edges()
            connections = []
            for x in edges:
                if x[0] == last:
                    connections.append(x[1])

            if x in connections:
                last = x
            elif self.G.node[last]['data'].is_file(x):
                return self.G.node[last]['data'][x]
            else:
                return None

        return self.G.node[last]['data']

    def create_folder(self, parent, name):
        self.data[name] = Folder()
        self.G.add_node(name)
        self.G.add_edge(self.data[parent], self.data[name])

    def dump(self):
        dumpable = {}
        dumpable['structure'] = json_graph.node_link_data(self.G)
        for datum in self.data:
            dumpable['data'][datum] = self.data[datum].dump()

        return json.dump(dumpable)

    def load(self, content):
        loaded = json.loads(content)
        self.G = json_graph.node_link_graph(loaded['structure'])

        for folder in loaded['data']:
            temp = Folder()
            temp.load(loaded['data'][folder])
            self.data[folder] = temp


if __name__ == '__main__':
    fs = FileSys()
    file = fs.resolve_file(['!'])
    file.create_file('testfile')
    fs.resolve_file(['!', 'testfile']).write('This file is a test!')

    print(fs.resolve_file(['!', 'testfile']).read())
