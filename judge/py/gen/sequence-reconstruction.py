"""Sequence Reconstruction at n = 10^4: overlapping chunks of nums fix every adjacent pair
(except the last pair on one seed), so a topological sort that rescans all nodes for the next
zero in-degree one runs ~n steps of O(n) each."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
EXTRA = 1000


def generate(rng):
    shape = pick_shape(rng)
    nums = list(range(1, N + 1))
    rng.shuffle(nums)
    gap = shape == 1
    longest = 400 if shape == 2 else 40
    last = N - 2 if gap else N - 1
    seqs = set()
    i = 0
    while i < last:
        j = min(last, i + rng.randint(1, longest))
        seqs.add(tuple(nums[i : j + 1]))
        i = j
    if gap:
        seqs.add((nums[N - 3], nums[N - 1]))
    pool = nums[: N - 1] if gap else nums
    for _ in range(EXTRA):
        idx = sorted(rng.sample(range(len(pool)), rng.randint(1, min(40, len(pool)))))
        seqs.add(tuple(pool[t] for t in idx))
    sequences = [list(s) for s in seqs]
    rng.shuffle(sequences)
    return {"nums": nums, "sequences": sequences}
