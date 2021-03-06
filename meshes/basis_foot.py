import bpy
import math

basis_foot_name = 'basis_foot'

def create_mesh(
    e, t, h, w1, w2, x, y, z,
    horizontal_tooth_width, horizontal_tooth_height, horizontal_tooth_thickness,
    vertical_tooth_width, vertical_tooth_height, vertical_tooth_thickness,
    yscale,
    with_leg_connexion
):
    mesh = bpy.data.meshes.new(
        basis_foot_name
        + '_' + str((
            e, t, h, w1, w2, x, y, z,
            horizontal_tooth_width, horizontal_tooth_height, horizontal_tooth_thickness,
            vertical_tooth_width, vertical_tooth_height, vertical_tooth_thickness,
            yscale,
            with_leg_connexion
        ))
    )

    ystart = y
    if with_leg_connexion:
        ystart -= e

    ht = 0.5 * t
    hh = 0.5 * h
    hhtw = 0.5 * horizontal_tooth_width
    hhtt = 0.5 * horizontal_tooth_thickness
    hvtt = 0.5 * vertical_tooth_thickness

    pi3 = math.pi / 3
    pi6 = math.pi / 6
    cpi3 = math.cos(pi3)
    spi3 = math.sin(pi3)
    cpi6 = math.cos(pi6)
    spi6 = math.sin(pi6)

    h2 = spi3 * w2
    w4 = cpi3 * w2

    h3 = 0.5 * (w2 - vertical_tooth_width) * cpi6
    w5 = 0.5 * (w2 - vertical_tooth_width) * spi6

    p1 = (x - ht, yscale * (ystart - w1), z + hh)
    p2 = (x + ht, yscale * (ystart - w1), z + hh)

    p3 = (p1[0] - h2, p1[1] - yscale * w4, z)
    p4 = (p2[0] - h2, p2[1] - yscale * w4, z)

    p5 = (x - (ht - hvtt) - hvtt - h3, yscale * (ystart - w1 - w5), z - hh)
    p6 = (x - (ht - hvtt) + hvtt - h3, yscale * (ystart - w1 - w5), z - hh)

    p7 = (p5[0] - vertical_tooth_width * cpi6, p5[1] - yscale * vertical_tooth_width * spi6, p5[2])
    p8 = (p6[0] - vertical_tooth_width * cpi6, p6[1] - yscale * vertical_tooth_width * spi6, p6[2])

    vertices = [
        (x - ht, yscale * ystart, z + hh),
        (x + ht, yscale * ystart, z + hh),

        (x - ht, yscale * ystart, z - hh),
        (x + ht, yscale * ystart, z - hh),

        p1,
        p2,

        (p1[0], p1[1], z - hh),
        (p2[0], p2[1], z - hh),

        p3,
        p4,

        (p3[0], p3[1], z - hh),
        (p4[0], p4[1], z - hh),

        p5,
        p6,

        p7,
        p8,

        (p5[0], p5[1], p5[2] - vertical_tooth_height),
        (p6[0], p6[1], p6[2] - vertical_tooth_height),

        (p7[0], p7[1], p7[2] - vertical_tooth_height),
        (p8[0], p8[1], p8[2] - vertical_tooth_height),
    ]

    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),

        (4, 5), (5, 7), (7, 6), (6, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),

        (8, 9), (9, 11), (11, 10), (10, 8),

        (4, 8), (5, 9), (6, 10), (7, 11),

        (12, 13), (13, 15), (15, 14), (14, 12),

        (16, 17), (17, 19), (19, 18), (18, 16),
        (12, 16), (13, 17), (14, 18), (15, 19),
    ]

    faces = [
        (1, 0, 4, 5),
        (2, 3, 7, 6),
        (0, 2, 6, 4),
        (3, 1, 5, 7),

        (8, 9, 5, 4),
        (9, 11, 7, 5),
        (4, 6, 10, 8),
        (9, 8, 10, 11),

        (6, 7, 13, 12),
        (7, 11, 15, 13),
        (11, 10, 14, 15),
        (10, 6, 12, 14),

        (12, 13, 17, 16),
        (15, 14, 18, 19),
        (19, 17, 13, 15),
        (14, 12, 16, 18),

        (16, 17, 19, 18),
    ]

    if with_leg_connexion:
        nbverts = len(vertices)

        vertices.extend([
            (x - hhtt + e, yscale * (ystart + horizontal_tooth_height), z + hhtw - e),
            (x + hhtt - e, yscale * (ystart + horizontal_tooth_height), z + hhtw - e),

            (x - hhtt + e, yscale * (ystart + horizontal_tooth_height), z - hhtw + e),
            (x + hhtt - e, yscale * (ystart + horizontal_tooth_height), z - hhtw + e),

            (x - hhtt + e, yscale * ystart, z + hhtw - e),
            (x + hhtt - e, yscale * ystart, z + hhtw - e),

            (x - hhtt + e, yscale * ystart, z - hhtw + e),
            (x + hhtt - e, yscale * ystart, z - hhtw + e),
        ])

        edges.extend([
            (nbverts + 0, nbverts + 1), (nbverts + 1, nbverts + 3), (nbverts + 3, nbverts + 2), (nbverts + 2, nbverts + 0),
            (nbverts + 4, nbverts + 5), (nbverts + 5, nbverts + 7), (nbverts + 7, nbverts + 6), (nbverts + 6, nbverts + 4),
            (nbverts + 0, nbverts + 4), (nbverts + 1, nbverts + 5), (nbverts + 2, nbverts + 6), (nbverts + 3, nbverts + 7),
        ])

        faces.extend([
            (nbverts + 0, nbverts + 1, nbverts + 3, nbverts + 2),
            (nbverts + 1, nbverts + 0, nbverts + 4, nbverts + 5),
            (nbverts + 2, nbverts + 3, nbverts + 7, nbverts + 6),
            (nbverts + 0, nbverts + 2, nbverts + 6, nbverts + 4),
            (nbverts + 3, nbverts + 1, nbverts + 5, nbverts + 7),

            (0, 1, nbverts + 5, nbverts + 4),
            (3, 2, nbverts + 6, nbverts + 7),
            (2, 0, nbverts + 4, nbverts + 6),
            (1, 3, nbverts + 7, nbverts + 5),
        ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    if yscale < 0:
        mesh.flip_normals()

    return mesh