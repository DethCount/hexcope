import bpy
import math

basis_plate_axis_name = 'basis_plate_axis'

def create_mesh(
    e, t, r, p, x, z,
    top_t, top_r,
    bottom_t, bottom_r,
    rotor_t, rotor_r
):
    mesh = bpy.data.meshes.new(
        basis_plate_axis_name
        + '_' + str((
            e, t, r, p, x, z,
            top_t, top_r,
            bottom_t, bottom_r
        ))
    )

    tr = top_r - e
    br = bottom_r - e
    rr = rotor_r + 0.5 * e

    vertices = [
        (x, 0, z + top_t + e),
        (x, 0, z),
        (x, 0, z - t),
        (x, 0, z - t - bottom_t),
        (x, 0, z + top_t + e - rotor_t),
    ]
    edges = []
    faces = []

    nb_verts = len(vertices)

    nbidx_rotor = 4
    rotor_p = math.ceil((5 / 12) * p)
    rotor_max_tvl = None
    rotor_max_tvr = None
    for i in range (0, rotor_p + 1):
        alpha = i * (2 * math.pi) / p
        beta = 0 + alpha
        cb = math.cos(beta)
        sb = math.sin(beta)

        gamma = 0 - alpha
        cg = math.cos(gamma)
        sg = math.sin(gamma)

        tvl = nb_verts + i * nbidx_rotor
        bvl = tvl + 1
        tvr = tvl + 2
        bvr = tvl + 3

        vertices.extend([
            (x + rr * cb, rr * sb, z + top_t + e),
            (x + rr * cb, rr * sb, z + top_t + e - rotor_t),
            (x + rr * cg, rr * sg, z + top_t + e),
            (x + rr * cg, rr * sg, z + top_t + e - rotor_t),
        ])

        edges.extend([
            (tvl, bvl),
            (tvr, bvr),
        ])

        if i > 0:
            edges.extend([
                (tvl - nbidx_rotor, tvl),
                (bvl - nbidx_rotor, bvl),
                (tvr - nbidx_rotor, tvr),
                (bvr - nbidx_rotor, bvr),
            ])

            faces.extend([
                (tvl - nbidx_rotor, tvl, bvl, bvl - nbidx_rotor),
                (tvr, tvr - nbidx_rotor, bvr - nbidx_rotor, bvr),
                (bvl - nbidx_rotor, bvl, 4),
                (bvr, bvr - nbidx_rotor, 4),
            ])

        if i == rotor_p:
            edges.extend([
                (tvl, tvr),
                (bvl, bvr),
            ])

            faces.extend([
                (tvl, tvr, bvr, bvl),
                (bvl, bvr, 4),
            ])

            rotor_max_tvl = tvl
            rotor_max_tvr = tvr


    nb_verts2 = len(vertices)
    max_p = round(0.5 * p)
    for i in range(0, max_p + 1):
        alpha = i * (2 * math.pi) / p
        beta = 0 + alpha
        cb = math.cos(beta)
        sb = math.sin(beta)

        gamma = 0 - alpha
        cg = math.cos(gamma)
        sg = math.sin(gamma)

        nbidx = 12
        ttvl = nb_verts2 + i * nbidx
        tbvl = ttvl + 1
        wtvl = ttvl + 2
        wbvl = ttvl + 3
        btvl = ttvl + 4
        bbvl = ttvl + 5
        ttvr = ttvl + 6
        tbvr = ttvl + 7
        wtvr = ttvl + 8
        wbvr = ttvl + 9
        btvr = ttvl + 10
        bbvr = ttvl + 11

        vertices.extend([
            (x + tr * cb, tr * sb, z + top_t + e),
            (x + tr * cb, tr * sb, z),
            (x + r * cb, r * sb, z),
            (x + r * cb, r * sb, z - t),
            (x + br * cb, br * sb, z - t),
            (x + br * cb, br * sb, z - t - bottom_t),

            (x + tr * cg, tr * sg, z + top_t + e),
            (x + tr * cg, tr * sg, z),
            (x + r * cg, r * sg, z),
            (x + r * cg, r * sg, z - t),
            (x + br * cg, br * sg, z - t),
            (x + br * cg, br * sg, z - t - bottom_t),
        ])

        edges.extend([
            (ttvl, tbvl),
            (wtvl, wbvl),
            (btvl, bbvl),

            (ttvl, tbvl),
            (wtvl, wbvl),
            (btvl, bbvl),
        ])

        if i > 0:
            edges.extend([
                (ttvl - nbidx, ttvl),
                (tbvl - nbidx, tbvl),
                (wtvl - nbidx, wtvl),
                (wbvl - nbidx, wbvl),
                (btvl - nbidx, btvl),
                (bbvl - nbidx, bbvl),

                (ttvr - nbidx, ttvr),
                (tbvr - nbidx, tbvr),
                (wtvr - nbidx, wtvr),
                (wbvr - nbidx, wbvr),
                (btvr - nbidx, btvr),
                (bbvr - nbidx, bbvr),
            ])

            rotor_idx_l = nb_verts + min(i, rotor_p) * nbidx_rotor
            rotor_idx_r = rotor_idx_l + 2

            faces.extend([
                (ttvl - nbidx, ttvl, rotor_idx_l, rotor_idx_l - nbidx_rotor),
                (ttvl, ttvl - nbidx, tbvl - nbidx, tbvl),
                (tbvl, tbvl - nbidx, wtvl - nbidx, wtvl),
                (wtvl, wtvl - nbidx, wbvl - nbidx, wbvl),
                (wbvl, wbvl - nbidx, btvl - nbidx, btvl),
                (btvl, btvl - nbidx, bbvl - nbidx, bbvl),
                (bbvl, bbvl - nbidx, 3),

                (ttvr, ttvr - nbidx, rotor_idx_r - nbidx_rotor, rotor_idx_r),
                (ttvr - nbidx, ttvr, tbvr, tbvr - nbidx),
                (tbvr - nbidx, tbvr, wtvr, wtvr - nbidx),
                (wtvr - nbidx, wtvr, wbvr, wbvr - nbidx),
                (wbvr - nbidx, wbvr, btvr, btvr - nbidx),
                (btvr - nbidx, btvr, bbvr, bbvr - nbidx),
                (bbvr - nbidx, bbvr, 3),
            ])

    faces.extend([
        (rotor_max_tvr, rotor_max_tvl, ttvl, ttvr),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh