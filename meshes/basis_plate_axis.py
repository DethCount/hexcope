import bpy
import math

basis_plate_axis_name = 'basis_plate_axis'

def create_mesh(
    e, t, r, p, x, z,
    top_t, top_r,
    bottom_t, bottom_r
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

    vertices = [
        (x, 0, z + top_t + e),
        (x, 0, z),
        (x, 0, z - t),
        (x, 0, z - t - bottom_t),
    ]
    edges = []
    faces = []

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (2 * math.pi) / p
        beta = 0 + alpha
        cb = math.cos(beta)
        sb = math.sin(beta)

        nbidx = 6
        ttv = nb_verts + i * nbidx
        tbv = ttv + 1
        wtv = ttv + 2
        wbv = ttv + 3
        btv = ttv + 4
        bbv = ttv + 5

        vertices.extend([
            (x + tr * cb, tr * sb, z + top_t + e),
            (x + tr * cb, tr * sb, z),
            (x + r * cb, r * sb, z),
            (x + r * cb, r * sb, z - t),
            (x + br * cb, br * sb, z - t),
            (x + br * cb, br * sb, z - t - bottom_t),
        ])

        edges.extend([
            (ttv, tbv),
            (wtv, wbv),
            (btv, bbv),
        ])

        if i > 0:
            edges.extend([
                (ttv - nbidx, ttv),
                (tbv - nbidx, tbv),
                (wtv - nbidx, wtv),
                (wbv - nbidx, wbv),
                (btv - nbidx, btv),
                (bbv - nbidx, bbv),
            ])

            faces.extend([
                (ttv - nbidx, ttv, 0),
                (ttv, ttv - nbidx, tbv - nbidx, tbv),
                (tbv, tbv - nbidx, wtv - nbidx, wtv),
                (wtv, wtv - nbidx, wbv - nbidx, wbv),
                (wbv, wbv - nbidx, btv - nbidx, btv),
                (btv, btv - nbidx, bbv - nbidx, bbv),
                (bbv, bbv - nbidx, 3),
            ])


    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh