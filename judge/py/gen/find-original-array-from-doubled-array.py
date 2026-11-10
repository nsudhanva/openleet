"""Find Original Array From Doubled Array at n = 10^5: a shuffled valid doubled array (with zeros
and long doubling chains), or one with a single corrupted value."""

SEEDS = 3
N = 10**5


def generate(rng):
    half = N // 2
    if rng.random() < 0.5:
        original = [rng.randint(0, 5 * 10**4) for _ in range(half)]
    else:
        # Powers-of-two chains force the greedy to pair in the right order.
        original = [rng.choice([1, 3, 5, 0]) << rng.randint(0, 13) for _ in range(half)]
    changed = original + [2 * v for v in original]
    if rng.random() < 0.34:
        i = rng.randrange(N)
        changed[i] = changed[i] + 1 if changed[i] < 10**5 else changed[i] - 1
    rng.shuffle(changed)
    return {"changed": changed}
