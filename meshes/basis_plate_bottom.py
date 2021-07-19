import bpy
import math

basis_plate_bottom_name = 'basis_plate_bottom'

def create_mesh(
    e, t, r, sr, p, x, z,
    hex_side,
    top_plate_thickness
):
    mesh = bpy.data.meshes.new(
        basis_plate_bottom_name
        + '_' + str((
            e, t, r, sr, p, x, z,
            hex_side,
            top_plate_thickness
        ))
    )

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