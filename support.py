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
from meshes import \
    primary_mirror_normals, \
        half_hex, \
    secondary_mirror_spherical, \
        secondary_mirror_spherical_rays, \
        secondary_mirror_newton, \
    support_arm_block, \
        support_arm, \
        support_arm_head \

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
    normal_mesh = primary_mirror_normals.create_mesh(
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
        ray_mesh = secondary_mirror_spherical_rays.create_mesh(
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

arm_mesh = support_arm.create_mesh(
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

arm_head_mesh = support_arm_head.create_mesh(
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
    secondary_mesh = secondary_mirror_newton.create_mesh(
        support_newton_secondary_t,
        support_newton_secondary_rx,
        support_newton_secondary_ry,
        support_newton_secondary_rp
    )
else:
    secondary_mesh = secondary_mirror_spherical.create_mesh(
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