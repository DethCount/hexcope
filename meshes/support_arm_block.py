import bpy
import math
from mathutils import Vector

from optics import get_support_arm_point, hex2xy, hex2xyz
from meshes import half_hex

support_arm_block_name = 'support_arm_block'

# todo: thicker nose part
# wl : wing length: v4 distance from v3 along v35
def create_mesh(
    e, f, n, r, t, mx, my, wl, p,
    hex_thickness, hex_interior_thickness, hex_walls_height,
    primary_thickness,
    arm_radius,
    clip_depth, clip_thickness, clip_height, clip_e, clip_padding_x, clip_padding_z,
    is_left = False
):
    mesh = bpy.data.meshes.new(
        support_arm_block_name
        + '_' + str((
            e, f, n, r, t, mx, my, wl, p,
            hex_thickness, hex_interior_thickness, hex_walls_height,
            primary_thickness,
            arm_radius,
            clip_depth, clip_thickness, clip_height, clip_e
        ))
    )

    arm_points = get_support_arm_point(n, r, mx, my, 0)
    arm_point = arm_points[0 if is_left else 1]

    no_flip = n % 2 == 0 and not is_left or n % 2 != 0 and is_left

    face = None
    if n % 2 == 0:
        face = Vector((
            0.5 * n + 1,
            0,
            3 if is_left else 2
        ))
    else:
        face = Vector((
            math.ceil(0.5 * n) + (1 if is_left else 0),
            -1 if is_left else 1,
            2 if is_left else 3
        ))

    rp = Vector(hex2xyz(f, r, face.x, face.y, face.z, 2))
    lp = Vector(hex2xyz(f, r, face.x, face.y, face.z, 1))

    hex_total_thickness = hex_thickness + hex_walls_height
    z_displacement = -hex_walls_height

    rv = Vector((rp.x, rp.y, rp.z + z_displacement))
    lv = Vector((lp.x, lp.y, lp.z + z_displacement))

    vrl = lv - rv
    vrln = vrl.normalized()
    vmid = rv + 0.5 * vrl
    vpadx = clip_padding_x * vrln

    h0 = hex_walls_height
    h1 = hex_total_thickness
    h2 = min(rv.z, lv.z)
    h3 = max(rv.z, lv.z) + h1

    ar = arm_radius
    art = ar + t
    rvp = rv + vpadx
    lvp = lv - vpadx

    rv2 = Vector((arm_point[0], arm_point[1] - art, 0))
    lv2 = Vector((arm_point[0], arm_point[1] + art, 0))

    vertices = [
        (rvp.x, rvp.y, rvp.z),
        (rvp.x, rvp.y, rvp.z + h0),
        (rvp.x, rvp.y, rvp.z + h1),

        (lvp.x, lvp.y, lvp.z),
        (lvp.x, lvp.y, lvp.z + h0),
        (lvp.x, lvp.y, lvp.z + h1),

        # 6
        (rvp.x + t, rvp.y, h2),
        (rvp.x + t, rvp.y, h3),

        (lvp.x + t, lvp.y, h2),
        (lvp.x + t, lvp.y, h3),

        # 10
        (rv2.x, rv2.y, h2),
        (rv2.x, rv2.y, h3),

        (lv2.x, lv2.y, h2),
        (lv2.x, lv2.y, h3),

        # 14
        (arm_point[0] - ar, arm_point[1] - ar, h2),
        (arm_point[0] - ar, arm_point[1] - ar, h3),

        (arm_point[0] - ar, arm_point[1] + ar, h2),
        (arm_point[0] - ar, arm_point[1] + ar, h3),

        (arm_point[0] + ar, arm_point[1] - ar, h2),
        (arm_point[0] + ar, arm_point[1] - ar, h3),

        (arm_point[0] + ar, arm_point[1] + ar, h2),
        (arm_point[0] + ar, arm_point[1] + ar, h3),

        # 22
    ]

    edges = [
        (0, 1), (1, 2),
        (3, 4), (4, 5),
        (0, 3), (1, 4), (2, 5),

        (6, 7), (8, 9),
        (6, 8), (7, 9),
        (0, 6), (2, 7),
        (3, 8), (5, 9),

        (10, 11), (12, 13),
        (6, 10), (7, 11),
        (8, 12), (9, 13),
    ]

    faces = [
        (1, 2, 5, 4),
        (5, 2, 7, 9),
        (0, 3, 8, 6),
        (2, 0, 6, 7),
        (3, 5, 9, 8),
        (7, 6, 10, 11),
        (8, 9, 13, 12),
    ]

    nb_verts = len(vertices)

    apo_mid = None
    api_mid = None
    api_r = None
    api_l = None

    for i in range(0, p + 1):
        alpha = -math.pi / 2 + i * math.pi / p
        ca = math.cos(alpha)
        sa = math.sin(alpha)

        beta = i * math.tau / p
        cb = math.cos(beta)
        sb = math.sin(beta)

        vertices.extend([
            (arm_point[0] + art * ca, arm_point[1] + art * sa, h2),
            (arm_point[0] + art * ca, arm_point[1] + art * sa, h3),

            (arm_point[0] + ar * cb, arm_point[1] + ar * sb, h2),
            (arm_point[0] + ar * cb, arm_point[1] + ar * sb, h3),
        ])

        nbidx = 4
        apo_bv = nb_verts + i * nbidx
        apo_tv = apo_bv + 1
        api_bv = apo_bv + 2
        api_tv = apo_bv + 3

        edges.extend([
            (apo_tv, apo_bv),
            (api_tv, api_bv),
        ])

        if i > 0:
            edges.extend([
                (apo_tv, apo_tv - nbidx),
                (apo_bv, apo_bv - nbidx),

                (api_tv, api_tv - nbidx),
                (api_bv, api_bv - nbidx),
            ])

            faces.extend([
                (apo_tv, apo_tv - nbidx, apo_bv - nbidx, apo_bv),
                (api_tv - nbidx, api_tv, api_bv, api_bv - nbidx),
            ])

            if alpha < 0:
                faces.extend([
                    (apo_bv, apo_bv - nbidx, 18),
                    (apo_tv - nbidx, apo_tv, 19)
                ])
            else:
                if apo_mid == None:
                    apo_mid = apo_bv - nbidx

                faces.extend([
                    (apo_bv, apo_bv - nbidx, 20),
                    (apo_tv - nbidx, apo_tv, 21),
                ])

            if beta < math.pi / 2:
                faces.extend([
                    (api_bv - nbidx, api_bv, 20),
                    (api_tv, api_tv - nbidx, 21),
                ])
            elif beta < (5 if no_flip else 7) * math.pi / 6:
                if api_l == None:
                    api_l = api_bv - nbidx

                if no_flip:
                    faces.extend([
                        (api_bv - nbidx, api_bv, 12), # 16
                        (api_tv, api_tv - nbidx, 13), # 17
                    ])
                else:
                    faces.extend([
                        (api_bv - nbidx, api_bv, 8),
                        (api_tv, api_tv - nbidx, 9),
                    ])
            elif beta < 3 * math.pi / 2:
                if api_mid == None:
                    api_mid = api_bv - nbidx

                if no_flip:
                    faces.extend([
                        (api_bv - nbidx, api_bv, 6), # 14
                        (api_tv, api_tv - nbidx, 7), # 15
                    ])
                else:
                    faces.extend([
                        (api_bv - nbidx, api_bv, 10),
                        (api_tv, api_tv - nbidx, 11),
                    ])
            else:
                if api_r == None:
                    api_r = api_bv - nbidx

                faces.extend([
                    (api_bv - nbidx, api_bv, 18),
                    (api_tv, api_tv - nbidx, 19),
                ])

    faces.extend([
        (18, 20, apo_mid),
        (21, 19, apo_mid + 1),
        (18, 10, api_r),
        (11, 19, api_r + 1),
        (api_l, 12, 20),
        (13, api_l + 1, 21),
    ])

    if no_flip:
        faces.extend([
            (6, 8, 12),
            (7, 13, 9),

            (6, 12, api_mid),
            (13, 7, api_mid + 1),

            (10, 6, api_r),
            (7, 11, api_r + 1),
        ])
    else:
        faces.extend([
            (6, 8, 10),
            (7, 11, 9),

            (10, 8, api_mid),
            (9, 11, api_mid + 1),

            (8, 12, api_l),
            (9, api_l + 1, 13),
        ])

    ret = half_hex.create_clip_face(
        clip_e,
        f,
        r,
        clip_depth,
        clip_thickness,
        clip_height,
        face,
        hex_walls_height,
        1,
        len(vertices),
        vmid + Vector((0, 0, h0)),
        padding_x = clip_padding_x,
        padding_z = clip_padding_z
    )
    vertices.extend(ret[0])
    edges.extend(ret[1])
    faces.extend(ret[2])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh