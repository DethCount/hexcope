import sys
import bpy
import math

n = 1 # max distance (in r unit)
# f = 2.0 # focal length

trig_name = 'tri'
r = 1.0 # hex side
h = 0.04 # hex thickness
f = 12.5 # focal length
fw = 0.05 * r # fixation half width
fd = 0.03 # fixation hole diameter
p = 25 # precision in parts of 1

trig_h = 0.1 # triangle walls height

# f : focal length
# d : parabola height
# r : distance from parabola center
def dist2z(f, r):
    return (r * r) / (4 * f)

# f : focal length
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
# w : hex triangle vertex index cw from center
def hex2xyz(f, x, y, z, w):
    ytheta = math.pi / 6
    x2 = x * (3 * r)
    ytemp = y * (math.sqrt(3) * r)
    x2 += ytemp * math.cos(ytheta)
    y2 = ytemp * math.sin(ytheta)

    points = []
    for i in range(0, 6):
        theta = i * math.pi / 3
        x3 = x2 + r * math.cos(theta)
        y3 = y2 + r * math.sin(theta)
        points.append((
            x3,
            y3,
            dist2z(f, math.sqrt(x3 * x3 + y3 * y3))
        ))

    if w != 0:
        return points[(z + (w - 1)) % 6]

    z2 = 0
    for i in range(0, 6):
        z2 += points[i][2]

    z2 /= 6

    return (x2, y2, z2)

def create_rays(f, x, y, z):
    mesh = bpy.data.meshes.new('rays_mesh' + str((f, x, y, z)))

    e = 0.05
    p0 = (10, 10, 10)
    lp0 = math.sqrt(p0[0] ** 2 + p0[1] ** 2 + p0[2] ** 2)

    p1w0 = hex2xyz(f, x, y, z, 0)
    p1w1 = hex2xyz(f, x, y, z, 1)
    p1w2 = hex2xyz(f, x, y, z, 2)

    u = (p1w1[0] - p1w0[0], p1w1[1] - p1w0[1], p1w1[2] - p1w0[2])
    v = (p1w2[0] - p1w0[0], p1w2[1] - p1w0[1], p1w2[2] - p1w0[2])

    n = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

    np = (
        v[1] * u[2] - v[2] * u[1],
        v[2] * u[0] - v[0] * u[2],
        v[0] * u[1] - v[1] * u[0]
    )

    ln = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
    un = (n[0] / ln, n[1] / ln, n[2] / ln)

    lnp = math.sqrt(np[0] ** 2 + np[1] ** 2 + np[2] ** 2)
    unp = (np[0] / lnp, np[1] / lnp, np[2] / lnp)

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

    p1n = (
        p1w0[0] + ureflected[0] * far,
        p1w0[1] + ureflected[1] * far,
        p1w0[2] + ureflected[2] * far
    )

    pun = (
        p1w0[0] + un[0] * far,
        p1w0[1] + un[1] * far,
        p1w0[2] + un[2] * far
    )

    punp = (
        p1w0[0] + unp[0] * far,
        p1w0[1] + unp[1] * far,
        p1w0[2] + unp[2] * far
    )

    print('p1n: ' + str(p1n))

    vertices = [
        p0,
        p1w0,
        pun,
        p1n,

        (p0[0] + e, p0[1] + e, p0[2] + e),
        (p1w0[0] + e, p1w0[1] + e, p1w0[2] + e),
        (pun[0] + e, pun[1] + e, pun[2] + e),
        (p1n[0] + e, p1n[1] + e, p1n[2] + e),
    ]
    edges = [
        (0, 1),
    ]
    faces = [
        (0, 1, 5, 4),
        (1, 2, 6, 5),
    ]

    nb_verts = len(vertices)
    p = 10
    czmax = far
    czstep = 10
    for cz in range(1, math.ceil(czmax / czstep) + 1):
        print('### ' + str(cz))
        print(str(len(vertices)))
        for i in range(0, p + 1):
            alpha = i * (2 * math.pi) / p
            idx = len(vertices)
            vertices.extend([
                (5 * r * math.cos(alpha), r * math.sin(alpha), cz * czstep)
            ])


            print(str(len(vertices)) + ' vs ' + str(idx))

            if i > 0:
                edges.extend([(idx - 1, idx)])
            if i == p:
                edges.extend([(idx, idx - p)])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh


# f : focal length
# t : triangle thickness
# h : walls height
# fw : fixation half width
# fd : fixation hole diameter
# p : precision in parts of 1
# x : cartesian (1, 0)
# y : cartesian (math.cos(math.pi/6), math.sin(math.pi/6))
# z : hex triangle index ccw
def create_triangle_mesh(f, t, h, fw, fd, p, x, y, z):
    mesh = bpy.data.meshes.new('trig_mesh' + str((f,t,x,y,z)))

    c = r * math.cos(math.pi / 3)
    s = r * math.sin(math.pi / 3)
    fr = 0.5 * fd

    vertices = []

    v0 = hex2xyz(f, x, y, z, 0)
    print(str((x, y, z, 0)) + ' ' + str(v0))

    v1 = hex2xyz(f, x, y, z, 1)
    print(str((x, y, z, 1)) + ' ' + str(v1))

    v2 = hex2xyz(f, x, y, z, 2)
    print(str((x, y, z, 2)) + ' ' + str(v2))

    vmid = (
        (v0[0] + v1[0] + v2[0]) / 3,
        (v0[1] + v1[1] + v2[1]) / 3,
        (v0[2] + v1[2] + v2[2]) / 3
    )

    vmid01 = (v0[0] + (v1[0] - v0[0]) / 2, v0[1] + (v1[1] - v0[1]) / 2, v0[2] + (v1[2] - v0[2]) / 2)
    vmid12 = (v1[0] + (v2[0] - v1[0]) / 2, v1[1] + (v2[1] - v1[1]) / 2, v1[2] + (v2[2] - v1[2]) / 2)
    vmid20 = (v2[0] + (v0[0] - v2[0]) / 2, v2[1] + (v0[1] - v2[1]) / 2, v2[2] + (v0[2] - v2[2]) / 2)

    dxvmid01mid = vmid[0] - vmid01[0]
    dyvmid01mid = vmid[1] - vmid01[1]
    dzvmid01mid = vmid[2] - vmid01[2]
    dvmid01mid = math.sqrt(dxvmid01mid * dxvmid01mid + dyvmid01mid * dyvmid01mid + dzvmid01mid * dzvmid01mid)
    vmid01mid = (dxvmid01mid / dvmid01mid, dyvmid01mid / dvmid01mid, dzvmid01mid / dvmid01mid)
    vmid12mid = ((vmid[0] - vmid12[0]) / dvmid01mid, (vmid[1] - vmid12[1]) / dvmid01mid, (vmid[2] - vmid12[2]) / dvmid01mid)
    vmid20mid = ((vmid[0] - vmid20[0]) / dvmid01mid, (vmid[1] - vmid20[1]) / dvmid01mid, (vmid[2] - vmid20[2]) / dvmid01mid)

    v01 = ((v1[0] - v0[0]) / r, (v1[1] - v0[1]) / r, (v1[2] - v0[2]) / r)
    v12 = ((v2[0] - v1[0]) / r, (v2[1] - v1[1]) / r, (v2[2] - v1[2]) / r)
    v20 = ((v0[0] - v2[0]) / r, (v0[1] - v2[1]) / r, (v0[2] - v2[2]) / r)

    ri = r * (math.sqrt(3) / 6) # rayon cercle inscrit

    vertices.extend([
        v0, v1, v2,

        (v0[0], v0[1], v0[2] - t),
        (v1[0], v1[1], v1[2] - t),
        (v2[0], v2[1], v2[2] - t),

        (v0[0], v0[1], v0[2] - t - h),
        (v1[0], v1[1], v1[2] - t - h),
        (v2[0], v2[1], v2[2] - t - h),

        (v0[0] + t * (vmid[0] - v0[0]) / ri, v0[1] + t * (vmid[1] - v0[1]) / ri, v0[2] - t - h + t * (vmid[2] - v0[2]) / ri),
        (v1[0] + t * (vmid[0] - v1[0]) / ri, v1[1] + t * (vmid[1] - v1[1]) / ri, v1[2] - t - h + t * (vmid[2] - v1[2]) / ri),
        (v2[0] + t * (vmid[0] - v2[0]) / ri, v2[1] + t * (vmid[1] - v2[1]) / ri, v2[2] - t - h + t * (vmid[2] - v2[2]) / ri),

        (v0[0] + t * (vmid[0] - v0[0]) / ri, v0[1] + t * (vmid[1] - v0[1]) / ri, v0[2] - t + t * (vmid[2] - v0[2]) / ri),
        (v1[0] + t * (vmid[0] - v1[0]) / ri, v1[1] + t * (vmid[1] - v1[1]) / ri, v1[2] - t + t * (vmid[2] - v1[2]) / ri),
        (v2[0] + t * (vmid[0] - v2[0]) / ri, v2[1] + t * (vmid[1] - v2[1]) / ri, v2[2] - t + t * (vmid[2] - v2[2]) / ri),

        (vmid01[0] + v01[0] * fw, vmid01[1] + v01[1] * fw, vmid01[2] + v01[2] * fw - t - h),
        (vmid01[0] - v01[0] * fw, vmid01[1] - v01[1] * fw, vmid01[2] - v01[2] * fw - t - h),

        (vmid01[0] + v01[0] * fw + vmid01mid[0] * t, vmid01[1] + v01[1] * fw + vmid01mid[1] * t, vmid01[2] + v01[2] * fw + vmid01mid[2] * t - t - h),
        (vmid01[0] - v01[0] * fw + vmid01mid[0] * t, vmid01[1] - v01[1] * fw + vmid01mid[1] * t, vmid01[2] - v01[2] * fw + vmid01mid[2] * t - t - h),

        (vmid01[0] + v01[0] * fw, vmid01[1] + v01[1] * fw, vmid01[2] + v01[2] * fw - t - h - 2 * fw),
        (vmid01[0] - v01[0] * fw, vmid01[1] - v01[1] * fw, vmid01[2] - v01[2] * fw - t - h - 2 * fw),

        (vmid01[0] + v01[0] * fw + vmid01mid[0] * t, vmid01[1] + v01[1] * fw + vmid01mid[1] * t, vmid01[2] + v01[2] * fw + vmid01mid[2] * t - t - h - 2 * fw),
        (vmid01[0] - v01[0] * fw + vmid01mid[0] * t, vmid01[1] - v01[1] * fw + vmid01mid[1] * t, vmid01[2] - v01[2] * fw + vmid01mid[2] * t - t - h - 2* fw),

        (vmid12[0] + v12[0] * fw, vmid12[1] + v12[1] * fw, vmid12[2] + v12[2] * fw - t - h),
        (vmid12[0] - v12[0] * fw, vmid12[1] - v12[1] * fw, vmid12[2] - v12[2] * fw - t - h),

        (vmid12[0] + v12[0] * fw + vmid12mid[0] * t, vmid12[1] + v12[1] * fw + vmid12mid[1] * t, vmid12[2] + v12[2] * fw + vmid12mid[2] * t - t - h),
        (vmid12[0] - v12[0] * fw + vmid12mid[0] * t, vmid12[1] - v12[1] * fw + vmid12mid[1] * t, vmid12[2] - v12[2] * fw + vmid12mid[2] * t - t - h),


        (vmid12[0] + v12[0] * fw, vmid12[1] + v12[1] * fw, vmid12[2] + v12[2] * fw - t - h - 2 * fw),
        (vmid12[0] - v12[0] * fw, vmid12[1] - v12[1] * fw, vmid12[2] - v12[2] * fw - t - h - 2 * fw),

        (vmid12[0] + v12[0] * fw + vmid12mid[0] * t, vmid12[1] + v12[1] * fw + vmid12mid[1] * t, vmid12[2] + v12[2] * fw + vmid12mid[2] * t - t - h - 2 * fw),
        (vmid12[0] - v12[0] * fw + vmid12mid[0] * t, vmid12[1] - v12[1] * fw + vmid12mid[1] * t, vmid12[2] - v12[2] * fw + vmid12mid[2] * t - t - h - 2* fw),

        (vmid20[0] + v20[0] * fw, vmid20[1] + v20[1] * fw, vmid20[2] + v20[2] * fw - t - h),
        (vmid20[0] - v20[0] * fw, vmid20[1] - v20[1] * fw, vmid20[2] - v20[2] * fw - t - h),

        (vmid20[0] + v20[0] * fw + vmid20mid[0] * t, vmid20[1] + v20[1] * fw + vmid20mid[1] * t, vmid20[2] + v20[2] * fw + vmid20mid[2] * t - t - h),
        (vmid20[0] - v20[0] * fw + vmid20mid[0] * t, vmid20[1] - v20[1] * fw + vmid20mid[1] * t, vmid20[2] - v20[2] * fw + vmid20mid[2] * t - t - h),


        (vmid20[0] + v20[0] * fw, vmid20[1] + v20[1] * fw, vmid20[2] + v20[2] * fw - t - h - 2 * fw),
        (vmid20[0] - v20[0] * fw, vmid20[1] - v20[1] * fw, vmid20[2] - v20[2] * fw - t - h - 2 * fw),

        (vmid20[0] + v20[0] * fw + vmid20mid[0] * t, vmid20[1] + v20[1] * fw + vmid20mid[1] * t, vmid20[2] + v20[2] * fw + vmid20mid[2] * t - t - h - 2 * fw),
        (vmid20[0] - v20[0] * fw + vmid20mid[0] * t, vmid20[1] - v20[1] * fw + vmid20mid[1] * t, vmid20[2] - v20[2] * fw + vmid20mid[2] * t - t - h - 2* fw),
    ])

    edges = [
        (0, 1), (1, 2), (2, 0),
        (3, 4), (4, 5), (5, 3),
        (0, 3), (1, 4), (2, 5),

        (6, 7), (7, 8), (8, 6),
        (3, 6), (4, 7), (5, 8),

        (9, 10), (10, 11), (11, 9),
        (6, 9), (7, 10), (8, 11),

        (12, 13), (13, 14), (14, 12),
        (9, 12), (10, 13), (11, 14),

        # 01
        (15, 17), (16, 18),
        (19, 20), (20, 22),(21, 19),(21, 22),
        (15, 19), (16, 20), (17, 21), (18, 22),

        # 12
        (23, 25), (24, 26),
        (27, 28), (28, 30),(29, 27),(29, 30),
        (23, 27), (24, 28), (25, 29), (26, 30),

        # 20
        (31, 33), (32, 34),
        (35, 36), (36, 38),(37, 35),(37, 38),
        (31, 35), (32, 36), (33, 37), (34, 38),
    ]
    faces = [
        (0, 1, 2),
        (3, 4, 1, 0), (4, 5, 2, 1),(5, 3, 0, 2),
        (6, 7, 4, 3), (7, 8, 5, 4), (8, 6, 3, 5),
        (9, 10, 7, 6), (10, 11, 8, 7), (11, 9, 6, 8),
        (10, 9, 12, 13), (11, 10, 13, 14), (11, 9, 12, 14),
        (12, 13, 14),
        (15, 16, 18, 17),
        (19, 21, 22, 20), (16, 18, 22, 20), (15, 17, 21, 19),
        (23, 24, 26, 25),
        (27, 29, 30, 28), (24, 26, 30, 28), (23, 25, 29, 27),
        (31, 32, 34, 33),
        (35, 37, 38, 36), (32, 34, 38, 36), (31, 33, 37, 35),
    ]

    trig_h = (math.sqrt(3) / 6) * r
    trig_ih = trig_h - t

    c01 = (vmid01[0], vmid01[1], vmid01[2] - t - h - fw)
    lc01 = math.sqrt(c01[0] ** 2 + c01[1] ** 2 + c01[2] ** 2)
    c01n = (c01[0] / lc01, c01[1] / lc01, c01[2] / lc01)

    c12 = (vmid12[0], vmid12[1], vmid12[2] - t - h - fw)
    lc12 = math.sqrt(c12[0] ** 2 + c12[1] ** 2 + c12[2] ** 2)
    c12n = (c12[0] / lc12, c12[1] / lc12, c12[2] / lc12)

    c20 = (vmid20[0], vmid20[1], vmid20[2] - t - h - fw)
    lc20 = math.sqrt(c20[0] ** 2 + c20[1] ** 2 + c20[2] ** 2)
    c20n = (c20[0] / lc20, c20[1] / lc20, c20[2] / lc20)

    ltemp = math.sqrt(vmid01mid[0] ** 2 + vmid01mid[1] ** 2)
    nu01 = (
        vmid01mid[1] * v01[2] - vmid01mid[2] * v01[1],
        vmid01mid[2] * v01[0] - vmid01mid[0] * v01[2],
        vmid01mid[0] * v01[1] - vmid01mid[1] * v01[0],
    )

    nu12 = (
        vmid12mid[1] * v12[2] - vmid12mid[2] * v12[1],
        vmid12mid[2] * v12[0] - vmid12mid[0] * v12[2],
        vmid12mid[0] * v12[1] - vmid12mid[1] * v12[0],
    )

    nu20 = (
        vmid20mid[1] * v20[2] - vmid20mid[2] * v20[1],
        vmid20mid[2] * v20[0] - vmid20mid[0] * v20[2],
        vmid20mid[0] * v20[1] - vmid20mid[1] * v20[0],
    )

    print('01 : n : ' + str(vmid01mid) + ' u: ' + str(v01) + ' n x u:' + str(nu01))
    print('12 : n : ' + str(vmid12mid) + ' u: ' + str(v12) + ' n x u:' + str(nu12))
    print('20 : n : ' + str(vmid20mid) + ' u: ' + str(v20) + ' n x u:' + str(nu20))

    nb_verts = len(vertices)
    vertices.extend([
        c01, (c01[0] + v01[0], c01[1] + v01[1], c01[2] + v01[2]), (c01[0] + nu01[0], c01[1] + nu01[1], c01[2] + nu01[2]), (c01[0] + vmid01mid[0], c01[1] + vmid01mid[1], c01[2] + vmid01mid[2]),
        c12, (c12[0] + v12[0], c12[1] + v12[1], c12[2] + v12[2]), (c12[0] + nu12[0], c12[1] + nu12[1], c12[2] + nu12[2]), (c12[0] + vmid12mid[0], c12[1] + vmid12mid[1], c12[2] + vmid12mid[2]),
        c20, (c20[0] + v20[0], c20[1] + v20[1], c20[2] + v20[2]), (c20[0] + nu20[0], c20[1] + nu20[1], c20[2] + nu20[2]), (c20[0] + vmid20mid[0], c20[1] + vmid20mid[1], c20[2] + vmid20mid[2]),
    ])

    edges.extend([
        #(nb_verts, nb_verts + 1), (nb_verts, nb_verts + 2), (nb_verts, nb_verts + 3),
        #(nb_verts + 4, nb_verts + 5), (nb_verts + 4, nb_verts + 6), (nb_verts + 4, nb_verts + 7),
        #(nb_verts + 8, nb_verts + 9), (nb_verts + 8, nb_verts + 10), (nb_verts + 8, nb_verts + 11),
    ])

    nb_verts = len(vertices)

    vfw0 = None
    vfw1 = None
    vfw2 = None
    vfw3 = None

    for i in range(0, p + 1):
        alpha = i * (2 * math.pi) / p

        rx01 = fr * math.cos(alpha) * v01[0] + fr * math.sin(alpha) * nu01[0]
        ry01 = fr * math.cos(alpha) * v01[1] + fr * math.sin(alpha) * nu01[1]
        rz01 = fr * math.cos(alpha) * v01[2] + fr * math.sin(alpha) * nu01[2]

        rx12 = fr * math.cos(alpha) * v12[0] + fr * math.sin(alpha) * nu12[0]
        ry12 = fr * math.cos(alpha) * v12[1] + fr * math.sin(alpha) * nu12[1]
        rz12 = fr * math.cos(alpha) * v12[2] + fr * math.sin(alpha) * nu12[2]

        rx20 = fr * math.cos(alpha) * v20[0] + fr * math.sin(alpha) * nu20[0]
        ry20 = fr * math.cos(alpha) * v20[1] + fr * math.sin(alpha) * nu20[1]
        rz20 = fr * math.cos(alpha) * v20[2] + fr * math.sin(alpha) * nu20[2]

        l01 = (
            c01[0] + rx01,
            c01[1] + ry01,
            c01[2] + rz01
        )

        r01 = (
            c01[0] + vmid01mid[0] * t + rx01,
            c01[1] + vmid01mid[1] * t + ry01,
            c01[2] + vmid01mid[2] * t + rz01
        )

        l12 = (
            c12[0] + rx12,
            c12[1] + ry12,
            c12[2] + rz12
        )

        r12 = (
            c12[0] + vmid12mid[0] * t + rx12,
            c12[1] + vmid12mid[1] * t + ry12,
            c12[2] + vmid12mid[2] * t + rz12
        )

        l20 = (
            c20[0] + rx20,
            c20[1] + ry20,
            c20[2] + rz20
        )

        r20 = (
            c20[0] + vmid20mid[0] * t + rx20,
            c20[1] + vmid20mid[1] * t + ry20,
            c20[2] + vmid20mid[2] * t + rz20
        )

        idx = nb_verts + i * 6

        vertices.extend([l01, r01, l12, r12, l20, r20])
        edges.extend([
            (idx, idx + 1),
            (idx + 2, idx + 3),
            (idx + 4, idx + 5),
        ])

        if i > 0:
            edges.extend([
                (idx - 6, idx),
                (idx - 5, idx + 1),
                (idx - 4, idx + 2),
                (idx - 3, idx + 3),
                (idx - 2, idx + 4),
                (idx - 1, idx + 5),
            ])

            faces.extend([
                (idx - 6, idx, idx + 1, idx - 5),
                (idx - 4, idx + 2, idx + 3, idx - 3),
                (idx - 2, idx + 4, idx + 5, idx - 1),
            ])

            if alpha < math.pi / 2:
                faces.extend([
                    (19, idx - 6, idx),
                    (21, idx - 5, idx + 1),
                    (27, idx - 4, idx + 2),
                    (29, idx - 3, idx + 3),
                    (35, idx - 2, idx + 4),
                    (37, idx - 1, idx + 5),
                ])
                if vfw0 == None:
                    vfw0 = idx - 6
            elif alpha < math.pi:
                faces.extend([
                    (20, idx - 6, idx),
                    (22, idx - 5, idx + 1),
                    (28, idx - 4, idx + 2),
                    (30, idx - 3, idx + 3),
                    (36, idx - 2, idx + 4),
                    (38, idx - 1, idx + 5),
                ])
                if vfw1 == None:
                    vfw1 = idx - 6
            elif alpha < 3 * (math.pi / 2):
                faces.extend([
                    (16, idx - 6, idx),
                    (18, idx - 5, idx + 1),
                    (24, idx - 4, idx + 2),
                    (26, idx - 3, idx + 3),
                    (32, idx - 2, idx + 4),
                    (34, idx - 1, idx + 5),
                ])
                if vfw2 == None:
                    vfw2 = idx - 6
            else:
                faces.extend([
                    (15, idx - 6, idx),
                    (17, idx - 5, idx + 1),
                    (23, idx - 4, idx + 2),
                    (25, idx - 3, idx + 3),
                    (31, idx - 2, idx + 4),
                    (33, idx - 1, idx + 5),
                ])
                if vfw3 == None:
                    vfw3 = idx - 6
    faces.extend([
        (19, vfw1, 20),
        (21, vfw1 + 1, 22),
        (27, vfw1 + 2, 28),
        (29, vfw1 + 3, 30),
        (35, vfw1 + 4, 36),
        (37, vfw1 + 5, 38),
        (20, vfw2, 16),
        (22, vfw2 + 1, 18),
        (28, vfw2 + 2, 24),
        (30, vfw2 + 3, 26),
        (36, vfw2 + 4, 32),
        (38, vfw2 + 5, 34),
        (16, vfw3, 15),
        (18, vfw3 + 1, 17),
        (24, vfw3 + 2, 23),
        (26, vfw3 + 3, 25),
        (32, vfw3 + 4, 31),
        (34, vfw3 + 5, 33),
        (15, vfw0, 19),
        (17, vfw0 + 1, 21),
        (23, vfw0 + 2, 27),
        (25, vfw0 + 3, 29),
        (31, vfw0 + 4, 35),
        (33, vfw0 + 5, 37),
    ])

    print(vfw1)

    # print('trig mesh' + str(vertices) + ' ' + str(edges) + ' ' + str(faces))

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh

hex_collection = bpy.data.collections.new('hex_collection')
bpy.context.scene.collection.children.link(hex_collection)

hex_arrows = [(0, 1), (-1, 2), (-1, 1), (0, -1), (1, -2), (1, -1)]
prev_hexes = [(0, 0)]
curr_hexes = []
hexes = prev_hexes

for i in range(0, n + 1):
    for j in range(0, len(prev_hexes)):
        for l in range(0, len(hex_arrows)):
            x = prev_hexes[j][0] + hex_arrows[l][0]
            y = prev_hexes[j][1] + hex_arrows[l][1]

            if (x, y) in hexes or (x, y) in curr_hexes:
                continue

            # print(str((x, y)) + ' not found')
            for z in range(0, 6):
                mesh = create_triangle_mesh(f, h, trig_h, fw, fd, p, x, y, z)

                # print('mesh created z: ' + str((x, y, z)) + str(mesh))
                triangle_object = bpy.data.objects.new(trig_name + '_0', mesh)
                hex_collection.objects.link(triangle_object)

            curr_hexes.append((x, y))
    prev_hexes = curr_hexes
    hexes.extend(curr_hexes)
    curr_hexes = []

ray_collection = bpy.data.collections.new('ray_collection')
bpy.context.scene.collection.children.link(ray_collection)

for i in range(0, len(hexes)):
        ray_mesh = create_rays(f, hexes[i][0], hexes[i][1], 0)
        ray_object = bpy.data.objects.new('ray_' + str(hexes[i][0]) + '_' + str(hexes[i][1]) + '_0', ray_mesh)
        ray_collection.objects.link(ray_object)

print('done')

# bpy.ops.export_mesh.stl(filepath="C:\\Users\\Count\\Documents\\projects\\hexcope\\stl\\support_", check_existing=True, filter_glob='*.stl', use_selection=False, global_scale=100.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OBJECT', axis_forward='Y', axis_up='Z')