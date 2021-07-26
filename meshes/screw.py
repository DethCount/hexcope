import bpy
import bmesh
import math
from mathutils import Vector

def screw_in(
    r,
    iterations,
    step_h,
    step_w,
    length,
    p,
    bm = None,
    z_start = 0,
    ccw = False
):
    if bm == None:
        bm = bmesh.new()

    qsw = 0.25 * step_w

    screw_r = r - step_h
    z_end = z_start - max((iterations + 1) * step_w, length)

    start = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    start_edges = list(set(
        e
        for v in start['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_start)),
        verts = start['verts']
    )

    end = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    end_edges = list(set(
        e
        for v in end['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_end)),
        verts = end['verts']
    )

    if iterations <= 0:
        bmesh.ops.bridge_loops(
            bm,
            edges = start_edges
                + end_edges
        )
    else:
        first_verts = list()
        last_verts = list()

        screw_bottom_end = list()
        screw_bottom_end_edges = list()

        screw_top_start = list()
        screw_top_start_edges = list()

        screw_top_end = list()
        screw_top_end_edges = list()

        screw_bottom_start = list()
        screw_bottom_start_edges = list()
        for i in range(0, iterations):
            for j in range(0, p + 1):
                alpha = i * math.tau + j * math.tau / p
                alpha *= -1 if ccw else 1
                ca = math.cos(alpha)
                sa = math.sin(alpha)

                rca = r * ca
                rsa = r * sa
                srca = screw_r * ca
                srsa = screw_r * sa

                z_bev = z_start - (i + j / p) * step_w

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (rca, rsa, z_bev)
                )

                bev = ret['vert'][0]
                screw_bottom_end.append(bev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (srca, srsa, z_bev - qsw)
                )

                tsv = ret['vert'][0]
                screw_top_start.append(tsv)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (srca, srsa, z_bev - 2 * qsw)
                )

                tev = ret['vert'][0]
                screw_top_end.append(tev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (rca, rsa, z_bev - 3 * qsw)
                )

                bsv = ret['vert'][0]
                screw_bottom_start.append(bsv)

                if i > 0 or j > 0:
                    e = bm.edges.new((prev_bev, bev))
                    screw_bottom_end_edges.append(e)

                    e = bm.edges.new((prev_tsv, tsv))
                    screw_top_start_edges.append(e)

                    e = bm.edges.new((prev_tev, tev))
                    screw_top_end_edges.append(e)

                    e = bm.edges.new((prev_bsv, bsv))
                    screw_bottom_start_edges.append(e)

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
            edges = screw_bottom_end_edges
                + screw_top_start_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_top_start_edges
                + screw_top_end_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_top_end_edges
                + screw_bottom_start_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_bottom_end_edges
                + screw_bottom_start_edges
        )

        bm.faces.new(first_verts)
        bm.faces.new(last_verts)


    bmesh.ops.bridge_loops(
        bm,
        edges = start_edges
            + end_edges
    )

    bmesh.ops.reverse_faces(bm, faces = bm.faces)

    return [bm, start, start_edges, end, end_edges]



def screw(
    r,
    iterations,
    step_h,
    step_w,
    p,
    bm = None,
    z_top = 0,
    ccw = False,
    top_length = 0,
    bottom_length = 0,
    tip_r = 0,
    tip_length = None,
    fill_tip = True
):
    if bm == None:
        bm = bmesh.new()

    qsw = 0.25 * step_w

    screw_r = r - step_h
    z_top_end = z_top + top_length - step_w
    z_start = z_top_end + step_w
    z_stop = z_start + (iterations + 1) * step_w
    z_tip = z_stop + (tip_length if tip_length != None else step_w)

    top = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    top_edges = list(set(
        e
        for v in top['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_top)),
        verts = top['verts']
    )

    top_end = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = r
    )

    top_end_edges = list(set(
        e
        for v in top_end['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_top_end)),
        verts = top_end['verts']
    )

    start = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = screw_r
    )

    start_edges = list(set(
        e
        for v in start['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_start)),
        verts = start['verts']
    )

    stop = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = screw_r
    )

    stop_edges = list(set(
        e
        for v in stop['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_stop)),
        verts = stop['verts']
    )

    tip = bmesh.ops.create_circle(
        bm,
        segments = p,
        radius = tip_r
    )

    tip_edges = list(set(
        e
        for v in tip['verts']
        for e in v.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_tip)),
        verts = tip['verts']
    )

    if iterations <= 0:
        bmesh.ops.bridge_loops(
            bm,
            edges = start_edges
                + stop_edges
        )
    else:
        first_verts = list()
        last_verts = list()

        screw_bottom_end = list()
        screw_bottom_end_edges = list()

        screw_top_start = list()
        screw_top_start_edges = list()

        screw_top_end = list()
        screw_top_end_edges = list()

        screw_bottom_start = list()
        screw_bottom_start_edges = list()
        for i in range(0, iterations):
            for j in range(0, p + 1):
                alpha = i * math.tau + j * math.tau / p
                alpha *= -1 if ccw else 1
                ca = math.cos(alpha)
                sa = math.sin(alpha)

                rca = r * ca
                rsa = r * sa
                srca = screw_r * ca
                srsa = screw_r * sa

                z_bev = z_start + (i + j / p) * step_w

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (srca, srsa, z_bev)
                )

                bev = ret['vert'][0]
                screw_bottom_end.append(bev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (rca, rsa, z_bev + qsw)
                )

                tsv = ret['vert'][0]
                screw_top_start.append(tsv)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (rca, rsa, z_bev + 2 * qsw)
                )

                tev = ret['vert'][0]
                screw_top_end.append(tev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (srca, srsa, z_bev + 3 * qsw)
                )

                bsv = ret['vert'][0]
                screw_bottom_start.append(bsv)

                if i > 0 or j > 0:
                    e = bm.edges.new((prev_bev, bev))
                    screw_bottom_end_edges.append(e)

                    e = bm.edges.new((prev_tsv, tsv))
                    screw_top_start_edges.append(e)

                    e = bm.edges.new((prev_tev, tev))
                    screw_top_end_edges.append(e)

                    e = bm.edges.new((prev_bsv, bsv))
                    screw_bottom_start_edges.append(e)

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
            edges = screw_bottom_end_edges
                + screw_top_start_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_top_start_edges
                + screw_top_end_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_top_end_edges
                + screw_bottom_start_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_bottom_end_edges
                + screw_bottom_start_edges
        )

        bm.faces.new(first_verts)
        bm.faces.new(last_verts)

    bmesh.ops.bridge_loops(
        bm,
        edges = top_edges
            + top_end_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = top_end_edges
            + start_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = start_edges
            + stop_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = stop_edges
            + tip_edges
    )

    if fill_tip != False:
        bmesh.ops.edgeloop_fill(
            bm,
            edges = tip_edges
        )

    return [bm, top, top_edges, tip, tip_edges]