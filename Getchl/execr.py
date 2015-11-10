from collections import deque


class Executer:
    def __init__(self):
        self.mode = 'default'
        self.coms = []

        self.tape = [deque()]
        self.ti = 0
        self.acc = 0

        self.deque = None
        self.update()

        self.block = []

    def update(self):
        self.deque = self.tape[self.ti]

    def com_20(self):  # <space>
        pass

    def com_21(self):  # !
        self.deque.append(int(not bool(self.deque.pop())))

    def com_22(self):  # "
        self.mode = 'string'

    def com_23(self):  # #
        pass

    def com_24(self):  # $
        self.deque.pop()

    def com_25(self):  # %
        a = self.deque.pop()
        b = self.deque.pop()
        self.deque.append((b % a) % 256)

    def com_26(self):  # &
        print(str(self.deque.pop()), end='')

    def com_27(self):  # '
        pass

    def com_28(self):  # (
        self.mode = 'blockbuilding'
        self.block = []

    def com_29(self):  # )
        pass

    def com_2A(self):  # *
        a = self.deque.pop()
        b = self.deque.pop()
        self.deque.append((b*a) % 256)

    def com_2B(self):  # +
        a = self.deque.pop()
        b = self.deque.pop()
        self.deque.append(b+a)

    def com_2C(self):  # ,
        self.mode = 'input'

    def com_2D(self):  # -
        a = self.deque.pop()
        b = self.deque.pop()
        self.deque.append((b-a) % 256)

    def com_2E(self):
        print(chr(self.deque.pop()), end='')

    def com_2F(self):  # /
        a = self.deque.pop()
        b = self.deque.pop()
        self.deque.append((b//a) % 256)

    def evalcom(self, char):
        if self.mode == 'default':
            self.coms.append('com_'+hex(ord(char))[2:].upper().zfill(2))
            getattr(self, self.coms[-1])()

        elif self.mode == 'string':
            if char == '"':
                self.mode = 'default'
            else:
                self.deque.append(ord(char))

        elif self.mode == 'blockbuilding':
            if char == ')':
                self.mode = 'default'
                self.coms.append(self.block)
            else:
                self.block.append(char)

    def evalgroup(self, group):
        for char in group:
            self.evalcom(char)
