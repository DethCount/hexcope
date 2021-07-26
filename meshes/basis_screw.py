import bpy
import bmesh
import math
from mathutils import Matrix, Vector
from meshes import screw

basis_screw_name = 'basis_screw'

def create_mesh(
    r,
    start_h,
    iterations,
    step_h,
    step_w,
    head_r,
    head_h,
    bottom_r,
    bottom_h,
    p
):
    bm = bmesh.new()

    z_head_top = -head_h
    z_head_bottom = -0.01

    head_top = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = head_r
    )

    head_top_edges = list(set(
        e
        for v in head_top['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_head_top)),
        verts = head_top['verts']
    )

    head_bottom = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = head_r
    )

    head_bottom_edges = list(set(
        e
        for v in head_bottom['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_head_bottom)),
        verts = head_bottom['verts']
    )

    screw_ret = screw.screw(
        r,
        iterations,
        step_h,
        step_w,
        p,
        bm,
        z_top = z_head_bottom,
        ccw = False,
        top_length = start_h,
        bottom_length = bottom_h,
        tip_r = r - 2 * step_h,
        tip_length = step_w
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = head_top_edges
            + head_bottom_edges
    )

    # bugfix aligned circles bridging
    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, -z_head_bottom)),
        verts = head_bottom['verts']
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = head_bottom_edges
            + screw_ret[2] # screw top
    )

    bmesh.ops.edgeloop_fill(
        bm,
        edges = head_top_edges
    )

    bmesh.ops.rotate(
        bm,
        cent = (0, 0, 0),
        matrix = Matrix.Rotation(math.pi / 2, 4, 'Y'),
        verts = bm.verts
    )

    bm.normal_update()

    mesh = bpy.data.meshes.new(
        basis_screw_name
        + '_' + str((
            r,
            start_h,
            iterations,
            step_h,
            step_w,
            head_r,
            head_h,
            bottom_r,
            bottom_h,
            p
        ))
    )

    bm.to_mesh(mesh)
    bm.free()

    return mesh
