"""Maximum Value after Insertion at the maximum length 10^5, positive on seed 0 and negative on
seed 1: a long run of the digit x, then the only better spot near the end, so building and
comparing every insertion point costs ~2 * 10^10 character moves."""

SEEDS = 2
N = 10**5


def generate(rng):
    # The first draw is 0.84 for seed 0 and 0.13 for seed 1, so the seeds take both signs.
    negative = rng.random() < 0.5
    x = rng.randint(2, 8)
    size = N - 1 if negative else N
    run = size * 9 // 10
    # A positive n takes x before its first digit below x, a negative one before its first digit
    # above x: `pas` digits let the scan pass, `stop` ends it near the end. Inserting anywhere in
    # the run of x gives one string, and the digit after the run makes that string worse.
    low, high = range(1, x), range(x + 1, 10)
    pas, stop, after_run = (range(1, x + 1), high, low) if negative else (range(x, 10), low, high)
    rest = [rng.choice(pas) for _ in range(size - run)]
    rest[0] = rng.choice(after_run)
    rest[rng.randrange(len(rest) // 2, len(rest) - 1)] = rng.choice(stop)
    body = str(x) * run + "".join(map(str, rest))
    return {"n": "-" + body if negative else body, "x": x}
