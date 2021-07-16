import bpy
import math

from optics import hex2xyz

primary_mirror_normals_name = 'primary_mirror_normals'

def create_mesh(e, f, r, x, y, z):
    mesh = bpy.data.meshes.new(
        primary_mirror_normals_name
        + '_' + str((e, f, x, y, z))
    )

    # print('primary_mirror_normals')
    p1w0 = hex2xyz(f, r, x, y, z, 0)
    p1w1 = hex2xyz(f, r, x, y, z, 1)
    p1w2 = hex2xyz(f, r, x, y, z, 2)

    u = (p1w1[0] - p1w0[0], p1w1[1] - p1w0[1], p1w1[2] - p1w0[2])
    v = (p1w2[0] - p1w0[0], p1w2[1] - p1w0[1], p1w2[2] - p1w0[2])

    n = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

    ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
    un = (n[0] / ln, n[1] / ln, n[2] / ln)

    dunxy = math.sqrt(un[0] ** 2 + un[1] ** 2)
    maxd0 = 0
    if dunxy > 0:
        maxd0 = math.sqrt(p1w0[0] ** 2 + p1w0[1] ** 2) / math.sqrt(un[0] ** 2 + un[1] ** 2)

    pun0 = (
        p1w0[0] + un[0] * maxd0,
        p1w0[1] + un[1] * maxd0,
        p1w0[2] + un[2] * maxd0
    )

    vertices = [
        p1w0,
        (p1w0[0] + e, p1w0[1] + e, p1w0[2] + e),
        pun0,
        (pun0[0] + e, pun0[1] + e, pun0[2] + e),
    ]
    edges = []
    faces = [
        (0, 1, 3, 2),
    ]

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh
