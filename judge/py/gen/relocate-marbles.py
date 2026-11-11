"""Relocate Marbles at 10^4 marbles and 10^4 moves, so rewriting the marble list on each move costs
~10^8 steps."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    spread = rng.choice((N // 2, LIMIT))
    nums = [rng.randint(1, spread) for _ in range(N)]
    occupied = list(set(nums))
    occupied.sort()
    rng.shuffle(occupied)
    where = {p: i for i, p in enumerate(occupied)}
    move_from, move_to = [], []
    for _ in range(N):
        f = occupied[rng.randrange(len(occupied))]
        t = rng.randint(1, spread)
        move_from.append(f)
        move_to.append(t)
        if t == f:
            continue
        i = where.pop(f)
        last = occupied.pop()
        if last != f:
            occupied[i] = last
            where[last] = i
        if t not in where:
            where[t] = len(occupied)
            occupied.append(t)
    return {"nums": nums, "moveFrom": move_from, "moveTo": move_to}
