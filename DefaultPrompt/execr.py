import re
from collections import deque

import DefaultPrompt.utility as utility


class Executer:
    def __init__(self):
        self.tp = [deque()]
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

    def do_inject(self, flags=[]):
        self.tp[self.tpi].append(self.IA[self.IAd])

    def do_push(self, flags=[]):
        self.tp[self.tpi].appendleft(self.IA[self.IAd])

    def do_eject(self, flags=[]):
        self.IA[self.IAd] = self.tp[self.tpi].popleft()

    def do_pop(self, flags=[]):
        self.IA[self.IAd] = self.tp[self.tpi].pop()

    def do_save(self, flags=[]):
        self.SA.append(self.IA[self.IAd])

    def do_retrieve(self, flags=[]):
        self.IA[self.IAd] = self.SA.pop()

    def do_west(self, flags=[]):
        self.tpi += 1
        if self.tpi > len(self.tp)-1:
            self.tp.append(deque)

    def do_east(self, flags=[]):
        self.tpi -= 1

    def do_right(self, flags=[]):
        if self.IAdcurrent:
            self.IAd += 1
        elif not self.IAdcurrent:
            self.IAi += 1

    def do_left(self, flags=[]):
        if self.IAdcurrent:
            self.IAd -= 1
        elif not self.IAdcurrent:
            self.IAi -= 1

    def do_swapp(self, flags=[]):
        self.IAdcurrent = not self.IAdcurrent

    def do_swaploc(self, flags=[]):
        self.IAd, self.IAi = self.IAi, self.IAd

    def do_echo(self, flags=[]):
        return self.IA[self.IAd]

    def do_inp(self, flags=[]):
        self.IA[self.IAi] = input()

    def do_curdir(self, flags=[]):
        self.IA[self.IAd] = self.cwd

    def do_cd(self, flags=[]):
        self.cwd = utility.simplify_path(self.cwd+self.IA[self.IAd])

    def do_add(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b+a)

    def do_sub(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b-a)

    def do_mult(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b*a)

    def do_div(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b/a)

    def do_exp(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b**a)

    def do_and(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b & a)

    def do_or(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b | a)

    def do_xor(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b ^ a)

    def do_nand(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(~(b & a))

    def do_nor(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(~(b | a))

    def do_xnor(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(~(b ^ a))

    def do_not(self, flags=[]):
        self.tp[self.tpi].appendleft(~self.tp[self.tpi].pop())

    def do_lshift(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b << a)

    def do_rshift(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b >> a)

    def do_eq(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b == a)

    def do_neq(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b != a)

    def do_lt(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b < a)

    def do_gt(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b > a)

    def do_lte(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b <= a)

    def do_gte(self, flags=[]):
        a = self.tp[self.tpi].pop()
        b = self.tp[self.tpi].pop()
        self.tp[self.tpi].appendleft(b >= a)


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

        else:
            return getattr(self, 'do_'+com.lower(), lambda: None)()

    def runline(self, line):
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