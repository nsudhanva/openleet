"""Cheapest Flights Within K Stops at n = 100 with up to the maximum 4950 flights: a cheap
chain through every city from src to dst hidden among expensive shortcuts, so the answer
depends on k, and Bellman-Ford style relaxation runs at full size."""

from itertools import pairwise

SEEDS = 3
N = 100


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    chain = list(pairwise(order))
    taken = set(chain)
    others = [(a, b) for a in range(N) for b in range(N) if a != b and (a, b) not in taken]
    count = rng.choice([N * (N - 1) // 2, 1000])
    extra = rng.sample(others, count - len(chain))
    flights = [[a, b, rng.randint(1, 10)] for a, b in chain]
    flights += [[a, b, rng.randint(5000, 10**4)] for a, b in extra]
    rng.shuffle(flights)
    k = rng.choice([rng.randint(0, N - 1), N - 1, rng.randint(0, 5)])
    return {"n": N, "flights": flights, "src": order[0], "dst": order[-1], "k": k}
