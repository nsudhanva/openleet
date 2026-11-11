"""Partition Array into K Distinct Groups at the maximum 10^5 values, ~6 * 10^4 of them
distinct, with one value repeated exactly as often as there are groups (or once more) and kept
in the last part, so counting each value by a scan does ~6 * 10^9 comparisons."""

SEEDS = 2
N = 10**5
K = 50


def generate(rng):
    groups = N // K
    heavy = rng.randint(1, 10**5)
    count = groups + rng.randrange(2)
    rest = [rng.randint(1, 10**5) for _ in range(N - count)]
    rest = [x if x != heavy else heavy % 10**5 + 1 for x in rest]
    tail = rest[len(rest) - count :] + [heavy] * count
    rng.shuffle(tail)
    return {"nums": rest[: len(rest) - count] + tail, "k": K}
