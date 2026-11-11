"""Find Good Days to Rob the Bank at n = 10^5 with time ~ n / 4: all-equal guards, or a long
valley with plateaus, so checking each day's two windows directly is ~10^9 comparisons."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        security = [rng.randint(0, 10**5)] * N
    else:
        # Non-increasing to a random bottom, then non-decreasing, both mostly flat.
        bottom = rng.randrange(N // 3, 2 * N // 3)
        security, v = [], 10**5
        for _ in range(bottom):
            security.append(v)
            if rng.random() < 0.3:
                v = max(0, v - rng.randint(0, 3))
        for _ in range(N - bottom):
            security.append(v)
            if rng.random() < 0.3:
                v = min(10**5, v + rng.randint(0, 3))
    return {"security": security, "time": rng.randint(N // 5, N // 3)}
