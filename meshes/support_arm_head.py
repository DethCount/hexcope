import bpy
import math

support_arm_head_name = 'arm_head_'

# e: margin
# t: head thickness arround arms
# h: head height
# d: distance between arms
# arm_r: arm radius
# arm_rp: arm circles precision
# spider_thickness: spider leg thickness
# spider_length: spider leg length
def create_mesh(e, t, h, arm_d, arm_r, arm_rp, spider_thickness, spider_length):
    mesh = bpy.data.meshes.new(support_arm_head_name + str((
        e, t, h,
        arm_d, arm_r, arm_rp,
        spider_thickness, spider_length
    )))

    pi4 = math.pi / 4

    hd = 0.5 * arm_d
    hst = 0.5 * spider_thickness
    hsl = 0.5 * spider_length

    ri = arm_r + e
    re = ri + t

    vertices = [
        (0, -hd + re, 0),
        (0, hd - re, 0),

        (re, -hd, 0),
        (re, hd, 0),

        (-re, hd, 0),
        (-re, -hd, 0),

        (0, -hd + re, -h),
        (0, hd - re, -h),

        # 8
        (re, -hd, -h),
        (re, hd, -h),

        (-re, hd, -h),
        (-re, -hd, -h),

        (ri * math.cos(pi4), -hd + ri * math.sin(pi4), 0),
        (ri * math.cos(pi4), hd - ri * math.sin(pi4), 0),

        (ri * math.cos(pi4), -hd + ri * math.sin(pi4), -h),
        (ri * math.cos(pi4), hd - ri * math.sin(pi4), -h),

        # 16
        (ri * math.cos(3 * pi4), -hd + ri * math.sin(3 * pi4), 0),
        (ri * math.cos(3 * pi4), hd - ri * math.sin(3 * pi4), 0),

        (ri * math.cos(3 * pi4), -hd + ri * math.sin(3 * pi4), -h),
        (ri * math.cos(3 * pi4), hd - ri * math.sin(3 * pi4), -h),

        (-re, -hst, 0),
        (-re, hst, 0),

        (-re, -hst, -h - t),
        (-re, hst, -h - t),

        # 24
        (0, -hst, -h - t),
        (0, hst, -h - t),

        (re, -hst, 0),
        (re, hst, 0),

        (re, -hst, -h),
        (re, hst, -h),

        (-re - spider_length, -hst, 0),
        (-re - spider_length, hst, 0),

        # 32
        (-re - spider_length, -hst, -h),
        (-re - spider_length, hst, -h),

        (-re - hsl, -hst, -h),
        (-re - hsl, hst, -h),
    ]

    edges = []

    faces = [
        (0, 2, 3, 1),
        (5, 0, 1, 4),

        (8, 6, 24, 28),
        (25, 7, 9, 29),
        (24, 6, 11, 22),
        (7, 25, 23, 10),
        (28, 24, 25, 29),
        (24, 22, 23, 25),

        (21, 4, 10, 23),
        (5, 20, 22, 11),

        (30, 20, 21, 31),
        (22, 34, 35, 23),
        (30, 31, 33, 32),
        (34, 32, 33, 35),
        (20, 30, 32, 28),
        (22, 28, 34),
        (31, 21, 29, 33),
        (29, 23, 35),

        (9, 3, 2, 8),

        (0, 12, 2),
        (3, 13, 1),
        (8, 14, 6),
        (7, 15, 9),

        (5, 16, 0),
        (1, 17, 4),
        (6, 18, 11),
        (10, 19, 7),
    ]

    nb_verts = len(vertices)

    for i in range(0, arm_rp + 1):
        alpha = i * math.pi / arm_rp
        beta = 0 + alpha

        cb = math.cos(beta)
        sb = math.sin(beta)

        recb = re * cb
        resb = re * sb

        ricb = ri * cb
        risb = ri * sb

        nbidx = 12

        trv = nb_verts + i * nbidx
        tlv = trv + 1
        brv = trv + 2
        blv = trv + 3

        trvi = trv + 4
        tlvi = trv + 5
        brvi = trv + 6
        blvi = trv + 7

        trvii = trv + 8
        tlvii = trv + 9
        brvii = trv + 10
        blvii = trv + 11

        vertices.extend([
            (recb, -hd - resb, 0),
            (recb, hd + resb, 0),

            (recb, -hd - resb, -h),
            (recb, hd + resb, -h),

            (ricb, -hd - risb, 0),
            (ricb, hd + risb, 0),

            (ricb, -hd - risb, -h),
            (ricb, hd + risb, -h),

            (ricb, -hd + risb, 0),
            (ricb, hd - risb, 0),

            (ricb, -hd + risb, -h),
            (ricb, hd - risb, -h),
        ])

        if i > 0:
            faces.extend([
                (trv - nbidx, trv, brv, brv - nbidx),
                (tlv, tlv - nbidx, blv - nbidx, blv),

                (trvi, trvi - nbidx, brvi - nbidx, brvi),
                (tlvi - nbidx, tlvi, blvi, blvi - nbidx),

                (trvi, trv, trv - nbidx, trvi - nbidx),
                (tlv, tlvi, tlvi - nbidx, tlv - nbidx),

                (brv, brvi, brvi - nbidx, brv - nbidx),
                (blvi, blv, blv - nbidx, blvi - nbidx),

                (trvii - nbidx, trvii, brvii, brvii - nbidx),
                (tlvii, tlvii - nbidx, blvii - nbidx, blvii),
            ])

            if alpha < pi4:
                faces.extend([
                    (trvii - nbidx, 2, trvii),
                    (tlvii - nbidx, tlvii, 3),

                    (brvii - nbidx, brvii, 8),
                    (blvii - nbidx, 9, blvii),
                ])
            elif alpha < 3 * pi4:
                faces.extend([
                    (trvii - nbidx, 0, trvii),
                    (tlvii - nbidx, tlvii, 1),

                    (brvii - nbidx, brvii, 6),
                    (blvii - nbidx, 7, blvii),
                ])
            else:
                faces.extend([
                    (trvii - nbidx, 5, trvii),
                    (tlvii - nbidx, tlvii, 4),

                    (brvii - nbidx, brvii, 11),
                    (blvii - nbidx, 10, blvii),
                ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh