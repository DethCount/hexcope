import bpy
import math
from mathutils import Euler

n = 1 # max distance (in r unit)
r = 1.0 # hex side
h = 0.04 # hex thickness
trig_h = 0.1 # triangle walls height
p = 100

basis_wheel_t = h
basis_wheel_h = 1.7
basis_wheel_r = r
basis_wheel_p = p # wheel precision
basis_wheel_wr = 0.8 * r # wheel radius
basis_wheel_mr = 0.2 * r
basis_wheel_e = 0.005

basis_arm_e = basis_wheel_e
basis_arm_t = 0.1
basis_arm_h = basis_wheel_h
basis_arm_w = 1.2 * r
basis_arm_p = 20
basis_arm_wheel_thickness = basis_wheel_t
basis_arm_wheel_radius = basis_wheel_wr
basis_arm_middle_bar_radius = basis_wheel_mr
basis_arm_teeth_width = r
basis_arm_teeth_height = 0.25
basis_arm_teeth_thickness = 0.6 * basis_arm_t

# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
# w : hex triangle vertex index cw from center
def hex2xy(x, y, z, w):
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
        return points[(z + (w - 1)) % 6]

    return (x2, y2)

# e: epsilon, smallest change in position
# t: thickness
# h: height
# r: hex side length
# p: precision in number of parts of 1
# wr: wheel radius
# mr: middle bar radius
# hex_thickness: mirror hex thickness
# hex_walls_height : mirror hex walls height
def create_basis_wheel_mesh(e, t, h, r, p, wr, mr, hex_thickness, hex_walls_height):
    mesh = bpy.data.meshes.new('basis_wheel_mesh' + str((e,t,h,r,hex_thickness,hex_walls_height)))

    hr = 0.5 * r
    # e *= 1
    h1 = -hex_thickness - hex_walls_height - e
    h1 = -r + r * math.sin(math.pi / 3)
    zo = 0.25 * hr
    zow = 0.5 * zo
    zop = 0.5 * zow

    vertices = [
        (-e, hr - e, 0), (-hex_thickness, hr - e, 0), (-hex_thickness, -hr + e, 0), (-e, -hr + e, 0),
        (-e, hr - e, h1), (-hex_thickness, hr - e, h1), (-hex_thickness, -hr + e, h1), (-e, -hr + e, h1),
        (-e, 0, -wr),(-hex_thickness, 0, -wr), (-e, 0, h1),(-hex_thickness, 0, h1),
        (-e, hr + zo + zop, -wr + zow), (-hex_thickness, hr + zo + zop, -wr + zow), (-hex_thickness, -hr - zo - zop, -wr + zow), (-e, -hr - zo - zop, -wr + zow),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    faces = [
        (0, 1, 2, 3),
        (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha =  (0.8 * math.pi / 3) - i * ((0.8 * math.pi / 3) / p)
        vertices.append((-hex_thickness, wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        vertices.append((-e, wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        rv = nb_verts + 2 * i
        lv = nb_verts + 2 * i + 1
        print(str(vertices[rv]) + ' ' + str(vertices[lv]))

        edges.append((rv, lv))

        if i > 0:
            edges.append((rv - 2, rv))
            edges.append((lv - 2, lv))
            faces.append((rv, lv, lv - 2, rv - 2))
            faces.append((13, rv - 2, rv))
            faces.append((12, lv - 2, lv))
        else:
            edges.extend([(lv, 4), (5, rv)])
            faces.append((4, 5, rv, lv))
            faces.append((5, rv, 13))
            faces.append((4, lv, 12))
            faces.append((5, 13, 11))
            faces.append((4, 12, 10))

    nb_verts = len(vertices)
    up_rv = nb_verts - 2
    up_lv = nb_verts - 1

    for i in range(0, p + 1):
        alpha = (0.8 * math.pi) / 3 - i * ((0.8 * math.pi / 3) / p)
        vertices.append((-hex_thickness, -wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        vertices.append((-e, -wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        rv = nb_verts + 2 * i
        lv = nb_verts + 2 * i + 1
        print(str(vertices[rv]) + ' ' + str(vertices[lv]))

        edges.append((rv, lv))

        if i > 0:
            edges.append((rv - 2, rv))
            edges.append((lv - 2, lv))
            faces.append((rv, lv, lv - 2, rv - 2))
            faces.append((14, rv - 2, rv))
            faces.append((15, lv - 2, lv))
        else:
            edges.extend([(lv, 7), (6, rv)])
            faces.append((7, 6, rv, lv))
            faces.append((6, rv, 14))
            faces.append((7, lv, 15))
            faces.append((6, 14, 11))
            faces.append((7, 15, 10))

    nb_verts = len(vertices)
    down_rv = nb_verts - 2
    down_lv = nb_verts - 1

    vertices.extend([
        (-hex_thickness, hr + zo, -wr), (-e, hr + zo, -wr), (-e, -hr - zo, -wr),(-hex_thickness, -hr - zo, -wr),
        (-hex_thickness, hr - zo, -wr + zow), (-e, hr - zo, -wr + zow), (-e, -hr + zo, -wr + zow),(-hex_thickness, -hr + zo, -wr + zow),
        (-hex_thickness, hr - zo + zop, -wr), (-e, hr - zo + zop, -wr), (-e, -hr + zo - zop, -wr),(-hex_thickness, -hr + zo - zop, -wr),
        (-hex_thickness, mr, -wr),(-e, mr, -wr),(-hex_thickness, -mr, -wr), (-e, -mr, -wr),
    ])

    print(str(vertices[up_rv]) + ' ' + str(vertices[up_lv]) + ' ' + str(vertices[down_rv]) + ' ' + str(vertices[down_lv]))

    edges.extend([
        (up_rv, nb_verts), (up_lv, nb_verts + 1),
        (down_rv, nb_verts + 3), (down_lv, nb_verts + 2),
        (nb_verts, 13), (nb_verts + 1, 12), (nb_verts + 3, 14), (nb_verts + 2, 15),
        (13, nb_verts + 4), (12, nb_verts + 5), (15, nb_verts + 6), (14, nb_verts + 7),
        (13, 12), (14, 15),(nb_verts + 4, nb_verts + 5), (nb_verts + 6, nb_verts + 7),
        (nb_verts + 8, nb_verts + 9), (nb_verts + 10, nb_verts + 11),
        (nb_verts + 4, nb_verts + 8), (nb_verts + 5, nb_verts + 9), (nb_verts + 6, nb_verts + 10), (nb_verts + 7, nb_verts + 11),
        (nb_verts + 8, nb_verts + 12), (nb_verts + 9, nb_verts + 13), (nb_verts + 10, nb_verts + 15), (nb_verts + 11, nb_verts + 14),
    ])

    faces.extend([
        (up_rv, nb_verts, nb_verts + 1, up_lv),
        (down_rv, nb_verts + 3, nb_verts + 2, down_lv),
        (up_rv, 13, nb_verts), (up_lv, 12, nb_verts + 1),
        (down_rv, 14, nb_verts + 3), (down_lv, 15, nb_verts + 2),
        (nb_verts, 13, 12, nb_verts + 1), (nb_verts + 3, 14, 15, nb_verts + 2),
        (13, 12, nb_verts + 5, nb_verts + 4), (14, 15, nb_verts + 6, nb_verts + 7),
        (13, nb_verts + 4, 11), (12, nb_verts + 5, 10),(14, nb_verts + 7, 11), (15, nb_verts + 6, 10),
        (nb_verts + 4, nb_verts + 8, nb_verts + 9, nb_verts + 5), (nb_verts + 6, nb_verts + 10, nb_verts + 11, nb_verts + 7),
        (nb_verts + 8, nb_verts + 12, nb_verts + 13, nb_verts + 9), (nb_verts + 10, nb_verts + 15, nb_verts + 14, nb_verts + 11),
    ])

    nb_verts_mid = len(vertices)

    mid_v1_r = None
    mid_v1_l = None
    mid_v2_r = None
    mid_v2_l = None

    for i in range(0, p + 1):
        alpha = i * (math.pi / p)
        vertices.extend([
            (-hex_thickness, mr * math.cos(alpha), -wr + mr * math.sin(alpha)),
            (-e, mr * math.cos(alpha), -wr + mr * math.sin(alpha)),
        ])
        rv = nb_verts_mid + 2 * i
        lv = nb_verts_mid + 2 * i + 1

        edges.append((rv, lv))

        if i > 0:
            edges.extend([
                (rv - 2, rv), (lv - 2, lv),
            ])
            faces.extend([
                (rv - 2, rv, lv, lv - 2),
            ])

            if alpha < math.pi / 3:
                faces.extend([
                    (rv - 2, rv, nb_verts + 4),
                    (lv - 2, lv, nb_verts + 5),
                ])
            elif alpha < 2 * (math.pi / 3):
                faces.extend([
                    (rv - 2, rv, 11),
                    (lv - 2, lv, 10),
                ])

                if mid_v1_r == None:
                    mid_v1_r = rv - 2
                    mid_v1_l = lv - 2
            else:
                faces.extend([
                    (rv - 2, rv, nb_verts + 7),
                    (lv - 2, lv, nb_verts + 6),
                ])
                if mid_v2_r == None:
                    mid_v2_r = rv - 2
                    mid_v2_l = lv - 2

    nb_verts_mid2 = len(vertices)

    faces.extend([
        (nb_verts + 4, nb_verts_mid, nb_verts + 8),
        (nb_verts + 5, nb_verts_mid + 1, nb_verts + 9),
        (nb_verts + 6, nb_verts_mid2 - 1, nb_verts + 10),
        (nb_verts + 7, nb_verts_mid2 - 2, nb_verts + 11),
        (nb_verts + 5, mid_v1_l, 10),
        (nb_verts + 8, mid_v1_r, 11),
        (nb_verts + 6, mid_v2_l, 10),
        (nb_verts + 7, mid_v2_r, 11),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh


# e: epsilon, smallest change in position
# t: thickness
# h: height
# r: hex side length
# p: precision in number of parts of 1
# wr: wheel radius
# mr: middle bar radius
# hex_thickness: mirror hex thickness
# hex_walls_height: mirror hex walls height
def create_basis_wheel_bottom_mesh(e, t, h, r, p, wr, mr, hex_thickness, hex_walls_height):
    mesh = bpy.data.meshes.new('basis_wheel_mesh_bottom' + str((e,t,h,r,hex_thickness,hex_walls_height)))

    hr = 0.5 * r
    # e *= 1
    h1 = -hex_thickness - hex_walls_height - e
    h1 = -r + r * math.sin(math.pi / 3)
    zo = 0.25 * hr
    zow = 0.5 * zo
    zop = 0.5 * zow

    vertices = [
        (-hex_thickness, 0, -wr), (-e, 0, -wr),
        (-hex_thickness, wr, -wr), (-e, wr, -wr), (-e, -wr, -wr),(-hex_thickness, -wr, -wr),
        (-hex_thickness, hr + zo, -wr), (-e, hr + zo, -wr), (-e, -hr - zo, -wr),(-hex_thickness, -hr - zo, -wr),
        (-hex_thickness, hr + zo + zop, -wr + zow),(-e, hr + zo + zop, -wr + zow), (-e, -hr - zo - zop, -wr + zow), (-hex_thickness, -hr - zo - zop, -wr + zow),
        (-hex_thickness, hr - zo, -wr + zow), (-e, hr - zo, -wr + zow), (-e, -hr + zo, -wr + zow),(-hex_thickness, -hr + zo, -wr + zow),
        (-hex_thickness, hr - zo + zop, -wr), (-e, hr - zo + zop, -wr), (-e, -hr + zo - zop, -wr),(-hex_thickness, -hr + zo - zop, -wr),
        (-hex_thickness, 0, -1.5 * wr), (-e, 0, -1.5 * wr),
        (-hex_thickness, mr, -wr), (-e, mr, -wr), (-hex_thickness, -mr, -wr), (-e, -mr, -wr),
    ]
    edges = [
        (2, 3), (4, 5),
        (2, 6), (3, 7), (4, 8), (5, 9),
        (6, 7), (8, 9),(10, 11), (12, 13),
        (6, 10), (7, 11), (8, 12), (9, 13),
        (10, 14), (11, 15),(14, 15),
        (12, 16), (13, 17), (16, 17),
        (14, 18), (15, 19), (18, 19),
        (16, 20), (17, 21), (20, 21),
        (24, 25), (26, 27),
        (24, 18), (25, 19), (26, 21), (27, 20),
    ]
    faces = [
        (2, 3, 7, 6), (4, 5, 9, 8),
        (6, 7, 11, 10), (8, 9, 13, 12),
        (10, 14, 15, 11),
        (12, 16, 17, 13),
        (14, 18, 19, 15),
        (16, 20, 21, 17),
        (6, 10, 14, 18),
        (7, 11, 15, 19),
        (8, 12, 16, 20),
        (9, 13, 17, 21),
        (24, 25, 19, 18), (26, 27, 20, 21),
    ]

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha =  -i * (math.pi / p)
        vertices.append((-hex_thickness, wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        vertices.append((-e, wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        rv = nb_verts + 2 * i
        lv = nb_verts + 2 * i + 1
        print(str(vertices[rv]) + ' ' + str(vertices[lv]))

        edges.append((rv, lv))

        if i > 0:
            edges.append((rv - 2, rv))
            edges.append((lv - 2, lv))
            faces.append((rv, lv, lv - 2, rv - 2))
            faces.append((22, rv - 2, rv))
            faces.append((23, lv - 2, lv))
        else:
            edges.extend([(lv, 3), (2, rv)])
            faces.append((3, 2, rv, lv))

    nb_verts_mid = len(vertices)

    mid_v1_r = None
    mid_v1_l = None
    mid_v2_r = None
    mid_v2_l = None

    for i in range(0, p + 1):
        alpha = i * (math.pi / p)
        beta = math.pi + alpha
        vertices.extend([
            (-hex_thickness, mr * math.cos(beta), -wr + mr * math.sin(beta)),
            (-e, mr * math.cos(beta), -wr + mr * math.sin(beta)),
        ])
        rv = nb_verts_mid + 2 * i
        lv = nb_verts_mid + 2 * i + 1

        edges.append((rv, lv))

        if i > 0:
            edges.extend([
                (rv - 2, rv), (lv - 2, lv),
            ])
            faces.extend([
                (rv - 2, rv, lv, lv - 2),
            ])

            if alpha < math.pi / 3:
                faces.extend([
                    (rv - 2, rv, 5),
                    (lv - 2, lv, 4),
                ])
            elif alpha < 2 * (math.pi / 3):
                faces.extend([
                    (rv - 2, rv, 22),
                    (lv - 2, lv, 23),
                ])

                if mid_v1_r == None:
                    mid_v1_r = rv - 2
                    mid_v1_l = lv - 2
            else:
                faces.extend([
                    (rv - 2, rv, 2),
                    (lv - 2, lv, 3),
                ])
                if mid_v2_r == None:
                    mid_v2_r = rv - 2
                    mid_v2_l = lv - 2

    nb_verts_mid2 = len(vertices)

    faces.extend([
        (mid_v1_r, 5, 22),
        (mid_v1_l, 4, 23),
        (mid_v2_r, 2, 22),
        (mid_v2_l, 3, 23),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

# e: epsilon, smallest change in position
# t: thickness
# h: height
# w: width
# p: precision in number of parts of 1
# wheel_thickness: wheel thickness
# wheel_radius: wheel radius
# middle_bar_radius: middle bar radius
# teeth_width: bottom teeth width
# teeth_height: bottom teeth height
# teeth_thickness: bottom teeth thickness
def create_basis_arm_mesh(e, t, h, w, p, wheel_thickness, wheel_radius, middle_bar_radius, teeth_width, teeth_height, teeth_thickness):
    mesh = bpy.data.meshes.new('basis_arm_' + str((e, t, h, w, p, wheel_thickness, wheel_radius, middle_bar_radius, teeth_width, teeth_height, teeth_thickness)))

    lr = t + middle_bar_radius # large radius
    hw = 0.5 * w

    vertices = [
        (-wheel_thickness - e, 0, -wheel_radius + middle_bar_radius + t),
        (-wheel_thickness - e - t, 0, -wheel_radius + middle_bar_radius + t),
        (-wheel_thickness - e - t, 0, -wheel_radius),
        (-wheel_thickness - e, 0, -wheel_radius),
    ]
    edges = [(0, 1)]
    faces = []

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (math.pi / 2) / p
        beta = alpha

        vertices.extend([
            (-wheel_thickness - e - t, lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),
            (-wheel_thickness - e, lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),

            (-wheel_thickness - e - t, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (-wheel_thickness - e, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),

            (-wheel_thickness - e - t, -lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),
            (-wheel_thickness - e, -lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),

            (-wheel_thickness - e - t, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (-wheel_thickness - e, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),

            (e + t, lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),
            (e, lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),

            (e + t, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (e, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),

            (e + t, -lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),
            (e, -lr * math.sin(beta), -wheel_radius + lr * math.cos(beta)),

            (e + t, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (e, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
        ])

        llllv = nb_verts + 16 * i
        lllrv = nb_verts + 16 * i + 1

        llslv = nb_verts + 16 * i + 2
        llsrv = nb_verts + 16 * i + 3

        lrllv = nb_verts + 16 * i + 4
        lrlrv = nb_verts + 16 * i + 5

        lrslv = nb_verts + 16 * i + 6
        lrsrv = nb_verts + 16 * i + 7

        rlllv = nb_verts + 16 * i + 8
        rllrv = nb_verts + 16 * i + 9

        rlslv = nb_verts + 16 * i + 10
        rlsrv = nb_verts + 16 * i + 11

        rrllv = nb_verts + 16 * i + 12
        rrlrv = nb_verts + 16 * i + 13

        rrslv = nb_verts + 16 * i + 14
        rrsrv = nb_verts + 16 * i + 15

        edges.extend([
            (llllv, lllrv),
            (llslv, llsrv),

            (lrllv, lrlrv),
            (lrslv, lrsrv),

            (rlllv, rllrv),
            (rlslv, rlsrv),

            (rrllv, rrlrv),
            (rrslv, rrsrv),
        ])

        if i > 0:
            faces.extend([
                (llllv - 16, llllv, lllrv, lllrv - 16),
                (llllv - 16, llllv, llslv, llslv - 16),
                (lllrv - 16, lllrv, llsrv, llsrv - 16),
                (llslv - 16, llslv, llsrv, llsrv - 16),

                (lrllv - 16, lrllv, lrlrv, lrlrv - 16),
                (lrllv - 16, lrllv, lrslv, lrslv - 16),
                (lrlrv - 16, lrlrv, lrsrv, lrsrv - 16),
                (lrslv - 16, lrslv, lrsrv, lrsrv - 16),

                (rlllv - 16, rlllv, rllrv, rllrv - 16),
                (rlllv - 16, rlllv, rlslv, rlslv - 16),
                (rllrv - 16, rllrv, rlsrv, rlsrv - 16),
                (rlslv - 16, rlslv, rlsrv, rlsrv - 16),

                (rrllv - 16, rrllv, rrlrv, rrlrv - 16),
                (rrllv - 16, rrllv, rrslv, rrslv - 16),
                (rrlrv - 16, rrlrv, rrsrv, rrsrv - 16),
                (rrslv - 16, rrslv, rrsrv, rrsrv - 16),
            ])

    nb_verts = len(vertices)

    vertices.extend([
        (-wheel_thickness - e - t, hw, -1.5 * wheel_radius),
        (-wheel_thickness - e, hw, -1.5 * wheel_radius),

        (-wheel_thickness - e - t, -hw, -1.5 * wheel_radius),
        (-wheel_thickness - e, -hw, -1.5 * wheel_radius),

        (e + t, hw, -1.5 * wheel_radius),
        (e, hw, -1.5 * wheel_radius),

        (e + t, -hw, -1.5 * wheel_radius),
        (e, -hw, -1.5 * wheel_radius),
    ])

    edges.extend([
        (llllv, nb_verts),
        (lllrv, nb_verts + 1),

        (lrllv, nb_verts + 2),
        (lrlrv, nb_verts + 3),

        (rlllv, nb_verts + 4),
        (rllrv, nb_verts + 5),

        (rrllv, nb_verts + 6),
        (rrlrv, nb_verts + 7),
    ])

    faces.extend([
        (llllv, nb_verts, nb_verts + 1, lllrv),
        (lrllv, nb_verts + 2, nb_verts + 3, lrlrv),
        (rlllv, nb_verts + 4, nb_verts + 5, rllrv),
        (rrllv, nb_verts + 6, nb_verts + 7, rrlrv),
        (llllv, llslv, nb_verts),
        (lllrv, llsrv, nb_verts + 1),
        (lrllv, lrslv, nb_verts + 2),
        (lrlrv, lrsrv, nb_verts + 3),
        (rlllv, rlslv, nb_verts + 4),
        (rllrv, rlsrv, nb_verts + 5),
        (rrllv, rrslv, nb_verts + 6),
        (rrlrv, rrsrv, nb_verts + 7),
    ])

    nb_verts2 = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (math.pi / 2) / p
        beta = math.pi / 2 + alpha

        vertices.extend([
            (-wheel_thickness - e - t, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (-wheel_thickness - e, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),

            (-wheel_thickness - e - t, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (-wheel_thickness - e, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),

            (e + t, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (e, middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),

            (e + t, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
            (e, -middle_bar_radius * math.sin(beta), -wheel_radius + middle_bar_radius * math.cos(beta)),
        ])

        lllv = nb_verts2 + 8 * i
        llrv = lllv + 1
        lrlv = lllv + 2
        lrrv = lllv + 3
        rllv = lllv + 4
        rlrv = lllv + 5
        rrlv = lllv + 6
        rrrv = lllv + 7

        edges.extend([
            (lllv, llrv),
            (lrlv, lrrv),
            (rllv, rlrv),
            (rrlv, rrrv),
        ])

        if i > 0:
            faces.extend([
                (lllv - 8, lllv, llrv, llrv - 8),
                (lrlv - 8, lrlv, lrrv, lrrv - 8),
                (rllv - 8, rllv, rlrv, rlrv - 8),
                (rrlv - 8, rrlv, rrrv, rrrv - 8),

                (lllv - 8, lllv, nb_verts),
                (llrv - 8, llrv, nb_verts + 1),

                (lrlv - 8, lrlv, nb_verts + 2),
                (lrrv - 8, lrrv, nb_verts + 3),

                (rllv - 8, rllv, nb_verts + 4),
                (rlrv - 8, rlrv, nb_verts + 5),

                (rrlv - 8, rrlv, nb_verts + 6),
                (rrrv - 8, rrrv, nb_verts + 7),
            ])

    faces.extend([
        (nb_verts, nb_verts + 2, lllv),
        (nb_verts + 1, nb_verts + 3, llrv),
        (nb_verts + 4, nb_verts + 6, rllv),
        (nb_verts + 5, nb_verts + 7, rlrv),
    ])

    nb_verts3 = len(vertices)

    vertices.extend([
        (-wheel_thickness - e - t, hw, -2 * wheel_radius - e),
        (-wheel_thickness - e, hw, -2 * wheel_radius - e),

        (-wheel_thickness - e - t, -hw, -2 * wheel_radius - e),
        (-wheel_thickness - e, -hw, -2 * wheel_radius - e),

        (e + t, hw, -2 * wheel_radius - e),
        (e, hw, -2 * wheel_radius - e),

        (e + t, -hw, -2 * wheel_radius - e),
        (e, -hw, -2 * wheel_radius - e),
    ])

    edges.extend([
        (nb_verts, nb_verts3),
        (nb_verts + 1, nb_verts3 + 1),
        (nb_verts + 2, nb_verts3 + 2),
        (nb_verts + 3, nb_verts3 + 3),
        (nb_verts + 4, nb_verts3 + 4),
        (nb_verts + 5, nb_verts3 + 5),
        (nb_verts + 6, nb_verts3 + 6),
        (nb_verts + 7, nb_verts3 + 7),
        (nb_verts3, nb_verts3 + 1), (nb_verts3 + 1, nb_verts3 + 3),  (nb_verts3 + 3, nb_verts3 + 2), (nb_verts3 + 2, nb_verts3),
        (nb_verts3 + 5, nb_verts3 + 4), (nb_verts3 + 4, nb_verts3 + 6), (nb_verts3 + 6, nb_verts3 + 7), (nb_verts3 + 7, nb_verts3 + 5),
        (nb_verts3 + 1, nb_verts3 + 5),
        (nb_verts3 + 3, nb_verts3 + 7),
    ])

    faces.extend([
        (nb_verts, nb_verts3, nb_verts3 + 2, nb_verts + 2),
        (nb_verts + 1, nb_verts3 + 1, nb_verts3 + 3, nb_verts + 3),
        (nb_verts + 4, nb_verts3 + 4, nb_verts3 + 6, nb_verts + 6),
        (nb_verts + 5, nb_verts3 + 5, nb_verts3 + 7, nb_verts + 7),
        (nb_verts, nb_verts3, nb_verts3 + 1, nb_verts + 1),
        (nb_verts + 2, nb_verts3 + 2, nb_verts3 + 3, nb_verts + 3),
        (nb_verts + 4, nb_verts3 + 4, nb_verts3 + 5, nb_verts + 5),
        (nb_verts + 6, nb_verts3 + 6, nb_verts3 + 7, nb_verts + 7),
        (nb_verts3 + 1, nb_verts3 + 5, nb_verts3 + 7, nb_verts3 + 3),
    ])

    nb_verts4 = len(vertices)
    h1 = h - wheel_radius - e - middle_bar_radius - t - teeth_height
    print('h1: ' + str(h1))

    h2 = -2 * wheel_radius - e - h1

    h3 = h2 - teeth_height

    vertices.extend([
        (-wheel_thickness - e - t, hw, h2),
        (-wheel_thickness - e - t, -hw, h2),

        (e + t, hw, h2),
        (e + t, -hw, h2),

        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, 0.5 * teeth_width, h2),
        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, -0.5 * teeth_width, h2),

        (0.5 * teeth_thickness, 0.5 * teeth_width, h2),
        (0.5 * teeth_thickness, -0.5 * teeth_width, h2),

        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, 0.5 * teeth_width, h3),
        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, -0.5 * teeth_width, h3),

        (0.5 * teeth_thickness, 0.5 * teeth_width, h3),
        (0.5 * teeth_thickness, -0.5 * teeth_width, h3),
    ])

    edges.extend([
        (nb_verts4, nb_verts4 + 1),
        (nb_verts4 + 1, nb_verts4 + 3),
        (nb_verts4 + 3, nb_verts4 + 2),
        (nb_verts4 + 2, nb_verts4),

        (nb_verts3, nb_verts4),
        (nb_verts3 + 4, nb_verts4 + 2),
        (nb_verts3 + 6, nb_verts4 + 3),
        (nb_verts3 + 2, nb_verts4 + 1),

        (nb_verts4 + 4, nb_verts4 + 6),
        (nb_verts4 + 6, nb_verts4 + 7),
        (nb_verts4 + 7, nb_verts4 + 5),
        (nb_verts4 + 5, nb_verts4 + 4),

        (nb_verts4 + 8, nb_verts4 + 10),
        (nb_verts4 + 10, nb_verts4 + 11),
        (nb_verts4 + 11, nb_verts4 + 9),
        (nb_verts4 + 9, nb_verts4 + 8),

        (nb_verts4 + 4, nb_verts4 + 8),
        (nb_verts4 + 5, nb_verts4 + 9),
        (nb_verts4 + 6, nb_verts4 + 10),
        (nb_verts4 + 7, nb_verts4 + 11),
    ])

    faces.extend([
        (nb_verts3, nb_verts4, nb_verts4 + 1, nb_verts3 + 2),
        (nb_verts3 + 6, nb_verts4 + 3, nb_verts4 + 2, nb_verts3 + 4),

        (nb_verts3 + 2, nb_verts4 + 1, nb_verts4 + 3, nb_verts3 + 6),
        (nb_verts3, nb_verts4, nb_verts4 + 2, nb_verts3 + 4),

        (nb_verts4, nb_verts4 + 1, nb_verts4 + 5, nb_verts4 + 4),
        (nb_verts4 + 2, nb_verts4 + 3, nb_verts4 + 7, nb_verts4 + 6),

        (nb_verts4 + 1, nb_verts4 + 3, nb_verts4 + 7, nb_verts4 + 5),
        (nb_verts4, nb_verts4 + 2, nb_verts4 + 6, nb_verts4 + 4),

        (nb_verts4 + 4, nb_verts4 + 5, nb_verts4 + 9, nb_verts4 + 8),
        (nb_verts4 + 5, nb_verts4 + 7, nb_verts4 + 11, nb_verts4 + 9),
        (nb_verts4 + 7, nb_verts4 + 11, nb_verts4 + 10, nb_verts4 + 6),
        (nb_verts4 + 8, nb_verts4 + 10, nb_verts4 + 6, nb_verts4 + 4),

        (nb_verts4 + 8, nb_verts4 + 9, nb_verts4 + 11, nb_verts4 + 10),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def move_basis_to(obj, hex):
    hex_1 = hex2xy(0, 0, hex, 1)
    hex_2 = hex2xy(0, 0, hex, 2)
    hex_mid = (
        0.5 * (hex_1[0] + hex_2[0]),
        0.5 * (hex_1[1] + hex_2[1])
    )

    obj.location.x = hex_mid[0]
    obj.location.y = hex_mid[1]
    obj.location.z = h
    obj.rotation_euler = Euler((0, 0, (hex + 0.5) * (math.pi / 3)), 'XYZ')

    return

basis_collection = bpy.data.collections.new('basis_collection')
bpy.context.scene.collection.children.link(basis_collection)

hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]

basis_wheel_mesh = create_basis_wheel_mesh(
    basis_wheel_e,
    basis_wheel_t,
    basis_wheel_h,
    basis_wheel_r,
    basis_wheel_p,
    basis_wheel_wr,
    basis_wheel_mr,
    h,
    trig_h
)
basis_wheel_bottom_mesh = create_basis_wheel_bottom_mesh(
    basis_wheel_e,
    basis_wheel_t,
    basis_wheel_h,
    basis_wheel_r,
    basis_wheel_p,
    basis_wheel_wr,
    basis_wheel_mr,
    h,
    trig_h
)

basis_arm_mesh = create_basis_arm_mesh(
    basis_arm_e,
    basis_arm_t,
    basis_arm_h,
    basis_arm_w,
    basis_arm_p,
    basis_arm_wheel_thickness,
    basis_arm_wheel_radius,
    basis_arm_middle_bar_radius,
    basis_arm_teeth_width,
    basis_arm_teeth_height,
    basis_arm_teeth_thickness
)

# print('basis wheel mesh created: ' + str(basis_wheel_mesh))
basis_wheel_object_r = bpy.data.objects.new('basis_wheel_r', basis_wheel_mesh)
basis_collection.objects.link(basis_wheel_object_r)
move_basis_to(basis_wheel_object_r, 0)

basis_wheel_object_r_bottom = bpy.data.objects.new('basis_wheel_r_bottom', basis_wheel_bottom_mesh)
basis_collection.objects.link(basis_wheel_object_r_bottom)
move_basis_to(basis_wheel_object_r_bottom, 0)

basis_arm_r = bpy.data.objects.new('basis_arm_r', basis_arm_mesh)
basis_collection.objects.link(basis_arm_r)
move_basis_to(basis_arm_r, 0)

basis_wheel_object_l = bpy.data.objects.new('basis_wheel_l', basis_wheel_mesh)
basis_collection.objects.link(basis_wheel_object_l)
move_basis_to(basis_wheel_object_l, 3)

basis_wheel_object_l_bottom = bpy.data.objects.new('basis_wheel_l_bottom', basis_wheel_bottom_mesh)
basis_collection.objects.link(basis_wheel_object_l_bottom)
move_basis_to(basis_wheel_object_l_bottom, 3)

basis_arm_l = bpy.data.objects.new('basis_arm_l', basis_arm_mesh)
basis_collection.objects.link(basis_arm_l)
move_basis_to(basis_arm_l, 3)

print('done')
# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\basis_", check_existing=True, filter_glob='*.stl', use_selection=False, global_scale=100.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z')