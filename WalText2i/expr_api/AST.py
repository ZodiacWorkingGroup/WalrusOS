from random import randrange


class Exp:
    def __repr__(self):
        return str(dir(self))


class NumExp(Exp):
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        if type(self.val) == str:
            return float(self.val)
        else:
            return self.val

    def __repr__(self):
        return '(NumExp: '+repr(self.val)+')'


class InumExp(Exp):
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        return self.val

    def __repr__(self):
        return '(InumExp: '+repr(self.val)+')'


class VarExp(Exp):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env.get(self.name)

    def __repr__(self):
        return '(VarExp: '+repr(self.name)+')'


class BinopAexp(Exp):
    def __init__(self, l, r, op):
        self.left = l
        self.right = r
        self.op = op

    def eval(self, env):
        if self.op == '~':
            lr = self.left.eval(env).real
            rr = self.right.eval(env).real
            li = self.left.eval(env).imag
            ri = self.right.eval(env).imag

            if lr == rr and li == ri:
                return complex(lr, li)
            elif lr == rr and li != ri:
                return complex(lr, randrange(li, ri))
            elif lr != rr and li == ri:
                return complex(randrange(lr, rr), li)
            else:
                return complex(randrange(lr, rr),
                       randrange(li, ri))

        elif self.op == '..':
            return OpSet(*[range(self.left.eval(env), self.right.evel(env))])

        elif self.op == '|':
            return None

        elif self.op == '+':
            return self.left.eval(env)+self.right.eval(env)

        elif self.op == '-':
            return self.left.eval(env)-self.right.eval(env)

        elif self.op == '*':
            return self.left.eval(env)*self.right.eval(env)

        elif self.op == '/':
            return self.left.eval(env)/self.right.eval(env)

        elif self.op == '%':
            return self.left.eval(env)%self.right.eval(env)

    def __repr__(self):
        return '(BinopExp: '+repr(self.op)+', '+repr(self.left)+', '+repr(self.right)+')'


class UnopAexp(Exp):
    def __init__(self, arg, op):
        self.arg = arg
        self.op = op

    def eval(self, env):
        if self.op == '-':
            return -self.arg.eval(env)
        elif self.op == '$':
            return self.arg.eval(env).conjugate()

    def __repr__(self):
        return '(UnOpExp: '+repr(self.op)+', '+repr(self.arg)+')'


class ParenExp(Exp):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        return self.exp.eval(env)

    def __repr__(self):
        return '(ParenExp: '+repr(self.exp)+')'
