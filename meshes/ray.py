import bpy
from mathutils import Vector

ray_name = 'ray'

def create_mesh(start, end, thickness):
    ht = 0.5 * thickness
    htv = Vector((ht, ht, ht))

    vertices = [
        start - htv,
        start + htv,
        end - htv,
        end + htv
    ]

    edges = [(0, 1)]

    faces = [(0, 1, 3, 2)]

    mesh = bpy.data.meshes.new(ray_name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    return mesh
