"""Avoid Flood in the City at ~10^5 days and 33,333 lakes, every dry day forced to one lake (a
unique answer): each lake rained on then a dry day, then the second rains in reverse or in the
same order, or all first rains then a dry day before each second rain, so scanning dry days from
either end, or forward from the lake's last rain, is quadratic."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    lakes = rng.sample(range(1, 10**9 + 1), N // 3)
    if shape == 2:
        rains = lakes[:]
        for lake in lakes:
            rains += [0, lake]
        return {"rains": rains}
    rains = []
    for lake in lakes:
        rains += [lake, 0]
    return {"rains": rains + (lakes[::-1] if shape == 0 else lakes)}
