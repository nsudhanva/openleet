"""Student Attendance Record II at n near 10^5, the size that breaks memoized recursion
and anything super-linear."""

SEEDS = 2


def generate(rng):
    return {"n": rng.choice([10**5, rng.randint(9 * 10**4, 10**5)])}
