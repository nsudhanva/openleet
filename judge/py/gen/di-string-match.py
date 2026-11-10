"""DI String Match at length 10^5: random I/D, or long runs of one letter."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        s = "".join(rng.choice("ID") for _ in range(N))
    else:
        parts, total = [], 0
        while total < N:
            run = min(rng.randint(1000, 20000), N - total)
            parts.append(rng.choice("ID") * run)
            total += run
        s = "".join(parts)
    return {"s": s}
