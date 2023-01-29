from typing import Tuple

import numpy as np
from numba import jit


@jit
def resolve_disc_disc_collision_fn(
    position_a: np.ndarray,
    position_b: np.ndarray,
    velocity_a: np.ndarray,
    velocity_b: np.ndarray,
    radius_a: float,
    radius_b: float,
    inverse_mass_a: float,
    inverse_mass_b: float,
    bouncing_a: float,
    bouncing_b: float,
) -> Tuple[Tuple[int]]:
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


@jit
def resolve_disc_vertex_collision_fn(
    position_disc: np.ndarray,
    position_vertex: np.ndarray,
    velocity: np.ndarray,
    radius: float,
    bouncing_disc: float,
    bouncing_vertex: float,
) -> Tuple[int]:
    dist = np.linalg.norm(position_disc - position_vertex)
    if 0 < dist <= radius:
        normal = (position_disc - position_vertex) / dist
        position_disc += normal * (radius - dist)
        normal_velocity = np.dot(velocity, normal)
        if normal_velocity < 0:
            bouncing_factor = -(1 + bouncing_disc * bouncing_vertex)
            velocity += normal * normal_velocity * bouncing_factor

    return (position_disc, velocity)


@jit
def resolve_disc_segment_collision_no_curve_fn(
    position_disc: np.ndarray,
    position_vertex_0: np.ndarray,
    position_vertex_1: np.ndarray,
) -> Tuple[float, np.ndarray]:
    normal_segment = position_vertex_1 - position_vertex_0
    normal_disc_v0 = position_disc - position_vertex_0
    normal_disc_v1 = position_disc - position_vertex_1
    if (
        np.dot(normal_segment, normal_disc_v0) > 0
        and np.dot(normal_segment, normal_disc_v1) < 0
    ):
        normal = [normal_segment[1], -normal_segment[0]] / np.linalg.norm(
            normal_segment
        )
        dist = np.dot(normal, normal_disc_v1)

        return dist, normal

    return None, None


@jit
def resolve_disc_segment_collision_curve_fn(
    position_disc: np.ndarray,
    circle_center: np.ndarray,
    circle_radius: float,
    circle_tangeant_0: np.ndarray,
    circle_tangeant_1: np.ndarray,
    curve: float,
) -> Tuple[float, np.ndarray]:
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

    return None, None


@jit
def resolve_disc_segment_final_fn(
    dist: float,
    normal: np.ndarray,
    position_disc: np.ndarray,
    velocity: np.ndarray,
    radius: float,
    bouncing_disc: float,
    bouncing_segment: float,
) -> Tuple[int]:
    if dist < radius:
        position_disc += normal * (radius - dist)
        normal_velocity = np.dot(velocity, normal)
        if normal_velocity < 0:
            bouncing_factor = -(1 + bouncing_disc * bouncing_segment)
            velocity += normal * normal_velocity * bouncing_factor

    return (position_disc, velocity)


@jit
def resolve_disc_plane_collision_fn(
    position_disc: np.ndarray,
    normal_plane: np.ndarray,
    velocity: np.ndarray,
    distance_plane: float,
    radius: float,
    bouncing_disc: float,
    bouncing_plane: float,
) -> Tuple[int]:
    norm_plane = normal_plane / np.linalg.norm(normal_plane)
    dist = distance_plane - np.dot(position_disc, norm_plane) + radius
    if dist > 0:
        position_disc += norm_plane * dist
        normal_velocity = np.dot(velocity, norm_plane)
        if normal_velocity < 0:
            bouncing_factor = -(1 + bouncing_disc * bouncing_plane)
            velocity += normal_plane * normal_velocity * bouncing_factor

    return (position_disc, velocity)
