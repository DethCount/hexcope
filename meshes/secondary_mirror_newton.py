import importlib
import bpy
import bmesh

import math
from mathutils import Matrix, Vector

from optics import get_newton_dist_to_spider_arm
from meshes import screw

import importlib
importlib.reload(screw)

secondary_mirror_newton_name = 'newton_secondary'

# t: thickness
# top_t: top thickness
# rx: secondary mirror radius along x in secondary mirror plane
# ry: secondary mirror radius along y in secondary mirror plane
# rp: circles precision
def create_mesh(
    t, top_t, rx, ry, rp,
    arm_n,
    spider_r, spider_screw_length, spider_rp, spider_D, spider_P, spider_end_h
):
    mesh = bpy.data.meshes.new(
        secondary_mirror_newton_name + '_tmp'
    )

    rpa = arm_n * rp

    dists = get_newton_dist_to_spider_arm(arm_n, rx, ry)
    dists_rpa = get_newton_dist_to_spider_arm(rpa, rx, ry)

    pi4m = -0.25 * math.pi
    cpi4m = math.cos(pi4m)
    spi4m = math.sin(pi4m)

    vertices = [
        (0, 0, t),
        (0, 0, 0),
    ]
    edges = []
    faces = []

    nb_verts = len(vertices)

    holes = list()
    for i in range(0, rpa + 1):
        alpha = i * math.tau / rpa

        ca = math.cos(alpha)
        sa = math.sin(alpha)

        x = rx * ca
        y = ry * sa
        dca = dists_rpa[i if i != rpa else 0] * ca
        dsa = dists_rpa[i if i != rpa else 0] * sa

        make_hole = i % rp in [0, 1]

        xc = x * cpi4m
        xs = x * -spi4m

        xic = xc - t * ca
        xis = xs - t * ca
        yi = y - t * sa
        dic = dca - top_t * ca
        dis = dsa - top_t * sa

        ztop = rx * cpi4m

        nbidx = 7
        trv = nb_verts + nbidx * i
        brv = trv + 1
        rrv = trv + 2
        brrv = trv + 3
        ritrv = trv + 4
        britrv = trv + 5
        ribrv = trv + 6

        tlv = trv - nbidx
        blv = brv - nbidx
        rlv = rrv - nbidx
        brlv = brrv - nbidx
        ritlv = ritrv - nbidx
        britlv = britrv - nbidx
        riblv = ribrv - nbidx

        vertices.extend([
            (xc, y, xs), # oblique ellipse with vertical thickness
            (xc, y, xs - t), # oblique ellipse
            (dca, dsa, ztop + top_t), # horizontal top ellipse with thickness (xc, y, ztop + top_t) (not conserving angles)
            (dca, dsa, ztop), # horizontal top ellipse (xc, y, ztop)
            (dic, dis, ztop + top_t), # internal horizontal top ellipse with thickness (xic, yi, ztop + top_t)
            (dic, dis, ztop), # internal horizontal top ellipse (xic, yi, ztop)
            (xic, yi, xis), # internal oblique ellipse with vertical thickness
        ])

        edges.extend([
            (trv, brv),
            (trv, brrv),
            (ritrv, britrv),
            (britrv, ribrv),
        ])

        if i > 0:
            edges.extend([
                (trv, tlv),
                (brv, blv),
                (rrv, rlv),
                (brrv, brlv),
                (ritrv, ritlv),
                (britrv, britlv),
                (ribrv, riblv),
            ])

            faces.extend([
                (trv, tlv, blv, brv),
                (1, brv, blv),
                (trv, brrv, brlv, tlv),
                (rrv, ritrv, ritlv, rlv),
                (ritlv, ritrv, britrv, britlv),
                (britlv, britrv, ribrv, riblv),
                (0, riblv, ribrv),
            ])

            hole_face = (brrv, rrv, rlv, brlv)
            if not make_hole:
                faces.append(hole_face)
            else:
                holes.append(hole_face)

        if i % rp != 0:
            edges.append((brrv, rrv))

    holes_l = len(holes)
    for i in range(0, round(holes_l / 2)):
        alpha = i * math.tau / arm_n
        ca = math.cos(alpha)
        sa = math.sin(alpha)

        rca = dists[i] * ca
        rsa = dists[i] * sa


        hole_idx = 2 * i - 1 if i > 0 else holes_l - 1
        next_hole_idx = hole_idx + 1 if hole_idx + 1 < holes_l else 0

        v1 = None
        v2 = None
        v3 = None
        v4 = None
        for j in range(0, spider_rp + 1):
            beta = j * math.tau / spider_rp

            y = 0.5 * spider_D * math.cos(beta)
            z = 0.5 * spider_D * math.sin(beta)

            x2 = rca - y * sa
            y2 = rsa + y * ca
            z2 = ztop + 0.5 * top_t + z

            vidx = len(vertices)
            vertices.append((x2, y2, z2))

            if j > 0:
                edges.append((vidx, vidx - 1))

                if beta < math.tau / 4:
                    if v1 is None:
                        v1 = vidx - 1
                    faces.extend([
                        (vidx, vidx - 1, holes[next_hole_idx][1])
                    ])
                elif beta < math.tau / 2:
                    if v2 is None:
                        v2 = vidx - 1
                    faces.extend([
                        (vidx, vidx - 1, holes[hole_idx][2])
                    ])
                elif beta < 3 * math.tau / 4:
                    if v3 is None:
                        v3 = vidx - 1
                    faces.extend([
                        (vidx, vidx - 1, holes[hole_idx][3])
                    ])
                else:
                    if v4 is None:
                        v4 = vidx - 1
                    faces.extend([
                        (vidx, vidx - 1, holes[next_hole_idx][0])
                    ])

        faces.extend([
            (v1, holes[next_hole_idx][0], holes[next_hole_idx][1]),
            (v2, holes[next_hole_idx][1], holes[hole_idx][2]),
            (v3, holes[hole_idx][2], holes[hole_idx][3]),
            (v4, holes[hole_idx][3], holes[next_hole_idx][0])
        ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    bm = bmesh.new()
    bm.from_mesh(mesh)
    del mesh

    for i in range(0, arm_n):
        alpha = i * math.tau / arm_n
        ret = screw.screw_in(
            spider_r,
            spider_screw_length,
            spider_rp,
            bm = None,
            z_start=0,
            z_scale=-1,
            fill_end=True,
            D=spider_D,
            P=spider_P,
            end_h=spider_end_h
        )

        bmesh.ops.rotate(
            ret[0],
            verts = ret[0].verts[:],
            matrix = Matrix.Rotation(-0.5 * math.pi, 3, 'Y')
        )

        bmesh.ops.translate(
            ret[0],
            verts = ret[0].verts,
            vec = Vector((dists[i], 0, ztop + 0.5 * top_t))
        )

        bmesh.ops.rotate(
            ret[0],
            verts = ret[0].verts[:],
            matrix = Matrix.Rotation(alpha, 3, 'Z')
        )

        mesh = bpy.data.meshes.new(secondary_mirror_newton_name + '_tmp_screw_in')
        ret[0].to_mesh(mesh)
        ret[0].free()
        bm.from_mesh(mesh)

    mesh = bpy.data.meshes.new(
        secondary_mirror_newton_name
        + '_' + str((
            t, rx, ry, rp,
            arm_n,
            spider_r, spider_screw_length, spider_rp, spider_D, spider_P, spider_end_h
        ))
    )

    bm.to_mesh(mesh)
    bm.free()

    return mesh