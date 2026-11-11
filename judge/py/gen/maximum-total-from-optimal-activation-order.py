"""Maximum Total from Optimal Activation Order at n = 6 * 10^4 split into six groups of ~10^4
sharing a limit in [n / 20, n / 5], so taking each group's best values by repeated maximum
costs ~5 * 10^8 steps."""

SEEDS = 2
N = 6 * 10**4
GROUPS = 6


def generate(rng):
    limits = rng.sample(range(max(1, N // 20), N // 5 + 1), GROUPS)
    return {
        "value": [rng.randint(1, 10**5) for _ in range(N)],
        "limit": [rng.choice(limits) for _ in range(N)],
    }
