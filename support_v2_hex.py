import sys
import bpy
import mathutils
import math

n = 1 # max distance (in r unit)
# f = 2.0 # focal length

trig_name = 'tri'
r = 1.0 # hex side
h = 0.04 # hex thickness
f = 5 # focal length
d = 1.0 # parabola height

trig_h = 0.1 # triangle walls height

# f : focal length
# d : parabola height
# r : distance from parabola center
def dist2z(f, d, r):
    return (r * r) / (4 * f)

# f : focal length
# d : parabola height
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
# w : hex triangle vertex index cw from center
def hex2xyz(f, d, x, y, z, w):
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
            y3,
            dist2z(f, d, math.sqrt(x3 * x3 + y3 * y3))
        ))

    if w != 0:
        return points[(z + (w - 1)) % 6]

    z2 = 0
    for i in range(0, 6):
        z2 += points[i][2]

    z2 /= 6

    return (x2, y2, z2)


# f : focal length
# d : parabola height
# t : triangle thickness
# h : walls height
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
def create_triangle_mesh(f, d, t, h, x, y, z):
    mesh = bpy.data.meshes.new('trig_mesh' + str((f,d,t,x,y,z)))

    c = r * math.cos(math.pi / 3)
    s = r * math.sin(math.pi / 3)

    vertices = []

    v0 = hex2xyz(f, d, x, y, z, 0)
    print(str((x, y, z, 0)) + ' ' + str(v0))

    v1 = hex2xyz(f, d, x, y, z, 1)
    print(str((x, y, z, 1)) + ' ' + str(v1))

    v2 = hex2xyz(f, d, x, y, z, 2)
    print(str((x, y, z, 2)) + ' ' + str(v2))

    vmid = (
        (v0[0] + v1[0] + v2[0]) / 3,
        (v0[1] + v1[1] + v2[1]) / 3,
        (v0[2] + v1[2] + v2[2]) / 3
    )

    ri = r * (math.sqrt(3) / 6) # rayon cercle inscrit

    vertices.extend([
        v0, v1, v2,

        (v0[0], v0[1], v0[2] - t),
        (v1[0], v1[1], v1[2] - t),
        (v2[0], v2[1], v2[2] - t),

        (v0[0], v0[1], v0[2] - t - h),
        (v1[0], v1[1], v1[2] - t - h),
        (v2[0], v2[1], v2[2] - t - h),

        (v0[0] + t * (vmid[0] - v0[0]) / ri, v0[1] + t * (vmid[1] - v0[1]) / ri, v0[2] - t - h + t * (vmid[2] - v0[2]) / ri),
        (v1[0] + t * (vmid[0] - v1[0]) / ri, v1[1] + t * (vmid[1] - v1[1]) / ri, v1[2] - t - h + t * (vmid[2] - v1[2]) / ri),
        (v2[0] + t * (vmid[0] - v2[0]) / ri, v2[1] + t * (vmid[1] - v2[1]) / ri, v2[2] - t - h + t * (vmid[2] - v2[2]) / ri),

        (v0[0] + t * (vmid[0] - v0[0]) / ri, v0[1] + t * (vmid[1] - v0[1]) / ri, v0[2] - t + t * (vmid[2] - v0[2]) / ri),
        (v1[0] + t * (vmid[0] - v1[0]) / ri, v1[1] + t * (vmid[1] - v1[1]) / ri, v1[2] - t + t * (vmid[2] - v1[2]) / ri),
        (v2[0] + t * (vmid[0] - v2[0]) / ri, v2[1] + t * (vmid[1] - v2[1]) / ri, v2[2] - t + t * (vmid[2] - v2[2]) / ri),
    ])

    edges = [
        (0, 1), (1, 2), (2, 0),
        (3, 4), (4, 5), (5, 3),
        (0, 3), (1, 4), (2, 5),

        (6, 7), (7, 8), (8, 6),
        (3, 6), (4, 7), (5, 8),

        (9, 10), (10, 11), (11, 9),
        (6, 9), (7, 10), (8, 11),

        (12, 13), (13, 14), (14, 12),
        (9, 12), (10, 13), (11, 14),
    ]
    faces = [
        (0, 1, 2),
        (3, 4, 1, 0), (4, 5, 2, 1),(5, 3, 0, 2),
        (6, 7, 4, 3), (7, 8, 5, 4), (8, 6, 3, 5),
        (9, 10, 7, 6), (10, 11, 8, 7), (11, 9, 6, 8),
        (10, 9, 12, 13), (11, 10, 13, 14), (11, 9, 12, 14),
        (12, 13, 14),
    ]

    # print('trig mesh' + str(vertices) + ' ' + str(edges) + ' ' + str(faces))

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

hex_collection = bpy.data.collections.new('hex_collection')
bpy.context.scene.collection.children.link(hex_collection)

hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]
prev_hexes = [(0, 0)]
curr_hexes = []
hexes = prev_hexes

for i in range(0, n + 1):
    for j in range(0, len(prev_hexes)):
        for l in range(0, len(hex_arrows)):
            x = prev_hexes[j][0] + hex_arrows[l][0]
            y = prev_hexes[j][1] + hex_arrows[l][1]

            if (x, y) in hexes or (x, y) in curr_hexes:
                continue

            # print(str((x, y)) + ' not found')
            for z in range(0, 6):
                mesh = create_triangle_mesh(f, d, h,trig_h, x, y, z)

                # print('mesh created z: ' + str((x, y, z)) + str(mesh))
                triangle_object = bpy.data.objects.new(trig_name + '_0', mesh)
                hex_collection.objects.link(triangle_object)

            curr_hexes.append((x, y))
    prev_hexes = curr_hexes
    hexes.extend(curr_hexes)
    curr_hexes = []

print('done')

# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\support_", check_existing=True, filter_glob='*.stl', use_selection=False, global_scale=100.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z')