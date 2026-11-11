"""Most Frequent IDs at n = 4 * 10^4 steps over ~3 * 10^4 distinct IDs (mostly additions, some
removals that keep every count non-negative), so taking the maximum over all counts after each
step is ~10^9 steps."""

SEEDS = 2
N = 4 * 10**4
IDS = 10**5


def generate(rng):
    count = {}
    nums, freq = [], []
    for _ in range(N):
        x = rng.randint(1, IDS)
        have = count.get(x, 0)
        f = (
            -rng.randint(1, min(have, 10**5))
            if have and rng.random() < 0.3
            else rng.randint(1, 10**5)
        )
        count[x] = have + f
        nums.append(x)
        freq.append(f)
    return {"nums": nums, "freq": freq}
