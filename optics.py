import math

from mathutils import Vector

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

def get_support_arm_point_margin_x(n, r):
    return 0.5 * (n % 2) * r

def get_support_arm_point_margin_y(n, r):
    return - 0.25 * math.sqrt(3) * r

def get_right_boundary_hex_xyz(f, n, r):
    return hex2xyz(
        f,
        r,
        math.floor(0.5 * (n + 1)),
        1 if n % 2 == 0 else 0,
        0,
        1 if n % 2 == 0 else 2
    )

def get_right_boundary_hex_xy(n, r):
    return hex2xy(
        r,
        math.floor(0.5 * (n + 1)),
        1 if n % 2 == 0 else 0,
        0,
        1 if n % 2 == 0 else 2
    )

# n: hexcope iterations
# r: hex side length
# alpha: arm position around mirror
def get_support_arm_point(n, r, alpha = 0):
    support_arm_point = get_right_boundary_hex_xy(n, r)
    support_arm_point = (
        support_arm_point[0] + get_support_arm_point_margin_x(n, r),
        support_arm_point[1] + get_support_arm_point_margin_y(n, r)
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
# arm_n: number of pairs of arm
# arm_omega: position starting angle
def get_support_arm_points(n, r, arm_n, arm_omega):
    points = []
    for i in range(0, arm_n):
        points.append(
            get_support_arm_point(
                n,
                r,
                arm_omega + i * math.tau / arm_n
            )
        )

    return points

def get_newton_dist_to_spider_arm(arm_n, rx, ry):
    dists = list()

    cpi4m = math.cos(-0.25 * math.pi)
    for i in range(0, arm_n):
        alpha = 0.5 * math.pi + i * math.tau / arm_n
        a = rx * cpi4m
        e = math.sqrt(1 - (a / ry) ** 2)

        dists.append(
            math.sqrt(a ** 2 / (1 - e ** 2 * math.cos(alpha) ** 2))
        )

    return dists

def get_spherical_dist_to_spider_arm(arm_n, r):
    dists = list()
    for i in range(0, arm_n):
        dists.append(r)

    return dists