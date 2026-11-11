"""Minimum Number of Operations to Make Array Empty at n = 8 * 10^4: about 27,000 distinct
values, each two to four times, so counting each distinct value with a full scan is ~2 * 10^9
comparisons."""

SEEDS = 2
N = 8 * 10**4


def generate(rng):
    counts, total = [], 0
    while N - total > 4:
        counts.append(rng.randint(2, 4))
        total += counts[-1]
    if N - total == 1:
        counts[-1] += 1
    elif total < N:
        counts.append(N - total)
    values = rng.sample(range(1, 10**6 + 1), len(counts))
    nums = [v for v, c in zip(values, counts, strict=True) for _ in range(c)]
    rng.shuffle(nums)
    return {"nums": nums}
