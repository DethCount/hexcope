import bpy
import math

n = 3 # max distance (in r unit)
# f = 2.0 # focal length

hex_name = 'hex'
r = 1.0 # hex side
h = 0.1 # hex thickness
e = 0.0 # distance between hex tiles

support_name = 'supp'
support_r = 0.4 * r # support wing length
support_h = 0.01 # support wing height
support_w = 0.1 # support wing width
support_d = 0.02 # support head height
support_hp = 100 # support head precision

support_t_name = 'trig'
support_t_h = 0.02 # support triangle (half hex) height

support_lbar_name = 'lbar'
support_bar_name = 'bar'

def create_hex_mesh(r, h):
    hex_mesh = bpy.data.meshes.new('hex_mesh')

    c = r * math.cos(math.pi / 3)
    s = r * math.sin(math.pi / 3)

    vertices = [
        (0, 0, 0),(0, 0, h),
        (r, 0, 0),(c, s, 0), (-c, s, 0),(-r, 0, 0),(-c, -s, 0),(c, -s, 0),
        (r, 0, h),(c, s, h), (-c, s, h),(-r, 0, h),(-c, -s, h),(c, -s, h),
    ]
    edges = [
        (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 2),
        (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 8),
        (2, 8), (3, 9), (4, 10), (5, 11), (6, 12), (7, 13)
    ]
    faces = [
        (0, 2, 3), (0, 3, 4),(0, 4, 5),(0, 5, 6),(0, 6, 7),(0, 7, 2),
        (1, 8, 9),(1, 9, 10),(1, 10, 11),(1, 11, 12),(1, 12, 13),(1, 13, 8),
        (2, 3, 9, 8),(3, 4, 10, 9),(4, 5, 11, 10),(5, 6, 12, 11),(6, 7, 13, 12),(7, 2, 8, 13)
    ]

    hex_mesh.from_pydata(vertices, edges, faces)
    hex_mesh.update()

    return hex_mesh

# hp: support head cylinder precision
def create_support_mesh(z, r, h, w, d, hp):
    support_mesh = bpy.data.meshes.new('support_mesh')

    c = math.cos(math.pi / 3)
    s = math.sin(math.pi / 3)
    rc = r * c
    rs = r * s
    hw = 0.5 * w
    hwc = hw * c
    hws = hw * s
    hcr = (math.sqrt(3) / 3) * w
    hth = hcr * c # half triangle height

    vertices = [
        (0, 0, z),
        (hth, hw, z), (r, hw, z), (r, -hw, z), (hth, -hw, z),
        (-hcr, 0, z),
        (hth - rc, hw + rs, z), (-hcr - rc, rs, z),
        (-hcr - rc, -rs, z), (hth - rc, - hw - rs, z),

        (hth, hw, z + h), (r, hw, z + h), (r, -hw, z + h), (hth, -hw, z + h),
        (-hcr, 0, z + h),
        (hth - rc, hw + rs, z + h), (-hcr - rc, rs, z + h),
        (-hcr - rc, -rs, z + h), (hth - rc, - hw - rs, z + h),
    ]
    edges = [
        (1, 2), (2, 3), (3, 4), (4, 1),
        (1, 4), (4, 5), (5, 1),
        (1, 6), (6, 7), (7, 5), (5, 1),
        (5, 8), (8, 9), (9, 4),

        (10, 11), (11, 12), (12, 13), (13, 10),
        (10, 13), (13, 14), (14, 10),
        (10, 15), (15, 16), (16, 14), (14, 10),
        (14, 17), (17, 18), (18, 13),

        (1, 10), (2, 11), (3, 12), (4, 13),
        (5, 14),
        (6, 15), (7, 16),
        (8, 17), (9, 18)
    ]
    faces = [
        (1, 2, 3, 4),
        (1, 4, 5),
        (1, 6, 7, 5),
        (5, 8, 9, 4),

        (13, 12, 11, 10),
        (14, 13, 10),
        (10, 15, 16, 14),
        (14, 17, 18, 13),

        (1, 2, 11, 10), (2, 3, 12, 11), (3, 4, 13, 12),
        (1, 6, 15, 10), (6, 7, 16, 15), (7, 5, 14, 16),
        (5, 8, 17, 14), (8, 9, 18, 17), (9, 4, 13, 18)
    ]

    if d > 0:
        bottom_center = len(vertices)
        vertices.append((0, 0, z + h))
        vertices.append((0, 0, z + h + d))
        top_center = bottom_center + 1

        print('' + str(vertices[bottom_center]) + ' ' + str(vertices[top_center]) + ' ' + str(hw))

        for i in range(0, hp):
            theta = (i * math.tau) / hp
            print(str(theta))

            x = hcr * math.cos(theta)
            y = hcr * math.sin(theta)
            vertices.append((x, y, z + h))
            vertices.append((x, y, z + h + d))
            lv = len(vertices)

            edges.append((lv - 2, lv - 1)) # side

            if i > 0:
                edges.append((lv - 4, lv - 2)) # bottom circle
                edges.append((lv - 3, lv - 1)) # top circle

                faces.append((bottom_center, lv - 4, lv - 2)) # bottom circle
                faces.append((top_center, lv - 3, lv - 1)) # top circle
                faces.append((lv - 4, lv - 2, lv - 1, lv - 3)) # side

            if i == hp - 1:
                start_bottom = lv - 2 * hp
                start_top = start_bottom + 1

                edges.append((lv - 2, start_bottom)) # closed bottom circle
                edges.append((lv - 1, start_top)) # closed top circle

                faces.append((bottom_center, start_bottom, lv - 2)) # closed bottom circle
                faces.append((top_center, start_top, lv - 1)) # closed top circle
                faces.append((lv - 2 * hp, lv - 2, lv - 1, lv - 2 * hp + 1)) # closed side

    support_mesh.from_pydata(vertices, edges, faces)
    support_mesh.update()

    return support_mesh

def create_support_t_mesh(z, r, w, h):
    support_t_mesh = bpy.data.meshes.new('support_t_mesh')

    a = math.pi / 3
    c = math.cos(a)
    s = math.sin(a)
    hr = 0.5 * r
    hw = 0.5 * w
    rc = r * c
    rs = r * s
    hwc = hw * c
    hws = hw * s

    vertices = [
        (r * c + hwc, rs + hws, z), (-r - hw, 0, z), (rc + hwc, -rs - hws, z),
        (r * c - hwc, rs - hws, z), (-r + hw, 0, z), (rc - hwc, -rs + hws, z),
        (r * c + hwc, rs + hws, z + h), (-r - hw, 0, z + h), (rc + hwc, -rs - hws, z + h),
        (r * c - hwc, rs - hws, z + h), (-r + hw, 0, z + h), (rc - hwc, -rs + hws, z + h),
    ]
    edges = [
        (0, 1), (1, 2), (2, 0),
        (3, 4), (4, 5), (5, 3),

        (6, 7), (7, 8), (8, 6),
        (9, 10), (10, 11), (11, 9),

        (0, 6), (1, 7), (2, 8),
        (3, 9), (4, 10), (5, 11),
    ]
    faces = [
        (1, 0, 3, 4), (2, 5, 3, 0), (4, 5, 2, 1),
        (7, 6, 9, 10), (8, 11, 9, 6), (10, 11, 8, 7),
        (1, 0, 6, 7), (2, 1, 7, 8), (2, 0, 6, 8),
        (4, 3, 9, 10), (5, 4, 10, 11), (5, 3, 9, 11),
    ]

    support_t_mesh.from_pydata(vertices, edges, faces)
    support_t_mesh.update()

    return support_t_mesh

def create_support_lbar_mesh(z, r, w, h):
    support_lbar_mesh = bpy.data.meshes.new('support_lbar_mesh')

    a = math.pi / 3
    c = math.cos(a)
    s = math.sin(a)
    hr = 0.5 * r
    hw = 0.5 * w
    rc = r * c
    rs = r * s

    vertices = [
        (-rc - hw, rs + hw, z), (rc + hw, rs + hw, z), (rc + hw, rs - hw, z), (-rc - hw, rs - hw, z),
        (-rc - hw, rs + hw, z + h), (rc + hw, rs + hw, z + h), (rc + hw, rs - hw, z + h), (-rc - hw, rs - hw, z + h),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 1),
        (4, 5), (5, 6), (6, 7), (7, 4),

        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    faces = [
        (3, 2, 1, 0),
        (7, 6, 5, 4),
        (1, 0, 4, 5), (2, 1, 5, 6), (3, 2, 6, 7), (0, 3, 7, 4)
    ]

    support_lbar_mesh.from_pydata(vertices, edges, faces)
    support_lbar_mesh.update()

    return support_lbar_mesh


