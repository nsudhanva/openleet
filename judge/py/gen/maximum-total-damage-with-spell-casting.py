"""Maximum Total Damage With Spell Casting at n = 3 * 10^4: clusters 20 wide spread over
[1, 10^9] (~2.5 * 10^4 distinct damages), so a DP over every value is out of reach and scanning
every earlier distinct damage for each one costs ~3 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    bases = rng.sample(range(1, 10**9 - 20, 1000), N // 8)
    return {"power": [rng.choice(bases) + rng.randrange(20) for _ in range(N)]}
