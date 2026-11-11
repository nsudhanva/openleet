"""Number of Flowers in Full Bloom at 2 * 10^4 flowers and 2 * 10^4 people, half arriving on a
bloom's first or last day, so checking every flower for every person costs 4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**9


def generate(rng):
    flowers = []
    for _ in range(N):
        start = rng.randint(1, TOP)
        flowers.append([start, min(TOP, start + rng.randint(0, 10**8))])
    people = []
    for _ in range(N):
        if rng.random() < 0.5:
            people.append(rng.choice(rng.choice(flowers)))
        else:
            people.append(rng.randint(1, TOP))
    return {"flowers": flowers, "people": people}
