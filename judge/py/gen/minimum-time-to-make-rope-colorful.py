"""Minimum Time to Make Rope Colorful at n = 10^5: 6 * 10^4 balloons with no equal neighbours,
then runs of one colour up to 2000 long, so removing one balloon at a time and rescanning from
the start is ~2.4 * 10^9 steps."""

SEEDS = 2
N = 10**5
PLAIN = 6 * 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    colors = [rng.choice(LETTERS)]
    while len(colors) < PLAIN:
        c = rng.choice(LETTERS)
        if c != colors[-1]:
            colors.append(c)
    while len(colors) < N:
        colors += [rng.choice(LETTERS)] * rng.randint(1, 2000)
    colors = colors[:N]
    return {"colors": "".join(colors), "neededTime": [rng.randint(1, 10**4) for _ in range(N)]}
