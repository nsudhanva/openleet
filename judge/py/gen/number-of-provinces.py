"""Number of Provinces at n = 200: either many small provinces or a few large dense ones."""

SEEDS = 2
N = 200


def generate(rng):
    groups = rng.choice([rng.randint(30, 80), rng.randint(1, 5)])
    label = [rng.randrange(groups) for _ in range(N)]
    density = rng.choice([0.05, 0.5])
    m = [[0] * N for _ in range(N)]
    for i in range(N):
        m[i][i] = 1
        for j in range(i + 1, N):
            if label[i] == label[j] and rng.random() < density:
                m[i][j] = m[j][i] = 1
    return {"isConnected": m}
