import bpy
import math

from optics import get_support_arm_point, hex2xy, hex2xyz

support_arm_name = 'support_arm'

def create_mesh(
    e, f, n, r, t, m, p,
    hex_thickness, hex_walls_height,
    primary_thickness,
    arm_radius
):
    mesh_name = support_arm_name + '_' + str(())
    mesh = bpy.data.meshes.new(mesh_name)

    arm_points = get_support_arm_point(n, r, m, 0)

    ht = 0.5 * t
    ch = 0.2
    rh = ch * 0.5 * math.sqrt(3) * r
    h = arm_points[1][1] + rh
    wv = 0.5 * r * (1 if n % 2 else -1)

    x0 = arm_points[0][0] - m
    x1 = x0 + ch * wv
    x2 = x0 + wv
    print('n', str(n), str(1 if n % 2 else -1), str(x0), str(x1))

    outer_r = max(
        x0 + m,
        math.sqrt((arm_points[0][0] + m) ** 2 + h ** 2)
    )

    if n % 2 == 0:
        y2 = hex2xyz(f, r, math.floor(0.5 * n), 1, 5, 1)[2]
        y3 = hex2xyz(f, r, math.floor(0.5 * n), 1, 0, 1)[2]
        y5 = hex2xyz(f, r, math.floor(0.5 * n), 1, 0, 2)[2]
    else:
        y2 = hex2xyz(f, r, math.ceil(0.5 * n), 0, 0, 1)[2]
        y3 = hex2xyz(f, r, math.ceil(0.5 * n), 0, 5, 1)[2]
        y5 = hex2xyz(f, r, math.ceil(0.5 * n) + 1, -2, 0, 1)[2]

    y2 -= hex_thickness + hex_walls_height + t
    y3 -= hex_thickness + hex_walls_height + t
    y5 -= hex_thickness + hex_walls_height + t
    y4 = y3 + ch * (y5 - y3)
    print('y4', str(y4), str(y3), str(y5), str(y5 - y3), str(ch))
    y0 = y4
    y1 = y3

    v0 = (x1, -h, y0)
    v1 = (x0, arm_points[0][1], y1)
    v2 = (x2, 0, y2)
    v3 = (x0, arm_points[1][1], y3)
    v4 = (x1, h, y4)

    h0 = t
    h1 = h0 + hex_thickness + hex_walls_height + primary_thickness
    h2 = h1 - hex_walls_height
    h3 = h1 + t
    h4 = min(v2[2], v3[2], v4[2])
    h5 = max(v2[2], v3[2], v4[2]) + h3

    vertices = [
        (v0[0], v0[1], v0[2]),
        (v0[0], v0[1], v0[2] + h0),
        (v0[0], v0[1], v0[2] + h1),
        (v0[0], v0[1], v0[2] + h3),

        (v1[0], v1[1], v1[2]),
        (v1[0], v1[1], v1[2] + h0),
        (v1[0], v1[1], v1[2] + h1),
        (v1[0], v1[1], v1[2] + h3),

        # 8
        (v2[0], v2[1], v2[2]),
        (v2[0], v2[1], v2[2] + h0),
        (v2[0], v2[1], v2[2] + h1),
        (v2[0], v2[1], v2[2] + h3),

        (v3[0], v3[1], v3[2]),
        (v3[0], v3[1], v3[2] + h0),
        (v3[0], v3[1], v3[2] + h1),
        (v3[0], v3[1], v3[2] + h3),

        # 16
        (v4[0], v4[1], v4[2]),
        (v4[0], v4[1], v4[2] + h0),
        (v4[0], v4[1], v4[2] + h1),
        (v4[0], v4[1], v4[2] + h3),

        # 20
        (v0[0] - 2 * hex_thickness, v0[1], v0[2]),
        (v0[0] - 2 * hex_thickness, v0[1], v0[2] + h0),
        (v0[0] - 2 * hex_thickness, v0[1], v0[2] + h1),
        (v0[0] - 2 * hex_thickness, v0[1], v0[2] + h3),

        (v1[0] - 2 * hex_thickness, v1[1], v1[2]),
        (v1[0] - 2 * hex_thickness, v1[1], v1[2] + h0),
        (v1[0] - 2 * hex_thickness, v1[1], v1[2] + h1),
        (v1[0] - 2 * hex_thickness, v1[1], v1[2] + h3),

        # 28
        (v2[0] - 2 * hex_thickness, v2[1], v2[2]),
        (v2[0] - 2 * hex_thickness, v2[1], v2[2] + h0),
        (v2[0] - 2 * hex_thickness, v2[1], v2[2] + h1),
        (v2[0] - 2 * hex_thickness, v2[1], v2[2] + h3),

        (v3[0] - 2 * hex_thickness, v3[1], v3[2]),
        (v3[0] - 2 * hex_thickness, v3[1], v3[2] + h0),
        (v3[0] - 2 * hex_thickness, v3[1], v3[2] + h1),
        (v3[0] - 2 * hex_thickness, v3[1], v3[2] + h3),

        # 36
        (v4[0] - 2 * hex_thickness, v4[1], v4[2]),
        (v4[0] - 2 * hex_thickness, v4[1], v4[2] + h0),
        (v4[0] - 2 * hex_thickness, v4[1], v4[2] + h1),
        (v4[0] - 2 * hex_thickness, v4[1], v4[2] + h3),
    ]
    edges = [
        (0, 3),
        (0, 3),
        (4, 7),
        (8, 11),
        (12, 15),
        (16, 19),
        (0, 4), (4, 8), (8, 12), (12, 16),
        (3, 7), (7, 11), (11, 15), (15, 19),

        (0, 20), (4, 24), (8, 28), (12, 32), (16, 36),
        (1, 21), (5, 25), (9, 29), (13, 33), (17, 37),
        (2, 22), (6, 26), (10, 30), (14, 34), (18, 38),
        (3, 23), (7, 27), (11, 31), (15, 35), (19, 39),

        (20, 21), (24, 25), (28, 29), (32, 33), (36, 37),
        (22, 23), (26, 27), (30, 31), (34, 35), (38, 39),

        (20, 24), (24, 28), (28, 32), (32, 36),
        (21, 25), (25, 29), (29, 33), (33, 37),
        (22, 26), (26, 30), (30, 34), (34, 38),
        (23, 27), (27, 31), (31, 35), (35, 39),
    ]
    faces = [
        (20, 21, 25, 24), (24, 25, 29, 28), (28, 29, 33, 32), (32, 33, 37, 36),
        (1, 2, 6, 5), (5, 6, 10, 9), (9, 10, 14, 13), (13, 14, 18, 17),
        (22, 23, 27, 26), (26, 27, 31, 30), (30, 31, 35, 34), (34, 35, 39, 38),
        (0, 1, 21, 20), (16, 17, 37, 36),
        (2, 3, 23, 22), (18, 19, 39, 38),
        (0, 4, 24, 20), (4, 8, 28, 24), (8, 12, 32, 28), (12, 16, 36, 32),
        (1, 5, 25, 21), (5, 9, 29, 25), (9, 13, 33, 29), (13, 17, 37, 33),
        (2, 6, 26, 22), (6, 10, 30, 26), (10, 14, 34, 30), (14, 18, 38, 34),
        (3, 7, 27, 23), (7, 11, 31, 27), (11, 15, 35, 31), (15, 19, 39, 35),
    ]

    nb_verts = len(vertices)

    max_angle = math.asin(h / outer_r)
    print('max_angle', str(max_angle), str(h / outer_r))

    for i in range(0, p + 1):
        alpha = i * max_angle / p
        ca = math.cos(alpha)
        sa = math.sin(alpha)

        beta = i * math.tau / p
        cb = math.cos(beta)
        sb = math.sin(beta)
        ar = arm_radius + 0.5 * e

        vertices.extend([
            (outer_r * ca, outer_r * sa, h5),
            (outer_r * ca, outer_r * sa, h4),

            (outer_r * ca, -outer_r * sa, h5),
            (outer_r * ca, -outer_r * sa, h4),

            (arm_points[0][0] + ar * cb, arm_points[0][1] + ar * sb, h5),
            (arm_points[0][0] + ar * cb, arm_points[0][1] + ar * sb, h4),

            (arm_points[1][0] + ar * cb, arm_points[1][1] + ar * sb, h5),
            (arm_points[1][0] + ar * cb, arm_points[1][1] + ar * sb, h4),
        ])

        nbidx = 8
        rtv = nb_verts + i * nbidx
        rbv = rtv + 1
        ltv = rtv + 2
        lbv = rtv + 3
        lctv = rtv + 4
        lcbv = rtv + 5
        rctv = rtv + 6
        rcbv = rtv + 7

        edges.extend([
            (rtv, rbv),
            (ltv, lbv),
            (lctv, lcbv),
            (rctv, rcbv),
        ])

        if i > 0:
            edges.extend([
                (rtv, rtv - nbidx),
                (rbv, rbv - nbidx),
                (ltv - nbidx, ltv),
                (lbv - nbidx, lbv),
                (lcbv - nbidx, lcbv),
                (rcbv - nbidx, rcbv),
            ])

            faces.extend([
                (rtv, rtv - nbidx, rbv - nbidx, rbv),
                (ltv - nbidx, ltv, lbv, lbv - nbidx),
                (lctv - nbidx, lctv, lcbv, lcbv - nbidx),
                (rctv - nbidx, rctv, rcbv, rcbv - nbidx),
            ])

    edges.extend([
        (rtv, 19),
        (rbv, 16),
        (ltv, 3),
        (lbv, 0),
    ])

    faces.extend([
        (3, 0, lbv, ltv),
        (19, 16, rbv, rtv),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh