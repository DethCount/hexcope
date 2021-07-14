import os
import sys
import bpy
import math
from mathutils import Euler

sys.dont_write_bytecode = 1
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )

from hyperparameters import n, r, h, f, p, e, trig_h, primary_t, support_secondary_is_newton
from optics import parabolic_z, spherical_z, hex2xy, hex2xyz, get_support_arm_points
from meshes import half_hex, support_arm_block

#n = 0
p = 25
fw = 0.05 * r # fixation half width
fd = 0.03 # fixation hole diameter

current_triangle_num = 0
trig_name = 'tri'

support_spider_t = 0.03
support_spider_h = 0.1
support_spider_w = 2.0

support_secondary_z = 12

support_spherical_secondary_name = 'spherical_secondary_mirror'
support_spherical_secondary_t = support_spider_h
support_spherical_secondary_z = support_secondary_z + support_spherical_secondary_t
support_spherical_secondary_r = r
support_spherical_secondary_f = 10.0 * r
support_spherical_secondary_rp = 25

support_newton_secondary_name = 'newton_secondary_mirror'
support_newton_secondary_t = support_spider_h
support_newton_secondary_rx = r
support_newton_secondary_ry = support_newton_secondary_rx
support_newton_secondary_rp = 25
support_newton_secondary_z = support_secondary_z + support_newton_secondary_rx * math.cos(math.pi / 4) + support_newton_secondary_t

support_secondary_final_name = support_spherical_secondary_name
support_secondary_final_z = support_spherical_secondary_z

if support_secondary_is_newton:
    support_secondary_final_name = support_newton_secondary_name
    support_secondary_final_z = support_newton_secondary_z

support_arm_e = e
support_arm_r = 0.1
support_arm_t = 0.03
support_arm_h = 2
support_arm_rp = 25
support_arm_hp = 18
support_arm_n = 3
support_arm_omega = 0
support_arm_margin = 0.25 * r
support_arm_points = get_support_arm_points(n, r, support_arm_margin, support_arm_n, support_arm_omega)
support_arm_d = math.sqrt(support_arm_points[0][1][0] ** 2 + support_arm_points[0][1][1] ** 2)
support_arm_rld = math.sqrt((support_arm_points[0][1][0] - support_arm_points[0][0][0]) ** 2 + (support_arm_points[0][1][1] - support_arm_points[0][0][1]) ** 2)
support_arm_z = parabolic_z(f, support_arm_d) - h
support_arm_nz = math.ceil(support_secondary_z / support_arm_h)

support_arm_block_e = e
support_arm_block_f = f
support_arm_block_n = n
support_arm_block_r = r
support_arm_block_t = h
support_arm_block_m = support_arm_margin
support_arm_block_p = p
support_arm_block_hex_thickness = h
support_arm_block_hex_walls_height = trig_h
support_arm_block_hex_primary_thickness = primary_t
support_arm_block_arm_radius = support_arm_r

support_arm_head_e = support_arm_e
support_arm_head_t = 0.05
support_arm_head_h = support_spider_h
support_arm_head_z = support_secondary_final_z
support_arm_head_arm_d = support_arm_rld
support_arm_head_arm_r = support_arm_r
support_arm_head_arm_rp = support_arm_rp
support_arm_spider_thickness = support_spider_t
support_arm_spider_length = 1.5 * r

def create_primary_mirror_normal(e, f, r, x, y, z):
    mesh = bpy.data.meshes.new('primary_mirror_normals_' + str((
        e, f, x, y, z
    )))

    # print('primary_mirror_normals')
    p1w0 = hex2xyz(f, r, x, y, z, 0)
    p1w1 = hex2xyz(f, r, x, y, z, 1)
    p1w2 = hex2xyz(f, r, x, y, z, 2)

    u = (p1w1[0] - p1w0[0], p1w1[1] - p1w0[1], p1w1[2] - p1w0[2])
    v = (p1w2[0] - p1w0[0], p1w2[1] - p1w0[1], p1w2[2] - p1w0[2])

    n = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

    ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
    un = (n[0] / ln, n[1] / ln, n[2] / ln)

    dunxy = math.sqrt(un[0] ** 2 + un[1] ** 2)
    maxd0 = 0
    if dunxy > 0:
        maxd0 = math.sqrt(p1w0[0] ** 2 + p1w0[1] ** 2) / math.sqrt(un[0] ** 2 + un[1] ** 2)

    pun0 = (
        p1w0[0] + un[0] * maxd0,
        p1w0[1] + un[1] * maxd0,
        p1w0[2] + un[2] * maxd0
    )

    vertices = [
        p1w0,
        (p1w0[0] + e, p1w0[1] + e, p1w0[2] + e),
        pun0,
        (pun0[0] + e, pun0[1] + e, pun0[2] + e),
    ]
    edges = []
    faces = [
        (0, 1, 3, 2),
    ]

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def create_spherical_rays(e, h, r, f, x, y, z, primary_f, hex_side):
    mesh = bpy.data.meshes.new('rays_mesh' + str((
        e, h, r, f, x, y, z, primary_f, hex_side
    )))

    p0 = (10, 10, 10)

    # print('spherical_rays')
    p1w0 = hex2xyz(primary_f, hex_side, x, y, z, 0)
    p1w1 = hex2xyz(primary_f, hex_side, x, y, z, 1)
    p1w2 = hex2xyz(primary_f, hex_side, x, y, z, 2)

    u = (p1w1[0] - p1w0[0], p1w1[1] - p1w0[1], p1w1[2] - p1w0[2])
    v = (p1w2[0] - p1w0[0], p1w2[1] - p1w0[1], p1w2[2] - p1w0[2])

    n = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

    ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
    un = (n[0] / ln, n[1] / ln, n[2] / ln)

    d10 = (
        p1w0[0] - p0[0],
        p1w0[1] - p0[1],
        p1w0[2] - p0[2]
    )

    ld10 = math.sqrt(d10[0] ** 2 + d10[1] ** 2 + d10[2] ** 2)

    ud10 = (
        d10[0] / ld10,
        d10[1] / ld10,
        d10[2] / ld10
    )

    reflected = (
        ud10[0] - ud10[1] * un[0],
        ud10[1] + ud10[2] * un[1],
        ud10[2] + ud10[0] * un[2],
    )

    lreflected = math.sqrt(reflected[0] ** 2 + reflected[1] ** 2 + reflected[2] ** 2)
    ureflected = (
        reflected[0] / lreflected,
        reflected[1] / lreflected,
        reflected[2] / lreflected
    )

    far = 100

    sh = f - math.sqrt(f ** 2 - r ** 2)

    dunxy = math.sqrt(un[0] ** 2 + un[1] ** 2)
    maxd0 = 0
    maxd = 0
    h0 = 0
    if dunxy > 0:
        maxd0 = math.sqrt(p1w0[0] ** 2 + p1w0[1] ** 2) / math.sqrt(un[0] ** 2 + un[1] ** 2)
        h0 = maxd0 * un[2]
        #maxd = (secondary_h + h - secondary_f) / un[2]
    #maxd0z = (secondary_h + h - p1w0[2]) / un[2]
    maxd = h + f / math.sqrt(p1w0[0] ** 2 + p1w0[1] ** 2 + (un[2] * maxd0 - p1w0[2]) ** 2)
    # print('sh: ' + str(sh) + ' maxd: ' + str(maxd) + ' h0: ' + str(h0))

    p1n = (
        p1w0[0] + ureflected[0] * maxd0,
        p1w0[1] + ureflected[1] * maxd0,
        p1w0[2] + ureflected[2] * maxd0
    )

    pun = (
        p1w0[0] + un[0] * maxd,
        p1w0[1] + un[1] * maxd,
        p1w0[2] + un[2] * maxd
    )

    # print('p1n: ' + str(p1n))

    vertices = [
        p0,
        p1w0,
        pun,
        p1n,

        (p0[0] + e, p0[1] + e, p0[2] + e),
        (p1w0[0] + e, p1w0[1] + e, p1w0[2] + e),
        (pun[0] + e, pun[1] + e, pun[2] + e),
        (p1n[0] + e, p1n[1] + e, p1n[2] + e),

        (pun[0], pun[1], -2.0),
        (pun[0] + e, pun[1] + e, -2.0 + e),
    ]
    edges = [
        (0, 1),
    ]
    faces = [
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 6, 9, 8),
    ]

    nb_verts = len(vertices)
    p = 10
    czmax = far
    czstep = 10
    for cz in range(1, math.ceil(czmax / czstep) + 1):
        # print('### ' + str(cz))
        # print(str(len(vertices)))
        for i in range(0, p + 1):
            alpha = i * (2 * math.pi) / p
            idx = len(vertices)
            vertices.extend([
                (5 * r * math.cos(alpha), r * math.sin(alpha), cz * czstep)
            ])


            # print(str(len(vertices)) + ' vs ' + str(idx))

            if i > 0:
                edges.extend([(idx - 1, idx)])
            if i == p:
                edges.extend([(idx, idx - p)])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh


# f : focal length
# s : triangle side length
# t : triangle thickness
# h : walls height
# fw : fixation half width
# fd : fixation hole diameter
# p : precision in parts of 1
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
def create_triangle_mesh(f, s, t, h, fw, fd, p, x, y, z):
    mesh_name = 'trig_mesh' + str((f, s, t, h, fw, fd, p, x, y, z))
    mesh = bpy.data.meshes.new(mesh_name)
    # print('create_triangle_mesh: ' + str((f, s, t, h, fw, fd, p, x, y, z)))

    fr = 0.5 * fd

    v0 = hex2xyz(f, s, x, y, z, 0)
    v1 = hex2xyz(f, s, x, y, z, 1)
    v2 = hex2xyz(f, s, x, y, z, 2)

    vmid = (
        (v0[0] + v1[0] + v2[0]) / 3,
        (v0[1] + v1[1] + v2[1]) / 3,
        (v0[2] + v1[2] + v2[2]) / 3
    )

    vertices = []
    edges = []
    faces = []

    #global current_triangle_num
    #current_triangle_num += 1

    #bpy.ops.object.text_add()
    #bpy.context.object.data.body = str(current_triangle_num)
    #bpy.context.object.data.extrude = 0.02
    ##bpy.context.object.data.bevel_depth = 0.02
    ##bpy.context.object.data.bevel_resolution = 8
    #bpy.context.object.location.x = v0[0]
    #bpy.context.object.location.y = v0[1]
    #bpy.context.object.location.z = v0[2]
    #bpy.ops.transform.resize(value=(0, 0.1, 0))

    #bpy.context.view_layer.objects.active = mesh
    #bpy.ops.object.parent_set()

    #bpy.ops.object.convert(target='MESH', keep_original=False)
    #vertices.extend(bpy.context.object.data.vertices)

    #text_verts = []
    #for v in bpy.context.object.data.vertices:
        #vv = (v.co[0] + vmid[0], v.co[1] + vmid[1], v.co[2] + vmid[2])
        #print(str(vv))
        #text_verts.append(vv)

    #vertices.extend(text_verts)

    #text_edges = []
    #for ed in bpy.context.object.data.edges:
        # print(str(tuple(ed.vertices)))
        #text_edges.append(tuple(ed.vertices))

    #print(str(text_edges))
    #edges.extend(text_edges)

    #print(str(bpy.context.object.data.face_maps))
    #faces.extend(bpy.context.object.data.face_maps)
    #bpy.ops.object.delete()

    nb_verts_text = len(vertices)


    # print('triangle')

    vmid01 = (v0[0] + (v1[0] - v0[0]) / 2, v0[1] + (v1[1] - v0[1]) / 2, v0[2] + (v1[2] - v0[2]) / 2)
    vmid12 = (v1[0] + (v2[0] - v1[0]) / 2, v1[1] + (v2[1] - v1[1]) / 2, v1[2] + (v2[2] - v1[2]) / 2)
    vmid20 = (v2[0] + (v0[0] - v2[0]) / 2, v2[1] + (v0[1] - v2[1]) / 2, v2[2] + (v0[2] - v2[2]) / 2)

    dxvmid01mid = vmid[0] - vmid01[0]
    dyvmid01mid = vmid[1] - vmid01[1]
    dzvmid01mid = vmid[2] - vmid01[2]
    dvmid01mid = math.sqrt(dxvmid01mid * dxvmid01mid + dyvmid01mid * dyvmid01mid + dzvmid01mid * dzvmid01mid)
    vmid01mid = (dxvmid01mid / dvmid01mid, dyvmid01mid / dvmid01mid, dzvmid01mid / dvmid01mid)
    vmid12mid = ((vmid[0] - vmid12[0]) / dvmid01mid, (vmid[1] - vmid12[1]) / dvmid01mid, (vmid[2] - vmid12[2]) / dvmid01mid)
    vmid20mid = ((vmid[0] - vmid20[0]) / dvmid01mid, (vmid[1] - vmid20[1]) / dvmid01mid, (vmid[2] - vmid20[2]) / dvmid01mid)

    v01 = ((v1[0] - v0[0]) / r, (v1[1] - v0[1]) / r, (v1[2] - v0[2]) / r)
    v12 = ((v2[0] - v1[0]) / r, (v2[1] - v1[1]) / r, (v2[2] - v1[2]) / r)
    v20 = ((v0[0] - v2[0]) / r, (v0[1] - v2[1]) / r, (v0[2] - v2[2]) / r)

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

        (vmid01[0] + v01[0] * fw, vmid01[1] + v01[1] * fw, vmid01[2] + v01[2] * fw - t - h),
        (vmid01[0] - v01[0] * fw, vmid01[1] - v01[1] * fw, vmid01[2] - v01[2] * fw - t - h),

        (vmid01[0] + v01[0] * fw + vmid01mid[0] * t, vmid01[1] + v01[1] * fw + vmid01mid[1] * t, vmid01[2] + v01[2] * fw + vmid01mid[2] * t - t - h),
        (vmid01[0] - v01[0] * fw + vmid01mid[0] * t, vmid01[1] - v01[1] * fw + vmid01mid[1] * t, vmid01[2] - v01[2] * fw + vmid01mid[2] * t - t - h),

        (vmid01[0] + v01[0] * fw, vmid01[1] + v01[1] * fw, vmid01[2] + v01[2] * fw - t - h - 2 * fw),
        (vmid01[0] - v01[0] * fw, vmid01[1] - v01[1] * fw, vmid01[2] - v01[2] * fw - t - h - 2 * fw),

        (vmid01[0] + v01[0] * fw + vmid01mid[0] * t, vmid01[1] + v01[1] * fw + vmid01mid[1] * t, vmid01[2] + v01[2] * fw + vmid01mid[2] * t - t - h - 2 * fw),
        (vmid01[0] - v01[0] * fw + vmid01mid[0] * t, vmid01[1] - v01[1] * fw + vmid01mid[1] * t, vmid01[2] - v01[2] * fw + vmid01mid[2] * t - t - h - 2* fw),

        (vmid12[0] + v12[0] * fw, vmid12[1] + v12[1] * fw, vmid12[2] + v12[2] * fw - t - h),
        (vmid12[0] - v12[0] * fw, vmid12[1] - v12[1] * fw, vmid12[2] - v12[2] * fw - t - h),

        (vmid12[0] + v12[0] * fw + vmid12mid[0] * t, vmid12[1] + v12[1] * fw + vmid12mid[1] * t, vmid12[2] + v12[2] * fw + vmid12mid[2] * t - t - h),
        (vmid12[0] - v12[0] * fw + vmid12mid[0] * t, vmid12[1] - v12[1] * fw + vmid12mid[1] * t, vmid12[2] - v12[2] * fw + vmid12mid[2] * t - t - h),


        (vmid12[0] + v12[0] * fw, vmid12[1] + v12[1] * fw, vmid12[2] + v12[2] * fw - t - h - 2 * fw),
        (vmid12[0] - v12[0] * fw, vmid12[1] - v12[1] * fw, vmid12[2] - v12[2] * fw - t - h - 2 * fw),

        (vmid12[0] + v12[0] * fw + vmid12mid[0] * t, vmid12[1] + v12[1] * fw + vmid12mid[1] * t, vmid12[2] + v12[2] * fw + vmid12mid[2] * t - t - h - 2 * fw),
        (vmid12[0] - v12[0] * fw + vmid12mid[0] * t, vmid12[1] - v12[1] * fw + vmid12mid[1] * t, vmid12[2] - v12[2] * fw + vmid12mid[2] * t - t - h - 2* fw),

        (vmid20[0] + v20[0] * fw, vmid20[1] + v20[1] * fw, vmid20[2] + v20[2] * fw - t - h),
        (vmid20[0] - v20[0] * fw, vmid20[1] - v20[1] * fw, vmid20[2] - v20[2] * fw - t - h),

        (vmid20[0] + v20[0] * fw + vmid20mid[0] * t, vmid20[1] + v20[1] * fw + vmid20mid[1] * t, vmid20[2] + v20[2] * fw + vmid20mid[2] * t - t - h),
        (vmid20[0] - v20[0] * fw + vmid20mid[0] * t, vmid20[1] - v20[1] * fw + vmid20mid[1] * t, vmid20[2] - v20[2] * fw + vmid20mid[2] * t - t - h),


        (vmid20[0] + v20[0] * fw, vmid20[1] + v20[1] * fw, vmid20[2] + v20[2] * fw - t - h - 2 * fw),
        (vmid20[0] - v20[0] * fw, vmid20[1] - v20[1] * fw, vmid20[2] - v20[2] * fw - t - h - 2 * fw),

        (vmid20[0] + v20[0] * fw + vmid20mid[0] * t, vmid20[1] + v20[1] * fw + vmid20mid[1] * t, vmid20[2] + v20[2] * fw + vmid20mid[2] * t - t - h - 2 * fw),
        (vmid20[0] - v20[0] * fw + vmid20mid[0] * t, vmid20[1] - v20[1] * fw + vmid20mid[1] * t, vmid20[2] - v20[2] * fw + vmid20mid[2] * t - t - h - 2* fw),
    ])

    edges.extend([
        (nb_verts_text, nb_verts_text + 1),
        (nb_verts_text + 1, nb_verts_text + 2),
        (nb_verts_text + 2, nb_verts_text),

        (nb_verts_text + 3, nb_verts_text + 4),
        (nb_verts_text + 4, nb_verts_text + 5),
        (nb_verts_text + 5, nb_verts_text + 3),

        (nb_verts_text, nb_verts_text + 3),
        (nb_verts_text + 1, nb_verts_text + 4),
        (nb_verts_text + 2, nb_verts_text + 5),

        (nb_verts_text + 6, nb_verts_text + 7),
        (nb_verts_text + 7, nb_verts_text + 8),
        (nb_verts_text + 8, nb_verts_text + 6),

        (nb_verts_text + 3, nb_verts_text + 6),
        (nb_verts_text + 4, nb_verts_text + 7),
        (nb_verts_text + 5, nb_verts_text + 8),

        (nb_verts_text + 9, nb_verts_text + 10),
        (nb_verts_text + 10, nb_verts_text + 11),
        (nb_verts_text + 11, nb_verts_text + 9),

        (nb_verts_text + 6, nb_verts_text + 9),
        (nb_verts_text + 7, nb_verts_text + 10),
        (nb_verts_text + 8, nb_verts_text + 11),

        (nb_verts_text + 12, nb_verts_text + 13),
        (nb_verts_text + 13, nb_verts_text + 14),
        (nb_verts_text + 14, nb_verts_text + 12),

        (nb_verts_text + 9, nb_verts_text + 12),
        (nb_verts_text + 10, nb_verts_text + 13),
        (nb_verts_text + 11, nb_verts_text + 14),

        # 01
        (nb_verts_text + 15, nb_verts_text + 17),
        (nb_verts_text + 16, nb_verts_text + 18),

        (nb_verts_text + 19, nb_verts_text + 20),
        (nb_verts_text + 20, nb_verts_text + 22),
        (nb_verts_text + 21, nb_verts_text + 19),
        (nb_verts_text + 21, nb_verts_text + 22),

        (nb_verts_text + 15, nb_verts_text + 19),
        (nb_verts_text + 16, nb_verts_text + 20),
        (nb_verts_text + 17, nb_verts_text + 21),
        (nb_verts_text + 18, nb_verts_text + 22),

        # 12
        (nb_verts_text + 23, nb_verts_text + 25),
        (nb_verts_text + 24, nb_verts_text + 26),

        (nb_verts_text + 27, nb_verts_text + 28),
        (nb_verts_text + 28, nb_verts_text + 30),
        (nb_verts_text + 29, nb_verts_text + 27),
        (nb_verts_text + 29, nb_verts_text + 30),

        (nb_verts_text + 23, nb_verts_text + 27),
        (nb_verts_text + 24, nb_verts_text + 28),
        (nb_verts_text + 25, nb_verts_text + 29),
        (nb_verts_text + 26, nb_verts_text + 30),

        # 20
        (nb_verts_text + 31, nb_verts_text + 33),
        (nb_verts_text + 32, nb_verts_text + 34),

        (nb_verts_text + 35, nb_verts_text + 36),
        (nb_verts_text + 36, nb_verts_text + 38),
        (nb_verts_text + 37, nb_verts_text + 35),
        (nb_verts_text + 37, nb_verts_text + 38),

        (nb_verts_text + 31, nb_verts_text + 35),
        (nb_verts_text + 32, nb_verts_text + 36),
        (nb_verts_text + 33, nb_verts_text + 37),
        (nb_verts_text + 34, nb_verts_text + 38),
    ])

    faces.extend([
        (nb_verts_text, nb_verts_text + 1, nb_verts_text + 2),

        (nb_verts_text + 3, nb_verts_text + 4, nb_verts_text + 1, nb_verts_text),
        (nb_verts_text + 4, nb_verts_text + 5, nb_verts_text + 2, nb_verts_text + 1),
        (nb_verts_text + 5, nb_verts_text + 3, nb_verts_text, nb_verts_text + 2),

        (nb_verts_text + 6, nb_verts_text + 7, nb_verts_text + 4, nb_verts_text + 3),
        (nb_verts_text + 7, nb_verts_text + 8, nb_verts_text + 5, nb_verts_text + 4),
        (nb_verts_text + 8, nb_verts_text + 6, nb_verts_text + 3, nb_verts_text + 5),

        (nb_verts_text + 10, nb_verts_text + 9, nb_verts_text + 12, nb_verts_text + 13),
        (nb_verts_text + 11, nb_verts_text + 10, nb_verts_text + 13, nb_verts_text + 14),
        (nb_verts_text + 9, nb_verts_text + 11, nb_verts_text + 14, nb_verts_text + 12),

        (nb_verts_text + 12, nb_verts_text + 14, nb_verts_text + 13),

        (nb_verts_text + 6, nb_verts_text + 20, nb_verts_text + 16),
        (nb_verts_text + 9, nb_verts_text + 18, nb_verts_text + 22),
        (nb_verts_text + 6, nb_verts_text + 9, nb_verts_text + 22, nb_verts_text + 20),

        (nb_verts_text + 19, nb_verts_text + 20, nb_verts_text + 22, nb_verts_text + 21),

        (nb_verts_text + 7, nb_verts_text + 15, nb_verts_text + 19),
        (nb_verts_text + 10, nb_verts_text + 21, nb_verts_text + 17),
        (nb_verts_text + 10, nb_verts_text + 7, nb_verts_text + 19, nb_verts_text + 21),

        (nb_verts_text + 7, nb_verts_text + 28, nb_verts_text + 24),
        (nb_verts_text + 10, nb_verts_text + 26, nb_verts_text + 30),
        (nb_verts_text + 7, nb_verts_text + 10, nb_verts_text + 30, nb_verts_text + 28),

        (nb_verts_text + 27, nb_verts_text + 28, nb_verts_text + 30, nb_verts_text + 29),

        (nb_verts_text + 8, nb_verts_text + 23, nb_verts_text + 27),
        (nb_verts_text + 11, nb_verts_text + 29, nb_verts_text + 25),
        (nb_verts_text + 11, nb_verts_text + 8, nb_verts_text + 27, nb_verts_text + 29),

        (nb_verts_text + 8, nb_verts_text + 36, nb_verts_text + 32),
        (nb_verts_text + 11, nb_verts_text + 34, nb_verts_text + 38),
        (nb_verts_text + 8, nb_verts_text + 11, nb_verts_text + 38, nb_verts_text + 36),

        (nb_verts_text + 35, nb_verts_text + 36, nb_verts_text + 38, nb_verts_text + 37),

        (nb_verts_text + 6, nb_verts_text + 31, nb_verts_text + 35),
        (nb_verts_text + 9, nb_verts_text + 37, nb_verts_text + 33),
        (nb_verts_text + 9, nb_verts_text + 6, nb_verts_text + 35, nb_verts_text + 37),
    ])

    trig_h = (math.sqrt(3) / 6) * r
    trig_ih = trig_h - t

    c01 = (vmid01[0], vmid01[1], vmid01[2] - t - h - fw)
    lc01 = math.sqrt(c01[0] ** 2 + c01[1] ** 2 + c01[2] ** 2)
    c01n = (c01[0] / lc01, c01[1] / lc01, c01[2] / lc01)

    c12 = (vmid12[0], vmid12[1], vmid12[2] - t - h - fw)
    lc12 = math.sqrt(c12[0] ** 2 + c12[1] ** 2 + c12[2] ** 2)
    c12n = (c12[0] / lc12, c12[1] / lc12, c12[2] / lc12)

    c20 = (vmid20[0], vmid20[1], vmid20[2] - t - h - fw)
    lc20 = math.sqrt(c20[0] ** 2 + c20[1] ** 2 + c20[2] ** 2)
    c20n = (c20[0] / lc20, c20[1] / lc20, c20[2] / lc20)

    ltemp = math.sqrt(vmid01mid[0] ** 2 + vmid01mid[1] ** 2)
    nu01 = (
        vmid01mid[1] * v01[2] - vmid01mid[2] * v01[1],
        vmid01mid[2] * v01[0] - vmid01mid[0] * v01[2],
        vmid01mid[0] * v01[1] - vmid01mid[1] * v01[0],
    )

    nu12 = (
        vmid12mid[1] * v12[2] - vmid12mid[2] * v12[1],
        vmid12mid[2] * v12[0] - vmid12mid[0] * v12[2],
        vmid12mid[0] * v12[1] - vmid12mid[1] * v12[0],
    )

    nu20 = (
        vmid20mid[1] * v20[2] - vmid20mid[2] * v20[1],
        vmid20mid[2] * v20[0] - vmid20mid[0] * v20[2],
        vmid20mid[0] * v20[1] - vmid20mid[1] * v20[0],
    )

    # print('01 : n : ' + str(vmid01mid) + ' u: ' + str(v01) + ' n x u:' + str(nu01))
    # print('12 : n : ' + str(vmid12mid) + ' u: ' + str(v12) + ' n x u:' + str(nu12))
    # print('20 : n : ' + str(vmid20mid) + ' u: ' + str(v20) + ' n x u:' + str(nu20))

    nb_verts = len(vertices)
    vertices.extend([
        c01, (c01[0] + v01[0], c01[1] + v01[1], c01[2] + v01[2]), (c01[0] + nu01[0], c01[1] + nu01[1], c01[2] + nu01[2]), (c01[0] + vmid01mid[0], c01[1] + vmid01mid[1], c01[2] + vmid01mid[2]),
        c12, (c12[0] + v12[0], c12[1] + v12[1], c12[2] + v12[2]), (c12[0] + nu12[0], c12[1] + nu12[1], c12[2] + nu12[2]), (c12[0] + vmid12mid[0], c12[1] + vmid12mid[1], c12[2] + vmid12mid[2]),
        c20, (c20[0] + v20[0], c20[1] + v20[1], c20[2] + v20[2]), (c20[0] + nu20[0], c20[1] + nu20[1], c20[2] + nu20[2]), (c20[0] + vmid20mid[0], c20[1] + vmid20mid[1], c20[2] + vmid20mid[2]),
    ])

    edges.extend([
        #(nb_verts, nb_verts + 1), (nb_verts, nb_verts + 2), (nb_verts, nb_verts + 3),
        #(nb_verts + 4, nb_verts + 5), (nb_verts + 4, nb_verts + 6), (nb_verts + 4, nb_verts + 7),
        #(nb_verts + 8, nb_verts + 9), (nb_verts + 8, nb_verts + 10), (nb_verts + 8, nb_verts + 11),
    ])

    nb_verts = len(vertices)

    vfw0 = None
    vfw1 = None
    vfw2 = None
    vfw3 = None

    for i in range(0, p + 1):
        alpha = i * (2 * math.pi) / p

        rx01 = fr * math.cos(alpha) * v01[0] + fr * math.sin(alpha) * nu01[0]
        ry01 = fr * math.cos(alpha) * v01[1] + fr * math.sin(alpha) * nu01[1]
        rz01 = fr * math.cos(alpha) * v01[2] + fr * math.sin(alpha) * nu01[2]

        rx12 = fr * math.cos(alpha) * v12[0] + fr * math.sin(alpha) * nu12[0]
        ry12 = fr * math.cos(alpha) * v12[1] + fr * math.sin(alpha) * nu12[1]
        rz12 = fr * math.cos(alpha) * v12[2] + fr * math.sin(alpha) * nu12[2]

        rx20 = fr * math.cos(alpha) * v20[0] + fr * math.sin(alpha) * nu20[0]
        ry20 = fr * math.cos(alpha) * v20[1] + fr * math.sin(alpha) * nu20[1]
        rz20 = fr * math.cos(alpha) * v20[2] + fr * math.sin(alpha) * nu20[2]

        l01 = (
            c01[0] + rx01,
            c01[1] + ry01,
            c01[2] + rz01
        )

        r01 = (
            c01[0] + vmid01mid[0] * t + rx01,
            c01[1] + vmid01mid[1] * t + ry01,
            c01[2] + vmid01mid[2] * t + rz01
        )

        l12 = (
            c12[0] + rx12,
            c12[1] + ry12,
            c12[2] + rz12
        )

        r12 = (
            c12[0] + vmid12mid[0] * t + rx12,
            c12[1] + vmid12mid[1] * t + ry12,
            c12[2] + vmid12mid[2] * t + rz12
        )

        l20 = (
            c20[0] + rx20,
            c20[1] + ry20,
            c20[2] + rz20
        )

        r20 = (
            c20[0] + vmid20mid[0] * t + rx20,
            c20[1] + vmid20mid[1] * t + ry20,
            c20[2] + vmid20mid[2] * t + rz20
        )

        idx = nb_verts + i * 6

        vertices.extend([l01, r01, l12, r12, l20, r20])
        edges.extend([
            (idx, idx + 1),
            (idx + 2, idx + 3),
            (idx + 4, idx + 5),
        ])

        if i > 0:
            edges.extend([
                (idx - 6, idx),
                (idx - 5, idx + 1),
                (idx - 4, idx + 2),
                (idx - 3, idx + 3),
                (idx - 2, idx + 4),
                (idx - 1, idx + 5),
            ])

            faces.extend([
                (idx, idx - 6, idx - 5, idx + 1),
                (idx + 2, idx - 4, idx - 3, idx + 3),
                (idx + 4, idx - 2, idx - 1, idx + 5),
            ])

            if alpha < math.pi / 2:
                faces.extend([
                    (19, idx - 6, idx),
                    (21, idx + 1, idx - 5),
                    (27, idx - 4, idx + 2),
                    (29, idx + 3, idx - 3),
                    (35, idx - 2, idx + 4),
                    (37, idx + 5, idx - 1),
                ])
                if vfw0 == None:
                    vfw0 = idx - 6
            elif alpha < math.pi:
                faces.extend([
                    (20, idx - 6, idx),
                    (22, idx + 1, idx - 5),
                    (28, idx - 4, idx + 2),
                    (30, idx + 3, idx - 3),
                    (36, idx - 2, idx + 4),
                    (38, idx + 5, idx - 1),
                ])
                if vfw1 == None:
                    vfw1 = idx - 6
            elif alpha < 3 * (math.pi / 2):
                faces.extend([
                    (16, idx - 6, idx),
                    (18, idx + 1, idx - 5),
                    (24, idx - 4, idx + 2),
                    (26, idx + 3, idx - 3),
                    (32, idx - 2, idx + 4),
                    (34, idx + 5, idx - 1),
                ])
                if vfw2 == None:
                    vfw2 = idx - 6
            else:
                faces.extend([
                    (15, idx - 6, idx),
                    (17, idx + 1, idx - 5),
                    (23, idx - 4, idx + 2),
                    (25, idx + 3, idx - 3),
                    (31, idx - 2, idx + 4),
                    (33, idx + 5, idx - 1),
                ])
                if vfw3 == None:
                    vfw3 = idx - 6
    faces.extend([
        (19, vfw1, 20),
        (22, vfw1 + 1, 21),
        (27, vfw1 + 2, 28),
        (30, vfw1 + 3, 29),
        (35, vfw1 + 4, 36),
        (38, vfw1 + 5, 37),
        (20, vfw2, 16),
        (18, vfw2 + 1, 22),
        (28, vfw2 + 2, 24),
        (26, vfw2 + 3, 30),
        (36, vfw2 + 4, 32),
        (34, vfw2 + 5, 38),
        (16, vfw3, 15),
        (17, vfw3 + 1, 18),
        (24, vfw3 + 2, 23),
        (25, vfw3 + 3, 26),
        (32, vfw3 + 4, 31),
        (33, vfw3 + 5, 34),
        (15, vfw0, 19),
        (21, vfw0 + 1, 17),
        (23, vfw0 + 2, 27),
        (29, vfw0 + 3, 25),
        (31, vfw0 + 4, 35),
        (37, vfw0 + 5, 33),
    ])

    # print(vfw1)

    # print('trig mesh' + str(vertices) + ' ' + str(edges) + ' ' + str(faces))


    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh


# r: external radius
# t: thickness
# h: height
# rp: circles precision
# hp: number of inner circles
def create_arm_mesh(r, t, h, rp, hp):
    mesh = bpy.data.meshes.new('arm_' + str((r, t, h, rp, hp)))

    vertices = []
    edges = []
    faces = []

    hs = h / (hp + 1)
    ri = r - t

    nb_verts = len(vertices)

    for i in range(0, hp + 2):
        for j in range(0, rp + 1):
            alpha = j * math.tau / rp

            nbidx = 2

            trv = nb_verts + i * nbidx * (rp + 1) + j * nbidx
            trvi = trv + 1
            tlv = trv - nbidx
            tlvi = tlv + 1

            brv = trv - nbidx * (rp + 1)
            brvi = brv + 1
            blv = brv - nbidx
            blvi = blv + 1

            vertices.extend([
                (r * math.cos(alpha), r * math.sin(alpha), hs * i),
                (ri * math.cos(alpha), ri * math.sin(alpha), hs * i),
            ])

            if i == 0 or i == hp + 1:
                edges.extend([
                    #(trv, trvi),
                ])

                if j > 0:
                    if i == 0:
                        faces.extend([
                            (trvi, trv, tlv, tlvi),
                        ])
                    else:
                        faces.extend([
                            (trv, trvi, tlvi, tlv),
                        ])


            if j > 0 and i > 0:
                faces.extend([
                    (blv, brv, trv, tlv),
                    (brvi, blvi, tlvi, trvi),
                ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

# e: margin
# t: head thickness arround arms
# h: head height
# d: distance between arms
# arm_r: arm radius
# arm_rp: arm circles precision
# spider_thickness: spider leg thickness
# spider_length: spider leg length
def create_arm_head_mesh(e, t, h, arm_d, arm_r, arm_rp, spider_thickness, spider_length):
    mesh = bpy.data.meshes.new('arm_head_' + str((
        e, t, h,
        arm_d, arm_r, arm_rp,
        spider_thickness, spider_length
    )))

    pi4 = math.pi / 4

    hd = 0.5 * arm_d
    hst = 0.5 * spider_thickness
    hsl = 0.5 * spider_length

    ri = arm_r + e
    re = ri + t

    vertices = [
        (0, -hd + re, 0),
        (0, hd - re, 0),

        (re, -hd, 0),
        (re, hd, 0),

        (-re, hd, 0),
        (-re, -hd, 0),

        (0, -hd + re, -h),
        (0, hd - re, -h),

        # 8
        (re, -hd, -h),
        (re, hd, -h),

        (-re, hd, -h),
        (-re, -hd, -h),

        (ri * math.cos(pi4), -hd + ri * math.sin(pi4), 0),
        (ri * math.cos(pi4), hd - ri * math.sin(pi4), 0),

        (ri * math.cos(pi4), -hd + ri * math.sin(pi4), -h),
        (ri * math.cos(pi4), hd - ri * math.sin(pi4), -h),

        # 16
        (ri * math.cos(3 * pi4), -hd + ri * math.sin(3 * pi4), 0),
        (ri * math.cos(3 * pi4), hd - ri * math.sin(3 * pi4), 0),

        (ri * math.cos(3 * pi4), -hd + ri * math.sin(3 * pi4), -h),
        (ri * math.cos(3 * pi4), hd - ri * math.sin(3 * pi4), -h),

        (-re, -hst, 0),
        (-re, hst, 0),

        (-re, -hst, -h - t),
        (-re, hst, -h - t),

        # 24
        (0, -hst, -h - t),
        (0, hst, -h - t),

        (re, -hst, 0),
        (re, hst, 0),

        (re, -hst, -h),
        (re, hst, -h),

        (-re - spider_length, -hst, 0),
        (-re - spider_length, hst, 0),

        # 32
        (-re - spider_length, -hst, -h),
        (-re - spider_length, hst, -h),

        (-re - hsl, -hst, -h),
        (-re - hsl, hst, -h),
    ]

    edges = []

    faces = [
        (0, 2, 3, 1),
        (5, 0, 1, 4),

        (8, 6, 24, 28),
        (25, 7, 9, 29),
        (24, 6, 11, 22),
        (7, 25, 23, 10),
        (28, 24, 25, 29),
        (24, 22, 23, 25),

        (21, 4, 10, 23),
        (5, 20, 22, 11),

        (30, 20, 21, 31),
        (22, 34, 35, 23),
        (30, 31, 33, 32),
        (34, 32, 33, 35),
        (20, 30, 32, 28),
        (22, 28, 34),
        (31, 21, 29, 33),
        (29, 23, 35),

        (9, 3, 2, 8),

        (0, 12, 2),
        (3, 13, 1),
        (8, 14, 6),
        (7, 15, 9),

        (5, 16, 0),
        (1, 17, 4),
        (6, 18, 11),
        (10, 19, 7),
    ]

    nb_verts = len(vertices)

    for i in range(0, arm_rp + 1):
        alpha = i * math.pi / arm_rp
        beta = 0 + alpha

        cb = math.cos(beta)
        sb = math.sin(beta)

        recb = re * cb
        resb = re * sb

        ricb = ri * cb
        risb = ri * sb

        nbidx = 12

        trv = nb_verts + i * nbidx
        tlv = trv + 1
        brv = trv + 2
        blv = trv + 3

        trvi = trv + 4
        tlvi = trv + 5
        brvi = trv + 6
        blvi = trv + 7

        trvii = trv + 8
        tlvii = trv + 9
        brvii = trv + 10
        blvii = trv + 11

        vertices.extend([
            (recb, -hd - resb, 0),
            (recb, hd + resb, 0),

            (recb, -hd - resb, -h),
            (recb, hd + resb, -h),

            (ricb, -hd - risb, 0),
            (ricb, hd + risb, 0),

            (ricb, -hd - risb, -h),
            (ricb, hd + risb, -h),

            (ricb, -hd + risb, 0),
            (ricb, hd - risb, 0),

            (ricb, -hd + risb, -h),
            (ricb, hd - risb, -h),
        ])

        if i > 0:
            faces.extend([
                (trv - nbidx, trv, brv, brv - nbidx),
                (tlv, tlv - nbidx, blv - nbidx, blv),

                (trvi, trvi - nbidx, brvi - nbidx, brvi),
                (tlvi - nbidx, tlvi, blvi, blvi - nbidx),

                (trvi, trv, trv - nbidx, trvi - nbidx),
                (tlv, tlvi, tlvi - nbidx, tlv - nbidx),

                (brv, brvi, brvi - nbidx, brv - nbidx),
                (blvi, blv, blv - nbidx, blvi - nbidx),

                (trvii - nbidx, trvii, brvii, brvii - nbidx),
                (tlvii, tlvii - nbidx, blvii - nbidx, blvii),
            ])

            if alpha < pi4:
                faces.extend([
                    (trvii - nbidx, 2, trvii),
                    (tlvii - nbidx, tlvii, 3),

                    (brvii - nbidx, brvii, 8),
                    (blvii - nbidx, 9, blvii),
                ])
            elif alpha < 3 * pi4:
                faces.extend([
                    (trvii - nbidx, 0, trvii),
                    (tlvii - nbidx, tlvii, 1),

                    (brvii - nbidx, brvii, 6),
                    (blvii - nbidx, 7, blvii),
                ])
            else:
                faces.extend([
                    (trvii - nbidx, 5, trvii),
                    (tlvii - nbidx, tlvii, 4),

                    (brvii - nbidx, brvii, 11),
                    (blvii - nbidx, 10, blvii),
                ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

# t: thickness
# rx: secondary mirror radius along x in secondary mirror plane
# ry: secondary mirror radius along y in secondary mirror plane
# rp: circles precision
def create_newton_secondary_mirror_mesh(t, rx, ry, rp):
    mesh = bpy.data.meshes.new('newton_secondary_' + str((t, rx, ry, rp)))

    pi4m = -math.pi / 4
    cpi4m = math.cos(pi4m)
    spi4m = math.sin(pi4m)

    vertices = [
        (0, 0, t),
        (0, 0, 0),
    ]
    edges = []
    faces = []

    nb_verts = len(vertices)

    for i in range(0, rp + 1):
        alpha = i * math.tau / rp

        x = rx * math.cos(alpha)
        y = ry * math.sin(alpha)

        xi = (rx - t) * math.cos(alpha)
        yi = (ry - t) * math.sin(alpha)

        z = 0

        nbidx = 5
        trv = nb_verts + nbidx * i
        brv = trv + 1
        rrv = trv + 2
        ritrv = trv + 3
        ribrv = trv + 4
        tlv = trv - nbidx
        blv = brv - nbidx
        rlv = rrv - nbidx
        ritlv = ritrv - nbidx
        riblv = ribrv - nbidx

        vertices.extend([
            (x * cpi4m + z * spi4m, y, x * -spi4m + z * cpi4m + t),
            (x * cpi4m + z * spi4m, y, x * -spi4m + z * cpi4m),
            (x * cpi4m + z * spi4m, y, rx * cpi4m + t),
            (xi * cpi4m + z * spi4m, yi, rx * cpi4m + t),
            (xi * cpi4m + z * spi4m, yi, xi * -spi4m + z * cpi4m + t),
        ])

        edges.extend([
            (trv, brv),
            (trv, rrv),
            (ritrv, ribrv),
        ])

        if i > 0:
            edges.extend([
                (trv, tlv),
                (brv, blv),
                (rrv, rlv),
                (ritrv, ritlv),
                (ribrv, riblv),
            ])

            faces.extend([
                (trv, tlv, blv, brv),
                (1, brv, blv),
                (trv, rrv, rlv, tlv),
                (rrv, ritrv, ritlv, rlv),
                (ritrv, ritlv, riblv, ribrv),
                (0, ribrv, riblv),
            ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

# t: thickness
# st: spider arm thickness
# sw: spider arm length
# f: secondary mirror focal length
# r: secondary mirror radius
# rp: circles precision
# arm_n: number of spider arms
def create_spherical_secondary_mirror_mesh(t, f, r, rp):
    mesh = bpy.data.meshes.new('secondary_' + str((t, f, r, rp)))

    vertices = []
    edges = []
    faces = []

    nb_verts = len(vertices)

    for sr in range(0, rp + 1):
        x = r - sr * r / rp
        z = spherical_z(f, r, x)

        for i in range(0, rp + 1):
            alpha = i * math.tau / rp

            nbidx = 2
            tv = nb_verts + sr * (rp + 1) * nbidx + nbidx * i
            bv = tv + 1
            utv = nb_verts + (sr - 1) * (rp + 1) * nbidx + nbidx * i
            ubv = utv + 1

            vertices.extend([
                (x * math.cos(alpha), x * math.sin(alpha), z + t),
                (x * math.cos(alpha), x * math.sin(alpha), z),
            ])

            if i > 0:
                edges.extend([
                    (tv, tv - nbidx),
                    (bv, bv - nbidx),
                ])

                if sr == 0:
                    faces.extend([
                        (tv, tv - nbidx, bv - nbidx, bv),
                    ])
                elif sr > 0:
                    faces.extend([
                        (tv, tv - nbidx, utv - nbidx, utv),
                        (bv - nbidx, bv, ubv, ubv - nbidx),
                    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

hex_collection = bpy.data.collections.new('hex_collection')
bpy.context.scene.collection.children.link(hex_collection)

hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]
prev_hexes = [(0, 0)]
curr_hexes = []
hexes = prev_hexes

if support_secondary_is_newton:
    half_hex.create_object(e, f, r, h, trig_h, 0, 0, 0)
    half_hex.create_object(e, f, r, h, trig_h, 0, 0, 3)

for i in range(0, n + 1):
    for j in range(0, len(prev_hexes)):
        for l in range(0, len(hex_arrows)):
            x = prev_hexes[j][0] + hex_arrows[l][0]
            y = prev_hexes[j][1] + hex_arrows[l][1]

            if (x, y) in hexes or (x, y) in curr_hexes:
                continue

            half_hex.create_object(e, f, r, h, trig_h, x, y, 0)
            half_hex.create_object(e, f, r, h, trig_h, x, y, 3)

            curr_hexes.append((x, y))
    prev_hexes = curr_hexes
    hexes.extend(curr_hexes)
    curr_hexes = []

ray_collection = bpy.data.collections.new('ray_collection')
bpy.context.scene.collection.children.link(ray_collection)

for i in range(0, len(hexes)):
    e = 0.05
    normal_mesh = create_primary_mirror_normal(
        e,
        f,
        r,
        hexes[i][0],
        hexes[i][1],
        0
    )

    normal_object = bpy.data.objects.new('primary_mirror_normal_' + str(hexes[i][0]) + '_' + str(hexes[i][1]) + '_0', normal_mesh)
    ray_collection.objects.link(normal_object)

    if not support_secondary_is_newton:
        ray_mesh = create_spherical_rays(
            e,
            support_spherical_secondary_z,
            support_spherical_secondary_r,
            support_spherical_secondary_f,
            hexes[i][0],
            hexes[i][1],
            0,
            f,
            r
        )
        ray_object = bpy.data.objects.new('ray_' + str(hexes[i][0]) + '_' + str(hexes[i][1]) + '_0', ray_mesh)
        ray_collection.objects.link(ray_object)

arm_mesh = create_arm_mesh(
    support_arm_r,
    support_arm_t,
    support_arm_h,
    support_arm_rp,
    support_arm_hp
)

arm_block_mesh = support_arm_block.create_mesh(
    support_arm_block_e,
    support_arm_block_f,
    support_arm_block_n,
    support_arm_block_r,
    support_arm_block_t,
    support_arm_block_m,
    support_arm_block_p,
    support_arm_block_hex_thickness,
    support_arm_block_hex_walls_height,
    support_arm_block_hex_primary_thickness,
    support_arm_block_arm_radius
)

arm_head_mesh = create_arm_head_mesh(
    support_arm_head_e,
    support_arm_head_t,
    support_arm_head_h,
    support_arm_head_arm_d,
    support_arm_head_arm_r,
    support_arm_head_arm_rp,
    support_arm_spider_thickness,
    support_arm_spider_length
)

if support_secondary_is_newton:
    secondary_mesh = create_newton_secondary_mirror_mesh(
        support_newton_secondary_t,
        support_newton_secondary_rx,
        support_newton_secondary_ry,
        support_newton_secondary_rp
    )
else:
    secondary_mesh = create_spherical_secondary_mirror_mesh(
        support_spherical_secondary_t,
        support_spherical_secondary_f,
        support_spherical_secondary_r,
        support_spherical_secondary_rp
    )

arm_collection = bpy.data.collections.new('arm_collection')
bpy.context.scene.collection.children.link(arm_collection)

for z in range(0, support_arm_nz):
    for i in range(0, len(support_arm_points)):
        alpha = i * math.tau / support_arm_n
        beta = support_arm_omega + alpha
        rot = Euler((0, 0, beta), 'XYZ')

        sz = support_arm_z + z * (support_arm_h + support_arm_e)

        if z == 0:
            arm_block = bpy.data.objects.new(
                'arm_block_' + str(support_arm_block_n) + '_' + str(i),
                arm_block_mesh
            )
            arm_block.rotation_euler = rot
            arm_collection.objects.link(arm_block)

        arm_object_l = bpy.data.objects.new('arm_' + str(i) + '_l', arm_mesh)
        arm_collection.objects.link(arm_object_l)

        arm_object_l.location.x = support_arm_points[i][0][0]
        arm_object_l.location.y = support_arm_points[i][0][1]
        arm_object_l.location.z = sz

        arm_object_r = bpy.data.objects.new('arm_' + str(i) + '_r', arm_mesh)
        arm_collection.objects.link(arm_object_r)

        arm_object_r.location.x = support_arm_points[i][1][0]
        arm_object_r.location.y = support_arm_points[i][1][1]
        arm_object_r.location.z = sz

        if z != support_arm_nz - 1:
            continue

        arm_head_object = bpy.data.objects.new('arm_head_' + str(i), arm_head_mesh)
        arm_collection.objects.link(arm_head_object)

        arm_head_object.location.x = 0.5 * (support_arm_points[i][0][0] + support_arm_points[i][1][0])
        arm_head_object.location.y = 0.5 * (support_arm_points[i][0][1] + support_arm_points[i][1][1])
        arm_head_object.location.z = support_arm_head_z
        arm_head_object.rotation_euler = rot

secondary_object = bpy.data.objects.new(support_secondary_final_name, secondary_mesh)
arm_collection.objects.link(secondary_object)
secondary_object.location.z = support_secondary_z

# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\support_", check_existing=True, filter_glob='*.stl', use_selection=False, global_scale=100.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z')

print("\nDONE\n\n\n")