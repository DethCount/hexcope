import bpy
import math

basis_leg_name = 'basis_leg'

def create_mesh(
    e, t, h, w, x, z,
    teeth_width, teeth_height, teeth_thickness,
    side_teeth_width, side_teeth_height, side_teeth_thickness, side_teeth_z
):
    mesh = bpy.data.meshes.new(
        basis_leg_name
        + '_' + str((
            e, t, h, w, x, z,
            teeth_width, teeth_height, teeth_thickness,
            side_teeth_width, side_teeth_height, side_teeth_thickness, side_teeth_z
        ))
    )

    hw = 0.5 * w
    ht = 0.5 * t
    htt = 0.5 * teeth_thickness
    htw = 0.5 * teeth_width
    hstt = 0.5 * side_teeth_thickness
    hstw = 0.5 * side_teeth_width

    sth = z - e - h + teeth_height + side_teeth_z # total side teeth z

    vertices = [
        (x - ht, hw, z + teeth_height - e),
        (x - ht, -hw, z + teeth_height - e),
        (x + ht, hw, z + teeth_height - e),
        (x + ht, -hw, z + teeth_height - e),

        (x - htt - e, htw + e, z + teeth_height - e),
        (x - htt - e, -htw - e, z + teeth_height - e),
        (x + htt + e, htw + e, z + teeth_height - e),
        (x + htt + e, -htw - e, z + teeth_height - e),

        # 8
        (x - ht, hw, z - e),
        (x - ht, -hw, z - e),
        (x + ht, hw, z - e),
        (x + ht, -hw, z - e),

        (x - htt - e, htw + e, z - e),
        (x - htt - e, -htw - e, z - e),
        (x + htt + e, htw + e, z - e),
        (x + htt + e, -htw - e, z - e),

        # 16
        (x - ht, hw, z - e - h + teeth_height),
        (x - ht, -hw, z - e - h + teeth_height),
        (x + ht, hw, z - e - h + teeth_height),
        (x + ht, -hw, z - e - h + teeth_height),

        (x - htt, htw, z - e - h + teeth_height),
        (x - htt, -htw, z - e - h + teeth_height),
        (x + htt, htw, z - e - h + teeth_height),
        (x + htt, -htw, z - e - h + teeth_height),

        # 24
        (x - htt, htw, z - e - h),
        (x - htt, -htw, z - e - h),
        (x + htt, htw, z - e - h),
        (x + htt, -htw, z - e - h),

        (x - hstt, hw, sth + hstw),
        (x - hstt, -hw, sth + hstw),
        (x + hstt, hw, sth + hstw),
        (x + hstt, -hw, sth + hstw),

        # 32
        (x - hstt, hw, sth - hstw),
        (x - hstt, -hw, sth - hstw),
        (x + hstt, hw, sth - hstw),
        (x + hstt, -hw, sth - hstw),

        (x - hstt, hw - side_teeth_height, sth + hstw),
        (x - hstt, -hw + side_teeth_height, sth + hstw),
        (x + hstt, hw - side_teeth_height, sth + hstw),
        (x + hstt, -hw + side_teeth_height, sth + hstw),

        #40
        (x - hstt, hw - side_teeth_height, sth - hstw),
        (x - hstt, -hw + side_teeth_height, sth - hstw),
        (x + hstt, hw - side_teeth_height, sth - hstw),
        (x + hstt, -hw + side_teeth_height, sth - hstw),
    ]
    edges = [
        (0, 1), (1, 3), (3, 2), (2, 0),
        (4, 5), (5, 7), (7, 6), (6, 4),
        (8, 9), (9, 11), (11, 10), (10, 8),
        (12, 13), (13, 15), (15, 14), (14, 12),
        (4, 12),(5, 13), (6, 14), (7, 15),
        (0, 8), (1, 9), (2, 10), (3, 11),
        (16, 17), (17, 19), (19, 18), (18, 16),
        (8, 16), (9, 17), (10, 18), (11, 19),
        (20, 21), (21, 23), (23, 22), (22, 20),
        (24, 25), (25, 27), (27, 26), (26, 24),
        (20, 24), (21, 25), (22, 26), (23, 27),

        (28, 30), (30, 34), (34, 32), (32, 28),
        (36, 38), (38, 42), (42, 40), (40, 36),
        (28, 36), (30, 38), (32, 40), (34, 42),

        (29, 31), (31, 35), (35, 33), (33, 29),
        (37, 39), (39, 43), (43, 41), (41, 37),
        (29, 37), (31, 39), (33, 41), (35, 43),
    ]
    faces = [
        (0, 1, 5, 4),
        (1, 3, 7, 5),
        (3, 2, 6, 7),
        (2, 0, 4, 6),

        (12, 13, 15, 14),

        (12, 4, 5, 13),
        (6, 14, 15, 7),
        (4, 12, 14, 6),
        (7, 15, 13, 5),

        (1, 0, 8, 9),
        (3, 1, 9, 11),
        (2, 3, 11, 10),
        (0, 2, 10, 8),

        (8, 16, 17, 9),
        (18, 10, 11, 19),

        (16, 20, 21, 17),
        (22, 18, 19, 23),
        (20, 16, 18, 22),
        (17, 21, 23, 19),

        (20, 24, 25, 21),
        (26, 22, 23, 27),
        (24, 20, 22, 26),
        (21, 25, 27, 23),

        (25, 24, 26, 27),

        (36, 38, 42, 40),
        (38, 36, 28, 30),
        (40, 42, 34, 32),
        (36, 40, 32, 28),
        (42, 38, 30, 34),

        (39, 37, 41, 43),
        (37, 39, 31, 29),
        (43, 41, 33, 35),
        (41, 37, 29, 33),
        (39, 43, 35, 31),

        (8, 10, 30, 28),
        (32, 34, 18, 16),
        (8, 28, 32, 16),
        (30, 10, 18, 34),

        (11, 9, 29, 31),
        (35, 33, 17, 19),
        (29, 9, 17, 33),
        (11, 31, 35, 19),
    ]

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh