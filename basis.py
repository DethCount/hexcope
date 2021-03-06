import os
import sys
import bpy
import math
from mathutils import Euler, Matrix, Vector

sys.dont_write_bytecode = 1
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from hyperparameters import f, r, h, p, e, trig_h, \
    clip_depth, clip_thickness, clip_height, clip_e
from optics import hex2xy
from meshes import \
    basis_arm, \
    basis_cap, \
    basis_foot, \
    basis_leg, \
    mainboard, \
    basis_plate_axis, \
    basis_plate_bottom, \
    basis_plate_top, \
    basis_screw, \
    basis_wheel

import importlib
importlib.reload(basis_screw)
importlib.reload(basis_cap)

if bpy.context.scene.objects.get('Camera'):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

basis_wheel_e = e
basis_wheel_f = f
basis_wheel_t = h
basis_wheel_h = 0.17
basis_wheel_r = r
basis_wheel_p = p # wheel precision
basis_wheel_wr = 0.8 * r # wheel radius
basis_wheel_mr = 0.2 * r
basis_wheel_clip_depth = clip_depth
basis_wheel_clip_thickness = clip_thickness
basis_wheel_clip_height = clip_height
basis_wheel_clip_e = clip_e
basis_wheel_arm_t = 0.01
basis_wheel_top_z = 0
basis_wheel_bottom_z = -basis_wheel_wr * math.sin(math.pi / 3)

basis_arm_e = basis_wheel_e
basis_arm_t = basis_wheel_arm_t
basis_arm_h = basis_wheel_h
basis_arm_w = 1.2 * r
basis_arm_p = 20
basis_arm_z = basis_wheel_bottom_z
basis_arm_wheel_thickness = basis_wheel_t
basis_arm_wheel_radius = basis_wheel_wr
basis_arm_middle_bar_radius = basis_wheel_mr
basis_arm_teeth_width = r
basis_arm_teeth_height = 0.02
basis_arm_teeth_thickness = 0.8 * basis_arm_t

basis_screw_r = basis_wheel_mr - e
basis_screw_length = 0.015
basis_screw_start = 2 * basis_wheel_t + basis_wheel_arm_t
basis_screw_head_r = basis_screw_r + 0.003
basis_screw_head_h = 0.003
basis_screw_p = 100

basis_cap_r = basis_screw_r
basis_cap_t = 0.003
basis_cap_top_h = 0.005
basis_cap_bottom_h = 0.0001
basis_cap_h = basis_cap_bottom_h + 1.5 * basis_screw_length + basis_cap_top_h + basis_cap_t
basis_cap_p = basis_screw_p
basis_cap_head_r = basis_cap_r + 0.01
basis_cap_head_length = 0.01

basis_leg_e = basis_arm_e
basis_leg_t = 2 * basis_arm_t + 2 * basis_arm_e
basis_leg_h = basis_arm_h + 0.01
basis_leg_w = basis_arm_w
basis_leg_x = -0.5 * basis_arm_wheel_thickness
basis_leg_z = basis_arm_z - basis_arm_h
basis_leg_teeth_width = basis_arm_teeth_width
basis_leg_teeth_height = basis_arm_teeth_height
basis_leg_teeth_thickness = basis_arm_teeth_thickness
basis_leg_side_teeth_width = 0.040
basis_leg_side_teeth_height = 0.015
basis_leg_side_teeth_thickness = 0.6 * basis_leg_t
basis_leg_side_teeth_z = 0.5 * (2 * 0.004 + basis_leg_side_teeth_width)
basis_leg_with_foot_connexion = True
basis_leg_power_on_p = 50
basis_leg_power_on_ri = 0.01
basis_leg_power_on_re = 0.0145
basis_leg_power_on_z = basis_leg_power_on_re + 0.002
basis_leg_power_on_height = 0.013

