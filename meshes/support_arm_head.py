import bpy
import bmesh
import math
from mathutils import Matrix, Vector
from meshes import screw

support_arm_head_name = 'arm_head_'
support_arm_head_screw_in_name = 'arm_head_screw_in'

# t: head thickness arround arms
# p: circular precision
# with_top_screw: adds screws allowing to fix support arms on top
# arm_dist: distance between arms
# arm_rp: arm circular precision
# arm_outer_r: arm radius
# arm_inner_r: arm screw radius
# arm_screw_length: arm screw length
# arm_D: arm metric thread diameter
# arm_P: arm metric thread pitch
# spider_rp: spider circular precision
# spider_r: spider radius
# spider_screw_length: spider screw length
# spider_D: spider metric thread diameter
# spider_p: spider metric thread pitch
def create_mesh(
    t, p, height, width, with_spider_screw, with_spider_screw_in, with_top_screw, with_bottom_screw_in, ocular_r, ocular_z,
    arm_dist, arm_rp, arm_outer_r, arm_inner_r, arm_screw_length, arm_D, arm_P, arm_screw_in_length, arm_screw_in_end_h,
    spider_rp, spider_r, spider_screw_length, spider_screw_z, spider_D, spider_P, spider_end_h
):
    hw = 0.5 * arm_dist
    ro = arm_outer_r + t
    ri = arm_inner_r

    # arm_hole_p = arm_rp + (4 - arm_rp % 4)
    # arm_hole_cuts = 0.25 * (arm_hole_p - 4)

    x0 = 0.5 * width
    y0 = spider_r
    y1 = hw - arm_outer_r
    y2 = hw
    y3 = ocular_r

    zsmid = spider_screw_z
    zst = spider_screw_z + spider_r
    zsb = spider_screw_z - spider_r

    zoct = None
    zocb = None
    if ocular_r > 0:
        zoct = ocular_z + ocular_r
        zocb = ocular_z - ocular_r

    mesh = bpy.data.meshes.new('tmp_arm_head')

    vertices = [
        (x0, 0, 0),
        (-x0, 0, 0),

        (x0, y0, 0),
        (-x0, y0, 0),

        (x0, y1, 0),
        (-x0, y1, 0),

        # 6
        (x0, 0, height),
        (-x0, 0, height),

        (x0, y0, height),
        (-x0, y0, height),

        (x0, y1, height),
        (-x0, y1, height),

        # 12
        (0, y2, 0),
        (0, y2, height),

        # 14
        (x0, 0, zsmid),
        (-x0, 0, zsmid),

        (x0, y0, zsb),
        (-x0, y0, zsb),

        (x0, y0, zst),
        (-x0, y0, zst),
    ]

    edges = [
        (1, 3), (3, 2), (2, 0),
        (3, 5), (5, 4), (4, 2),

        (7, 9), (9, 8), (8, 6),
        (9, 11), (11, 10), (10, 8),

        (4, 10), (5, 11),
    ]

    faces = [
        (0, 1, 3, 2),
        (2, 3, 5, 4),

        (7, 6, 8, 9),
        (9, 8, 10, 11),
    ]

    nb_verts0 = len(vertices)

    if ocular_r > 0:
        vertices.extend([
            (x0, y3, zoct),
            (-x0, y3, zoct),

            (x0, y3, zocb),
            (-x0, y3, zocb),
        ])

        faces.extend([
            (8, 16, 10),
            (9, 11, 17),

            (10, 16, nb_verts0),
            (17, 11, nb_verts0 + 1),

            (nb_verts0 + 2, 4, 10, nb_verts0),
            (5, nb_verts0 + 3, nb_verts0 + 1, 11),
        ])
    else:
        edges.extend([
            (2, 8), (3, 9),
        ])

        faces.extend([
            (2, 4, 10, 8),
            (5, 3, 9, 11),
        ])

    ri2mid = None
    obv_start = None
    obv_stop = None
    for i in range(0, arm_rp + 1):
        alpha = i * math.pi / arm_rp
        beta = math.pi + alpha

        roca = ro * math.cos(alpha)
        rosa = ro * math.sin(alpha)
        rica = ri * math.cos(alpha)
        risa = ri * math.sin(alpha)
        ricb = ri * math.cos(beta)
        risb = ri * math.sin(beta)

        verts = [
            (roca, y2 + rosa, 0),
            (roca, y2 + rosa, height),

            (rica, y2 + risa, 0),
            (rica, y2 + risa, height),

            (ricb, y2 + risb, 0),
            (ricb, y2 + risb, height),
        ]

        nbidx = len(verts)
        obv = len(vertices)
        otv = obv + 1
        ibv = obv + 2
        itv = obv + 3
        i2bv = obv + 4
        i2tv = obv + 5

        vertices.extend(verts)

        edges.extend([
            (obv, otv),
        ])

        if i > 0:
            edges.extend([
                (obv, obv - nbidx),
                (otv, otv - nbidx),
            ])

            faces.extend([
                (obv - nbidx, obv, otv, otv - nbidx),
                (itv, itv - nbidx, otv - nbidx, otv),
                (ibv - nbidx, ibv, obv, obv - nbidx),
            ])

            if alpha < math.pi / 2:
                faces.extend([
                    (i2bv - nbidx, i2bv, 5),
                    (i2tv, i2tv - nbidx, 11),
                ])
            else:
                if ri2mid == None:
                    ri2mid = i2bv - nbidx

                faces.extend([
                    (i2bv - nbidx, i2bv, 4),
                    (i2tv, i2tv - nbidx, 10),
                ])

            if not with_top_screw:
                faces.extend([
                    (13, itv - nbidx, itv),
                    (13, i2tv - nbidx, i2tv),
                ])

            if not with_bottom_screw_in:
                faces.extend([
                    (12, ibv, ibv - nbidx),
                    (12, i2bv, i2bv - nbidx),
                ])

            if i == arm_rp:
                obv_stop = obv
        else:
            obv_start = obv

    faces.extend([
        (5, ri2mid, 4),
        (10, ri2mid + 1, 11),

        (4, obv_stop + 4, obv_start),
        (5, obv_stop, obv_start + 4),

        (10, obv_start + 1, obv_stop + 5),
        (11, obv_start + 5, obv_stop + 1),

        (4, obv_start, obv_start + 1, 10),
        (obv_stop, 5, 11, obv_stop + 1),
    ])

    nb_verts = len(vertices)

    bvmid = None
    for i in range(0, spider_rp + 1):
        alpha = i * math.pi / spider_rp
        beta = -0.5 * math.pi + alpha
        y = spider_r * math.cos(beta)
        z =  zsmid + spider_r * math.sin(beta)

        y2 = 0.5 * spider_D * math.cos(beta)
        z2 =  zsmid + 0.5 * spider_D * math.sin(beta)

        verts = [
            (-x0, y, z),
            (x0, y2, z2),
        ]

        nbidx = len(verts)
        bv = len(vertices)
        tv = bv + 1

        vertices.extend(verts)

        if i > 0:
            edges.extend([
                (bv - nbidx, bv),
                (tv - nbidx, tv),
            ])

            if not with_spider_screw:
                faces.append((bv, bv - nbidx, 15))
            if not with_spider_screw_in:
                faces.append((tv - nbidx, tv, 14))

            if alpha < math.pi / 2:
                faces.extend([
                    (bv - nbidx, bv, 17),
                    (tv, tv - nbidx, 16),
                ])
            else:
                if bvmid is None:
                    bvmid = bv - nbidx

                faces.extend([
                    (bv - nbidx, bv, 19),
                    (tv, tv - nbidx, 18),
                ])

    faces.extend([
        (19, bv, 7, 9),
        (bv + 1, 18, 8, 6),
        (19, bvmid, 17),
        (18, bvmid + 1, 16),
    ])

    nb_verts2 = len(vertices)

    if ocular_r > 0:
        for i in range(0, p + 1):
            alpha = i * math.pi / p
            beta = -0.5 * math.pi + alpha
            rcb = ocular_r * math.cos(beta)
            rsb = ocular_r * math.sin(beta)

            verts = [
                (-x0, rcb, ocular_z + rsb),
                (x0, rcb, ocular_z + rsb),
            ]

            nbidx = len(verts)
            obv = len(vertices)
            otv = obv + 1

            vertices.extend(verts)

            edges.extend([
                (obv, otv)
            ])

            if i > 0:
                edges.extend([
                    (obv - nbidx, obv),
                    (otv - nbidx, otv)
                ])

                faces.extend([
                    (obv, obv - nbidx, otv - nbidx, otv),
                ])

                if alpha < 0.5 * math.pi:
                    faces.extend([
                        (obv - nbidx, obv, nb_verts0 + 3),
                        (otv, otv - nbidx, nb_verts0 + 2),
                    ])
                else:
                    faces.extend([
                        (obv - nbidx, obv, nb_verts0 + 1),
                        (otv, otv - nbidx, nb_verts0 + 0),
                    ])

        faces.extend([
            (nb_verts0, 16, nb_verts + 1, otv),
            (17, nb_verts0 + 1, obv, nb_verts),
            (nb_verts2 + 1, 0, 4, nb_verts0 + 2),
            (1, nb_verts2, nb_verts0 + 3, 5),
        ])
    else:
        faces.extend([
            (1, nb_verts, 17, 3),
            (nb_verts + 1, 0, 2, 16),
        ])


    mesh.from_pydata(vertices, edges, faces)

    bm = bmesh.new()
    bm.from_mesh(mesh)

    # mirror x
    ret = bmesh.ops.mirror(
        bm,
        geom = bm.faces[:] + bm.verts[:] + bm.edges[:],
        axis = 'Y'
    )

    bmesh.ops.reverse_faces(
        bm,
        faces = list(set(
            geom
            for geom in ret['geom']
            if isinstance(geom, bmesh.types.BMFace)
        ))
    )

    for i in [-1, 1]:
        if with_bottom_screw_in:
            ret = screw.screw_in(
                arm_inner_r,
                arm_screw_in_length,
                arm_rp,
                bm = None,
                z_start = 0,
                z_scale = -1,
                fill_end=True,
                D=arm_D,
                P=arm_P,
                start_h=0,
                end_h=arm_screw_in_end_h
            )

            bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((0, i * hw, 0)))
            mesh_screw_in = bpy.data.meshes.new('tmp_arm_head_screw_in')
            ret[0].to_mesh(mesh_screw_in)
            bm.from_mesh(mesh_screw_in)
            del mesh_screw_in

        if with_top_screw:
            ret = screw.screw(
                arm_inner_r,
                arm_screw_length,
                arm_rp,
                bm = None,
                # z_top = 0,
                # top_length = 0,
                tip_r = 0.5 * arm_inner_r,
                #tip_length = 0,
                fill_tip = True,
                D=arm_D,
                P=arm_P,
                # max_screw_bottom_precision = 10,
                ccw = True
            )

            bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((0, i * hw, height)))
            mesh_screw = bpy.data.meshes.new('tmp_arm_head_top_screw')
            ret[0].to_mesh(mesh_screw)
            bm.from_mesh(mesh_screw)
            del mesh_screw

    if with_spider_screw_in:
        ret = screw.screw_in(
            spider_r,
            spider_screw_length,
            spider_rp,
            bm = None,
            z_start = 0,
            z_scale = -1,
            fill_end=True,
            D=spider_D,
            P=spider_P,
            start_h=0,
            end_h=spider_end_h
        )

        bmesh.ops.rotate(ret[0], verts = ret[0].verts, matrix = Matrix.Rotation(-0.5 * math.pi, 3, 'Y'))
        bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((x0, 0, zsmid)))
        mesh_screw_in = bpy.data.meshes.new('tmp_arm_head_spider_screw_in')
        ret[0].to_mesh(mesh_screw_in)
        bm.from_mesh(mesh_screw_in)
        del mesh_screw_in

    if with_spider_screw:
        ret = screw.screw(
            spider_r,
            spider_screw_length,
            spider_rp,
            bm = None,
            # z_top = 0,
            # top_length = 0,
            tip_r = 0.5 * spider_r,
            # tip_length = 0,
            fill_tip=True,
            D=spider_D,
            P=spider_P,
            #max_screw_bottom_precision=10
        )

        bmesh.ops.rotate(ret[0], verts = ret[0].verts, matrix = Matrix.Rotation(-0.5 * math.pi, 3, 'Y'))
        bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((-x0, 0, zsmid)))
        mesh_screw = bpy.data.meshes.new('tmp_arm_head_spider_screw')
        ret[0].to_mesh(mesh_screw)
        bm.from_mesh(mesh_screw)
        del mesh_screw

    # screw_in front face
    # screw back face

    mesh = bpy.data.meshes.new(support_arm_head_name + str((
        t, p, height, width, with_spider_screw, with_spider_screw_in, with_top_screw, with_bottom_screw_in, ocular_r, ocular_z,
        arm_dist, arm_rp, arm_outer_r, arm_inner_r, arm_screw_length, arm_D, arm_P, arm_screw_in_length, arm_screw_in_end_h,
        spider_rp, spider_r, spider_screw_length, spider_screw_z, spider_D, spider_P, spider_end_h
    )))

    bm.to_mesh(mesh)

    return mesh