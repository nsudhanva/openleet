"""8 * 10^4 starting numbers, the first 3 * 10^4 all paired, then 2.6 * 10^4 calls whose adds
repeat the last unique (every eighth the first), so rescanning the queue per show or removing
from a plain list of uniques costs ~4 * 10^8 steps."""

SEEDS = 2
PAIRED = 3 * 10**4
SINGLE = 5 * 10**4
CALLS = 26 * 10**3


def generate(rng):
    vals = rng.sample(range(10**4, 10**5), PAIRED // 2 + SINGLE)
    front = vals[: PAIRED // 2] * 2
    rng.shuffle(front)
    singles = vals[PAIRED // 2 :]
    ops, args = ["FirstUnique"], [[front + singles]]
    lo, hi = 0, SINGLE - 1
    for i in range(CALLS // 2):
        # Repeating the last unique makes a list of uniques scan to its end to drop it;
        # repeating the first moves the answer one place further back.
        if i % 8:
            value, hi = singles[hi], hi - 1
        else:
            value, lo = singles[lo], lo + 1
        ops += ["showFirstUnique", "add"]
        args += [[], [value]]
    return {"ops": ops, "args": args}
