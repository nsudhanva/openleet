"""Push Dominoes at n = 10^5: long stretches of '.', so simulating one second at a time is
quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        s = ["."] * N
        s[0] = "R"
        s[-1] = "L"
        for _ in range(rng.randint(0, 5)):
            s[rng.randrange(N)] = rng.choice("LR")
    else:
        s = [rng.choice("LR") if rng.random() < 0.01 else "." for _ in range(N)]
    return {"dominoes": "".join(s)}
