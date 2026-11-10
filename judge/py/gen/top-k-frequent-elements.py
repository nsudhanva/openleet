"""Top K Frequent Elements at n = 10^5 with up to all 20001 possible values in play and a strict
frequency gap at the k boundary, so the answer is unique."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    values = list(range(-(10**4), 10**4 + 1))
    rng.shuffle(values)
    if shape == 0:
        distinct, k = 20001, rng.randint(1000, 5000)
    elif shape == 1:
        distinct = 400
        k = rng.randint(1, distinct)
    else:
        distinct, k = rng.randint(2000, 20001), rng.randint(1, 50)
    # The rest get counts in [1, cap]; the top k get at least cap + 1 each.
    cap = rng.randint(1, max(1, N // distinct))
    while cap > 1 and k * (cap + 1) + (distinct - k) * cap > N:
        cap -= 1
    rest = [rng.randint(1, cap) for _ in range(distinct - k)]
    top = [cap + 1] * k
    leftover = N - sum(rest) - sum(top)
    while leftover > 0:
        add = min(leftover, rng.randint(1, 2 * leftover // k + 1))
        top[rng.randrange(k)] += add
        leftover -= add
    nums = []
    for v, c in zip(values[:distinct], top + rest, strict=True):
        nums.extend([v] * c)
    rng.shuffle(nums)
    return {"nums": nums, "k": k}
