import bpy
import math

mainboard_name = 'mainboard'
mainboard_cover_name = 'mainboard_cover'

def create_mesh(
    e, t, h, w,
    wall_thickness,
    board_width,
    board_length,
    screw_height,
    screw_p,
    screw_ri,
    screw_re,
    screw_pos_tl,
    screw_pos_tr,
    screw_pos_br,
    screw_pos_bl,
    x, y, z,
    power_pos,
    power_width,
    usb_pos,
    usb_width
):
    hw = 0.5 * w
    hpw = 0.5 * power_width
    huw = 0.5 * usb_width

    dtl = (x, y + hw + e, z + e)
    dtr = (dtl[0], dtl[1] - w - 2 * e, dtl[2])
    dbr = (dtl[0], dtl[1] - w - 2 * e, dtl[2] - h - 2 * e)
    dbl = (dtl[0], dtl[1], dtl[2] - h - 2 * e)

    utl = (dtl[0] - t, dtl[1], dtl[2])
    utr = (dtr[0] - t, dtr[1], dtr[2])
    ubr = (dbr[0] - t, dbr[1], dbr[2])
    ubl = (dbl[0] - t, dbl[1], dbl[2])

    pos_screw_tl = (dtl[0], dtl[1] - e - screw_pos_tl[0], dtl[2] - e - screw_pos_tl[1])
    pos_screw_tr = (dtl[0], dtl[1] - e - screw_pos_tr[0], dtl[2] - e - screw_pos_tr[1])
    pos_screw_br = (dtl[0], dtl[1] - e - screw_pos_br[0], dtl[2] - e - screw_pos_br[1])
    pos_screw_bl = (dtl[0], dtl[1] - e - screw_pos_bl[0], dtl[2] - e - screw_pos_bl[1])

    mesh = bpy.data.meshes.new(
        mainboard_name
        + '_' + str((
            e, t, h, w,
            wall_thickness,
            board_width,
            board_length,
            screw_height,
            screw_p,
            screw_ri,
            screw_re,
            screw_pos_tl,
            screw_pos_tr,
            screw_pos_br,
            screw_pos_bl,
            x, y, z,
            power_pos,
            power_width,
            usb_pos,
            usb_width
        ))
    )

    vertices = [
        pos_screw_tl,
        pos_screw_tr,
        pos_screw_br,
        pos_screw_bl,

        # 4
        dtl,
        (dtl[0], dtl[1] + wall_thickness, dtl[2] + wall_thickness),
        (dtr[0], dtr[1] - wall_thickness, dtr[2] + wall_thickness),
        dtr,

        # 8
        utl,
        (utl[0], utl[1] + wall_thickness, utl[2] + wall_thickness),

        #10
        (utl[0], utl[1] - e - power_pos + hpw, utl[2] + wall_thickness),
        (dtl[0] - screw_height, dtl[1] - e - power_pos + hpw, dtl[2] + wall_thickness),
        (dtl[0] - screw_height, dtl[1] - e - power_pos - hpw, dtl[2] + wall_thickness),
        (utl[0], utl[1] - e - power_pos - hpw, utl[2] + wall_thickness),

        # 14
        (utr[0], utr[1] - wall_thickness, utr[2] + wall_thickness),
        utr,

        # 16
        (utl[0], utl[1] - e - power_pos - hpw, utl[2]),
        (dtl[0] - screw_height, dtl[1] - e - power_pos - hpw, dtl[2]),
        (dtl[0] - screw_height, dtl[1] - e - power_pos + hpw, dtl[2]),
        (utl[0], utl[1] - e - power_pos + hpw, utl[2]),

        # 20
        dbl,
        (dbl[0], dbl[1] + wall_thickness, dbl[2] - wall_thickness),
        (dbr[0], dbr[1] - wall_thickness, dbr[2] - wall_thickness),
        dbr,

        # 24
        ubl,
        (ubl[0], ubl[1] + wall_thickness, ubl[2] - wall_thickness),
        (ubr[0], ubr[1] - wall_thickness, ubr[2] - wall_thickness),
        ubr,

        # 28
        (ubl[0], ubl[1] + wall_thickness, ubl[2] + e + usb_pos - huw),
        (dbl[0] - screw_height, dbl[1] + wall_thickness, dbl[2] + e + usb_pos - huw),
        (dbl[0] - screw_height, dbl[1] + wall_thickness, dbl[2] + e + usb_pos + huw),
        (ubl[0], ubl[1] + wall_thickness, ubl[2] + e + usb_pos + huw),

        # 32
        (ubl[0], ubl[1], ubl[2] + e + usb_pos - huw),
        (dbl[0] - screw_height, dbl[1], dbl[2] + e + usb_pos - huw),
        (dbl[0] - screw_height, dbl[1], dbl[2] + e + usb_pos + huw),
        (ubl[0], ubl[1], ubl[2] + e + usb_pos + huw),

        #36
        (dtl[0] - screw_height, dtl[1], dtl[2]),
        (dtl[0] - screw_height, dtl[1] + wall_thickness, dtl[2] + wall_thickness),

        # 38
        (pos_screw_tl[0], dtl[1], pos_screw_tl[2] + screw_re),
        (pos_screw_tl[0], pos_screw_tl[1] - screw_re, pos_screw_tl[2] + screw_re),
        (pos_screw_tl[0], pos_screw_tl[1] - screw_re, pos_screw_tl[2] - screw_re),
        (pos_screw_tl[0], dtl[1], pos_screw_tl[2] - screw_re),

        #42
        (pos_screw_tl[0] - screw_height, dtl[1], pos_screw_tl[2] + screw_re),
        (pos_screw_tl[0] - screw_height, pos_screw_tl[1] - screw_re, pos_screw_tl[2] + screw_re),
        (pos_screw_tl[0] - screw_height, pos_screw_tl[1] - screw_re, pos_screw_tl[2] - screw_re),
        (pos_screw_tl[0] - screw_height, dtl[1], pos_screw_tl[2] - screw_re),

        # 46
        (pos_screw_tr[0], pos_screw_tr[1] + screw_re, dtr[2]),
        (pos_screw_tr[0], dtr[1], dtr[2]),
        (pos_screw_tr[0], dtr[1], pos_screw_tr[2] - screw_re),
        (pos_screw_tr[0], pos_screw_tr[1] + screw_re, pos_screw_tr[2] - screw_re),

        #50
        (pos_screw_tr[0] - screw_height, pos_screw_tr[1] + screw_re, dtr[2]),
        (pos_screw_tr[0] - screw_height, dtr[1], dtr[2]),
        (pos_screw_tr[0] - screw_height, dtr[1], pos_screw_tr[2] - screw_re),
        (pos_screw_tr[0] - screw_height, pos_screw_tr[1] + screw_re, pos_screw_tr[2] - screw_re),

        # 54
        (pos_screw_br[0], pos_screw_br[1] + screw_re, pos_screw_br[2] + screw_re),
        (pos_screw_br[0], dbr[1], pos_screw_br[2] + screw_re),
        (pos_screw_br[0], dbr[1], dbr[2]),
        (pos_screw_br[0], pos_screw_br[1] + screw_re, dbr[2]),

        # 58
        (pos_screw_br[0] - screw_height, pos_screw_br[1] + screw_re, pos_screw_br[2] + screw_re),
        (pos_screw_br[0] - screw_height, dbr[1], pos_screw_br[2] + screw_re),
        (pos_screw_br[0] - screw_height, dbr[1], dbr[2]),
        (pos_screw_br[0] - screw_height, pos_screw_br[1] + screw_re, dbr[2]),

        # 62
        (pos_screw_bl[0], dbl[1], pos_screw_bl[2] + screw_re),
        (pos_screw_bl[0], pos_screw_bl[1] - screw_re, pos_screw_bl[2] + screw_re),
        (pos_screw_bl[0], pos_screw_bl[1] - screw_re, dbl[2]),
        (pos_screw_bl[0], dbl[1], dbl[2]),

        # 66
        (pos_screw_bl[0] - screw_height, dbl[1], pos_screw_bl[2] + screw_re),
        (pos_screw_bl[0] - screw_height, pos_screw_bl[1] - screw_re, pos_screw_bl[2] + screw_re),
        (pos_screw_bl[0] - screw_height, pos_screw_bl[1] - screw_re, dbl[2]),
        (pos_screw_bl[0] - screw_height, dbl[1], dbl[2]),
    ]

    edges = [
        (4, 5),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (8, 9), (37, 12), (12, 13), (13, 14),
        (14, 15), (15, 16), (16, 17), (17, 36),
        (6, 14), (7, 15),
        (12, 17), (13, 16),

        (20, 21), (21, 22), (22, 23), (23, 20),
        (24, 25), (25, 26), (26, 27), (27, 24),
        (20, 24), (21, 25), (22, 26), (23, 27),

        (7, 23), (15, 27),
        (6, 22), (14, 26),

        (20, 4),
        (21, 5),

        (24, 32), (32, 33), (33, 34), (34, 35), (35, 8),
        (25, 28), (28, 29), (29, 30), (30, 31), (31, 9),
        (28, 32), (29, 33), (30, 34), (31, 35),

        (36, 37),
        (4, 36), (36, 8),
        (5, 37), (37, 9),

        (38, 39), (39, 40), (40, 41), (41, 38),
        (42, 43), (43, 44), (44, 45), (45, 42),
        (38, 42), (39, 43), (40, 44), (41, 45),

        (46, 47), (47, 48), (48, 49), (49, 46),
        (50, 51), (51, 52), (52, 53), (53, 50),
        (46, 50), (47, 51), (48, 52), (49, 53),

        (54, 55), (55, 56), (56, 57), (57, 54),
        (58, 59), (59, 60), (60, 61), (61, 58),
        (54, 58), (55, 59), (56, 60), (57, 61),

        (62, 63), (63, 64), (64, 65), (65, 62),
        (66, 67), (67, 68), (68, 69), (69, 66),
        (62, 66), (63, 67), (64, 68), (65, 69),
    ]

    faces = [
        #(5, 4, 8, 9),
        # (7, 6, 14, 15),
        (16, 15, 14, 13),
        (17, 16, 13, 12),
        (36, 17, 12, 37),
        #(19, 18, 11, 10),
        #(8, 19, 10, 9),
        (8, 36, 37, 9),

        #(5, 9, 10, 11),
        (5, 37, 12, 6),
        (6, 12, 13, 14),

        (8, 4, 36, 19),
        (36, 4, 7, 17),
        (17, 7, 15, 16),

        (20, 24, 27, 23),
        (21, 22, 26, 25),
        (24, 25, 26, 27),

        (7, 23, 27, 15),
        (22, 6, 14, 26),
        (14, 15, 27, 26),

        (24, 20, 33, 32),
        (33, 20, 4, 34),
        (34, 4, 8, 35),

        (21, 25, 28, 29),
        (21, 29, 30, 5),
        (5, 30, 31, 9),

        (24, 32, 28, 25),
        (32, 33, 29, 28),
        (30, 29, 33, 34),
        (31, 30, 34, 35),
        (9, 31, 35, 8),

        (39, 38, 42, 43),
        (41, 40, 44, 45),
        (40, 39, 43, 44),
        (38, 41, 45, 42),

        (47, 46, 50, 51),
        (48, 47, 51, 52),
        (49, 48, 52, 53),
        (46, 49, 53, 50),

        (55, 54, 58, 59),
        (56, 55, 59, 60),
        (57, 56, 60, 61),
        (54, 57, 61, 58),

        (63, 62, 66, 67),
        (64, 63, 67, 68),
        (65, 64, 68, 69),
        (62, 65, 69, 66),
    ]

    nbverts = len(vertices)
    i1 = None
    i2 = None
    i3 = None
    for i in range(0, screw_p + 1):
        alpha = i * (2 * math.pi / screw_p)
        ca = math.cos(alpha)
        sa = math.sin(alpha)
        ci = screw_ri * ca
        si = screw_ri * sa

        nbidx = 8
        tl_bi = nbverts + i * nbidx
        tl_ti = tl_bi + 1
        tr_bi = tl_bi + 2
        tr_ti = tl_bi + 3
        br_bi = tl_bi + 4
        br_ti = tl_bi + 5
        bl_bi = tl_bi + 6
        bl_ti = tl_bi + 7

        vertices.extend([
            (pos_screw_tl[0], pos_screw_tl[1] + ci, pos_screw_tl[2] + si),
            (pos_screw_tl[0] - screw_height, pos_screw_tl[1] + ci, pos_screw_tl[2] + si),

            (pos_screw_tr[0], pos_screw_tr[1] + ci, pos_screw_tr[2] + si),
            (pos_screw_tr[0] - screw_height, pos_screw_tr[1] + ci, pos_screw_tr[2] + si),

            (pos_screw_br[0], pos_screw_br[1] + ci, pos_screw_br[2] + si),
            (pos_screw_br[0] - screw_height, pos_screw_br[1] + ci, pos_screw_br[2] + si),

            (pos_screw_bl[0], pos_screw_bl[1] + ci, pos_screw_bl[2] + si),
            (pos_screw_bl[0] - screw_height, pos_screw_bl[1] + ci, pos_screw_bl[2] + si),
        ])

        edges.extend([
            (tl_bi, tl_ti),
            (tr_bi, tr_ti),
            (br_bi, br_ti),
            (bl_bi, bl_ti),
        ])

        if i > 0:
            edges.extend([
                (tl_bi, tl_bi - nbidx),
                (tl_ti, tl_ti - nbidx),

                (tr_bi, tr_bi - nbidx),
                (tr_ti, tr_ti - nbidx),

                (br_bi, br_bi - nbidx),
                (br_ti, br_ti - nbidx),

                (bl_bi, bl_bi - nbidx),
                (bl_ti, bl_ti - nbidx),
            ])

            faces.extend([
                (tl_bi - nbidx, tl_bi, tl_ti, tl_ti - nbidx),
                (tl_bi, tl_bi - nbidx, 0),

                (tr_bi - nbidx, tr_bi, tr_ti, tr_ti - nbidx),
                (tr_bi, tr_bi - nbidx, 1),

                (br_bi - nbidx, br_bi, br_ti, br_ti - nbidx),
                (br_bi, br_bi - nbidx, 2),

                (bl_bi - nbidx, bl_bi, bl_ti, bl_ti - nbidx),
                (bl_bi, bl_bi - nbidx, 3),
            ])

            if alpha > 1.5 * math.pi:
                if i3 is None:
                    i3 = tl_bi
                faces.extend([
                    (tl_ti - nbidx, tl_ti, 45),
                    (tr_ti - nbidx, tr_ti, 53),
                    (br_ti - nbidx, br_ti, 61),
                    (bl_ti - nbidx, bl_ti, 69),
                ])
            elif alpha > math.pi:
                if i2 is None:
                    i2 = tl_bi
                faces.extend([
                    (tl_ti - nbidx, tl_ti, 44),
                    (tr_ti - nbidx, tr_ti, 52),
                    (br_ti - nbidx, br_ti, 60),
                    (bl_ti - nbidx, bl_ti, 68),
                ])
            elif alpha > 0.5 * math.pi:
                if i1 is None:
                    i1 = tl_bi
                faces.extend([
                    (tl_ti - nbidx, tl_ti, 43),
                    (tr_ti - nbidx, tr_ti, 51),
                    (br_ti - nbidx, br_ti, 59),
                    (bl_ti - nbidx, bl_ti, 67),
                ])
            else:
                faces.extend([
                    (tl_ti - nbidx, tl_ti, 42),
                    (tr_ti - nbidx, tr_ti, 50),
                    (br_ti - nbidx, br_ti, 58),
                    (bl_ti - nbidx, bl_ti, 66),
                ])

    faces.extend([
        (42, i1 + 1, 43),
        (43, i2 + 1, 44),
        (44, i3 + 1, 45),
        (45, nbverts + 1, 42),

        (50, i1 + 3, 51),
        (51, i2 + 3, 52),
        (52, i3 + 3, 53),
        (53, nbverts + 3, 50),

        (58, i1 + 5, 59),
        (59, i2 + 5, 60),
        (60, i3 + 5, 61),
        (61, nbverts + 5, 58),

        (66, i1 + 7, 67),
        (67, i2 + 7, 68),
        (68, i3 + 7, 69),
        (69, nbverts + 7, 66),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

def create_cover_mesh(
    mainboard_e,
    t, h, w,
    mainboard_wall_thickness,
    board_width,
    board_length,
    screw_height,
    screw_p,
    screw_ri,
    screw_re,
    screw_pos_tl,
    screw_pos_tr,
    screw_pos_br,
    screw_pos_bl,
    power_pos,
    power_width,
    usb_pos,
    usb_width,
    wall_thickness,
    e,
    x, y, z,
    screw_height2,
    motor_width,
    motor_height,
    motor1_pos,
    motor2_pos,
    motor3_pos,
    motor4_pos,
    spi_width,
    spi_height,
    spi_pos,
):
    hw = 0.5 * w

    x -= 0.001 # mainboard pcb thickness

    dtl = (x - screw_height - screw_height2, y + hw + e, z + e)
    dtr = (dtl[0], dtl[1] - w - 2 * e, dtl[2])
    dbr = (dtl[0], dtl[1] - w - 2 * e, dtl[2] - h - 2 * e)
    dbl = (dtl[0], dtl[1], dtl[2] - h - 2 * e)

    utl = (dtl[0] - wall_thickness, dtl[1], dtl[2])
    utr = (dtr[0] - wall_thickness, dtr[1], dtr[2])
    ubr = (dbr[0] - wall_thickness, dbr[1], dbr[2])
    ubl = (dbl[0] - wall_thickness, dbl[1], dbl[2])

    pos_screw_mtl = (dtl[0], dtl[1] - screw_pos_tl[0] - e, dtl[2] - screw_pos_tl[1] - e)
    pos_screw_mtr = (dtl[0], dtl[1] - screw_pos_tr[0] - e, dtl[2] - screw_pos_tr[1] - e)
    pos_screw_mbr = (dtl[0], dtl[1] - screw_pos_br[0] - e, dtl[2] - screw_pos_br[1] - e)
    pos_screw_mbl = (dtl[0], dtl[1] - screw_pos_bl[0] - e, dtl[2] - screw_pos_bl[1] - e)

    pos_screw_dtl = (pos_screw_mtl[0] + screw_height2, pos_screw_mtl[1], pos_screw_mtl[2])
    pos_screw_dtr = (pos_screw_mtr[0] + screw_height2, pos_screw_mtr[1], pos_screw_mtr[2])
    pos_screw_dbr = (pos_screw_mbr[0] + screw_height2, pos_screw_mbr[1], pos_screw_mbr[2])
    pos_screw_dbl = (pos_screw_mbl[0] + screw_height2, pos_screw_mbl[1], pos_screw_mbl[2])

    pos_screw_utl = (pos_screw_mtl[0] - wall_thickness, pos_screw_mtl[1], pos_screw_mtl[2])
    pos_screw_utr = (pos_screw_mtr[0] - wall_thickness, pos_screw_mtr[1], pos_screw_mtr[2])
    pos_screw_ubr = (pos_screw_mbr[0] - wall_thickness, pos_screw_mbr[1], pos_screw_mbr[2])
    pos_screw_ubl = (pos_screw_mbl[0] - wall_thickness, pos_screw_mbl[1], pos_screw_mbl[2])

    pos_screw_mtl_box_tl = (pos_screw_mtl[0], pos_screw_mtl[1] + screw_re, pos_screw_mtl[2] + screw_re)
    pos_screw_mtl_box_tr = (pos_screw_mtl[0], pos_screw_mtl[1] - screw_re, pos_screw_mtl[2] + screw_re)
    pos_screw_mtl_box_br = (pos_screw_mtl[0], pos_screw_mtl[1] - screw_re, pos_screw_mtl[2] - screw_re)
    pos_screw_mtl_box_bl = (pos_screw_mtl[0], pos_screw_mtl[1] + screw_re, pos_screw_mtl[2] - screw_re)

    pos_screw_mtr_box_tl = (pos_screw_mtr[0], pos_screw_mtr[1] + screw_re, pos_screw_mtr[2] + screw_re)
    pos_screw_mtr_box_tr = (pos_screw_mtr[0], pos_screw_mtr[1] - screw_re, pos_screw_mtr[2] + screw_re)
    pos_screw_mtr_box_br = (pos_screw_mtr[0], pos_screw_mtr[1] - screw_re, pos_screw_mtr[2] - screw_re)
    pos_screw_mtr_box_bl = (pos_screw_mtr[0], pos_screw_mtr[1] + screw_re, pos_screw_mtr[2] - screw_re)

    pos_screw_mbr_box_tl = (pos_screw_mbr[0], pos_screw_mbr[1] + screw_re, pos_screw_mbr[2] + screw_re)
    pos_screw_mbr_box_tr = (pos_screw_mbr[0], pos_screw_mbr[1] - screw_re, pos_screw_mbr[2] + screw_re)
    pos_screw_mbr_box_br = (pos_screw_mbr[0], pos_screw_mbr[1] - screw_re, pos_screw_mbr[2] - screw_re)
    pos_screw_mbr_box_bl = (pos_screw_mbr[0], pos_screw_mbr[1] + screw_re, pos_screw_mbr[2] - screw_re)

    pos_screw_mbl_box_tl = (pos_screw_mbl[0], pos_screw_mbl[1] + screw_re, pos_screw_mbl[2] + screw_re)
    pos_screw_mbl_box_tr = (pos_screw_mbl[0], pos_screw_mbl[1] - screw_re, pos_screw_mbl[2] + screw_re)
    pos_screw_mbl_box_br = (pos_screw_mbl[0], pos_screw_mbl[1] - screw_re, pos_screw_mbl[2] - screw_re)
    pos_screw_mbl_box_bl = (pos_screw_mbl[0], pos_screw_mbl[1] + screw_re, pos_screw_mbl[2] - screw_re)

    pos_screw_utl_box_tl = (pos_screw_utl[0], pos_screw_utl[1] + screw_ri, pos_screw_utl[2] + screw_ri)
    pos_screw_utl_box_tr = (pos_screw_utl[0], pos_screw_utl[1] - screw_ri, pos_screw_utl[2] + screw_ri)
    pos_screw_utl_box_br = (pos_screw_utl[0], pos_screw_utl[1] - screw_ri, pos_screw_utl[2] - screw_ri)
    pos_screw_utl_box_bl = (pos_screw_utl[0], pos_screw_utl[1] + screw_ri, pos_screw_utl[2] - screw_ri)

    pos_screw_utr_box_tl = (pos_screw_utr[0], pos_screw_utr[1] + screw_ri, pos_screw_utr[2] + screw_ri)
    pos_screw_utr_box_tr = (pos_screw_utr[0], pos_screw_utr[1] - screw_ri, pos_screw_utr[2] + screw_ri)
    pos_screw_utr_box_br = (pos_screw_utr[0], pos_screw_utr[1] - screw_ri, pos_screw_utr[2] - screw_ri)
    pos_screw_utr_box_bl = (pos_screw_utr[0], pos_screw_utr[1] + screw_ri, pos_screw_utr[2] - screw_ri)

    pos_screw_ubr_box_tl = (pos_screw_ubr[0], pos_screw_ubr[1] + screw_ri, pos_screw_ubr[2] + screw_ri)
    pos_screw_ubr_box_tr = (pos_screw_ubr[0], pos_screw_ubr[1] - screw_ri, pos_screw_ubr[2] + screw_ri)
    pos_screw_ubr_box_br = (pos_screw_ubr[0], pos_screw_ubr[1] - screw_ri, pos_screw_ubr[2] - screw_ri)
    pos_screw_ubr_box_bl = (pos_screw_ubr[0], pos_screw_ubr[1] + screw_ri, pos_screw_ubr[2] - screw_ri)

    pos_screw_ubl_box_tl = (pos_screw_ubl[0], pos_screw_ubl[1] + screw_ri, pos_screw_ubl[2] + screw_ri)
    pos_screw_ubl_box_tr = (pos_screw_ubl[0], pos_screw_ubl[1] - screw_ri, pos_screw_ubl[2] + screw_ri)
    pos_screw_ubl_box_br = (pos_screw_ubl[0], pos_screw_ubl[1] - screw_ri, pos_screw_ubl[2] - screw_ri)
    pos_screw_ubl_box_bl = (pos_screw_ubl[0], pos_screw_ubl[1] + screw_ri, pos_screw_ubl[2] - screw_ri)

    mesh = bpy.data.meshes.new(
        mainboard_cover_name
        + '_' + str((
            e, t, h, w,
            wall_thickness,
            board_width,
            board_length,
            screw_height,
            screw_p,
            screw_ri,
            screw_re,
            screw_pos_tl,
            screw_pos_tr,
            screw_pos_br,
            screw_pos_bl,
            power_pos,
            power_width,
            usb_pos,
            usb_width,
            x, y, z,
            screw_height2,
            motor_width,
            motor_height,
            motor1_pos,
            motor2_pos,
            motor3_pos,
            motor4_pos,
            spi_width,
            spi_height,
            spi_pos,
        ))
    )

    vertices = [
        dtl,
        dtr,
        dbr,
        dbl,

        #4
        utl,
        utr,
        ubr,
        ubl,

        #8
        (dtl[0], dtl[1] - motor1_pos[0] - e, dtl[2] - motor1_pos[1] - e),
        (dtl[0], dtl[1] - motor1_pos[0] - e - motor_width, dtl[2] - motor1_pos[1] - e),
        (dtl[0], dtl[1] - motor1_pos[0] - e - motor_width, dtl[2] - motor1_pos[1] - motor_height - e),
        (dtl[0], dtl[1] - motor1_pos[0] - e, dtl[2] - motor1_pos[1] - motor_height - e),

        #12
        (utl[0], utl[1] - motor1_pos[0] - e, utl[2] - motor1_pos[1] - e),
        (utl[0], utl[1] - motor1_pos[0] - e - motor_width, utl[2] - motor1_pos[1] - e),
        (utl[0], utl[1] - motor1_pos[0] - e - motor_width, utl[2] - motor1_pos[1] - motor_height - e),
        (utl[0], utl[1] - motor1_pos[0] - e, utl[2] - motor1_pos[1] - motor_height - e),

        #16
        (dtl[0], dtl[1] - motor2_pos[0] - e, dtl[2] - motor2_pos[1] - e),
        (dtl[0], dtl[1] - motor2_pos[0] - e - motor_width, dtl[2] - motor2_pos[1] - e),
        (dtl[0], dtl[1] - motor2_pos[0] - e - motor_width, dtl[2] - motor2_pos[1] - motor_height - e),
        (dtl[0], dtl[1] - motor2_pos[0] - e, dtl[2] - motor2_pos[1] - motor_height - e),

        #20
        (utl[0], utl[1] - motor2_pos[0] - e, utl[2] - motor2_pos[1] - e),
        (utl[0], utl[1] - motor2_pos[0] - e - motor_width, utl[2] - motor2_pos[1] - e),
        (utl[0], utl[1] - motor2_pos[0] - e - motor_width, utl[2] - motor2_pos[1] - motor_height - e),
        (utl[0], utl[1] - motor2_pos[0] - e, utl[2] - motor2_pos[1] - motor_height - e),

        #24
        (dtl[0], dtl[1] - motor3_pos[0] - e, dtl[2] - motor3_pos[1] - e),
        (dtl[0], dtl[1] - motor3_pos[0] - e - motor_width, dtl[2] - motor3_pos[1] - e),
        (dtl[0], dtl[1] - motor3_pos[0] - e - motor_width, dtl[2] - motor3_pos[1] - motor_height - e),
        (dtl[0], dtl[1] - motor3_pos[0] - e, dtl[2] - motor3_pos[1] - motor_height - e),

        #28
        (utl[0], utl[1] - motor3_pos[0] - e, utl[2] - motor3_pos[1] - e),
        (utl[0], utl[1] - motor3_pos[0] - e - motor_width, utl[2] - motor3_pos[1] - e),
        (utl[0], utl[1] - motor3_pos[0] - e - motor_width, utl[2] - motor3_pos[1] - motor_height - e),
        (utl[0], utl[1] - motor3_pos[0] - e, utl[2] - motor3_pos[1] - motor_height - e),

        #32
        (dtl[0], dtl[1] - motor4_pos[0] - e, dtl[2] - motor4_pos[1] - e),
        (dtl[0], dtl[1] - motor4_pos[0] - e - motor_width, dtl[2] - motor4_pos[1] - e),
        (dtl[0], dtl[1] - motor4_pos[0] - e - motor_width, dtl[2] - motor4_pos[1] - motor_height - e),
        (dtl[0], dtl[1] - motor4_pos[0] - e, dtl[2] - motor4_pos[1] - motor_height - e),

        #36
        (utl[0], utl[1] - motor4_pos[0] - e, utl[2] - motor4_pos[1] - e),
        (utl[0], utl[1] - motor4_pos[0] - e - motor_width, utl[2] - motor4_pos[1] - e),
        (utl[0], utl[1] - motor4_pos[0] - e - motor_width, utl[2] - motor4_pos[1] - motor_height - e),
        (utl[0], utl[1] - motor4_pos[0] - e, utl[2] - motor4_pos[1] - motor_height - e),

        #40
        (dtl[0], dtl[1] - spi_pos[0] - e, dtl[2] - spi_pos[1] - e),
        (dtl[0], dtl[1] - spi_pos[0] - e - spi_width, dtl[2] - spi_pos[1] - e),
        (dtl[0], dtl[1] - spi_pos[0] - e - spi_width, dtl[2] - spi_pos[1] - spi_height - e),
        (dtl[0], dtl[1] - spi_pos[0] - e, dtl[2] - spi_pos[1] - spi_height - e),

        #44
        (utl[0], utl[1] - spi_pos[0] - e, utl[2] - spi_pos[1] - e),
        (utl[0], utl[1] - spi_pos[0] - e - spi_width, utl[2] - spi_pos[1] - e),
        (utl[0], utl[1] - spi_pos[0] - e - spi_width, utl[2] - spi_pos[1] - spi_height - e),
        (utl[0], utl[1] - spi_pos[0] - e, utl[2] - spi_pos[1] - spi_height - e),

        #48
        pos_screw_mtl_box_tl,
        pos_screw_mtl_box_tr,
        pos_screw_mtl_box_br,
        pos_screw_mtl_box_bl,

        #52
        pos_screw_mtr_box_tl,
        pos_screw_mtr_box_tr,
        pos_screw_mtr_box_br,
        pos_screw_mtr_box_bl,

        #56
        pos_screw_mbr_box_tl,
        pos_screw_mbr_box_tr,
        pos_screw_mbr_box_br,
        pos_screw_mbr_box_bl,

        #60
        pos_screw_mbl_box_tl,
        pos_screw_mbl_box_tr,
        pos_screw_mbl_box_br,
        pos_screw_mbl_box_bl,

        #64
        pos_screw_utl_box_tl,
        pos_screw_utl_box_tr,
        pos_screw_utl_box_br,
        pos_screw_utl_box_bl,

        # 68
        pos_screw_utr_box_tl,
        pos_screw_utr_box_tr,
        pos_screw_utr_box_br,
        pos_screw_utr_box_bl,

        # 72
        pos_screw_ubr_box_tl,
        pos_screw_ubr_box_tr,
        pos_screw_ubr_box_br,
        pos_screw_ubr_box_bl,

        # 76
        pos_screw_ubl_box_tl,
        pos_screw_ubl_box_tr,
        pos_screw_ubl_box_br,
        pos_screw_ubl_box_bl,
    ]

    edges = [
        (0, 1),
        # contours
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),

        # motor 1
        (8, 9), (9, 10), (10, 11), (11, 8),
        (12, 13), (13, 14), (14, 15), (15, 12),
        (8, 12), (9, 13), (10, 14), (11, 15),

        # motor 2
        (16, 17), (17, 18), (18, 19), (19, 16),
        (20, 21), (21, 22), (22, 23), (23, 20),
        (16, 20), (17, 21), (18, 22), (19, 23),

        # motor 3
        (24, 25), (25, 26), (26, 27), (27, 24),
        (28, 29), (29, 30), (30, 31), (31, 28),
        (24, 28), (25, 29), (26, 30), (27, 31),

        # motor 4
        (32, 33), (33, 34), (34, 35), (35, 32),
        (36, 37), (37, 38), (38, 39), (39, 36),
        (32, 36), (33, 37), (34, 38), (35, 39),

        # spi
        (40, 41), (41, 42), (42, 43), (43, 40),
        (44, 45), (45, 46), (46, 47), (47, 44),
        (40, 44), (41, 45), (42, 46), (43, 47),

        # screw_mtl_box
        (48, 49), (49, 50), (50, 51), (51, 48),
        # screw_mtr_box
        (52, 53), (53, 54), (54, 55), (55, 52),
        # screw_mbr_box
        (56, 57), (57, 58), (58, 59), (59, 56),
        # screw_mbl_box
        (60, 61), (61, 62), (62, 63), (63, 60),

        # screw_utl_box
        (64, 65), (65, 66), (66, 67), (67, 64),
        # screw_utr_box
        (68, 69), (69, 70), (70, 71), (71, 68),
        # screw_ubr_box
        (72, 73), (73, 74), (74, 75), (75, 72),
        # screw_ubl_box
        (76, 77), (77, 78), (78, 79), (79, 76),
    ]

    faces = [
        # contours
        (1, 0, 4, 5),
        (2, 1, 5, 6),
        (3, 2, 6, 7),
        (0, 3, 7, 4),

        # motor 1
        (8, 9, 13, 12),
        (9, 10, 14, 13),
        (10, 11, 15, 14),
        (11, 8, 12, 15),

        # motor 2
        (16, 17, 21, 20),
        (17, 18, 22, 21),
        (18, 19, 23, 22),
        (19, 16, 20, 23),

        # motor 3
        (24, 25, 29, 28),
        (25, 26, 30, 29),
        (26, 27, 31, 30),
        (27, 24, 28, 31),

        # motor 4
        (32, 33, 37, 36),
        (33, 34, 38, 37),
        (34, 35, 39, 38),
        (35, 32, 36, 39),

        # spi
        (40, 41, 45, 44),
        (41, 42, 46, 45),
        (42, 43, 47, 46),
        (43, 40, 44, 47),

        # fill inner faces
        (0, 48, 51),
        (0, 49, 48),
        (0, 52, 49),
        (0, 53, 52),
        (0, 1, 53),
        (50, 49, 52, 55),
        (1, 54, 53),
        (50, 55, 8),
        (8, 55, 54, 9),
        (1, 9, 54),
        (8, 11, 50),
        (1, 10, 9),
        (11, 16, 50),
        (16, 11, 10, 17),
        (1, 17, 10),
        (16, 19, 50),
        (1, 18, 17),
        (24, 19, 18, 25),
        (18, 1, 2, 25),
        (41, 50, 19, 24),
        (51, 50, 41, 40),
        (24, 27, 41),
        (2, 26, 25),
        (27, 32, 41),
        (32, 27, 26, 33),
        (2, 33, 26),
        (42, 41, 32, 35),
        (34, 33, 2, 57),
        (35, 56, 42),
        (56, 35, 34, 57),
        (2, 58, 57),
        (2, 59, 58),
        (42, 56, 59),
        (2, 42, 59),
        (2, 43, 42),
        (2, 62, 43),
        (3, 63, 62, 2),
        (62, 61, 40, 43),
        (3, 60, 63),
        (61, 60, 40),
        (60, 51, 40),
        (3, 0, 51, 60),

        # fill outer faces
        (4, 67, 64),
        (4, 64, 65),
        (4, 65, 68),
        (4, 68, 69),
        (4, 69, 5),
        (65, 66, 71, 68),
        (5, 69, 70),
        (71, 66, 12),
        (71, 12, 13, 70),
        (5, 70, 13),
        (12, 66, 15),
        (5, 13, 14),
        (15, 66, 20),
        (15, 20, 21, 14),
        (5, 14, 21),
        (20, 66, 23),
        (5, 21, 22),
        (23, 28, 29, 22),
        (5, 22, 29, 6),
        (66, 45, 28, 23),
        (66, 67, 44, 45),
        (28, 45, 31),
        (6, 29, 30),
        (31, 45, 36),
        (31, 36, 37, 30),
        (6, 30, 37),
        (45, 46, 39, 36),
        (37, 38, 73, 6),
        (39, 46, 72),
        (39, 72, 73, 38),
        (6, 73, 74),
        (6, 74, 75),
        (46, 75, 72),
        (6, 75, 46),
        (6, 46, 47),
        (6, 47, 78),
        (79, 7, 6, 78),
        (77, 78, 47, 44),
        (7, 79, 76),
        (76, 77, 44),
        (76, 44, 67),
        (4, 7, 76, 67),
    ]

    nbverts = len(vertices)

    i1 = None
    i2 = None
    i3 = None

    for i in range(0, screw_p + 1):
        alpha = i * (2 * math.pi / screw_p)
        ca = math.cos(alpha)
        sa = math.sin(alpha)
        ci = screw_ri * ca
        si = screw_ri * sa
        ce = screw_re * ca
        se = screw_re * sa

        nbidx = 16

        tl_bi = nbverts + i * nbidx
        tl_be = tl_bi + 1
        tl_me = tl_bi + 2
        tl_ti = tl_bi + 3
        tr_bi = tl_bi + 4
        tr_be = tl_bi + 5
        tr_me = tl_bi + 6
        tr_ti = tl_bi + 7
        br_bi = tl_bi + 8
        br_be = tl_bi + 9
        br_me = tl_bi + 10
        br_ti = tl_bi + 11
        bl_bi = tl_bi + 12
        bl_be = tl_bi + 13
        bl_me = tl_bi + 14
        bl_ti = tl_bi + 15

        vertices.extend([
            (pos_screw_dtl[0], pos_screw_dtl[1] + ci, pos_screw_dtl[2] + si),
            (pos_screw_dtl[0], pos_screw_dtl[1] + ce, pos_screw_dtl[2] + se),
            (pos_screw_mtl[0], pos_screw_mtl[1] + ce, pos_screw_mtl[2] + se),
            (pos_screw_utl[0], pos_screw_utl[1] + ci, pos_screw_utl[2] + si),

            (pos_screw_dtr[0], pos_screw_dtr[1] + ci, pos_screw_dtr[2] + si),
            (pos_screw_dtr[0], pos_screw_dtr[1] + ce, pos_screw_dtr[2] + se),
            (pos_screw_mtr[0], pos_screw_mtr[1] + ce, pos_screw_mtr[2] + se),
            (pos_screw_utr[0], pos_screw_utr[1] + ci, pos_screw_utr[2] + si),

            (pos_screw_dbr[0], pos_screw_dbr[1] + ci, pos_screw_dbr[2] + si),
            (pos_screw_dbr[0], pos_screw_dbr[1] + ce, pos_screw_dbr[2] + se),
            (pos_screw_mbr[0], pos_screw_mbr[1] + ce, pos_screw_mbr[2] + se),
            (pos_screw_ubr[0], pos_screw_ubr[1] + ci, pos_screw_ubr[2] + si),

            (pos_screw_dbl[0], pos_screw_dbl[1] + ci, pos_screw_dbl[2] + si),
            (pos_screw_dbl[0], pos_screw_dbl[1] + ce, pos_screw_dbl[2] + se),
            (pos_screw_mbl[0], pos_screw_mbl[1] + ce, pos_screw_mbl[2] + se),
            (pos_screw_ubl[0], pos_screw_ubl[1] + ci, pos_screw_ubl[2] + si),
        ])

        edges.extend([
            (tl_bi, tl_ti),
            (tl_be, tl_me),

            (tr_bi, tr_ti),
            (tr_be, tr_me),

            (br_bi, br_ti),
            (br_be, br_me),

            (bl_bi, bl_ti),
            (bl_be, bl_me),
        ])

        if i > 0:
            edges.extend([
                (tl_bi, tl_bi - nbidx),
                (tl_be, tl_be - nbidx),
                (tl_me, tl_me - nbidx),
                (tl_ti, tl_ti - nbidx),

                (tr_bi, tr_bi - nbidx),
                (tr_be, tr_be - nbidx),
                (tr_me, tr_me - nbidx),
                (tr_ti, tr_ti - nbidx),

                (br_bi, br_bi - nbidx),
                (br_be, br_be - nbidx),
                (br_me, br_me - nbidx),
                (br_ti, br_ti - nbidx),

                (bl_bi, bl_bi - nbidx),
                (bl_be, bl_be - nbidx),
                (bl_me, bl_me - nbidx),
                (bl_ti, bl_ti - nbidx),
            ])

            faces.extend([
                (tl_be, tl_be - nbidx, tl_me - nbidx, tl_me),
                (tl_be - nbidx, tl_be, tl_bi, tl_bi - nbidx),
                (tl_bi - nbidx, tl_bi, tl_ti, tl_ti - nbidx),

                (tr_be, tr_be - nbidx, tr_me - nbidx, tr_me),
                (tr_be - nbidx, tr_be, tr_bi, tr_bi - nbidx),
                (tr_bi - nbidx, tr_bi, tr_ti, tr_ti - nbidx),

                (br_be, br_be - nbidx, br_me - nbidx, br_me),
                (br_be - nbidx, br_be, br_bi, br_bi - nbidx),
                (br_bi - nbidx, br_bi, br_ti, br_ti - nbidx),

                (bl_be, bl_be - nbidx, bl_me - nbidx, bl_me),
                (bl_be - nbidx, bl_be, bl_bi, bl_bi - nbidx),
                (bl_bi - nbidx, bl_bi, bl_ti, bl_ti - nbidx),
            ])

            if alpha > 1.5 * math.pi:
                if i3 is None:
                    i3 = i

                faces.extend([
                    (tl_me, tl_me - nbidx, 51),
                    (tr_me, tr_me - nbidx, 55),
                    (br_me, br_me - nbidx, 59),
                    (bl_me, bl_me - nbidx, 63),

                    (tl_ti - nbidx, tl_ti, 67),
                    (tr_ti - nbidx, tr_ti, 71),
                    (br_ti - nbidx, br_ti, 75),
                    (bl_ti - nbidx, bl_ti, 79),
                ])
            elif alpha > math.pi:
                if i2 is None:
                    i2 = i

                faces.extend([
                    (tl_me, tl_me - nbidx, 50),
                    (tr_me, tr_me - nbidx, 54),
                    (br_me, br_me - nbidx, 58),
                    (bl_me, bl_me - nbidx, 62),

                    (tl_ti - nbidx, tl_ti, 66),
                    (tr_ti - nbidx, tr_ti, 70),
                    (br_ti - nbidx, br_ti, 74),
                    (bl_ti - nbidx, bl_ti, 78),
                ])
            elif alpha > 0.5 * math.pi:
                if i1 is None:
                    i1 = i

                faces.extend([
                    (tl_me, tl_me - nbidx, 49),
                    (tr_me, tr_me - nbidx, 53),
                    (br_me, br_me - nbidx, 57),
                    (bl_me, bl_me - nbidx, 61),

                    (tl_ti - nbidx, tl_ti, 65),
                    (tr_ti - nbidx, tr_ti, 69),
                    (br_ti - nbidx, br_ti, 73),
                    (bl_ti - nbidx, bl_ti, 77),
                ])
            else:
                faces.extend([
                    (tl_me, tl_me - nbidx, 48),
                    (tr_me, tr_me - nbidx, 52),
                    (br_me, br_me - nbidx, 56),
                    (bl_me, bl_me - nbidx, 60),

                    (tl_ti - nbidx, tl_ti, 64),
                    (tr_ti - nbidx, tr_ti, 68),
                    (br_ti - nbidx, br_ti, 72),
                    (bl_ti - nbidx, bl_ti, 76),
                ])

    faces.extend([
        (51, nbverts + 2, 48),
        (48, nbverts + (i1 - 1) * nbidx + 2, 49),
        (49, nbverts + (i2 - 1) * nbidx + 2, 50),
        (50, nbverts + (i3 - 1) * nbidx + 2, 51),

        (55, nbverts + 6, 52),
        (52, nbverts + (i1 - 1) * nbidx + 6, 53),
        (53, nbverts + (i2 - 1) * nbidx + 6, 54),
        (54, nbverts + (i3 - 1) * nbidx + 6, 55),

        (59, nbverts + 10, 56),
        (56, nbverts + (i1 - 1) * nbidx + 10, 57),
        (57, nbverts + (i2 - 1) * nbidx + 10, 58),
        (58, nbverts + (i3 - 1) * nbidx + 10, 59),

        (63, nbverts + 14, 60),
        (60, nbverts + (i1 - 1) * nbidx + 14, 61),
        (61, nbverts + (i2 - 1) * nbidx + 14, 62),
        (62, nbverts + (i3 - 1) * nbidx + 14, 63),

        (67, nbverts + 3, 64),
        (64, nbverts + (i1 - 1) * nbidx + 3, 65),
        (65, nbverts + (i2 - 1) * nbidx + 3, 66),
        (66, nbverts + (i3 - 1) * nbidx + 3, 67),

        (71, nbverts + 7, 68),
        (68, nbverts + (i1 - 1) * nbidx + 7, 69),
        (69, nbverts + (i2 - 1) * nbidx + 7, 70),
        (70, nbverts + (i3 - 1) * nbidx + 7, 71),

        (75, nbverts + 11, 72),
        (72, nbverts + (i1 - 1) * nbidx + 11, 73),
        (73, nbverts + (i2 - 1) * nbidx + 11, 74),
        (74, nbverts + (i3 - 1) * nbidx + 11, 75),

        (79, nbverts + 15, 76),
        (76, nbverts + (i1 - 1) * nbidx + 15, 77),
        (77, nbverts + (i2 - 1) * nbidx + 15, 78),
        (78, nbverts + (i3 - 1) * nbidx + 15, 79),
    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh