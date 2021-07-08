import os
import sys
import bpy
import math
from mathutils import Euler

sys.dont_write_bytecode = 1
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from hyperparameters import r, h, p, e, trig_h
from optics import hex2xy

basis_wheel_e = e
basis_wheel_t = h
basis_wheel_h = 1.7
basis_wheel_r = r
basis_wheel_p = p # wheel precision
basis_wheel_wr = 0.8 * r # wheel radius
basis_wheel_mr = 0.2 * r
basis_wheel_kr = 0.25 * r
basis_wheel_kw = basis_wheel_t

basis_arm_e = basis_wheel_e
basis_arm_t = 0.1
basis_arm_h = basis_wheel_h
basis_arm_w = 1.2 * r
basis_arm_p = 20
basis_arm_wheel_thickness = basis_wheel_t
basis_arm_wheel_radius = basis_wheel_wr
basis_arm_middle_bar_radius = basis_wheel_mr
basis_arm_teeth_width = r
basis_arm_teeth_height = 0.2
basis_arm_teeth_thickness = 0.8 * basis_arm_t

basis_leg_e = basis_arm_e
basis_leg_t = 2 * basis_arm_t + basis_arm_wheel_thickness + 2 * basis_arm_e
basis_leg_h = basis_arm_h
basis_leg_w = basis_arm_w
basis_leg_x = -0.5 * basis_arm_wheel_thickness
basis_leg_z = -basis_arm_wheel_radius - basis_arm_h + basis_arm_middle_bar_radius + basis_arm_t
basis_leg_teeth_width = basis_arm_teeth_width
basis_leg_teeth_height = basis_arm_teeth_height
basis_leg_teeth_thickness = basis_arm_teeth_thickness
basis_leg_side_teeth_width = 0.1
basis_leg_side_teeth_height = 0.15
basis_leg_side_teeth_thickness = 0.6 * basis_leg_t
basis_leg_side_teeth_z = 0.5 * (2 * 0.04 + basis_leg_side_teeth_width)

basis_foot_e = basis_leg_e
basis_foot_t = basis_leg_t
basis_foot_h = 2 * basis_leg_side_teeth_z
basis_foot_w1 = 0.1
basis_foot_w2 = 0.4 * basis_leg_w
basis_foot_x = basis_leg_x
basis_foot_y = -0.5 * basis_leg_w
basis_foot_z = basis_leg_z - basis_leg_e - basis_leg_h + 0.5 * basis_foot_h + basis_leg_teeth_height
basis_foot_horizontal_tooth_width = basis_leg_side_teeth_width
basis_foot_horizontal_tooth_height = basis_leg_side_teeth_height
basis_foot_horizontal_tooth_thickness = basis_leg_side_teeth_thickness
basis_foot_vertical_tooth_width = 0.5 * basis_foot_w2
basis_foot_vertical_tooth_height = 0.6 * basis_leg_teeth_height
basis_foot_vertical_tooth_thickness = 1.5 * basis_leg_teeth_thickness

basis_plate_top_e = basis_foot_e
basis_plate_top_t = basis_leg_teeth_height
basis_plate_top_r = 1.1 * r
basis_plate_top_sr = basis_arm_middle_bar_radius
basis_plate_top_p = 50
basis_plate_top_x = basis_foot_x
basis_plate_top_z = basis_foot_z - 0.5 * basis_foot_h
basis_plate_top_hex_side = r
basis_plate_top_large_tooth_width = basis_leg_teeth_width
basis_plate_top_large_tooth_height = basis_leg_teeth_height
basis_plate_top_large_tooth_thickness = basis_leg_teeth_thickness
basis_plate_top_small_teeth_width = basis_foot_vertical_tooth_width
basis_plate_top_small_teeth_height = basis_foot_vertical_tooth_height
basis_plate_top_small_teeth_thickness = basis_foot_vertical_tooth_thickness
basis_plate_top_leg_width = basis_leg_w
basis_plate_top_foot_w1 = basis_foot_w1
basis_plate_top_foot_w2 = basis_foot_w2
basis_plate_top_foot_thickness = basis_foot_t

basis_plate_axis_e = basis_plate_top_e
basis_plate_axis_t = h
basis_plate_axis_r = 0.5 * r
basis_plate_axis_p = basis_plate_top_p
basis_plate_axis_x = basis_plate_top_x - (math.sqrt(3) / 2) * r + 0.5 * h
basis_plate_axis_z = basis_plate_top_z - basis_plate_top_t - basis_plate_axis_e
basis_plate_axis_top_t = basis_plate_top_t
basis_plate_axis_top_r = basis_plate_top_sr
basis_plate_axis_bottom_t = basis_plate_top_t
basis_plate_axis_bottom_r = basis_plate_top_sr

basis_plate_bottom_e = basis_plate_top_e
basis_plate_bottom_t = basis_plate_axis_bottom_t
basis_plate_bottom_r = basis_plate_top_r
basis_plate_bottom_sr = basis_plate_axis_bottom_r
basis_plate_bottom_p = basis_plate_top_p
basis_plate_bottom_x = basis_plate_top_x
basis_plate_bottom_z = basis_plate_axis_z - basis_plate_axis_t - basis_plate_bottom_e
basis_plate_bottom_hex_side = basis_plate_top_hex_side
basis_plate_bottom_top_plate_thickness = basis_plate_top_t

# e: epsilon, smallest change in position
# t: thickness
# h: height
# r: hex side length
# p: precision in number of parts of 1
# wr: wheel radius
# mr: middle bar radius
# kr: key radius
# kw: key width
# hex_thickness: mirror hex thickness
# hex_walls_height : mirror hex walls height
def create_basis_wheel_mesh(e, t, h, r, p, wr, mr, kr, kw, hex_thickness, hex_walls_height):
    mesh = bpy.data.meshes.new('basis_wheel_mesh' + str((e,t,h,r,hex_thickness,hex_walls_height)))

    pi3 = math.pi / 3

    hr = 0.5 * r
    h1 = -hex_thickness - hex_walls_height - e
    h1 = -r + r * math.sin(math.pi / 3)
    zo = 0.25 * hr
    zow = 0.5 * zo
    zop = 0.5 * zow
    hkw = 0.5 * kw

    vertices = [
        (-e, hr - e, 0),
        (-hex_thickness, hr - e, 0),
        (-hex_thickness, -hr + e, 0),
        (-e, -hr + e, 0),

        (-hex_thickness, hr - e, -hex_thickness - e),
        (-2 * hex_thickness - e, hr - e, -hex_thickness - e),
        (-2 * hex_thickness - e, -hr + e, -hex_thickness - e),
        (-hex_thickness, -hr + e, -hex_thickness - e),

        (-hex_thickness, hr - e, -2 * hex_thickness - e),
        (-2 * hex_thickness - e, hr - e, -2 * hex_thickness - e),
        (-2 * hex_thickness - e, -hr + e, -2 * hex_thickness - e),
        (-hex_thickness, -hr + e, -2 * hex_thickness - e),

        (-e, hr - e, h1),
        (-hex_thickness, hr - e, h1),
        (-hex_thickness, -hr + e, h1),
        (-e, -hr + e, h1),

        (-e, 0, -wr),
        (-hex_thickness, 0, -wr),
        (-e, 0, h1),
        (-hex_thickness, 0, h1),

        (-e, hr + zo + zop, -wr + zow),
        (-hex_thickness, hr + zo + zop, -wr + zow),
        (-hex_thickness, -hr - zo - zop, -wr + zow),
        (-e, -hr - zo - zop, -wr + zow),
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (8, 9), (9, 10), (10, 11), (11, 8),
        (4, 8), (5, 9), (6, 10), (7, 11),

        (12, 13), (13, 14), (14, 15), (15, 12),
        (0, 12),
        (1, 4), (4, 8), (8, 13),
        (2, 7), (7, 11), (11, 14),
        (3, 15),
    ]
    faces = [
        (0, 1, 2, 3),

        (4, 5, 6, 7),
        (9, 8, 11, 10),
        (2, 1, 4, 7),
        (11, 8, 13, 14),

        (6, 5, 9, 10),
        (5, 4, 8, 9),
        (7, 6, 10, 11),

        (1, 0, 12, 13),
        (3, 2, 14, 15),
        (0, 3, 15, 12),
    ]

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (-0.8 * pi3) / p
        beta = 0.8 * pi3 + alpha

        vertices.extend([
            (-hex_thickness, wr * math.cos(beta), -wr + wr * math.sin(beta)),
            (-e, wr * math.cos(beta), -wr + wr * math.sin(beta)),
        ])

        rv = nb_verts + 2 * i
        lv = nb_verts + 2 * i + 1

        edges.append((rv, lv))

        if i > 0:
            edges.extend([
                (rv - 2, rv),
                (lv - 2, lv),
            ])

            faces.extend([
                (rv, rv - 2, lv - 2, lv),
                (21, rv - 2, rv),
                (20, lv, lv - 2)
            ])
        else:
            edges.extend([
                (lv, 12),
                (13, rv)
            ])

            faces.extend([
                (13, 12, lv, rv),
                (13, rv, 21),
                (20, lv, 12),
                (13, 21, 19),
                (18, 20, 12),
            ])

    nb_verts = len(vertices)
    up_rv = nb_verts - 2
    up_lv = nb_verts - 1

    for i in range(0, p + 1):
        alpha = i * (-0.8 * pi3) / p
        beta = 0.8 * pi3 + alpha

        vertices.extend([
            (-hex_thickness, -wr * math.cos(beta), -wr + wr * math.sin(beta)),
            (-e, -wr * math.cos(beta), -wr + wr * math.sin(beta))
        ])

        rv = nb_verts + 2 * i
        lv = nb_verts + 2 * i + 1

        edges.append((rv, lv))

        if i > 0:
            edges.extend([
                (lv, lv - 2),
                (rv - 2, rv),
            ])

            faces.extend([
                (rv - 2, rv, lv, lv - 2),
                (22, rv, rv - 2),
                (23, lv - 2, lv),
            ])
        else:
            edges.extend([
                (lv, 15),
                (14, rv)
            ])

            faces.extend([
                (15, 14, rv, lv),
                (22, rv, 14),
                (15, lv, 23),
                (14, 19, 22),
                (15, 23, 18),
            ])

    nb_verts = len(vertices)
    down_rv = nb_verts - 2
    down_lv = nb_verts - 1

    vertices.extend([
        (-hex_thickness, hr + zo, -wr),
        (-e, hr + zo, -wr),
        (-e, -hr - zo, -wr),
        (-hex_thickness, -hr - zo, -wr),

        (-hex_thickness, hr - zo, -wr + zow),
        (-e, hr - zo, -wr + zow),
        (-e, -hr + zo, -wr + zow),
        (-hex_thickness, -hr + zo, -wr + zow),

        (-hex_thickness, hr - zo + zop, -wr),
        (-e, hr - zo + zop, -wr),
        (-e, -hr + zo - zop, -wr),
        (-hex_thickness, -hr + zo - zop, -wr),

        (-hex_thickness, mr, -wr),
        (-e, mr, -wr),
        (-hex_thickness, -mr, -wr),
        (-e, -mr, -wr),
    ])

    #print(str(vertices[up_rv]) + ' ' + str(vertices[up_lv]) + ' ' + str(vertices[down_rv]) + ' ' + str(vertices[down_lv]))

    edges.extend([
        (up_rv, nb_verts),
        (up_lv, nb_verts + 1),

        (down_rv, nb_verts + 3),
        (down_lv, nb_verts + 2),

        (nb_verts, 21),
        (nb_verts + 1, 20),
        (nb_verts + 3, 22),
        (nb_verts + 2, 23),

        (21, nb_verts + 4),
        (20, nb_verts + 5),
        (23, nb_verts + 6),
        (22, nb_verts + 7),

        (21, 20),
        (22, 23),
        (nb_verts + 4, nb_verts + 5),
        (nb_verts + 6, nb_verts + 7),

        (nb_verts + 8, nb_verts + 9),
        (nb_verts + 10, nb_verts + 11),

        (nb_verts + 4, nb_verts + 8),
        (nb_verts + 5, nb_verts + 9),
        (nb_verts + 6, nb_verts + 10),
        (nb_verts + 7, nb_verts + 11),

        (nb_verts + 8, nb_verts + 12),
        (nb_verts + 9, nb_verts + 13),
        (nb_verts + 10, nb_verts + 15),
        (nb_verts + 11, nb_verts + 14),
    ])

    faces.extend([
        (up_rv, up_lv, nb_verts + 1, nb_verts),
        (down_rv, nb_verts + 3, nb_verts + 2, down_lv),

        (up_rv, nb_verts, 21),
        (up_lv, 20, nb_verts + 1),

        (down_rv, 22, nb_verts + 3),
        (down_lv, nb_verts + 2, 23),

        (21, nb_verts, nb_verts + 1, 20),
        (nb_verts + 3, 22, 23, nb_verts + 2),

        (21, 20, nb_verts + 5, nb_verts + 4),
        (23, 22, nb_verts + 7, nb_verts + 6),

        (21, nb_verts + 4, 19),
        (18, nb_verts + 5, 20),
        (19, nb_verts + 7, 22),
        (23, nb_verts + 6, 18),

        (nb_verts + 4, nb_verts + 5, nb_verts + 9, nb_verts + 8),
        (nb_verts + 6, nb_verts + 7, nb_verts + 11, nb_verts + 10),

        (nb_verts + 8, nb_verts + 9, nb_verts + 13, nb_verts + 12),
        (nb_verts + 10, nb_verts + 11, nb_verts + 14, nb_verts + 15),
    ])

    nb_verts_mid = len(vertices)

    mid_v1_r = None
    mid_v1_l = None
    mid_v2_r = None
    mid_v2_l = None
    ktrv = None
    ktlv = None
    kbrv = None
    kblv = None

    for i in range(0, p + 1):
        alpha = i * (math.pi / p)
        beta = 0 + alpha

        vertices.extend([
            (-hex_thickness, mr * math.cos(beta), -wr + mr * math.sin(beta)),
            (-e, mr * math.cos(beta), -wr + mr * math.sin(beta)),
        ])

        nbidx = 2
        rv = nb_verts_mid + nbidx * i
        lv = nb_verts_mid + nbidx * i + 1

        lateral_face = True

        if i > 0:
            if alpha < pi3:
                faces.extend([
                    (rv - nbidx, rv, nb_verts + 4),
                    (lv, lv - nbidx, nb_verts + 5),
                ])
            elif alpha < 2 * pi3:
                if abs(vertices[rv][1]) > hkw:
                    if ktrv == None and kbrv != None:
                        ktrv = rv
                        ktlv = lv
                    else:
                        faces.extend([
                            (rv - nbidx, rv, 19),
                            (lv, lv - nbidx, 18),
                        ])

                else:
                    lateral_face = False
                    if vertices[rv][1] > 0:
                        if kbrv == None:
                            kbrv = rv - nbidx
                            kblv = lv - nbidx

                if mid_v1_r == None:
                    mid_v1_r = rv - nbidx
                    mid_v1_l = lv - nbidx
            else:
                faces.extend([
                    (rv - nbidx, rv, nb_verts + 7),
                    (lv, lv - nbidx, nb_verts + 6),
                ])

                if mid_v2_r == None:
                    mid_v2_r = rv - nbidx
                    mid_v2_l = lv - nbidx

        if lateral_face and (ktrv == None or rv != ktrv):
            edges.append((rv, lv))

            if i > 0:
                edges.extend([
                    (rv - nbidx, rv), (lv - nbidx, lv),
                ])

                faces.extend([
                    (rv, rv - nbidx, lv - nbidx, lv),
                ])


    nb_verts_mid2 = len(vertices)

    vertices.extend([
        (-hex_thickness, hkw, -wr + mr),
        (-e, hkw, -wr + mr),
        (-e, -hkw, -wr + mr),
        (-hex_thickness, -hkw, -wr + mr),

        (-hex_thickness, hkw, -wr + kr),
        (-e, hkw, -wr + kr),
        (-e, -hkw, -wr + kr),
        (-hex_thickness, -hkw, -wr + kr),
    ])

    faces.extend([
        (nb_verts + 4, nb_verts + 8, nb_verts_mid),
        (nb_verts + 5, nb_verts_mid + 1, nb_verts + 9),
        (nb_verts + 6, nb_verts + 10, nb_verts_mid2 - 1),
        (nb_verts + 7, nb_verts_mid2 - 2, nb_verts + 11),

        (mid_v1_l, nb_verts + 5, 18),
        (nb_verts + 6, mid_v2_l, 18),
        (nb_verts + 4, mid_v1_r, 19),
        (mid_v2_r, nb_verts + 7, 19),

        (kbrv, kblv, nb_verts_mid2 + 1, nb_verts_mid2),
        (ktlv, ktrv, nb_verts_mid2 + 3, nb_verts_mid2 + 2),
        (nb_verts_mid2, nb_verts_mid2 + 1, nb_verts_mid2 + 5, nb_verts_mid2 + 4),
        (nb_verts_mid2 + 4, nb_verts_mid2 + 5, nb_verts_mid2 + 6, nb_verts_mid2 + 7),
        (nb_verts_mid2 + 3, nb_verts_mid2 + 7, nb_verts_mid2 + 6, nb_verts_mid2 + 2),

        (ktrv, nb_verts_mid2 + 7, nb_verts_mid2 + 3),
        (ktrv, 19, nb_verts_mid2 + 7),

        (kbrv, nb_verts_mid2, nb_verts_mid2 + 4),
        (kbrv, nb_verts_mid2 + 4, 19),

        (ktlv, nb_verts_mid2 + 2, nb_verts_mid2 + 6),
        (ktlv, nb_verts_mid2 + 6, 18),

        (kblv, nb_verts_mid2 + 5, nb_verts_mid2 + 1),
        (kblv, 18, nb_verts_mid2 + 5),

        (nb_verts_mid2 + 7, 19, nb_verts_mid2 + 4),
        (nb_verts_mid2 + 5, 18, nb_verts_mid2 + 6),
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
# kr: key radius
# kw: key width
# hex_thickness: mirror hex thickness
# hex_walls_height: mirror hex walls height
def create_basis_wheel_bottom_mesh(e, t, h, r, p, wr, mr, kr, kw, hex_thickness, hex_walls_height):
    mesh = bpy.data.meshes.new('basis_wheel_mesh_bottom' + str((
        e, t, h, r, p, wr, mr, kr, kw,
        hex_thickness, hex_walls_height
    )))

    pi3 = math.pi / 3

    hr = 0.5 * r
    h1 = -hex_thickness - hex_walls_height - e
    h1 = -r + r * math.sin(pi3)
    zo = 0.25 * hr
    zow = 0.5 * zo
    zop = 0.5 * zow
    hkw = 0.5 * kw

    vertices = [
        (-hex_thickness, 0, -wr),
        (-e, 0, -wr),

        (-hex_thickness, wr, -wr),
        (-e, wr, -wr),
        (-e, -wr, -wr),
        (-hex_thickness, -wr, -wr),

        (-hex_thickness, hr + zo - e, -wr),
        (-e, hr + zo - e, -wr),
        (-e, -hr - zo + e, -wr),
        (-hex_thickness, -hr - zo + e, -wr),

        (-hex_thickness, hr + zo + zop - e, -wr + zow - e),
        (-e, hr + zo + zop - e, -wr + zow - e),
        (-e, -hr - zo - zop + e, -wr + zow - e),
        (-hex_thickness, -hr - zo - zop + e, -wr + zow - e),

        (-hex_thickness, hr - zo + e, -wr + zow - e),
        (-e, hr - zo + e, -wr + zow - e),
        (-e, -hr + zo - e, -wr + zow - e),
        (-hex_thickness, -hr + zo - e, -wr + zow - e),

        (-hex_thickness, hr - zo + zop + e, -wr),
        (-e, hr - zo + zop + e, -wr),
        (-e, -hr + zo - zop - e, -wr),
        (-hex_thickness, -hr + zo - zop - e, -wr),

        (-hex_thickness, 0, -1.5 * wr),
        (-e, 0, -1.5 * wr),

        (-hex_thickness, mr, -wr),
        (-e, mr, -wr),
        (-hex_thickness, -mr, -wr),
        (-e, -mr, -wr),
    ]

    edges = [
        (2, 3),
        (4, 5),

        (2, 6),
        (3, 7),
        (4, 8),
        (5, 9),

        (6, 7),
        (8, 9),
        (10, 11),
        (12, 13),

        (6, 10),
        (7, 11),
        (8, 12),
        (9, 13),

        (10, 14),
        (11, 15),
        (14, 15),

        (12, 16),
        (13, 17),
        (16, 17),

        (14, 18),
        (15, 19),
        (18, 19),

        (16, 20),
        (17, 21),
        (20, 21),

        (24, 25),
        (26, 27),

        (24, 18),
        (25, 19),
        (26, 21),
        (27, 20),
    ]
    faces = [
        (3, 2, 6, 7),
        (5, 4, 8, 9),

        (7, 6, 10, 11),
        (9, 8, 12, 13),

        (10, 14, 15, 11),
        (12, 16, 17, 13),
        (14, 18, 19, 15),
        (16, 20, 21, 17),

        (10, 6, 18, 14),
        (7, 11, 15, 19),
        (12, 8, 20, 16),
        (9, 13, 17, 21),

        (24, 25, 19, 18),
        (27, 26, 21, 20),
    ]

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha =  -i * (math.pi / p)

        vertices.extend([
            (-hex_thickness, wr * math.cos(alpha), -wr + wr * math.sin(alpha)),
            (-e, wr * math.cos(alpha), -wr + wr * math.sin(alpha)),
        ])

        nbidx = 2
        rv = nb_verts + nbidx * i
        lv = nb_verts + nbidx * i + 1

        edges.append((rv, lv))

        if i > 0:
            edges.extend([
                (rv - nbidx, rv),
                (lv - nbidx, lv),
            ])

            faces.extend([
                (lv - nbidx, lv, rv, rv - nbidx),
                (22, rv - nbidx, rv),
                (lv, lv - nbidx, 23),
            ])
        else:
            edges.extend([
                (lv, 3),
                (2, rv)
            ])

            faces.append((3, 2, rv, lv))

    nb_verts_mid = len(vertices)

    mid_v1_r = None
    mid_v1_l = None
    mid_v2_r = None
    mid_v2_l = None

    ktrv = None
    ktlv = None
    kbrv = None
    kblv = None

    for i in range(0, p + 1):
        alpha = i * (math.pi / p)
        beta = math.pi + alpha

        vertices.extend([
            (-hex_thickness, mr * math.cos(beta), -wr + mr * math.sin(beta)),
            (-e, mr * math.cos(beta), -wr + mr * math.sin(beta)),
        ])

        nbidx = 2
        rv = nb_verts_mid + nbidx * i
        lv = nb_verts_mid + nbidx * i + 1

        lateral_face = True

        if i > 0:
            if alpha < pi3:
                faces.extend([
                    (rv - nbidx, rv, 5),
                    (lv, lv - nbidx, 4),
                ])
            elif alpha < 2 * pi3:
                if abs(vertices[rv][1]) > hkw:
                    if kbrv == None and ktrv != None:
                        kbrv = rv
                        kblv = lv
                    else:
                        faces.extend([
                            (rv - nbidx, rv, 22),
                            (lv, lv - nbidx, 23),
                        ])

                else:
                    lateral_face = False
                    if vertices[rv][1] < 0:
                        print('rvy: ' + str(vertices[rv][1]) + ' hkw:' + str(hkw))
                        if ktrv == None:
                            ktrv = rv - nbidx
                            ktlv = lv - nbidx

                if mid_v1_r == None:
                    mid_v1_r = rv - nbidx
                    mid_v1_l = lv - nbidx
            else:
                faces.extend([
                    (rv - nbidx, rv, 2),
                    (lv, lv - nbidx, 3),
                ])

                if mid_v2_r == None:
                    mid_v2_r = rv - 2
                    mid_v2_l = lv - 2

        if lateral_face and (kbrv == None or rv != kbrv):
            edges.append((rv, lv))

            if i > 0:
                edges.extend([
                    (rv - nbidx, rv), (lv - nbidx, lv),
                ])

                faces.extend([
                    (rv, rv - nbidx, lv - nbidx, lv),
                ])

    nb_verts_mid2 = len(vertices)

    vertices.extend([
        (-hex_thickness, hkw, -wr -mr),
        (-e, hkw, -wr - mr),
        (-e, -hkw, -wr - mr),
        (-hex_thickness, -hkw, -wr - mr),

        (-hex_thickness, hkw, -wr - kr),
        (-e, hkw, -wr - kr),
        (-e, -hkw, -wr - kr),
        (-hex_thickness, -hkw, -wr - kr),
    ])

    faces.extend([
        (mid_v1_r, 22, 5),
        (mid_v1_l, 4, 23),
        (mid_v2_r, 2, 22),
        (mid_v2_l, 23, 3),

        (kblv, kbrv, nb_verts_mid2, nb_verts_mid2 + 1),
        (ktrv, ktlv, nb_verts_mid2 + 2, nb_verts_mid2 + 3),
        (nb_verts_mid2 + 1, nb_verts_mid2, nb_verts_mid2 + 4, nb_verts_mid2 + 5),
        (nb_verts_mid2 + 5, nb_verts_mid2 + 4, nb_verts_mid2 + 7, nb_verts_mid2 + 6),
        (nb_verts_mid2 + 7, nb_verts_mid2 + 3, nb_verts_mid2 + 2, nb_verts_mid2 + 6),

        (ktrv, nb_verts_mid2 + 3, nb_verts_mid2 + 7),
        (ktrv, 22, nb_verts_mid2 + 7),

        (kbrv, nb_verts_mid2 + 4, nb_verts_mid2),
        (kbrv, nb_verts_mid2 + 4, 22),

        (ktlv, nb_verts_mid2 + 6, nb_verts_mid2 + 2),
        (ktlv, nb_verts_mid2 + 6, 23),

        (kblv, nb_verts_mid2 + 1, nb_verts_mid2 + 5),
        (kblv, 23, nb_verts_mid2 + 5),

        (nb_verts_mid2 + 4, 22, nb_verts_mid2 + 7),
        (nb_verts_mid2 + 6, 23, nb_verts_mid2 + 5),
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

    h2 = -2 * wheel_radius - e - h1

    h3 = h2 - teeth_height

    vertices.extend([
        (-wheel_thickness - e - t, hw, h2),
        (-wheel_thickness - e - t, -hw, h2),

        (e + t, hw, h2),
        (e + t, -hw, h2),

        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, 0.5 * teeth_width, h2),
        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, -0.5 * teeth_width, h2),

        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, 0.5 * teeth_width, h2),
        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, -0.5 * teeth_width, h2),

        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, 0.5 * teeth_width, h3),
        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, -0.5 * teeth_width, h3),

        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, 0.5 * teeth_width, h3),
        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, -0.5 * teeth_width, h3),
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

def create_basis_leg_mesh(e, t, h, w, x, z, teeth_width, teeth_height, teeth_thickness, side_teeth_width, side_teeth_height, side_teeth_thickness, side_teeth_z):
    mesh = bpy.data.meshes.new('basis_leg_' + str((e, t, h, w, x, z, teeth_width, teeth_height, teeth_thickness, side_teeth_width, side_teeth_height, side_teeth_thickness, side_teeth_z)))

    hw = 0.5 * w
    ht = 0.5 * t
    htt = 0.5 * teeth_thickness
    htw = 0.5 * teeth_width
    hstt = 0.5 * side_teeth_thickness
    hstw = 0.5 * side_teeth_width

    sth = z - e - h + teeth_height + side_teeth_z # total side teeth z

    vertices = [
        (x - ht - e, hw + e, z + teeth_height - e),
        (x - ht - e, -hw - e, z + teeth_height - e),
        (x + ht + e, hw + e, z + teeth_height - e),
        (x + ht + e, -hw - e, z + teeth_height - e),

        (x - htt - e, htw + e, z + teeth_height - e),
        (x - htt - e, -htw - e, z + teeth_height - e),
        (x + htt + e, htw + e, z + teeth_height - e),
        (x + htt + e, -htw - e, z + teeth_height - e),

        # 8
        (x - ht - e, hw + e, z - e),
        (x - ht - e, -hw - e, z - e),
        (x + ht + e, hw + e, z - e),
        (x + ht + e, -hw - e, z - e),

        (x - htt - e, htw + e, z - e),
        (x - htt - e, -htw - e, z - e),
        (x + htt + e, htw + e, z - e),
        (x + htt + e, -htw - e, z - e),

        # 16
        (x - ht, hw, z - e - h + teeth_height),
        (x - ht, -hw, z - e - h + teeth_height),
        (x + ht, hw, z - e - h + teeth_height),
        (x + ht, -hw, z - e - h + teeth_height),

        (x - htt, htw, z - e - h + teeth_height),
        (x - htt, -htw, z - e - h + teeth_height),
        (x + htt, htw, z - e - h + teeth_height),
        (x + htt, -htw, z - e - h + teeth_height),

        # 24
        (x - htt, htw, z - e - h),
        (x - htt, -htw, z - e - h),
        (x + htt, htw, z - e - h),
        (x + htt, -htw, z - e - h),

        (x - hstt, hw, sth + hstw),
        (x - hstt, -hw, sth + hstw),
        (x + hstt, hw, sth + hstw),
        (x + hstt, -hw, sth + hstw),

        # 32
        (x - hstt, hw, sth - hstw),
        (x - hstt, -hw, sth - hstw),
        (x + hstt, hw, sth - hstw),
        (x + hstt, -hw, sth - hstw),

        (x - hstt, hw - side_teeth_height, sth + hstw),
        (x - hstt, -hw + side_teeth_height, sth + hstw),
        (x + hstt, hw - side_teeth_height, sth + hstw),
        (x + hstt, -hw + side_teeth_height, sth + hstw),

        #40
        (x - hstt, hw - side_teeth_height, sth - hstw),
        (x - hstt, -hw + side_teeth_height, sth - hstw),
        (x + hstt, hw - side_teeth_height, sth - hstw),
        (x + hstt, -hw + side_teeth_height, sth - hstw),
    ]
    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),
        (4, 5), (5, 7), (7, 6), (6, 4),
        (8, 9), (9, 11), (11, 10), (10, 8),
        (12, 13), (13, 15), (15, 14), (14, 12),
        (4, 12),(5, 13), (6, 14), (7, 15),
        (0, 8), (1, 9), (2, 10), (3, 11),
        (16, 17), (17, 19), (19, 18), (18, 16),
        (8, 16), (9, 17), (10, 18), (11, 19),
        (20, 21), (21, 23), (23, 22), (22, 20),
        (24, 25), (25, 27), (27, 26), (26, 24),
        (20, 24), (21, 25), (22, 26), (23, 27),

        (28, 30), (30, 34), (34, 32), (32, 28),
        (36, 38), (38, 42), (42, 40), (40, 36),
        (28, 36), (30, 38), (32, 40), (34, 42),

        (29, 31), (31, 35), (35, 33), (33, 29),
        (37, 39), (39, 43), (43, 41), (41, 37),
        (29, 37), (31, 39), (33, 41), (35, 43),
    ]
    faces = [
        (0, 1, 5, 4),
        (1, 3, 7, 5),
        (3, 2, 6, 7),
        (2, 0, 4, 6),

        (12, 13, 15, 14),

        (12, 4, 5, 13),
        (6, 14, 15, 7),
        (4, 12, 14, 6),
        (7, 15, 13, 5),

        (1, 0, 8, 9),
        (3, 1, 9, 11),
        (2, 3, 11, 10),
        (0, 2, 10, 8),

        (8, 16, 17, 9),
        (18, 10, 11, 19),

        (16, 20, 21, 17),
        (22, 18, 19, 23),
        (20, 16, 18, 22),
        (17, 21, 23, 19),

        (20, 24, 25, 21),
        (26, 22, 23, 27),
        (24, 20, 22, 26),
        (21, 25, 27, 23),

        (25, 24, 26, 27),

        (36, 38, 42, 40),
        (38, 36, 28, 30),
        (40, 42, 34, 32),
        (36, 40, 32, 28),
        (42, 38, 30, 34),

        (39, 37, 41, 43),
        (37, 39, 31, 29),
        (43, 41, 33, 35),
        (41, 37, 29, 33),
        (39, 43, 35, 31),

        (8, 10, 30, 28),
        (32, 34, 18, 16),
        (8, 28, 32, 16),
        (30, 10, 18, 34),

        (11, 9, 29, 31),
        (35, 33, 17, 19),
        (29, 9, 17, 33),
        (11, 31, 35, 19),
    ]

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def create_foot_mesh(e, t, h, w1, w2, x, y, z, horizontal_tooth_width, horizontal_tooth_height, horizontal_tooth_thickness, vertical_tooth_width, vertical_tooth_height, vertical_tooth_thickness, yscale):
    mesh = bpy.data.meshes.new('basis_foot_' + str((e, t, h, w1, w2, x, y, z, horizontal_tooth_width, horizontal_tooth_height, horizontal_tooth_thickness, vertical_tooth_width, vertical_tooth_height, vertical_tooth_thickness, yscale)))

    ht = 0.5 * t
    hh = 0.5 * h
    hhtw = 0.5 * horizontal_tooth_width
    hhtt = 0.5 * horizontal_tooth_thickness
    hvtw = 0.5 * vertical_tooth_width
    hvtt = 0.5 * vertical_tooth_thickness

    pi3 = math.pi / 3
    pi6 = math.pi / 6
    cpi3 = math.cos(pi3)
    spi3 = math.sin(pi3)
    cpi6 = math.cos(pi6)
    spi6 = math.sin(pi6)

    w3 = spi3 * t
    h1 = spi6 * w3

    h2 = spi3 * w2
    w4 = cpi3 * w2

    h3 = 0.5 * (w2 - vertical_tooth_width) * cpi6
    w5 = 0.5 * (w2 - vertical_tooth_width) * spi6

    p1 = (x - ht, yscale * (y - e - w1), z + hh)
    p2 = (x + ht, yscale * (y - e - w1), z + hh)

    p3 = (p1[0] - h2, p1[1] - yscale * w4, z)
    p4 = (p2[0] - h2, p2[1] - yscale * w4, z)

    p5 = (x - (ht - hvtt) - hvtt - h3, yscale * (y - e - w1 - w5), z - hh)
    p6 = (x - (ht - hvtt) + hvtt - h3, yscale * (y - e - w1 - w5), z - hh)

    p7 = (p5[0] - vertical_tooth_width * cpi6, p5[1] - yscale * vertical_tooth_width * spi6, p5[2])
    p8 = (p6[0] - vertical_tooth_width * cpi6, p6[1] - yscale * vertical_tooth_width * spi6, p6[2])

    vertices = [
        (x - hhtt + e, yscale * (y - e + horizontal_tooth_height), z + hhtw - e),
        (x + hhtt - e, yscale * (y - e + horizontal_tooth_height), z + hhtw - e),

        (x - hhtt + e, yscale * (y - e + horizontal_tooth_height), z - hhtw + e),
        (x + hhtt - e, yscale * (y - e + horizontal_tooth_height), z - hhtw + e),

        (x - hhtt + e, yscale * (y - e), z + hhtw - e),
        (x + hhtt - e, yscale * (y - e), z + hhtw - e),

        (x - hhtt + e, yscale * (y - e), z - hhtw + e),
        (x + hhtt - e, yscale * (y - e), z - hhtw + e),

        (x - ht, yscale * (y - e), z + hh),
        (x + ht, yscale * (y - e), z + hh),

        (x - ht, yscale * (y - e), z - hh),
        (x + ht, yscale * (y - e), z - hh),

        p1,
        p2,

        (p1[0], p1[1], z - hh),
        (p2[0], p2[1], z - hh),

        p3,
        p4,

        (p3[0], p3[1], z - hh),
        (p4[0], p4[1], z - hh),

        p5,
        p6,

        p7,
        p8,

        (p5[0], p5[1], p5[2] - vertical_tooth_height),
        (p6[0], p6[1], p6[2] - vertical_tooth_height),

        (p7[0], p7[1], p7[2] - vertical_tooth_height),
        (p8[0], p8[1], p8[2] - vertical_tooth_height),
    ]
    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),
        (4, 5), (5, 7), (7, 6), (6, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),

        (8, 9), (9, 11), (11, 10), (10, 8),

        (12, 13), (13, 15), (15, 14), (14, 12),
        (8, 12), (9, 13), (10, 14), (11, 15),

        (16, 17), (17, 19), (19, 18), (18, 16),

        (12, 16), (13, 17), (14, 18), (15, 19),

        (20, 21), (21, 23), (23, 22), (22, 20),

        (24, 25), (25, 27), (27, 26), (26, 24),
        (20, 24), (21, 25), (22, 26), (23, 27),
    ]
    faces = [
        (0, 1, 3, 2),
        (1, 0, 4, 5),
        (2, 3, 7, 6),
        (0, 2, 6, 4),
        (3, 1, 5, 7),

        (8, 9, 5, 4),
        (11, 10, 6, 7),
        (10, 8, 4, 6),
        (9, 11, 7, 5),

        (9, 8, 12, 13),
        (10, 11, 15, 14),
        (8, 10, 14, 12),
        (11, 9, 13, 15),

        (16, 17, 13, 12),
        (17, 19, 15, 13),
        (12, 14, 18, 16),
        (17, 16, 18, 19),

        (14, 15, 21, 20),
        (15, 19, 23, 21),
        (19, 18, 22, 23),
        (18, 14, 20, 22),

        (20, 21, 25, 24),
        (23, 22, 26, 27),
        (27, 25, 21, 23),
        (22, 20, 24, 26),

        (24, 25, 27, 26),
    ]

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh
def create_plate_top_mesh(
    e, t, r, sr, p, x, z,
    hex_side,
    large_tooth_width, large_tooth_height, large_tooth_thickness,
    small_teeth_width, small_teeth_height, small_teeth_thickness,
    leg_width,
    foot_w1, foot_w2, foot_thickness
):
    mesh = bpy.data.meshes.new('basis_plate_top_' + str((
        e, t, r, sr, p, x, z,
        hex_side,
        large_tooth_width, large_tooth_height, large_tooth_thickness,
        small_teeth_width, small_teeth_height, small_teeth_thickness,
        leg_width,
        foot_w1, foot_w2
    )))

    hw = 0.5 * leg_width
    hltt = 0.5 * large_tooth_thickness
    hltw = 0.5 * large_tooth_width

    hstt = 0.5 * small_teeth_thickness
    hstw = 0.5 * small_teeth_width
    hft = 0.5 * foot_thickness

    cx = -(math.sqrt(3) / 2) * hex_side

    pi6 = math.pi / 6
    cpi6 = math.cos(pi6)
    spi6 = math.sin(pi6)

    w3 = 0.5 * (foot_w2 - small_teeth_width - 2 * e)
    h3 = foot_w2 - w3

    nw = w3 * spi6
    fw = h3 * spi6

    ny = hw + foot_w1 + e + nw
    fy = hw + foot_w1 + e + fw

    nh = w3 * cpi6
    fh = h3 * cpi6

    rz = 0.5 * (r - sr)
    zo = 0.5 * rz
    zow = 0.5 * zo
    zop = 0.5 * zow
    zo = 0.25 * rz


    vertices = [
        (cx, 0, z),
        (cx, 0, z - t),

        #leg
        (x - hltt - e, hltw + e, z),
        (x + hltt + e, hltw + e, z),

        (x - hltt - e, -hltw - e, z),
        (x + hltt + e, -hltw - e, z),

        (x - hltt - e, hltw + e, z - t),
        (x + hltt + e, hltw + e, z - t),

        (x - hltt - e, -hltw - e, z - t),
        (x + hltt + e, -hltw - e, z - t),

        #right foot
        (x - (hft - hstt) - hstt - e - nh, ny, z),
        (x - (hft - hstt) + hstt + e - nh, ny, z),

        (x - (hft - hstt) - hstt - e - nh, ny, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - nh, ny, z - small_teeth_height),

        (x - (hft - hstt) - hstt - e - fh, fy, z),
        (x - (hft - hstt) + hstt + e - fh, fy, z),

        (x - (hft - hstt) - hstt - e - fh, fy, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - fh, fy, z - small_teeth_height),

        # left foot
        (x - (hft - hstt) - hstt - e - nh, -ny, z),
        (x - (hft - hstt) + hstt + e - nh, -ny, z),

        (x - (hft - hstt) - hstt - e - nh, -ny, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - nh, -ny, z - small_teeth_height),

        (x - (hft - hstt) - hstt - e - fh, -fy, z),
        (x - (hft - hstt) + hstt + e - fh, -fy, z),

        (x - (hft - hstt) - hstt - e - fh, -fy, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - fh, -fy, z - small_teeth_height),
    ]
    edges = [
        (2, 3), (3, 5), (5, 4), (4, 2),
        (6, 7), (7, 9), (9, 8), (8, 6),
        (2, 6), (3, 7), (4, 8), (5, 9),

        (10, 11), (11, 13), (13, 12), (12, 10),
        (14, 15), (15, 17), (17, 16), (16, 14),
        (10, 14), (11, 15), (12, 16), (13, 17),

        (18, 19), (19, 21), (21, 20), (20, 18),
        (22, 23), (23, 25), (25, 24), (24, 22),
        (18, 22), (19, 23), (20, 24), (21, 25),
    ]
    faces = [
        (3, 2, 6, 7),
        (4, 5, 9, 8),
        (2, 4, 8, 6),
        (5, 3, 7, 9),

        (10, 11, 13, 12),
        (15, 14, 16, 17),
        (13, 11, 15, 17),
        (10, 12, 16, 14),
        (12, 13, 17, 16),

        (19, 18, 20, 21),
        (22, 23, 25, 24),
        (19, 21, 25, 23),
        (20, 18, 22, 24),
        (21, 20, 24, 25),

        (2, 3, 11, 10),
        (5, 4, 18, 19),
    ]

    nb_verts2 = len(vertices)

    vertices.extend([
        (cx, sr + zo + e, z),
        (cx - zow + e, sr + zo + e - zop, z),
        (cx - zow + e, sr + rz - e + zo + zop, z),
        (cx, sr + rz - e + zo, z),

        (cx, -sr - zo, z),
        (cx + zow, -sr - zo + zop, z),
        (cx + zow, -sr - rz - zo - zop, z),
        (cx, -sr - rz - zo, z),

        (cx, sr + zo + e, z - t),
        (cx - zow + e, sr + zo + e - zop, z - t),
        (cx - zow + e, sr + rz - e + zo + zop, z - t),
        (cx, sr + rz - e + zo, z - t),

        (cx, -sr - zo, z - t),
        (cx + zow, -sr - zo + zop, z - t),
        (cx + zow, -sr - rz - zo - zop, z - t),
        (cx, -sr - rz - zo, z - t),
    ])

    nb_verts = len(vertices)

    i0 = None
    i1 = None
    i2 = None
    i3 = None
    i4 = None
    i5 = None
    i6 = None

    for i in range(0, p + 1):
        alpha = i * math.pi / p
        beta = -math.pi / 2 + alpha

        c = math.cos(beta)
        s = math.sin(beta)
        rc = r * c
        rs = r * s
        src = sr * c
        srs = sr * s

        vertices.extend([
            (cx + rc, rs, z),
            (cx + rc, rs, z - t),

            (cx + src, srs, z),
            (cx + src, srs, z - t),
        ])

        nbidx = 4
        tv = nb_verts + nbidx * i
        bv = tv + 1
        stv = tv + 2
        sbv = tv + 3

        if alpha >= math.pi / 6 and alpha < 5 * (math.pi / 6):
            edges.append((tv, bv))

        edges.extend([
            (stv, sbv),
        ])

        if i > 0:
            if alpha >= math.pi / 6 and alpha < 5 * (math.pi / 6):
                edges.extend([
                    (tv - nbidx, tv),
                    (bv - nbidx, bv),
                ])
                faces.extend([
                    (tv, tv - nbidx, bv - nbidx, bv),
                ])

            edges.extend([
                (stv - nbidx, stv),
                (sbv - nbidx, sbv),
            ])

            faces.extend([
                (stv - nbidx, stv, sbv, sbv - nbidx),
            ])

            if alpha < math.pi / 6:
                faces.extend([
                    #(tv - nbidx, tv, 23),
                    (stv, stv - nbidx, nb_verts2 + 5),

                    #(bv, bv - nbidx, 9),
                    (sbv - nbidx, sbv, 8),
                ])

                if i0 == None:
                    i0 = tv - nbidx
            elif alpha < math.pi / 3:
                faces.extend([
                    (tv - nbidx, tv, 19),
                    (stv, stv - nbidx, 18),

                    (bv, bv - nbidx, 9),
                    (sbv - nbidx, sbv, 8),
                ])

                if i1 == None:
                    i1 = tv - nbidx
            elif alpha < math.pi / 2:
                faces.extend([
                    (tv - nbidx, tv, 5),
                    (stv, stv - nbidx, 4),

                    (bv, bv - nbidx, 9),
                    (sbv - nbidx, sbv, 8),
                ])

                if i2 == None:
                    i2 = tv - nbidx
            elif alpha < 2 * math.pi / 3:
                faces.extend([
                    (tv - nbidx, tv, 3),
                    (stv, stv - nbidx, 2),

                    (bv, bv - nbidx, 7),
                    (sbv - nbidx, sbv, 6),
                ])

                if i3 == None:
                    i3 = tv - nbidx
            elif alpha < 5 * math.pi / 6:
                faces.extend([
                    (tv - nbidx, tv, 11),
                    (stv, stv - nbidx, 10),

                    (bv, bv - nbidx, 7),
                    (sbv - nbidx, sbv, 6),
                ])

                if i4 == None:
                    i4 = tv - nbidx
            else:
                faces.extend([
                    #(tv - nbidx, tv, 15),
                    #(stv, stv - nbidx, 14),
                    (stv, stv - nbidx, 10),

                    #(bv, bv - nbidx, 7),
                    (sbv - nbidx, sbv, 6),
                ])

                if i5 == None:
                    i5 = tv - nbidx

            if i == p and i6 == None:
                i6 = tv


    nb_verts3 = len(vertices)

    vertices.extend([
        (cx, r * math.cos(math.pi / 6), z),
        (cx, r * math.cos(math.pi / 6), z - t),
        (cx, -r * math.cos(math.pi / 6), z),
        (cx, -r * math.cos(math.pi / 6), z - t),
    ])

    faces.extend([
        #(i0 + 2, i0, 22),
        (nb_verts3 + 2, 23, 22),
        (i1, 19, 23),
        (i1 + 2, 22, 18),
        (i2, 5, 19),
        (i2 + 2, 18, 4),
        (i3, 3, 5),
        (i3 + 2, 4, 2),
        (i4, 11, 3),
        (i4 + 2, 2, 10),
        (i5, 15, 11),
        (i6 + 2, 10, 14),
        (nb_verts3, 14, 15),
        (nb_verts3, i6 + 2, 14),

        #(i0 + 1, i0 + 3, 8),
        (nb_verts3 + 3, 8, 9),
        (i3 + 1, 9, 7),
        (i3 + 3, 6, 8),
        (nb_verts3 + 1, 7, 6),
        (i6 + 3, nb_verts3 + 1, 6),
    ])


    edges.extend([
        (i6 + 2, nb_verts2),
        (nb_verts2, nb_verts2 + 1),
        (nb_verts2 + 1, nb_verts2 + 2),
        (nb_verts2 + 2, nb_verts2 + 3),
        (nb_verts2 + 3, nb_verts3),

        (i0 + 2, nb_verts2 + 4),
        (nb_verts2 + 4, nb_verts2 + 5),
        (nb_verts2 + 5, nb_verts2 + 6),
        (nb_verts2 + 6, nb_verts2 + 7),
        (nb_verts2 + 7, nb_verts3 + 2),

        (i6 + 3, nb_verts2 + 8),
        (nb_verts2 + 8, nb_verts2 + 9),
        (nb_verts2 + 9, nb_verts2 + 10),
        (nb_verts2 + 10, nb_verts2 + 11),
        (nb_verts2 + 11, nb_verts3 + 1),

        (i0 + 3, nb_verts2 + 12),
        (nb_verts2 + 12, nb_verts2 + 13),
        (nb_verts2 + 13, nb_verts2 + 14),
        (nb_verts2 + 14, nb_verts2 + 15),
        (nb_verts2 + 15, nb_verts3 + 3),
    ])
    faces.extend([
        (i6 + 2, nb_verts2, nb_verts2 + 8, i6 + 3),
        (nb_verts2, nb_verts2 + 1, nb_verts2 + 9, nb_verts2 + 8),
        (nb_verts2 + 1, nb_verts2 + 2, nb_verts2 + 10, nb_verts2 + 9),
        (nb_verts2 + 2, nb_verts2 + 3, nb_verts2 + 11, nb_verts2 + 10),
        (nb_verts2 + 3, nb_verts3, nb_verts3 + 1, nb_verts2 + 11),

        (nb_verts2 + 4, i0 + 2, i0 + 3, nb_verts2 + 12),
        (nb_verts2 + 5, nb_verts2 + 4, nb_verts2 + 12, nb_verts2 + 13),
        (nb_verts2 + 6, nb_verts2 + 5, nb_verts2 + 13, nb_verts2 + 14),
        (nb_verts2 + 7, nb_verts2 + 6, nb_verts2 + 14, nb_verts2 + 15),
        (nb_verts3 + 2, nb_verts2 + 7, nb_verts2 + 15, nb_verts3 + 3),

        (nb_verts2 + 1, nb_verts2, nb_verts2 + 3, nb_verts2 + 2),
        (nb_verts2 + 8, nb_verts2 + 9, nb_verts2 + 10, nb_verts2 + 11),

        (i0 + 2, nb_verts2 + 4, nb_verts2 + 5),
        ##(i0 + 2, nb_verts2 + 5, 22),
        (nb_verts2 + 5, nb_verts2 + 6, 22),
        (nb_verts2 + 6, nb_verts2 + 7, nb_verts3 + 2),
        (22, nb_verts2 + 6, nb_verts3 + 2),

        (i0 + 3, nb_verts2 + 13, nb_verts2 + 12),
        (nb_verts3 + 3, nb_verts2 + 15, nb_verts2 + 14),
        (nb_verts2 + 14, nb_verts2 + 13, 8),
        (nb_verts3 + 3, nb_verts2 + 14, 8),
        (8, nb_verts2 + 13, i0 + 3),

        (i5, nb_verts3, 15),
        (nb_verts3, i5, i5 + 1, nb_verts3 + 1),
        (nb_verts3 + 1, i5 + 1, 7),

        (i1, nb_verts3 + 2, 23),
        (nb_verts3 + 2, i1, i1 + 1, nb_verts3 + 3),
        (nb_verts3 + 3, i1 + 1, 9),

        (i1 + 2, 22, nb_verts2 + 5),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def create_plate_bottom_mesh(
    e, t, r, sr, p, x, z,
    hex_side,
    top_plate_thickness
):
    mesh = bpy.data.meshes.new('basis_plate_bottom_' + str((
        e, t, r, sr, p, x, z,
        hex_side,
        top_plate_thickness
    )))

    cx = -(math.sqrt(3) / 2) * hex_side
    sre = sr - e

    pi2 = math.pi / 2
    pi3 = math.pi / 3
    pi6 = math.pi / 6

    b0 = None
    b1 = None
    for i in range(0, p + 1):
        alpha = i * (math.pi) / p
        beta = -pi2 + alpha
        if b0 == None and alpha >= pi6:
            b0 = beta - math.pi / p
        elif b1 == None and alpha >= 5 * pi6:
            b1 = beta - math.pi / p
            break

    vertices = [
        (cx, 0, z),
        (cx, 0, z - t),
        (cx, sr, z),
        (cx, sr, z - t),
        (cx, -sr, z),
        (cx, -sr, z - t),
        (cx + r * math.cos(b0), r * math.sin(b0), z),
        (cx + r * math.cos(b0), r * math.sin(b0), z - t),
        (cx + r * math.cos(b1), r * math.sin(b1), z),
        (cx + r * math.cos(b1), r * math.sin(b1), z - t),
    ]
    edges = []
    faces = []

    nb_verts = len(vertices)

    i0 = None
    i1 = None
    for i in range(0, p + 1):
        alpha = i * (math.pi) / p
        beta = -pi2 + alpha

        nbidx = 4
        stv = nb_verts + nbidx * i
        sbv = stv + 1
        tv = stv + 2
        bv = stv + 3

        vertices.extend([
            (cx + sr * math.cos(beta), sr * math.sin(beta), z),
            (cx + sr * math.cos(beta), sr * math.sin(beta), z - t),
            (cx + r * math.cos(beta), r * math.sin(beta), z),
            (cx + r * math.cos(beta), r * math.sin(beta), z - t),
        ])


        edges.extend([
            (stv, sbv),
        ])

        if alpha >= pi6 and alpha < 5 * pi6:
            edges.extend([
                (tv, bv),
                (stv, tv),
                (sbv, bv),
            ])

            if i0 == None:
                i0 = stv - nbidx

        if i1 == None and alpha > 5 * pi6:
            i1 = stv - nbidx

        if i > 0:
            edges.extend([
                (stv - nbidx, stv),
                (sbv - nbidx, sbv),
            ])

            faces.extend([
                (sbv, sbv - nbidx, stv - nbidx, stv),
            ])

            if alpha >= pi6 and alpha < 5 * pi6:
                edges.extend([
                    (tv - nbidx, tv),
                    (bv - nbidx, bv),
                ])

                faces.extend([
                    (bv - nbidx, bv, tv, tv - nbidx),
                    (stv, stv - nbidx, tv - nbidx, tv),
                    (sbv - nbidx, sbv, bv, bv - nbidx),
                ])

            if alpha < pi6:
                faces.extend([
                    (6, stv - nbidx, stv),
                    (7, sbv, sbv - nbidx),
                ])
            elif alpha >= 5 * pi6:
                faces.extend([
                    (8, stv - nbidx, stv),
                    (9, sbv, sbv - nbidx),
                ])

    nb_verts2 = len(vertices)

    lr = r - r * math.sin(-pi2 + 5 * pi6)
    rz = 0.5 * (r - sr - lr)
    zo = 0.5 * rz
    zow = 0.5 * zo
    zop = 0.5 * zow

    vertices.extend([
        (cx, r * math.sin(-pi2 + pi6), z),
        (cx, r * math.sin(-pi2 + pi6), z - t),

        (cx, r * math.sin(-pi2 + 5 * pi6), z),
        (cx, r * math.sin(-pi2 + 5 * pi6), z - t),

        # outer tooth
        (cx, sr + rz - zo + e, z),
        (cx, sr + rz - zo + e, z - t),

        (cx - zow + e, sr + rz - zo + e - zop, z),
        (cx - zow + e, sr + rz - zo + e - zop, z - t),

        (cx - zow + e, sr + rz + zo - e + zop, z),
        (cx - zow + e, sr + rz + zo - e + zop, z - t),

        (cx, sr + rz + zo - e, z),
        (cx, sr + rz + zo - e, z - t),

        # inner tooth
        (cx, -sr - rz + zo, z),
        (cx, -sr - rz + zo, z - t),

        (cx + zow, -sr - rz + zo + zop, z),
        (cx + zow, -sr - rz + zo + zop, z - t),

        (cx + zow, -sr - rz - zo - zop, z),
        (cx + zow, -sr - rz - zo - zop, z - t),

        (cx, -sr - rz - zo, z),
        (cx, -sr - rz - zo, z - t),
    ])

    edges.extend([
        (i0 + 2, nb_verts2),
        (i0 + 3, nb_verts2 + 1),
        (i0 + 2, i0 + 3),
        (nb_verts2, nb_verts2 + 1),

        (nb_verts2 + 4, nb_verts2 + 6),
        (nb_verts2 + 6, nb_verts2 + 8),
        (nb_verts2 + 8, nb_verts2 + 10),

        (nb_verts2 + 5, nb_verts2 + 7),
        (nb_verts2 + 7, nb_verts2 + 9),
        (nb_verts2 + 9, nb_verts2 + 11),

        (nb_verts2 + 12, nb_verts2 + 14),
        (nb_verts2 + 14, nb_verts2 + 16),
        (nb_verts2 + 16, nb_verts2 + 18),

        (nb_verts2 + 13, nb_verts2 + 15),
        (nb_verts2 + 15, nb_verts2 + 17),
        (nb_verts2 + 17, nb_verts2 + 19),

        (4, nb_verts2 + 12),
        (5, nb_verts2 + 13),
        (nb_verts2 + 18, nb_verts2),
        (nb_verts2 + 19, nb_verts2 + 1),
    ])

    faces.extend([
        (nb_verts2 + 1, i0 + 3, i0 + 2, nb_verts2),
        (nb_verts2 + 6, nb_verts2 + 4, nb_verts2 + 10, nb_verts2 + 8),
        (nb_verts2 + 5, nb_verts2 + 7, nb_verts2 + 9, nb_verts2 + 11),
        (nb_verts2 + 2, i1 + 2, nb_verts2 + 2),
        (2, i1 + 2, nb_verts2 + 2),
        (i1 + 3, 3, nb_verts2 + 3),
        (2, nb_verts2 + 4, nb_verts2 + 5, 3),
        (nb_verts2 + 4, nb_verts2 + 6, nb_verts2 + 7, nb_verts2 + 5),
        (nb_verts2 + 6, nb_verts2 + 8, nb_verts2 + 9, nb_verts2 + 7),
        (nb_verts2 + 8, nb_verts2 + 10, nb_verts2 + 11, nb_verts2 + 9),
        (nb_verts2 + 10, nb_verts2 + 2, nb_verts2 + 3, nb_verts2 + 11),
        (nb_verts2 + 2, i1 + 2, i1 + 3, nb_verts2 + 3),

        (nb_verts2 + 12, 4, 5, nb_verts2 + 13),
        (nb_verts2 + 14, nb_verts2 + 12, nb_verts2 + 13, nb_verts2 + 15),
        (nb_verts2 + 16, nb_verts2 + 14, nb_verts2 + 15, nb_verts2 + 17),
        (nb_verts2 + 18, nb_verts2 + 16, nb_verts2 + 17, nb_verts2 + 19),
        (nb_verts2, nb_verts2 + 18, nb_verts2 + 19, nb_verts2 + 1),

        (4, nb_verts2 + 12, nb_verts2 + 14),
        (5, nb_verts2 + 15, nb_verts2 + 13),
        (nb_verts2 + 16, i0 + 2, nb_verts2 + 14),
        (nb_verts2 + 15, i0 + 3, nb_verts2 + 17),
        (nb_verts2 + 16, nb_verts2 + 18, nb_verts2),
        (nb_verts2 + 19, nb_verts2 + 17, nb_verts2 + 1),
        (nb_verts2 + 16, nb_verts2, i0 + 2),
        (nb_verts2 + 1, nb_verts2 + 17, i0 + 3),
        (4, nb_verts2 + 14, i0 + 2),
        (5, i0 + 3, nb_verts2 + 15),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def create_plate_axis_mesh(e, t, r, p, x, z, top_t, top_r, bottom_t, bottom_r):

    mesh = bpy.data.meshes.new('basis_plate_axis_' + str((
        e, t, r, p, x, z,
        top_t, top_r,
        bottom_t, bottom_r
    )))

    tr = top_r - e
    br = bottom_r - e

    vertices = [
        (x, 0, z + top_t + e),
        (x, 0, z),
        (x, 0, z - t),
        (x, 0, z - t - bottom_t),
    ]
    edges = []
    faces = []

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (2 * math.pi) / p
        beta = 0 + alpha

        nbidx = 6
        ttv = nb_verts + i * nbidx
        tbv = ttv + 1
        wtv = ttv + 2
        wbv = ttv + 3
        btv = ttv + 4
        bbv = ttv + 5

        vertices.extend([
            (x + tr * math.cos(beta), tr * math.sin(beta), z + top_t + e),
            (x + tr * math.cos(beta), tr * math.sin(beta), z),
            (x + r * math.cos(beta), r * math.sin(beta), z),
            (x + r * math.cos(beta), r * math.sin(beta), z - t),
            (x + br * math.cos(beta), br * math.sin(beta), z - t),
            (x + br * math.cos(beta), br * math.sin(beta), z - t - bottom_t),
        ])

        edges.extend([
            (ttv, tbv),
            (wtv, wbv),
            (btv, bbv),
        ])

        if i > 0:
            edges.extend([
                (ttv - nbidx, ttv),
                (tbv - nbidx, tbv),
                (wtv - nbidx, wtv),
                (wbv - nbidx, wbv),
                (btv - nbidx, btv),
                (bbv - nbidx, bbv),
            ])

            faces.extend([
                (ttv - nbidx, ttv, 0),
                (ttv, ttv - nbidx, tbv - nbidx, tbv),
                (tbv, tbv - nbidx, wtv - nbidx, wtv),
                (wtv, wtv - nbidx, wbv - nbidx, wbv),
                (wbv, wbv - nbidx, btv - nbidx, btv),
                (btv, btv - nbidx, bbv - nbidx, bbv),
                (bbv, bbv - nbidx, 3),
            ])


    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def move_basis_to(obj, hex):
    hex_1 = hex2xy(r, 0, 0, hex, 1)
    hex_2 = hex2xy(r, 0, 0, hex, 2)
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
    basis_wheel_kr,
    basis_wheel_kw,
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
    basis_wheel_kr,
    basis_wheel_kw,
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

basis_leg_mesh = create_basis_leg_mesh(
    basis_leg_e,
    basis_leg_t,
    basis_leg_h,
    basis_leg_w,
    basis_leg_x,
    basis_leg_z,
    basis_leg_teeth_width,
    basis_leg_teeth_height,
    basis_leg_teeth_thickness,
    basis_leg_side_teeth_width,
    basis_leg_side_teeth_height,
    basis_leg_side_teeth_thickness,
    basis_leg_side_teeth_z
)

basis_foot_mesh_r = create_foot_mesh(
    basis_foot_e,
    basis_foot_t,
    basis_foot_h,
    basis_foot_w1,
    basis_foot_w2,
    basis_foot_x,
    basis_foot_y,
    basis_foot_z,
    basis_foot_horizontal_tooth_width,
    basis_foot_horizontal_tooth_height,
    basis_foot_horizontal_tooth_thickness,
    basis_foot_vertical_tooth_width,
    basis_foot_vertical_tooth_height,
    basis_foot_vertical_tooth_thickness,
    1 # yscale
)

basis_foot_mesh_l = create_foot_mesh(
    basis_foot_e,
    basis_foot_t,
    basis_foot_h,
    basis_foot_w1,
    basis_foot_w2,
    basis_foot_x,
    basis_foot_y,
    basis_foot_z,
    basis_foot_horizontal_tooth_width,
    basis_foot_horizontal_tooth_height,
    basis_foot_horizontal_tooth_thickness,
    basis_foot_vertical_tooth_width,
    basis_foot_vertical_tooth_height,
    basis_foot_vertical_tooth_thickness,
    -1 # yscale
)

basis_plate_top_mesh = create_plate_top_mesh(
    basis_plate_top_e,
    basis_plate_top_t,
    basis_plate_top_r,
    basis_plate_top_sr,
    basis_plate_top_p,
    basis_plate_top_x,
    basis_plate_top_z,
    basis_plate_top_hex_side,
    basis_plate_top_large_tooth_width,
    basis_plate_top_large_tooth_height,
    basis_plate_top_large_tooth_thickness,
    basis_plate_top_small_teeth_width,
    basis_plate_top_small_teeth_height,
    basis_plate_top_small_teeth_thickness,
    basis_plate_top_leg_width,
    basis_plate_top_foot_w1,
    basis_plate_top_foot_w2,
    basis_plate_top_foot_thickness
)

basis_plate_axis_mesh = create_plate_axis_mesh(
    basis_plate_axis_e,
    basis_plate_axis_t,
    basis_plate_axis_r,
    basis_plate_axis_p,
    basis_plate_axis_x,
    basis_plate_axis_z,
    basis_plate_axis_top_t,
    basis_plate_axis_top_r,
    basis_plate_axis_bottom_t,
    basis_plate_axis_bottom_r
)

basis_plate_bottom_mesh = create_plate_bottom_mesh(
    basis_plate_bottom_e,
    basis_plate_bottom_t,
    basis_plate_bottom_r,
    basis_plate_bottom_sr,
    basis_plate_bottom_p,
    basis_plate_bottom_x,
    basis_plate_bottom_z,
    basis_plate_bottom_hex_side,
    basis_plate_bottom_top_plate_thickness
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

basis_leg_r = bpy.data.objects.new('basis_leg_r', basis_leg_mesh)
basis_collection.objects.link(basis_leg_r)
move_basis_to(basis_leg_r, 0)

basis_foot_rr = bpy.data.objects.new('basis_foot_rr', basis_foot_mesh_r)
basis_collection.objects.link(basis_foot_rr)
move_basis_to(basis_foot_rr, 0)

basis_foot_rl = bpy.data.objects.new('basis_foot_rl', basis_foot_mesh_l)
basis_collection.objects.link(basis_foot_rl)
move_basis_to(basis_foot_rl, 0)

basis_plate_top_r = bpy.data.objects.new('basis_plate_top_r', basis_plate_top_mesh)
basis_collection.objects.link(basis_plate_top_r)
move_basis_to(basis_plate_top_r, 0)

basis_plate_bottom_r = bpy.data.objects.new('basis_plate_bottom_r', basis_plate_bottom_mesh)
basis_collection.objects.link(basis_plate_bottom_r)
move_basis_to(basis_plate_bottom_r, 0)

basis_plate_axis = bpy.data.objects.new('basis_plate_axis', basis_plate_axis_mesh)
basis_collection.objects.link(basis_plate_axis)
move_basis_to(basis_plate_axis, 0)


basis_wheel_object_l = bpy.data.objects.new('basis_wheel_l', basis_wheel_mesh)
basis_collection.objects.link(basis_wheel_object_l)
move_basis_to(basis_wheel_object_l, 3)

basis_wheel_object_l_bottom = bpy.data.objects.new('basis_wheel_l_bottom', basis_wheel_bottom_mesh)
basis_collection.objects.link(basis_wheel_object_l_bottom)
move_basis_to(basis_wheel_object_l_bottom, 3)

basis_arm_l = bpy.data.objects.new('basis_arm_l', basis_arm_mesh)
basis_collection.objects.link(basis_arm_l)
move_basis_to(basis_arm_l, 3)

basis_leg_l = bpy.data.objects.new('basis_leg_l', basis_leg_mesh)
basis_collection.objects.link(basis_leg_l)
move_basis_to(basis_leg_l, 3)

basis_foot_lr = bpy.data.objects.new('basis_foot_lr', basis_foot_mesh_r)
basis_collection.objects.link(basis_foot_lr)
move_basis_to(basis_foot_lr, 3)

basis_foot_ll = bpy.data.objects.new('basis_foot_ll', basis_foot_mesh_l)
basis_collection.objects.link(basis_foot_ll)
move_basis_to(basis_foot_ll, 3)

basis_plate_top_l = bpy.data.objects.new('basis_plate_top_l', basis_plate_top_mesh)
basis_collection.objects.link(basis_plate_top_l)
move_basis_to(basis_plate_top_l, 3)

basis_plate_bottom_l = bpy.data.objects.new('basis_plate_bottom_l', basis_plate_bottom_mesh)
basis_collection.objects.link(basis_plate_bottom_l)
move_basis_to(basis_plate_bottom_l, 3)

print('done')
# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\basis_", check_existing=True, filter_glob='*.stl', use_selection=False, global_scale=100.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z')