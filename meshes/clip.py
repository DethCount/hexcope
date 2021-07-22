import bpy
import math
from mathutils import Vector

clip_name = 'clip'

def create_mesh(depth, thickness, height, precision):
    mesh = bpy.data.meshes.new(clip_name + str((
        depth, thickness, height, precision
    )))

    # 2 equilateral triangle wide basis
    # + 1 triangle row (triangle height = 0.5 * math.sqrt(3) * triangle side)
    # + almost half circles centered on next triangle row
    # + math.sin(math.pi / 2 - pi / 3) from half circles over triangle row
    triangle_side_length = depth / \
        (3 * math.sqrt(3) / 2 + math.sin(math.pi / 6))

    triangle_h = 0.5 * math.sqrt(3) * triangle_side_length
    start_angle = math.pi / 3 + math.pi / 6
    arc_angle = 5 * math.pi / 6
    hs = 0.5 * triangle_side_length
    hh = 0.5 * height

    vt = Vector((thickness, 0, 0))
    vz = Vector((0, 0, hh))

    v0 = Vector((-hs, 0, 0))
    v1 = Vector((-triangle_side_length, triangle_h, 0))
    v2 = Vector((0, 2 * triangle_h, 0))
    v3 = Vector((triangle_side_length, triangle_h, 0))
    v4 = Vector((hs, 0, 0))

    v0o = v0 - vt
    v1o = v1 - vt
    v2o = v2 + Vector((0, thickness, 0))
    v3o = v3 + vt
    v4o = v4 + vt

    vertices = [
        v0 + vz, v1 + vz, v2 + vz, v3 + vz, v4 + vz,
        v0 - vz, v1 - vz, v2 - vz, v3 - vz, v4 - vz,
        v0o + vz, v1o + vz, v2o + vz, v3o + vz, v4o + vz,
        v0o - vz, v1o - vz, v2o - vz, v3o - vz, v4o - vz
    ]
    edges = [
        (0, 1), (0, 1), (3, 4),
        (5, 6), (8, 9),
        (10, 11), (13, 14),
        (15, 16), (18, 19),

        (0, 5), (4, 9),
        (5, 10), (9, 14),
        (10, 15), (14, 19),
        (15, 0), (19, 4),
    ]
    faces = [
        (0, 5, 10, 15),
        (4, 9, 14, 19),
        (0, 1, 11, 10), (10, 11, 16, 15), (15, 16, 6, 5), (5, 6, 1, 0),
        (3, 4, 14, 13), (13, 14, 19, 18), (18, 19, 9, 8), (8, 9, 4, 3),
    ]

    c1 = (-hs, 2 * triangle_h)
    c2 = (hs, 2 * triangle_h)
    nb_verts = len(vertices)

    r = 0.75 * triangle_side_length
    ro = r + thickness
    min_y = c1[1] + r * math.sin(start_angle + arc_angle)
    max_idx = None
    for i in range(0, precision + 1):
        alpha = start_angle + i * arc_angle / precision
        c = math.cos(alpha)
        s = math.sin(alpha)

        x = r * c
        y = r * s
        xo = ro * c
        yo = ro * s

        vi = Vector((
            c1[0] + x,
            c1[1] + y,
            0
        ))

        vio = Vector((
            c1[0] + xo,
            c1[1] + yo,
            0
        ))

        vim = Vector((
            c2[0] - x,
            c2[1] + y,
            0
        ))

        vimo = Vector((
            c2[0] - xo,
            c2[1] + yo,
            0
        ))

        verts = [
            vi + vz, vi - vz, vio - vz, vio + vz,
            vim + vz, vim - vz, vimo - vz, vimo + vz
        ]
        vertices.extend(verts)

        nbidx = 8
        idx = nb_verts + i * nbidx

        if i > 0:
            edges.extend([
                (idx - nbidx, idx),
                (idx + 1 - nbidx, idx + 1),
                (idx + 4 - nbidx, idx + 4),
                (idx + 5 - nbidx, idx + 5),
            ])

            faces.extend([
                (idx - nbidx, idx, idx + 1, idx + 1 - nbidx),
                (idx + 4 - nbidx, idx + 4, idx + 5, idx + 5 - nbidx),
            ])

            print(str(vio[1]), str(min_y))

            if vio[1] > min_y:
                edges.extend([
                    (idx + 2 - nbidx, idx + 2),
                    (idx + 3 - nbidx, idx + 3),
                    (idx + 6 - nbidx, idx + 6),
                    (idx + 7 - nbidx, idx + 7),
                ])

                faces.extend([
                    (idx + 1 - nbidx, idx + 1, idx + 2, idx + 2 - nbidx),
                    (idx + 2 - nbidx, idx + 2, idx + 3, idx + 3 - nbidx),
                    (idx + 3 - nbidx, idx + 3, idx, idx - nbidx),

                    (idx + 5 - nbidx, idx + 5, idx + 6, idx + 6 - nbidx),
                    (idx + 6 - nbidx, idx + 6, idx + 7, idx + 7 - nbidx),
                    (idx + 7 - nbidx, idx + 7, idx + 4, idx + 4 - nbidx),
                ])
            else:
                print('max_idx', idx)
                if max_idx == None:
                    max_idx = idx - nbidx
                    faces.extend([
                        (idx, idx + 1, max_idx + 3, max_idx + 2),
                        (idx + 4, idx + 5, max_idx + 7, max_idx + 6),
                    ])

                faces.extend([
                    (idx + 1 - nbidx, idx + 1, max_idx + 2, max_idx + 2 - nbidx),
                    (max_idx + 3 - nbidx, max_idx + 3, idx, idx - nbidx),

                    (idx + 5 - nbidx, idx + 5, max_idx + 6, max_idx + 6 - nbidx),
                    (max_idx + 7 - nbidx, max_idx + 7, idx + 4, idx + 4 - nbidx),
                ])

            if i == precision and max_idx != None:
                edges.extend([
                    (idx, 1),
                    (idx + 1, 6),
                    (max_idx + 2, 16),
                    (max_idx + 3, 11),

                    (idx + 4, 3),
                    (idx + 5, 8),
                    (max_idx + 6, 18),
                    (max_idx + 7, 13),

                    (nb_verts, 2),
                    (nb_verts + 1, 7),
                    (nb_verts + 2, 17),
                    (nb_verts + 3, 12),

                    (nb_verts + 4, 2),
                    (nb_verts + 5, 7),
                    (nb_verts + 6, 17),
                    (nb_verts + 7, 12),
                ])

                faces.extend([
                    (idx, 1, 11, max_idx + 3),
                    (max_idx + 3, 11, 16, max_idx + 2),
                    (max_idx + 2, 16, 6, idx + 1),
                    (idx + 1, 6, 1, idx),

                    (idx + 4, 3, 13, max_idx + 7),
                    (max_idx + 7, 13, 18, max_idx + 6),
                    (max_idx + 6, 18, 8, idx + 5),
                    (idx + 5, 8, 3, idx + 4),

                    (nb_verts, 2, 7, nb_verts + 1),
                    (nb_verts + 1, 7, 17, nb_verts + 2),
                    (nb_verts + 2, 17, 12, nb_verts + 3),
                    (nb_verts + 3, 12, 2, nb_verts),

                    (nb_verts + 4, 2, 7, nb_verts + 5),
                    (nb_verts + 5, 7, 17, nb_verts + 6),
                    (nb_verts + 6, 17, 12, nb_verts + 7),
                    (nb_verts + 7, 12, 2, nb_verts + 4),
                ])



    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh