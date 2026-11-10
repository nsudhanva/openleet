"""Unique Number of Occurrences at n = 1000: counts built as 1, 2, 3, ... (all unique) or with
one collision."""

SEEDS = 2
N = 1000


def generate(rng):
    collide = rng.random() < 0.5
    values = rng.sample(range(-1000, 1001), 60)
    arr = []
    count = 1
    for v in values:
        if len(arr) + count > N:
            break
        arr.extend([v] * count)
        count += 1
    if collide:
        # Duplicate one existing count with a fresh value.
        fresh = next(v for v in values if v not in arr)
        arr.extend([fresh] * min(rng.randint(1, count - 1), N - len(arr)))
    rng.shuffle(arr)
    return {"arr": arr}
