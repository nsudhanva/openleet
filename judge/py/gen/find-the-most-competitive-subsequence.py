"""Find the Most Competitive Subsequence at n = 10^5 with k near n / 2 on a noisy rising
sequence, so each window's minimum sits near its start and taking the minimum of every
remaining window is ~2.5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    step = rng.choice((10, 1000))
    noise = rng.choice((3, 15)) * step // 10
    nums = [i * step + rng.randint(0, noise) for i in range(N)]
    return {"nums": nums, "k": rng.randint(N * 2 // 5, N * 3 // 5)}
