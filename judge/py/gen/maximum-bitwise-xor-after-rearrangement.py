"""Maximum Bitwise XOR After Rearrangement at n = 2 * 10^5 (the maximum) where s is mostly ones
and t's zeros all sit at its end, so searching the rest of t for each position's best bit is
~4 * 10^10 steps."""

SEEDS = 2
N = 2 * 10**5


def generate(rng):
    s = "".join("0" if rng.random() < 0.05 else "1" for _ in range(N))
    zeros = rng.randint(N // 3, 2 * N // 3)
    return {"s": s, "t": "1" * (N - zeros) + "0" * zeros}
