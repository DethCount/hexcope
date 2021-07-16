import bpy
import math

support_arm_name = 'arm'

# r: external radius
# t: thickness
# h: height
# rp: circles precision
# hp: number of inner circles
def create_mesh(
    r, t, h, rp, hp
):
    mesh = bpy.data.meshes.new(
        support_arm_name + '_' + str((r, t, h, rp, hp))
    )

    vertices = []
    edges = []
    faces = []

    hs = h / (hp + 1)
    ri = r - t

    nb_verts = len(vertices)

    for i in range(0, hp + 2):
        for j in range(0, rp + 1):
            alpha = j * math.tau / rp

            nbidx = 2

            trv = nb_verts + i * nbidx * (rp + 1) + j * nbidx
            trvi = trv + 1
            tlv = trv - nbidx
            tlvi = tlv + 1

            brv = trv - nbidx * (rp + 1)
            brvi = brv + 1
            blv = brv - nbidx
            blvi = blv + 1

            vertices.extend([
                (
                    r * math.cos(alpha),
                    r * math.sin(alpha),
                    hs * i
                ),
                (
                    ri * math.cos(alpha),
                    ri * math.sin(alpha),
                    hs * i
                ),
            ])

            if i == 0 or i == hp + 1:
                edges.extend([
                    #(trv, trvi),
                ])

                if j > 0:
                    if i == 0:
                        faces.extend([
                            (trvi, trv, tlv, tlvi),
                        ])
                    else:
                        faces.extend([
                            (trv, trvi, tlvi, tlv),
                        ])


            if j > 0 and i > 0:
                faces.extend([
                    (blv, brv, trv, tlv),
                    (brvi, blvi, tlvi, trvi),
                ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh