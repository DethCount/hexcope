import bpy
import bmesh
import math
from mathutils import Euler, Matrix

from optics import get_support_arm_point
from meshes import screw

import importlib
importlib.reload(screw)

spider_arm_name = 'spider_arm'

def create_mesh(r, length, screw_length, screw_precision = 25, screw_D = None, screw_P = None, screw_end_h = 0):
    bm = bmesh.new()

    screw.screw_in(
        r,
        screw_length,
        screw_precision,
        bm,
        z_start=0,
        z_scale=-1,
        fill_end=True,
        D=screw_D,
        P=screw_P,
        end_h=screw_end_h
    )

    screw.screw(
        r,
        screw_length,
        screw_precision,
        bm,
        z_top = 0,
        top_length=length,
        tip_r=0.5 * r,
        tip_length = screw_end_h,
        D=screw_D,
        P=screw_P
    )

    bmesh.ops.rotate(
        bm,
        verts = bm.verts[:],
        matrix = Matrix.Rotation(-0.5 * math.pi, 3, 'Y')
    )

    mesh = bpy.data.meshes.new(spider_arm_name + str((
        r, length,
        screw_length, screw_D, screw_P
    )))

    bm.to_mesh(mesh)

    return mesh

def create_full_arm(
    n,
    hex_side_length,
    secondary_z,
    secondary_dist_to_spider_arm,
    support_arm_mx,
    support_arm_my,
    support_arm_head_width,
    r,
    screw_length,
    screw_precision = 25,
    screw_D = None,
    screw_P = None,
    screw_end_h = 0
):
    objs = list()
    arm_points_x = list()
    hahw = 0.5 * support_arm_head_width

    for i in range(0, n + 1):
        arm_points_x.append(
            get_support_arm_point(
                i,
                hex_side_length,
                support_arm_mx,
                support_arm_my,
                0
            )[0][0]
        )

        length = arm_points_x[i] - (arm_points_x[i - 1] if i > 0 else (secondary_dist_to_spider_arm + hahw))

        # print(str(i), str(length), str(secondary_dist_to_spider_arm), str(arm_points_x[i]), str(hahw))

        mesh = create_mesh(
            r,
            length,
            screw_length,
            screw_precision,
            screw_D,
            screw_P,
            screw_end_h
        )

        obj = bpy.data.objects.new(spider_arm_name + '_' + str(i), mesh)
        obj.location.x = arm_points_x[i] - hahw
        obj.location.z = secondary_z
        objs.append(obj)

    return objs