import bpy
import math
from mathutils import Euler

n = 1 # max distance (in r unit)
r = 1.0 # hex side
h = 0.04 # hex thickness
trig_h = 0.1 # triangle walls height

basis_wheel_t = 0.1
basis_wheel_h = 1.7
basis_wheel_r = r
basis_wheel_p = 100 # wheel precision
basis_wheel_e = 0.005

# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
# w : hex triangle vertex index cw from center
def hex2xy(x, y, z, w):
    ytheta = math.pi / 6
    x2 = x * (3 * r)
    ytemp = y * (math.sqrt(3) * r)
    x2 += ytemp * math.cos(ytheta)
    y2 = ytemp * math.sin(ytheta)

    points = []
    for i in range(0, 6):
        theta = i * math.pi / 3
        x3 = x2 + r * math.cos(theta)
        y3 = y2 + r * math.sin(theta)
        points.append((
            x3,
            y3
        ))

    if w != 0:
        return points[(z + (w - 1)) % 6]

    return (x2, y2)

# e: epsilon, smallest change in position
# t: thickness
# h: height
# ht: teeth height
# hex_thickness: mirror hex thickness
def create_basis_wheel_mesh(e, t, h, r, p, hex_thickness, hex_walls_height):
    mesh = bpy.data.meshes.new('basis_wheel_mesh' + str((e,t,h,r,hex_thickness,hex_walls_height)))

    hr = 0.5 * r
    wr = 0.8 * r # wheel radius
    # e *= 1
    h1 = -hex_thickness - hex_walls_height - e
    h1 = -r + r * math.sin(math.pi / 3)
    zo = 0.25 * hr
    zow = 0.5 * zo
    zop = 0.5 * zow

    vertices = [
        (-e, hr - e, 0), (-hex_thickness, hr - e, 0), (-hex_thickness, -hr + e, 0), (-e, -hr + e, 0),
        (-e, hr - e, h1), (-hex_thickness, hr - e, h1), (-hex_thickness, -hr + e, h1), (-e, -hr + e, h1),
        (-e, 0, -wr),(-hex_thickness, 0, -wr), (-e, 0, h1),(-hex_thickness, 0, h1),
        (-e, hr + zo + zop, -wr + zow), (-hex_thickness, hr + zo + zop, -wr + zow), (-hex_thickness, -hr - zo - zop, -wr + zow), (-e, -hr - zo - zop, -wr + zow),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    faces = [
        (0, 1, 2, 3),
        (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]

    nb_verts = len(vertices)

    for i in range(0, p):
        alpha =  (0.8 * math.pi / 3) - i * ((0.8 * math.pi / 3) / p)
        vertices.append((-hex_thickness, wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        vertices.append((-e, wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        rv = nb_verts + 2 * i
        lv = nb_verts + 2 * i + 1
        print(str(vertices[rv]) + ' ' + str(vertices[lv]))

        edges.append((rv, lv))

        if i > 0:
            edges.append((rv - 2, rv))
            edges.append((lv - 2, lv))
            faces.append((rv, lv, lv - 2, rv - 2))
            faces.append((13, rv - 2, rv))
            faces.append((12, lv - 2, lv))
        else:
            edges.extend([(lv, 4), (5, rv)])
            faces.append((4, 5, rv, lv))
            faces.append((5, rv, 13))
            faces.append((4, lv, 12))
            faces.append((5, 13, 11))
            faces.append((4, 12, 10))

    nb_verts = len(vertices)
    up_rv = nb_verts - 2
    up_lv = nb_verts - 1

    for i in range(0, p):
        alpha = (0.8 * math.pi) / 3 - i * ((0.8 * math.pi / 3) / p)
        vertices.append((-hex_thickness, -wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        vertices.append((-e, -wr * math.cos(alpha), -wr + wr * math.sin(alpha)))
        rv = nb_verts + 2 * i
        lv = nb_verts + 2 * i + 1
        print(str(vertices[rv]) + ' ' + str(vertices[lv]))

        edges.append((rv, lv))

        if i > 0:
            edges.append((rv - 2, rv))
            edges.append((lv - 2, lv))
            faces.append((rv, lv, lv - 2, rv - 2))
            faces.append((14, rv - 2, rv))
            faces.append((15, lv - 2, lv))
        else:
            edges.extend([(lv, 7), (6, rv)])
            faces.append((7, 6, rv, lv))
            faces.append((6, rv, 14))
            faces.append((7, lv, 15))
            faces.append((6, 14, 11))
            faces.append((7, 15, 10))

    nb_verts = len(vertices)
    down_rv = nb_verts - 2
    down_lv = nb_verts - 1

    vertices.extend([
        (-hex_thickness, hr + zo, -wr), (-e, hr + zo, -wr), (-e, -hr - zo, -wr),(-hex_thickness, -hr - zo, -wr),
        (-hex_thickness, hr - zo - zop, -wr + zow), (-e, hr - zo - zop, -wr + zow), (-e, -hr + zo + zop, -wr + zow),(-hex_thickness, -hr + zo + zop, -wr + zow),
        (-hex_thickness, hr - zo + zop, -wr), (-e, hr - zo + zop, -wr), (-e, -hr + zo - zop, -wr),(-hex_thickness, -hr + zo - zop, -wr),
    ])

    print(str(vertices[up_rv]) + ' ' + str(vertices[up_lv]) + ' ' + str(vertices[down_rv]) + ' ' + str(vertices[down_lv]))

    edges.extend([
        (up_rv, nb_verts), (up_lv, nb_verts + 1),
        (down_rv, nb_verts + 3), (down_lv, nb_verts + 2),
        (nb_verts, 13), (nb_verts + 1, 12), (nb_verts + 3, 14), (nb_verts + 2, 15),
        (13, nb_verts + 4), (12, nb_verts + 5), (15, nb_verts + 6), (14, nb_verts + 7),
        (13, 12), (14, 15),(nb_verts + 4, nb_verts + 5), (nb_verts + 6, nb_verts + 7),
        (nb_verts + 8, nb_verts + 9), (nb_verts + 10, nb_verts + 11),
        (nb_verts + 4, nb_verts + 8), (nb_verts + 5, nb_verts + 9), (nb_verts + 6, nb_verts + 10), (nb_verts + 7, nb_verts + 11),
        (nb_verts + 8, 9), (nb_verts + 9, 8), (nb_verts + 10, 8), (nb_verts + 11, 9),
    ])

    faces.extend([
        (up_rv, nb_verts, nb_verts + 1, up_lv),
        (down_rv, nb_verts + 3, nb_verts + 2, down_lv),
        (up_rv, 13, nb_verts), (up_lv, 12, nb_verts + 1),
        (down_rv, 14, nb_verts + 3), (down_lv, 15, nb_verts + 2),
        (nb_verts, 13, 12, nb_verts + 1), (nb_verts + 3, 14, 15, nb_verts + 2),
        (13, 12, nb_verts + 5, nb_verts + 4), (14, 15, nb_verts + 6, nb_verts + 7),
        (13, nb_verts + 4, 11), (12, nb_verts + 5, 10),(14, nb_verts + 7, 11), (15, nb_verts + 6, 10),
        (nb_verts + 4, nb_verts + 8, nb_verts + 9, nb_verts + 5), (nb_verts + 6, nb_verts + 10, nb_verts + 11, nb_verts + 7),
        (nb_verts + 8, 9, 8, nb_verts + 9), (nb_verts + 10, 8, 9, nb_verts + 11),
        (nb_verts + 4, nb_verts + 8, 9), (nb_verts + 5, nb_verts + 9, 8),(nb_verts + 7, nb_verts + 11, 9), (nb_verts + 6, nb_verts + 10, 8),
        (9, nb_verts + 4, 11), (8, nb_verts + 5, 10),(9, nb_verts + 7, 11), (8, nb_verts + 6, 10),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def move_basis_to(obj, hex):
    hex_1 = hex2xy(0, 0, hex, 1)
    hex_2 = hex2xy(0, 0, hex, 2)
    hex_mid = (
        0.5 * (hex_1[0] + hex_2[0]),
        0.5 * (hex_1[1] + hex_2[1])
    )

    obj.location.x = hex_mid[0]
    obj.location.y = hex_mid[1]
    obj.location.z = h
    obj.rotation_euler = Euler((0, 0, (hex + 0.5) * (math.pi / 3)), 'XYZ')

    return

basis_collection = bpy.data.collections.new('basis_collection')
bpy.context.scene.collection.children.link(basis_collection)

hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]

basis_wheel_mesh = create_basis_wheel_mesh(
    basis_wheel_e,
    basis_wheel_t,
    basis_wheel_h,
    basis_wheel_r,
    basis_wheel_p,
    h,
    trig_h
)
# print('basis wheel mesh created: ' + str(basis_wheel_mesh))
basis_wheel_object_r = bpy.data.objects.new('basis_wheel_r', basis_wheel_mesh)
basis_collection.objects.link(basis_wheel_object_r)
move_basis_to(basis_wheel_object_r, 0)

basis_wheel_object_l = bpy.data.objects.new('basis_wheel_l', basis_wheel_mesh)
basis_collection.objects.link(basis_wheel_object_l)
move_basis_to(basis_wheel_object_l, 3)

print('done')
# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\basis_", check_existing=True, filter_glob='*.stl', use_selection=False, global_scale=100.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z')