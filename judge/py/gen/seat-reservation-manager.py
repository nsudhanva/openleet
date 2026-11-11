"""Seat Reservation Manager with n = 10^5 and 10^5 calls: 3 * 10^4 reserves, 2 * 10^4 unreserves
of random seats in the upper part of them, then 2.5 * 10^4 reserve/unreserve pairs, so about
2 * 10^4 freed seats stay pending and taking the smallest by scanning the seats or the freed set
costs ~10^4 to 2 * 10^4 steps per reserve."""

from heapq import heapify, heappop, heappush

SEEDS = 2
N = 10**5
FIRST = 3 * 10**4
FREED = 2 * 10**4
PAIRS = 25000


def generate(rng):
    ops, args = ["SeatManager"], [[N]]
    low = FIRST // 4
    pool = list(range(low + 1, FIRST + 1))  # reserved seats that may be unreserved
    ops += ["reserve"] * FIRST
    args += [[]] * FIRST
    freed = []
    for _ in range(FREED):
        j = rng.randrange(len(pool))
        pool[j], pool[-1] = pool[-1], pool[j]
        freed.append(pool.pop())
        ops.append("unreserve")
        args.append([freed[-1]])
    heapify(freed)
    for _ in range(PAIRS):
        pool.append(heappop(freed))
        ops.append("reserve")
        args.append([])
        j = rng.randrange(len(pool))
        pool[j], pool[-1] = pool[-1], pool[j]
        seat = pool.pop()
        heappush(freed, seat)
        ops.append("unreserve")
        args.append([seat])
    return {"ops": ops, "args": args}
