"""Make Array Non-decreasing at n = 5 * 10^4: values that climb slowly through noise, so taking
the prefix maximum afresh for every element is ~10^9 comparisons."""

SEEDS = 2
N = 5 * 10**4
TOP = 2 * 10**5


def generate(rng):
    nums = []
    for i in range(N):
        base = TOP * i // N
        nums.append(min(TOP, max(1, base + rng.randint(-TOP // 50, TOP // 100))))
    return {"nums": nums}
