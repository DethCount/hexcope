from mathutils import Vector

def create_ray(
    start, end,
    z, r, f
):
    return [
        end,
        end + Vector((0, 0, -1)) * f
    ]