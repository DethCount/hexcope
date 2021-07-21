import os
import sys
import bpy
import math
from mathutils import Euler, Matrix, Vector

sys.dont_write_bytecode = 1
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from hyperparameters import r, h, p, e, trig_h
from optics import hex2xy
from meshes import \
    basis_arm, \
    basis_cap, \
    basis_foot, \
    basis_leg, \
    basis_plate_axis, \
    basis_plate_bottom, \
    basis_plate_top, \
    basis_screw, \
    basis_wheel

basis_wheel_e = e
basis_wheel_t = h
basis_wheel_h = 1.7
basis_wheel_r = r
basis_wheel_p = p # wheel precision
basis_wheel_wr = 0.8 * r # wheel radius
basis_wheel_mr = 0.2 * r
basis_wheel_arm_t = 0.1
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
basis_arm_teeth_height = 0.2
basis_arm_teeth_thickness = 0.8 * basis_arm_t

basis_screw_r = basis_wheel_mr - e
basis_screw_start_e = 0.03
basis_screw_start = 2 * basis_wheel_t + basis_wheel_arm_t + basis_screw_start_e
basis_screw_iterations = 3
basis_screw_step_h = 0.02
basis_screw_step_w = 0.03
basis_screw_head_r = basis_screw_r + 0.03
basis_screw_head_h = 0.03
basis_screw_bottom_r = basis_screw_r - 2 * basis_screw_step_h
basis_screw_bottom_h = basis_screw_step_w
basis_screw_p = 100

basis_cap_r = basis_screw_r
basis_cap_t = basis_screw_step_h
basis_cap_iterations = basis_screw_iterations + 1
basis_cap_bottom_h = basis_screw_start_e
basis_cap_h = basis_cap_bottom_h + (basis_cap_iterations + 1) * basis_screw_step_w + basis_cap_t
basis_cap_step_h = basis_screw_step_h
basis_cap_step_w = basis_screw_step_w
basis_cap_p = basis_screw_p

basis_leg_e = basis_arm_e
basis_leg_t = 2 * basis_arm_t + 2 * basis_arm_e
basis_leg_h = basis_arm_h
basis_leg_w = basis_arm_w
basis_leg_x = -0.5 * basis_arm_wheel_thickness
basis_leg_z = basis_arm_z - basis_arm_h
basis_leg_teeth_width = basis_arm_teeth_width
basis_leg_teeth_height = basis_arm_teeth_height
basis_leg_teeth_thickness = basis_arm_teeth_thickness
basis_leg_side_teeth_width = 0.1
basis_leg_side_teeth_height = 0.15
basis_leg_side_teeth_thickness = 0.6 * basis_leg_t
basis_leg_side_teeth_z = 0.5 * (2 * 0.04 + basis_leg_side_teeth_width)

basis_foot_e = basis_leg_e
basis_foot_t = basis_leg_t
basis_foot_h = 2 * basis_leg_side_teeth_z
basis_foot_w1 = 0.1
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

basis_plate_axis_e = basis_plate_top_e
basis_plate_axis_t = h
basis_plate_axis_r = basis_plate_top_r * math.cos(math.pi / 6)
basis_plate_axis_p = basis_plate_top_p
basis_plate_axis_x = basis_plate_top_x - (math.sqrt(3) / 2) * r + 0.5 * h
basis_plate_axis_z = basis_plate_top_z - basis_plate_top_t - basis_plate_axis_e
basis_plate_axis_top_t = basis_plate_top_t
basis_plate_axis_top_r = basis_plate_top_sr
basis_plate_axis_bottom_t = basis_plate_top_t
basis_plate_axis_bottom_r = basis_plate_top_sr

basis_plate_bottom_e = basis_plate_top_e
basis_plate_bottom_t = basis_plate_axis_bottom_t
basis_plate_bottom_r = basis_plate_top_r
basis_plate_bottom_sr = basis_plate_axis_bottom_r
basis_plate_bottom_p = basis_plate_top_p
basis_plate_bottom_x = basis_plate_top_x
basis_plate_bottom_z = basis_plate_axis_z - basis_plate_axis_t - basis_plate_bottom_e
basis_plate_bottom_hex_side = basis_plate_top_hex_side
basis_plate_bottom_top_plate_thickness = basis_plate_top_t

def move_basis_to(obj, hex):
    hex_1 = hex2xy(r, 0, 0, hex, 1)
    hex_2 = hex2xy(r, 0, 0, hex, 2)
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

basis_wheel_mesh = basis_wheel.create_mesh(
    basis_wheel_e,
    basis_wheel_t,
    basis_wheel_h,
    basis_wheel_r,
    basis_wheel_p,
    basis_wheel_wr,
    basis_wheel_mr,
    basis_wheel_top_z,
    h,
    trig_h,
    basis_wheel_arm_t,
)

basis_wheel_screw_mesh = basis_screw.create_mesh(
    basis_screw_r,
    basis_screw_start,
    basis_screw_iterations,
    basis_screw_step_h,
    basis_screw_step_w,
    basis_screw_head_r,
    basis_screw_head_h,
    basis_screw_bottom_r,
    basis_screw_bottom_h,
    basis_screw_p
)
basis_wheel_screw_mesh.transform(
    Matrix.Translation(
        Vector((-0.5 * basis_wheel_t - 0.5 * basis_wheel_arm_t - basis_wheel_t, 0, basis_wheel_bottom_z))
    )
)

basis_wheel_screw_cap_mesh = basis_cap.create_mesh(
    basis_cap_r,
    basis_cap_t,
    basis_cap_h,
    basis_cap_iterations,
    basis_cap_step_h,
    basis_cap_step_w,
    basis_cap_bottom_h,
    basis_cap_p
)
basis_wheel_screw_cap_mesh.transform(
    Matrix.Translation(
        Vector((0.5 * basis_wheel_arm_t + basis_wheel_t, 0, basis_wheel_bottom_z))
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
    basis_leg_side_teeth_z
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
    1 # yscale
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
    -1 # yscale
)

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
    basis_plate_top_foot_thickness
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
    basis_plate_axis_bottom_r
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
basis_wheel_object_r = bpy.data.objects.new('basis_wheel_r', basis_wheel_mesh)
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

basis_foot_rr = bpy.data.objects.new('basis_foot_rr', basis_foot_mesh_r)
basis_collection.objects.link(basis_foot_rr)
move_basis_to(basis_foot_rr, 0)

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


basis_wheel_object_l = bpy.data.objects.new('basis_wheel_l', basis_wheel_mesh)
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

basis_leg_l = bpy.data.objects.new('basis_leg_l', basis_leg_mesh)
basis_collection.objects.link(basis_leg_l)
move_basis_to(basis_leg_l, 3)

basis_foot_lr = bpy.data.objects.new('basis_foot_lr', basis_foot_mesh_r)
basis_collection.objects.link(basis_foot_lr)
move_basis_to(basis_foot_lr, 3)

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
# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\", check_existing=True, filter_glob='*.stl', use_selection=False, global_scale=100.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z')