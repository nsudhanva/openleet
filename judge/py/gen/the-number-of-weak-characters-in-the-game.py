"""The Number of Weak Characters in the Game at n = 2 * 10^4, mostly a staircase where no one
dominates anyone, so checking every character against every other is ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    attack = rng.sample(range(1, 10**5 + 1), N)
    defense = sorted(rng.sample(range(1, 10**5 + 1), N), reverse=True)
    pairs = sorted(attack)
    props = [[a, d] for a, d in zip(pairs, defense, strict=True)]
    for _ in range(rng.randint(10, 100)):
        props[rng.randrange(N)][1] = rng.randint(1, 10**5)
    rng.shuffle(props)
    return {"properties": props}
