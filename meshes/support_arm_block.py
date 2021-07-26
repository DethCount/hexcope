import bpy
import math
from mathutils import Vector

from optics import get_support_arm_point, hex2xy, hex2xyz
from meshes import half_hex

support_arm_block_name = 'support_arm_block'

# todo: thicker nose part
# wl : wing length: v4 distance from v3 along v35
def create_mesh(
    e, f, n, r, t, m, wl, p,
    hex_thickness, hex_interior_thickness, hex_walls_height,
    primary_thickness,
    arm_radius,
    clip_depth, clip_thickness, clip_height, clip_precision
):
    mesh = bpy.data.meshes.new(
        support_arm_block_name
        + '_' + str((
            e, f, n, r, t, m, wl, p,
            hex_thickness, hex_interior_thickness, hex_walls_height,
            primary_thickness,
            arm_radius,
            clip_depth, clip_thickness, clip_height, clip_precision
        ))
    )

    arm_points = get_support_arm_point(n, r, m, 0)

    fit = hex_thickness + hex_interior_thickness

    if n % 2 == 0:
        face_l = Vector((0.5 * n + 1, 0, 3))
        face_r = Vector((face_l.x, face_l.y, 2))

        p5 = Vector(hex2xyz(f, r, face_r.x - 1, face_r.y + 1, 0, 2))
        p2o = Vector(hex2xyz(f, r, face_r.x - 1, face_r.y + 1, 4, 1))
        p3o = Vector(hex2xyz(f, r, face_r.x - 1, face_r.y + 1, 5, 0))
    else:
        face_l = Vector((math.ceil(0.5 * n) + 1, -1, 2))
        face_r = Vector((face_l.x - 1, face_l.y + 2, 3))

        p5 = Vector(hex2xyz(f, r, face_r.x - 1, face_r.y + 1, 0, 1))
        p2o = Vector(hex2xyz(f, r, face_r.x, face_r.y - 1, 0, 0))
        p3o = Vector(hex2xyz(f, r, face_r.x, face_r.y - 1, 1, 2))

    p2 = Vector(hex2xyz(f, r, face_r.x, face_r.y, face_r.z, 2))
    p3 = Vector(hex2xyz(f, r, face_r.x, face_r.y, face_r.z, 1))

    v2on = (p2o - p2).normalized()
    v3on = (p3o - p3).normalized()
    v35n = (p5 - p3).normalized()
    v1on = Vector((v3on.x, -v3on.y, v3on.z))
    v0on = v1on
    v4on = v3on
    p4 = p3 + v35n * wl

    outer_r = max(
        p2.x + m,
        math.sqrt((arm_points[0][0] + m) ** 2 + p4.y ** 2)
    )
    max_angle = math.asin(p4.y / outer_r)
    arc_string_x = outer_r * math.cos(max_angle)

    hex_total_thickness = hex_thickness + hex_walls_height + primary_thickness
    z_displacement = -(hex_total_thickness - primary_thickness)

    v0 = Vector((p4.x, -p4.y, p4.z + z_displacement))
    v1 = Vector((p3.x, -p3.y, p3.z + z_displacement))
    v2 = Vector((p2.x, p2.y, p2.z + z_displacement))
    v3 = Vector((p3.x, p3.y, p3.z + z_displacement))
    v4 = Vector((p4.x, p4.y, p4.z + z_displacement))

    v12 = v2 - v1
    v23 = v3 - v2
    v12mid = v2 - 0.5 * v12
    v23mid = v2 + 0.5 * v23

    v0o = v0 + v0on * fit
    v1o = v1 + v1on * fit
    v2o = v2 + v2on * fit
    v3o = v3 + v3on * fit
    v4o = v4 + v4on * fit

    h0 = t
    h1 = h0 + hex_total_thickness
    h2 = h1 + t
    h3 = min(v2.z, v3.z, v4.z)
    h4 = max(v2.z, v3.z, v4.z) + h2
    h5 = h0 + hex_walls_height

    vh5 = Vector((0, 0, h5))

    ar = arm_radius + 0.5 * e

    vertices = [
        (v0.x, v0.y, h3),
        (v0.x, v0.y, v0.z + h0),
        (v0.x, v0.y, v0.z + h1),
        (v0.x, v0.y, h4),

        (v1.x, v1.y, h3),
        (v1.x, v1.y, v1.z + h0),
        (v1.x, v1.y, v1.z + h5),
        (v1.x, v1.y, v1.z + h1),
        (v1.x, v1.y, h4),

        # 9
        (v2.x, v2.y, h3),
        (v2.x, v2.y, v2.z + h0),
        (v2.x, v2.y, v2.z + h5),
        (v2.x, v2.y, v2.z + h1),
        (v2.x, v2.y, h4),

        (v3.x, v3.y, h3),
        (v3.x, v3.y, v3.z + h0),
        (v3.x, v3.y, v3.z + h5),
        (v3.x, v3.y, v3.z + h1),
        (v3.x, v3.y, h4),

        # 19
        (v4.x, v4.y, h3),
        (v4.x, v4.y, v4.z + h0),
        (v4.x, v4.y, v4.z + h1),
        (v4.x, v4.y, h4),

        # 23
        (v0o.x, v0o.y, v0o.z),
        (v0o.x, v0o.y, v0o.z + h0),
        (v0o.x, v0o.y, v0o.z + h1),
        (v0o.x, v0o.y, v0o.z + h2),

        (v1o.x, v1o.y, v1o.z),
        (v1o.x, v1o.y, v1o.z + h0),
        (v1o.x, v1o.y, v1o.z + h1),
        (v1o.x, v1o.y, v1o.z + h2),

        # 31
        (v2o.x, v2o.y, v2o.z),
        (v2o.x, v2o.y, v2o.z + h0),
        (v2o.x, v2o.y, v2o.z + h1),
        (v2o.x, v2o.y, v2o.z + h2),

        (v3o.x, v3o.y, v3o.z),
        (v3o.x, v3o.y, v3o.z + h0),
        (v3o.x, v3o.y, v3o.z + h1),
        (v3o.x, v3o.y, v3o.z + h2),

        # 39
        (v4o.x, v4o.y, v4o.z),
        (v4o.x, v4o.y, v4o.z + h0),
        (v4o.x, v4o.y, v4o.z + h1),
        (v4o.x, v4o.y, v4o.z + h2),

        # 43
        (arm_points[0][0] - ar, arm_points[0][1] - ar, h3),
        (arm_points[0][0] - ar, arm_points[0][1] - ar, h4),

        (arm_points[0][0] - ar, arm_points[0][1] + ar, h3),
        (arm_points[0][0] - ar, arm_points[0][1] + ar, h4),

        (arm_points[0][0] + ar, arm_points[0][1] - ar, h3),
        (arm_points[0][0] + ar, arm_points[0][1] - ar, h4),

        (arm_points[0][0] + ar, arm_points[0][1] + ar, h3),
        (arm_points[0][0] + ar, arm_points[0][1] + ar, h4),

        # 51
        (arm_points[1][0] - ar, arm_points[1][1] - ar, h3),
        (arm_points[1][0] - ar, arm_points[1][1] - ar, h4),

        (arm_points[1][0] - ar, arm_points[1][1] + ar, h3),
        (arm_points[1][0] - ar, arm_points[1][1] + ar, h4),

        (arm_points[1][0] + ar, arm_points[1][1] - ar, h3),
        (arm_points[1][0] + ar, arm_points[1][1] - ar, h4),

        (arm_points[1][0] + ar, arm_points[1][1] + ar, h3),
        (arm_points[1][0] + ar, arm_points[1][1] + ar, h4),

        # 59
        (arc_string_x, 0, h3),
        (arc_string_x, 0, h4),

        # 61
        (arm_points[0][0] - ar, arm_points[0][1] + m, h3),
        (arm_points[0][0] - ar, arm_points[0][1] + m, h4),

        (arm_points[0][0] + ar, arm_points[0][1] + m, h3),
        (arm_points[0][0] + ar, arm_points[0][1] + m, h4),

        (arm_points[1][0] - ar, arm_points[1][1] - m, h3),
        (arm_points[1][0] - ar, arm_points[1][1] - m, h4),

        (arm_points[1][0] + ar, arm_points[1][1] - m, h3),
        (arm_points[1][0] + ar, arm_points[1][1] - m, h4),

        # 69
        (v2.x + hex_thickness, v2.y, h3),
        (v2.x + hex_thickness, v2.y, h4),

        # 71
        (arm_points[0][0] - ar + hex_thickness, arm_points[0][1] + m, h3),
        (arm_points[0][0] - ar + hex_thickness, arm_points[0][1] + m, h4),

        (arm_points[1][0] - ar + hex_thickness, arm_points[1][1] - m, h3),
        (arm_points[1][0] - ar + hex_thickness, arm_points[1][1] - m, h4),
    ]

    edges = [
        (0, 3),
        (0, 3),
        (4, 8),
        (9, 13),
        (14, 18),
        (19, 22),
        (0, 4), (4, 9), (9, 14), (14, 19),
        (3, 8), (8, 13), (13, 18), (18, 22),

        (0, 23), (4, 27), (9, 31), (14, 35), (19, 39),
        (1, 24), (5, 28), (10, 32), (15, 36), (20, 40),
        (2, 25), (7, 29), (12, 33), (17, 37), (21, 41),
        (3, 26), (8, 30), (13, 34), (18, 38), (22, 42),

        (23, 24), (27, 28), (31, 32), (35, 36), (39, 40),
        (25, 26), (29, 30), (33, 34), (37, 38), (41, 42),

        (23, 27), (27, 31), (31, 35), (35, 39),
        (24, 28), (28, 32), (32, 36), (36, 40),
        (25, 29), (29, 33), (33, 37), (37, 41),
        (26, 30), (30, 34), (34, 38), (38, 42),

        (61, 62), (63, 64), (65, 66), (67, 68),
        (71, 63), (73, 67), (72, 64), (74, 68),
    ]

    faces = [
        (23, 24, 28, 27), (27, 28, 32, 31), (31, 32, 36, 35), (35, 36, 40, 39),
        (1, 2, 7, 5),
        (6, 7, 12, 11),
        (11, 12, 17, 16),
        (15, 17, 21, 20),
        (25, 26, 30, 29), (29, 30, 34, 33), (33, 34, 38, 37), (37, 38, 42, 41),
        (0, 1, 24, 23), (20, 19, 39, 40),
        (2, 3, 26, 25), (22, 21, 41, 42),
        (4, 0, 23, 27), (9, 4, 27, 31), (14, 9, 31, 35), (19, 14, 35, 39),
        (1, 5, 28, 24), (5, 10, 32, 28), (10, 15, 36, 32), (15, 20, 40, 36),
        (7, 2, 25, 29), (12, 7, 29, 33), (17, 12, 33, 37), (21, 17, 37, 41),
        (3, 8, 30, 26), (8, 13, 34, 30), (13, 18, 38, 34), (18, 22, 42, 38),

        (0, 4, 45, 43),
        (8, 3, 44, 46),

        (14, 19, 53, 51),
        (22, 18, 52, 54),

        (45, 4, 61),
        (8, 46, 62),

        (14, 51, 65),
        (52, 18, 66),

        (49, 45, 61, 63), (46, 50, 64, 62),
        (51, 55, 67, 65), (56, 52, 66, 68),

        (63, 64, 60, 59),
        (68, 67, 59, 60),

        (49, 63, 59),
        (50, 60, 64),
        (55, 59, 67),
        (56, 68, 60),

        (69, 70, 72, 71),
        (70, 69, 73, 74),
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
                (rtv - nbidx, rtv, 60),
                (rbv, rbv - nbidx, 59),
                (ltv, ltv - nbidx, 60),
                (lbv - nbidx, lbv, 59),
            ])

            if beta < math.pi / 2:
                faces.extend([
                    (rctv, rctv - nbidx, 58),
                    (rcbv - nbidx, rcbv, 57),
                    (lctv, lctv - nbidx, 50),
                    (lcbv - nbidx, lcbv, 49),
                ])
            elif beta < math.pi:
                faces.extend([
                    (rctv, rctv - nbidx, 54),
                    (rcbv - nbidx, rcbv, 53),
                    (lctv, lctv - nbidx, 46),
                    (lcbv - nbidx, lcbv, 45),
                ])
            elif beta < 3 * math.pi / 2:
                faces.extend([
                    (rctv, rctv - nbidx, 52),
                    (rcbv - nbidx, rcbv, 51),
                    (lctv, lctv - nbidx, 44),
                    (lcbv - nbidx, lcbv, 43),
                ])
            else:
                faces.extend([
                    (rctv, rctv - nbidx, 56),
                    (rcbv - nbidx, rcbv, 55),
                    (lctv, lctv - nbidx, 48),
                    (lcbv - nbidx, lcbv, 47),
                ])

    edges.extend([
        (rtv, 22),
        (rbv, 19),
        (ltv, 3),
        (lbv, 0),
    ])

    faces.extend([
        (3, 0, lbv, ltv),
        (19, 22, rtv, rbv),

        (ltv, 48, 44, 3),
        (47, lbv, 0, 43),

        (58, rtv, 22, 54),
        (rbv, 57, 53, 19),
    ])

    if n % 2 == 0:
        faces.extend([
            (69, 61, 4, 9),
            (8, 62, 70, 13),

            (9, 14, 65, 69),
            (18, 13, 70, 66),

            (61, 62, 64, 63),
            (66, 65, 67, 68),

            (61, 69, 71),
            (62, 72, 70),
            (65, 73, 69),
            (66, 70, 74),

            (ltv, 50, 48),
            (lbv, 47, 49),
            (rtv, 58, 56),
            (rbv, 55, 57),
            (ltv, 60, 50),
            (rtv, 56, 60),
            (lbv, 49, 59),
            (rbv, 59, 55),
        ])
    else:
        faces.extend([
            (9, 69, 71, 61),
            (70, 13, 62, 72),

            (69, 9, 65, 73),
            (13, 70, 74, 66),

            (64, 63, 71, 72),
            (67, 68, 74, 73),

            (48, ltv, 60, 50),
            (rtv, 58, 56, 60),
            (lbv, 47, 49, 59),
            (57, rbv, 59, 55),
        ])

    ret = half_hex.create_clip_face(
        f,
        r,
        clip_depth,
        clip_thickness,
        clip_height,
        clip_precision,
        face_l,
        hex_walls_height,
        1,
        len(vertices),
        v12mid + vh5
    )
    vertices.extend(ret[0])
    edges.extend(ret[1])
    faces.extend(ret[2])

    ret = half_hex.create_clip_face(
        f,
        r,
        clip_depth,
        clip_thickness,
        clip_height,
        clip_precision,
        face_r,
        hex_walls_height,
        1,
        len(vertices),
        v23mid + vh5
    )
    vertices.extend(ret[0])
    edges.extend(ret[1])
    faces.extend(ret[2])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh