import math

# f : focal length
# d : parabola height
# r : distance from parabola center
def parabolic_z(f, r):
    return (r * r) / (2 * f)

# f: focal length
# r: mirror radius
# d: distance to center in xy plane
def spherical_z(f, r, d):
    return math.sqrt(f - d ** 2) - math.sqrt(f - r ** 2)

# r : hex side length
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
# w : hex triangle vertex index cw from center
def hex2xy(r, x, y, z, w):
    # print('hex2xy: ' + str((r, x, y, z, w)))
    ytheta = math.pi / 6
    x2 = x * (3 * r)
    ytemp = y * (math.sqrt(3) * r)
    x2 += ytemp * math.cos(ytheta)
    y2 = ytemp * math.sin(ytheta)

    points = []
    for i in range(0, 6):
        theta = i * math.pi / 3
        x3 = x2 + r * math.cos(theta)
        y3 = y2 + r * math.sin(theta)
        points.append((
            x3,
            y3
        ))

    if w != 0:
        # print(' => ' + str(points[(z + (w - 1)) % 6]))
        return points[(z + (w - 1)) % 6]

    # print(' => ' + str((x2, y2)))
    return (x2, y2)

# f : focal length
# r : hex side length
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
# w : hex triangle vertex index cw from center
def hex2xyz(f, r, x, y, z, w):
    # print('hex2xyz: ' + str((f, r, x, y, z, w)))
    ytheta = math.pi / 6
    x2 = x * (3 * r)
    ytemp = y * (math.sqrt(3) * r)
    x2 += ytemp * math.cos(ytheta)
    y2 = ytemp * math.sin(ytheta)

    points = []
    for i in range(0, 6):
        theta = i * math.pi / 3
        x3 = x2 + r * math.cos(theta)
        y3 = y2 + r * math.sin(theta)
        points.append((
            x3,
            y3,
            parabolic_z(f, math.sqrt(x3 * x3 + y3 * y3))
        ))

    if w != 0:
        # print(' => ' + str(points[(z + (w - 1)) % 6]))
        return points[(z + (w - 1)) % 6]

    z2 = 0
    for i in range(0, 6):
        z2 += points[i][2]

    z2 /= 6

    # print(' => ' + str((x2, y2, z2)))
    return (x2, y2, z2)