basis_foot_e = basis_leg_e
basis_foot_t = basis_leg_t
basis_foot_h = 2 * basis_leg_side_teeth_z
basis_foot_w1 = 0.01
basis_foot_w2 = 0.4 * basis_leg_w
basis_foot_x = basis_leg_x
basis_foot_y = -0.5 * basis_leg_w
basis_foot_z = basis_leg_z - basis_leg_e - basis_leg_h + 0.5 * basis_foot_h + basis_leg_teeth_height
basis_foot_horizontal_tooth_width = basis_leg_side_teeth_width
basis_foot_horizontal_tooth_height = basis_leg_side_teeth_height
basis_foot_horizontal_tooth_thickness = basis_leg_side_teeth_thickness
basis_foot_vertical_tooth_width = 0.5 * basis_foot_w2
basis_foot_vertical_tooth_height = 0.6 * basis_leg_teeth_height
basis_foot_vertical_tooth_thickness = 1.5 * basis_leg_teeth_thickness

mainboard_e = 0.002
mainboard_board_width = 0.072
mainboard_board_length = 0.107
mainboard_wall_thickness = 0.008
mainboard_cover_wall_thickness = 0.003
mainboard_screw_height = 0.004
mainboard_cover_screw_height2 = 0.011
mainboard_t = mainboard_screw_height + 0.001 + mainboard_cover_screw_height2 + mainboard_cover_wall_thickness
mainboard_h = mainboard_board_length + 2 * e
mainboard_w = mainboard_board_width + 2 * e
mainboard_screw_p = p
mainboard_screw_ri = 0.0015
mainboard_screw_re = 0.0035
mainboard_screw_pos_tl = (0.003, 0.014)
mainboard_screw_pos_tr = (0.0685, 0.003)
mainboard_screw_pos_br = (0.0685, 0.103)
mainboard_screw_pos_bl = (0.003, 0.103)
mainboard_x = basis_leg_x - 0.5 * basis_leg_t
mainboard_y = 0
mainboard_z = basis_leg_z - basis_leg_h + basis_leg_teeth_height + mainboard_h + mainboard_wall_thickness + mainboard_e
mainboard_power_pos = 0.004
mainboard_power_width = 0.012
mainboard_usb_pos = 0.081
mainboard_usb_width = 0.014

mainboard_cover_e = mainboard_e - 0.001
mainboard_cover_x = mainboard_x
mainboard_cover_y = mainboard_y
mainboard_cover_z = mainboard_z
mainboard_cover_motor_width = 0.006
mainboard_cover_motor_height = 0.013
mainboard_cover_motor1_pos = (0.066, 0.013)
mainboard_cover_motor2_pos = (0.066, 0.036)
mainboard_cover_motor3_pos = (0.066, 0.06)
mainboard_cover_motor4_pos = (0.066, 0.083)
mainboard_cover_spi_width = 0.015
mainboard_cover_spi_height = 0.01
mainboard_cover_spi_pos = (0.012, 0.094)

basis_plate_top_e = basis_foot_e
basis_plate_top_t = basis_leg_teeth_height
basis_plate_top_r = 1.1 * r
basis_plate_top_sr = basis_arm_middle_bar_radius
basis_plate_top_p = 50
basis_plate_top_x = basis_foot_x
basis_plate_top_z = basis_foot_z - 0.5 * basis_foot_h
basis_plate_top_hex_side = r
basis_plate_top_large_tooth_width = basis_leg_teeth_width
basis_plate_top_large_tooth_height = basis_leg_teeth_height
basis_plate_top_large_tooth_thickness = basis_leg_teeth_thickness
basis_plate_top_small_teeth_width = basis_foot_vertical_tooth_width
basis_plate_top_small_teeth_height = basis_foot_vertical_tooth_height
basis_plate_top_small_teeth_thickness = basis_foot_vertical_tooth_thickness
basis_plate_top_leg_width = basis_leg_w
basis_plate_top_foot_w1 = basis_foot_w1
basis_plate_top_foot_w2 = basis_foot_w2
basis_plate_top_foot_thickness = basis_foot_t
basis_plate_top_stator_side = 0.043
basis_plate_top_stator_wall_thickness = 0.004
basis_plate_top_stator_wall_height = 0.5 * basis_plate_top_stator_side

basis_plate_axis_e = basis_plate_top_e
basis_plate_axis_t = 0.004
basis_plate_axis_r = basis_plate_top_r * math.cos(math.pi / 6)
basis_plate_axis_p = basis_plate_top_p
basis_plate_axis_x = basis_plate_top_x - (math.sqrt(3) / 2) * r + 0.5 * h
basis_plate_axis_z = basis_plate_top_z - basis_plate_top_t - basis_plate_axis_e
basis_plate_axis_top_t = basis_plate_top_t
basis_plate_axis_top_r = basis_plate_top_sr
basis_plate_axis_bottom_t = basis_plate_top_t
basis_plate_axis_bottom_r = basis_plate_top_sr
basis_plate_axis_rotor_t = basis_plate_top_t
basis_plate_axis_rotor_r = 0.0025

basis_plate_bottom_e = basis_plate_top_e
basis_plate_bottom_t = basis_plate_axis_bottom_t
basis_plate_bottom_r = basis_plate_top_r
basis_plate_bottom_sr = basis_plate_axis_bottom_r
basis_plate_bottom_p = basis_plate_top_p
basis_plate_bottom_x = basis_plate_top_x
basis_plate_bottom_z = basis_plate_axis_z - basis_plate_axis_t - basis_plate_bottom_e
basis_plate_bottom_hex_side = basis_plate_top_hex_side
basis_plate_bottom_top_plate_thickness = basis_plate_top_t

def move_basis_to(obj, z):
    v1 = hex2xy(r, 0, 0, z, 1)
    v2 = hex2xy(r, 0, 0, z, 2)
    hex_mid = (
        0.5 * (v1[0] + v2[0]),
        0.5 * (v1[1] + v2[1])
    )

    obj.location.x = hex_mid[0]
    obj.location.y = hex_mid[1]
    obj.location.z = h
    obj.rotation_euler = Euler((0, 0, (z + 0.5) * (math.pi / 3)), 'XYZ')

    return

basis_collection = bpy.data.collections.new('basis_collection')
bpy.context.scene.collection.children.link(basis_collection)

hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]

basis_wheel_mesh_r = basis_wheel.create_mesh(
    basis_wheel_e,
    basis_wheel_f,
    basis_wheel_t,
    basis_wheel_h,
    basis_wheel_r,
    basis_wheel_p,
    basis_wheel_wr,
    basis_wheel_mr,
    basis_wheel_top_z,
    h,
    trig_h,
    Vector((0, 0, 0)),
    basis_wheel_clip_depth,
    basis_wheel_clip_thickness,
    basis_wheel_clip_height,
    basis_wheel_clip_e,
    basis_wheel_arm_t
)

basis_wheel_mesh_l = basis_wheel.create_mesh(
    basis_wheel_e,
    basis_wheel_f,
    basis_wheel_t,
    basis_wheel_h,
    basis_wheel_r,
    basis_wheel_p,
    basis_wheel_wr,
    basis_wheel_mr,
    basis_wheel_top_z,
    h,
    trig_h,
    Vector((0, 0, 3)),
    basis_wheel_clip_depth,
    basis_wheel_clip_thickness,
    basis_wheel_clip_height,
    basis_wheel_clip_e,
    basis_wheel_arm_t
)

basis_wheel_screw_mesh = basis_screw.create_mesh(
    basis_screw_r,
    basis_screw_length,
    basis_screw_start,
    basis_screw_head_r,
    basis_screw_head_h,
    basis_screw_p
)
basis_wheel_screw_mesh.transform(
    Matrix.Translation(
        Vector((
            -0.5 * basis_wheel_t \
                - 0.5 * basis_wheel_arm_t \
                - basis_wheel_t,
            0,
            basis_wheel_bottom_z
        ))
    )
)

