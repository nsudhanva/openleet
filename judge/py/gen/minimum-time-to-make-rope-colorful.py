"""Minimum Time to Make Rope Colorful at n = 10^5: 6 * 10^4 balloons with no equal neighbours,
then runs of one colour up to 20000 long, so removing one balloon at a time (rescanning the run
or the whole rope for the cheapest) is quadratic in the run length, ~10^9 steps or more."""

SEEDS = 2
N = 10**5
PLAIN = 6 * 10**4
RUN = 20000
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    colors = [rng.choice(LETTERS)]
    while len(colors) < PLAIN:
        c = rng.choice(LETTERS)
        if c != colors[-1]:
            colors.append(c)
    while len(colors) < N:
        colors += [rng.choice(LETTERS)] * rng.randint(1, RUN)
    colors = colors[:N]
    return {"colors": "".join(colors), "neededTime": [rng.randint(1, 10**4) for _ in range(N)]}
