import bpy
import bmesh
import math
from mathutils import Matrix, Vector
from meshes import screw

support_arm_head_name = 'arm_head_'
support_arm_head_screw_in_name = 'arm_head_screw_in'

# e: margin
# t: head thickness arround arms
# h: head height
# arm_d: distance between arms
# arm_r: arm radius
# arm_rp: arm circles precision
# spider_thickness: spider leg thickness
# spider_length: spider leg length
def create_mesh(
    t, p,
    arm_dist, arm_rp, arm_outer_r, arm_inner_r, arm_screw_length, arm_D, arm_P,
    spider_r, spider_screw_length, spider_D, spider_P
):
    hw = 0.5 * arm_dist
    p1 = p + 1 if p % 2 == 0 else p
    base_circle_r = arm_outer_r + t
    total_h = 2 * t + arm_screw_length

    arm_hole_p = arm_rp + (4 - arm_rp % 4)
    arm_hole_cuts = 0.25 * (arm_hole_p - 4)

    bm = bmesh.new()

    square_size = arm_outer_r + t
    circle_radius = arm_inner_r

    bmesh.ops.create_grid(
        bm,
        x_segments=2,
        y_segments=2,
        size=square_size,
    )

    bm.faces.remove(bm.faces[:].pop())
    bmesh.ops.subdivide_edges(
        bm,
        edges=bm.edges,
        cuts=arm_hole_cuts,
        )

    left_base_verts = list(
        v
        for v in bm.verts
        if v.co.y < 0
    )

    base_edges = list(set(
        edg
        for v in bm.verts
        for edg in v.link_edges
    ))

    bmesh.ops.create_circle(
        bm,
        segments=4 * (arm_hole_cuts + 1),
        radius=circle_radius,
        )

    bmesh.ops.bridge_loops(bm, edges=bm.edges)

    top = bmesh.ops.extrude_edge_only(
        bm,
        edges = base_edges
    )

    top_verts = set()
    left_top_verts = set()
    top_edges = set()
    for geom in top['geom']:
        if isinstance(geom, bmesh.types.BMVert):
            top_verts.add(geom)
            if geom.co.y < 0:
                left_top_verts.add(geom)
                print('added', str(geom))
        if isinstance(geom, bmesh.types.BMEdge) and geom.is_boundary:
            top_edges.add(geom)

    to_dissolve_edges = set()
    for edg in bm.edges:
        print('edg comp', str(edg.verts[0].co), str(edg.verts[1].co), str(edg.verts[0].co.x == edg.verts[1].co.x), str(edg.verts[0].co.y == edg.verts[1].co.y))
        if edg.verts[0].co.x == edg.verts[1].co.x \
            and edg.verts[0].co.y == edg.verts[1].co.y:
            print('edg added', str(edg))
            to_dissolve_edges.add(edg)
            top_verts.discard(edg.verts[0])
            print('removed 0', str(edg.verts[0]))
            top_verts.discard(edg.verts[1])
            print('removed 1', str(edg.verts[1]))
            left_top_verts.discard(edg.verts[0])
            left_top_verts.discard(edg.verts[1])

    top_verts = list(top_verts)
    left_top_verts = list(left_top_verts)
    top_edges = list(top_edges)
    to_dissolve_edges = list(to_dissolve_edges)

    bmesh.ops.translate(
        bm,
        vec = (0, 0, total_h),
        verts = top_verts
    )

    ret = bmesh.ops.subdivide_edges(
        bm,
        edges = to_dissolve_edges
    )

    bmesh.ops.delete(
        bm,
        geom = ret['geom_inner'],
        context = 'VERTS'
    )

    bmesh.ops.edgeloop_fill(
        bm,
        edges = top_edges
    )

    ret = screw.screw_in(
        arm_inner_r,
        arm_screw_length,
        arm_hole_p,
        bm = bm,
        z_start = 0,
        z_scale = -1,
        fill_end=True,
        D=arm_D,
        P=arm_P,
        start_h=0,
        end_h=0.5 * t
    )

    bmesh.ops.translate(
        bm,
        vec = (0, hw, 0),
        verts = bm.verts
    )

    bmesh.ops.translate(
        bm,
        vec = (0, -hw + square_size, 0),
        verts = left_top_verts + left_base_verts
    )



    print(str(hw))
    bevel_edges = set()
    for v in bm.verts:
        print(str(v.co))
        if v.co.y >= hw:
            for edg in v.link_edges:
                #if edg.is_boundary:
                dv = edg.verts[1].co - edg.verts[0].co
                if dv.cross(Vector((0, 0, 1))).length == 0:
                    bevel_edges.add(edg)
    bevel_edges = list(bevel_edges)

    print(str(bevel_edges))


    bmesh.ops.bevel(
        bm,
        geom=bevel_edges,
        loop_slide=True,
        profile=0.5, # round
        offset=arm_outer_r + t,
        segments=p
    )

    # create half circle
    # base_grid_verts = bmesh.ops.create_grid(
    #     bm,
    #     x_segments = 2,
    #     y_segments = 2,
    #     size = arm_outer_r + t
    # )['verts']
    # bm.faces.remove(bm.faces[:].pop())
    # bmesh.ops.subdivide_edges(
    #     bm,
    #     edges=bm.edges,
    #     cuts=arm_hole_cuts,
    #     )

    # bmesh.ops.bridge_loops(bm, edges = bm.edges)

    # base_flat_edges = list([
    #     bm.edges.new((base_flat_top_left_vert, base_flat_bottom_left_vert)),
    #     bm.edges.new((base_flat_top_right_vert, base_flat_middle_right_vert)),
    #     bm.edges.new((base_flat_middle_right_vert, base_flat_bottom_right_vert)),
    #     bm.edges.new((base_flat_top_left_vert, base_flat_top_right_vert)),
    #     bm.edges.new((base_flat_bottom_left_vert, base_flat_bottom_right_vert)),
    # ])

    # bmesh.ops.holes_fill(
    #     bm,
    #     edges = base_circle_left_edges
    #         + base_flat_edges
    # )

    # # bm.edges.remove(base_flat_edges[1])

    # # translate 0.5 * arm_dist
    # bmesh.ops.translate(
    #     bm,
    #     verts = base_circle_verts,
    #     vec = (0, 0.5 * arm_dist, 0),
    # )

    # # extrude
    # ret = bmesh.ops.extrude_edge_only(
    #     bm,
    #     edges = bm.edges
    # )

    # top_edges = list(set(
    #     geom
    #     for geom in ret['geom']
    #     if isinstance(geom, bmesh.types.BMEdge)
    # ))

    # bmesh.ops.holes_fill(
    #     bm,
    #     edges = top_edges
    # )

    # # top_faces = list(set(
    # #     face
    # #     for edg in top_edges
    # #     for face in edg.link_faces
    # #     if face.normal.cross(Vector((0, 0, 1))).length == 0 # normal in z direction
    # # ))

    # # translate 2 * t + arm_screw_length
    # bmesh.ops.translate(
    #     bm,
    #     verts = list(
    #         geom
    #         for geom in ret['geom']
    #         if isinstance(geom, bmesh.types.BMVert)
    #     ),
    #     vec = (0, 0, total_h)
    # )

    # bmesh.ops.translate(
    #     bm,
    #     verts = bm.verts[:],
    #     vec = (0, -0.5 * arm_dist, 0)
    # )


    # bmesh.ops.translate(
    #     bm,
    #     verts = bm.verts[:],
    #     vec = (0, 0.5 * arm_dist, 0)
    # )

    # # screw_in arms with r = arm_r, z_start = t

    # # bmesh.ops.bridge_loops(
    # #     bm,
    # #     edges = base_circle_edges
    # #         + base_left_flat_edges
    # #         + ret[2]
    # # )

    # mirror x
    ret = bmesh.ops.mirror(
        bm,
        geom = bm.faces[:] + bm.verts[:] + bm.edges[:],
        axis = 'Y'
    )

    # bmesh.ops.reverse_faces(
    #     bm,
    #     faces = list(set(
    #         face
    #         for geom in ret['geom']
    #         if isinstance(geom, bmesh.types.BMEdge)
    #         for face in geom.link_faces
    #     ))
    # )

    # screw_in front face
    # screw back face

    mesh = bpy.data.meshes.new(support_arm_head_name + str((
        t, p,
        arm_dist, arm_rp, arm_outer_r, arm_inner_r, arm_screw_length, arm_D, arm_P,
        spider_r, spider_screw_length, spider_D, spider_P
    )))

    bm.to_mesh(mesh)

    return mesh