basis_wheel_screw_cap_mesh = basis_cap.create_mesh(
    basis_cap_r,
    basis_cap_t,
    basis_cap_h,
    basis_cap_p,
    basis_cap_top_h,
    basis_cap_bottom_h,
    bm = None,
    head_r = basis_cap_head_r,
    head_length = basis_cap_head_length
)
basis_wheel_screw_cap_mesh.transform(
    Matrix.Translation(
        Vector((
            basis_wheel_arm_t + e,
            0,
            basis_wheel_bottom_z
        ))
    )
)

basis_arm_mesh = basis_arm.create_mesh(
    basis_arm_e,
    basis_arm_t,
    basis_arm_h,
    basis_arm_w,
    basis_arm_p,
    basis_arm_z,
    basis_arm_wheel_thickness,
    basis_arm_wheel_radius,
    basis_arm_middle_bar_radius,
    basis_arm_teeth_width,
    basis_arm_teeth_height,
    basis_arm_teeth_thickness
)

basis_leg_mesh = basis_leg.create_mesh(
    basis_leg_e,
    basis_leg_t,
    basis_leg_h,
    basis_leg_w,
    basis_leg_x,
    basis_leg_z,
    basis_leg_teeth_width,
    basis_leg_teeth_height,
    basis_leg_teeth_thickness,
    basis_leg_side_teeth_width,
    basis_leg_side_teeth_height,
    basis_leg_side_teeth_thickness,
    basis_leg_side_teeth_z,
    basis_leg_with_foot_connexion,
    basis_leg_power_on_p,
    basis_leg_power_on_ri,
    basis_leg_power_on_re,
    basis_leg_power_on_z,
    basis_leg_power_on_height
)

mainboard_mesh = mainboard.create_mesh(
    mainboard_e,
    mainboard_t,
    mainboard_h,
    mainboard_w,
    mainboard_wall_thickness,
    mainboard_board_width,
    mainboard_board_length,
    mainboard_screw_height,
    mainboard_screw_p,
    mainboard_screw_ri,
    mainboard_screw_re,
    mainboard_screw_pos_tl,
    mainboard_screw_pos_tr,
    mainboard_screw_pos_br,
    mainboard_screw_pos_bl,
    mainboard_x,
    mainboard_y,
    mainboard_z,
    mainboard_power_pos,
    mainboard_power_width,
    mainboard_usb_pos,
    mainboard_usb_width
)

mainboard_cover_mesh = mainboard.create_cover_mesh(
    mainboard_e,
    mainboard_t,
    mainboard_h,
    mainboard_w,
    mainboard_wall_thickness,
    mainboard_board_width,
    mainboard_board_length,
    mainboard_screw_height,
    mainboard_screw_p,
    mainboard_screw_ri,
    mainboard_screw_re,
    mainboard_screw_pos_tl,
    mainboard_screw_pos_tr,
    mainboard_screw_pos_br,
    mainboard_screw_pos_bl,
    mainboard_power_pos,
    mainboard_power_width,
    mainboard_usb_pos,
    mainboard_usb_width,
    mainboard_cover_wall_thickness,
    mainboard_cover_e,
    mainboard_cover_x,
    mainboard_cover_y,
    mainboard_cover_z,
    mainboard_cover_screw_height2,
    mainboard_cover_motor_width,
    mainboard_cover_motor_height,
    mainboard_cover_motor1_pos,
    mainboard_cover_motor2_pos,
    mainboard_cover_motor3_pos,
    mainboard_cover_motor4_pos,
    mainboard_cover_spi_width,
    mainboard_cover_spi_height,
    mainboard_cover_spi_pos
)

basis_foot_mesh_r = basis_foot.create_mesh(
    basis_foot_e,
    basis_foot_t,
    basis_foot_h,
    basis_foot_w1,
    basis_foot_w2,
    basis_foot_x,
    basis_foot_y,
    basis_foot_z,
    basis_foot_horizontal_tooth_width,
    basis_foot_horizontal_tooth_height,
    basis_foot_horizontal_tooth_thickness,
    basis_foot_vertical_tooth_width,
    basis_foot_vertical_tooth_height,
    basis_foot_vertical_tooth_thickness,
    1, # yscale
    basis_leg_with_foot_connexion
)

basis_foot_mesh_l = basis_foot.create_mesh(
    basis_foot_e,
    basis_foot_t,
    basis_foot_h,
    basis_foot_w1,
    basis_foot_w2,
    basis_foot_x,
    basis_foot_y,
    basis_foot_z,
    basis_foot_horizontal_tooth_width,
    basis_foot_horizontal_tooth_height,
    basis_foot_horizontal_tooth_thickness,
    basis_foot_vertical_tooth_width,
    basis_foot_vertical_tooth_height,
    basis_foot_vertical_tooth_thickness,
    -1, # yscale
    basis_leg_with_foot_connexion
)

if not basis_leg_with_foot_connexion:
    basis_leg_mesh = basis_leg.leg_with_feets_mesh(basis_leg_mesh, basis_foot_mesh_l, basis_foot_mesh_r)

basis_leg_l_mesh = basis_leg.mainboard_leg_mesh(basis_leg_mesh, mainboard_mesh)

basis_plate_top_mesh = basis_plate_top.create_mesh(
    basis_plate_top_e,
    basis_plate_top_t,
    basis_plate_top_r,
    basis_plate_top_sr,
    basis_plate_top_p,
    basis_plate_top_x,
    basis_plate_top_z,
    basis_plate_top_hex_side,
    basis_plate_top_large_tooth_width,
    basis_plate_top_large_tooth_height,
    basis_plate_top_large_tooth_thickness,
    basis_plate_top_small_teeth_width,
    basis_plate_top_small_teeth_height,
    basis_plate_top_small_teeth_thickness,
    basis_plate_top_leg_width,
    basis_plate_top_foot_w1,
    basis_plate_top_foot_w2,
    basis_plate_top_foot_thickness,
    basis_plate_top_stator_side,
    basis_plate_top_stator_wall_thickness,
    basis_plate_top_stator_wall_height
)

basis_plate_axis_mesh = basis_plate_axis.create_mesh(
    basis_plate_axis_e,
    basis_plate_axis_t,
    basis_plate_axis_r,
    basis_plate_axis_p,
    basis_plate_axis_x,
    basis_plate_axis_z,
    basis_plate_axis_top_t,
    basis_plate_axis_top_r,
    basis_plate_axis_bottom_t,
    basis_plate_axis_bottom_r,
    basis_plate_axis_rotor_t,
    basis_plate_axis_rotor_r
)

basis_plate_bottom_mesh = basis_plate_bottom.create_mesh(
    basis_plate_bottom_e,
    basis_plate_bottom_t,
    basis_plate_bottom_r,
    basis_plate_bottom_sr,
    basis_plate_bottom_p,
    basis_plate_bottom_x,
    basis_plate_bottom_z,
    basis_plate_bottom_hex_side,
    basis_plate_bottom_top_plate_thickness
)

# print('basis wheel mesh created: ' + str(basis_wheel_mesh))
basis_wheel_object_r = bpy.data.objects.new('basis_wheel_r', basis_wheel_mesh_r)
basis_collection.objects.link(basis_wheel_object_r)
move_basis_to(basis_wheel_object_r, 0)

basis_arm_r = bpy.data.objects.new('basis_arm_r', basis_arm_mesh)
basis_collection.objects.link(basis_arm_r)
move_basis_to(basis_arm_r, 0)

basis_screw_obj_r = bpy.data.objects.new('basis_screw_r', basis_wheel_screw_mesh)
basis_collection.objects.link(basis_screw_obj_r)
move_basis_to(basis_screw_obj_r, 0)

basis_cap_r = bpy.data.objects.new('basis_cap_r', basis_wheel_screw_cap_mesh)
basis_collection.objects.link(basis_cap_r)
move_basis_to(basis_cap_r, 0)

basis_leg_r = bpy.data.objects.new('basis_leg_r', basis_leg_mesh)
basis_collection.objects.link(basis_leg_r)
move_basis_to(basis_leg_r, 0)

if basis_leg_with_foot_connexion:
    basis_foot_rr = bpy.data.objects.new('basis_foot_rr', basis_foot_mesh_r)
    basis_collection.objects.link(basis_foot_rr)
    move_basis_to(basis_foot_rr, 0)

if basis_leg_with_foot_connexion:
    basis_foot_rl = bpy.data.objects.new('basis_foot_rl', basis_foot_mesh_l)
    basis_collection.objects.link(basis_foot_rl)
    move_basis_to(basis_foot_rl, 0)

basis_plate_top_r = bpy.data.objects.new('basis_plate_top_r', basis_plate_top_mesh)
basis_collection.objects.link(basis_plate_top_r)
move_basis_to(basis_plate_top_r, 0)

basis_plate_bottom_r = bpy.data.objects.new('basis_plate_bottom_r', basis_plate_bottom_mesh)
basis_collection.objects.link(basis_plate_bottom_r)
move_basis_to(basis_plate_bottom_r, 0)

basis_plate_axis = bpy.data.objects.new('basis_plate_axis', basis_plate_axis_mesh)
basis_collection.objects.link(basis_plate_axis)
move_basis_to(basis_plate_axis, 0)


basis_wheel_object_l = bpy.data.objects.new('basis_wheel_l', basis_wheel_mesh_l)
basis_collection.objects.link(basis_wheel_object_l)
move_basis_to(basis_wheel_object_l, 3)

basis_arm_l = bpy.data.objects.new('basis_arm_l', basis_arm_mesh)
basis_collection.objects.link(basis_arm_l)
move_basis_to(basis_arm_l, 3)

basis_screw_obj_l = bpy.data.objects.new('basis_screw_l', basis_wheel_screw_mesh)
basis_collection.objects.link(basis_screw_obj_l)
move_basis_to(basis_screw_obj_l, 3)

basis_cap_l = bpy.data.objects.new('basis_cap_l', basis_wheel_screw_cap_mesh)
basis_collection.objects.link(basis_cap_l)
move_basis_to(basis_cap_l, 3)

basis_leg_l = bpy.data.objects.new('basis_leg_l', basis_leg_l_mesh)
basis_collection.objects.link(basis_leg_l)
move_basis_to(basis_leg_l, 3)

basis_mainboard_cover = bpy.data.objects.new('basis_mainboard_cover', mainboard_cover_mesh)
basis_collection.objects.link(basis_mainboard_cover)
move_basis_to(basis_mainboard_cover, 3)

if basis_leg_with_foot_connexion:
    basis_foot_lr = bpy.data.objects.new('basis_foot_lr', basis_foot_mesh_r)
    basis_collection.objects.link(basis_foot_lr)
    move_basis_to(basis_foot_lr, 3)

if basis_leg_with_foot_connexion:
    basis_foot_ll = bpy.data.objects.new('basis_foot_ll', basis_foot_mesh_l)
    basis_collection.objects.link(basis_foot_ll)
    move_basis_to(basis_foot_ll, 3)

basis_plate_top_l = bpy.data.objects.new('basis_plate_top_l', basis_plate_top_mesh)
basis_collection.objects.link(basis_plate_top_l)
move_basis_to(basis_plate_top_l, 3)

basis_plate_bottom_l = bpy.data.objects.new('basis_plate_bottom_l', basis_plate_bottom_mesh)
basis_collection.objects.link(basis_plate_bottom_l)
move_basis_to(basis_plate_bottom_l, 3)

print('done')
# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\", check_existing=True, filter_glob='*.stl', global_scale=1000.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z', use_selection=False)