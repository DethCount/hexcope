import bpy
import bmesh
import math
from mathutils import Matrix, Vector
from meshes import screw

import importlib
importlib.reload(screw)

basis_screw_name = 'basis_screw'

def create_mesh(
    r,
    length,
    start_h,
    head_r,
    head_h,
    p
):
    bm = bmesh.new()

    z_head_top = -head_h
    z_head_bottom = -0.001 * head_h

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

    screw_P = screw.get_P(2.0 * r)
    screw_ret = screw.screw(
        r,
        length,
        p,
        bm,
        z_top = z_head_bottom,
        top_length = start_h,
        tip_r = r - 2 * screw_P,
        tip_length = screw_P,
        fill_tip = True,
        P = screw_P
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
            length,
            start_h,
            head_r,
            head_h,
            p
        ))
    )

    bm.to_mesh(mesh)
    bm.free()

    return mesh
