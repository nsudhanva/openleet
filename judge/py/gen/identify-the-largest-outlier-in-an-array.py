"""Identify the Largest Outlier at n = 10^5 where the only valid outlier is the smallest element
(specials are multiples of 8, the outlier is 4 mod 8), so pairing every outlier candidate with
every sum candidate costs ~10^10 checks."""

SEEDS = 2
N = 100000


def generate(rng):
    # Specials lie in [-984, 1000]; their total is pulled into range so it can be an element.
    special = [8 * rng.randint(-123, 125) for _ in range(N - 2)]
    excess = sum(special) - 8 * rng.randint(-60, 60)
    i = 0
    while excess:
        x = special[i]
        step = max(min(excess, x + 984), x - 1000)
        special[i] = x - step
        excess -= step
        i = (i + 1) % (N - 2)
    # Every other candidate x leaves (s - x) / 2 equal to 2 mod 4, which is never present.
    nums = [*special, sum(special), -996 + 8 * rng.randint(0, 1)]
    rng.shuffle(nums)
    return {"nums": nums}
