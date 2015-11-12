from sys import exit


class Executer:
    def __init__(self):
        self.mode = ['default']
        self.coms = []

        self.rawcoms = ''
        self.labels = {}

        self.tape = {0: []}
        self.ti = 0
        self.acc = 0
        self.max = 0
        self.safe = False
        self.prime = 0

        self.qm = False

        self.globals = {}
        self.globalstrs = {}
        self.funcs = {}

        self.stack = self.tape[0]

        self.block = []

    def update(self):
        if self.ti in self.tape:
            self.stack = self.tape[self.ti]
        else:
            self.tape[self.ti] = []
            self.stack = self.tape[self.ti]

    def pop(self):
        if len(self.stack) == 0:
            return 0
        else:
            return self.stack.pop()

    def popnts(self):
        popped = None
        ret = ''
        while popped != 0 and len(self.stack) > 0:
            popped = self.pop()
            ret += chr(popped)

        return ret.strip('\0')

    def push(self, v):
        if len(self.stack) < self.max or self.max == 0:
            if self.qm:
                self.stack.insert(0, int(v) % 256)
            else:
                self.stack.append(int(v) % 256)

    def com_20_p0(self):  # <space>
        return 0

    def com_21_p0(self):  # !
        if self.max == 0 or len(self.stack) < self.max:
            self.push(int(not bool(self.pop())))
            return 0
        else:
            return -2

    def com_22_p0(self):  # "
        self.mode.append('string')
        return 0

    def com_23_p0(self):  # #
        pass

    def com_24_p0(self):  # $
        if len(self.stack) > 0:
            self.pop()
        else:
            return -1

    def com_25_p0(self):  # %
        if len(self.stack) < 2 and not self.safe:
            return -1
        elif self.stack[-2] == 0 or len(self.stack) < 2:
            return -3
        else:
            a = self.pop()
            b = self.pop()
            self.push(b % a)
            return 0

    def com_26_p0(self):  # &
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b & a)
            return 0

    def com_27_p0(self):  # '
        self.prime += 1
        return 0

    def com_28_p0(self):  # (
        self.mode.append('blockbuilding')
        self.block = []
        return 0

    def com_29_p0(self):  # )
        pass

    def com_2a_p0(self):  # *
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b*a)

    def com_2b_p0(self):  # +
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b+a)

    def com_2c_p0(self):  # ,
        self.mode.append('input')
        return 0

    def com_2d_p0(self):  # -
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b-a)

    def com_2e_p0(self):  # .
        if len(self.stack) < 1 and not self.safe:
            return -1
        else:
            out = self.pop()
            print(chr(out), end='')
            if out == 0:
                return -6
            else:
                return 0

    def com_2f_p0(self):  # /
        if len(self.stack) < 2 and not self.safe:
            return -1
        elif self.stack[-2] == 0 or len(self.stack) < 2:
            return -3
        else:
            a = self.pop()
            b = self.pop()
            self.push(b//a)
            return 0

    def com_30_p0(self):  # 0
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(0)
            return 0

    def com_31_p0(self):  # 1
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(1)
            return 0

    def com_32_p0(self):  # 2
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(2)
            return 0

    def com_33_p0(self):  # 3
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(3)
            return 0

    def com_34_p0(self):  # 4
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(4)
            return 0

    def com_35_p0(self):  # 5
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(5)
            return 0

    def com_36_p0(self):  # 6
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(6)
            return 0

    def com_37_p0(self):  # 7
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(7)
            return 0

    def com_38_p0(self):  # 8
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(8)
            return 0

    def com_39_p0(self):  # 9
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(9)
            return 0

    def com_3a_p0(self):  # :
        if len(self.stack) == 0 and not self.safe:
            return -1
        elif len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            a = self.pop()
            self.push(a)
            self.push(a)
            return 0

    def com_3b_p0(self):  # ;
        exit()

    def com_3c_p0(self):  # <
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b < a)
            return 0

    def com_3d_p0(self):  # =
        if len(self.stack) == 0 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b == a)
            return 0

    def com_3e_p0(self):  # >
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b > a)
            return 0

    def com_3f_p0(self):  # ?
        if len(self.stack) < 3 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            c = self.pop()
            if a != 0:
                self.push(b)
            else:
                self.push(c)
            return 0

    def com_40_p0(self):  # @
        cont = 0
        while cont == 0:
            cont = self.evalgroup(self.coms[-2])

    def com_41_p0(self):  # A
        self.push(10)
        return 0

    def com_42_p0(self):  # B
        self.push(11)
        return 0

    def com_43_p0(self):  # C
        self.push(12)
        return 0

    def com_44_p0(self):  # D
        self.push(13)
        return 0

    def com_45_p0(self):  # E
        self.push(14)
        return 0

    def com_46_p0(self):  # F
        self.push(15)
        return 0

    def com_47_p0(self):  # G
        if len(self.stack) < 1 and not self.safe:  # Remember: The null name for a variable is a valid name in this case
            return -1
        else:
            v = self.pop()
            s = self.popnts()
            self.globals[s] = v
            return 0

    def com_48_p0(self):  # H
        pass

    def com_49_p0(self):  # I
        self.stack = self.stack[::-1]
        return 0

    def com_4a_p0(self):  # J
        if len(self.stack) == 0 and not self.safe:
            return -1
        else:
            j = self.pop()-127
            self.ti += j
            self.update()
            return 0

    def com_4b_p0(self):  # K
        pass

    def com_4c_p0(self):  # L
        self.ti += 1
        self.update()
        return 0

    def com_4d_p0(self):  # M
        if len(self.stack) == 0 and not self.safe:
            return -1
        else:
            self.max = self.pop()
            for x in self.tape:
                while len(self.tape[x]) > self.max:
                    del self.tape[x][-1]
            return 0

    def com_4e_p0(self):  # N
        pass

    def com_4f_p0(self):  # O
        pass

    def com_50_p0(self):  # P
        pass

    def com_51_p0(self):  # Q
        self.qm = not self.qm
        return 0

    def com_52_p0(self):  # R
        self.ti -= 1
        self.update()
        return 0

    def com_53_p0(self):  # S
        pass

    def com_54_p0(self):  # T
        pass

    def com_55_p0(self):  # U
        pass

    def com_56_p0(self):  # V
        pass

    def com_57_p0(self):  # W
        pass

    def com_58_p0(self):  # X
        pass

    def com_59_p0(self):  # Y
        pass

    def com_5a_p0(self):  # Z
        pass

    def com_5b_p0(self):  # [
        if len(self.stack) < 3 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            c = self.pop()

            self.push(a)
            self.push(c)
            self.push(b)

            return 0

    def com_5c_p0(self):  # \
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(a)
            self.push(b)

            return 0

    def com_5d_p0(self):  # [
        if len(self.stack) < 3 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            c = self.pop()

            self.push(b)
            self.push(a)
            self.push(c)

            return 0

    def com_5e_p0(self):  # ^
        if len(self.stack) < 1 and not self.safe:
            return -1
        else:
            a = self.pop()
            self.acc = a
            return 0

    def com_5f_p0(self):  # _
        if len(self.stack) == self.max and not self.max == 0:
            return -2
        else:
            self.push(self.acc)
            return 0

    def com_60_p0(self):  # `
        if len(self.stack) < 1 and not self.safe:
            return -2
        else:
            ch = self.pop()
            self.evalcom(ch)

    def com_61_p0(self):  # a
        pass

    def com_62_p0(self):  # b
        pass

    def com_63_p0(self):  # c
        pass

    def com_64_p0(self):  # d
        pass

    def com_65_p0(self):  # e
        pass

    def com_66_p0(self):  # f
        pass

    def com_67_p0(self):  # g
        pass

    def com_68_p0(self):  # h
        pass

    def com_69_p0(self):  # i
        if len(self.stack) < 1 and not self.safe:
            return -1
        else:
            self.push(self.pop())
            return 0

    def com_6a_p0(self):  # j
        pass

    def com_6b_p0(self):  # k
        pass

    def com_6c_p0(self):  # l
        pass

    def com_6d_p0(self):  # m
        pass

    def com_6e_p0(self):  # n
        pass

    def com_6f_p0(self):  # o
        pass

    def com_70_p0(self):  # p
        pass

    def com_71_p0(self):  # q
        pass

    def com_72_p0(self):  # r
        pass

    def com_73_p0(self):  # s
        pass

    def com_74_p0(self):  # t
        pass

    def com_75_p0(self):  # u
        pass

    def com_76_p0(self):  # v
        pass

    def com_77_p0(self):  # w
        pass

    def com_78_p0(self):  # x
        pass

    def com_79_p0(self):  # y
        pass

    def com_7a_p0(self):  # z
        pass

    def com_7b_p0(self):  # {
        self.mode.append('comment')

    def com_7c_p0(self):  # |
        if len(self.stack) < 2 and not self.safe:
            return -1
        else:
            a = self.pop()
            b = self.pop()
            self.push(b & a)
            return 0

    def com_7d_p0(self):  # }
        pass

    def com_7e_p0(self):  # ~
        self.safe = not self.safe
        return 0

    def evalcom(self, char):
        mode = self.mode[-1]

        if self.rawcoms[-1] != "'":
            self.prime = 0

        self.rawcoms += char
        if mode == 'default':
            self.coms.append('com_'+hex(ord(char))[2:].lower().zfill(2)+'p'+str(self.prime))
            return getattr(self, self.coms[-1])()

        elif mode == 'string':
            if char == '"':
                self.mode.pop()
            else:
                self.push(ord(char))

        elif mode == 'blockbuilding':
            if char == ')':
                self.mode.pop()
                self.coms.append(self.block)
            else:
                self.block.append(char)

        elif mode == 'input':
            if char:
                self.push(ord(char))
            else:
                return -5

        elif mode == 'comment':
            if char == '}':
                self.mode.pop()

        return 0

    def evalgroup(self, group):
        rets = []
        for char in group:
            rets.append(self.evalcom(char))

        return rets

    def reexecutefrom(self, label):
        start = self.labels[label]
        for ch in self.rawcoms[start:]:
            self.evalcom(ch)

