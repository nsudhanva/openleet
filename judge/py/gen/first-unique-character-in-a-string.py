"""First Unique Character at 10^5 letters: every letter repeated except one near the end, or no
unique letter at all."""

SEEDS = 3
N = 10**5


def generate(rng):
    alpha = list("abcdefghijklmnopqrstuvwxyz")
    rng.shuffle(alpha)
    lone, rest = alpha[0], alpha[1 : rng.randint(2, 26)]
    s = [rng.choice(rest) for _ in range(N - 1)]
    for i, ch in enumerate(rest):  # every repeated letter appears at least twice
        s[2 * i] = s[2 * i + 1] = ch
    if rng.random() < 0.67:
        s.insert(rng.randrange(N - 50, N), lone)
    else:
        s.append(s[0])
    return {"s": "".join(s)}
