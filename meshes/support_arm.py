import bpy
import bmesh
import math
from meshes import screw

support_arm_name = 'arm'

# h: total height
# outer_r: external radius
# inner_r: internal radius
# precision: circles precision
def create_mesh(
    h,
    outer_r,
    inner_r,
    screw_length,
    precision,
    bm = None,
    D = None,
    P = None
):
    if bm == None:
        bm = bmesh.new()

    d = D if D != None else screw.get_D(2 * inner_r)
    step_h = 0.5 * d
    step_w = P if P != None else screw.get_P(d)

    screw_in_ret = screw.screw_in(
        inner_r,
        screw_length + 2 * step_w,
        precision,
        bm,
        z_start = 0.001,
        z_scale = -1,
        fill_end=True,
        D = d,
        P = step_w
    )

    screw_ret = screw.screw(
        outer_r,
        screw_length,
        precision,
        bm,
        z_top = 0,
        top_length=h - screw_length - step_w,
        tip_r = 0.5 * step_h,
        tip_length = step_w,
        fill_tip=True,
        D = d,
        P = step_w
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = screw_in_ret[2]
            + screw_ret[2]
    )

    mesh = bpy.data.meshes.new(
        support_arm_name + '_' + str((
            h,
            outer_r,
            inner_r,
            screw_length,
            precision,
            bm,
            D,
            P
        ))
    )

    bm.to_mesh(mesh)
    bm.free()

    return mesh