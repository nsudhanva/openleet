"""K Empty Slots at n = 2 * 10^4: a grid of spacing m ~ n / 4 lit first, then offset 1, 2, ... in
every cell with k = 2m - 1 (answer -1), mirrored on one seed, or two lit runs closing in from both
ends (answer day n - k), so rescanning bulbs or walking each k-gap costs ~5 * 10^7 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        # The gap between the runs shrinks by one each day, so it is first k on day n - k.
        lo, hi, bulbs = 1, N, []
        while lo <= hi:
            if rng.random() < 0.5:
                bulbs.append(lo)
                lo += 1
            else:
                bulbs.append(hi)
                hi -= 1
        return {"bulbs": bulbs, "k": rng.randint(1, 20)}
    # Every pair at distance k + 1 = 2m straddles a lit grid point, and the gap after the left
    # bulb (before the right one, when mirrored) stays empty up to the next grid point.
    m = N // 4 + rng.randint(-(N // 200), N // 200)
    bulbs = [p for o in range(m) for p in range(1 + o, N + 1, m)]
    if shape == 1:
        bulbs = [N + 1 - p for p in bulbs]
    return {"bulbs": bulbs, "k": 2 * m - 1}
