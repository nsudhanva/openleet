"""Matchsticks to Square with 15 sticks whose total is a multiple of 4: a solvable square cut
side by side, or an unsolvable set (odd side length but only two odd sticks) that still
passes the sum and max-stick checks, so backtracking must exhaust the search."""

SEEDS = 3


def generate(rng):
    if rng.random() < 0.5:
        side = rng.randint(10**6, 10**8)
        sticks = []
        for count in [4, 4, 4, 3]:
            cuts = sorted(rng.sample(range(1, side), count - 1))
            sticks.extend(b - a for a, b in zip([0, *cuts], [*cuts, side], strict=False))
        rng.shuffle(sticks)
        return {"matchsticks": sticks}
    # Each side of odd length needs an odd number of odd sticks, so four sides need at least
    # four odd sticks; with exactly two the answer is false.
    side = rng.randrange(10**6, 10**7) * 2 + 1
    evens = [2 * rng.randint(side // 8, side // 7) for _ in range(13)]
    rest = 4 * side - sum(evens)
    first = rng.randrange(1, rest, 2)
    sticks = [*evens, first, rest - first]
    rng.shuffle(sticks)
    return {"matchsticks": sticks}
