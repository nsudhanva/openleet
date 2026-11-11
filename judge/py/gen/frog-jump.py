"""Frog Jump with 2000 stones packed densely (0..1998, or 0..~2200 with random gaps) and a last
stone just out of reach or reachable only by speeding up the whole way, so a search that does
not remember (stone, jump) pairs explores exponentially many paths."""

from _shapes import pick_shape

SEEDS = 3
N = 2000


def generate(rng):
    shape = pick_shape(rng)
    if shape == 1:
        stones = [0, 1, *sorted(rng.sample(range(2, N * 11 // 10), N - 3))]
        stones.append(stones[-1] + 80)
    else:
        stones = [*range(N - 1), N - 2 + (64 if shape == 0 else 62)]
    return {"stones": stones}
