"""3 * 10^4 low peaks at distinct x, a few repeated and a few under tall mountains, so about
half the peaks are visible and checking each against every other mountain costs ~5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
LIMIT = 10**5


def generate(rng):
    tall = rng.randint(5, 20)
    twins = rng.randint(50, 200)
    xs = rng.sample(range(1, LIMIT + 1), N - tall - twins)
    peaks = [[x, rng.randint(1, 3)] for x in xs]
    # Identical copies hide each other; tall mountains hide the low peaks near them.
    peaks += [list(rng.choice(peaks)) for _ in range(twins)]
    peaks += [[rng.randint(1, LIMIT), rng.randint(100, 2000)] for _ in range(tall)]
    rng.shuffle(peaks)
    return {"peaks": peaks}
