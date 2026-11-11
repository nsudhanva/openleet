"""Auction System on one busy item: 1.2 * 10^4 bids, then 1.8 * 10^4 calls, mostly updates and
removals that lower or drop the top bid, or 1.9 * 10^4 bids then 1.9 * 10^4 calls, mostly
getHighestBidder, so rescanning the item's bids whenever the top bid falls, or on every query,
costs ~2 * 10^8 to 3 * 10^8 steps."""

import heapq

from _shapes import pick_shape

SEEDS = 3
CALLS = 3 * 10**4
FILL = 12000
MANY_CALLS = 38000
MANY_FILL = 19000
TOP = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:  # many bids, mostly queries, changes at random
        calls, fill, band = MANY_CALLS, MANY_FILL, 1000
        ask, update, remove, aim = 0.95, 0.97, 0.99, 0.0
    else:  # changes aimed at the top bid; a narrow band makes ties, broken by the larger userId
        calls, fill, band = CALLS, FILL, (1000, 10**9)[shape]
        ask, update, remove, aim = 0.2, 0.85, 0.97, 0.9
    item = rng.randint(1, TOP)
    users = rng.sample(range(1, TOP + 1), fill)
    ops, args = ["AuctionSystem"], [[]]
    bids = {}  # userId -> amount, for the busy item
    heap = []  # (-amount, -userId); stale entries are skipped at the top
    for u in users:
        bids[u] = rng.randint(1, band)
        heap.append((-bids[u], -u))
        ops.append("addBid")
        args.append([u, item, bids[u]])
    heapq.heapify(heap)
    active = list(bids)  # users with a bid, for random picks; pos finds one to swap out in O(1)
    pos = {u: k for k, u in enumerate(active)}

    def leader():
        while heap and bids.get(-heap[0][1]) != -heap[0][0]:
            heapq.heappop(heap)
        return -heap[0][1] if heap else None

    def pick(p):
        return leader() if rng.random() < p else rng.choice(active)

    def put(u, amount, op):
        bids[u] = amount
        heapq.heappush(heap, (-amount, -u))
        ops.append(op)
        args.append([u, item, amount])

    for _ in range(calls - fill):
        x = rng.random()
        if x < ask or len(active) < 2:
            ops.append("getHighestBidder")
            args.append([item if rng.random() < 0.95 else rng.randint(1, TOP)])
        elif x < update:
            u = pick(aim)
            put(u, rng.randint(1, max(1, bids[u] - 1)), "updateBid")
        elif x < remove:
            u = pick(aim * 8 / 9)
            last = active.pop()
            if last != u:
                active[pos[u]] = last
                pos[last] = pos[u]
            del pos[u], bids[u]
            ops.append("removeBid")
            args.append([u, item])
        else:
            u = rng.randint(1, TOP)
            if u not in bids:
                pos[u] = len(active)
                active.append(u)
            put(u, rng.randint(1, band), "addBid")
    return {"ops": ops, "args": args}
