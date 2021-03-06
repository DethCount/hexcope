import types
import bpy
import bmesh
import math
from mathutils import Matrix, Vector
from meshes import screw

import importlib
importlib.reload(screw)

basis_cap_name = 'basis_cap'

def create_mesh(
    r,
    t,
    h,
    p,
    top_h = 0,
    bottom_h = 0,
    bm = None,
    head_r = None,
    head_length = None,
):
    if bm == None:
        bm = bmesh.new()

    zz_inner_top = -h -top_h
    zz_top = zz_inner_top - t
    zz_butt = -0.01
    z_screw_start = -bottom_h
    screw_length = h - bottom_h

    outer_r = r + t

    if head_r == None:
        head_r = outer_r + t

    if head_length == None:
        head_length = 0.25 * h

    circle_top = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = outer_r
    )

    circle_top_edges = list(set(
        edg
        for vec in circle_top['verts']
        for edg in vec.link_edges)
    )

    circle_head_start = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = head_r
    )

    circle_head_start_edges = list(set(
        edg
        for vec in circle_head_start['verts']
        for edg in vec.link_edges)
    )

    circle_head_end = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = head_r
    )

    circle_head_end_edges = list(set(
        edg
        for vec in circle_head_end['verts']
        for edg in vec.link_edges)
    )

    circle_head_end_bottom = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = outer_r
    )

    circle_head_end_bottom_edges = list(set(
        edg
        for vec in circle_head_end_bottom['verts']
        for edg in vec.link_edges)
    )

    circle_bottom = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = outer_r
    )

    circle_bottom_edges = list(set(
        edg
        for vec in circle_bottom['verts']
        for edg in vec.link_edges)
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_top_edges
            + circle_head_start_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_head_start_edges
            + circle_head_end_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_head_end_edges
            + circle_head_end_bottom_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_head_end_bottom_edges
            + circle_bottom_edges
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, zz_top)),
        verts = circle_top['verts']
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, zz_top)),
        verts = circle_head_start['verts']
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, zz_top + head_length)),
        verts = circle_head_end['verts']
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, zz_top + head_length)),
        verts = circle_head_end_bottom['verts']
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, zz_butt)),
        verts = circle_bottom['verts']
    )

    for i in range(0, p):
        alpha = i * 6 * math.tau / p
        x = t * math.cos(alpha)
        y = t * math.sin(alpha)

        bmesh.ops.translate(
            bm,
            vec = Vector((x, y, 0)),
            verts = [
                circle_head_start['verts'][i],
                circle_head_end['verts'][i]
            ]
        )

    circle_inner_butt = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    circle_inner_butt_edges = list(set(
        edg
        for vec in circle_inner_butt['verts']
        for edg in vec.link_edges)
    )

    screw_ret = screw.screw_in(
        r,
        screw_length,
        p,
        bm,
        z_screw_start,
        fill_end=True,
        end_h=top_h
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_bottom_edges
            + circle_inner_butt_edges
    )

    bmesh.ops.edgeloop_fill(
        bm,
        edges = circle_top_edges
    )

    bmesh.ops.reverse_faces(bm, faces = bm.faces)

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
            p,
            top_h,
            bottom_h,
            head_r,
            head_length,
        ))
    )

    bm.to_mesh(mesh)
    bm.free()

    return mesh