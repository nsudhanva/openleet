"""Maximum Manhattan Distance After K Changes at length 10^5 (the maximum) of random moves with a
small k, so recounting the moves of every prefix is 5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {"s": "".join(rng.choice("NSEW") for _ in range(N)), "k": rng.randint(0, 50)}
