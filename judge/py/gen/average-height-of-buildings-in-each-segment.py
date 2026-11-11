"""Average Height of Buildings: 5 * 10^4 buildings with heights 1..3 (equal-average segments
merge) or 3 * 10^4 with random heights, all over one shared point, so summing every building over
each segment, or the active heights at each of the ~10^5 events, is ~10^9 steps."""

SEEDS = 2
N = 5 * 10**4
END = 10**5


def generate(rng):
    n, top = (N, 3) if rng.random() < 0.5 else (N * 3 // 5, 10**5)
    mid = END // 2
    rand = rng.random
    return {
        "buildings": [
            [int(rand() * mid), mid + 1 + int(rand() * (END - mid)), 1 + int(rand() * top)]
            for _ in range(n)
        ]
    }
