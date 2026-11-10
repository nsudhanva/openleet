"""Remove K Digits at length 10^5: an ascending-then-descending number or one with many zeros
behind the leading digit, so naive repeated scans are quadratic and leading zeros matter."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.choice(["mountain", "zeros", "random"])
    if shape == "mountain":
        up = sorted(rng.randint(1, 9) for _ in range(N // 2))
        num = up + sorted((rng.randint(0, 9) for _ in range(N - N // 2)), reverse=True)
    elif shape == "zeros":
        num = [rng.randint(1, 9)] + [
            0 if rng.random() < 0.7 else rng.randint(1, 9) for _ in range(N - 1)
        ]
    else:
        num = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(N - 1)]
    k = rng.randint(N // 4, 3 * N // 4)
    return {"num": "".join(map(str, num)), "k": k}
