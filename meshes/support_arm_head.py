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
    t, p, with_top_screw,
    arm_dist, arm_rp, arm_outer_r, arm_inner_r, arm_screw_length, arm_D, arm_P,
    spider_rp, spider_r, spider_screw_length, spider_D, spider_P
):
    hw = 0.5 * arm_dist
    base_width = arm_outer_r + t
    screw_in_end_h = 0.5 * t
    total_h = t + arm_screw_length + screw_in_end_h
    ro = arm_outer_r + t
    ri = arm_inner_r

    # arm_hole_p = arm_rp + (4 - arm_rp % 4)
    # arm_hole_cuts = 0.25 * (arm_hole_p - 4)

    x0 = base_width
    y0 = spider_r
    y1 = hw - arm_outer_r
    y2 = hw

    zmid = 0.5 * total_h
    zst = zmid + spider_r
    zsb = zmid - spider_r

    mesh = bpy.data.meshes.new('tmp_arm_head')

    vertices = [
        (x0, 0, 0),
        (-x0, 0, 0),

        (x0, y0, 0),
        (-x0, y0, 0),

        (x0, y1, 0),
        (-x0, y1, 0),

        # 6
        (x0, 0, total_h),
        (-x0, 0, total_h),

        (x0, y0, total_h),
        (-x0, y0, total_h),

        (x0, y1, total_h),
        (-x0, y1, total_h),

        # 12
        (0, y2, 0),
        (0, y2, total_h),

        # 14
        (x0, y0, zst),
        (-x0, y0, zst),

        (x0, y0, zsb),
        (-x0, y0, zsb),
    ]

    edges = [
        (1, 3), (3, 2), (2, 0),
        (3, 5), (5, 4), (4, 2),

        (7, 9), (9, 8), (8, 6),
        (9, 11), (11, 10), (10, 8),

        (2, 8), (3, 9), (4, 10), (5, 11),
    ]

    faces = [
        (0, 1, 3, 2),
        (2, 3, 5, 4),

        (7, 6, 8, 9),
        (9, 8, 10, 11),

        (2, 4, 10, 8),
        (5, 3, 9, 11),
    ]

    ri2mid = None
    obv_start = None
    obv_stop = None
    top_screw_circle = list()
    bottom_screw_circle = list()
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
            (roca, y2 + rosa, total_h),

            (rica, y2 + risa, 0),
            (rica, y2 + risa, total_h),

            (ricb, y2 + risb, 0),
            (ricb, y2 + risb, total_h),
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

    for i in range(0, spider_rp + 1):
        alpha = i * math.pi / spider_rp
        beta = -0.5 * math.pi + alpha
        y = spider_r * math.cos(beta)
        z =  zmid + spider_r * math.sin(beta)

        verts = [
            (-x0, y, z),
            (x0, y, z),
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

            if alpha < math.pi / 2:
                faces.extend([
                    (bv - nbidx, bv, 17),
                    (tv, tv - nbidx, 16),
                ])
            else:
                faces.extend([
                    (bv - nbidx, bv, 15),
                    (tv, tv - nbidx, 14),
                ])

    faces.extend([
        (1, nb_verts, 17, 3),
        (nb_verts + 1, 0, 2, 16),

        (15, bv, 7, 9),
        (bv + 1, 14, 8, 6),
    ])


    mesh.from_pydata(vertices, edges, faces)

    bm = bmesh.new()
    bm.from_mesh(mesh)

    ret = screw.screw_in(
        arm_inner_r,
        arm_screw_length,
        arm_rp,
        bm = None,
        z_start = 0,
        z_scale = -1,
        fill_end=True,
        D=arm_D,
        P=arm_P,
        start_h=0,
        end_h=screw_in_end_h
    )

    bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((0, hw, 0)))
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
            # max_screw_bottom_precision = 10
        )

        bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((0, hw, total_h)))
        mesh_screw = bpy.data.meshes.new('tmp_arm_head_top_screw')
        ret[0].to_mesh(mesh_screw)
        bm.from_mesh(mesh_screw)
        del mesh_screw

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
        end_h=spider_r
    )

    bmesh.ops.rotate(ret[0], verts = ret[0].verts, matrix = Matrix.Rotation(-0.5 * math.pi, 3, 'Y'))
    bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((x0, 0, zmid)))
    mesh_screw_in = bpy.data.meshes.new('tmp_arm_head_spider_screw_in')
    ret[0].to_mesh(mesh_screw_in)
    bm.from_mesh(mesh_screw_in)
    del mesh_screw_in

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
    bmesh.ops.translate(ret[0], verts = ret[0].verts, vec = Vector((-x0, 0, zmid)))
    mesh_screw = bpy.data.meshes.new('tmp_arm_head_spider_screw')
    ret[0].to_mesh(mesh_screw)
    bm.from_mesh(mesh_screw)
    del mesh_screw

    # screw_in front face
    # screw back face

    mesh = bpy.data.meshes.new(support_arm_head_name + str((
        t, p,
        arm_dist, arm_rp, arm_outer_r, arm_inner_r, arm_screw_length, arm_D, arm_P,
        spider_r, spider_screw_length, spider_D, spider_P
    )))

    bm.to_mesh(mesh)

    return mesh