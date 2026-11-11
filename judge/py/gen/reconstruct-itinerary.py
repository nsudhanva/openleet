"""Reconstruct Itinerary at the maximum 300 tickets: JFK's lexically first ticket leads to a hub
with ~120 loops and no way back, while the real route first tours back to JFK, so backtracking
tries every order of the loops before it backs out."""

from itertools import pairwise, product
from string import ascii_uppercase

SEEDS = 2
TICKETS = 300


def generate(rng):
    names = ["".join(p) for p in product(ascii_uppercase, repeat=3)]
    names.remove("JFK")
    tour_len = rng.randint(TICKETS // 8, TICKETS // 5)
    loops = []
    left = TICKETS - tour_len - 1
    while left >= 2:
        size = 3 if left >= 3 and rng.random() < 0.3 else 2
        loops.append(size)
        left -= size
    tour_len += left
    picked = sorted(rng.sample(names, 1 + 6 + sum(size - 1 for size in loops)))
    # The hub sorts first, so it is the lexically smallest choice out of JFK.
    hub, pool, stops = picked[0], picked[1:7], picked[7:]
    rng.shuffle(stops)
    walk = ["JFK", rng.choice(pool)]
    while len(walk) < tour_len:
        walk.append(rng.choice([p for p in pool if p != walk[-1]]))
    tickets = [[a, b] for a, b in pairwise([*walk, "JFK"])]
    tickets.append(["JFK", hub])
    for size in loops:
        route = [hub, *(stops.pop() for _ in range(size - 1)), hub]
        tickets += [[a, b] for a, b in pairwise(route)]
    rng.shuffle(tickets)
    return {"tickets": tickets}
