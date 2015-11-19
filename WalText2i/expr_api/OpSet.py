class OpSet:
    def __init__(self, *args):
        self.contents = set(args)

    def __add__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(x+y)

        else:
            for x in self.contents:
                newcont.append(x+other)

        return OpSet(*newcont)

    def __radd__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(x+y)

        else:
            for x in self.contents:
                newcont.append(x+other)

        return OpSet(*newcont)

    def __sub__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(x-y)

        else:
            for x in self.contents:
                newcont.append(x-other)

        return OpSet(*newcont)

    def __rsub__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(y-x)

        else:
            for x in self.contents:
                newcont.append(other-x)

        return OpSet(*newcont)

    def __mul__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(x*y)

        else:
            for x in self.contents:
                newcont.append(x*other)

        return OpSet(*newcont)

    def __rmul__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(y*x)

        else:
            for x in self.contents:
                newcont.append(other*x)

        return OpSet(*newcont)

    def __truediv__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(x//y)

        else:
            for x in self.contents:
                newcont.append(x//other)

        return OpSet(*newcont)

    def __rtruediv__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(y//x)

        else:
            for x in self.contents:
                newcont.append(other//x)

        return OpSet(*newcont)

    def __mod__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(x % y)

        else:
            for x in self.contents:
                newcont.append(x % other)

        return OpSet(*newcont)

    def __rmod__(self, other):
        newcont = []
        if type(other) in [OpSet, set, list]:
            for x in self.contents:
                for y in other:
                    newcont.append(y % x)

        else:
            for x in self.contents:
                newcont.append(other % x)

        return OpSet(*newcont)

    def __repr__(self):
        return 'OpSet( '+str(self.contents)+' )'
