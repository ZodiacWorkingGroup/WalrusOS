import json
import WalText2.renderers as rend
from tkinter import BUTT, ROUND, PROJECTING
import unicodedata  # For combining diacritic detection

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')  # Unicode support (for ? character)


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

        elif ins == 'rect':
            canvas.create_rectangle((x+args[0])*scalar, (y-args[1])*scalar, (x+args[2])*scalar, (y-args[3])*scalar,
                                    outline=color)

        elif ins == 'fillrect':
            canvas.create_rectangle((x+args[0])*scalar, (y-args[1])*scalar, (x+args[2])*scalar, (y-args[3])*scalar,
                                    outline=color, fill=color)

        elif ins == 'circle':
            rend.draw_circle(canvas, x+args[0], y-args[1], args[2],
                        fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'arc':
            rend.draw_arc(canvas, x+args[0], y-args[1], args[2], args[2], args[3], args[4], 0,
                     fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'ellipse':
            rend.draw_ellipse(canvas, x+args[0], y-args[1], args[2], args[3], args[4],
                         fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'ellarc':
            rend.draw_arc(canvas, x+args[0], y-args[1], args[2], args[3], args[4], args[5], args[6],
                     fill=color, scalar=scalar, width=size, cap=PROJECTING)

        elif ins == 'size':
            size = args[0]+font_weight


def create_text(canvas, text, font_family, line_base, color='black', charsep=10, scalar=1, font_weight=0, cursor=False):
    xpos = 20
    for char in text:
        global size
        size = 1+font_weight
        if not unicodedata.combining(char):
            lastleft = xpos
            if font_family.get(char):
                try:
                    createchar(canvas, font_family[char][0], xpos, line_base, color, scalar, font_weight)
                    xpos += font_family[char][1]['width']
                    lasttop = int(font_family[char][1].get('top', 0))
                except IndexError as e:
                    print('Errored char: '+char)
                    raise e

            elif font_family.get('unknown'):
                createchar(canvas, font_family['unknown'][0], xpos, line_base, color, scalar, font_weight)
                xpos += font_family['unknown'][1]['width']
                lasttop = font_family['unknown'][1].get('top', 0)
            else:
                createchar(canvas, ['line 0 0 14 0', 'line 0 14 14 14', 'line 0 0 0 14', 'line 14 0 14 14'])
                xpos += 14
                lasttop = 14

        else:
            if font_family.get(char):
                createchar(canvas, font_family[char][0], lastleft, lasttop+3, color, scalar, font_weight)

        xpos += charsep

    if cursor:
        canvas.create_line(xpos, line_base, xpos, line_base+14)


def loadfont(text):
    return json.loads(text)
