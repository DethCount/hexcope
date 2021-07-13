import bpy
import math

# e: epsilon, smallest change in position
# t: thickness
# h: height
# r: hex side length
# p: precision in number of parts of 1
# wr: wheel radius
# mr: middle bar radius
# kr: key radius
# kw: key width
# hex_thickness: mirror hex thickness
# hex_walls_height : mirror hex walls height
def create_mesh(e, t, h, r, p, wr, mr, kr, kw, z, hex_thickness, hex_walls_height):
    mesh = bpy.data.meshes.new('basis_wheel_mesh' + str((
        e, t, h, r, p, wr, mr, kr, kw, z,
        hex_thickness, hex_walls_height
    )))

    pi2 = math.pi / 2
    pi3 = math.pi / 3

    hr = 0.5 * r
    hkw = 0.5 * kw

    z0 = z - hex_thickness - e
    z1 = z0 - hex_thickness
    z0o = z0 - hex_walls_height
    z1o = z1 - hex_walls_height
    z2 = z + -wr * math.sin(pi3)
    z3 = z2 + mr
    z4 = z2 + kr
    z5 = z2 - mr
    z6 = z2 - kr

    vertices = [
        (-e, hr - e, 0),
        (-hex_thickness, hr - e, 0),
        (-hex_thickness, -hr + e, 0),
        (-e, -hr + e, 0),

        (-hex_thickness, hr - e, z0),
        (-2 * hex_thickness - e, hr - e, z0),
        (-2 * hex_thickness - e, -hr + e, z0),
        (-hex_thickness, -hr + e, z0),

        # 8
        (-hex_thickness, hr - e, z1),
        (-2 * hex_thickness - e, hr - e, z1),
        (-2 * hex_thickness - e, -hr + e, z1),
        (-hex_thickness, -hr + e, z1),

        (-e, hr - e, z0o),
        (-e + hex_thickness, hr - e, z0o),
        (-e + hex_thickness, -hr + e, z0o),
        (-e, -hr + e, z0o),

        # 16
        (-e + hex_thickness, hr - e, z1o),
        (-e + hex_thickness, -hr + e, z1o),

        # 18
        (-e, hr - e, z1),
        (-hex_thickness, hr - e, z1),
        (-hex_thickness, -hr + e, z1),
        (-e, -hr + e, z1),

        (-e, 0, z2),
        (-hex_thickness, 0, z2),
        (-e, 0, z1),
        (-hex_thickness, 0, z1),

        # 26
        (-e, hr - e, z1o),
        (-e, -hr + e, z1o),
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (8, 9), (9, 10), (10, 11), (11, 8),
        (4, 8), (5, 9), (6, 10), (7, 11),
        (12, 13), (13, 14), (14, 15), (15, 12),
        (26, 16), (16, 17), (17, 27),
        (13, 16), (14, 17),

        (18, 19), (19, 20), (20, 21), (21, 18),
        (0, 18),
        (1, 4), (4, 8), (8, 19),
        (2, 7), (7, 11), (11, 20),
        (3, 21),
        (26, 27), (12, 26), (15, 27),
    ]
    faces = [
        (0, 1, 2, 3),

        (4, 5, 6, 7),
        (9, 8, 11, 10),
        (2, 1, 4, 7),
        (11, 8, 19, 20),

        (6, 5, 9, 10),
        (5, 4, 8, 9),
        (7, 6, 10, 11),

        (1, 0, 18, 19),
        (3, 2, 20, 21),
        (0, 3, 15, 12),

        (13, 12, 15, 14),
        (12, 13, 16, 26),
        (14, 15, 27, 17),
        (13, 14, 17, 16),
        (16, 17, 27, 26),
    ]

    nb_verts = len(vertices)
    tv = None

    for i in range(0, p + 1):
        alpha = i * math.pi / p
        beta = pi2 + alpha
        cb = math.cos(beta)
        sb = math.sin(beta)

        vertices.extend([
            (-hex_thickness, wr * cb, z2 + wr * sb),
            (-e, wr * cb, z2 + wr * sb),

            (-hex_thickness, mr * cb, z2 + mr * sb),
            (-e, mr * cb, z2 + mr * sb),


            (-hex_thickness, -wr * cb, z2 + wr * sb),
            (-e, -wr * cb, z2 + wr * sb),

            (-hex_thickness, -mr * cb, z2 + mr * sb),
            (-e, -mr * cb, z2 + mr * sb),
        ])

        nbidx = 8
        lrv = nb_verts + nbidx * i
        llv = lrv + 1
        srv = lrv + 2
        slv = lrv + 3
        rlrv = lrv + 4
        rllv = lrv + 5
        rsrv = lrv + 6
        rslv = lrv + 7

        if i > 0:
            edges.extend([
                (srv - nbidx, srv),
                (slv - nbidx, slv),
                (rsrv - nbidx, rsrv),
                (rslv - nbidx, rslv),
            ])

            if alpha < pi2 and ( \
                vertices[lrv - nbidx][1] > vertices[11][1]
                or vertices[lrv - nbidx][2] > vertices[11][2]
            ):
                faces.extend([
                    (24, slv, slv - nbidx),
                    (25, srv - nbidx, srv),
                    (24, rslv - nbidx, rslv),
                    (25, rsrv, rsrv - nbidx),
                ])
            else:
                if tv == None:
                    tv = True

                    edges.extend([
                        (llv - nbidx, lrv - nbidx),
                        (21, llv - nbidx),
                        (11, lrv - nbidx),

                        (rllv - nbidx, rlrv - nbidx),
                        (18, rllv - nbidx),
                        (8, rlrv - nbidx),
                    ])

                    faces.extend([
                        (21, slv, 24),
                        (25, srv, 11),
                        (24, rslv, 18),
                        (8, rsrv, 25),

                        (slv, slv - nbidx, 21, llv - nbidx),
                        (srv - nbidx, srv, lrv - nbidx, 11),
                        (rslv - nbidx, rslv, rllv - nbidx, 18),
                        (rsrv, rsrv - nbidx, 8, rlrv - nbidx),

                        (lrv - nbidx, llv - nbidx, 21, 11),
                        (rllv - nbidx, rlrv - nbidx, 8, 18),
                    ])
                edges.extend([
                    (lrv, llv),
                    (rlrv, rllv),

                    (lrv - nbidx, lrv),
                    (llv - nbidx, llv),
                    (rlrv - nbidx, rlrv),
                    (rllv - nbidx, rllv),
                ])
                faces.extend([
                    (lrv - nbidx, lrv, llv, llv - nbidx),

                    (lrv, lrv - nbidx, srv - nbidx, srv),
                    (llv - nbidx, llv, slv, slv - nbidx),

                    (rlrv, rlrv - nbidx, rllv - nbidx, rllv),

                    (rlrv - nbidx, rlrv, rsrv, rsrv - nbidx),
                    (rllv, rllv - nbidx, rslv - nbidx, rslv),
                ])

            faces.extend([
                (srv, srv - nbidx, slv - nbidx, slv),
                (rsrv - nbidx, rsrv, rslv, rslv - nbidx),
            ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh