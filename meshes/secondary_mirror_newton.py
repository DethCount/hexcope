import bpy
import math

secondary_mirror_newton_name = 'newton_secondary'

# t: thickness
# rx: secondary mirror radius along x in secondary mirror plane
# ry: secondary mirror radius along y in secondary mirror plane
# rp: circles precision
def create_mesh(t, rx, ry, rp):
    mesh = bpy.data.meshes.new(
        secondary_mirror_newton_name
        + '_' + str((t, rx, ry, rp))
    )

    pi4m = -math.pi / 4
    cpi4m = math.cos(pi4m)
    spi4m = math.sin(pi4m)

    vertices = [
        (0, 0, t),
        (0, 0, 0),
    ]
    edges = []
    faces = []

    nb_verts = len(vertices)

    for i in range(0, rp + 1):
        alpha = i * math.tau / rp

        x = rx * math.cos(alpha)
        y = ry * math.sin(alpha)

        xi = (rx - t) * math.cos(alpha)
        yi = (ry - t) * math.sin(alpha)

        z = 0

        nbidx = 5
        trv = nb_verts + nbidx * i
        brv = trv + 1
        rrv = trv + 2
        ritrv = trv + 3
        ribrv = trv + 4
        tlv = trv - nbidx
        blv = brv - nbidx
        rlv = rrv - nbidx
        ritlv = ritrv - nbidx
        riblv = ribrv - nbidx

        vertices.extend([
            (
                x * cpi4m + z * spi4m,
                y,
                x * -spi4m + z * cpi4m + t
            ),
            (x * cpi4m + z * spi4m, y, x * -spi4m + z * cpi4m),
            (x * cpi4m + z * spi4m, y, rx * cpi4m + t),
            (xi * cpi4m + z * spi4m, yi, rx * cpi4m + t),
            (
                xi * cpi4m + z * spi4m,
                yi,
                xi * -spi4m + z * cpi4m + t
            ),
        ])

        edges.extend([
            (trv, brv),
            (trv, rrv),
            (ritrv, ribrv),
        ])

        if i > 0:
            edges.extend([
                (trv, tlv),
                (brv, blv),
                (rrv, rlv),
                (ritrv, ritlv),
                (ribrv, riblv),
            ])

            faces.extend([
                (trv, tlv, blv, brv),
                (1, brv, blv),
                (trv, rrv, rlv, tlv),
                (rrv, ritrv, ritlv, rlv),
                (ritrv, ritlv, riblv, ribrv),
                (0, ribrv, riblv),
            ])

    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh