"""Maximum Increasing Triplet Value at n = 2 * 10^4 over [1, 10^9], so scanning the left side for
each middle element's best smaller value is 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    nums = [rng.randint(1, LIMIT) for _ in range(N)]
    # Guarantee a triplet: an increasing run of three at a random place.
    i = rng.randrange(N - 2)
    nums[i : i + 3] = sorted(rng.sample(range(1, LIMIT + 1), 3))
    return {"nums": nums}
