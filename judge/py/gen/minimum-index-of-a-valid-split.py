"""Minimum Index of a Valid Split at n ~ 10^5: the dominant value is thin at the front and packed
at the back, so the first valid split is within a few hundred of the end (or there is none) and
recounting both sides at every split is ~10^10 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    n = N - 1 if shape == 1 else N
    # Shape 0: the first valid split is n - 2; 1: none; 2: a few hundred before the end.
    count = (n + 1) // 2 if shape == 1 else n // 2 + 1
    if shape == 2:
        count += rng.randint(n // 2000, n // 300)
    tail = 2 * n // 5
    x = rng.randint(1, 1000)
    others = [v for v in range(1, 1001) if v != x]
    head = [x] * (count - tail) + [rng.choice(others) for _ in range(n - count)]
    rng.shuffle(head)
    # The front stays non-dominant: no prefix of the head has x as half or more of it.
    seen = 0
    for i, v in enumerate(head):
        seen += v == x
        if 2 * seen >= i + 1:
            j = next(k for k in range(len(head) - 1, i, -1) if head[k] != x)
            head[i], head[j] = head[j], head[i]
            seen -= 1
    return {"nums": head + [x] * tail}
