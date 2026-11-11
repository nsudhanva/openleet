"""Last Moment Before All Ants Fall Out of a Plank at n = 10^4 with an ant on nearly every
position (a random band near each end left empty), so simulating the collisions tick by tick
costs ~10^8 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    # The empty bands make the answer depend on the data instead of always being n.
    a = rng.randint(1, N // 10)
    b = rng.randint(1, N // 10)
    left, right = [], []
    for x in range(a, N - b + 1):
        (left if rng.random() < 0.5 else right).append(x)
    rng.shuffle(left)
    rng.shuffle(right)
    return {"n": N, "left": left, "right": right}
