"""Course Schedule III with 10^4 courses: short durations with tight, clustered deadlines, so
the greedy keeps swapping courses through its heap."""

SEEDS = 2
N = 10**4


def generate(rng):
    courses = []
    for _ in range(N):
        if rng.random() < 0.5:
            d = rng.randint(1, 10**4)
            last = rng.randint(1, 10**4)
        else:
            d = rng.randint(1, 20)
            last = rng.randint(max(1, d), 10**4)
        courses.append([d, last])
    return {"courses": courses}
