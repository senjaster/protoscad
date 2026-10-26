# mypy: ignore-errors
# ruff: noqa

import trimesh
from manifold3d import Manifold as m3d


# Helper to convert a Manifold into a Trimesh
def manifold2trimesh(manifold):
    mesh = manifold.to_mesh()

    if mesh.vert_properties.shape[1] > 3:
        vertices = mesh.vert_properties[:, :3]
        colors = (mesh.vert_properties[:, 3:] * 255).astype(np.uint8)
    else:
        vertices = mesh.vert_properties
        colors = None

    return trimesh.Trimesh(vertices=vertices, faces=mesh.tri_verts, vertex_colors=colors)


def main():
    m3d.extrude()
    m3d.cube
    cube = m3d.cylinder(radius_low=0.1, radius_high=0.3, height=2, circular_segments=50)
    cube = cube.minkowski_sum(m3d.sphere(0.5, 200))
    print(cube.volume())
    mesh = manifold2trimesh(cube)

    trimesh.exchange.export.export_mesh(mesh, "cube4.stl", "stl")


if __name__ == "__main__":
    main()
