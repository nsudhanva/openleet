"""Largest Element in an Array After Merge Operations at n = 10^5: n / 2 small values that
all merge, before a strictly decreasing tail of n / 2 large ones, so a simulation that rescans
from the right (or pops from the list) after each merge walks the whole tail every time,
~2.5 * 10^9 steps."""

SEEDS = 2
N = 10**5
LIMIT = 10**6


def generate(rng):
    tail_len = N // 2
    step = LIMIT // 2 // tail_len
    tail, v = [], LIMIT
    for _ in range(tail_len):
        tail.append(v)
        v -= rng.randint(1, step)
    # Mostly rising, so nearly every small value merges into the run on its right.
    head = [rng.randint(1, LIMIT // 2) for _ in range(N - tail_len)]
    head.sort()
    for _ in range(len(head) // 20):
        i = rng.randrange(len(head) - 1)
        head[i], head[i + 1] = head[i + 1], head[i]
    return {"nums": head + tail}
