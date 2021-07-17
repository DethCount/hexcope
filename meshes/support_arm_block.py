import bpy
import math
from mathutils import Vector

from optics import get_support_arm_point, hex2xy, hex2xyz

support_arm_block_name = 'support_arm_block'

# todo: thicker nose part
def create_mesh(
    e, f, n, r, t, m, p,
    hex_thickness, hex_walls_height,
    primary_thickness,
    arm_radius
):
    mesh = bpy.data.meshes.new(
        support_arm_block_name
        + '_' + str((
            e, f, n, r, t, m, p,
            hex_thickness, hex_walls_height,
            primary_thickness,
            arm_radius
        ))
    )

    arm_points = get_support_arm_point(n, r, m, 0)
    ch = 0.2

    if n % 2 == 0:
        p2 = Vector(hex2xyz(f, r, math.floor(0.5 * n), 1, 5, 1))
        p3 = Vector(hex2xyz(f, r, math.floor(0.5 * n), 1, 0, 1))
        p5 = Vector(hex2xyz(f, r, math.floor(0.5 * n), 1, 0, 2))
    else:
        p2 = Vector(hex2xyz(f, r, math.ceil(0.5 * n), 0, 0, 1))
        p3 = Vector(hex2xyz(f, r, math.ceil(0.5 * n), 0, 5, 1))
        p5 = Vector(hex2xyz(f, r, math.ceil(0.5 * n) + 1, -2, 0, 1))

    v35n = (p5 - p3).normalized()
    p4 = p3 + v35n * ch

    outer_r = max(
        p2.x + m,
        math.sqrt((arm_points[0][0] + m) ** 2 + p4.y ** 2)
    )
    max_angle = math.asin(p4.y / outer_r)
    arc_string_x = outer_r * math.cos(max_angle)

    hex_total_thickness = hex_thickness + hex_walls_height + t

    v0 = Vector((p4.x, -p4.y, p4.z - hex_total_thickness))
    v1 = Vector((p3.x, -p3.y, p3.z - hex_total_thickness))
    v2 = Vector((p2.x, p2.y, p2.z - hex_total_thickness))
    v3 = Vector((p3.x, p3.y, p3.z - hex_total_thickness))
    v4 = Vector((p4.x, p4.y, p4.z - hex_total_thickness))

    h0 = t
    h1 = h0 + hex_thickness + hex_walls_height + primary_thickness
    h2 = h1 + t
    h3 = min(v2.z, v3.z, v4.z)
    h4 = max(v2.z, v3.z, v4.z) + h2

    ar = arm_radius + 0.5 * e

    vertices = [
        (v0.x, v0.y, h3),
        (v0.x, v0.y, v0.z + h0),
        (v0.x, v0.y, v0.z + h1),
        (v0.x, v0.y, h4),

        (v1.x, v1.y, h3),
        (v1.x, v1.y, v1.z + h0),
        (v1.x, v1.y, v1.z + h1),
        (v1.x, v1.y, h4),

        # 8
        (v2.x, v2.y, h3),
        (v2.x, v2.y, v2.z + h0),
        (v2.x, v2.y, v2.z + h1),
        (v2.x, v2.y, h4),

        (v3.x, v3.y, h3),
        (v3.x, v3.y, v3.z + h0),
        (v3.x, v3.y, v3.z + h1),
        (v3.x, v3.y, h4),

        # 16
        (v4.x, v4.y, h3),
        (v4.x, v4.y, v4.z + h0),
        (v4.x, v4.y, v4.z + h1),
        (v4.x, v4.y, h4),

        # 20
        (v0.x - 2 * hex_thickness, v0.y, h3),
        (v0.x - 2 * hex_thickness, v0.y, v0.z + h0),
        (v0.x - 2 * hex_thickness, v0.y, v0.z + h1),
        (v0.x - 2 * hex_thickness, v0.y, h4),

        (v1.x - 2 * hex_thickness, v1.y, h3),
        (v1.x - 2 * hex_thickness, v1.y, v1.z + h0),
        (v1.x - 2 * hex_thickness, v1.y, v1.z + h1),
        (v1.x - 2 * hex_thickness, v1.y, h4),

        # 28
        (v2.x - 2 * hex_thickness, v2.y, h3),
        (v2.x - 2 * hex_thickness, v2.y, v2.z + h0),
        (v2.x - 2 * hex_thickness, v2.y, v2.z + h1),
        (v2.x - 2 * hex_thickness, v2.y, h4),

        (v3.x - 2 * hex_thickness, v3.y, h3),
        (v3.x - 2 * hex_thickness, v3.y, v3.z + h0),
        (v3.x - 2 * hex_thickness, v3.y, v3.z + h1),
        (v3.x - 2 * hex_thickness, v3.y, h4),

        # 36
        (v4.x - 2 * hex_thickness, v4.y, h3),
        (v4.x - 2 * hex_thickness, v4.y, v4.z + h0),
        (v4.x - 2 * hex_thickness, v4.y, v4.z + h1),
        (v4.x - 2 * hex_thickness, v4.y, h4),

        # 40
        (arm_points[0][0] - ar, arm_points[0][1] - ar, h3),
        (arm_points[0][0] - ar, arm_points[0][1] - ar, h4),

        (arm_points[0][0] - ar, arm_points[0][1] + ar, h3),
        (arm_points[0][0] - ar, arm_points[0][1] + ar, h4),

        (arm_points[0][0] + ar, arm_points[0][1] - ar, h3),
        (arm_points[0][0] + ar, arm_points[0][1] - ar, h4),

        (arm_points[0][0] + ar, arm_points[0][1] + ar, h3),
        (arm_points[0][0] + ar, arm_points[0][1] + ar, h4),

        # 48
        (arm_points[1][0] - ar, arm_points[1][1] - ar, h3),
        (arm_points[1][0] - ar, arm_points[1][1] - ar, h4),

        (arm_points[1][0] - ar, arm_points[1][1] + ar, h3),
        (arm_points[1][0] - ar, arm_points[1][1] + ar, h4),

        (arm_points[1][0] + ar, arm_points[1][1] - ar, h3),
        (arm_points[1][0] + ar, arm_points[1][1] - ar, h4),

        (arm_points[1][0] + ar, arm_points[1][1] + ar, h3),
        (arm_points[1][0] + ar, arm_points[1][1] + ar, h4),

        # 56
        (arc_string_x, 0, h3),
        (arc_string_x, 0, h4),

        # 58
        (arm_points[0][0] - ar, arm_points[0][1] + m, h3),
        (arm_points[0][0] - ar, arm_points[0][1] + m, h4),

        (arm_points[0][0] + ar, arm_points[0][1] + m, h3),
        (arm_points[0][0] + ar, arm_points[0][1] + m, h4),

        (arm_points[1][0] - ar, arm_points[1][1] - m, h3),
        (arm_points[1][0] - ar, arm_points[1][1] - m, h4),

        (arm_points[1][0] + ar, arm_points[1][1] - m, h3),
        (arm_points[1][0] + ar, arm_points[1][1] - m, h4),
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

        (58, 59), (60, 61), (62, 63), (64, 65),
        (58, 60), (62, 64), (59, 61), (63, 65),
    ]

    faces = [
        (20, 21, 25, 24), (24, 25, 29, 28), (28, 29, 33, 32), (32, 33, 37, 36),
        (1, 2, 6, 5), (5, 6, 10, 9), (9, 10, 14, 13), (13, 14, 18, 17),
        (22, 23, 27, 26), (26, 27, 31, 30), (30, 31, 35, 34), (34, 35, 39, 38),
        (0, 1, 21, 20), (17, 16, 36, 37),
        (2, 3, 23, 22), (19, 18, 38, 39),
        (4, 0, 20, 24), (8, 4, 24, 28), (12, 8, 28, 32), (16, 12, 32, 36),
        (1, 5, 25, 21), (5, 9, 29, 25), (9, 13, 33, 29), (13, 17, 37, 33),
        (6, 2, 22, 26), (10, 6, 26, 30), (14, 10, 30, 34), (18, 14, 34, 38),
        (3, 7, 27, 23), (7, 11, 31, 27), (11, 15, 35, 31), (15, 19, 39, 35),

        (0, 4, 42, 40),
        (7, 3, 41, 43),

        (12, 16, 50, 48),
        (19, 15, 49, 51),

        (42, 4, 58),
        (7, 43, 59),

        (12, 48, 62),
        (49, 15, 63),

        (8, 58, 4),
        (7, 59, 11),

        (8, 12, 62),
        (15, 11, 63),

        (58, 59, 61, 60),
        (46, 42, 58, 60), (43, 47, 61, 59),

        (63, 62, 64, 65),
        (48, 52, 64, 62), (53, 49, 63, 65),

        (46, 60, 56),
        (47, 57, 61),
        (52, 56, 64),
        (53, 65, 57),

        (60, 61, 57, 56),
        (65, 64, 56, 57),

        (59, 58, 8, 11),
        (62, 63, 11, 8),
    ]

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha = i * max_angle / p
        ca = math.cos(alpha)
        sa = math.sin(alpha)

        beta = i * math.tau / p
        cb = math.cos(beta)
        sb = math.sin(beta)

        vertices.extend([
            (outer_r * ca, outer_r * sa, h4),
            (outer_r * ca, outer_r * sa, h3),

            (outer_r * ca, -outer_r * sa, h4),
            (outer_r * ca, -outer_r * sa, h3),

            (arm_points[0][0] + ar * cb, arm_points[0][1] + ar * sb, h4),
            (arm_points[0][0] + ar * cb, arm_points[0][1] + ar * sb, h3),

            (arm_points[1][0] + ar * cb, arm_points[1][1] + ar * sb, h4),
            (arm_points[1][0] + ar * cb, arm_points[1][1] + ar * sb, h3),
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
                (rtv - nbidx, rtv, 57),
                (rbv, rbv - nbidx, 56),
                (ltv, ltv - nbidx, 57),
                (lbv - nbidx, lbv, 56),
            ])

            if beta < math.pi / 2:
                faces.extend([
                    (rctv, rctv - nbidx, 55),
                    (rcbv - nbidx, rcbv, 54),
                    (lctv, lctv - nbidx, 47),
                    (lcbv - nbidx, lcbv, 46),
                ])
            elif beta < math.pi:
                faces.extend([
                    (rctv, rctv - nbidx, 51),
                    (rcbv - nbidx, rcbv, 50),
                    (lctv, lctv - nbidx, 43),
                    (lcbv - nbidx, lcbv, 42),
                ])
            elif beta < 3 * math.pi / 2:
                faces.extend([
                    (rctv, rctv - nbidx, 49),
                    (rcbv - nbidx, rcbv, 48),
                    (lctv, lctv - nbidx, 41),
                    (lcbv - nbidx, lcbv, 40),
                ])
            else:
                faces.extend([
                    (rctv, rctv - nbidx, 53),
                    (rcbv - nbidx, rcbv, 52),
                    (lctv, lctv - nbidx, 45),
                    (lcbv - nbidx, lcbv, 44),
                ])

    edges.extend([
        (rtv, 19),
        (rbv, 16),
        (ltv, 3),
        (lbv, 0),
    ])

    faces.extend([
        (3, 0, lbv, ltv),
        (16, 19, rtv, rbv),

        (ltv, 45, 41, 3),
        (44, lbv, 0, 40),

        (55, rtv, 19, 51),
        (rbv, 54, 50, 16),
    ])

    if n % 2 == 0:
        faces.extend([
            (ltv, 47, 45),
            (lbv, 44, 46),
            (rtv, 53, 55),
            (rbv, 52, 54),
            (ltv, 57, 47),
            (rtv, 53, 57),
            (lbv, 46, 56),
            (rbv, 56, 52),
        ])
    else:
        faces.extend([
            (45, ltv, 11, 47),
            (rtv, 55, 53, 11),
            (lbv, 44, 46, 8),
            (54, rbv, 8, 52),
        ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh