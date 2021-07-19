import bpy
import math

basis_arm_name = 'basis_arm'

# e: epsilon, smallest change in position
# t: thickness
# h: height
# w: width
# p: precision in number of parts of 1
# z: z position
# wheel_thickness: wheel thickness
# wheel_radius: wheel radius
# middle_bar_radius: middle bar radius
# teeth_width: bottom teeth width
# teeth_height: bottom teeth height
# teeth_thickness: bottom teeth thickness
def create_mesh(
    e, t, h, w, p, z,
    wheel_thickness, wheel_radius,
    middle_bar_radius,
    teeth_width, teeth_height, teeth_thickness
):
    mesh = bpy.data.meshes.new(
        basis_arm_name
        + '_' + str((
            e, t, h, w, p, z,
            wheel_thickness, wheel_radius,
            middle_bar_radius,
            teeth_width, teeth_height, teeth_thickness
        ))
    )

    lr = t + middle_bar_radius # large radius
    hw = 0.5 * w
    hwr = 0.5 * wheel_radius
    hwt = 0.5 * wheel_thickness
    htt = 0.5 * teeth_thickness
    htw = 0.5 * teeth_width

    h1 = h - (wheel_radius + e + teeth_height)# arm filled block height

    z0 = z + lr
    z1 = z - hwr
    z2 = z - wheel_radius - e
    z3 = z2 - h1 # teeth top z
    z4 = z3 - teeth_height # teeth bottom z

    x = -hwt
    xr = x + 0.5 * t
    xl = x - 0.5 * t
    xr2 = x + t
    xl2 = x - t
    xr3 = x + htt
    xl3 = x - htt

    vertices = [
        (xl, 0, z0),
        (xl - t, 0, z0),
        (xl - t, 0, z),
        (xl, 0, z),
    ]
    edges = [(0, 1)]
    faces = []

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (math.pi / 2) / p
        beta = alpha

        cb = math.cos(beta)
        sb = math.sin(beta)

        lrsb = lr * sb
        mbry = middle_bar_radius * sb

        lz = z + lr * cb
        sz = z + middle_bar_radius * cb

        vertices.extend([
            (xl, lrsb, lz),
            (xl, -lrsb, lz),

            (xl, mbry, sz),
            (xl, -mbry, sz),

            (xr, lrsb, lz),
            (xr, -lrsb, lz),

            (xr, mbry, sz),
            (xr, -mbry, sz),
        ])

        nbidx = 8

        lllv = nb_verts + nbidx * i
        llrv = lllv + 1
        lslv = lllv + 2
        lsrv = lllv + 3
        rllv = lllv + 4
        rlrv = lllv + 5
        rslv = lllv + 6
        rsrv = lllv + 7

        edges.extend([
            (lllv, rllv),
            (llrv, rlrv),
            (lslv, rslv),
            (lsrv, rsrv),
        ])

        if i > 0:
            edges.extend([
                (lllv, lllv - nbidx),
                (llrv, llrv - nbidx),
                (lslv, lslv - nbidx),
                (lsrv, lsrv - nbidx),
            ])

            faces.extend([
                (lllv - nbidx, lllv, lslv, lslv - nbidx),
                (llrv - nbidx, llrv, lsrv, lsrv - nbidx),

                (rllv - nbidx, rllv, rslv, rslv - nbidx),
                (rlrv - nbidx, rlrv, rsrv, rsrv - nbidx),

                (lllv, lllv - nbidx, rllv - nbidx, rllv),
                (llrv - nbidx, llrv, rlrv, rlrv - nbidx),

                (lslv, lslv - nbidx, rslv - nbidx, rslv),
                (lsrv - nbidx, lsrv, rsrv, rsrv - nbidx),
            ])

    nb_verts = len(vertices)

    vertices.extend([
        (xl, hw, z1),
        (xl, -hw, z1),

        (xr, hw, z1),
        (xr, -hw, z1),
    ])

    edges.extend([
        (nb_verts, nb_verts + 2),
        (nb_verts + 1, nb_verts + 3),

        (lllv, nb_verts),
        (llrv, nb_verts + 1),

        (rllv, nb_verts + 2),
        (rlrv, nb_verts + 3),
    ])

    faces.extend([
        (lllv, nb_verts, nb_verts + 2, rllv),
        (llrv, nb_verts + 1, nb_verts + 3, rlrv),
        (lllv, lslv, nb_verts),
        (llrv, lsrv, nb_verts + 1),
        (rllv, rslv, nb_verts + 2),
        (rlrv, rsrv, nb_verts + 3),
    ])

    nb_verts2 = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (math.pi / 2) / p
        beta = math.pi / 2 + alpha

        cb = math.cos(beta)
        sb = math.sin(beta)

        mbry = middle_bar_radius * sb
        sz = z + middle_bar_radius * cb

        vertices.extend([
            (xl, mbry, sz),
            (xl, -mbry, sz),

            (xr, mbry, sz),
            (xr, -mbry, sz),
        ])

        nbidx = 4
        llv = nb_verts2 + nbidx * i
        lrv = llv + 1
        rlv = llv + 2
        rrv = llv + 3

        edges.extend([
            (llv, llv - nbidx),
            (lrv, lrv - nbidx),
            (llv, rlv),
            (lrv, rrv),
        ])

        if i > 0:
            faces.extend([
                (llv - nbidx, llv, rlv, rlv - nbidx),
                (lrv - nbidx, lrv, rrv, rrv - nbidx),

                (llv - nbidx, llv, nb_verts),
                (lrv - nbidx, lrv, nb_verts + 1),

                (rlv - nbidx, rlv, nb_verts + 2),
                (rrv - nbidx, rrv, nb_verts + 3),
            ])

    faces.extend([
        (nb_verts, nb_verts + 1, llv),
        (nb_verts + 2, nb_verts + 3, rlv),
    ])

    nb_verts3 = len(vertices)

    vertices.extend([
        (xl, hw, z2),
        (xl, -hw, z2),

        (xr, hw, z2),
        (xr, -hw, z2),

        (xl2, hw, z2 - t),
        (xl2, -hw, z2 - t),

        (xr2, hw, z2 - t),
        (xr2, -hw, z2 - t),
    ])

    edges.extend([
        (nb_verts, nb_verts3),
        (nb_verts + 1, nb_verts3 + 1),
        (nb_verts + 2, nb_verts3 + 2),
        (nb_verts + 3, nb_verts3 + 3),

        (nb_verts3, nb_verts3 + 1),
        (nb_verts3 + 1, nb_verts3 + 3),
        (nb_verts3 + 3, nb_verts3 + 2),
        (nb_verts3 + 2, nb_verts3),

        (nb_verts3, nb_verts3 + 4),
        (nb_verts3 + 1, nb_verts3 + 5),
        (nb_verts3 + 2, nb_verts3 + 6),
        (nb_verts3 + 3, nb_verts3 + 7),
    ])

    faces.extend([
        (nb_verts, nb_verts3, nb_verts3 + 2, nb_verts + 2),
        (nb_verts + 1, nb_verts3 + 1, nb_verts3 + 3, nb_verts + 3),
        (nb_verts, nb_verts3, nb_verts3 + 1, nb_verts + 1),
        (nb_verts + 2, nb_verts3 + 2, nb_verts3 + 3, nb_verts + 3),

        (nb_verts3, nb_verts3 + 4, nb_verts3 + 6, nb_verts3 + 2),
        (nb_verts3 + 1, nb_verts3 + 5, nb_verts3 + 7, nb_verts3 + 3),
        (nb_verts3, nb_verts3 + 1, nb_verts3 + 5, nb_verts3 + 4),
        (nb_verts3 + 2, nb_verts3 + 3, nb_verts3 + 7, nb_verts3 + 6),
    ])

    nb_verts4 = len(vertices)

    vertices.extend([
        (xl2, hw, z3),
        (xl2, -hw, z3),

        (xr2, hw, z3),
        (xr2, -hw, z3),

        (xl3, htw, z3),
        (xl3, -htw, z3),

        (xr3, htw, z3),
        (xr3, -htw, z3),

        (xl3, htw, z4),
        (xl3, -htw, z4),

        (xr3, htw, z4),
        (xr3, -htw, z4),
    ])

    edges.extend([
        (nb_verts3 + 4, nb_verts4),
        (nb_verts3 + 5, nb_verts4 + 1),
        (nb_verts3 + 6, nb_verts4 + 2),
        (nb_verts3 + 7, nb_verts4 + 3),

        (nb_verts4, nb_verts4 + 1),
        (nb_verts4 + 1, nb_verts4 + 3),
        (nb_verts4 + 3, nb_verts4 + 2),
        (nb_verts4 + 2, nb_verts4),

        (nb_verts4 + 4, nb_verts4 + 6),
        (nb_verts4 + 6, nb_verts4 + 7),
        (nb_verts4 + 7, nb_verts4 + 5),
        (nb_verts4 + 5, nb_verts4 + 4),

        (nb_verts4 + 8, nb_verts4 + 10),
        (nb_verts4 + 10, nb_verts4 + 11),
        (nb_verts4 + 11, nb_verts4 + 9),
        (nb_verts4 + 9, nb_verts4 + 8),

        (nb_verts4 + 4, nb_verts4 + 8),
        (nb_verts4 + 5, nb_verts4 + 9),
        (nb_verts4 + 6, nb_verts4 + 10),
        (nb_verts4 + 7, nb_verts4 + 11),
    ])

    faces.extend([
        (nb_verts3 + 4, nb_verts4, nb_verts4 + 1, nb_verts3 + 5),
        (nb_verts3 + 6, nb_verts4 + 2, nb_verts4 + 3, nb_verts3 + 7),
        (nb_verts3 + 4, nb_verts4, nb_verts4 + 2, nb_verts3 + 6),
        (nb_verts3 + 5, nb_verts4 + 1, nb_verts4 + 3, nb_verts3 + 7),

        (nb_verts4, nb_verts4 + 1, nb_verts4 + 5, nb_verts4 + 4),
        (nb_verts4 + 2, nb_verts4 + 3, nb_verts4 + 7, nb_verts4 + 6),

        (nb_verts4 + 1, nb_verts4 + 3, nb_verts4 + 7, nb_verts4 + 5),
        (nb_verts4, nb_verts4 + 2, nb_verts4 + 6, nb_verts4 + 4),

        (nb_verts4 + 4, nb_verts4 + 5, nb_verts4 + 9, nb_verts4 + 8),
        (nb_verts4 + 5, nb_verts4 + 7, nb_verts4 + 11, nb_verts4 + 9),
        (nb_verts4 + 7, nb_verts4 + 11, nb_verts4 + 10, nb_verts4 + 6),
        (nb_verts4 + 8, nb_verts4 + 10, nb_verts4 + 6, nb_verts4 + 4),

        (nb_verts4 + 8, nb_verts4 + 9, nb_verts4 + 11, nb_verts4 + 10),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh