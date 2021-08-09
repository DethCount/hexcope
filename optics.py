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
        return points[round((z + (w - 1)) % 6)]

    z2 = 0
    for i in range(0, 6):
        z2 += points[i][2]

    z2 /= 6

    # print(' => ' + str((x2, y2, z2)))
    return (x2, y2, z2)

# n: hexcope iterations
# r: hex side length
# mx: margin over x axis between hex side and arm point
# my: margin over y axis between hex side and arm point
# alpha: arm position around mirror
def get_support_arm_point(n, r, mx, my, alpha):
    support_arm_point = hex2xy(
        r,
        math.floor(0.5 * (n + 1)),
        1 if n % 2 == 0 else 0,
        0,
        1 if n % 2 == 0 else 2
    )

    support_arm_point = (
        support_arm_point[0] + mx,
        support_arm_point[1] + my
    )

    ca = math.cos(alpha)
    sa = math.sin(alpha)
    xca = support_arm_point[0] * ca
    xsa = support_arm_point[0] * sa
    yca = support_arm_point[1] * ca
    ysa = support_arm_point[1] * sa

    return [
        (\
            xca + ysa,
            xsa - yca,
        ),
        (\
            xca - ysa,
            xsa + yca,
        )
    ]

# n: hexcope iterations
# r: hex side length
# m: margin between hex side and arm point
# arm_n: number of pairs of arm
# arm_omega: position starting angle
def get_support_arm_points(n, r, mx, my, arm_n, arm_omega):
    points = []
    for i in range(0, arm_n):
        points.append(
            get_support_arm_point(
                n,
                r,
                mx,
                my,
                arm_omega + i * math.tau / arm_n
            )
        )

    return points
