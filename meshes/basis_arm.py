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

    h1 = h - (wheel_radius + e + teeth_height)# arm filled block height

    z0 = z + lr
    z1 = z - hwr
    z2 = z - wheel_radius - e
    z3 = z2 - h1 # teeth top z
    z4 = z3 - teeth_height # teeth bottom z

    vertices = [
        (-wheel_thickness - e, 0, z0),
        (-wheel_thickness - e - t, 0, z0),
        (-wheel_thickness - e - t, 0, z),
        (-wheel_thickness - e, 0, z),
    ]
    edges = [(0, 1)]
    faces = []

    nb_verts = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (math.pi / 2) / p
        beta = alpha

        cb = math.cos(beta)
        sb = math.sin(beta)

        lz = z + lr * cb
        sz = z + middle_bar_radius * cb

        vertices.extend([
            (-wheel_thickness - e - t, lr * sb, lz),
            (-wheel_thickness - e, lr * sb, lz),

            (-wheel_thickness - e - t, middle_bar_radius * sb, sz),
            (-wheel_thickness - e, middle_bar_radius * sb, sz),

            (-wheel_thickness - e - t, -lr * sb, lz),
            (-wheel_thickness - e, -lr * sb, lz),

            (-wheel_thickness - e - t, -middle_bar_radius * sb, sz),
            (-wheel_thickness - e, -middle_bar_radius * sb, sz),

            (e + t, lr * sb, lz),
            (e, lr * sb, lz),

            (e + t, middle_bar_radius * sb, sz),
            (e, middle_bar_radius * sb, sz),

            (e + t, -lr * sb, z + lr * cb),
            (e, -lr * sb, z + lr * cb),

            (e + t, -middle_bar_radius * sb, sz),
            (e, -middle_bar_radius * sb, sz),
        ])

        llllv = nb_verts + 16 * i
        lllrv = nb_verts + 16 * i + 1

        llslv = nb_verts + 16 * i + 2
        llsrv = nb_verts + 16 * i + 3

        lrllv = nb_verts + 16 * i + 4
        lrlrv = nb_verts + 16 * i + 5

        lrslv = nb_verts + 16 * i + 6
        lrsrv = nb_verts + 16 * i + 7

        rlllv = nb_verts + 16 * i + 8
        rllrv = nb_verts + 16 * i + 9

        rlslv = nb_verts + 16 * i + 10
        rlsrv = nb_verts + 16 * i + 11

        rrllv = nb_verts + 16 * i + 12
        rrlrv = nb_verts + 16 * i + 13

        rrslv = nb_verts + 16 * i + 14
        rrsrv = nb_verts + 16 * i + 15

        edges.extend([
            (llllv, lllrv),
            (llslv, llsrv),

            (lrllv, lrlrv),
            (lrslv, lrsrv),

            (rlllv, rllrv),
            (rlslv, rlsrv),

            (rrllv, rrlrv),
            (rrslv, rrsrv),
        ])

        if i > 0:
            faces.extend([
                (llllv - 16, llllv, lllrv, lllrv - 16),
                (llllv - 16, llllv, llslv, llslv - 16),
                (lllrv - 16, lllrv, llsrv, llsrv - 16),
                (llslv - 16, llslv, llsrv, llsrv - 16),

                (lrllv - 16, lrllv, lrlrv, lrlrv - 16),
                (lrllv - 16, lrllv, lrslv, lrslv - 16),
                (lrlrv - 16, lrlrv, lrsrv, lrsrv - 16),
                (lrslv - 16, lrslv, lrsrv, lrsrv - 16),

                (rlllv - 16, rlllv, rllrv, rllrv - 16),
                (rlllv - 16, rlllv, rlslv, rlslv - 16),
                (rllrv - 16, rllrv, rlsrv, rlsrv - 16),
                (rlslv - 16, rlslv, rlsrv, rlsrv - 16),

                (rrllv - 16, rrllv, rrlrv, rrlrv - 16),
                (rrllv - 16, rrllv, rrslv, rrslv - 16),
                (rrlrv - 16, rrlrv, rrsrv, rrsrv - 16),
                (rrslv - 16, rrslv, rrsrv, rrsrv - 16),
            ])

    nb_verts = len(vertices)

    vertices.extend([
        (-wheel_thickness - e - t, hw, z1),
        (-wheel_thickness - e, hw, z1),

        (-wheel_thickness - e - t, -hw, z1),
        (-wheel_thickness - e, -hw, z1),

        (e + t, hw, z1),
        (e, hw, z1),

        (e + t, -hw, z1),
        (e, -hw, z1),
    ])

    edges.extend([
        (llllv, nb_verts),
        (lllrv, nb_verts + 1),

        (lrllv, nb_verts + 2),
        (lrlrv, nb_verts + 3),

        (rlllv, nb_verts + 4),
        (rllrv, nb_verts + 5),

        (rrllv, nb_verts + 6),
        (rrlrv, nb_verts + 7),
    ])

    faces.extend([
        (llllv, nb_verts, nb_verts + 1, lllrv),
        (lrllv, nb_verts + 2, nb_verts + 3, lrlrv),
        (rlllv, nb_verts + 4, nb_verts + 5, rllrv),
        (rrllv, nb_verts + 6, nb_verts + 7, rrlrv),
        (llllv, llslv, nb_verts),
        (lllrv, llsrv, nb_verts + 1),
        (lrllv, lrslv, nb_verts + 2),
        (lrlrv, lrsrv, nb_verts + 3),
        (rlllv, rlslv, nb_verts + 4),
        (rllrv, rlsrv, nb_verts + 5),
        (rrllv, rrslv, nb_verts + 6),
        (rrlrv, rrsrv, nb_verts + 7),
    ])

    nb_verts2 = len(vertices)

    for i in range(0, p + 1):
        alpha = i * (math.pi / 2) / p
        beta = math.pi / 2 + alpha

        cb = math.cos(beta)
        sb = math.sin(beta)

        sz = z + middle_bar_radius * cb

        vertices.extend([
            (-wheel_thickness - e - t, middle_bar_radius * sb, sz),
            (-wheel_thickness - e, middle_bar_radius * sb, sz),

            (-wheel_thickness - e - t, -middle_bar_radius * sb, sz),
            (-wheel_thickness - e, -middle_bar_radius * sb, sz),

            (e + t, middle_bar_radius * sb, sz),
            (e, middle_bar_radius * sb, sz),

            (e + t, -middle_bar_radius * sb, sz),
            (e, -middle_bar_radius * sb, sz),
        ])

        lllv = nb_verts2 + 8 * i
        llrv = lllv + 1
        lrlv = lllv + 2
        lrrv = lllv + 3
        rllv = lllv + 4
        rlrv = lllv + 5
        rrlv = lllv + 6
        rrrv = lllv + 7

        edges.extend([
            (lllv, llrv),
            (lrlv, lrrv),
            (rllv, rlrv),
            (rrlv, rrrv),
        ])

        if i > 0:
            faces.extend([
                (lllv - 8, lllv, llrv, llrv - 8),
                (lrlv - 8, lrlv, lrrv, lrrv - 8),
                (rllv - 8, rllv, rlrv, rlrv - 8),
                (rrlv - 8, rrlv, rrrv, rrrv - 8),

                (lllv - 8, lllv, nb_verts),
                (llrv - 8, llrv, nb_verts + 1),

                (lrlv - 8, lrlv, nb_verts + 2),
                (lrrv - 8, lrrv, nb_verts + 3),

                (rllv - 8, rllv, nb_verts + 4),
                (rlrv - 8, rlrv, nb_verts + 5),

                (rrlv - 8, rrlv, nb_verts + 6),
                (rrrv - 8, rrrv, nb_verts + 7),
            ])

    faces.extend([
        (nb_verts, nb_verts + 2, lllv),
        (nb_verts + 1, nb_verts + 3, llrv),
        (nb_verts + 4, nb_verts + 6, rllv),
        (nb_verts + 5, nb_verts + 7, rlrv),
    ])

    nb_verts3 = len(vertices)

    vertices.extend([
        (-wheel_thickness - e - t, hw, z2),
        (-wheel_thickness - e, hw, z2),

        (-wheel_thickness - e - t, -hw, z2),
        (-wheel_thickness - e, -hw, z2),

        (e + t, hw, z2),
        (e, hw, z2),

        (e + t, -hw, z2),
        (e, -hw, z2),
    ])

    edges.extend([
        (nb_verts, nb_verts3),
        (nb_verts + 1, nb_verts3 + 1),
        (nb_verts + 2, nb_verts3 + 2),
        (nb_verts + 3, nb_verts3 + 3),
        (nb_verts + 4, nb_verts3 + 4),
        (nb_verts + 5, nb_verts3 + 5),
        (nb_verts + 6, nb_verts3 + 6),
        (nb_verts + 7, nb_verts3 + 7),
        (nb_verts3, nb_verts3 + 1), (nb_verts3 + 1, nb_verts3 + 3),  (nb_verts3 + 3, nb_verts3 + 2), (nb_verts3 + 2, nb_verts3),
        (nb_verts3 + 5, nb_verts3 + 4), (nb_verts3 + 4, nb_verts3 + 6), (nb_verts3 + 6, nb_verts3 + 7), (nb_verts3 + 7, nb_verts3 + 5),
        (nb_verts3 + 1, nb_verts3 + 5),
        (nb_verts3 + 3, nb_verts3 + 7),
    ])

    faces.extend([
        (nb_verts, nb_verts3, nb_verts3 + 2, nb_verts + 2),
        (nb_verts + 1, nb_verts3 + 1, nb_verts3 + 3, nb_verts + 3),
        (nb_verts + 4, nb_verts3 + 4, nb_verts3 + 6, nb_verts + 6),
        (nb_verts + 5, nb_verts3 + 5, nb_verts3 + 7, nb_verts + 7),
        (nb_verts, nb_verts3, nb_verts3 + 1, nb_verts + 1),
        (nb_verts + 2, nb_verts3 + 2, nb_verts3 + 3, nb_verts + 3),
        (nb_verts + 4, nb_verts3 + 4, nb_verts3 + 5, nb_verts + 5),
        (nb_verts + 6, nb_verts3 + 6, nb_verts3 + 7, nb_verts + 7),
        (nb_verts3 + 1, nb_verts3 + 5, nb_verts3 + 7, nb_verts3 + 3),
    ])

    nb_verts4 = len(vertices)

    vertices.extend([
        (-wheel_thickness - e - t, hw, z3),
        (-wheel_thickness - e - t, -hw, z3),

        (e + t, hw, z3),
        (e + t, -hw, z3),

        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, 0.5 * teeth_width, z3),
        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, -0.5 * teeth_width, z3),

        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, 0.5 * teeth_width, z3),
        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, -0.5 * teeth_width, z3),

        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, 0.5 * teeth_width, z4),
        (-0.5 * wheel_thickness - 0.5 * teeth_thickness, -0.5 * teeth_width, z4),

        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, 0.5 * teeth_width, z4),
        (-0.5 * wheel_thickness + 0.5 * teeth_thickness, -0.5 * teeth_width, z4),
    ])

    edges.extend([
        (nb_verts4, nb_verts4 + 1),
        (nb_verts4 + 1, nb_verts4 + 3),
        (nb_verts4 + 3, nb_verts4 + 2),
        (nb_verts4 + 2, nb_verts4),

        (nb_verts3, nb_verts4),
        (nb_verts3 + 4, nb_verts4 + 2),
        (nb_verts3 + 6, nb_verts4 + 3),
        (nb_verts3 + 2, nb_verts4 + 1),

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
        (nb_verts3, nb_verts4, nb_verts4 + 1, nb_verts3 + 2),
        (nb_verts3 + 6, nb_verts4 + 3, nb_verts4 + 2, nb_verts3 + 4),

        (nb_verts3 + 2, nb_verts4 + 1, nb_verts4 + 3, nb_verts3 + 6),
        (nb_verts3, nb_verts4, nb_verts4 + 2, nb_verts3 + 4),

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