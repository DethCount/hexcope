import bpy
import bmesh
import math
from mathutils import Matrix, Vector
from meshes import screw

basis_cap_name = 'basis_cap'

def create_mesh(
    r,
    t,
    h,
    iterations,
    step_h,
    step_w,
    bottom_h,
    p
):
    bm = bmesh.new()

    zz_top = -h
    zz_butt = -0.01
    z_screw_start = -bottom_h
    screw_length = z_screw_start - (zz_top + t)

    r_outer = r + t

    circle_top = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r_outer
    )

    circle_top_edges = list(set(
        e
        for v in circle_top['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, zz_top)),
        verts = circle_top['verts']
    )

    circle_bottom = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r_outer
    )

    circle_bottom_edges = list(set(
        e
        for v in circle_bottom['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, zz_butt)),
        verts = circle_bottom['verts']
    )

    circle_inner_butt = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    circle_inner_butt_edges = list(set(
        e
        for v in circle_inner_butt['verts']
        for e in v.link_edges)
    )

    screw_ret = screw.screw_in(
        r, iterations, step_h, step_w, screw_length, p,
        bm, z_screw_start, True
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_top_edges
            + circle_bottom_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_bottom_edges
            + circle_inner_butt_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_inner_butt_edges
            + screw_ret[2] # start_edges
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, -zz_butt)),
        verts = circle_bottom['verts']
    )

    bmesh.ops.edgeloop_fill(
        bm,
        edges = circle_top_edges
            + screw_ret[4] # end_edges
    )

    bmesh.ops.rotate(
        bm,
        cent = (0, 0, 0),
        matrix = Matrix.Rotation(-math.pi / 2, 4, 'Y'),
        verts = bm.verts
    )

    bm.normal_update()

    mesh = bpy.data.meshes.new(
        basis_cap_name
        + '_' + str((
            r,
            t,
            h,
            iterations,
            step_h,
            step_w,
            bottom_h,
            p
        ))
    )

    bm.to_mesh(mesh)
    bm.free()

    return mesh