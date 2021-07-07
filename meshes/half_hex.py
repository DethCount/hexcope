import bpy
import math
from mathutils import Vector

from optics import hex2xyz

half_hex_name = 'half_hex'
half_hex_num = 0

# f : focal length
# s : hex side length
# t : half hex thickness
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : first hex triangle index ccw
def create_mesh(f, s, t, x, y, z):
    mesh_name = 'half_hex_mesh' + str((f, s, t, x, y, z))
    mesh = bpy.data.meshes.new(mesh_name)

    v0 = hex2xyz(f, s, x, y, z, 0)
    v1 = hex2xyz(f, s, x, y, z, 1)
    v2 = hex2xyz(f, s, x, y, z + 1, 1)
    v3 = hex2xyz(f, s, x, y, z + 2, 1)
    v4 = hex2xyz(f, s, x, y, z + 2, 2)

    vertices = [
        v0,
        (v0[0], v0[1], v0[2] - t),

        v1,
        (v1[0], v1[1], v1[2] - t),

        v2,
        (v2[0], v2[1], v2[2] - t),

        v3,
        (v3[0], v3[1], v3[2] - t),

        v4,
        (v4[0], v4[1], v4[2] - t),
    ]

    edges = [
        (0, 2), (2, 4), (4, 6), (6, 8), (8, 0),
        (1, 3), (3, 5), (5, 7), (7, 9), (9, 1),
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9),
    ]

    faces = [
        (0, 2, 4), (0, 4, 6), (0, 6, 8),
        (1, 9, 7), (1, 7, 5), (1, 5, 3),
        (0, 1, 3, 2), (2, 3, 5, 4), (4, 5, 7, 6), (6, 7, 9, 8), (8, 9, 1, 0),
    ]

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def create_object(f, s, t, x, y, z):
    global half_hex_num
    half_hex_num += 1

    obj_name = half_hex_name + '_' + str(half_hex_num)

    obj = bpy.data.objects.new(
        obj_name,
        create_mesh(f, s, t, x, y, z)
    )

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

    p0 = hex2xyz(f, s, x, y, z, 0)
    p2 = hex2xyz(f, s, x, y, z + 1, 1)
    p3 = hex2xyz(f, s, x, y, z + 2, 1)

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
    bpy.context.object.location.z = mid[2] - t

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