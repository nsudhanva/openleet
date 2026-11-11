"""Widest Possible Fence at 500 planks: 120 pairs summing to one height among random heights up
to 10^9, so ~1.25 * 10^5 candidate heights each counted over all 500 planks is ~6 * 10^7
steps."""

SEEDS = 2
N = 500
PAIRS = 120
TOP = 10**9


def generate(rng):
    height = rng.randint(TOP // 2, TOP)
    planks = []
    for _ in range(PAIRS):
        x = rng.randint(1, height - 1)
        planks += [x, height - x]
    planks += [rng.randint(1, TOP) for _ in range(N - len(planks))]
    rng.shuffle(planks)
    return {"planks": planks}
