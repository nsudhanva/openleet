"""Number Container System with 5.2 * 10^4 calls: 3.3 * 10^4 indices filled with one number, then
changes that move its smallest index to another number (or 2.6 * 10^4 indices, then mostly finds),
so taking the minimum index whenever it leaves, or on every find, costs ~3 * 10^8 steps."""

import heapq

from _shapes import pick_shape

SEEDS = 3
CALLS = 52000
FILL = 33000  # drop-heavy shapes; the find-heavy shape fills half the calls


def generate(rng):
    shape = pick_shape(rng)
    fill = CALLS // 2 if shape == 2 else FILL
    ask, aim = (0.9, 0.5) if shape == 2 else (0.03, 0.98)
    # Small numbers keep the JSON short; indices must be distinct, so they stay ~5 digits.
    number = rng.randint(1, 100)
    others = rng.sample([x for x in range(1, 101) if x != number], 50)
    indices = rng.sample(range(1, 10**5 + 1), fill)
    ops, args = ["NumberContainers"], [[]]
    owner = {}
    for i in indices:
        owner[i] = number
        ops.append("change")
        args.append([i, number])
    heap = sorted(indices)  # the number's indices; stale ones are skipped at the top

    def smallest():
        while heap and owner[heap[0]] != number:
            heapq.heappop(heap)
        return heap[0] if heap else None

    for _ in range(CALLS - fill):
        if rng.random() < ask:
            ops.append("find")
            args.append([number if rng.random() < 0.95 else rng.choice(others)])
            continue
        top = rng.random() < aim
        i = smallest() if top else None
        if i is None:  # a random index; or the number holds none (only in tiny tests)
            i = rng.choice(indices)
        target = rng.choice(others) if top or owner[i] == number else number
        owner[i] = target
        if target == number:
            heapq.heappush(heap, i)
        ops.append("change")
        args.append([i, target])
    return {"ops": ops, "args": args}
