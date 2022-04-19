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

    bottom_inner_circle_end = bmesh.ops.create_circle(
        bm,
        segments = screw_precision,
        radius = 0.5 * screw_D
    )

    bottom_inner_circle_end_edges = list(set(
        edg
        for v in bottom_inner_circle_end['verts']
        for edg in v.link_edges
    ))

    bmesh.ops.edgeloop_fill(
        bm,
        edges = bottom_inner_circle_end_edges
    )

    ret = bmesh.ops.extrude_edge_only(
        bm,
        edges = bottom_inner_circle_end_edges
    )

    bottom_inner_circle = list(set(
        geom
        for geom in ret['geom']
        if isinstance(geom, bmesh.types.BMVert)
    ))

    bottom_inner_circle_edges = list(set(
        geom
        for geom in ret['geom']
        if isinstance(geom, bmesh.types.BMEdge)
    ))

    bottom_outer_circle = bmesh.ops.create_circle(
        bm,
        segments=screw_precision,
        radius = r
    )

    bottom_outer_circle_edges = list(set(
        edg
        for v in bottom_outer_circle['verts']
        for edg in v.link_edges
    ))

    bmesh.ops.bridge_loops(
        bm,
        edges = bottom_inner_circle_edges
            + bottom_outer_circle_edges
    )

    ret = bmesh.ops.extrude_edge_only(
        bm,
        edges = bottom_outer_circle_edges
    )

    bottom_outer_circle_end = list(set(
        geom
        for geom in ret['geom']
        if isinstance(geom, bmesh.types.BMVert)
    ))

    bottom_outer_circle_end_edges = list(set(
        edg
        for v in bottom_outer_circle_end
        for edg in v.link_edges
    ))

    top_inner_circle = bmesh.ops.create_circle(
        bm,
        segments=screw_precision,
        radius = 0.5 * screw_D
    )

    top_inner_circle_edges = list(set(
        edg
        for v in top_inner_circle['verts']
        for edg in v.link_edges
    ))

    # bmesh.ops.bridge_loops(
    #     bm,
    #     edges = top_inner_circle_edges
    #         + bottom_outer_circle_end_edges
    # )

    ret = bmesh.ops.extrude_edge_only(
        bm,
        edges = top_inner_circle_edges
    )

    top_inner_circle_end = list(set(
        geom
        for geom in ret['geom']
        if isinstance(geom, bmesh.types.BMVert)
    ))

    top_inner_circle_end_edges = list(set(
        edg
        for v in top_inner_circle_end
        for edg in v.link_edges
    ))

    bmesh.ops.edgeloop_fill(
        bm,
        edges = top_inner_circle_end_edges
    )

    bmesh.ops.translate(
        bm,
        verts = bottom_inner_circle_end['verts'],
        vec = (0, 0, screw_length + screw_end_h)
    )

    bmesh.ops.translate(
        bm,
        verts = bottom_outer_circle_end,
        vec = (0, 0, length - screw_length)
    )

    bmesh.ops.translate(
        bm,
        verts = top_inner_circle['verts'],
        vec = (0, 0, length - screw_length)
    )

    bmesh.ops.translate(
        bm,
        verts = top_inner_circle_end,
        vec = (0, 0, length)
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
    arm_idx,
    n,
    hex_side_length,
    secondary_z,
    secondary_dist_to_spider_arm,
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
            get_support_arm_point(i, hex_side_length, 0)[0][0]
        )

        length = arm_points_x[i] - (arm_points_x[i - 1] if i > 0 else (secondary_dist_to_spider_arm + hahw))

        mesh = create_mesh(
            r,
            length,
            screw_length,
            screw_precision,
            screw_D,
            screw_P,
            screw_end_h
        )

        obj = bpy.data.objects.new(spider_arm_name + '_' + str(arm_idx) + '_' + str(i), mesh)
        obj.location.x = arm_points_x[i] - hahw
        obj.location.z = secondary_z
        objs.append(obj)

    return objs