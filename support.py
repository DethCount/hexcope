import os
import sys
import importlib
import bpy
import math
from mathutils import Euler, Matrix

sys.dont_write_bytecode = 1
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )

from hyperparameters import n, r, h, f, e, trig_h, \
    primary_t, support_secondary_is_newton, \
    clip_depth, clip_thickness, clip_height, clip_e

from optics import hex2xyz, \
    get_right_boundary_hex_xyz, \
    get_support_arm_points, \
    get_newton_dist_to_spider_arm, \
    get_spherical_dist_to_spider_arm

from meshes import \
    screw, \
        basis_cap, \
    ray, \
    primary_mirror_normals, \
        half_hex, \
    secondary_mirror_spherical, \
        secondary_mirror_spherical_rays, \
        secondary_mirror_newton, \
        secondary_mirror_newton_rays, \
    support_arm_block, \
        support_arm, \
        support_arm_head, \
    spider_arm

importlib.reload(screw)
importlib.reload(basis_cap)
importlib.reload(primary_mirror_normals)
importlib.reload(half_hex)
importlib.reload(secondary_mirror_spherical)
importlib.reload(secondary_mirror_newton)
importlib.reload(support_arm_block)
importlib.reload(support_arm)
importlib.reload(support_arm_head)
importlib.reload(spider_arm)

if bpy.context.scene.objects.get('Camera'):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

current_triangle_num = 0
trig_name = 'tri'
draw_rays = True

support_half_hex_e = 0.0015
support_half_hex_f = f
support_half_hex_s = r
support_half_hex_t = h
support_half_hex_it = 0.25 * support_half_hex_t
support_half_hex_walls_height = trig_h
support_half_hex_font_size = 0.01
support_half_hex_font_extrusion = 0.001
support_half_hex_clip_depth = clip_depth
support_half_hex_clip_height = clip_height
support_half_hex_clip_thickness = clip_thickness
support_half_hex_clip_e = clip_e

support_primary_z = -hex2xyz(f, r, 0, 0, 0, 0)[2]

support_spider_rp = 25 # precision
support_spider_r = 0.005
support_spider_screw_length = 0.008
support_spider_D = 0.008
support_spider_P = None
# print(screw.get_P(support_spider_D))
support_spider_screw_end_h = support_spider_D

support_secondary_z = support_half_hex_t + (1.25 if n == 0 else 1.1)

support_secondary_t = support_spider_r + support_spider_screw_length + support_spider_screw_end_h

support_spherical_secondary_name = 'spherical_secondary_mirror'
support_spherical_secondary_t = support_secondary_t
support_spherical_secondary_z = support_secondary_z + support_spherical_secondary_t
support_spherical_secondary_r = r
support_spherical_secondary_f = 10.0 * r
support_spherical_secondary_rp = 100

support_newton_secondary_name = 'newton_secondary_mirror'
support_newton_secondary_t = 0.002
support_newton_secondary_top_t = support_secondary_t
support_newton_secondary_rx = 0.05 if n == 0 else r
support_newton_secondary_ry = support_newton_secondary_rx
support_newton_secondary_rp = 25
support_newton_secondary_z = support_secondary_z \
    + support_newton_secondary_rx * math.cos(-0.25 * math.pi) \
    + 0.5 * support_newton_secondary_top_t
print('newton sec z', str(support_newton_secondary_z))

support_arm_e = e
support_arm_h = 0.2
support_arm_outer_r = 0.01
support_arm_inner_r = 0.007
support_arm_screw_length = 0.02
support_arm_precision = 50
support_arm_D = screw.get_D(2 * support_arm_inner_r)
support_arm_P = screw.get_P(support_arm_D)

support_arm_n = 6 # should be 1, 2, 3 or 6
support_arm_omega = 0
support_arm_points = get_support_arm_points(
    n,
    r,
    support_arm_n,
    support_arm_omega
)
support_arm_d = math.sqrt(
    support_arm_points[0][1][0] ** 2
    + support_arm_points[0][1][1] ** 2
)
support_arm_rld = math.sqrt(
    (support_arm_points[0][1][0] - support_arm_points[0][0][0]) ** 2 \
    + (support_arm_points[0][1][1] - support_arm_points[0][0][1]) ** 2
)
support_arm_outer_length = support_arm_h - support_arm_screw_length

support_secondary_final_name = support_spherical_secondary_name
support_secondary_final_t = support_spherical_secondary_t
support_secondary_final_z = support_spherical_secondary_z
support_secondary_final_dist_to_spider_arm = list()

if support_secondary_is_newton:
    support_secondary_final_name = support_newton_secondary_name
    support_secondary_final_t = support_newton_secondary_t
    support_secondary_final_z = support_newton_secondary_z
    support_secondary_final_dist_to_spider_arm = get_newton_dist_to_spider_arm(
        support_arm_n,
        support_newton_secondary_rx,
        support_newton_secondary_ry
    )
else:
    support_secondary_final_dist_to_spider_arm = get_spherical_dist_to_spider_arm(
        support_arm_n,
        support_spherical_secondary_r
    )

support_arm_block_e = e
support_arm_block_f = f
support_arm_block_n = n
support_arm_block_r = r
support_arm_block_t = h
support_arm_block_wl = 0.017
support_arm_block_p = 50
support_arm_block_hex_thickness = support_half_hex_t
support_arm_block_hex_interior_thickness = support_half_hex_it
support_arm_block_hex_walls_height = trig_h
support_arm_block_hex_primary_thickness = primary_t
support_arm_block_arm_radius = support_arm_outer_r
support_arm_block_clip_depth = support_half_hex_clip_depth
support_arm_block_clip_thickness = support_half_hex_clip_thickness
support_arm_block_clip_height = support_half_hex_clip_height
support_arm_block_clip_e = support_half_hex_clip_e
support_arm_block_clip_padding_x = 0.004
support_arm_block_clip_padding_z = 0
support_arm_blocking_screw_r = support_arm_block_arm_radius
support_arm_blocking_screw_length = support_arm_block_t - 0.004
support_arm_blocking_screw_rp = support_arm_block_p
support_arm_blocking_screw_D = None
support_arm_blocking_screw_P = None
support_arm_blocking_screw_tip_r = 0.5 * support_arm_blocking_screw_r
support_arm_blocking_screw_tip_length = 0.001
support_arm_block_z = support_primary_z
support_arm_block_total_z = get_right_boundary_hex_xyz(support_arm_block_f, support_arm_block_n, support_arm_block_r)[2]

support_arm_block_screw_cap_r = support_arm_blocking_screw_r
support_arm_block_screw_cap_t = 0.003
support_arm_block_screw_cap_cap_h = 0.005
support_arm_block_screw_cap_h = support_arm_block_screw_cap_cap_h
support_arm_block_screw_cap_rp = support_arm_blocking_screw_rp
support_arm_block_screw_cap_z_screw_start = 0
support_arm_block_screw_cap_head_r = support_arm_block_screw_cap_r + 0.003

support_arm_head_t = 0.005
support_arm_head_p = 25
support_arm_head_with_spider_screw = True
support_arm_head_with_spider_screw_in = False
support_arm_head_with_top_screw = False
support_arm_head_with_bottom_screw = True
support_arm_head_ocular_r = 0.0255
support_arm_head_arm_dist = support_arm_rld
support_arm_head_arm_rp = support_arm_precision
support_arm_head_arm_outer_r = support_arm_outer_r
support_arm_head_arm_inner_r = support_arm_inner_r
support_arm_head_arm_screw_length = support_arm_screw_length
support_arm_head_arm_D = support_arm_D
support_arm_head_arm_P = support_arm_P
support_arm_head_arm_screw_in_length = support_arm_head_arm_screw_length + 2 * support_arm_P
support_arm_head_arm_screw_in_end_h = 2 * support_arm_P
support_arm_head_min_height = support_arm_head_t + support_arm_head_arm_screw_in_length + support_arm_head_arm_screw_in_end_h
support_arm_head_height = 0.5 * support_arm_head_min_height + (support_secondary_final_z - support_secondary_z) + support_arm_head_ocular_r + 2 * support_arm_head_t
support_arm_head_width = 2 * (support_arm_head_arm_outer_r + support_arm_head_t)
support_arm_head_spider_rp = support_spider_rp
support_arm_head_spider_r = support_spider_r
support_arm_head_spider_screw_length = support_spider_screw_length
support_arm_head_spider_screw_z = 0.5 * support_arm_head_min_height
support_arm_head_spider_screw_z_with_ocular = support_arm_head_height - 0.5 * support_arm_head_min_height
support_arm_head_ocular_z = support_arm_head_spider_screw_z_with_ocular - (support_secondary_final_z - support_secondary_z)
support_arm_head_spider_D = support_spider_D
support_arm_head_spider_P = support_spider_P
support_arm_head_spider_screw_end_h = support_spider_screw_end_h

