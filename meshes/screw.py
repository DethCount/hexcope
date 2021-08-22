import bpy
import bmesh
import math
from mathutils import Vector

DEFAULT_P = {
    "0.001": 0.00025,
    "0.0011": 0.00025,
    "0.0012": 0.00025,
    "0.0014": 0.0003,
    "0.0016": 0.00035,
    "0.002": 0.0004,
    "0.0025": 0.00045,
    "0.003": 0.0005,
    "0.004": 0.0007,
    "0.005": 0.0008,
    "0.006": 0.001,
    "0.008": 0.00125,
    "0.01": 0.0015,
    "0.012": 0.00175,
    "0.014": 0.002,
    "0.016": 0.002,
    "0.018": 0.0025,
    "0.02": 0.0025,
    "0.022": 0.0025,
    "0.024": 0.003,
    "0.027": 0.003,
    "0.03": 0.0035,
    "0.033": 0.0035,
    "0.036": 0.004,
    "0.039": 0.004,
    "0.042": 0.0045,
    "0.045": 0.0045,
    "0.048": 0.005,
    "0.052": 0.005,
    "0.056": 0.0055,
    "0.06": 0.0055,
    "0.064": 0.006
}

def get_d1(D, P):
    return D - 1.8025 * P

def get_d2(D, P):
    return D - 0.6495 * P

def get_d3(D, P):
    return D - 1.2268 * P

def get_r0(D, P):
    return 0.5 * get_d1(D, P)

def get_r1(D, P):
    return

def get_H(P):
    return 0.5 * math.sqrt(3) * P

def get_D(d):
    final_d = None
    for normalized_d in DEFAULT_P:
        f_normalized_d = float(normalized_d)
        if f_normalized_d > d:
            break

        final_d = f_normalized_d

    return final_d

def get_P(D):
    d = get_D(D)
    if d != None:
        return math.sqrt(3) * DEFAULT_P[str(d)]

    return None

def screw_in(
    r,
    length,
    precision,
    bm = None,
    z_start = 0,
    z_scale = 1,
    fill_start = False,
    fill_end = False,
    D = None,
    P = None,
    start_h = 0,
    end_h = 0,
    max_screw_top_precision = 5,
    ccw = False
):
    if bm == None:
        bm = bmesh.new()

    d = D if D != None else get_D(2.0 * r)
    # print('D', str(D), str(2 * r), str(d))
    step_w = (P if P != None else get_P(d))
    # print('P', str(P), str(step_w))
    step_h = get_H(step_w)
    iterations = math.floor(length / step_w)

    r0 = 0.5 * d
    r1 = r0 - (1 - 0.125 - 0.25) * step_h
    screw_top_r = 0.0625 * step_w
    screw_bottom_r = 0.125 * step_w
    r2 = r0 + math.sqrt(3) * screw_top_r

    z_rot_scale = z_scale if ccw else -z_scale

    z_te = z_scale * screw_top_r
    z_bs = z_scale * (0.5 * step_w - screw_bottom_r)
    z_be = z_scale * (0.5 * step_w + screw_bottom_r)
    z_ts = z_scale * (step_w - screw_top_r)

    z0 = z_scale * z_start
    z1 = z0 - z_scale * (0 if start_h <= 0 else start_h)
    z_screw_end = z1 - z_scale * iterations * step_w
    z_end = z_screw_end - z_scale * end_h
    z_last_start = z_screw_end

    start = bmesh.ops.create_circle(
        bm,
        segments = precision,
        radius = r0
    )

    start_edges = list(set(
        edg
        for vec in start['verts']
        for edg in vec.link_edges)
    )

    if start_h > 0:
        before_start = bmesh.ops.create_circle(
            bm,
            segments = precision,
            radius = r
        )

        before_start_edges = list(set(
            edg
            for vec in before_start['verts']
            for edg in vec.link_edges)
        )

        bmesh.ops.translate(
            bm,
            vec = Vector((0, 0, z0)),
            verts = before_start['verts']
        )

        bmesh.ops.bridge_loops(
            bm,
            edges = before_start_edges
                + start_edges
        )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z1)),
        verts = start['verts']
    )

    end = bmesh.ops.create_circle(
        bm,
        segments = precision,
        radius = r0
    )

    end_edges = list(set(
        edg
        for vec in end['verts']
        for edg in vec.link_edges)
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
        start_first_loop = bmesh.ops.create_circle(
            bm,
            segments = precision + 1,
            radius = r0
        )

        start_first_loop_edges = list(set(
            edg
            for vec in start_first_loop['verts']
            for edg in vec.link_edges
        ))

        start_first_loop_b = bmesh.ops.create_circle(
            bm,
            segments = precision + 1,
            radius = r0
        )

        start_first_loop_b_edges = list(set(
            edg
            for vec in start_first_loop_b['verts']
            for edg in vec.link_edges
        ))

        start_first_loop_c = bmesh.ops.create_circle(
            bm,
            segments = precision + 1,
            radius = r0
        )

        start_first_loop_c_edges = list(set(
            edg
            for vec in start_first_loop_c['verts']
            for edg in vec.link_edges
        ))

        stop_last_loop = bmesh.ops.create_circle(
            bm,
            segments = precision + 1,
            radius = r0
        )

        stop_last_loop_edges = list(set(
            edg
            for vec in stop_last_loop['verts']
            for edg in vec.link_edges
        ))

        for i in range(0, len(start_first_loop['verts'])):
            ip = i / precision
            alpha = z_rot_scale * ip * math.tau
            ca = math.cos(alpha)
            sa = math.sin(alpha)
            z = z1 - z_scale * ip * step_w
            z_last = z_last_start - z_scale * ip * step_w

            bmesh.ops.translate(
                bm,
                vec = Vector((
                    -start_first_loop['verts'][i].co[0] + r0 * ca,
                    -start_first_loop['verts'][i].co[1] + r0 * sa,
                    min(z1, z + z_scale * screw_top_r) if z_scale >= 0
                        else max(z1, z + z_scale * screw_top_r)
                )),
                verts = [start_first_loop['verts'][i]]
            )

            bmesh.ops.translate(
                bm,
                vec = Vector((
                    -start_first_loop_b['verts'][i].co[0] + r2 * ca,
                    -start_first_loop_b['verts'][i].co[1] + r2 * sa,
                    z
                )),
                verts = [start_first_loop_b['verts'][i]]
            )

            bmesh.ops.translate(
                bm,
                vec = Vector((
                    -start_first_loop_c['verts'][i].co[0] + r0 * ca,
                    -start_first_loop_c['verts'][i].co[1] + r0 * sa,
                    min(z1, z - z_scale * screw_top_r) if z_scale >= 0
                        else max(z1, z - z_scale * screw_top_r)
                )),
                verts = [start_first_loop_c['verts'][i]]
            )

            bmesh.ops.translate(
                bm,
                vec = Vector((
                    -stop_last_loop['verts'][i].co[0] + r0 * ca,
                    -stop_last_loop['verts'][i].co[1] + r0 * sa,
                    max(z_end, z_last) if z_scale >= 0
                        else min(z_end, z_last)
                )),
                verts = [stop_last_loop['verts'][i]]
            )


        first_verts = list()
        last_verts = list()

        screw_bottom_end = list()
        screw_bottom_end_edges = list()

        screw_top_start = list()
        screw_top_start_edges = list()

        screw_top_circle = list()
        screw_top_circle_edges = list()

        screw_top_end = list()
        screw_top_end_edges = list()

        screw_bottom_start = list()
        screw_bottom_start_edges = list()

        for i in range(0, iterations):
            for j in range(0, precision + 1):
                jp = j / precision
                alpha = z_rot_scale * jp * math.tau
                ca = math.cos(alpha)
                sa = math.sin(alpha)

                dca = r0 * ca
                dsa = r0 * sa
                d1ca = r1 * ca
                d1sa = r1 * sa

                z = z1 - z_scale * (i + jp) * step_w

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (
                        dca,
                        dsa,
                        max(z_end, z - z_te) if z_scale >= 0
                            else min(z_end, z - z_te)
                    )
                )
                tev = ret['vert'][0]
                screw_top_end.append(tev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (
                        d1ca,
                        d1sa,
                        max(z_end, z - z_bs) if z_scale >= 0
                            else min(z_end, z - z_bs)
                    )
                )
                bsv = ret['vert'][0]
                screw_bottom_start.append(bsv)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (
                        d1ca,
                        d1sa,
                        max(z_end, z - z_be) if z_scale >= 0
                            else min(z_end, z - z_be)
                    )
                )
                bev = ret['vert'][0]
                screw_bottom_end.append(bev)

                tsco = (
                    dca,
                    dsa,
                    max(z_end, z - z_ts) if z_scale >= 0
                        else min(z_end, z - z_ts)
                )
                ret = bmesh.ops.create_vert(
                    bm,
                    co = tsco
                )
                tsv = ret['vert'][0]
                screw_top_start.append(tsv)

                if i > 0 or j > 0:
                    edg = bm.edges.new((prev_tev, tev))
                    screw_top_end_edges.append(edg)

                    edg = bm.edges.new((prev_bsv, bsv))
                    screw_bottom_start_edges.append(edg)

                    edg = bm.edges.new((prev_bev, bev))
                    screw_bottom_end_edges.append(edg)

                    edg = bm.edges.new((prev_tsv, tsv))
                    screw_top_start_edges.append(edg)

                    if i == iterations - 1 and j == precision:
                        last_verts.extend([tev, bsv, bev, tsv])
                else:
                    first_verts.extend([tev, bsv, bev, tsv])

                tcv = list()
                for k in range(0, max_screw_top_precision + 1):
                    kmstp = k / max_screw_top_precision
                    beta = (kmstp if z_scale < 0 else (1 - kmstp)) * math.pi
                    sb = math.sin(beta)
                    rk = r0 + screw_top_r * sb
                    z_st = tsco[2] - 2 * z_scale * screw_top_r * kmstp

                    if j == 0:
                        screw_top_circle.append(list())
                        screw_top_circle_edges.append(list())

                    ret = bmesh.ops.create_vert(
                        bm,
                        co = (
                            rk * ca,
                            rk * sa,
                            max(z_end, z_st) if z_scale >= 0
                                else min(z_end, z_st)
                        )
                    )

                    tcv.append(ret['vert'][0])
                    screw_top_circle[k].append(tcv[k])

                    if i > 0 or j > 0:
                        edg = bm.edges.new((prev_tcv[k], tcv[k]))
                        screw_top_circle_edges[k].append(edg)

                prev_tev = tev
                prev_bsv = bsv
                prev_bev = bev
                prev_tsv = tsv
                prev_tcv = tcv

        for k in range(0, max_screw_top_precision + 1):
            if k != 0:
                bmesh.ops.bridge_loops(
                    bm,
                    edges = screw_top_circle_edges[k - 1]
                        + screw_top_circle_edges[k]
                )

        bmesh.ops.bridge_loops(
            bm,
            edges = screw_top_end_edges
                + screw_bottom_start_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_bottom_start_edges
                + screw_bottom_end_edges
        )
        bmesh.ops.bridge_loops(
            bm,
            edges = screw_bottom_end_edges
                + screw_top_start_edges
        )

        first_face = bm.faces.new(first_verts)
        last_face = bm.faces.new(last_verts)

    bmesh.ops.bridge_loops(
        bm,
        edges = start_edges
            + start_first_loop_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = start_first_loop_edges
            + start_first_loop_b_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = start_first_loop_b_edges
            + start_first_loop_c_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = stop_last_loop_edges
            + end_edges
    )

    if fill_start == True:
        print(str(ccw), str(fill_start))
        bmesh.ops.edgeloop_fill(
            bm,
            edges = start_edges
        )

    if fill_end == True:
        bmesh.ops.edgeloop_fill(
            bm,
            edges = end_edges
        )

    if (z_scale < 0 and not ccw) or (ccw and z_scale >= 0):
        bmesh.ops.reverse_faces(bm, faces = list(set(
            f
            for edg in start_edges
                + start_first_loop_edges
                + start_first_loop_b_edges
                + start_first_loop_c_edges
                + stop_last_loop_edges
                + screw_top_end_edges
                + screw_bottom_start_edges
                + screw_bottom_end_edges
                + screw_top_start_edges
                + end_edges
            for f in edg.link_faces
        )))

        first_face.normal_flip()
    else:
        last_face.normal_flip()

    if ccw:
        bmesh.ops.reverse_faces(bm, faces = list(set(
            f
            for edg in start_edges
                + start_first_loop_edges
                + start_first_loop_b_edges
                + start_first_loop_c_edges
                + end_edges
            for f in edg.link_faces
        )))

    return [
        bm,
        before_start if start_h > 0 else start,
        before_start_edges if start_h > 0 else start_edges,
        end,
        end_edges
    ]

def screw(
    r,
    length,
    precision,
    bm = None,
    z_top = 0,
    top_length = 0,
    tip_r = 0,
    tip_length = None,
    fill_tip = True,
    D = None,
    P = None,
    max_screw_bottom_precision = 10,
    e = 0.002,
    ccw = False
):
    if bm == None:
        bm = bmesh.new()

    d = D if D != None else get_D(2.0 * r)
    step_w = P if P != None else get_P(d)
    step_h = get_H(step_w)
    iterations = math.floor(length / step_w)
    rot_sign = -1 if ccw else 1

    e = min(e, 0.5 * step_h)

    r0 = 0.5 * ((d - e) if d > e else d)
    r1 = r0 - (1 - 0.125 - 0.25) * step_h
    screw_top_r = 0.0625 * step_w
    screw_bottom_r = 0.125 * step_w
    r2 = r1 - math.sqrt(3) * screw_bottom_r
    tip_r_final = min(tip_r, r1 - 0.5 * e)

    z_be = screw_bottom_r
    z_ts = 0.5 * step_w - screw_top_r
    z_te = 0.5 * step_w + screw_top_r
    z_bs = step_w - screw_bottom_r

    z_top_end = (z_top + top_length - step_w) if top_length > 0 else 0
    z_start = z_top_end + step_w
    z_stop = z_start + (iterations + 1) * step_w + screw_bottom_r
    z_tip = z_stop + (tip_length if tip_length != None else step_w)

    top = bmesh.ops.create_circle(
        bm,
        segments = precision,
        radius = r
    )

    top_edges = list(set(
        edg
        for vec in top['verts']
        for edg in vec.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_top)),
        verts = top['verts']
    )

    if top_length > 0:
        top_end = bmesh.ops.create_circle(
            bm,
            segments = precision,
            radius = r
        )

        top_end_edges = list(set(
            edg
            for vec in top_end['verts']
            for edg in vec.link_edges)
        )

        bmesh.ops.translate(
            bm,
            vec = Vector((0, 0, z_top_end)),
            verts = top_end['verts']
        )

    start = bmesh.ops.create_circle(
        bm,
        segments = precision,
        radius = r1
    )

    start_edges = list(set(
        edg
        for vec in start['verts']
        for edg in vec.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_start)),
        verts = start['verts']
    )

    start_first_loop = bmesh.ops.create_circle(
        bm,
        segments = precision + 1,
        radius = r1
    )

    start_first_loop_edges = list(set(
        edg
        for vec in start_first_loop['verts']
        for edg in vec.link_edges)
    )

    start_first_loop_b = bmesh.ops.create_circle(
        bm,
        segments = precision + 1,
        radius = r1
    )

    start_first_loop_b_edges = list(set(
        edg
        for vec in start_first_loop_b['verts']
        for edg in vec.link_edges)
    )

    start_first_loop_c = bmesh.ops.create_circle(
        bm,
        segments = precision + 1,
        radius = r1
    )

    start_first_loop_c_edges = list(set(
        edg
        for vec in start_first_loop_c['verts']
        for edg in vec.link_edges)
    )

    stop_last_loop = bmesh.ops.create_circle(
        bm,
        segments = precision + 1,
        radius = r1
    )

    stop_last_loop_edges = list(set(
        edg
        for vec in stop_last_loop['verts']
        for edg in vec.link_edges)
    )

    for i in range(0, len(start_first_loop['verts'])):
        ip = i / precision
        alpha = rot_sign * ip * math.tau
        ca = math.cos(alpha)
        sa = math.sin(alpha)
        z = z_start + ip * step_w
        z_last = z_stop - ip * step_w

        vec = Vector((
            -start_first_loop['verts'][i].co[0] + r1 * ca,
            -start_first_loop['verts'][i].co[1] + r1 * sa,
            z - screw_bottom_r
        ))

        vec2 = Vector((
            -start_first_loop_b['verts'][i].co[0] + (r1 if alpha < 0.75 * math.pi else r2) * ca,
            -start_first_loop_b['verts'][i].co[1] + (r1 if alpha < 0.75 * math.pi else r2) * sa,
            z
        ))

        vec3 = Vector((
            -start_first_loop_c['verts'][i].co[0] + r1 * ca,
            -start_first_loop_c['verts'][i].co[1] + r1 * sa,
            z + screw_bottom_r
        ))

        vec4 = Vector((
            -stop_last_loop['verts'][i].co[0] + r1 * ca,
            -stop_last_loop['verts'][i].co[1] - r1 * sa,
            z_last
        ))

        bmesh.ops.translate(
            bm,
            vec = vec,
            verts = [start_first_loop['verts'][i]]
        )

        bmesh.ops.translate(
            bm,
            vec = vec2,
            verts = [start_first_loop_b['verts'][i]]
        )

        bmesh.ops.translate(
            bm,
            vec = vec3,
            verts = [start_first_loop_c['verts'][i]]
        )

        bmesh.ops.translate(
            bm,
            vec = vec4,
            verts = [stop_last_loop['verts'][i]]
        )

    stop = bmesh.ops.create_circle(
        bm,
        segments = precision,
        radius = r1
    )

    stop_edges = list(set(
        edg
        for vec in stop['verts']
        for edg in vec.link_edges)
    )

    bmesh.ops.translate(
        bm,
        vec = Vector((0, 0, z_stop)),
        verts = stop['verts']
    )

    tip = bmesh.ops.create_circle(
        bm,
        segments = precision,
        radius = tip_r_final
    )

    tip_edges = list(set(
        edg
        for vec in tip['verts']
        for edg in vec.link_edges)
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
        screw_bottom_end_first_loop = list()

        screw_top_start = list()
        screw_top_start_edges = list()

        screw_top_end = list()
        screw_top_end_edges = list()

        screw_bottom_start = list()
        screw_bottom_start_edges = list()

        screw_bottom_start = list()
        screw_bottom_start_edges = list()

        screw_bottom_circle = list()
        screw_bottom_circle_edges = list()

        prev_bev = None
        prev_tsv = None
        prev_tev = None
        prev_bsv = None
        prev_bcv = list()
        for i in range(0, iterations):
            for j in range(0, precision + 1):
                jp = j / precision
                alpha = rot_sign * jp * math.tau
                ca = math.cos(alpha)
                sa = math.sin(alpha)

                r0ca = r0 * ca
                r0sa = r0 * sa
                r1ca = r1 * ca
                r1sa = r1 * sa

                z = z_start + (i + jp) * step_w

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (r1ca, r1sa, z + z_be)
                )

                bev = ret['vert'][0]
                screw_bottom_end.append(bev)
                if i == 0:
                    screw_bottom_end_first_loop.append(bev)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (r0ca, r0sa, z + z_ts)
                )

                tsv = ret['vert'][0]
                screw_top_start.append(tsv)

                ret = bmesh.ops.create_vert(
                    bm,
                    co = (r0ca, r0sa, z + z_te)
                )

                tev = ret['vert'][0]
                screw_top_end.append(tev)

                bsco = (r1ca, r1sa, z + z_bs)
                ret = bmesh.ops.create_vert(
                    bm,
                    co = bsco
                )

                bsv = ret['vert'][0]
                screw_bottom_start.append(bsv)

                bcv = list()
                for k in range(0, max_screw_bottom_precision + 1):
                    kmsbp = k / max_screw_bottom_precision
                    beta = (1 - rot_sign * kmsbp) * math.pi
                    sb = math.sin(beta)
                    rk = r1 - screw_bottom_r * sb

                    if j == 0:
                        screw_bottom_circle.append(list())
                        screw_bottom_circle_edges.append(list())

                    ret = bmesh.ops.create_vert(
                        bm,
                        co = (
                            rk * ca,
                            rk * sa,
                            bsco[2] + 2 * screw_bottom_r * kmsbp
                        )
                    )

                    bcv.append(ret['vert'][0])
                    screw_bottom_circle[k].append(bcv[k])

                    if i > 0 or j > 0:
                        edg = bm.edges.new((prev_bcv[k], bcv[k]))
                        screw_bottom_circle_edges[k].append(edg)

                if i > 0 or j > 0:
                    edg = bm.edges.new((prev_bev, bev))
                    screw_bottom_end_edges.append(edg)

                    edg = bm.edges.new((prev_tsv, tsv))
                    screw_top_start_edges.append(edg)

                    edg = bm.edges.new((prev_tev, tev))
                    screw_top_end_edges.append(edg)

                    edg = bm.edges.new((prev_bsv, bsv))
                    screw_bottom_start_edges.append(edg)

                    if i == iterations - 1 and j == precision:
                        last_verts.extend([bev, tsv, tev, bsv])
                else:
                    first_verts.extend([bev, tsv, tev, bsv])

                prev_bev = bev
                prev_tsv = tsv
                prev_tev = tev
                prev_bsv = bsv
                prev_bcv = bcv

        screw_bottom_circles_edges = list()
        for k in range(0, max_screw_bottom_precision + 1):
            screw_bottom_circles_edges.extend(screw_bottom_circle_edges[k])

            if k != 0:
                bmesh.ops.bridge_loops(
                    bm,
                    edges = screw_bottom_circle_edges[k - 1]
                        + screw_bottom_circle_edges[k]
                )

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

        first_face = bm.faces.new(first_verts)
        last_face = bm.faces.new(last_verts)
        if not ccw:
            last_face.normal_flip()
        else:
            first_face.normal_flip()

    if top_length > 0:
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
    else:
        bmesh.ops.bridge_loops(
            bm,
            edges = top_edges
                + start_edges
        )

    bmesh.ops.bridge_loops(
        bm,
        edges = start_edges
            + start_first_loop_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = start_first_loop_edges
            + start_first_loop_b_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = start_first_loop_b_edges
            + start_first_loop_c_edges
    )

    bmesh.ops.bridge_loops(
        bm,
        edges = stop_last_loop_edges
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

    if ccw:
        bmesh.ops.reverse_faces(bm, faces = list(set(
            f
            for edg in screw_bottom_end_edges
                + screw_top_start_edges
                + screw_top_end_edges
                + screw_bottom_start_edges
                + screw_bottom_circles_edges
            for f in edg.link_faces
        )))

    return [bm, top, top_edges, tip, tip_edges]