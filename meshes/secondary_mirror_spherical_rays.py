import bpy
import math

from optics import hex2xyz

secondary_mirror_spherical_rays = 'rays'

def create_mesh(
    e, h, r, f, x, y, z,
    primary_f, hex_side
):
    mesh = bpy.data.meshes.new(
        secondary_mirror_spherical_rays
        + '_' + str((
            e, h, r, f, x, y, z,
            primary_f, hex_side
        ))
    )

    p0 = (10, 10, 10)

    # print('spherical_rays')
    p1w0 = hex2xyz(primary_f, hex_side, x, y, z, 0)
    p1w1 = hex2xyz(primary_f, hex_side, x, y, z, 1)
    p1w2 = hex2xyz(primary_f, hex_side, x, y, z, 2)

    u = (p1w1[0] - p1w0[0], p1w1[1] - p1w0[1], p1w1[2] - p1w0[2])
    v = (p1w2[0] - p1w0[0], p1w2[1] - p1w0[1], p1w2[2] - p1w0[2])

    n = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

    ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
    un = (n[0] / ln, n[1] / ln, n[2] / ln)

    d10 = (
        p1w0[0] - p0[0],
        p1w0[1] - p0[1],
        p1w0[2] - p0[2]
    )

    ld10 = math.sqrt(d10[0] ** 2 + d10[1] ** 2 + d10[2] ** 2)

    ud10 = (
        d10[0] / ld10,
        d10[1] / ld10,
        d10[2] / ld10
    )

    reflected = (
        ud10[0] - ud10[1] * un[0],
        ud10[1] + ud10[2] * un[1],
        ud10[2] + ud10[0] * un[2],
    )

    lreflected = math.sqrt(reflected[0] ** 2 + reflected[1] ** 2 + reflected[2] ** 2)
    ureflected = (
        reflected[0] / lreflected,
        reflected[1] / lreflected,
        reflected[2] / lreflected
    )

    far = 100

    sh = f - math.sqrt(f ** 2 - r ** 2)

    dunxy = math.sqrt(un[0] ** 2 + un[1] ** 2)
    maxd0 = 0
    maxd = 0
    h0 = 0
    if dunxy > 0:
        maxd0 = math.sqrt(p1w0[0] ** 2 + p1w0[1] ** 2) / math.sqrt(un[0] ** 2 + un[1] ** 2)
        h0 = maxd0 * un[2]
        #maxd = (secondary_h + h - secondary_f) / un[2]
    #maxd0z = (secondary_h + h - p1w0[2]) / un[2]
    maxd = h + f / math.sqrt(p1w0[0] ** 2 + p1w0[1] ** 2 + (un[2] * maxd0 - p1w0[2]) ** 2)
    # print('sh: ' + str(sh) + ' maxd: ' + str(maxd) + ' h0: ' + str(h0))

    p1n = (
        p1w0[0] + ureflected[0] * maxd0,
        p1w0[1] + ureflected[1] * maxd0,
        p1w0[2] + ureflected[2] * maxd0
    )

    pun = (
        p1w0[0] + un[0] * maxd,
        p1w0[1] + un[1] * maxd,
        p1w0[2] + un[2] * maxd
    )

    # print('p1n: ' + str(p1n))

    vertices = [
        p0,
        p1w0,
        pun,
        p1n,

        (p0[0] + e, p0[1] + e, p0[2] + e),
        (p1w0[0] + e, p1w0[1] + e, p1w0[2] + e),
        (pun[0] + e, pun[1] + e, pun[2] + e),
        (p1n[0] + e, p1n[1] + e, p1n[2] + e),

        (pun[0], pun[1], -2.0),
        (pun[0] + e, pun[1] + e, -2.0 + e),
    ]
    edges = [
        (0, 1),
    ]
    faces = [
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 6, 9, 8),
    ]

    nb_verts = len(vertices)
    p = 10
    czmax = far
    czstep = 10
    for cz in range(1, math.ceil(czmax / czstep) + 1):
        for i in range(0, p + 1):
            alpha = i * (2 * math.pi) / p
            idx = len(vertices)
            vertices.extend([
                (5 * r * math.cos(alpha), r * math.sin(alpha), cz * czstep)
            ])

            if i > 0:
                edges.extend([(idx - 1, idx)])
            if i == p:
                edges.extend([(idx, idx - p)])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh