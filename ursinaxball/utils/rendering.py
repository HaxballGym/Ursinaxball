from numpy import cos, sin


def arc(
    x: float,
    y: float,
    radius: float,
    start_angle: float,
    end_angle: float,
    clockwise=True,
    segments=16,
) -> list[tuple[float, float]]:
    points = []
    for i in range(segments + 1):
        angle = start_angle + (end_angle - start_angle) * i / segments
        x_pos = x + radius * cos(angle)
        y_pos = y + radius * sin(angle)
        points.append((x_pos, y_pos))
    if clockwise:
        return points[::-1]
    else:
        return points
