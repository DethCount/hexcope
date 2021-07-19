import bpy
import math

# e: epsilon, smallest change in position
# t: thickness
# h: height
# r: hex side length
# p: precision in number of parts of 1
# wr: wheel radius
# mr: middle bar radius
# hex_thickness: mirror hex thickness
# hex_walls_height : mirror hex walls height
def create_mesh(
    e, t, h, r, p, wr, mr, z,
    hex_thickness, hex_walls_height,
    arm_t
):
    mesh = bpy.data.meshes.new('basis_wheel_mesh' + str((
        e, t, h, r, p, wr, mr, z,
        hex_thickness, hex_walls_height,
        arm_t
    )))

    pi2 = math.pi / 2
    pi3 = math.pi / 3

    he = 0.5 * e
    hr = 0.5 * r
    hht = 0.5 * hex_thickness
    hat = 0.5 * arm_t

    z0 = z - hex_thickness - e
    z1 = z0 - hex_thickness
    z0o = z0 - hex_walls_height
    z1o = z1 - hex_walls_height
    z2 = z - wr * math.sin(pi3)
    z3 = z0o - hex_thickness

    xr0 = e
    xl0 = -hex_thickness
    xr1 = xr0 + hex_thickness
    xl1 = xl0 - hex_thickness
    xl2 = xl0 + hht - hat - t - he
    xr2 = xl2 + t
    xl3 = xr0 - hht + hat + he
    xr3 = xl3 + t

    yt0 = hr - e
    yb0 = -yt0

    vertices = [
        (xr0, yt0, 0),
        (xl0, yt0, 0),
        (xl0, yb0, 0),
        (xr0, yb0, 0),

        (xl0, yt0, z0),
        (xl1, yt0, z0),
        (xl1, yb0, z0),
        (xl0, yb0, z0),

        # 8
        (xl0, yt0, z0o),
        (xl1, yt0, z0o),
        (xl1, yb0, z0o),
        (xl0, yb0, z0o),

        (xr0, yt0, z0o),
        (xr1, yt0, z0o),
        (xr1, yb0, z0o),
        (xr0, yb0, z0o),

        # 16
        (xr1, yt0, z0o),
        (xr1, yb0, z0o),

        # 18
        (xr0, yt0, z1),
        (xl0, yt0, z1),
        (xl0, yb0, z1),
        (xr0, yb0, z1),

        (xr0, 0, z2),
        (xl0, 0, z2),
        (xr0, 0, z1),
        (xl0, 0, z1),

        # 26
        (xr0, yt0, z0o),
        (xr0, yb0, z0o),

        # 28
        (xl2, yt0, z0o),
        (xr3, yt0, z0o),
        (xl2, yb0, z0o),
        (xr3, yb0, z0o),

        # 32
        (xl3, yt0, z3),
        (xr2, yt0, z3),
        (xl3, yb0, z3),
        (xr2, yb0, z3),

        # 36
        (xl2, yt0, z3),
        (xr3, yt0, z3),
        (xl2, yb0, z3),
        (xr3, yb0, z3),

        # 40
        (xl2, 0, z3),
        (xr2, 0, z3),
        (xl3, 0, z3),
        (xr3, 0, z3),

        # 44
        (xr2, yt0, z0o),
        (xl3, yt0, z0o),
        (xr2, yb0, z0o),
        (xl3, yb0, z0o),
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

        (28, 29), (29, 31), (31, 30), (30, 28),
    ]

    faces = [
        (0, 1, 2, 3),

        (4, 5, 6, 7),
        (2, 1, 4, 7),
        (11, 8, 19, 20),

        (6, 5, 9, 10),
        (5, 4, 8, 9),
        (7, 6, 10, 11),

        (1, 0, 18, 19),
        (3, 2, 20, 21),
        (0, 3, 15, 12),

        (13, 12, 15, 14),

        (28, 30, 10, 9),
        (31, 29, 13, 14),

        (33, 32, 34, 35),
    ]

    nb_verts = len(vertices)
    tv = None

    for i in range(0, p + 1):
        alpha = i * math.pi / p
        beta = pi2 + alpha
        cb = math.cos(beta)
        sb = math.sin(beta)
        wrcb = wr * cb
        wrsb = wr * sb
        mrcb = mr * cb
        mrsb = mr * sb
        z2wr = z2 + wrsb
        z2mr = z2 + mrsb

        vertices.extend([
            (xl2, wrcb, z2wr),
            (xr2, wrcb, z2wr),

            (xl2, mrcb, z2mr),
            (xr2, mrcb, z2mr),

            (xl2, -wrcb, z2wr),
            (xr2, -wrcb, z2wr),

            (xl2, -mrcb, z2mr),
            (xr2, -mrcb, z2mr),

            (xl3, wrcb, z2wr),
            (xr3, wrcb, z2wr),

            (xl3, mrcb, z2mr),
            (xr3, mrcb, z2mr),

            (xl3, -wrcb, z2wr),
            (xr3, -wrcb, z2wr),

            (xl3, -mrcb, z2mr),
            (xr3, -mrcb, z2mr),
        ])

        nbidx = 16
        rlllv = nb_verts + nbidx * i
        rllrv = rlllv + 1
        rlslv = rlllv + 2
        rlsrv = rlllv + 3
        rrllv = rlllv + 4
        rrlrv = rlllv + 5
        rrslv = rlllv + 6
        rrsrv = rlllv + 7
        llllv = rlllv + 8
        lllrv = rlllv + 9
        llslv = rlllv + 10
        llsrv = rlllv + 11
        lrllv = rlllv + 12
        lrlrv = rlllv + 13
        lrslv = rlllv + 14
        lrsrv = rlllv + 15

        if i > 0:
            edges.extend([
                (rlslv - nbidx, rlslv),
                (rlsrv - nbidx, rlsrv),
                (rrslv - nbidx, rrslv),
                (rrsrv - nbidx, rrsrv),

                (llslv - nbidx, llslv),
                (llsrv - nbidx, llsrv),
                (lrslv - nbidx, lrslv),
                (lrsrv - nbidx, lrsrv),
            ])

            if alpha < pi2 and ( \
                vertices[rlllv - nbidx][1] > vertices[32][1]
                or vertices[rlllv - nbidx][2] > vertices[32][2]
            ):
                faces.extend([
                    (41, rlsrv, rlsrv - nbidx),
                    (40, rlslv - nbidx, rlslv),
                    (41, rrsrv - nbidx, rrsrv),
                    (40, rrslv, rrslv - nbidx),

                    (43, llsrv, llsrv - nbidx),
                    (42, llslv - nbidx, llslv),
                    (43, lrsrv - nbidx, lrsrv),
                    (42, lrslv, lrslv - nbidx),
                ])
            else:
                if tv == None:
                    tv = True

                    edges.extend([
                        (rllrv - nbidx, rlllv - nbidx),
                        (46, rllrv - nbidx),
                        (30, rlllv - nbidx),

                        (rrlrv - nbidx, rrllv - nbidx),
                        (44, rrlrv - nbidx),
                        (28, rrllv - nbidx),

                        (lllrv - nbidx, llllv - nbidx),
                        (31, lllrv - nbidx),
                        (47, llllv - nbidx),

                        (lrlrv - nbidx, lrllv - nbidx),
                        (29, lrlrv - nbidx),
                        (45, lrllv - nbidx),
                    ])

                    faces.extend([
                        (35, rlsrv - nbidx, 41),
                        (40, rlslv - nbidx, 38),
                        (41, rrsrv - nbidx, 33),
                        (36, rrslv - nbidx, 40),

                        (39, llsrv - nbidx, 43),
                        (42, llslv - nbidx, 34),
                        (43, lrsrv - nbidx, 37),
                        (32, lrslv - nbidx, 42),

                        (36, 38, 30, 28),
                        (39, 37, 29, 31),

                        (30, 38, rlllv - nbidx),
                        (36, 28, rrllv - nbidx),

                        (rlsrv, rlsrv - nbidx, 35, rllrv - nbidx),
                        (38, rlslv - nbidx, rlslv, rlllv - nbidx),
                        (33, rrsrv - nbidx, rrsrv, rrlrv - nbidx),
                        (rrslv, rrslv - nbidx, 36, rrllv - nbidx),

                        (39, 31, lllrv - nbidx),
                        (29, 37, lrlrv - nbidx),

                        (llsrv, llsrv - nbidx, 39, lllrv - nbidx),
                        (34, llslv - nbidx, llslv, llllv - nbidx),
                        (37, lrsrv - nbidx, lrsrv, lrlrv - nbidx),
                        (lrslv, lrslv - nbidx, 32, lrllv - nbidx),

                        (rlllv - nbidx, rllrv - nbidx, 46, 30),
                        (rrlrv - nbidx, rrllv - nbidx, 28, 44),

                        (llllv - nbidx, lllrv - nbidx, 31, 47),
                        (lrlrv - nbidx, lrllv - nbidx, 45, 29),

                        (rllrv - nbidx, llllv - nbidx, 47, 46),
                        (llllv - nbidx, rllrv - nbidx, 35, 34),

                        (lrllv - nbidx, rrlrv - nbidx, 44, 45),
                        (rrlrv - nbidx, lrllv - nbidx, 32, 33),
                    ])
                edges.extend([
                    (rlllv, rllrv),
                    (rrllv, rrlrv),

                    (llllv, lllrv),
                    (lrllv, lrlrv),

                    (rlllv - nbidx, rlllv),
                    (rllrv - nbidx, rllrv),
                    (rrllv - nbidx, rrllv),
                    (rrlrv - nbidx, rrlrv),

                    (llllv - nbidx, llllv),
                    (lllrv - nbidx, lllrv),
                    (lrllv - nbidx, lrllv),
                    (lrlrv - nbidx, lrlrv),
                ])

                faces.extend([
                    (rlllv - nbidx, rlllv, rllrv, rllrv - nbidx),
                    (rlllv, rlllv - nbidx, rlslv - nbidx, rlslv),
                    (rllrv - nbidx, rllrv, rlsrv, rlsrv - nbidx),
                    (rrllv, rrllv - nbidx, rrlrv - nbidx, rrlrv),
                    (rrllv - nbidx, rrllv, rrslv, rrslv - nbidx),
                    (rrlrv, rrlrv - nbidx, rrsrv - nbidx, rrsrv),

                    (llllv - nbidx, llllv, lllrv, lllrv - nbidx),
                    (llllv, llllv - nbidx, llslv - nbidx, llslv),
                    (lllrv - nbidx, lllrv, llsrv, llsrv - nbidx),
                    (lrllv, lrllv - nbidx, lrlrv - nbidx, lrlrv),
                    (lrllv - nbidx, lrllv, lrslv, lrslv - nbidx),
                    (lrlrv, lrlrv - nbidx, lrsrv - nbidx, lrsrv),
                ])

            faces.extend([
                (rlslv, rlslv - nbidx, rlsrv - nbidx, rlsrv),
                (rrslv - nbidx, rrslv, rrsrv, rrsrv - nbidx),

                (llslv, llslv - nbidx, llsrv - nbidx, llsrv),
                (lrslv - nbidx, lrslv, lrsrv, lrsrv - nbidx),
            ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh