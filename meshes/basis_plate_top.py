import bpy
import math

basis_plate_top_name = 'basis_plate_top'

def create_mesh(
    e, t, r, sr, p, x, z,
    hex_side,
    large_tooth_width, large_tooth_height, large_tooth_thickness,
    small_teeth_width, small_teeth_height, small_teeth_thickness,
    leg_width,
    foot_w1, foot_w2, foot_thickness,
    basis_plate_top_stator_side,
    basis_plate_top_stator_wall_thickness,
    basis_plate_top_stator_wall_height,
):
    mesh = bpy.data.meshes.new(
        basis_plate_top_name
        + '_' + str((
            e, t, r, sr, p, x, z,
            hex_side,
            large_tooth_width, large_tooth_height, large_tooth_thickness,
            small_teeth_width, small_teeth_height, small_teeth_thickness,
            leg_width,
            foot_w1, foot_w2
        ))
    )

    hw = 0.5 * leg_width
    hltt = 0.5 * large_tooth_thickness
    hltw = 0.5 * large_tooth_width

    hstt = 0.5 * small_teeth_thickness
    hstw = 0.5 * small_teeth_width
    hft = 0.5 * foot_thickness

    hss = 0.5 * basis_plate_top_stator_side

    cx = -(math.sqrt(3) / 2) * hex_side

    pi6 = math.pi / 6
    cpi6 = math.cos(pi6)
    spi6 = math.sin(pi6)

    w3 = 0.5 * (foot_w2 - small_teeth_width - 2 * e)
    h3 = foot_w2 - w3

    nw = w3 * spi6
    fw = h3 * spi6

    ny = hw + foot_w1 + e + nw
    fy = hw + foot_w1 + e + fw

    nh = w3 * cpi6
    fh = h3 * cpi6

    rz = 0.5 * (r - sr)
    zo = 0.5 * rz
    zow = 0.5 * zo
    zop = 0.5 * zow
    zo = 0.25 * rz
    zswt = z + basis_plate_top_stator_wall_height
    zswte = zswt - basis_plate_top_stator_wall_thickness


    vertices = [
        (cx, 0, z),
        (cx, 0, z - t),

        #leg
        (x - hltt - e, hltw + e, z),
        (x + hltt + e, hltw + e, z),

        (x - hltt - e, -hltw - e, z),
        (x + hltt + e, -hltw - e, z),

        (x - hltt - e, hltw + e, z - t),
        (x + hltt + e, hltw + e, z - t),

        (x - hltt - e, -hltw - e, z - t),
        (x + hltt + e, -hltw - e, z - t),

        #right foot
        (x - (hft - hstt) - hstt - e - nh, ny, z),
        (x - (hft - hstt) + hstt + e - nh, ny, z),

        (x - (hft - hstt) - hstt - e - nh, ny, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - nh, ny, z - small_teeth_height),

        (x - (hft - hstt) - hstt - e - fh, fy, z),
        (x - (hft - hstt) + hstt + e - fh, fy, z),

        (x - (hft - hstt) - hstt - e - fh, fy, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - fh, fy, z - small_teeth_height),

        # left foot
        (x - (hft - hstt) - hstt - e - nh, -ny, z),
        (x - (hft - hstt) + hstt + e - nh, -ny, z),

        (x - (hft - hstt) - hstt - e - nh, -ny, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - nh, -ny, z - small_teeth_height),

        (x - (hft - hstt) - hstt - e - fh, -fy, z),
        (x - (hft - hstt) + hstt + e - fh, -fy, z),

        (x - (hft - hstt) - hstt - e - fh, -fy, z - small_teeth_height),
        (x - (hft - hstt) + hstt + e - fh, -fy, z - small_teeth_height),

        # stator walls
        (cx, hss, z),
        (cx + hss, hss, z),
        (cx + hss, -hss, z),
        (cx, -hss, z),
        (cx, -hss - basis_plate_top_stator_wall_thickness, z),
        (cx + hss + basis_plate_top_stator_wall_thickness, -hss - basis_plate_top_stator_wall_thickness, z),
        (cx + hss + basis_plate_top_stator_wall_thickness, hss + basis_plate_top_stator_wall_thickness, z),
        (cx, hss + basis_plate_top_stator_wall_thickness, z),

        (cx, hss, zswt),
        (cx + hss, hss, zswt),
        (cx + hss, -hss, zswt),
        (cx, -hss, zswt),
        (cx, -hss - basis_plate_top_stator_wall_thickness, zswte),
        (cx + hss + basis_plate_top_stator_wall_thickness, -hss - basis_plate_top_stator_wall_thickness, zswte),
        (cx + hss + basis_plate_top_stator_wall_thickness, hss + basis_plate_top_stator_wall_thickness, zswte),
        (cx, hss + basis_plate_top_stator_wall_thickness, zswte),
    ]
    edges = [
        (2, 3), (3, 5), (5, 4), (4, 2),
        (6, 7), (7, 9), (9, 8), (8, 6),
        (2, 6), (3, 7), (4, 8), (5, 9),

        (10, 11), (11, 13), (13, 12), (12, 10),
        (14, 15), (15, 17), (17, 16), (16, 14),
        (10, 14), (11, 15), (12, 16), (13, 17),

        (18, 19), (19, 21), (21, 20), (20, 18),
        (22, 23), (23, 25), (25, 24), (24, 22),
        (18, 22), (19, 23), (20, 24), (21, 25),

        (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, 33), (33, 26),
        (34, 35), (35, 36), (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 34),
        (26, 34), (27, 35), (28, 36), (29, 37), (30, 38), (31, 39), (32, 40), (33, 41),
    ]
    faces = [
        (3, 2, 6, 7),
        (4, 5, 9, 8),
        (2, 4, 8, 6),
        (5, 3, 7, 9),

        (10, 11, 13, 12),
        (15, 14, 16, 17),
        (13, 11, 15, 17),
        (10, 12, 16, 14),
        (12, 13, 17, 16),

        (19, 18, 20, 21),
        (22, 23, 25, 24),
        (19, 21, 25, 23),
        (20, 18, 22, 24),
        (21, 20, 24, 25),

        (2, 3, 11, 10),
        (5, 4, 18, 19),

        (26, 27, 35, 34),
        (27, 28, 36, 35),
        (28, 29, 37, 36),

        (30, 31, 39, 38),
        (31, 32, 40, 39),
        (32, 33, 41, 40),

        (26, 34, 41, 33),
        (34, 35, 40, 41),
        (35, 36, 39, 40),
        (36, 37, 38, 39),
        (38, 37, 29, 30),
    ]

    nb_verts2 = len(vertices)

    vertices.extend([
        (cx, sr + zo + e, z),
        (cx - zow + e, sr + zo + e - zop, z),
        (cx - zow + e, sr + rz - e + zo + zop, z),
        (cx, sr + rz - e + zo, z),

        (cx, -sr - zo, z),
        (cx + zow, -sr - zo + zop, z),
        (cx + zow, -sr - rz - zo - zop, z),
        (cx, -sr - rz - zo, z),

        (cx, sr + zo + e, z - t),
        (cx - zow + e, sr + zo + e - zop, z - t),
        (cx - zow + e, sr + rz - e + zo + zop, z - t),
        (cx, sr + rz - e + zo, z - t),

        (cx, -sr - zo, z - t),
        (cx + zow, -sr - zo + zop, z - t),
        (cx + zow, -sr - rz - zo - zop, z - t),
        (cx, -sr - rz - zo, z - t),
    ])

    nb_verts = len(vertices)

    i0 = None
    i1 = None
    i2 = None
    i3 = None
    i4 = None
    i5 = None
    i6 = None

    for i in range(0, p + 1):
        alpha = i * math.pi / p
        beta = -math.pi / 2 + alpha

        c = math.cos(beta)
        s = math.sin(beta)
        rc = r * c
        rs = r * s
        src = sr * c
        srs = sr * s

        vertices.extend([
            (cx + rc, rs, z),
            (cx + rc, rs, z - t),

            (cx + src, srs, z),
            (cx + src, srs, z - t),
        ])

        nbidx = 4
        tv = nb_verts + nbidx * i
        bv = tv + 1
        stv = tv + 2
        sbv = tv + 3

        if alpha >= math.pi / 6 and alpha < 5 * (math.pi / 6):
            edges.append((tv, bv))

        edges.extend([
            (stv, sbv),
        ])

        if i > 0:
            if alpha >= math.pi / 6 and alpha < 5 * (math.pi / 6):
                edges.extend([
                    (tv - nbidx, tv),
                    (bv - nbidx, bv),
                ])
                faces.extend([
                    (tv, tv - nbidx, bv - nbidx, bv),
                ])

            edges.extend([
                (stv - nbidx, stv),
                (sbv - nbidx, sbv),
            ])

            faces.extend([
                (stv - nbidx, stv, sbv, sbv - nbidx),
            ])

            if alpha < math.pi / 6:
                faces.extend([
                    (stv, stv - nbidx, nb_verts2 + 5),
                    (sbv - nbidx, sbv, 8),
                ])

                if i0 == None:
                    i0 = tv - nbidx
            elif alpha < math.pi / 3:
                faces.extend([
                    (tv - nbidx, tv, 19),
                    (stv, stv - nbidx, 18),

                    (bv, bv - nbidx, 9),
                    (sbv - nbidx, sbv, 8),
                ])

                if i1 == None:
                    i1 = tv - nbidx
            elif alpha < math.pi / 2:
                faces.extend([
                    (tv - nbidx, tv, 5),
                    (stv, stv - nbidx, 4),

                    (bv, bv - nbidx, 9),
                    (sbv - nbidx, sbv, 8),
                ])

                if i2 == None:
                    i2 = tv - nbidx
            elif alpha < 2 * math.pi / 3:
                faces.extend([
                    (tv - nbidx, tv, 3),
                    (stv, stv - nbidx, 2),

                    (bv, bv - nbidx, 7),
                    (sbv - nbidx, sbv, 6),
                ])

                if i3 == None:
                    i3 = tv - nbidx
            elif alpha < 5 * math.pi / 6:
                faces.extend([
                    (tv - nbidx, tv, 11),
                    (stv, stv - nbidx, 10),

                    (bv, bv - nbidx, 7),
                    (sbv - nbidx, sbv, 6),
                ])

                if i4 == None:
                    i4 = tv - nbidx
            else:
                faces.extend([
                    (stv, stv - nbidx, 10),
                    (sbv - nbidx, sbv, 6),
                ])

                if i5 == None:
                    i5 = tv - nbidx

            if i == p and i6 == None:
                i6 = tv


    nb_verts3 = len(vertices)

    cp6 = math.cos(math.pi / 6)
    vertices.extend([
        (cx, r * cp6, z),
        (cx, r * cp6, z - t),
        (cx, -r * cp6, z),
        (cx, -r * cp6, z - t),
    ])

    faces.extend([
        (nb_verts3 + 2, 23, 22),
        (i1, 19, 23),
        (i1 + 2, 22, 18),
        (i2, 5, 19),
        (i2 + 2, 18, 4),
        (i3, 3, 5),
        (i3 + 2, 4, 2),
        (i4, 11, 3),
        (i4 + 2, 2, 10),
        (i5, 15, 11),
        (i6 + 2, 10, 14),
        (nb_verts3, 14, 15),
        (nb_verts3, i6 + 2, 14),

        (nb_verts3 + 3, 8, 9),
        (i3 + 1, 9, 7),
        (i3 + 3, 6, 8),
        (nb_verts3 + 1, 7, 6),
        (i6 + 3, nb_verts3 + 1, 6),
    ])


    edges.extend([
        (i6 + 2, nb_verts2),
        (nb_verts2, nb_verts2 + 1),
        (nb_verts2 + 1, nb_verts2 + 2),
        (nb_verts2 + 2, nb_verts2 + 3),
        (nb_verts2 + 3, nb_verts3),

        (i0 + 2, nb_verts2 + 4),
        (nb_verts2 + 4, nb_verts2 + 5),
        (nb_verts2 + 5, nb_verts2 + 6),
        (nb_verts2 + 6, nb_verts2 + 7),
        (nb_verts2 + 7, nb_verts3 + 2),

        (i6 + 3, nb_verts2 + 8),
        (nb_verts2 + 8, nb_verts2 + 9),
        (nb_verts2 + 9, nb_verts2 + 10),
        (nb_verts2 + 10, nb_verts2 + 11),
        (nb_verts2 + 11, nb_verts3 + 1),

        (i0 + 3, nb_verts2 + 12),
        (nb_verts2 + 12, nb_verts2 + 13),
        (nb_verts2 + 13, nb_verts2 + 14),
        (nb_verts2 + 14, nb_verts2 + 15),
        (nb_verts2 + 15, nb_verts3 + 3),
    ])
    faces.extend([
        # outer left horizontal tooth
        (i6 + 2, nb_verts2, nb_verts2 + 8, i6 + 3),
        (nb_verts2, nb_verts2 + 1, nb_verts2 + 9, nb_verts2 + 8),
        (nb_verts2 + 1, nb_verts2 + 2, nb_verts2 + 10, nb_verts2 + 9),
        (nb_verts2 + 2, nb_verts2 + 3, nb_verts2 + 11, nb_verts2 + 10),
        (nb_verts2 + 3, nb_verts3, nb_verts3 + 1, nb_verts2 + 11),
        (nb_verts2 + 1, nb_verts2, nb_verts2 + 3, nb_verts2 + 2),
        (nb_verts2 + 8, nb_verts2 + 9, nb_verts2 + 10, nb_verts2 + 11),


        # inner right horizontal tooth
        (nb_verts2 + 4, i0 + 2, i0 + 3, nb_verts2 + 12),
        (nb_verts2 + 5, nb_verts2 + 4, nb_verts2 + 12, nb_verts2 + 13),
        (nb_verts2 + 6, nb_verts2 + 5, nb_verts2 + 13, nb_verts2 + 14),
        (nb_verts2 + 7, nb_verts2 + 6, nb_verts2 + 14, nb_verts2 + 15),
        (nb_verts3 + 2, nb_verts2 + 7, nb_verts2 + 15, nb_verts3 + 3),

        # top right
        (i0 + 2, nb_verts2 + 4, nb_verts2 + 5),
        (i1 + 2, nb_verts2 + 5, 22),
        (nb_verts2 + 5, nb_verts2 + 6, 22),
        (nb_verts2 + 6, nb_verts2 + 7, nb_verts3 + 2),
        (22, nb_verts2 + 6, nb_verts3 + 2),

        # bottom right
        (i0 + 3, nb_verts2 + 13, nb_verts2 + 12),
        (nb_verts3 + 3, nb_verts2 + 15, nb_verts2 + 14),
        (nb_verts2 + 14, nb_verts2 + 13, 8),
        (nb_verts3 + 3, nb_verts2 + 14, 8),
        (8, nb_verts2 + 13, i0 + 3),

        (15, i5, nb_verts3),
        (nb_verts3, i5, i5 + 1, nb_verts3 + 1),
        (i5 + 1, 7, nb_verts3 + 1),

        (i1, 23, nb_verts3 + 2),
        (i1, nb_verts3 + 2, nb_verts3 + 3, i1 + 1),
        (9, i1 + 1, nb_verts3 + 3),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh