from math import sin, cos, radians


def getpoint(centre, a, b, t, theta):  # Not the issue
    x = centre[0]
    y = centre[1]
    theta = radians(theta)
    return {'x': round(x + a*cos(t)*cos(theta) - b*sin(t)*sin(theta)),  # Credit to \oren\ from IRC for this code
            'y': round(y + a*cos(t)*sin(theta) + b*sin(t)*cos(theta))
            }


def between(deg, s, e):  # Not the issue'
    s = radians(s)
    e = radians(e)
    if s <= e:
        return s <= deg <= e
    else:
        return deg >= s or deg <= e


def draw_arc(canvas, x, y, r1, r2, s, e, theta, res=1, scalar=1, **kwargs):  # The issue
    points = [[]]
    res *= 20

    step = 0
    step2 = 1/res
    r = []
    while step <= 6.28:
        if between(step, s, e):
            points[-1].append((getpoint((x, y), r1, r2, step, theta), getpoint((x, y), r1, r2, step2, theta)))

        elif points[-1]:
            points.append([])

        step = step2
        step2 += 1/res

    for seg in points:
        for ln in seg:
            r.append(canvas.create_line(ln[0]['x']*scalar, ln[0]['y']*scalar, ln[1]['x']*scalar, ln[1]['y']*scalar,
                                        **kwargs))

    return r  # So that I can delete specific lines


def draw_ellipse(canvas, x, y, r1, r2, theta, res=1, scalar=1, **kwargs):
    return draw_arc(canvas, x, y, r1, r2, 0, 360, theta, res, scalar, **kwargs)


def draw_circle(canvas, x, y, r, res=1, scalar=1, **kwargs):
    print('x='+str(x))
    print('y='+str(y))
    print('r='+str(r))
    return draw_ellipse(canvas, x, y, r, r, 0, res, scalar, **kwargs)


def draw_parabarc(canvas, x, y, a, b, c, start, end, theta=0, res=1, scalar=1, **kwargs):
    points = []
    res *= 20
    step = start
    step2 = start+1/res
    while step < end:
        points.append(((x + step, y - a*(step**2) + b*step + c), (x + step2, y - a*step2**2 + b*step2 + c)))
        step = step2
        step2 += 1/res

    r = []

    for ln in points:
        r.append(canvas.create_line(ln[0][0]*scalar, ln[0][1]*scalar, ln[1][0]*scalar, ln[1][1]*scalar,
                                    **kwargs))

    return r