support_arm_nz = math.ceil((support_secondary_final_z - support_arm_block_total_z - support_arm_head_min_height + 0.5 * support_arm_outer_length) / support_arm_outer_length)
support_arm_nz_with_ocular = math.ceil((support_secondary_final_z - support_arm_block_total_z - support_arm_head_height + 0.5 * support_arm_outer_length) / support_arm_outer_length)
support_arm_z = support_secondary_final_z \
    - support_arm_head_min_height \
    + support_arm_head_spider_screw_z \
    - support_arm_nz * support_arm_outer_length \
    - (math.ceil(0.5 * support_arm_nz) - 1) * support_arm_head_min_height
support_arm_z_with_ocular = support_secondary_final_z \
    - support_arm_head_height \
    + support_arm_head_spider_screw_z \
    - support_arm_nz_with_ocular * support_arm_outer_length \
    - (math.ceil(0.5 * support_arm_nz_with_ocular) - 1) * support_arm_head_min_height

hex_collection = bpy.data.collections.new('hex_collection')
bpy.context.scene.collection.children.link(hex_collection)

hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]
prev_hexes = [(0, 0)]
curr_hexes = []
hexes = prev_hexes

if support_secondary_is_newton:
    half_hex.create_object(
        support_half_hex_e,
        support_half_hex_f,
        support_half_hex_s,
        support_half_hex_t,
        support_half_hex_it,
        support_half_hex_walls_height,
        support_half_hex_font_size,
        support_half_hex_font_extrusion,
        0,
        0,
        0,
        support_half_hex_clip_depth,
        support_half_hex_clip_height,
        support_half_hex_clip_thickness,
        support_half_hex_clip_e
    )
    half_hex.create_object(
        support_half_hex_e,
        support_half_hex_f,
        support_half_hex_s,
        support_half_hex_t,
        support_half_hex_it,
        support_half_hex_walls_height,
        support_half_hex_font_size,
        support_half_hex_font_extrusion,
        0,
        0,
        3,
        support_half_hex_clip_depth,
        support_half_hex_clip_height,
        support_half_hex_clip_thickness,
        support_half_hex_clip_e
    )

for i in range(0, n + 1):
    for j in range(0, len(prev_hexes)):
        for l in range(0, len(hex_arrows)):
            x = prev_hexes[j][0] + hex_arrows[l][0]
            y = prev_hexes[j][1] + hex_arrows[l][1]

            if (x, y) in hexes or (x, y) in curr_hexes:
                continue

            half_hex.create_object(
                support_half_hex_e,
                support_half_hex_f,
                support_half_hex_s,
                support_half_hex_t,
                support_half_hex_it,
                support_half_hex_walls_height,
                support_half_hex_font_size,
                support_half_hex_font_extrusion,
                x,
                y,
                0,
                support_half_hex_clip_depth,
                support_half_hex_clip_height,
                support_half_hex_clip_thickness,
                support_half_hex_clip_e
            )

            half_hex.create_object(
                support_half_hex_e,
                support_half_hex_f,
                support_half_hex_s,
                support_half_hex_t,
                support_half_hex_it,
                support_half_hex_walls_height,
                support_half_hex_font_size,
                support_half_hex_font_extrusion,
                x,
                y,
                3,
                support_half_hex_clip_depth,
                support_half_hex_clip_height,
                support_half_hex_clip_thickness,
                support_half_hex_clip_e
            )

            curr_hexes.append((x, y))
    prev_hexes = curr_hexes
    hexes.extend(curr_hexes)
    curr_hexes = []

if draw_rays:
    ray_collection = bpy.data.collections.new('ray_collection')
    bpy.context.scene.collection.children.link(ray_collection)
    primary_ray_collection = bpy.data.collections.new('primary_collection')
    ray_collection.children.link(primary_ray_collection)
    secondary_ray_collection = bpy.data.collections.new('secondary_collection')
    ray_collection.children.link(secondary_ray_collection)

    for i in range(0, len(hexes)):
        primary_ray = primary_mirror_normals.create_ray(
            f,
            r,
            hexes[i][0],
            hexes[i][1],
            0
        )

        primary_ray_mesh = ray.create_mesh(primary_ray[0], primary_ray[1], 0.005)

        primary_ray_object = bpy.data.objects.new('primary_mirror_normal_' + str(hexes[i][0]) + '_' + str(hexes[i][1]) + '_0', primary_ray_mesh)
        primary_ray_collection.objects.link(primary_ray_object)

        if support_secondary_is_newton:
            secondary_ray = secondary_mirror_newton_rays.create_ray(
                primary_ray[0],
                primary_ray[1],
                support_newton_secondary_z,
                support_newton_secondary_t,
                support_newton_secondary_top_t,
                support_newton_secondary_rx,
                support_newton_secondary_ry,
            )
        else:
            secondary_ray = secondary_mirror_spherical_rays.create_ray(
                primary_ray[0],
                primary_ray[1],
                support_spherical_secondary_z,
                support_spherical_secondary_r,
                support_spherical_secondary_f
            )

        if secondary_ray is not None:
            secondary_rays_mesh = ray.create_mesh(secondary_ray[0], secondary_ray[1], 0.005)
            secondary_rays_object = bpy.data.objects.new('ray_' + str(hexes[i][0]) + '_' + str(hexes[i][1]) + '_0', secondary_rays_mesh)
            secondary_ray_collection.objects.link(secondary_rays_object)

arm_mesh = support_arm.create_mesh(
    support_arm_e,
    support_arm_h,
    support_arm_outer_r,
    support_arm_inner_r,
    support_arm_screw_length,
    support_arm_precision,
    bm = None,
    D = support_arm_D,
    P = support_arm_P
)

separator_arm_mesh = support_arm.create_mesh(
    support_arm_e,
    support_arm_h,
    support_arm_outer_r,
    support_arm_inner_r,
    support_arm_screw_length,
    support_arm_precision,
    bm = None,
    D = support_arm_D,
    P = support_arm_P,
    ccw_bottom = True
)

arm_block_mesh_l = support_arm_block.create_mesh(
    support_arm_block_e,
    support_arm_block_f,
    support_arm_block_n,
    support_arm_block_r,
    support_arm_block_t,
    support_arm_block_wl,
    support_arm_block_p,
    support_arm_block_hex_thickness,
    support_arm_block_hex_interior_thickness,
    support_arm_block_hex_walls_height,
    support_arm_block_hex_primary_thickness,
    support_arm_block_arm_radius,
    support_arm_block_clip_depth,
    support_arm_block_clip_thickness,
    support_arm_block_clip_height,
    support_arm_block_clip_e,
    support_arm_block_clip_padding_x,
    support_arm_block_clip_padding_z,
    support_arm_blocking_screw_r,
    support_arm_blocking_screw_length,
    support_arm_blocking_screw_rp,
    support_arm_blocking_screw_D,
    support_arm_blocking_screw_P,
    is_left = True
)

arm_block_mesh_l.transform(
    Matrix.Translation(
        (0, 0, support_arm_block_z)
    )
)

support_arm_blocking_screw_mesh = screw.capped_screw(
    support_arm_blocking_screw_r,
    support_arm_block_screw_cap_t,
    support_arm_block_screw_cap_h,
    support_arm_block_screw_cap_cap_h,
    support_arm_block_screw_cap_rp,
    support_arm_blocking_screw_length,
    screw_D = support_arm_blocking_screw_D,
    screw_P = support_arm_blocking_screw_P,
    screw_tip_r = support_arm_blocking_screw_tip_r,
    screw_tip_length = support_arm_blocking_screw_tip_length,
    z_screw_start = support_arm_block_screw_cap_z_screw_start,
    bm = None,
    head_r = support_arm_block_screw_cap_head_r
)

arm_block_mesh_r = support_arm_block.create_mesh(
    support_arm_block_e,
    support_arm_block_f,
    support_arm_block_n,
    support_arm_block_r,
    support_arm_block_t,
    support_arm_block_wl,
    support_arm_block_p,
    support_arm_block_hex_thickness,
    support_arm_block_hex_interior_thickness,
    support_arm_block_hex_walls_height,
    support_arm_block_hex_primary_thickness,
    support_arm_block_arm_radius,
    support_arm_block_clip_depth,
    support_arm_block_clip_thickness,
    support_arm_block_clip_height,
    support_arm_block_clip_e,
    support_arm_block_clip_padding_x,
    support_arm_block_clip_padding_z,
    support_arm_blocking_screw_r,
    support_arm_blocking_screw_length,
    support_arm_blocking_screw_rp,
    support_arm_blocking_screw_D,
    support_arm_blocking_screw_P,
    is_left = False
)
arm_block_mesh_r.transform(
    Matrix.Translation(
        (0, 0, support_arm_block_z)
    )
)

arm_head_mesh = support_arm_head.create_mesh(
    support_arm_head_t,
    support_arm_head_p,
    support_arm_head_min_height,
    support_arm_head_width,
    support_arm_head_with_spider_screw,
    support_arm_head_with_spider_screw_in,
    support_arm_head_with_top_screw,
    support_arm_head_with_bottom_screw,
    0,
    None,
    support_arm_head_arm_dist,
    support_arm_head_arm_rp,
    support_arm_head_arm_outer_r,
    support_arm_head_arm_inner_r,
    support_arm_head_arm_screw_length,
    support_arm_head_arm_D,
    support_arm_head_arm_P,
    support_arm_head_arm_screw_in_length,
    support_arm_head_arm_screw_in_end_h,
    support_arm_head_spider_rp,
    support_arm_head_spider_r,
    support_arm_head_spider_screw_length,
    support_arm_head_spider_screw_z,
    support_arm_head_spider_D,
    support_arm_head_spider_P,
    support_arm_head_spider_screw_end_h
)


arm_separator_mesh = support_arm_head.create_mesh(
    support_arm_head_t,
    support_arm_head_p,
    support_arm_head_min_height,
    support_arm_head_width,
    False,
    False,
    True,
    True,
    0,
    None,
    support_arm_head_arm_dist,
    support_arm_head_arm_rp,
    support_arm_head_arm_outer_r,
    support_arm_head_arm_inner_r,
    support_arm_head_arm_screw_length,
    support_arm_head_arm_D,
    support_arm_head_arm_P,
    support_arm_head_arm_screw_in_length,
    support_arm_head_arm_screw_in_end_h,
    support_arm_head_spider_rp,
    support_arm_head_spider_r,
    support_arm_head_spider_screw_length,
    support_arm_head_spider_screw_z,
    support_arm_head_spider_D,
    support_arm_head_spider_P,
    support_arm_head_spider_screw_end_h
)

if support_secondary_is_newton:
    arm_head_with_ocular_mesh = support_arm_head.create_mesh(
        support_arm_head_t,
        support_arm_head_p,
        support_arm_head_height,
        support_arm_head_width,
        support_arm_head_with_spider_screw,
        support_arm_head_with_spider_screw_in,
        support_arm_head_with_top_screw,
        support_arm_head_with_bottom_screw,
        support_arm_head_ocular_r,
        support_arm_head_ocular_z,
        support_arm_head_arm_dist,
        support_arm_head_arm_rp,
        support_arm_head_arm_outer_r,
        support_arm_head_arm_inner_r,
        support_arm_head_arm_screw_length,
        support_arm_head_arm_D,
        support_arm_head_arm_P,
        support_arm_head_arm_screw_in_length,
        support_arm_head_arm_screw_in_end_h,
        support_arm_head_spider_rp,
        support_arm_head_spider_r,
        support_arm_head_spider_screw_length,
        support_arm_head_spider_screw_z_with_ocular,
        support_arm_head_spider_D,
        support_arm_head_spider_P,
        support_arm_head_spider_screw_end_h
    )

    secondary_mesh = secondary_mirror_newton.create_mesh(
        support_newton_secondary_t,
        support_newton_secondary_top_t,
        support_newton_secondary_rx,
        support_newton_secondary_ry,
        support_newton_secondary_rp,
        support_arm_n,
        support_spider_r,
        support_spider_screw_length,
        support_spider_rp,
        support_spider_D,
        support_spider_P,
        support_spider_screw_end_h
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

spider_collection = bpy.data.collections.new('spider_collection')
bpy.context.scene.collection.children.link(spider_collection)

for i in range(0, len(support_arm_points)):
    no_ocular = i > 0 or not support_secondary_is_newton
    nz = support_arm_nz if no_ocular else support_arm_nz_with_ocular
    bz = support_arm_z if no_ocular else support_arm_z_with_ocular
    nb_separator = 0

    sz = bz
    for z in range(0, nz):
        if z > 0 and z % 2 == 0:
            arm_separator_obj = bpy.data.objects.new(
                'arm_separator_' + str(support_arm_block_n) + '_' + str(i) + '_' + str(z),
                arm_separator_mesh
            )
            arm_separator_obj.rotation_euler = rot
            arm_separator_obj.location.x = 0.5 * (support_arm_points[i][0][0] + support_arm_points[i][1][0])
            arm_separator_obj.location.y = 0.5 * (support_arm_points[i][0][1] + support_arm_points[i][1][1])
            arm_separator_obj.location.z = sz
            arm_collection.objects.link(arm_separator_obj)
            sz += support_arm_head_min_height
            nb_separator += 1

        alpha = i * math.tau / support_arm_n
        beta = support_arm_omega + alpha
        rot = Euler((0, 0, beta), 'XYZ')

        if z == 0:
            arm_block_l = bpy.data.objects.new(
                'arm_block_' + str(support_arm_block_n) + '_' + str(i) + '_l',
                arm_block_mesh_l
            )
            arm_block_l.rotation_euler = rot
            arm_collection.objects.link(arm_block_l)

            arm_block_screw_l = bpy.data.objects.new(
                'arm_block_screw_' + str(support_arm_block_n) + '_' + str(i) + '_l',
                support_arm_blocking_screw_mesh
            )
            arm_block_screw_l.location.x = support_arm_points[i][0][0] + support_arm_block_arm_radius + support_arm_blocking_screw_length
            arm_block_screw_l.location.y = support_arm_points[i][0][1]
            arm_block_screw_l.location.z = support_arm_block_total_z
            arm_block_screw_l.rotation_euler = rot
            arm_collection.objects.link(arm_block_screw_l)

            arm_block_r = bpy.data.objects.new(
                'arm_block_' + str(support_arm_block_n) + '_' + str(i) + '_r',
                arm_block_mesh_r
            )
            arm_block_r.rotation_euler = rot
            arm_collection.objects.link(arm_block_r)

        arm_object_l = bpy.data.objects.new('separator_arm_' + str(i) + '_l', separator_arm_mesh) if (z > 0 and z % 2 == 0) \
            else bpy.data.objects.new('arm_' + str(i) + '_l', arm_mesh)
        arm_collection.objects.link(arm_object_l)

        arm_object_l.location.x = support_arm_points[i][0][0]
        arm_object_l.location.y = support_arm_points[i][0][1]
        arm_object_l.location.z = sz

        arm_object_r = bpy.data.objects.new('separator_arm_' + str(i) + '_r', separator_arm_mesh) if (z > 0 and z % 2 == 0) \
            else bpy.data.objects.new('arm_' + str(i) + '_r', arm_mesh)
        arm_collection.objects.link(arm_object_r)

        arm_object_r.location.x = support_arm_points[i][1][0]
        arm_object_r.location.y = support_arm_points[i][1][1]
        arm_object_r.location.z = sz

        sz += support_arm_outer_length

        if z != nz - 1:
            continue

        arm_head_object = bpy.data.objects.new(
            'arm_head_' + str(i),
            arm_head_mesh if no_ocular else arm_head_with_ocular_mesh
        )
        arm_collection.objects.link(arm_head_object)

        arm_head_object.location.x = 0.5 * (support_arm_points[i][0][0] + support_arm_points[i][1][0])
        arm_head_object.location.y = 0.5 * (support_arm_points[i][0][1] + support_arm_points[i][1][1])
        arm_head_object.location.z = sz
        arm_head_object.rotation_euler = rot

        spider_arms = bpy.data.objects.new(
            'spider_arms_' + str(i),
            bpy.data.meshes.new('spider_arms_' + str(i))
        )
        spider_collection.objects.link(spider_arms)
        spider_arms.rotation_euler = rot

        spider_arms_objs = spider_arm.create_full_arm(
            i,
            n,
            r,
            support_secondary_final_z,
            support_secondary_final_dist_to_spider_arm[i],
            support_arm_head_width,
            support_spider_r,
            support_spider_screw_length,
            support_spider_rp,
            support_spider_D,
            support_spider_P,
            support_spider_screw_end_h
        )

        for obj in spider_arms_objs:
            spider_collection.objects.link(obj)
            obj.parent = spider_arms

secondary_object = bpy.data.objects.new(support_secondary_final_name, secondary_mesh)
spider_collection.objects.link(secondary_object)
secondary_object.location.z = support_secondary_z

# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\support_", check_existing=True, filter_glob='*.stl', global_scale=1000.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z', use_selection=False)

print("\nDONE\n\n\n")