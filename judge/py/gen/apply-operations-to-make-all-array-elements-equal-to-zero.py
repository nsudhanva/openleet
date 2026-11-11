"""Apply Operations to Make All Array Elements Equal to Zero at n = 2 * 10^4 with k = n / 2:
a sum of random window counts (answer true), or the same with the last element raised by k
(false only at the end, with the sum still a multiple of k), so subtracting each window element
by element is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    k = N // 2 + rng.randint(-N // 20, N // 20)
    top = 10**6 // k
    counts = [rng.randint(0, top) for _ in range(N - k + 1)]
    nums, run = [], 0
    for i in range(N):
        run += (counts[i] if i < len(counts) else 0) - (counts[i - k] if i >= k else 0)
        nums.append(run)
    if rng.random() < 0.5:
        nums[-1] += k
    return {"nums": nums, "k": k}
