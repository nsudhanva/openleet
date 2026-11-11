"""Maximum Number of Operations With the Same Score II on 400 equal values with a few different
ones, so all three moves stay open and the unmemoised search cannot finish."""

SEEDS = 2
N = 400


def generate(rng):
    v = rng.randint(1, 500)
    nums = [v] * N
    for i in rng.sample(range(N // 4, 3 * N // 4), rng.randint(1, 3)):
        nums[i] = v + rng.randint(1, 500)
    return {"nums": nums}
