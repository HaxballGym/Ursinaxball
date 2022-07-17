import numpy as np


def converter_array(x):
    return np.array(x, dtype=float)


def converter_array_none(x):
    return np.array(x, dtype=float) if x is not None else None
