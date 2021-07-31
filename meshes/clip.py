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
    e, depth, thickness, height, fvi, is_left_clip = True
):
    triangle_side_length = get_triangle_side_length(depth, thickness)
    triangle_h = get_triangle_h(triangle_side_length)

    hs = 0.5 * triangle_side_length
    hh = 0.5 * height

    dx = hs - e - triangle_side_length * math.cos(start_angle + arc_angle)
    sx = dx + thickness

    v_border = Vector((sx, 0, 0))
    vt = Vector((thickness, 0, 0))
    vz = Vector((0, 0, hh))

    mul = 1 if is_left_clip else -1

    v0 = Vector((mul * -dx, 0, 0))
    v1 = Vector((mul * -dx, triangle_h, 0))
    v2 = Vector((mul * -dx, depth - 0.5 * e, 0))

    v0o = v0 - mul * vt
    v1ol = v1 - mul * 2 * vt
    v1or = v1 - mul * vt
    v2o = v2 - mul * vt

    vertices = [
        -v_border + vz,
        -v_border - vz,
        v_border - vz,
        v_border + vz,

        # 4
        v0 + vz, v1 + vz, v2 + vz,

        # 7
        v0 - vz, v1 - vz, v2 - vz,

        # 10
        v0o + vz, v1ol + vz, v1or + vz, v2o + vz,

        # 14
        v0o - vz, v1ol - vz, v1or - vz, v2o - vz,
    ]

    surface_verts = [fvi, fvi + 1, fvi + 2, fvi + 3]

    edges = [
        (fvi, fvi + 1),
        (fvi, fvi + 1),
        (fvi + 1, fvi + 2),
        (fvi + 2, fvi + 3),
        (fvi + 3, fvi),

        (fvi + 10, fvi + 12), (fvi + 12, fvi + 11), (fvi + 11, fvi + 13), (fvi + 13, fvi + 6),
        (fvi + 6, fvi + 5), (fvi + 5, fvi + 4),

        (fvi + 14, fvi + 16), (fvi + 16, fvi + 15), (fvi + 15, fvi + 17), (fvi + 17, fvi + 9),
        (fvi + 9, fvi + 8), (fvi + 8, fvi + 7),
    ]

    faces = []
    if is_left_clip:
        faces.extend([
            (fvi + 4, fvi + 3, fvi + 2, fvi + 7),

            (fvi + 12, fvi + 10, fvi + 4, fvi + 5),
            (fvi + 11, fvi + 5, fvi + 6, fvi + 13),

            (fvi + 14, fvi + 16, fvi + 8, fvi + 7),
            (fvi + 8, fvi + 15, fvi + 17, fvi + 9),

            (fvi + 10, fvi + 12, fvi + 16, fvi + 14),
            (fvi + 12, fvi + 11, fvi + 15, fvi + 16),
            (fvi + 11, fvi + 13, fvi + 17, fvi + 15),
            (fvi + 13, fvi + 6, fvi + 9, fvi + 17),
            (fvi + 6, fvi + 5, fvi + 8, fvi + 9),
            (fvi + 5, fvi + 4, fvi + 7, fvi + 8),
        ])
    else:
        faces.extend([
            (fvi, fvi + 4, fvi + 7, fvi + 1),

            (fvi + 10, fvi + 12, fvi + 5, fvi + 4),
            (fvi + 5, fvi + 11, fvi + 13, fvi + 6),

            (fvi + 16, fvi + 14, fvi + 7, fvi + 8),
            (fvi + 15, fvi + 8, fvi + 9, fvi + 17),

            (fvi + 12, fvi + 10, fvi + 14, fvi + 16),
            (fvi + 11, fvi + 12, fvi + 16, fvi + 15),
            (fvi + 13, fvi + 11, fvi + 15, fvi + 17),
            (fvi + 6, fvi + 13, fvi + 17, fvi + 9),
            (fvi + 5, fvi + 6, fvi + 9, fvi + 8),
            (fvi + 4, fvi + 5, fvi + 8, fvi + 7),
        ])

    return [vertices, edges, faces, surface_verts]

def create_clip_hole_mesh_data(e, depth, thickness, height, fvi, is_left_clip = True):
    triangle_side_length = get_triangle_side_length(depth, thickness)
    triangle_h = get_triangle_h(triangle_side_length)

    hs = 0.5 * triangle_side_length
    hh = 0.5 * (height + e)

    sx = hs + thickness - triangle_side_length * math.cos(start_angle + arc_angle)
    sx2 = sx + triangle_side_length * math.cos(math.pi - arc_angle)

    y1 = -triangle_h + 0.5 * e
    y2 = -depth

    mul = 1 if is_left_clip else -1

    vertices = [
        Vector((mul * -sx, 0, hh)),
        Vector((mul * -sx, 0, -hh)),

        Vector((mul * sx2, 0, hh)),
        Vector((mul * sx2, 0, -hh)),

        Vector((mul * -sx, y1, hh)),
        Vector((mul * -sx, y1, -hh)),

        Vector((mul * -sx2, y1, hh)),
        Vector((mul * -sx2, y1, -hh)),

        Vector((mul * -sx2, y2, hh)),
        Vector((mul * -sx2, y2, -hh)),

        Vector((0, y2, hh)),
        Vector((0, y2, -hh)),
    ]

    edges = [
        (fvi, fvi + 1),
        (fvi, fvi + 1),
        (fvi + 1, fvi + 3),
        (fvi + 3, fvi + 2),
        (fvi + 2, fvi),

        (fvi + 4, fvi + 5),
        (fvi + 6, fvi + 7),
        (fvi + 8, fvi + 9),
        (fvi + 10, fvi + 11),

        (fvi, fvi + 4),
        (fvi + 4, fvi + 6),
        (fvi + 6, fvi + 8),
        (fvi + 8, fvi + 10),
        (fvi + 10, fvi + 2),

        (fvi + 1, fvi + 5),
        (fvi + 5, fvi + 7),
        (fvi + 7, fvi + 9),
        (fvi + 9, fvi + 11),
        (fvi + 11, fvi + 3),
    ]

    faces = []

    if is_left_clip:
        surface_verts = [fvi, fvi + 1, fvi + 3, fvi + 2]

        faces.extend([

            (fvi + 1, fvi, fvi + 4, fvi + 5),
            (fvi + 5, fvi + 4, fvi + 6, fvi + 7),
            (fvi + 7, fvi + 6, fvi + 8, fvi + 9),
            (fvi + 9, fvi + 8, fvi + 10, fvi + 11),
            (fvi + 11, fvi + 10, fvi + 2, fvi + 3),

            (fvi, fvi + 2, fvi + 4),
            (fvi + 3, fvi + 1, fvi + 5),

            (fvi + 4, fvi + 8, fvi + 6),
            (fvi + 5, fvi + 7, fvi + 9),

            (fvi + 4, fvi + 10, fvi + 8),
            (fvi + 5, fvi + 9, fvi + 11),

            (fvi + 2, fvi + 10, fvi + 4),
            (fvi + 3, fvi + 5, fvi + 11),
        ])
    else:
        surface_verts = [fvi + 2, fvi + 3, fvi + 1, fvi]

        faces.extend([
            (fvi, fvi + 1, fvi + 5, fvi + 4),
            (fvi + 4, fvi + 5, fvi + 7, fvi + 6),
            (fvi + 6, fvi + 7, fvi + 9, fvi + 8),
            (fvi + 8, fvi + 9, fvi + 11, fvi + 10),
            (fvi + 10, fvi + 11, fvi + 3, fvi + 2),

            (fvi + 2, fvi, fvi + 4),
            (fvi + 1, fvi + 3, fvi + 5),

            (fvi + 4, fvi + 6, fvi + 8),
            (fvi + 5, fvi + 9, fvi + 7),

            (fvi + 4, fvi + 8, fvi + 10),
            (fvi + 5, fvi + 11, fvi + 9),

            (fvi + 2, fvi + 4, fvi + 10),
            (fvi + 3, fvi + 11, fvi + 5),
        ])

    return [vertices, edges, faces, surface_verts]

def is_clip_face(face, w_l):
    return (face.z % 2 == 0 and w_l != 0) or w_l == 2


# surface_indices: expected (tl, bl, br, tr)
def get_clip(
    e,
    depth,
    thickness,
    height,
    face,
    fvi = 0,
    face_w_l = 1,
    is_left_clip = True,
    position = None,
    angle = None,
    axis = None
):
    vertices = []
    edges = []
    faces = []

    surface = []

    if is_clip_face(face, face_w_l):
        ret = create_clip_mesh_data(e, depth, thickness, height, fvi, is_left_clip)
        vertices.extend(ret[0])
        edges.extend(ret[1])
        faces.extend(ret[2])
        surface = ret[3]
    else:
        ret = create_clip_hole_mesh_data(e, depth, thickness, height, fvi, is_left_clip)
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