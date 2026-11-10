"""K Closest Points at 10^4 points in [-10^4, 10^4]^2, with k chosen where the k-th and
(k+1)-th distances differ so the answer set is unique."""

SEEDS = 3
N = 10**4


def generate(rng):
    span = rng.choice([30, 10**4])
    points = [[rng.randint(-span, span), rng.randint(-span, span)] for _ in range(N)]
    dist = sorted(x * x + y * y for x, y in points)
    while True:
        k = rng.choice([1, N, rng.randint(1, N)])
        if k == N or dist[k - 1] < dist[k]:
            return {"points": points, "k": k}
