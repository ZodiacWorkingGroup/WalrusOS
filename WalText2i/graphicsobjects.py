class Line:
    def __init__(self, x1, y1, x2, y2, **kwargs):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.kwargs = kwargs

    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, self.kwarg)


class Form(list):
    def draw(self, canvas):
        for part in self:
            part.draw(canvas)


class Text(list):
    def draw(self, canvas):
        for letter in self:
            letter.draw(canvas)