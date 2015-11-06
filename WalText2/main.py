import json
from WalText2.renderers import *
from tkinter import BUTT, ROUND, PROJECTING


def lexcom(com):
    com = com.split()
    r = []
    for c in com:
        if c.replace('.', '', 1).isdigit() or c[0] == '-' and c[1:].replace('.', '', 1).isdigit():
            r.append(float(c))
        else:
            r.append(c)

    return r

size = 1


def createchar(canvas, commands, x, y, color='black', scalar=1, font_weight=0):
    global size
    for com in commands:
        com = lexcom(com)
        ins = com[0]
        args = com[1:]
        if ins == 'line':
            canvas.create_line((x+args[0])*scalar, (y-args[1])*scalar, (x+args[2])*scalar, (y-args[3])*scalar,
                               fill=color, width=size, cap=PROJECTING)

        elif ins == 'circle':
            draw_circle(canvas, x+args[0], y-args[1], args[2],
                        fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'arc':
            draw_arc(canvas, x+args[0], y-args[1], args[2], args[2], args[3], args[4], 0,
                     fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'ellipse':
            draw_ellipse(canvas, x+args[0], y-args[1], args[2], args[3], args[4],
                         fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'ellarc':
            draw_arc(canvas, x+args[0], y-args[1], args[2], args[3], args[4], args[5], args[6],
                     fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'size':
            size = args[0]+font_weight


def create_text(canvas, text, font_family, line_base, color='black', charsep=10, scalar=1, font_weight=0):
    xpos = 20
    for char in text:
        global size
        size = 1+font_weight
        if font_family.get(char):
            createchar(canvas, font_family[char][0], xpos, line_base, color, scalar, font_weight)
            xpos += font_family[char][1]['width']

        elif font_family.get('unknown'):
            createchar(canvas, font_family['unknown'][0], xpos, line_base, color, scalar, font_weight)
            xpos += font_family['unknown'][1]['width']
        else:
            xpos += 30

        xpos += charsep


def loadfont(text):
    return json.loads(text)