def create_support_bar_mesh(z, r, w, h):
    support_bar_mesh = bpy.data.meshes.new('support_bar_mesh')

    a = math.pi / 3
    c = math.cos(a)
    s = math.sin(a)
    hr = 0.5 * r
    hw = 0.5 * w
    rc = r * c
    rs = r * s
    hth = math.sqrt(3) * hr

    vertices = [
        (-hr - hw, hth + hw, z), (-hr + hw, hth + hw, z), (-hr + hw, -hth - hw, z), (-hr - hw, -hth - hw, z),
        (-hr - hw, hth + hw, z + h), (-hr + hw, hth + hw, z + h), (-hr + hw, -hth - hw, z + h), (-hr - hw, -hth - hw, z + h),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 1),
        (4, 5), (5, 6), (6, 7), (7, 4),

        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    faces = [
        (3, 2, 1, 0),
        (7, 6, 5, 4),
        (1, 0, 4, 5), (2, 1, 5, 6), (3, 2, 6, 7), (0, 3, 7, 4)
    ]

    support_bar_mesh.from_pydata(vertices, edges, faces)
    support_bar_mesh.update()

    return support_bar_mesh

hex_collection = bpy.data.collections.new('hex_collection')
bpy.context.scene.collection.children.link(hex_collection)

hex_mesh = create_hex_mesh(r, h)
hex_length = (3 * r + 2 * e, math.sqrt(3) * r + e)
hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]
hex_ytheta = math.pi / 6


hex_object = bpy.data.objects.new(hex_name + '_0', hex_mesh)
hex_collection.objects.link(hex_object)
prev_hexes = [(0, 0)]
curr_hexes = []
hexes = []

for i in range(0, n + 1):
    for j in range(0, len(prev_hexes)):
        for l in range(0, len(hex_arrows)):
            x = prev_hexes[j][0] + hex_arrows[l][0]
            y = prev_hexes[j][1] + hex_arrows[l][1]

            if (x, y) in prev_hexes:
                continue

            cx = x * hex_length[0] + y * hex_length[1] * math.cos(hex_ytheta)
            cy = y * hex_length[1] * math.sin(hex_ytheta)

            print(str(cx) + ',' + str(cy))

            hex_object = bpy.data.objects.new(hex_name + '_' + str(i), hex_mesh)
            hex_collection.objects.link(hex_object)
            hex_object.location.x = cx
            hex_object.location.y = cy

            curr_hexes.append((x, y))
    prev_hexes = curr_hexes
    hexes.append(curr_hexes)
    curr_hexes = []

support_collection = bpy.data.collections.new('support_collection')
bpy.context.scene.collection.children.link(support_collection)

support_mesh = create_support_mesh(h, support_r, support_h, support_w, support_d, support_hp)

support_object = bpy.data.objects.new(support_name + '_0', support_mesh)
support_collection.objects.link(support_object)
support_object.location.x = r

support_t_mesh = create_support_t_mesh(h + support_h + support_d, r, 2 * support_w, support_t_h)
support_t_object = bpy.data.objects.new(support_t_name + '_0', support_t_mesh)
support_collection.objects.link(support_t_object)

support_lbar_mesh = create_support_lbar_mesh(h + support_h + support_d, r, support_w, support_t_h)
support_lbar_object = bpy.data.objects.new(support_lbar_name + '_0', support_lbar_mesh)
support_collection.objects.link(support_lbar_object)

support_bar_mesh = create_support_bar_mesh(h + support_h + support_d, r, support_w, support_t_h)
support_bar_object = bpy.data.objects.new(support_bar_name + '_0', support_bar_mesh)
support_collection.objects.link(support_bar_object)
