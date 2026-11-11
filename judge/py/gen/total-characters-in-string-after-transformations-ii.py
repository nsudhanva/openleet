"""Total Characters in String After Transformations II at 1000 letters and t of 10^8 to 10^9, so
applying the transformation one step at a time is over 10^10 steps."""

SEEDS = 2
N = 1000


def generate(rng):
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(N))
    nums = [rng.randint(1, 25) for _ in range(26)]
    return {"s": s, "t": rng.randint(10**8, 10**9), "nums": nums}
