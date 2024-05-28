from typing import TYPE_CHECKING

import numpy as np

from ursinaxball.modules.physics.fn_base import (
    resolve_disc_disc_collision_fn,
    resolve_disc_plane_collision_fn,
    resolve_disc_segment_collision_curve_fn,
    resolve_disc_segment_collision_no_curve_fn,
    resolve_disc_segment_final_fn,
    resolve_disc_vertex_collision_fn,
)
from ursinaxball.objects import Stadium
from ursinaxball.objects.base import Disc, Plane, Segment, Vertex

if TYPE_CHECKING:
    from ursinaxball.modules import PlayerHandler


def resolve_disc_disc_collision(disc_a: Disc, disc_b: Disc) -> None:
    """
    Resolves the collision between two discs
    """
    disc_a_res, disc_b_res = resolve_disc_disc_collision_fn(
        disc_a.position,
        disc_b.position,
        disc_a.speed,
        disc_b.speed,
        disc_a.radius,
        disc_b.radius,
        disc_a.inv_mass,
        disc_b.inv_mass,
        disc_a.b_coef,
        disc_b.b_coef,
    )
    disc_a.position = disc_a_res[0]
    disc_a.speed = disc_a_res[1]
    disc_b.position = disc_b_res[0]
    disc_b.speed = disc_b_res[1]


def resolve_disc_vertex_collision(disc: Disc, vertex: Vertex) -> None:
    """
    Resolves the collision between a disc and a vertex
    """
    disc_res = resolve_disc_vertex_collision_fn(
        disc.position,
        vertex.position,
        disc.speed,
        disc.radius,
        disc.b_coef,
        vertex.b_coef,
    )
    disc.position = disc_res[0]
    disc.speed = disc_res[1]


def segment_apply_bias(
    segment: Segment, dist: float, normal: np.ndarray
) -> tuple[float, np.ndarray]:
    """
    Applies the bias property during the collision between a segment and a disc
    """
    bias_segment = segment.bias
    if bias_segment == 0:
        if dist < 0:
            dist = -dist
            normal = -normal
    elif bias_segment < 0:
        bias_segment = -bias_segment
        dist = -dist
        normal = -normal

    if dist < -bias_segment:
        return np.inf, normal

    return dist, normal


def resolve_disc_segment_collision_no_curve(
    disc: Disc, segment: Segment
) -> tuple[float, np.ndarray] | tuple[None, None]:
    res = resolve_disc_segment_collision_no_curve_fn(
        disc.position,
        segment.vertices[0].position,
        segment.vertices[1].position,
    )

    return res


def resolve_disc_segment_collision_curve(
    disc: Disc, segment: Segment
) -> tuple[float, np.ndarray] | tuple[None, None]:
    res = resolve_disc_segment_collision_curve_fn(
        disc.position,
        segment.circle_center,
        segment.circle_radius,
        segment.circle_tangeant[0],
        segment.circle_tangeant[1],
        segment.curve,
    )
    return res


def resolve_disc_segment_collision(disc: Disc, segment: Segment) -> None:
    """
    Resolves the collision between a disc and a segment
    """
    if segment.curve == 0:
        dist, normal = resolve_disc_segment_collision_no_curve(disc, segment)
    else:
        dist, normal = resolve_disc_segment_collision_curve(disc, segment)

    if dist is not None and normal is not None:
        dist, normal = segment_apply_bias(segment, dist, normal)
        res = resolve_disc_segment_final_fn(
            dist,
            normal,
            disc.position,
            disc.speed,
            disc.radius,
            disc.b_coef,
            segment.bouncing_coefficient,
        )
        disc.position = res[0]
        disc.speed = res[1]


def resolve_disc_plane_collision(disc: Disc, plane: Plane) -> None:
    """
    Resolves the collision between a disc and a plane
    """
    disc_res = resolve_disc_plane_collision_fn(
        disc.position,
        plane.normal,
        disc.speed,
        plane.dist,
        disc.radius,
        disc.b_coef,
        plane.b_coef,
    )
    disc.position = disc_res[0]
    disc.speed = disc_res[1]


def resolve_collisions(stadium_game: Stadium) -> None:
    """
    Function that resolves the collisions between the discs and the other objects
    """
    for i, d_a in enumerate(stadium_game.discs):
        for j in range(i + 1, len(stadium_game.discs)):
            d_b = stadium_game.discs[j]
            if ((d_a.c_group & d_b.c_mask) != 0) and ((d_a.c_mask & d_b.c_group) != 0):
                resolve_disc_disc_collision(d_a, d_b)
        if d_a.inv_mass != 0:
            for p in stadium_game.planes:
                if ((d_a.c_group & p.c_mask) != 0) and ((d_a.c_mask & p.c_group) != 0):
                    resolve_disc_plane_collision(d_a, p)
            for s in stadium_game.segments:
                if ((d_a.c_group & s.c_mask) != 0) and ((d_a.c_mask & s.c_group) != 0):
                    resolve_disc_segment_collision(d_a, s)
            for v in stadium_game.vertices:
                if ((d_a.c_group & v.c_mask) != 0) and ((d_a.c_mask & v.c_group) != 0):
                    resolve_disc_vertex_collision(d_a, v)


def update_discs(stadium_game: Stadium, players: "list[PlayerHandler]") -> None:
    """
    Function that updates the position and velocity of the discs
    """
    for disc in stadium_game.discs:
        if hasattr(disc, "player_id"):
            continue
        disc.position += disc.speed
        disc.speed = (disc.speed + disc.gravity) * disc.damping

    for player in players:
        disc = player.disc
        disc.position += disc.speed
        damping = disc.kicking_damping if player.is_kicking() else disc.damping
        disc.speed = (disc.speed + disc.gravity) * damping
