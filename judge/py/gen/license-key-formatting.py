"""License Key Formatting on 10^5-character keys of letters, digits, and dashes, including
leading dashes and a key that is almost all dashes."""

SEEDS = 2
N = 10**5
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate(rng):
    if rng.random() < 0.5:
        s = "".join(rng.choice(CHARS) if rng.random() < 0.8 else "-" for _ in range(N))
    else:
        chars = ["-"] * N
        for i in rng.sample(range(N), rng.randint(1, 50)):
            chars[i] = rng.choice(CHARS)
        s = "".join(chars)
    return {"s": s, "k": rng.choice([1, rng.randint(1, 10**4)])}
