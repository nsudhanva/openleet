"""Maximize Win From Two Segments with 2 * 10^4 sorted prizes (with repeats) and a window holding
about a tenth of them, so trying every pair of segments is 2 * 10^8 pairs."""

SEEDS = 2
N = 2 * 10**4
SPAN = 10**9


def generate(rng):
    positions = sorted(rng.randint(1, SPAN // 1000) * 1000 for _ in range(N))
    return {"prizePositions": positions, "k": rng.randint(SPAN // 12, SPAN // 8)}
