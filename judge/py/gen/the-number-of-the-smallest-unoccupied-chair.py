"""The Number of the Smallest Unoccupied Chair at n = 10^4: most friends stay to the end and the
target arrives last, so scanning the chairs for each arrival is ~5 * 10^7 steps."""

SEEDS = 2
N = 10**4
T = 10**5


def generate(rng):
    arrivals = sorted(rng.sample(range(1, T // 2), N))
    times = []
    for a in arrivals:
        if rng.random() < 0.9:
            times.append([a, rng.randint(T - 100, T)])
        else:
            times.append([a, rng.randint(a + 1, min(T, a + 2000))])
    order = list(range(N))
    rng.shuffle(order)
    times = [times[i] for i in order]
    return {"times": times, "targetFriend": order.index(N - 1)}
