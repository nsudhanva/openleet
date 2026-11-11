"""Divide Players Into Teams of Equal Skill at n = 10^5 where every pair does sum to the same
total, so finding each partner by a linear search takes ~2.5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    total = rng.randint(800, 1200)
    skill = []
    for _ in range(N // 2):
        a = rng.randint(max(1, total - 1000), min(1000, total - 1))
        skill += [a, total - a]
    rng.shuffle(skill)
    return {"skill": skill}
