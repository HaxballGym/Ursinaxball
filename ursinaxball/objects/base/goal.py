from __future__ import annotations

import msgspec
import numpy as np
import numpy.typing as npt

from ursinaxball.utils.enums import TeamID


class GoalRaw(msgspec.Struct, rename="camel"):
    p0: tuple[float, float]
    p1: tuple[float, float]
    team: str

    def to_goal(self) -> Goal:
        return Goal(
            p0=np.array(self.p0),
            p1=np.array(self.p1),
            team=TeamID[self.team.upper()],
        )


class Goal(msgspec.Struct, rename="camel"):
    p0: npt.NDArray[np.float64]
    p1: npt.NDArray[np.float64]
    team: TeamID
