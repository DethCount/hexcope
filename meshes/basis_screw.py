import bpy
import bmesh
import math
from mathutils import Matrix, Vector

basis_screw_name = 'basis_screw'

def create_mesh(
    r,
    start,
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
    z_start_up = start
    z_start = start + step_w
    z_stop = z_start + iterations * step_w
    z_bottom = z_stop + bottom_h

    r_screw_bottom = r - step_h

    circle_head_top = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = head_r
    )
    circle_head_top_edges = list(set(
        e
        for v in circle_head_top['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_head_top)),
        verts = circle_head_top['verts']
    )

    circle_head_bottom = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = head_r
    )

    circle_head_bottom_edges = list(set(
        e
        for v in circle_head_bottom['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_head_bottom)),
        verts = circle_head_bottom['verts']
    )

    circle_screw_top = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    circle_screw_top_edges = list(set(
        e
        for v in circle_screw_top['verts']
        for e in v.link_edges)
    )

    circle_screw_start_up = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    circle_screw_start_up_edges = list(set(
        e
        for v in circle_screw_start_up['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_start_up)),
        verts = circle_screw_start_up['verts']
    )

    circle_screw_start = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r_screw_bottom
    )

    circle_screw_start_edges = list(set(
        e
        for v in circle_screw_start['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_start)),
        verts = circle_screw_start['verts']
    )

    circle_screw_stop = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r_screw_bottom
    )

    circle_screw_stop_edges = list(set(
        e
        for v in circle_screw_stop['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_stop)),
        verts = circle_screw_stop['verts']
    )

    circle_screw_bottom = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = bottom_r
    )

    circle_screw_bottom_edges = list(set(
        e
        for v in circle_screw_bottom['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_bottom)),
        verts = circle_screw_bottom['verts']
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_head_top_edges
            + circle_head_bottom_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_head_bottom_edges
            + circle_screw_top_edges
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, -z_head_bottom)),
        verts = circle_head_bottom['verts']
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_screw_top_edges
            + circle_screw_start_up_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_screw_start_up_edges
            + circle_screw_start_edges
    )

    if iterations <= 0:
        bmesh.ops.bridge_loops(
            bm,
            edges = circle_screw_start_edges
                + circle_screw_stop_edges
        )
    else:
        min_h = r * math.sin(math.pi / 4)
        circle_bottom_start_edges = list()
        for i in range(0, iterations):
            circle_top_start = bmesh.ops.create_circle(
                bm,
                segments = p,
                radius = r_screw_bottom
            )

            circle_top_start_edges = list(set(
                e
                for v in circle_top_start['verts']
                for e in v.link_edges)
            )

            bmesh.ops.translate(
                bm,
                vec = Vector((0, 0, z_start + i * step_w + step_w / 4)),
                verts = circle_top_start['verts']
            )

            if i == 0:
                bmesh.ops.bridge_loops(
                    bm,
                    edges = circle_screw_start_edges
                        + circle_top_start_edges
                )
            else:
                bmesh.ops.bridge_loops(
                    bm,
                    edges = circle_bottom_end_edges
                        + circle_top_start_edges
                )

            circle_top_end = bmesh.ops.create_circle(
                bm,
                segments = p,
                radius = r_screw_bottom
            )

            circle_top_end_edges = list(set(
                e
                for v in circle_top_end['verts']
                for e in v.link_edges)
            )

            bmesh.ops.translate(
                bm,
                vec = Vector((0, 0, z_start + i * step_w + 2 * step_w / 4)),
                verts = circle_top_end['verts']
            )

            bmesh.ops.bridge_loops(
                bm,
                edges = circle_top_start_edges
                    + circle_top_end_edges
            )

            vtop = circle_top_start['verts'] + circle_top_end['verts']

            bmesh.ops.translate(
                bm,
                vec = Vector((step_h, 0, 0)),
                verts = list(v
                    for v in vtop
                    if v.co.x > min_h
                )
            )

            bmesh.ops.translate(
                bm,
                vec = Vector((-step_h, 0, 0)),
                verts = list(v
                    for v in vtop
                    if v.co.x < -min_h
                )
            )

            circle_bottom_start = bmesh.ops.create_circle(
                bm,
                segments = p,
                radius = r_screw_bottom
            )

            circle_bottom_start_edges = list(set(
                e
                for v in circle_bottom_start['verts']
                for e in v.link_edges)
            )

            bmesh.ops.translate(
                bm,
                vec = Vector((0, 0, z_start + i * step_w + 3 * step_w / 4)),
                verts = circle_bottom_start['verts']
            )

            bmesh.ops.bridge_loops(
                bm,
                edges = circle_top_end_edges
                    + circle_bottom_start_edges
            )

            if i < iterations - 1:
                circle_bottom_end = bmesh.ops.create_circle(
                    bm,
                    segments = p,
                    radius = r_screw_bottom
                )

                circle_bottom_end_edges = list(set(
                    e
                    for v in circle_bottom_end['verts']
                    for e in v.link_edges)
                )

                bmesh.ops.translate(
                    bm,
                    vec = Vector((0, 0, z_start + (i + 1) * step_w)),
                    verts = circle_bottom_end['verts']
                )

                bmesh.ops.bridge_loops(
                    bm,
                    edges = circle_bottom_start_edges
                        + circle_bottom_end_edges
                )
            else:
                bmesh.ops.bridge_loops(
                    bm,
                    edges = circle_bottom_start_edges
                        + circle_screw_stop_edges
                )


    bmesh.ops.bridge_loops(
        bm,
        edges = circle_screw_stop_edges
            + circle_screw_bottom_edges
    )

    bmesh.ops.edgeloop_fill(
        bm,
        edges = circle_head_top_edges
            + circle_screw_bottom_edges
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
            start,
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
