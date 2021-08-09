import bpy
import math
from mathutils import Matrix, Vector

from optics import hex2xyz
from meshes import clip

half_hex_name = 'half_hex'
half_hex_num = 0

# e : margin
# f : focal length
# s : hex side length
# t : half hex thickness
# it : inner thickness
# wh : half hex walls height
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : first hex triangle index ccw
def create_mesh(
    e, f, s, t, it, wh, x, y, z,
    clip_depth,
    clip_height,
    clip_thickness,
    clip_e
):
    mesh_name = half_hex_name + '_' + str((e, f, s, t, it, wh, x, y, z))
    mesh = bpy.data.meshes.new(mesh_name)

    te = t + e
    fit = t + it

    v0 = hex2xyz(f, s, x, y, z, 0)
    v1 = hex2xyz(f, s, x, y, z, 1)
    v2 = hex2xyz(f, s, x, y, z + 1, 1)
    v3 = hex2xyz(f, s, x, y, z + 2, 1)
    v4 = hex2xyz(f, s, x, y, z + 2, 2)
    v5 = v4

    v01 = (Vector(v1) - Vector(v0))
    v03 = (Vector(v3) - Vector(v0))
    v12 = (Vector(v2) - Vector(v1))
    v20 = (Vector(v0) - Vector(v2))
    v23 = (Vector(v3) - Vector(v2))
    v34 = (Vector(v4) - Vector(v3))
    v40 = (Vector(v0) - Vector(v4))

    v01n = v01.normalized()
    v03n = v03.normalized()
    v12n = v12.normalized()
    v20n = v20.normalized()
    v23n = v23.normalized()
    v34n = v34.normalized()
    v40n = v40.normalized()

    n1 = v01n.cross(v12n).length
    n2 = v12n.cross(v23n).length
    n3 = v23n.cross(v34n).length
    n4 = v34n.cross(v40n).length

    w01 = v01n.copy()
    w03 = v03n.copy()
    w12 = v12n.copy()
    w20 = v20n.copy()
    w34 = v34n.copy()
    w40 = v40n.copy()

    n012 = w01.cross(w12).length
    n034 = w03.cross(w34).length
    n120 = w12.cross(w20).length
    n201 = w20.cross(w01).length
    n340 = w34.cross(w40).length
    n403 = w40.cross(w03).length

    d1 = t * (v12n - v01n) / n1
    d2 = t * (v23n - v12n) / n2
    d3 = t * (v34n - v23n) / n3
    d4 = t * (v40n - v34n) / n4

    d0 = tuple(t * (Vector(d1) + Vector(d4)).normalized())

    i0 = fit * (w01 - w20) / n201
    i1 = fit * (w12 - w01) / n012
    i2 = fit * (w20 - w12) / n120

    i3 = fit * (w03 - w40) / n403
    i4 = fit * (w34 - w03) / n034
    i5 = fit * (w40 - w34) / n340

    ecpi3 = e * math.cos(math.pi / 3)

    if x == 0 and y == 0:
        v1 = (
            (v1[0] - te - ecpi3) if z <= 0 else (v1[0] + te + ecpi3),
            v1[1],
            v1[2]
        )
        v2 = (
            (v2[0] - te) if z <= 0 else (v2[0] + te),
            (v2[1] - e) if z <= 0 else (v2[1] + e),
            v2[2]
        )
        v3 = (
            (v3[0] + e) if z <= 0 else (v3[0] - e),
            (v3[1] - e) if z <= 0 else (v3[1] + e),
            v3[2]
        )
        v4 = (
            (v4[0] + te + ecpi3) if z <= 0 else (v4[0] - te - ecpi3),
            (v4[1] + te) if z <= 0 else (v4[1] - te),
            v4[2]
        )
        v5 = (
            (v5[0] + te + ecpi3) if z <= 0 else (v5[0] - te - ecpi3),
            v5[1],
            v5[2]
        )

    vertices = [
        (v0[0], v0[1], v0[2] + t),
        v0,

        (v1[0], v1[1], v1[2] + t),
        v1,

        (v2[0], v2[1], v2[2] + t),
        v2,

        (v3[0], v3[1], v3[2] + t),
        v3,

        (v4[0], v4[1], v4[2] + t),
        v4,
    ]

    if x == 0 and y == 0:
        vertices.extend([
            (v5[0], v5[1], v5[2] + t),
            v5,
        ])
    else:
        vertices.extend([
            # 10
            (v0[0], v0[1], v0[2] - wh),
            (v1[0], v1[1], v1[2] - wh),
            (v2[0], v2[1], v2[2] - wh),
            (v3[0], v3[1], v3[2] - wh),
            (v4[0], v4[1], v4[2] - wh),

            # 15
            (v0[0] + d0[0], v0[1] + d0[1], v0[2] + d0[2] - wh),
            (v1[0] + d1[0], v1[1] + d1[1], v1[2] + d1[2] - wh),
            (v2[0] + d2[0], v2[1] + d2[1], v2[2] + d2[2] - wh),
            (v3[0] + d3[0], v3[1] + d3[1], v3[2] + d3[2] - wh),
            (v4[0] + d4[0], v4[1] + d4[1], v4[2] + d4[2] - wh),

            # 20
            (v0[0] + d0[0], v0[1] + d0[1], v0[2] + d0[2]),
            (v1[0] + d1[0], v1[1] + d1[1], v1[2] + d1[2]),
            (v2[0] + d2[0], v2[1] + d2[1], v2[2] + d2[2]),
            (v3[0] + d3[0], v3[1] + d3[1], v3[2] + d3[2]),
            (v4[0] + d4[0], v4[1] + d4[1], v4[2] + d4[2]),

            # 25
            (v0[0] + i0[0], v0[1] + i0[1], v0[2] + i0[2] + t),
            (v1[0] + i1[0], v1[1] + i1[1], v1[2] + i1[2] + t),
            (v2[0] + i2[0], v2[1] + i2[1], v2[2] + i2[2] + t),

            (v0[0] + i3[0], v0[1] + i3[1], v0[2] + i3[2] + t),
            (v3[0] + i4[0], v3[1] + i4[1], v3[2] + i4[2] + t),
            (v4[0] + i5[0], v4[1] + i5[1], v4[2] + i5[2] + t),

            # 31
            (v0[0] + i0[0], v0[1] + i0[1], v0[2] + i0[2]),
            (v1[0] + i1[0], v1[1] + i1[1], v1[2] + i1[2]),
            (v2[0] + i2[0], v2[1] + i2[1], v2[2] + i2[2]),

            (v0[0] + i3[0], v0[1] + i3[1], v0[2] + i3[2]),
            (v3[0] + i4[0], v3[1] + i4[1], v3[2] + i4[2]),
            (v4[0] + i5[0], v4[1] + i5[1], v4[2] + i5[2]),
        ])

    edges = [
        (0, 2), (2, 4), (4, 6), (6, 8),
        (1, 3), (3, 5), (5, 7), (7, 9),
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9),
    ]

    if x == 0 and y == 0:
        edges.extend([
            (8, 10), (10, 0),
            (9, 11), (11, 1),
            (10, 11),
        ])
    else:
        edges.extend([
            (8, 0),
            (9, 1),
            (10, 11), (11, 12), (12, 13), (13, 14), (14, 10),
            (1, 10), (3, 11), (5, 12), (7, 13), (9, 14),

            (15, 16), (16, 17), (17, 18), (18, 19), (19, 15),
            (10, 15), (11, 16), (12, 17), (13, 18), (14, 19),
            (20, 21), (21, 22), (22, 23), (23, 24), (24, 20),
            (15, 20), (16, 21), (17, 22), (18, 23), (19, 24),

            (25, 26), (26, 27), (27, 25),
            (28, 29), (29, 30), (30, 28),
            (31, 32), (32, 33), (33, 31),
            (34, 35), (35, 36), (36, 34),
            (25, 31), (26, 32), (27, 33),
            (28, 34), (29, 35), (30, 36),
        ])

    faces = [
        (0, 1, 3, 2), (2, 3, 5, 4), (4, 5, 7, 6), (6, 7, 9, 8),
        (0, 4, 6),
    ]

    if x == 0 and y == 0:
        faces.extend([
            (0, 2, 4), (0, 4, 6), (0, 6, 8),
            (0, 8, 10),
            (1, 11, 9),
            (8, 9, 11, 10),
            (10, 11, 1, 0),
            (1, 9, 7), (1, 7, 5), (1, 5, 3),
        ])
    else:
        faces.extend([
            (8, 9, 1, 0),

            (11, 10, 15, 16), (12, 11, 16, 17), (13, 12, 17, 18), (14, 13, 18, 19), (10, 14, 19, 15),
            (16, 15, 20, 21), (17, 16, 21, 22), (18, 17, 22, 23), (19, 18, 23, 24), (15, 19, 24, 20),

            (20, 23, 22),
            (21, 20, 31, 32), (22, 21, 32, 33), (20, 22, 33, 31),
            (32, 31, 25, 26), (33, 32, 26, 27), (31, 33, 27, 25),

            (23, 20, 34, 35), (24, 23, 35, 36), (20, 24, 36, 34),
            (35, 34, 28, 29), (36, 35, 29, 30), (34, 36, 30, 28),

            (0, 2, 26, 25), (2, 4, 27, 26), (4, 0, 25, 27),
            (0, 6, 29, 28), (6, 8, 30, 29), (8, 0, 28, 30),
        ])

    if x != 0 or y != 0:
        for i in range(0, 5):
            dz = 0
            w_l = 1
            position = None
            if i == 0:
                dz = 0
                w_l = 0
                position = (Vector(v0) + 0.5 * v01) if z <= 2 \
                    else (Vector(v1) - 0.5 * v01)
            elif i == 1:
                dz = 0
                position = (Vector(v1) + 0.5 * v12) if z <= 2 \
                    else (Vector(v2) - 0.5 * v12)
            elif i == 2:
                dz = 1
                position = (Vector(v2) + 0.5 * v23) if z <= 2 \
                    else (Vector(v3) - 0.5 * v23)
            elif i == 3:
                dz = 2
                position = (Vector(v3) + 0.5 * v34) if z <= 2 \
                    else (Vector(v4) - 0.5 * v34)
            elif i == 4:
                dz = 2
                w_l = 2
                position = (Vector(v4) + 0.5 * v40) if z <= 2 \
                    else (Vector(v0) - 0.5 * v40)

            ret = create_clip_face(
                clip_e,
                f,
                s,
                clip_depth,
                clip_thickness,
                clip_height,
                Vector((x, y, z + dz)),
                wh,
                w_l,
                len(vertices),
                position
            )

            vertices.extend(ret[0])
            edges.extend(ret[1])
            faces.extend(ret[2])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh


def create_clip_face(
    e,
    f,
    r,
    depth,
    thickness,
    height,
    face,
    face_height,
    face_w_l = 1,
    fvi = 0,
    position = None,
    angle = None,
    axis = 'Z',
    padding_x = 0,
    padding_z = 0,
):
    vl = Vector(hex2xyz(
        f,
        r,
        round(face.x),
        round(face.y),
        round(face.z),
        round(face_w_l)
    ))
    vr = Vector(hex2xyz(
        f,
        r,
        round(face.x),
        round(face.y),
        round(face.z),
        (round(face_w_l) + 1) % 3
    ))

    dv = vl - vr

    dvxyl = math.sqrt(dv.x ** 2 + dv.y ** 2)
    dvxz = Vector((dvxyl, 0, dv.z))
    lf = dvxz.length / r
    dvn = dvxz.normalized()
    displ = dvn * 0.25 * dvxz.length

    vxz = (0.5 * dvxz.length  - padding_x) * dvn
    voz = Vector((0, 0, face_height))
    pz = Vector((0, 0, padding_z))
    viz = voz - 2 * pz
    hvz = 0.5 * viz

    if angle == None:
        angle = ((face.z + 2 * face_w_l) - 3) * math.pi / 3

    rot = Matrix.Rotation(angle, 3, axis if axis != None else 'Z')

    vpos = position if position != None else Vector(0, 0, 0)

    vertices = [
        vpos + (rot @ -vxz - pz),
        vpos + (rot @ (-vxz - pz - viz)),
        vpos + (rot @ (vxz - pz - viz)),
        vpos + (rot @ vxz - pz)
    ]

    surface_indices = [fvi, fvi + 1, fvi + 2, fvi + 3]

    edges = []
    faces = []

    ret = clip.get_clip(
        e,
        depth,
        thickness,
        height,
        face,
        fvi + len(vertices),
        face_w_l,
        is_left_clip = True
    )

    for i in range(0, len(ret[0])):
        ret[0][i] += -displ - hvz
        ret[0][i] = vpos + (rot @ ret[0][i])

    vertices.extend(ret[0])
    # print('get_clip l ', str(len(vertices)), str(ret))
    edges.extend(ret[1])
    faces.extend(ret[2])
    surface_l = ret[3]

    ret = clip.get_clip(
        e,
        depth,
        thickness,
        height,
        face,
        fvi + len(vertices),
        face_w_l,
        is_left_clip = False
    )

    for i in range(0, len(ret[0])):
        ret[0][i] += displ - hvz
        ret[0][i] = vpos + (rot @ ret[0][i])

    # print('get_clip r', str(len(vertices)), str(ret))
    vertices.extend(ret[0])
    edges.extend(ret[1])
    faces.extend(ret[2])
    surface_r = ret[3]

    # f_fvi = fvi + len(vertices)
    edges.extend([
        (surface_indices[0], surface_indices[1]),
        (surface_indices[1], surface_indices[2]),
        (surface_indices[2], surface_indices[3]),
        (surface_indices[3], surface_indices[0])
    ])
    faces.extend([
        (surface_indices[0], surface_l[0], surface_l[1], surface_indices[1]),
        (surface_r[3], surface_indices[3], surface_indices[2], surface_r[2]),
        (surface_indices[0], surface_l[3], surface_l[0]),
        (surface_r[3], surface_r[0], surface_indices[3]),
        (surface_l[3], surface_indices[0], surface_indices[3], surface_r[0]),
        (surface_indices[1], surface_l[1], surface_l[2]),
        (surface_r[1], surface_r[2], surface_indices[2]),
        (surface_indices[1], surface_l[2], surface_r[1], surface_indices[2]),
        (surface_l[2], surface_l[3], surface_r[0], surface_r[1]),
    ])

    return [vertices, edges, faces]

def create_object(
    e, f, s, t, it, wh,
    font_size, font_extrusion,
    x, y, z,
    clip_depth,
    clip_height,
    clip_thickness,
    clip_e
):
    global half_hex_num
    half_hex_num += 1

    obj_name = half_hex_name + '_' + ('0' if half_hex_num < 10 else '') + str(half_hex_num)

    obj = bpy.data.objects.new(
        obj_name,
        create_mesh(
            e, f, s, t, it, wh, x, y, z,
            clip_depth,
            clip_height,
            clip_thickness,
            clip_e
        )
    )

    obj.location.z -= hex2xyz(f, s, 0, 0, 0, 0)[2]

    p0 = hex2xyz(f, s, x, y, z, 0)
    p2 = hex2xyz(f, s, x, y, z + 1, 1)
    p3 = hex2xyz(f, s, x, y, z + 2, 1)

    hex_collection = bpy.data.collections.get('hex_collection')
    hex_collection.objects.link(obj)

    bpy.ops.object.text_add()
    bpy.context.object.data.body = str(half_hex_num)
    bpy.context.object.data.align_x = 'CENTER'
    bpy.context.object.data.align_y = 'CENTER'
    bpy.context.object.data.size = font_size

    text_name = bpy.context.object.name

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.font.move(type='LINE_BEGIN')
    bpy.ops.font.move_select(type='NEXT_WORD')
    bpy.ops.font.style_set(style='UNDERLINE', clear=False)
    bpy.ops.object.mode_set( mode = 'OBJECT' )

    text_normal = Vector((0, 0, 1))
    half_hex_normal = \
        (
            (Vector(p2) - Vector(p0))
                .cross(Vector(p3) - Vector(p0))
        ).normalized()
    q = text_normal.rotation_difference(half_hex_normal)
    bpy.context.object.rotation_mode = 'QUATERNION'
    bpy.context.object.rotation_quaternion = q

    mid = (
        (p0[0] + p2[0] + p3[0]) / 3,
        (p0[1] + p2[1] + p3[1]) / 3,
        (p0[2] + p2[2] + p3[2]) / 3,
    )

    bpy.context.object.location.x = mid[0]
    bpy.context.object.location.y = mid[1]
    bpy.context.object.location.z = obj.location.z + mid[2]

    bpy.ops.transform.resize(value=(-1, 1, 1))
    bpy.ops.object.convert(target='MESH', keep_original=False)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all( action = 'SELECT' )   # Select all mesh elements
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value":(0, 0, -font_extrusion)} # Extrude by 1 BU on Z axis
    )
    bpy.ops.object.mode_set( mode = 'OBJECT' )

    hex_collection.objects.link(bpy.context.object)
    coll = bpy.data.collections.get('Collection')
    if bpy.context.object in coll.items():
        coll.objects.unlink(bpy.context.object)

    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]

    bpy.ops.object.parent_set()

    bpy.data.objects[obj_name].select_set(True)
    bpy.data.objects[text_name].select_set(True)

    bpy.ops.object.join()

    return obj