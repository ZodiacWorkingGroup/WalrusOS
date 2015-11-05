from math import sin, cos, radians


def getpoint(centre, a, b, t, theta):  # Not the issue
    x = centre[0]
    y = centre[1]
    theta = radians(theta)
    return {'x': round(x + a*cos(t)*cos(theta) - b*sin(t)*sin(theta)),  # Credit to \oren\ for this code
            'y': round(y + a*cos(t)*sin(theta) + b*sin(t)*cos(theta))
            }


def between(deg, s, e):  # Not the issue'
    s = radians(s)
    e = radians(e)
    if s <= e:
        return s <= deg <= e
    else:
        return deg >= s or deg <= e


def draw_arc(canvas, x, y, r1, r2, s, e, theta, res=1):  # The issue
    points = [[]]
    res *= 20

    step = 0
    step2 = 1/res
    while step <= 6.28:
        if between(step, s, e):
            points[-1].append((getpoint((x, y), r1, r2, step, theta), getpoint((x, y), r1, r2, step2, theta)))

        elif points[-1]:
            points.append([])

        step = step2
        step2 += 1/res

    for seg in points:
        for ln in seg:
            print(ln)
            canvas.create_line(ln[0]['x'], ln[0]['y'], ln[1]['x'], ln[1]['y'])


def draw_ellipse(canvas, x, y, r1, r2, theta, res=1):
    draw_arc(canvas, x, y, r1, r2, 0, 360, theta, res)


def draw_circle(canvas, x, y, r, res=1):
    draw_ellipse(canvas, x, y, r, r, 0, res)