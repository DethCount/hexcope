import importlib
import bpy
import bmesh

import math
from mathutils import Matrix, Vector

from optics import get_support_arm_point, hex2xy, hex2xyz
from meshes import \
    half_hex, \
    screw

importlib.reload(half_hex)
importlib.reload(screw)

support_arm_block_name = 'support_arm_block'

# todo: thicker nose part
# wl : wing length: v4 distance from v3 along v35
def create_mesh(
    e, f, n, r, t, wl, p,
    hex_thickness, hex_interior_thickness, hex_walls_height,
    primary_thickness,
    arm_radius,
    clip_depth, clip_thickness, clip_height, clip_e, clip_padding_x, clip_padding_z,
    blocking_screw_r, blocking_screw_length, blocking_screw_rp, blocking_screw_D, blocking_screw_P,
    is_left = False
):
    mesh = bpy.data.meshes.new(support_arm_block_name + '_tmp')

    arm_points = get_support_arm_point(n, r, 0)
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

    bsD = blocking_screw_D if blocking_screw_D is not None else screw.get_D(2 * blocking_screw_r)
    bsR = 0.5 * bsD

    h0 = hex_walls_height
    h1 = hex_total_thickness
    h2 = min(rv.z, lv.z)
    h3 = max(rv.z, lv.z) + h1
    h23mid = h2 + 0.5 * (h3 - h2)
    h22 = h23mid - bsR
    h32 = h23mid + bsR

    ar = arm_radius

    apor = math.sqrt((ar + t) ** 2 + (bsR + 0.5 * t) ** 2)

    art = ar + t
    arc = apor * math.cos(0.25 * math.pi)
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
        (arm_point[0] + ar, arm_point[1], h2),
        (arm_point[0] + ar, arm_point[1], h3),

        # 24
        (arm_point[0] + arc, arm_point[1] + bsR, h22),
        (arm_point[0] + arc, arm_point[1] + bsR, h32),

        (arm_point[0] + arc, arm_point[1] - bsR, h22),
        (arm_point[0] + arc, arm_point[1] - bsR, h32),
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

        (18, 20, 22),
        (21, 19, 23),

        (24, 25, 27, 26),
    ]

    nb_verts = len(vertices)

    api_mid = None
    api_r = None
    api_l = None

    for i in range(0, p + 1):
        alpha = -math.pi / 2 + i * 0.25 * math.pi / p
        ca = math.cos(alpha)
        sa = math.sin(alpha)

        alpha2 = math.pi / 2 - i * 0.25 * math.pi / p
        ca2 = math.cos(alpha2)
        sa2 = math.sin(alpha2)

        beta = i * math.tau / p
        cb = math.cos(beta)
        sb = math.sin(beta)

        vertices.extend([
            (arm_point[0] + art * ca, arm_point[1] + art * sa, h2),
            (arm_point[0] + art * ca, arm_point[1] + art * sa, h3),

            (arm_point[0] + art * ca2, arm_point[1] + art * sa2, h2),
            (arm_point[0] + art * ca2, arm_point[1] + art * sa2, h3),

            (arm_point[0] + ar * cb, arm_point[1] + ar * sb, h2),
            (arm_point[0] + ar * cb, arm_point[1] + ar * sb, h3),
        ])

        nbidx = 6
        apo_bv = nb_verts + i * nbidx
        apo_tv = apo_bv + 1
        apor_bv = apo_bv + 2
        apor_tv = apo_bv + 3
        api_bv = apo_bv + 4
        api_tv = apo_bv + 5

        edges.extend([
            (apo_tv, apo_bv),
            (apor_tv, apor_bv),
            (api_tv, api_bv),
        ])

        if i > 0:
            edges.extend([
                (apo_tv, apo_tv - nbidx),
                (apo_bv, apo_bv - nbidx),

                (apor_tv, apor_tv - nbidx),
                (apor_bv, apor_bv - nbidx),

                (api_tv, api_tv - nbidx),
                (api_bv, api_bv - nbidx),
            ])

            faces.extend([
                (apo_tv, apo_tv - nbidx, apo_bv - nbidx, apo_bv),
                (apor_tv, apor_tv - nbidx, apor_bv - nbidx, apor_bv),
                (api_tv - nbidx, api_tv, api_bv, api_bv - nbidx),
            ])

            faces.extend([
                (apo_bv, apo_bv - nbidx, 18),
                (apo_tv - nbidx, apo_tv, 19)
            ])

            faces.extend([
                (apor_bv, apor_bv - nbidx, 20),
                (apor_tv - nbidx, apor_tv, 21),
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
        (18, 10, api_r),
        (11, 19, api_r + 1),
        (api_l, 12, 20),
        (13, api_l + 1, 21),

        (18, apo_bv, apor_bv, 20),
        (19, apo_tv, apor_tv, 21),

        (apor_bv, 24, 25, apor_tv),
        (apo_bv, 26, 27, apo_tv),
        (apo_bv, 26, 24, apor_bv),
        (apo_tv, 27, 25, apor_tv),
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

    nb_verts2 = len(vertices)
    for i in range(0, blocking_screw_rp + 1):
        alpha = i * math.tau / blocking_screw_rp
        ca = math.cos(alpha)
        sa = math.sin(alpha)

        vertices.append((
            arm_point[0] + arc,
            arm_point[1] + bsR * ca,
            h23mid + bsR * sa
        ))

        idx = nb_verts2 + i

        if i > 0:
            edges.extend([
                (idx - 1, idx)
            ])

            if alpha < 0.5 * math.pi:
                faces.append((idx - 1, idx, 25))
            elif alpha < math.pi:
                faces.append((idx - 1, idx, 27))
            elif alpha < 1.5 * math.pi:
                faces.append((idx - 1, idx, 26))
            else:
                faces.append((idx - 1, idx, 24))

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

    bm = bmesh.new()
    # bm.from_mesh(mesh)

    ret = screw.screw_in(
        blocking_screw_r,
        blocking_screw_length,
        blocking_screw_rp,
        None,
        z_start=-ar,
        z_scale=-1,
        fill_start=True,
        fill_end=True,
        D=blocking_screw_D,
        P=blocking_screw_P,
        start_h=ar,
        end_h=ar
    )

    bm2 = bmesh.new()
    c1 = bmesh.ops.create_circle(bm2, segments = blocking_screw_rp, radius = bsR)
    c1_edges = list(set(
        edg
        for vec in c1['verts']
        for edg in vec.link_edges
    ))
    c2 = bmesh.ops.extrude_edge_only(bm2, edges = c1_edges)
    c2_verts = list(set(
        geom
        for geom in c2['geom']
        if isinstance(geom, bmesh.types.BMVert)
    ))
    c2_edges = list(set(
        geom
        for geom in c2['geom']
        if isinstance(geom, bmesh.types.BMEdge)
    ))

    bmesh.ops.edgeloop_fill(bm2, edges = c1_edges)
    bmesh.ops.edgeloop_fill(bm2, edges = c2_edges)

    bmesh.ops.translate(bm2, verts = c2_verts, vec = (0, 0, -blocking_screw_length - ar))

    bmesh.ops.rotate(
        bm2, # ret[0],
        verts = bm2.verts[:],#ret[0].verts[:],
        matrix = Matrix.Rotation(-0.5 * math.pi, 3, 'Y')
    )

    bmesh.ops.translate(
        bm2, # ret[0],
        verts = bm2.verts[:],#ret[0].verts[:],
        vec = (
            arm_point[0] + arc,
            arm_point[1],
            h23mid
        )
    )

    screw_in_mesh = bpy.data.meshes.new(support_arm_block_name + '_tmp_screw_in')
    # ret[0].to_mesh(screw_in_mesh)
    bm2.to_mesh(screw_in_mesh)
    # ret[0].free()

    obj_name = support_arm_block_name + '_tmp_obj'
    support_arm_obj = bpy.data.objects.new(obj_name, mesh)
    temp_collection = bpy.data.collections.new('temp_collection')
    bpy.context.scene.collection.children.link(temp_collection)
    temp_collection.objects.link(support_arm_obj)

    screw_in_obj = bpy.data.objects.new(support_arm_block_name + '_tmp_screw_in_obj', screw_in_mesh)
    temp_collection.objects.link(screw_in_obj)
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers['Boolean'].operation = 'DIFFERENCE'
    bpy.context.object.modifiers['Boolean'].object = screw_in_obj
    # mod_bool = support_arm_obj.modifiers.new(type='BOOLEAN', name='screw_in_bool')
    # mod_bool.object = screw_in_obj
    # mod_bool.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply({"object": support_arm_obj}, modifier = 'Boolean')

    depsgraph = bpy.context.evaluated_depsgraph_get()
    support_arm_eval_obj = support_arm_obj.evaluated_get(depsgraph)


    bm.from_mesh(support_arm_eval_obj.data)

    mesh = bpy.data.meshes.new(
        support_arm_block_name
        + '_' + str((
            e, f, n, r, t, wl, p,
            hex_thickness, hex_interior_thickness, hex_walls_height,
            primary_thickness,
            arm_radius,
            clip_depth, clip_thickness, clip_height, clip_e
        ))
    )

    bm.to_mesh(mesh)
    bm.free()

    return mesh