import bpy
import bmesh
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
# wh : half hex walls height
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : first hex triangle index ccw
def create_mesh(e, f, s, t, wh, x, y, z):
    mesh_name = half_hex_name + '_' + str((e, f, s, t, wh, x, y, z))
    mesh = bpy.data.meshes.new(mesh_name)

    hwh = 0.5 * wh

    te = t + e

    v0 = hex2xyz(f, s, x, y, z, 0)
    v1 = hex2xyz(f, s, x, y, z, 1)
    v2 = hex2xyz(f, s, x, y, z + 1, 1)
    v3 = hex2xyz(f, s, x, y, z + 2, 1)
    v4 = hex2xyz(f, s, x, y, z + 2, 2)
    v5 = v4

    v01 = Vector((v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])).normalized()
    v12 = Vector((v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])).normalized()
    v23 = Vector((v3[0] - v2[0], v3[1] - v2[1], v3[2] - v2[2])).normalized()
    v34 = Vector((v4[0] - v3[0], v4[1] - v3[1], v4[2] - v3[2])).normalized()
    v40 = Vector((v0[0] - v4[0], v0[1] - v4[1], v0[2] - v4[2])).normalized()

    n1 = v01.cross(v12).length
    n2 = v12.cross(v23).length
    n3 = v23.cross(v34).length
    n4 = v34.cross(v40).length

    w01 = Vector((v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])).normalized()
    w03 = Vector((v3[0] - v0[0], v3[1] - v0[1], v3[2] - v0[2])).normalized()
    w12 = Vector((v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])).normalized()
    w20 = Vector((v0[0] - v2[0], v0[1] - v2[1], v0[2] - v2[2])).normalized()
    w34 = Vector((v4[0] - v3[0], v4[1] - v3[1], v4[2] - v3[2])).normalized()
    w40 = Vector((v0[0] - v4[0], v0[1] - v4[1], v0[2] - v4[2])).normalized()

    n012 = w01.cross(w12).length
    n034 = w03.cross(w34).length
    n120 = w12.cross(w20).length
    n201 = w20.cross(w01).length
    n340 = w34.cross(w40).length
    n403 = w40.cross(w03).length

    d1 = (t * (v12[0] - v01[0]) / n1, t * (v12[1] - v01[1]) / n1, t * (v12[2] - v01[2]) / n1)
    d2 = (t * (v23[0] - v12[0]) / n2, t * (v23[1] - v12[1]) / n2, t * (v23[2] - v12[2]) / n2)
    d3 = (t * (v34[0] - v23[0]) / n3, t * (v34[1] - v23[1]) / n3, t * (v34[2] - v23[2]) / n3)
    d4 = (t * (v40[0] - v34[0]) / n4, t * (v40[1] - v34[1]) / n4, t * (v40[2] - v34[2]) / n4)

    d0 = tuple(t * (Vector(d1) + Vector(d4)).normalized())

    i0 = (2 * t * (w01[0] - w20[0]) / n201, 2 * t * (w01[1] - w20[1]) / n201, 2 * t * (w01[2] - w20[2]) / n201)
    i1 = (2 * t * (w12[0] - w01[0]) / n012, 2 * t * (w12[1] - w01[1]) / n012, 2 * t * (w12[2] - w01[2]) / n012)
    i2 = (2 * t * (w20[0] - w12[0]) / n120, 2 * t * (w20[1] - w12[1]) / n120, 2 * t * (w20[2] - w12[2]) / n120)

    i3 = (2 * t * (w03[0] - w40[0]) / n403, 2 * t * (w03[1] - w40[1]) / n403, 2 * t * (w03[2] - w40[2]) / n403)
    i4 = (2 * t * (w34[0] - w03[0]) / n034, 2 * t * (w34[1] - w03[1]) / n034, 2 * t * (w34[2] - w03[2]) / n034)
    i5 = (2 * t * (w40[0] - w34[0]) / n340, 2 * t * (w40[1] - w34[1]) / n340, 2 * t * (w40[2] - w34[2]) / n340)

    ecpi3 = e * math.cos(math.pi / 3)
    d4x = 0.5 * (te + ecpi3)

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

        # print(str(v1), str(v2), str(v3), str(v4), str(v5))

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
            (3, 1, 10, 11), (5, 3, 11, 12), (7, 5, 12, 13), (9, 7, 13, 14), (1, 9, 14, 10),

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

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    bm = bmesh.new()
    bm.from_mesh(mesh)

    if x != 0 or y != 0:
        clip_depth = t - 0.02
        clip_h = 0.5 * wh
        clip_t = 0.015
        clip_p = 25
        clip_mesh = clip.create_mesh(clip_depth, clip_t, clip_h, clip_p)
        if z <= 0:
            alpha = -math.pi / 3
            tv = Vector((
                v1[0] + v12[0] * 0.25 * s,
                v1[1] + v12[1] * 0.25 * s,
                v1[2] + v12[2] * 0.25 * s - hwh
            ))

            clip_mesh.transform(Matrix.Rotation(alpha, 4, 'Z'))
            clip_mesh.transform(Matrix.Translation(tv))

            bm.from_mesh(clip_mesh)

            tv2 = Vector((
                v12[0] * 0.5 * s,
                v12[1] * 0.5 * s,
                v12[2] * 0.5 * s
            ))

            clip_mesh.transform(Matrix.Translation(tv2))

            bm.from_mesh(clip_mesh)

            beta = math.pi / 3
            tv3 = Vector((
                v3[0] + v34[0] * 0.25 * s,
                v3[1] + v34[1] * 0.25 * s,
                v3[2] + v34[2] * 0.25 * s - hwh
            ))

            ri = Matrix.Rotation(-alpha, 4, 'Z')
            ti = Matrix.Translation(-tv - tv2)

            clip_mesh.transform(ti)
            clip_mesh.transform(ri)

            clip_mesh.transform(Matrix.Rotation(beta, 4, 'Z'))
            clip_mesh.transform(Matrix.Translation(tv3))

            bm.from_mesh(clip_mesh)

            tv4 = Vector((
                v34[0] * 0.5 * s,
                v34[1] * 0.5 * s,
                v34[2] * 0.5 * s
            ))

            clip_mesh.transform(Matrix.Translation(tv4))

            bm.from_mesh(clip_mesh)


            ri = Matrix.Rotation(-beta, 4, 'Z')
            ti = Matrix.Translation(-tv3 - tv4)

            clip_mesh.transform(ti)
            clip_mesh.transform(ri)
        else:
            alpha = math.pi
            tv = Vector((
                v2[0] + v23[0] * 0.25 * s,
                v2[1] + v23[1] * 0.25 * s,
                v2[2] + v23[2] * 0.25 * s - hwh
            ))

            clip_mesh.transform(Matrix.Rotation(alpha, 4, 'Z'))
            clip_mesh.transform(Matrix.Translation(tv))

            bm.from_mesh(clip_mesh)

            tv2 = Vector((
                v23[0] * 0.5 * s,
                v23[1] * 0.5 * s,
                v23[2] * 0.5 * s
            ))

            clip_mesh.transform(Matrix.Translation(tv2))

            bm.from_mesh(clip_mesh)

            ri = Matrix.Rotation(-alpha, 4, 'Z')
            ti = Matrix.Translation(-tv - tv2)

            clip_mesh.transform(ti)
            clip_mesh.transform(ri)

        gamma = math.pi if z <= 0 else 0
        tv5 = Vector((
            v4[0] + v40[0] * 0.25 * s,
            v4[1] + v40[1] * 0.25 * s,
            v4[2] + v40[2] * 0.25 * s - hwh
        ))

        clip_mesh.transform(Matrix.Rotation(gamma, 4, 'Z'))
        clip_mesh.transform(Matrix.Translation(tv5))

        bm.from_mesh(clip_mesh)

        tv6 = Vector((
            v40[0] * 0.5 * s,
            v40[1] * 0.5 * s,
            v40[2] * 0.5 * s
        ))

        clip_mesh.transform(Matrix.Translation(tv6))

        bm.from_mesh(clip_mesh)

    mesh = bpy.data.meshes.new(mesh_name)
    bm.to_mesh(mesh)
    bm.free()

    return mesh

def create_object(e, f, s, t, wh, x, y, z):
    global half_hex_num
    half_hex_num += 1

    obj_name = half_hex_name + '_' + ('0' if half_hex_num < 10 else '') + str(half_hex_num)

    obj = bpy.data.objects.new(
        obj_name,
        create_mesh(e, f, s, t, wh, x, y, z)
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

    bpy.ops.transform.resize(value=(-0.25, 0.25, 0.25))
    bpy.ops.object.convert(target='MESH', keep_original=False)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all( action = 'SELECT' )   # Select all mesh elements
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value":(0, 0, -t)} # Extrude by 1 BU on Z axis
    )
    bpy.ops.object.mode_set( mode = 'OBJECT' )

    hex_collection.objects.link(bpy.context.object)
    bpy.data.collections.get('Collection').objects.unlink(bpy.context.object)

    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]

    bpy.ops.object.parent_set()

    bpy.data.objects[obj_name].select_set(True)
    bpy.data.objects[text_name].select_set(True)

    bpy.ops.object.join()

    return obj