import re
from collections import deque

import DefaultPrompt.utility as utility


class Executer:
    def __init__(self):
        self.tp = [deque()]
        self.filesys = None
        self.tpi = 0
        self.SA = []
        self.IA = [0]
        self.IAd = 0
        self.IAi = 0

        self.IAdcurrent = True

        self.cwd = '!'

        self.strre = re.compile(r'^"[^"\\]*(?:\\.[^"\\]*)*"')
        self.numre = re.compile(r'^-?[0-9]+(\.[0-9]+)?$')
        self.boolre = re.compile(r'^(True|False)$')

    def do_inject(self, flags=None):
        self.tp[self.tpi].appendleft(self.IA[self.IAd])

    def do_push(self, flags=None):
        self.tp[self.tpi].append(self.IA[self.IAd])

    def do_eject(self, flags=None):
        self.IA[self.IAd] = self.tp[self.tpi].popleft()

    def do_pop(self, flags=None):
        self.IA[self.IAd] = self.tp[self.tpi].pop()

    def do_save(self, flags=None):
        self.SA.append(self.IA[self.IAd])

    def do_retrieve(self, flags=None):
        self.IA[self.IAd] = self.SA.pop()

    def do_west(self, flags=None):
        self.tpi += 1
        if self.tpi > len(self.tp)-1:
            self.tp.append(deque)

    def do_east(self, flags=None):
        self.tpi -= 1

    def do_right(self, flags=None):
        if self.IAdcurrent:
            self.IAd += 1
            if self.IAd > len(self.IA)-1:
                self.IA.append(0)
        elif not self.IAdcurrent:
            self.IAi += 1
            if self.IAi > len(self.IA)-1:
                self.IA.append(0)

    def do_left(self, flags=None):
        if self.IAdcurrent:
            self.IAd -= 1
        elif not self.IAdcurrent:
            self.IAi -= 1

    def do_swapp(self, flags=None):
        self.IAdcurrent = not self.IAdcurrent

    def do_swaploc(self, flags=None):
        self.IAd, self.IAi = self.IAi, self.IAd

    def do_echo(self, flags=None):
        return self.IA[self.IAd]

    def do_inp(self, flags=None):
        self.IA[self.IAi] = input()

    def do_cat(self, flags=None):
        self.IA[self.IAi] = self.filesys[self.IA[self.IAd]]

    def do_curdir(self, flags=None):
        self.IA[self.IAd] = self.cwd

    def do_cd(self, flags=None):
        self.cwd = utility.simplify_path(self.cwd+self.IA[self.IAd])

    def do_touch(self, flags=None):
        self.filesys.create_file(self.IA[self.IAd])

    def do_write(self, flags=None):
        self.filesys[self.IA[self.IAd]].write(self.IA[self.IAd+1])

    def do_add(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b+a)

    def do_sub(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b-a)

    def do_mult(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b*a)

    def do_div(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b/a)

    def do_mod(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b%a)

    def do_exp(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b**a)

    def do_and(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b & a)

    def do_or(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b | a)

    def do_xor(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b ^ a)

    def do_nand(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(~(b & a))

    def do_nor(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(~(b | a))

    def do_xnor(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(~(b ^ a))

    def do_not(self, flags=None):
        self.tp[self.tpi].append(~self.tp[self.tpi].pop())

    def do_lshift(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b << a)

    def do_rshift(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b >> a)

    def do_eq(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b == a)

    def do_neq(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b != a)

    def do_lt(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b < a)

    def do_gt(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b > a)

    def do_lte(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b <= a)

    def do_gte(self, flags=None):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].append(b >= a)

    def do___printdeque(self, flags=None):
        return self.tp[self.tpi]

    def do___printacc(self, flags=None):
        return self.IA

    def evalcom(self, com):
        if self.strre.match(com):
            if self.IAdcurrent:
                self.IA[self.IAd] = str(bytes(com[1:-1], 'utf-8').decode('unicode-escape'))
            else:
                self.IA[self.IAi] = com[1:-1]

        elif self.numre.match(com):
            if self.IAdcurrent:
                self.IA[self.IAd] = float(com)
            else:
                self.IA[self.IAi] = float(com)

        elif self.boolre.match(com):
            if self.IAdcurrent:
                self.IA[self.IAd] = bool(com)
            else:
                self.IA[self.IAi] = bool(com)

        elif 'do_'+com.lower() in dir(self):
            return getattr(self, 'do_'+com.lower(), lambda: None)()

        elif self.filesys.is_file(com.lower()):
            for line in self.filesys[com.lower()].read().split('\n'):
                self.runline(line, self.filesys)

        else:
            print('Unknown command: '+com.lower())

    def runline(self, line, filesys):
        self.filesys = filesys
        line = line.strip()
        todo = ['']
        r = ''
        stringmode = False
        for char in line:
            if char == '"':
                stringmode = not stringmode

            if char == ' ' and not stringmode:
                todo.append('')

            if char != ' ' or stringmode:
                todo[-1] += char

        for com in todo:
            if com:
                out = self.evalcom(com)
                if out:
                    r += str(out)

        return r


if __name__ == '__main__':
    e = Executer()
    e.runline(input('> '))
    while True:
        e.runline(input('\n> '))
