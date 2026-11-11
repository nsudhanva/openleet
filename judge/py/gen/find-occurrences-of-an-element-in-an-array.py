"""Find Occurrences of an Element in an Array with 10^4 numbers, x in half of them, and 10^4
queries, nine tenths asking for an occurrence in the back half, so scanning nums per query is
~10^8 steps."""

SEEDS = 2
N = 10**4
Q = 10**4


def generate(rng):
    x = rng.randint(1, 10**4)
    nums = [x if rng.random() < 0.5 else rng.randint(1, 10**4) for _ in range(N)]
    count = nums.count(x)
    queries = [
        rng.randint(max(1, count // 2), max(1, count))
        if rng.random() < 0.9
        else rng.randint(count + 1, 10**5)
        for _ in range(Q)
    ]
    return {"nums": nums, "queries": queries, "x": x}
