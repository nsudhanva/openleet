"""Minimum Health to Beat Game at n = 5 * 10^4 levels over the full damage range: trying the
armor on each level and replaying the game is ~2.5 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    damage = [rng.randint(0, 10**5) for _ in range(N)]
    return {"damage": damage, "armor": rng.randint(0, 10**5)}
