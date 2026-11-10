"""Maximum Vowels in a Substring of Length k at length 10^5 with mid-sized k, where recounting
each window is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    alphabet = rng.choice(["abcdefghijklmnopqrstuvwxyz", "aeioubc"])
    s = "".join(rng.choice(alphabet) for _ in range(N))
    return {"s": s, "k": rng.choice([N // 2, rng.randint(1, N)])}
