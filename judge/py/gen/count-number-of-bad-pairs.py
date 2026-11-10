"""Count Number of Bad Pairs at n = 10^5: random values, or nums[i] - i nearly constant so the
~5 * 10^9 pair count needs big integers and a quadratic scan is hopeless."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 10**9) for _ in range(N)]
    else:
        offsets = [rng.randint(1, 10**6) for _ in range(5)]
        nums = [i + rng.choice(offsets) for i in range(N)]
    return {"nums": nums}
