"""Alternating Groups II at n = 10^5: a fully alternating circle with k between n / 3 and 2n / 3
(checking each start's k tiles is ~5 * 10^9 steps), or alternating runs of length ~1000 with
k ~ 800 (~5 * 10^7), or of length ~30 with k ~ 25, ~3000 breaks (every break against every
start is ~10^8)."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
RUNS = (1000, 30)


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        colors = [i % 2 for i in range(N)]
        k = rng.randint(N // 3, 2 * N // 3)
    else:
        run = RUNS[shape - 1]
        colors, c = [], rng.randrange(2)
        while len(colors) < N:
            for _ in range(min(rng.randint(run // 2, 3 * run // 2), N - len(colors))):
                colors.append(c)
                c ^= 1
            c ^= 1  # a break: the next tile repeats this run's last color
        k = max(3, rng.randint(run * 7 // 10, run * 9 // 10))
    if rng.random() < 0.5:
        colors = [c ^ 1 for c in colors]
    return {"colors": colors, "k": k}
