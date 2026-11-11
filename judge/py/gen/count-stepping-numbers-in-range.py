"""Count Stepping Numbers in Range with a 15-digit low and a 40-digit high, so listing the ~10^12
stepping numbers in between is hopeless while the digit DP has a few thousand states."""

SEEDS = 2
LOW = 15
HIGH = 40


def generate(rng):
    low = str(rng.randint(1, 9)) + "".join(str(rng.randrange(10)) for _ in range(LOW - 1))
    high = str(rng.randint(1, 9)) + "".join(str(rng.randrange(10)) for _ in range(HIGH - 1))
    return {"low": low, "high": high}
