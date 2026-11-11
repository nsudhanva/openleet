"""Shifting Letters II with s.length = shifts.length = 2 * 10^4 and every shift spanning about
half the string, so applying each shift letter by letter does ~2 * 10^8 updates."""

SEEDS = 2
N = 2 * 10**4
Q = 2 * 10**4


def generate(rng):
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(N))
    shifts = []
    for _ in range(Q):
        start = rng.randrange(N // 4)
        end = rng.randrange(3 * N // 4, N)
        shifts.append([start, end, rng.randrange(2)])
    return {"s": s, "shifts": shifts}
