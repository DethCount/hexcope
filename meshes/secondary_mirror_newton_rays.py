import math
from mathutils import Vector

def create_ray(
    start, end,
    h, t, top_t, rx, ry
):
    if start.x != 0 or start.y != 0:
        return None

    un = (end - start).normalized()

    k = 0 if un.z == 0 else h / un.z

    z = h - 0.5 * top_t - rx * math.cos(-0.25 * math.pi) - t

    print('end_z', str(end.z))

    return [Vector((0, 0, z)), Vector((abs(h - end.z), 0, z))]