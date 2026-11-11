"""Count the Number of Powerful Integers with finish near 10^15 and a short suffix s, so trying
every prefix in front of s means 10^12 or more candidates while the digit DP has a few dozen
states."""

SEEDS = 2
DIGITS = 15


def generate(rng):
    limit = rng.randint(5, 9)
    finish = rng.randint(10 ** (DIGITS - 1), 10**DIGITS)
    start = rng.randint(1, 10 ** (DIGITS // 3))
    s = str(rng.randint(1, limit)) + "".join(
        str(rng.randint(0, limit)) for _ in range(rng.randint(0, 2))
    )
    return {"start": start, "finish": finish, "limit": limit, "s": s}
