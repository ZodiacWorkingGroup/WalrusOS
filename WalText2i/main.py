import json
import WalText2i.renderers as rend
from tkinter import PROJECTING
from math import degrees
from WalText2i.expr_api import exp_parser
import unicodedata  # For combining diacritic detection

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')


def lexcom(com):
    return com.split()

size = 1


def createchar(canvas, commands, x, y, color='black', scalar=1, font_weight=0):
    global size
    r = []
    env = {}
    for com in commands:
        com = lexcom(com)
        ins = com[0]
        args = com[1:]
        if ins == '=':
            env[args[0]] = exp_parser.parse(args[1]).eval(env)

        elif ins == 'line':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            r.append(canvas.create_line((x+args[0].real)*scalar, (y-args[0].imag)*scalar,
                                        (x+args[1].real)*scalar, (y-args[1].imag)*scalar,
                                        fill=color, width=size, cap=PROJECTING))

        elif ins == 'rect':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            r.append(canvas.create_rectangle((x+args[0].real)*scalar, (y-args[0].imag)*scalar,
                                             (x+args[0].real)*scalar, (y-args[1].imag)*scalar,
                                             outline=color))

        elif ins == 'fillrect':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            r.append(canvas.create_rectangle((x+args[0].real)*scalar, (y-args[0].imag)*scalar,
                                             (x+args[1].real)*scalar, (y-args[1].imag)*scalar,
                                             outline=color, fill=color))

        elif ins == 'circle':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            print(args)
            print(args[0].real)
            r.append(rend.draw_circle(canvas, x+args[0].real, y-args[0].imag, args[1].real,
                                      fill=color, scalar=scalar, width=size, cap=PROJECTING))

        elif ins == 'arc':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            args[2] = exp_parser.parse(args[2]).eval(env)
            args[3] = exp_parser.parse(args[3]).eval(env)
            r.append(rend.draw_arc(canvas, x+args[0].real, y-args[0].imag,
                                   args[1].real, args[1].real, args[2].real, args[3].real, 0,
                                   fill=color, scalar=scalar, width=size, cap=PROJECTING))

        elif ins == 'ellipse':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            args[2] = exp_parser.parse(args[2]).eval(env)
            args[3] = exp_parser.parse(args[3]).eval(env)
            r.append(rend.draw_ellipse(canvas, x+args[0].real, y-args[0].real, args[1].real, args[2].real, args[3].real,
                                       fill=color, scalar=scalar, width=size, cap=PROJECTING))

        elif ins == 'ellarc':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            args[2] = exp_parser.parse(args[2]).eval(env)
            args[3] = exp_parser.parse(args[3]).eval(env)
            args[4] = exp_parser.parse(args[4]).eval(env)
            args[5] = exp_parser.parse(args[5]).eval(env)
            r.append(rend.draw_arc(canvas, x+args[0].real, y-args[0].imag, args[1].real, args[2].real, args[3].real,
                                   args[4].real, args[5].real,
                                   fill=color, scalar=scalar, width=size, cap=PROJECTING))

        elif ins == 'parabarc':
            args[0] = exp_parser.parse(args[0]).eval(env)
            args[1] = exp_parser.parse(args[1]).eval(env)
            args[2] = exp_parser.parse(args[2]).eval(env)
            args[3] = exp_parser.parse(args[3]).eval(env)
            args[4] = exp_parser.parse(args[4]).eval(env)
            args[5] = exp_parser.parse(args[5]).eval(env)

            r.append(rend.draw_parabarc(canvas, x+args[0].real, y-args[0].imag, args[1].real, args[2].real,
                                        args[3].real, args[4].real, args[5].real,
                                        fill=color, scalar=scalar, width=size, cap=PROJECTING))

        elif ins == 'size':
            args[0] = exp_parser.parse(args[0]).eval(env)
            size = args[0].real+font_weight

    return r


def create_text(canvas, text, font_family, line_base, color='black', charsep=10, scalar=1, font_weight=0, cursor=False):
    xpos = 20
    r = []
    lastleft = 0
    lasttop = 0
    for char in text:
        print(char)
        global size
        size = 1+font_weight
        if not unicodedata.combining(char):
            lastleft = xpos
            if font_family.get(char):
                try:
                    r.append(createchar(canvas, font_family[char][0], xpos, line_base, color, scalar, font_weight))
                    xpos += exp_parser.parse(str(font_family[char][1].get('width', '0'))).eval({}).real
                    lasttop = exp_parser.parse(str(font_family[char][1].get('top', '0'))).eval({}).real
                except IndexError as e:
                    print('Errored char: '+char)
                    raise e

            elif font_family.get('unknown'):
                r.append(createchar(canvas, font_family['unknown'][0], xpos, line_base, color, scalar, font_weight))
                xpos += exp_parser.parse(str(font_family['unknown'][1].get('width', '0'))).eval({}).real
                lasttop = exp_parser.parse(str(font_family['unknown'][1].get('top', '0'))).eval({}).real
            else:
                r.append(createchar(canvas, ['line 0+0i 14+0i', 'line 0+14i 14+14i',
                                             'line 0+0i 0+14i', 'line 14+0i 14+14i'],
                                    xpos, line_base, color, scalar, font_weight))
                xpos += 14
                lasttop = 14

        else:
            if font_family.get(char):
                r.append(createchar(canvas, font_family[char][0], lastleft, lasttop+3, color, scalar, font_weight))

        xpos += charsep

    if cursor:
        canvas.create_line(xpos, line_base, xpos, line_base+16)

    return r


def loadfont(text):
    return json.loads(text)
