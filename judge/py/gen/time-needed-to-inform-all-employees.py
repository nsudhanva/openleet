"""Time Needed to Inform All Employees at n = 4 * 10^4: a deep thin hierarchy (a long chain with
short side branches), so walking up to the head from every employee is ~7 * 10^8 steps."""

SEEDS = 2
N = 4 * 10**4


def generate(rng):
    label = rng.sample(range(N), N)
    parent = [-1] * N
    for i in range(1, N):
        parent[i] = i - 1 if rng.random() < 0.9 else rng.randrange(max(0, i - 50), i)
    has_kids = [False] * N
    for i in range(1, N):
        has_kids[parent[i]] = True
    manager = [0] * N
    inform = [0] * N
    for i in range(N):
        manager[label[i]] = -1 if i == 0 else label[parent[i]]
        inform[label[i]] = rng.randint(0, 1000) if has_kids[i] else 0
    return {"n": N, "headID": label[0], "manager": manager, "informTime": inform}
