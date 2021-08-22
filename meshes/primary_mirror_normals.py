import bpy
import math
from mathutils import Vector

from optics import hex2xyz

primary_mirror_normals_name = 'primary_mirror_normals'

def create_ray(f, r, x, y, z):
    # print('primary_mirror_normals')
    p1w0 = Vector(hex2xyz(f, r, x, y, z, 0))
    p1w1 = Vector(hex2xyz(f, r, x, y, z, 1))
    p1w2 = Vector(hex2xyz(f, r, x, y, z, 2))

    u = p1w1 - p1w0
    v = p1w2 - p1w0

    un = u.cross(v).normalized()
    dunxy = math.sqrt(un.x ** 2 + un.y ** 2)

    maxd0 = f if dunxy == 0 else math.sqrt(p1w0.x ** 2 + p1w0.y ** 2) / dunxy

    return [p1w0, p1w0 + un * maxd0]
