"""Movement of Robots at n = 2 * 10^4 robots at distinct random positions with random directions,
so summing the distance of every pair after the move is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 2 * 10**9


def generate(rng):
    nums = rng.sample(range(-LIMIT, LIMIT + 1), N)
    s = "".join(rng.choice("LR") for _ in range(N))
    return {"nums": nums, "s": s, "d": rng.randint(0, 10**9)}
