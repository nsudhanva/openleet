"""Find Servers That Handled Most Number of Requests: in two seeds the first k = 10^4 of
4 * 10^4 requests pin all but a few servers, so walking from i % k is ~k / 2 steps each; in the
third, k = n = 8 * 10^4 with odd servers pinned and the rest churning, so the free set is big."""

from _shapes import pick_shape

SEEDS = 3
K = 10**4
N = 4 * 10**4
CHURN = 8 * 10**4


def generate(rng):
    if pick_shape(rng) == 2:
        arrival, t = [], 0
        for _ in range(CHURN):
            t += rng.randint(1, 2)
            arrival.append(t)
        load = [10**6 if i % 2 else rng.randint(1, 4000) for i in range(CHURN)]
        return {"k": CHURN, "arrival": arrival, "load": load}
    free = set(rng.sample(range(K), rng.randint(1, 3)))
    arrival, t = [], 0
    for _ in range(N):
        t += rng.randint(1, 5)
        arrival.append(t)
    # Requests to a free server finish before the next arrival; the rest hold theirs forever.
    load = [1 if i >= K or i in free else 10**9 for i in range(N)]
    return {"k": K, "arrival": arrival, "load": load}
