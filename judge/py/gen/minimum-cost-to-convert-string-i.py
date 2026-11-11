"""Minimum Cost to Convert String I with n = 10^5 mismatched letters and 2000 rules, so a fresh
shortest-path search over the rules for every position is about 2 * 10^8 steps."""

SEEDS = 2
N = 10**5
RULES = 2000
LIMIT = 10**6
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    # A cycle through all 26 letters keeps every conversion possible; the rest are random rules.
    cycle = list(LETTERS)
    rng.shuffle(cycle)
    original = cycle[:]
    changed = cycle[1:] + cycle[:1]
    while len(original) < RULES:
        x, y = rng.sample(LETTERS, 2)
        original.append(x)
        changed.append(y)
    cost = [rng.randint(1, LIMIT) for _ in range(RULES)]
    source, target = [], []
    for _ in range(N):
        x, y = rng.sample(LETTERS, 2)
        source.append(x)
        target.append(y)
    return {
        "source": "".join(source),
        "target": "".join(target),
        "original": original,
        "changed": changed,
        "cost": cost,
    }
