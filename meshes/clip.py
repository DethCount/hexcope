from optics import hex2xyz
import bpy
import math
from mathutils import Matrix, Vector

clip_name = 'clip'
start_angle = math.pi / 3 + math.pi / 6
arc_angle = 5 * math.pi / 6

# 2 equilateral triangle wide basis
# + 1 triangle row (triangle height = 0.5 * math.sqrt(3) * triangle side)
# + almost half circles centered on next triangle row
# + math.sin(math.pi / 2 - pi / 3) from half circles over triangle row
def get_triangle_side_length(depth, thickness):
    return (depth - thickness) / \
        (3 * 0.5 * math.sqrt(3) + math.sin(math.pi / 6))

def get_triangle_h(triangle_side_length):
    return 0.5 * math.sqrt(3) * triangle_side_length

def get_clip_radius(triangle_side_length):
    return 1.0 * triangle_side_length

# fvi: first vertex index
def create_clip_mesh_data(
    depth, thickness, height, precision, fvi
):
    triangle_side_length = get_triangle_side_length(depth, thickness)
    triangle_h = get_triangle_h(triangle_side_length)

    hs = 0.5 * triangle_side_length
    hh = 0.5 * height

    sx = hs + thickness - triangle_side_length * math.cos(start_angle + arc_angle)

    v_border = Vector((sx, 0, 0))
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
        -v_border + vz,
        -v_border - vz,
        v_border - vz,
        v_border + vz,

        v0 + vz, v1 + vz, v2 + vz, v3 + vz, v4 + vz,
        v0 - vz, v1 - vz, v2 - vz, v3 - vz, v4 - vz,
        v0o + vz, v1o + vz, v2o + vz, v3o + vz, v4o + vz,
        v0o - vz, v1o - vz, v2o - vz, v3o - vz, v4o - vz
    ]

    surface_verts = [fvi, fvi + 1, fvi + 2, fvi + 3]

    nb_verts = len(vertices)

    edges = [
        (fvi, fvi + 1),
        (fvi, fvi + 1),
        (fvi + 1, fvi + 2),
        (fvi + 2, fvi + 3),
        (fvi + 3, fvi),

        (fvi + 4, fvi + 5),
        (fvi + 7, fvi + 8),

        (fvi + 9, fvi + 10),
        (fvi + 12, fvi + 13),

        (fvi + 14, fvi + 15),
        (fvi + 17, fvi + 18),

        (fvi + 19, fvi + 20),
        (fvi + 22, fvi + 23),

        (fvi + 4, fvi + 9),
        (fvi + 8, fvi + 13),

        (fvi + 9, fvi + 19),
        (fvi + 13, fvi + 23),

        (fvi + 19, fvi + 14),
        (fvi + 23, fvi + 18),

        (fvi + 14, fvi + 4),
        (fvi + 18, fvi + 8),
    ]

    faces = [
        (fvi + 1, fvi, fvi + 14, fvi + 19),
        (fvi + 3, fvi + 2, fvi + 23, fvi + 18),
        (fvi + 9, fvi + 4, fvi + 8, fvi + 13),

        (fvi + 4, fvi + 9, fvi + 19, fvi + 14),
        (fvi + 8, fvi + 13, fvi + 23, fvi + 18),

        (fvi + 4, fvi + 5, fvi + 15, fvi + 14),
        (fvi + 14, fvi + 15, fvi + 20, fvi + 19),
        (fvi + 19, fvi + 20, fvi + 10, fvi + 9),
        (fvi + 9, fvi + 10, fvi + 5, fvi + 4),

        (fvi + 7, fvi + 8, fvi + 18, fvi + 17),
        (fvi + 17, fvi + 18, fvi + 23, fvi + 22),
        (fvi + 22, fvi + 23, fvi + 13, fvi + 12),
        (fvi + 12, fvi + 13, fvi + 8, fvi + 7),
    ]

    c1 = (-hs, 2 * triangle_h)
    c2 = (hs, 2 * triangle_h)

    r = get_clip_radius(triangle_side_length)
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
        nvi = fvi + nb_verts
        idx = nvi + i * nbidx

        if i > 0:
            edges.extend([
                (idx - nbidx, idx),
                (idx + 1 - nbidx, idx + 1),
                (idx + 4 - nbidx, idx + 4),
                (idx + 5 - nbidx, idx + 5),
            ])

            faces.extend([
                (idx - nbidx, idx, idx + 1, idx + 1 - nbidx),
                (idx + 4, idx + 4 - nbidx, idx + 5 - nbidx, idx + 5),
            ])

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

                    (idx + 5, idx + 5 - nbidx, idx + 6 - nbidx, idx + 6),
                    (idx + 6, idx + 6 - nbidx, idx + 7 - nbidx, idx + 7),
                    (idx + 7, idx + 7 - nbidx, idx + 4 - nbidx, idx + 4),
                ])
            else:
                if max_idx == None:
                    max_idx = idx - nbidx
                    faces.extend([
                        #(idx, idx + 1, max_idx + 3, max_idx + 2),
                        #(idx + 4, idx + 5, max_idx + 7, max_idx + 6),
                    ])

                faces.extend([
                    (idx + 1 - nbidx, idx + 1, max_idx + 2, max_idx + 2 - nbidx),
                    (max_idx + 3 - nbidx, max_idx + 3, idx, idx - nbidx),

                    (idx + 5, idx + 5 - nbidx, max_idx + 6 - nbidx, max_idx + 6),
                    (max_idx + 7, max_idx + 7 - nbidx, idx + 4 - nbidx, idx + 4),
                ])

            if i == precision and max_idx != None:
                edges.extend([
                    (idx, fvi + 5),
                    (idx + 1, fvi + 10),
                    (max_idx + 2, fvi + 20),
                    (max_idx + 3, fvi + 15),

                    (idx + 4, fvi + 7),
                    (idx + 5, fvi + 12),
                    (max_idx + 6, fvi + 22),
                    (max_idx + 7, fvi + 17),

                    (nvi, fvi + 6),
                    (nvi + 1, fvi + 11),
                    (nvi + 2, fvi + 21),
                    (nvi + 3, fvi + 16),

                    (nvi + 4, fvi + 6),
                    (nvi + 5, fvi + 11),
                    (nvi + 6, fvi + 21),
                    (nvi + 7, fvi + 16),
                ])

                faces.extend([
                    (idx, fvi + 5, fvi + 15, max_idx + 3),
                    (fvi + 15, max_idx + 3, max_idx + 2, fvi + 20),
                    (max_idx + 2, fvi + 20, fvi + 10, idx + 1),
                    (idx + 1, fvi + 10, fvi + 5, idx),

                    (idx + 4, fvi + 7, fvi + 17, max_idx + 7),
                    (max_idx + 7, fvi + 17, fvi + 22, max_idx + 6),
                    (max_idx + 6, fvi + 22, fvi + 12, idx + 5),
                    (idx + 5, fvi + 12, fvi + 7, idx + 4),

                    (fvi + 6, nvi, nvi + 1, fvi + 11),
                    (fvi + 11, nvi + 1, nvi + 2, fvi + 21),
                    (fvi + 21, nvi + 2, nvi + 3, fvi + 16),
                    (fvi + 16, nvi + 3, nvi, fvi + 6),

                    (nvi + 4, fvi + 6, fvi + 11, nvi + 5),
                    (nvi + 5, fvi + 11, fvi + 21, nvi + 6),
                    (nvi + 6, fvi + 21, fvi + 16, nvi + 7),
                    (nvi + 7, fvi + 16, fvi + 6, nvi + 4),
                ])

    return [vertices, edges, faces, surface_verts]

def create_clip_hole_mesh_data(depth, thickness, height, fvi):
    triangle_side_length = get_triangle_side_length(depth, thickness)
    triangle_h = get_triangle_h(triangle_side_length)

    hs = 0.5 * triangle_side_length
    hh = 0.5 * height

    sx = hs + thickness - triangle_side_length * math.cos(start_angle + arc_angle)
    sx2 = sx + triangle_side_length * math.cos(math.pi - arc_angle)

    y1 = -triangle_h
    y2 = -depth

    vertices = [
        Vector((-sx, 0, hh)),
        Vector((-sx, 0, -hh)),
        Vector((sx, 0, -hh)),
        Vector((sx, 0, hh)),

        Vector((-sx, y1, hh)),
        Vector((-sx, y1, -hh)),
        Vector((sx, y1, -hh)),
        Vector((sx, y1, hh)),

        Vector((-sx2, y1, hh)),
        Vector((-sx2, y1, -hh)),
        Vector((sx2, y1, -hh)),
        Vector((sx2, y1, hh)),

        Vector((-sx2, y2, hh)),
        Vector((-sx2, y2, -hh)),
        Vector((sx2, y2, -hh)),
        Vector((sx2, y2, hh)),
    ]

    surface_verts = [fvi, fvi + 1, fvi + 2, fvi + 3]

    edges = [
        (fvi, fvi + 1),
        (fvi + 1, fvi + 2),
        (fvi + 2, fvi + 3),
        (fvi + 3, fvi),

        (fvi + 4, fvi + 5),
        (fvi + 5, fvi + 6),
        (fvi + 6, fvi + 7),
        (fvi + 7, fvi + 4),

        (fvi + 8, fvi + 9),
        (fvi + 9, fvi + 10),
        (fvi + 10, fvi + 11),
        (fvi + 11, fvi + 8),

        (fvi + 12, fvi + 13),
        (fvi + 13, fvi + 14),
        (fvi + 14, fvi + 15),
        (fvi + 15, fvi + 12),

        (fvi, fvi + 4),
        (fvi + 1, fvi + 5),
        (fvi + 2, fvi + 6),
        (fvi + 3, fvi + 7),

        (fvi + 4, fvi + 8),
        (fvi + 5, fvi + 9),
        (fvi + 6, fvi + 10),
        (fvi + 7, fvi + 11),

        (fvi + 8, fvi + 12),
        (fvi + 9, fvi + 13),
        (fvi + 10, fvi + 14),
        (fvi + 11, fvi + 15),
    ]

    faces = [
        (fvi, fvi + 4, fvi + 5, fvi + 1),
        (fvi + 1, fvi + 5, fvi + 6, fvi + 2),
        (fvi + 2, fvi + 6, fvi + 7, fvi + 3),
        (fvi + 3, fvi + 7, fvi + 4, fvi),

        (fvi + 4, fvi + 8, fvi + 9, fvi + 5),
        (fvi + 5, fvi + 9, fvi + 10, fvi + 6),
        (fvi + 6, fvi + 10, fvi + 11, fvi + 7),
        (fvi + 7, fvi + 11, fvi + 8, fvi + 4),

        (fvi + 8, fvi + 12, fvi + 13, fvi + 9),
        (fvi + 9, fvi + 13, fvi + 14, fvi + 10),
        (fvi + 10, fvi + 14, fvi + 15, fvi + 11),
        (fvi + 11, fvi + 15, fvi + 12, fvi + 8),

        (fvi + 13, fvi + 12, fvi + 15, fvi + 14),
    ]

    return [vertices, edges, faces, surface_verts]

def is_clip_face(face, w_l):
    return (face.z % 2 == 0 and w_l != 0) or w_l == 2


# surface_indices: expected (tl, bl, br, tr)
def get_clip(
    depth,
    thickness,
    height,
    precision,
    face,
    fvi = 0,
    face_w_l = 1,
    position = None,
    angle = None,
    axis = None
):
    vertices = []
    edges = []
    faces = []

    surface = []

    if is_clip_face(face, face_w_l):
        ret = create_clip_mesh_data(depth, thickness, height, precision, fvi)
        vertices.extend(ret[0])
        edges.extend(ret[1])
        faces.extend(ret[2])
        surface = ret[3]
    else:
        ret = create_clip_hole_mesh_data(depth, thickness, height, fvi)
        vertices.extend(ret[0])
        edges.extend(ret[1])
        faces.extend(ret[2])
        surface = ret[3]

    if (angle != None and axis != None) or position != None:
        for i in range(0, len(vertices)):
            if (angle != None and axis != None):
                vertices[i] = Matrix.Rotation(angle, 3, axis) @ vertices[i]
            if position != None:
                vertices[i] += position

    return [vertices, edges, faces, surface]