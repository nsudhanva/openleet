"""K Closest Points at the maximum 10^4 points in [-10^4, 10^4]^2 with k just below n, where the
k-th and (k+1)-th distances differ so the answer set is unique; picking the nearest point k times
does ~5 * 10^7 distance checks."""

SEEDS = 2
N = 10**4
LIMIT = 10**4
SLACK = 100


def generate(rng):
    span = rng.choice([LIMIT // 100, LIMIT])
    points = [[rng.randint(-span, span), rng.randint(-span, span)] for _ in range(N)]
    dist = sorted(x * x + y * y for x, y in points)
    # The k just below n whose boundary is not a tie; k = n itself always works.
    ks = [k for k in range(N - SLACK, N) if dist[k - 1] < dist[k]]
    return {"points": points, "k": rng.choice(ks) if ks else N}
