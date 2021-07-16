import bpy
import math

from optics import spherical_z

secondary_mirror_spherical_name = 'secondary'

# t: thickness
# st: spider arm thickness
# sw: spider arm length
# f: secondary mirror focal length
# r: secondary mirror radius
# rp: circles precision
# arm_n: number of spider arms
def create_mesh(t, f, r, rp):
    mesh = bpy.data.meshes.new(
        secondary_mirror_spherical_name
        + '_' + str((t, f, r, rp))
    )

    vertices = []
    edges = []
    faces = []

    nb_verts = len(vertices)

    for sr in range(0, rp + 1):
        x = r - sr * r / rp
        z = spherical_z(f, r, x)

        for i in range(0, rp + 1):
            alpha = i * math.tau / rp

            nbidx = 2
            tv = nb_verts + sr * (rp + 1) * nbidx + nbidx * i
            bv = tv + 1
            utv = nb_verts + (sr - 1) * (rp + 1) * nbidx + nbidx * i
            ubv = utv + 1

            vertices.extend([
                (x * math.cos(alpha), x * math.sin(alpha), z + t),
                (x * math.cos(alpha), x * math.sin(alpha), z),
            ])

            if i > 0:
                edges.extend([
                    (tv, tv - nbidx),
                    (bv, bv - nbidx),
                ])

                if sr == 0:
                    faces.extend([
                        (tv, tv - nbidx, bv - nbidx, bv),
                    ])
                elif sr > 0:
                    faces.extend([
                        (tv, tv - nbidx, utv - nbidx, utv),
                        (bv - nbidx, bv, ubv, ubv - nbidx),
                    ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh