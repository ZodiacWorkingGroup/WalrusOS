import json
from WalText2.renderers import *


def lexcom(com):
    com = com.split()
    r = []
    for c in com:
        if c.replace('.', '', 1).isdigit():
            r.append(float(c))
        else:
            r.append(c)

    return r

size = 1


def drawchar(canvas, commands, x, y, color='black'):
    global size
    for com in commands:
        com = lexcom(com)
        ins = com[0]
        args = com[1:]
        if ins == 'line':
            canvas.create_line(x+args[0], y-args[1], x+args[2], y-args[3], fill=color, width=size)

        elif ins == 'circle':
            draw_circle(canvas, x+args[0], y-args[1], args[2], fill=color, width=size)

        elif ins == 'arc':
            draw_arc(canvas, x+args[0], y-args[1], args[2], args[2], args[3], args[4], 0, fill=color, width=size)

        elif ins == 'ellipse':
            draw_ellipse(canvas, x+args[0], y-args[1], args[2], args[3], 0, fill=color, width=size)

        elif ins == 'ellarc':
            draw_arc(canvas, x+args[0], y-args[1], args[2], args[3], args[4], args[5], args[6], fill=color, width=size)

        elif ins == 'size':
            size = args[0]


def render_text(canvas, text, font_family, line_base, color='black', charsep=10):
    xpos = 50
    for char in text:
        drawchar(canvas, font_family[char][0], xpos, line_base, color)
        xpos += font_family[char][1]['width']
        xpos += charsep


def loadfont(text):
    return json.loads(text)