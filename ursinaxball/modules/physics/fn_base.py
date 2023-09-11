import numpy as np
import numpy.typing as npt


def resolve_disc_disc_collision_fn(
    position_a: npt.NDArray[np.float64],
    position_b: npt.NDArray[np.float64],
    velocity_a: npt.NDArray[np.float64],
    velocity_b: npt.NDArray[np.float64],
    radius_a: float,
    radius_b: float,
    inverse_mass_a: float,
    inverse_mass_b: float,
    bouncing_a: float,
    bouncing_b: float,
):
    dist = np.linalg.norm(position_a - position_b)
    radius_sum = radius_a + radius_b
    if 0 < dist <= radius_sum:
        normal = (position_a - position_b) / dist
        mass_factor = inverse_mass_a / (inverse_mass_a + inverse_mass_b)
        position_a += normal * (radius_sum - dist) * mass_factor
        position_b -= normal * (radius_sum - dist) * (1 - mass_factor)
        relative_velocity = velocity_a - velocity_b
        normal_velocity = np.dot(relative_velocity, normal)
        if normal_velocity < 0:
            bouncing_factor = -(1 + bouncing_a * bouncing_b)
            velocity_a += normal * normal_velocity * bouncing_factor * mass_factor
            velocity_b -= normal * normal_velocity * bouncing_factor * (1 - mass_factor)

    return ((position_a, velocity_a), (position_b, velocity_b))


def resolve_disc_vertex_collision_fn(
    position_disc: npt.NDArray[np.float64],
    position_vertex: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    radius: float,
    bouncing_disc: float,
    bouncing_vertex: float,
):
    dist = np.linalg.norm(position_disc - position_vertex)
    if 0 < dist <= radius:
        normal = (position_disc - position_vertex) / dist
        position_disc += normal * (radius - dist)
        normal_velocity = np.dot(velocity, normal)
        if normal_velocity < 0:
            bouncing_factor = -(1 + bouncing_disc * bouncing_vertex)
            velocity += normal * normal_velocity * bouncing_factor

    return (position_disc, velocity)


def resolve_disc_segment_collision_no_curve_fn(
    position_disc: npt.NDArray[np.float64],
    position_vertex_0: npt.NDArray[np.float64],
    position_vertex_1: npt.NDArray[np.float64],
):
    normal_segment = position_vertex_1 - position_vertex_0
    normal_disc_v0 = position_disc - position_vertex_0
    normal_disc_v1 = position_disc - position_vertex_1
    if (
        np.dot(normal_segment, normal_disc_v0) > 0
        and np.dot(normal_segment, normal_disc_v1) < 0
    ):
        normal = np.array([-normal_segment[1], normal_segment[0]]) / np.linalg.norm(
            normal_segment
        )
        dist = np.dot(normal, normal_disc_v1)

        return dist, normal

    return None, None


def resolve_disc_segment_collision_curve_fn(
    position_disc: npt.NDArray[np.float64],
    circle_center: npt.NDArray[np.float64],
    circle_radius: float,
    circle_tangeant_0: npt.NDArray[np.float64],
    circle_tangeant_1: npt.NDArray[np.float64],
    curve: float,
):
    dist, normal = None, None
    normal_circle = position_disc - circle_center
    if (
        np.dot(normal_circle, circle_tangeant_0) > 0
        and np.dot(normal_circle, circle_tangeant_1) > 0
    ) != (curve < 0):
        dist_norm = np.linalg.norm(normal_circle)
        if dist_norm > 0:
            dist = dist_norm - circle_radius
            normal = normal_circle / dist_norm

    return dist, normal


def resolve_disc_segment_final_fn(
    dist: float,
    normal: npt.NDArray[np.float64],
    position_disc: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    radius: float,
    bouncing_disc: float,
    bouncing_segment: float,
):
    if dist < radius:
        position_disc += normal * (radius - dist)
        normal_velocity = np.dot(velocity, normal)
        if normal_velocity < 0:
            bouncing_factor = -(1 + bouncing_disc * bouncing_segment)
            velocity += normal * normal_velocity * bouncing_factor

    return (position_disc, velocity)


def resolve_disc_plane_collision_fn(
    position_disc: npt.NDArray[np.float64],
    normal_plane: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    distance_plane: float,
    radius: float,
    bouncing_disc: float,
    bouncing_plane: float,
):
    norm_plane = normal_plane / np.linalg.norm(normal_plane)
    dist = distance_plane - np.dot(position_disc, norm_plane) + radius
    if dist > 0:
        position_disc += norm_plane * dist
        normal_velocity = np.dot(velocity, norm_plane)
        if normal_velocity < 0:
            bouncing_factor = -(1 + bouncing_disc * bouncing_plane)
            velocity += normal_plane * normal_velocity * bouncing_factor

    return (position_disc, velocity)
