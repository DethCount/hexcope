import bpy
import bmesh
import math
from mathutils import Matrix, Vector

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
    z_inner_top = zz_top + t
    z_start = -bottom_h

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


    circle_start = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    circle_start_edges = list(set(
        e
        for v in circle_start['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_start)),
        verts = circle_start['verts']
    )

    circle_inner_top = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    circle_inner_top_edges = list(set(
        e
        for v in circle_inner_top['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_inner_top)),
        verts = circle_inner_top['verts']
    )

    if iterations <= 0:
        bmesh.ops.bridge_loops(
            bm,
            edges = circle_start_edges
                + circle_inner_top_edges
        )
    else:
        first_verts = list()
        last_verts = list()

        circle_screw_bottom_end = list()
        circle_screw_bottom_end_edges = list()

        circle_screw_top_start = list()
        circle_screw_top_start_edges = list()

        circle_screw_top_end = list()
        circle_screw_top_end_edges = list()

        circle_screw_bottom_start = list()
        circle_screw_bottom_start_edges = list()
        screw_r = r - step_h
        for i in range(0, iterations):
            for j in range(0, p + 1):
                alpha = i * math.tau + j * math.tau / p

                z_bev = z_start - (i * step_w + j * step_w / p)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (
                        r * math.cos(alpha),
                        r * math.sin(alpha),
                        z_bev
                    )
                )

                bev = ret['vert'][0]
                circle_screw_bottom_end.append(bev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (
                        screw_r * math.cos(alpha),
                        screw_r * math.sin(alpha),
                        z_bev - step_w / 4
                    )
                )

                tsv = ret['vert'][0]
                circle_screw_top_start.append(tsv)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (
                        screw_r * math.cos(alpha),
                        screw_r * math.sin(alpha),
                        z_bev - 2 * step_w / 4
                    )
                )

                tev = ret['vert'][0]
                circle_screw_top_end.append(tev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (
                        r * math.cos(alpha),
                        r * math.sin(alpha),
                        z_bev - 3 * step_w / 4
                    )
                )

                bsv = ret['vert'][0]
                circle_screw_bottom_start.append(bsv)

                if i > 0 or j > 0:
                    e = bm.edges.new((prev_bev, bev))
                    circle_screw_bottom_end_edges.append(e)

                    e = bm.edges.new((prev_tsv, tsv))
                    circle_screw_top_start_edges.append(e)

                    e = bm.edges.new((prev_tev, tev))
                    circle_screw_top_end_edges.append(e)

                    e = bm.edges.new((prev_bsv, bsv))
                    circle_screw_bottom_start_edges.append(e)

                    if i == iterations - 1 and j == p:
                        last_verts.extend([bev, tsv, tev, bsv])
                else:
                    first_verts.extend([bev, tsv, tev, bsv])

                prev_bev = bev
                prev_tsv = tsv
                prev_tev = tev
                prev_bsv = bsv

        bmesh.ops.bridge_loops(
            bm,
            edges = circle_screw_bottom_end_edges
                + circle_screw_top_start_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = circle_screw_top_start_edges
                + circle_screw_top_end_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = circle_screw_top_end_edges
                + circle_screw_bottom_start_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = circle_screw_bottom_end_edges
                + circle_screw_bottom_start_edges
        )

        bm.faces.new(first_verts)
        bm.faces.new(last_verts)

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
            + circle_start_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = circle_start_edges
            + circle_inner_top_edges
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, -zz_butt)),
        verts = circle_bottom['verts']
    )

    bmesh.ops.edgeloop_fill(
        bm,
        edges = circle_top_edges
            + circle_inner_top_edges
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